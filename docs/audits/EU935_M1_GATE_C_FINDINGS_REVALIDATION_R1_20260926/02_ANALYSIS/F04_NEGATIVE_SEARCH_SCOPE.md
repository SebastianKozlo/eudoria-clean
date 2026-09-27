# F04 — NEGATIVE-SEARCH SCOPE REVALIDATION

RUN_ID: EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926 (02_ANALYSIS)

## 1. THE HISTORICAL METHODS (read from the actual scripts; kept SEPARATE)

| method | script | corpus | predicate | expected target class | positive control | negative control | denominator | result (this run's re-derivation) |
|---|---|---|---|---|---|---|---|---|
| Parameters grid-absence | cellstream_census.py (c) | pcg_install\Data\Parameters (27 .vfs) | file SIZE == 4225/16641 or +16 or (n-16)%grid==0 | raw 65x65/129x129 grid files (+16B ArkVFS header variants) | (implicit: the size arithmetic) | the divisibility guard | 27 files | 0 hits (27 re-counted this run) |
| Textures entry-size census | cellstream_census.py (d) | Textures.bnt BNT2 index | entry SIZE in (4225, 16641, 4225+18, 16641+18) | raw/TGA-header grid payloads stored as entries | the historical +18 TGA variants | — | 8,381 entries (re-walked this run) | 0 hits |
| Expanded grid negatives (N-8) | expanded_negatives.py | ALL local 9.3.5 .bnt + raw files under pcg_install\Data | entry/file SIZE in {4225,16641}+{0,16,18,12} (8 size classes) | raw/+header grid payloads | the raw-u8 sizes 4225/16641 | — | 26 containers / 179,774 entries (re-walked this run) | 70 hits = 69 compressed TDF (terrain.bnt) + 1 NIF (Models.bnt 31657.nif); 0 grid data |
| Known-ID/provider search | iter029_idscan.json | 178 containers (89 BNT2 + 82 VFS + 7 ARK) across PCG_9_3_5 + EU2008 + JUL2003_originals | entry NAME matches 432502.*/459344.*/429259.* | the KNOWN world-data resource IDs | 429259 (found in 4 Textures.bnt containers — LOCAL both 9.x eras) | 432502/459344 = 0 hits anywhere | 178 containers (re-counted this run: 89/82/7) | 429259 LOCAL x4; 432502 = 0; 459344 = 0 |
| Review-time wide Textures scan | PE_MASTER_REVIEW (cellstream run) | Textures.bnt BNT2 index | 32 size classes (65x65/129x129 x u8/u16/24bpp/32bpp x header variants) | any u8/u16/RGB/RGBA grid-shape entry size | — | — | 8,381 entries | 0 hits (historical record; the 32-class set is PE-MASTER's review-time predicate, distinct from the recorded 8-class N-8 script) |

The 70-hit size scan and the known-ID/provider search are SEPARATE lines with
separate coverage — never merged (the 70 hits are size coincidences of compressed
TDFs + one NIF; the known-ID search is an exact-name enumeration; the 429259
presence is established ONLY by the latter).

## 2. §8.1 SYNTHETIC DETECTOR CONTROLS (predicate calibration — NOT evidence that historical resources exist)

Fixtures generated in 03_EVIDENCE/synthetic_detector_controls/ (deterministic
content; SHA256 per fixture in F04_NEGATIVE_SEARCH_CONTROLS.json):

| fixture | encoding | size (B) | N-8 predicate {4225,16641}+{0,12,16,18} | cellstream Textures predicate {4225,16641,+18s} |
|---|---|---|---|---|
| synthetic_raw_u8_65x65.bin | raw u8 65x65 | 4,225 | DETECTED | DETECTED |
| synthetic_raw_u8_129x129.bin | raw u8 129x129 | 16,641 | DETECTED | DETECTED |
| synthetic_rgb_65x65_tgalike.bin | RGB 65x65 + 18B header | 12,693 | MISSED | MISSED |
| synthetic_rgb_129x129_tgalike.bin | RGB 129x129 + 18B header | 49,941 | MISSED | MISSED |
| synthetic_rgba_65x65_tgalike.bin | RGBA 65x65 + 18B header | 16,918 | MISSED | MISSED |
| synthetic_rgba_129x129_tgalike.bin | RGBA 129x129 + 18B header | 66,582 | MISSED | MISSED |
| synthetic_zlib_65x65_u8.bin | zlib u8 65x65 (ramp) | 317 | MISSED | MISSED |
| synthetic_zlib_65x65_u8_zeros.bin | zlib u8 65x65 (zeros) | 27 | MISSED | MISSED |

Desktop's expected sizes re-derived exactly: RGB 129x129 TGA-like = 49,941 B
(129*129*3+18); RGBA 65x65 TGA-like = 16,918 B (65*65*4+18); zlib zeros = 27 B
(this run's zeros fixture = 27 B — matches Desktop's control; the ramp variant
= 317 B, both MISSED). INTERPRETATION: the historical size predicates ARE
sensitive to the raw encodings they were designed for and BLIND to RGB/RGBA/
compressed encodings of the same grids. The fixtures test the PREDICATE
boundary only — they are NOT evidence that historical resources of those
encodings exist in any corpus (labeled SYNTHETIC DETECTOR CONTROLS).

## 3. §8.2 BOUNDED NEGATIVE LANGUAGE (the corrected statement set)

VALID (what the record actually shows):
- "All 27 Parameters .vfs files were enumerated under the size/divisibility
  predicate; 0 matched."
- "All 8,381 Textures.bnt entries were enumerated under the 4-size (and,
  review-time, 32-size-class) predicates; 0 matched."
- "All 26 local 9.3.5 .bnt containers (179,774 entries) were enumerated under
  the 8-size predicate; 70 size-coincidences, all identified (69 compressed TDF
  + 1 NIF); 0 grid data."
- "All 178 containers across the three corpora were enumerated for the known IDs
  432502/459344/429259 by name; 429259 present in 4 Textures.bnt containers;
  432502 and 459344 absent."

INVALID (overclaims NOT made anymore):
- "All possible grid/cellstream representations are absent" — NOT proven: the
  RGB/RGBA/zlib/embedded encoding classes were NOT tested by the recorded
  predicates (demonstrated by the synthetic controls).
- Any statement implying the 70-hit scan proves the known-ID search's coverage
  or vice versa.

Carried status for the omitted classes: NOT_DETECTED_UNDER_THESE_PREDICATES +
UNKNOWN. No unrestricted decompression or asset-hunting campaign was started
(none authorized).

## 4. GATE-A IMPLICATION (P-CELLSTREAM/P-CLIMATE)

The honest BLOCKED-UNKNOWN for the cellstream/climate P0 SURVIVES on the
corrected basis: the acquisition paths remain post-M1/human-gated; the
exhaustive claim is now precisely scoped (index enumeration under explicit
predicates = YES; arbitrary-encoding detection = NO). See
01_RAW/GATE_REVALIDATION.csv GATE A.

## 5. RESULT

Desktop GC-F04 REPRODUCED: all denominators re-derived and matched (27; 8,381;
26; 179,774; 70 = 69+1; 178 = 89 BNT + 82 VFS + 7 ARK; 429259 x4; 432502/459344
= 0); the size-predicate insensitivity demonstrated with synthetic controls;
the two methods kept separate; the negative language corrected per §8.2.
Delta edges: UNRESOLVED A3/A4/A18/B4/C4/C5 (NEW_CORRECTION_EDGE — language
narrowing; no item renamed into a success).
