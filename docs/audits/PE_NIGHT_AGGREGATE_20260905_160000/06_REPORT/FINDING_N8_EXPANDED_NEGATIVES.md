# FINDING N-8 — THE EXPANDED CELLSTREAM NEGATIVES (the full-corpus grid scan)

**RUN**: the missed-night item #4 — the grid-shape scan over ALL the local 9.3.5
containers (completing RUN-4's Parameters/Textures-only scan).

## THE SCAN

26 containers / 179,774 BNT entries walked (Models, Terrain, Textures, Volumes,
Portals, Sounds, EffectSequences, UI, etc. — the full pcg_install\Data tree);
the targets: the 65x65 climate grid (4,225 B) + the 129x129 detail grids (16,641 B)
+ the raw/16/18/12-byte-header variants.

## THE RESULT

**70 size-coincidence "hits" — ZERO grid data.** All the hits are zlib-COMPRESSED
TDFs in terrain.bnt whose packed sizes land at 4,225-4,243 B (a ~0.04% coincidence
rate over 179,774 entries — the expected tail of the compressed-size distribution),
plus one Models.bnt NIF at 4,237. A compressed stream at a grid-shaped SIZE is not
a raw byte grid; no uncompressed 65x65/129x129 world-data grid exists locally.

## THE VERDICT

**The RUN-4 BLOCKED-UNKNOWN stands, now with the EXHAUSTIVE local negative**:
Parameters 0/27 + Textures 0/8,381 + the 12-byte BNT2 stub (RUN-4) + now ALL 26
containers / 179,774 entries / 70 coincidences-only. The 65x65 climate grid and the
129x129 detail grids are NOT in the local 9.3.5 corpus. Acquisition = post-M1
(patcher-era container / runtime capture / server track — human-gated), unchanged.

MILESTONE IMPACT: queue item #4's exhaustive-negative is now COMPLETE-corpus
(was: the Parameters/Textures subset + the prior 178-container citation).
