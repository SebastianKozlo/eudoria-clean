# R2-F01 — TERRAIN SAMPLE COUNTER CORRECTION RECORD

RUN_ID: EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927 (02_ANALYSIS)
Desktop finding: R2-F01 (GATEC_REAUDIT_R2_REPORT_20260927 section 6,
NEW_COUNTER_CORRECTION_REQUIRED, P2). Verdict: INDEPENDENTLY REPRODUCED.

## 1. THE CENSUS (fresh, this run; probe r2_f01_terrain_counter.mjs, node v22.22.0)

SOURCE: D:/Eudoria_Reconstruction/pcg_install/Data/Terrain/terrain.bnt
(PCG_9_3_5), SHA256 95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE6051
0299990, 125,064,817 B — hash pin re-verified fresh before the parse (READ-ONLY).

METHOD: BNT2 trailer parse. Trailer [dir_off u32]["BNT2"] at filesize-8; at
dir_off [count u32]; entries [name 0x0A-terminated][size u32][offset u32]
[crc u32][flags u32]. The index was consumed EXACTLY: p == filesize-8
(dir_off = 123,369,726, recorded in the JSON; count = 58,451).

MEASURED_QUANTITY / RESULT (full JSON: 03_EVIDENCE/R2_F01_TERRAIN_COUNTER.json):

| quantity | value |
|---|---|
| total index entries | 58,451 |
| eight-hex .tdf names | 58,451 (0 non-hex) |
| REGULAR (x in 0..219 AND y in 0..235) | 51,920 |
| distinct x among regular | 220, contiguous 0..219 |
| distinct y among regular | 236, contiguous 0..235 |
| SPECIAL (y in 0xff1a..0xffff) | 6,530 (y-range 65370..65535; x-range 0..217) |
| SENTINEL (7ffe7ffe.tdf) | 1 |
| duplicates | 0 |
| unclassified | 0 |
| EXCLUSION_SET | 6,530 special + 1 sentinel |

51,920 + 6,530 + 1 = 58,451 — every entry classified exactly once.

## 2. THE TWO INDEPENDENT ARITHMETIC PATHS (machine-executed, never hand-typed)

- Path A: 51,920 x 1,024 = 53,166,080 (regular tile blocks x 32x32 sample
  slots per block).
- Path B: (220x32) x (236x32) = 7,040 x 7,552 = 53,166,080 (the filename-xy
  grid dimensions x 32 pixels per axis — the mosaic extent).
- Both paths agree: 53,166,080.

FALSIFIER (recorded per the contract): 51,920 x 32 = 1,661,440 != 1,664,000 —
the old printed total is derivable from NO valid arithmetic over these
denominators (it was neither the tile count x samples-per-tile nor any other
product over the 51,920/32/220/236 denominator family).

## 3. THE PER-TILE DENOMINATOR (1024) FROM EXISTING FORMAT EVIDENCE

- R1 F03 section 7.2 B: "32x32 uint16 LE at payload offset 64" — 32x32 = 1,024
  sample slots per tile block (HEIGHT_DATA_OFFSET = 64, 64+2048 = 2112;
  2,048 bytes = 1,024 x uint16).
- The same file's DECODE EVIDENCE: 9,216/9,216 samples identical for 9 region
  tiles = 9 x 1,024 — internal consistency of the 1,024-per-tile denominator.
- Committed canon: the M1 gate matrix "220x236 = 51,920 regular" +
  docs/audits/CORRECTION_LEDGER.md PE-MASTER physical name census.

## 4. THE SAFE SEMANTIC (the corrected statement, EDIT A)

The total is 53,166,080 u16 SAMPLE SLOTS across the 51,920 regular 32x32 tile
blocks. EXPLICIT NOT-list:

- NOT unique height values (the count is slots, not distinct values);
- NOT unique world points;
- NOT historical original-client parity;
- NOT historical rendering coverage;
- NOT terrain-texture coverage;
- NOT proof of the RGB-TDF bridge.

BRIDGE_STATUS = UNKNOWN (the line in F03 is preserved byte-identical —
verified). Every calibration/unknown label elsewhere in the file is preserved
(structural checks: lines 1..101 and lines after the statement byte-identical
to the before-image; 03_EVIDENCE/EDIT_A_F03.diff shows exactly 1 removed +
11 added lines).

## 5. WHY THE CORRECTION WAS SAFE (blast radius)

The dependent-search record, timing-explicit (each value re-measured
2026-09-27): (a) Phase-1 search — pre-edit worktree, ALL 2,594 tracked repo
files (133,463,531 bytes), byte-level, literals "1,664,000"/"1664000"/
"1.664.000": ZERO tracked hits (the defect text lived only in the UNTRACKED
R1 package F03). (b) Post-Phase-4 re-verification — worktree WITH the R2 row
(all 2,594 tracked files, 133,465,692 bytes): exactly ONE tracked hit —
AUDIT_ENTRYPOINT.md line 30, this run's own R2 registration row, whose text
DESCRIBES the correction ("1,664,000 -> 53,166,080"); HEAD (cc747df)
contains ZERO hits; the R1 registration row (line 31) contains none. (c) The
R1 predecessor package (49 files, post-EDIT-A): exactly ONE occurrence — the
corrected F03 statement quoting the superseded value. (d) ZERO live
dependents of the old counter remain anywhere; the only occurrences are
correction descriptions. Per-item dispositions in 02_ANALYSIS/BLAST_RADIUS.md.
