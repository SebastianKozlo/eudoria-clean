# ITER-022 (Gate C, loop iter036) — .tez d-field ~20xxx id-space join vs templates.vfs / hierarchy.vfs

Session: 2026-09-04 12:30 physical. Charter PE_WORLD_SURFACE_FIDELITY_R1 (Gate C).
Data-level forensics only; all originals read-only; both eras labeled
(PCG_9_3_5 install + JUL-2003 corpus).

## Question

Does the `.tez` d-field ~20xxx id space (20068–20641, west-clustered; iter018
lead) join with the templates.vfs / hierarchy.vfs id spaces?

## Sources (SHA-verified)

- templates.vfs: PCG BE57818C... (560,788 B, 3,435 records) / JUL DDE352A9... (553,660 B, 3,065 records)
- hierarchy.vfs: PCG D9EFE06E... (7,055 tagged records) / JUL 1B2596CE... (6,946 tagged records)
- TerrainEditZones.bnt: JUL (1,015 records) / PCG (1,020 records)

## Result (explicit denominators)

- d-field ~20xxx distinct values: 7 (identical in both eras):
  20068, 20069, 20070, 20071, 20095, 20111, 20641 — carried by 233 records
  in both eras; value set and per-value counts are ERA-INVARIANT.
- Join vs templates record ids (3,065/3,435): 0/7.
- Join vs hierarchy value space (6,932/7,041): 0/7; zero raw byte occurrences.
- Join vs templates A-field / C-field / sub-record ids: 0/7.
- Join vs templates B-field resource space: 1/7 — 20070 == B(template 1969).

## The single byte-proven crossing

templates.vfs record 1969 (72-B single-block, byte-identical across eras):
`[1969][28][1][hash][1969][A=7353][B=20070][C=0][f32 1.77875]`
Hierarchy path 383→385→460→461→1969; node 461 hosts a 39-template family with
2xxxx–3xxxx B-resources (consecutive run 1968:19616, 1969:20070, 1970:20084,
1971:20203), era-stable.

## Verdicts (identity/operation/role split)

- d 20xxx vs templates record ids: NO JOIN — CONFIRMED.
- d 20xxx vs hierarchy values: NO JOIN — CONFIRMED.
- d=20070 == B(template 1969): occurrence CONFIRMED; shared-resource-space
  hypothesis PLAUSIBLE only (1/7 overlap, coincidence not excluded); final
  semantic role of d and B: UNVERIFIED (no consumer evidence).
- Era-diff templates JUL vs PCG: 3,064 common ids, 371 added, 1 removed
  (15646), 50 changed (extent-hash method, record granularity).
- sids.vfs control: sid id space 1..4214 — 0/7; the ~20xxx family is not the
  sid record-id space.

## Open lead

The 2xxxx numeric family spans 20001..20043.vfs parameter files, 24007.vfs
(Amethera zones), template B-space 2xxxx–3xxxx run, ArkScript chat slots
~20064–20068, and .tez d 20068–20641 — a cross-container parameter-resource
id space is PLAUSIBLE but needs consumer evidence (PE 9.3.5 RE path) before
any semantics claim.

Evidence: 99_Audits/PE_MILESTONE_1_WORLD_SURFACE_R1/03_EVIDENCE/iter022_*
(11 artifacts, SHA256 recorded in the session report and M1_LEDGER.md).
