# FINDING N-6 — THE TEZ<->FIELD FRAME RELATION PINNED (+ a layout/canon correction)

**RUN**: the georef open bound #2 (the TEZ frame vs the global field frame) — offline,
read-only, era 9.3.5. File: pcg_install\Data\TerrainEditZones\TerrainEditZones.bnt
(54,156 B, SHA at artifact_index; 171 .tez entries).

## THE CORRECTED RECORD LAYOUT (empirical, per-slot census over 1,020 records)

The prior layout claim ("48-byte records: X0/Z0/X1/Z1 floats + height + blends") was
RIGHT about the 48-byte stride but WRONG about the coordinate types. The per-slot
census (12 u32 slots each; int + float interpretations both computed) establishes:

```
[4 x i32  ] the rect: corner1=(slot00,slot01), corner2=(slot02,slot03)  (SIGNED INTS)
[f32 x 1  ] slot04 = the target height
[f32 x 4  ] slots05-08 = the blend parameters (range 0..1)
[u32 x 3  ] slots09-11 = flags/ids (small ints; 0, 1, 65536-patterns)
```
Evidence: slot00-03 decode as i32 with paired-similarity (corner1 ≈ corner2 per axis);
the raw-record hex (e.g. `64 c3 ff ff` = -15,260); slot04 as f32 = the height range;
slots05-08 as f32 = [0..1] with 1.0 (`00 00 80 3f`) present; the int-like census.

## THE FRAME MEASUREMENT (all 1,020 records, 0 layout fails)

```
X range: -32,144 .. +31,896      (corner1 -32,144..+31,744; corner2 -31,780..+31,896)
Z range: -31,664 .. +16,964      (corner1 -31,664..+16,956; corner2 -31,580..+16,964)
heights: -35.5 .. +645.1 m        (the field's (t-128)x5 range = -640..+635 — consistent;
                                   the edit targets may exceed the natural terrain max)
ALL 1,020 records: 100% inside the global-field frame (-65,536..+65,536) ✓
The magnitudes match the 24007.vfs historical locations (X -30,693..+25,070;
Z -28,980..+27,705) ✓ — the SAME world frame.
```

## THE CANON CORRECTION

The prior claim — "contains world-space float values up to 524,287 (= 2^19 - 1, the
world boundary)" (the pe-bnt-tdf skill TEZ section + the prior censuses) — is
**A MISPARSE**: the coordinate slots are SIGNED INT32 (not floats), and the actual
values top at ~32k, inside the field frame. The "524,287" figure was an artifact of
the int/float interpretation confusion (a float bit-pattern read as an int, or the
small-int flag slots misread). **There is NO evidence of a separate 2^19 world
boundary frame in the TEZ data.**

## THE GEOREF CONSEQUENCE

The RUN-3 georef honest bound "the TEZ<->field frame relationship NOT established"
is now CLOSED: **CONFIRMED — the TEZ edit layer operates in the SAME world frame as
the global field and the historical locations** (TEZ ⊂ field, one frame, no separate
planetary 2^19 extent). The world frame inventory (RUN-3) simplifies to:
**THE field frame is THE frame** (the historical locations, the TEZ edits, and the
field all share it).

MILESTONE IMPACT: georef/P-DATUM (queue #3) advances from "the TEZ relation open"
to "the frame closed with a canon correction". Wiki HOLD respected (the skill text
NOT edited; the correction recorded here + proposed for the ledger).
