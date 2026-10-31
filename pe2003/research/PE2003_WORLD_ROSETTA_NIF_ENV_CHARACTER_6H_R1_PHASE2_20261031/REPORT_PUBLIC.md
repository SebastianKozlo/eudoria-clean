# PE2003 World Rosetta — NIF / Environment / Character campaign R1, phase 2 (public summary)

- **Campaign ID:** PE2003_WORLD_ROSETTA_NIF_ENV_CHARACTER_6H_R1_PHASE2_20261031
- **Target era:** Project Entropia 2003, ISO 5.1.0.0 disc image (PC Gamer
  cover-disc, Nov 2003)
- **Nature:** sanitized public projection (phase 2 of 2). No game payloads,
  binaries or private absolute paths are included in this repository; the
  full evidence corpus is held in the internal frozen audit archive (sealed
  by the parent campaign QC before this publication).
- **Publication job:** PUB2_PHASE2_PUBLICATION (attempt PUB2_a1), 2026-10-31 UTC.

## Headline results (from the frozen phase-2 campaign evidence archive)

1. **Dedicated NIF 4.1.0.12 adapter.** A separate format module
   (`src/pesource/NifModelReader41.js`) implements NIF 4.1.0.12 with 12 block
   types, sharing semantics with the 10.1 witness reader only where proven.
   The 10.1 reader's version gate is untouched (4.1 still loud-fails there by
   design; negative control preserved). Validation: 43/43 unit tests PASS
   (independently re-run from scratch by campaign QC), oracle parity 22/22
   plus a 50-node graph catch against the stock Gamebryo 1.2 engine oracle,
   and era dispatch confirmed live in the browser (4.1 fixture → 4.1 adapter,
   10.1 regression fixture → witness reader).
2. **World culling and real performance measurements (W22).** Frustum×Box3
   culling with 3/3 sanity gates; measured draw-calls drop 23→13 (static,
   culling ON vs OFF) and frame samples improve ON vs OFF in both static and
   moving-camera runs. Caveat: SwiftShader software-rasterizer bounds — all
   seven limitations are declared in the internal archive; the numbers are
   honest measurements under that environment, not native-GPU numbers.
3. **Explore window (W25).** Radius-2 camera-follow streaming with a 40-tile
   cache and farthest-first eviction: 61 tiles loaded and 21 evictions
   observed over two 384 m legs; HUD and culling sanity verified after
   eviction churn; a grid-absolute fix for the earlier west-column overlap
   and the hair re-pair correction (era V7) are included.
4. **Character creator (2003): 21 controls recovered.** Labels and layout of
   all 21 character-creation controls are RECOVERED from the native client.
   Slider ranges are NATIVE_CODEC_RECOVERED byte-exact: uniform f32 in
   [0, 1.0039] with step 1/254, integers in [0, 254] (codec constants
   re-verified in the binary bytes by campaign QC). Hair is 17×2
   double-sourced (cross-script + registry agreement); Size is 0..299
   COMPUTED_RUNTIME; gender is byte-proven (slot 45: 1=MALE, 2=FEMALE).
   Control→slot mapping: 2 RECOVERED, 18 positional PLAUSIBLE, 1 UNKNOWN.
5. **Color palettes do not exist.** The 2003 character creator uses no
   discrete color tables: colors are continuous 3×f32 RGB applied through
   the native virtual-call chain (consumer-side residue-0 analysis across
   the four consumer scripts).
6. **Head appearance chain: 1/20 chain-confirmed.** One head-appearance
   candidate (id 19706) is chain-confirmed to a NIF mesh hit by corpus
   pattern scan; the remaining 18/20 have no baked references (runtime
   slot-26 hypothesis retained, HYPOTHESIS-labeled in the preview), one is
   female-line out-of-set with a matching texture signature.
7. **Marshalling contract byte-proven (schema V10).** The character-creation
   marshalling contract (ff8f handler; GCE results at +4/+8/+0x10;
   caller-side argument pop) is RECOVERED byte-proven; slot semantics
   corrected to random-access byte indexes (supersedes the earlier
   sequential reading); control census 47.
8. **Character preview (terrain/character_preview.html + .js).** Read-only
   engineering preview of avatar 208861 with hair re-pair era V7, plus a
   20-candidate head-appearance panel with SHA-verified textures and an
   explicit HYPOTHESIS badge (no claim promotion).
9. **Documentation wave (V6→V10).** All changed docs (README_QUICKSTART,
   CHARACTER_CREATION, FORMAT_SUPPORT, NIF_BINDINGS, TROUBLESHOOTING,
   KNOWLEDGE_COVERAGE.csv, CAPABILITY_MATRIX.json) reflect the final V10
   state with corrections marked as corrections; 17 knowledge records
   (KNOWLEDGE_RECORDS_PHASE2.json) are included.

## Honest gaps (maintained, not promoted)

- The character-creation **wire format is OPEN**.
- 18 positional control→slot joins remain **PLAUSIBLE** (not RECOVERED).
- Skin/eye color semantic domains live in still-undecoded ArkScripts.
- Runtime frida instrumentation was **FORBIDDEN** in this campaign
  (governance note in the campaign contract); all runtime evidence is
  non-instrumented browser-level.
- Performance numbers are SwiftShader-bounded (see item 2).

## Status vocabulary

Results above use the project evidence vocabulary (CONFIRMED /
STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED / REJECTED). Item statuses are
carried from the frozen campaign evidence archive; this public file is a
projection only and is not itself the evidence.

## Related

- Phase 1 public summary:
  `pe2003/research/PE2003_WORLD_ROSETTA_NIF_ENV_CHARACTER_6H_R1_20261030/REPORT_PUBLIC.md`
- Campaign runtime pages: `/terrain/world_iso.html`, `/terrain/inspector.html`,
  `/terrain/character_preview.html` (served by `server.mjs`, port 8140
  default).
