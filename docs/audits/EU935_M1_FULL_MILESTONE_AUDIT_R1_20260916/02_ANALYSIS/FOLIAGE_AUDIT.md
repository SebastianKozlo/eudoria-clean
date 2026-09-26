# FOLIAGE AUDIT - EU935-M1

PE-MASTER in-session audit content, persisted verbatim (formatted; no content
changes).

## RECOVERED MECHANISM (CONFIRMED)

- Loader registration FUN_0041dae0 + ArkVegetationClimateFactory @0x00420007.
- 45 ArkVegetation* RTTI classes.
- VCL: 32 files / 492 rows / 256 ids (255/256 resolve in Models.bnt; the 1
  unresolved = 10136, recorded).
- Grid / cell-record / spawn-loop / RNG arithmetic BYTE-LOCKED (iter035):
  76/76 bit-exact; 463,141 platform samples, 0 mismatches; exhaustive domain
  proofs 32768 rand01 + 65536 u16 + 7x32768 lerp/scale.

## NOT RECOVERED (historical inputs)

- Cell byte-stream content (the RECONSTRUCTION-ONLY stand-in).
- Per-location climate selection ([P-CLIMATE]).
- Historical placement / content - FOLIAGE IS NOT 1:1 and no standing
  document claims it (verified in this audit: V4 rows 10/19 carry
  RECONSTRUCTION-ONLY labels).

## CONTRACT CONSEQUENCE

Missing historical inputs do NOT violate the M1 closure contract (the V4.1
matrix honestly bounds them; Gate A terminal state satisfied by the
cellstream exhaustive negatives).
