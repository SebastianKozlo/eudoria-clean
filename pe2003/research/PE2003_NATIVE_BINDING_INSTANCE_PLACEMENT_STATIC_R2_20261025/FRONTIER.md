# FRONTIER — exact next static edges after R2

RUN_ID: PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025 | Authoring: 2026-10-25T11:18:13Z
Sources: J03/J04 coverage_and_limits + P02 what_would_close_it + P01 OPEN edge + J01b/J02 honest limits. Machine-readable form: BACKLOG.json (BLK-R2-01..10). 100% static edges only (no runtime proposals; the human's runtime job is independent).

## Decisive edge (highest value)

**BLK-R2-01 — registry+0x3C ctor chain / FUN_00468980.** The GCE-side instance tree's parent ([registry+0x3C], AddChild @0x502ff3–0x502ffe) has an unpinned ctor/vtable (FUN_00468980 chain, NOFN region, not followed; registry pre-built — GCE ctor FUN_004892a0 takes [GCE+0x5C] as a parameter). If owner+0x1C (or the [X+8] NIF root) is, or is under, the registry+0x3C tree, the network→model instance join closes statically; otherwise the two scene systems are root-disjoint. This single edge decides the STILL_AMBIGUOUS verdict.

## Supporting edges

- **BLK-R2-02 — FUN_00403e80 arg provenance.** owner+0x1C stores FUN_00403e80(arg) of an unidentified cursor-array class ([this+0x34] object array, [this+0x68] id array, [this+0x74] cursor); 190 indirect [reg+0x10] call sites — bounded provenance walk with denominators, not a blind sweep.
- **BLK-R2-03 — binder-patched HOSTCALL case ids 4652/4653.** Runtime data at bind time, but the static residual is the HOSTCALL case-id registration table consumed by dispatcher 0x441df0 (case-space 0x7fffec7a–0x7fffec7f is known; the 4508/4057 HOSTCALL slots 3008/364/220/2124/128 need their case resolutions).
- **BLK-R2-04 — ctx+0x50 append method** (FUN_005b71e0 parse context). arr[0]=block-0 holds under both interpretations (J03 coverage note) — low priority, not load-bearing.
- **BLK-R2-05 — 0x5E6E10/0x5E7378 create-fn mapping** (two of the 13 family vtables with no direct body-scan hit; deeper ctor chains).
- **BLK-R2-06 — 4508 literal @0x5bcfe5** — the ONLY file-wide LE32 occurrence of 4508, outside the chain; struct-offset probe of the enclosing function/operand.
- **BLK-R2-07 — owner-class block-type dispatch via the type registry** (0x61Exxx global slot → factory map; P01's OPEN edge on the NIF_FILE_LOCAL classification).
- **BLK-R2-08 — native DYN dispatch caller** (which native code queries f1=1617/1611 on a 4508/4057 instance and forwards the id toward FUN_0051F6E0; reference-reachability walk from FUN_00452860 callers over [+0x2c] DYN lists).
- **BLK-R2-09 — 0xFC transform-stream drain beyond FUN_00506e10** (inherited R1 T3-d2; may require runtime — flagged honestly).
- **BLK-R2-10 — f1 property-id semantics (1611/1617) and the +1 sibling pairing (296446/218758)** — corpus-wide f1 census would characterize the property space.

## What would close the standing verdicts

- INSTANCE join STILL_AMBIGUOUS → resolved by BLK-R2-01 (+02/03); a negative result (root-disjoint) would equally be a finding.
- SOURCE_UNKNOWN → only a proven join plus recovered values could change it; no static edge currently promises authentic world values for 296445/218757 (the NIF files carry none; the network channel values are runtime data).
