# PE2003 World Rosetta — NIF / Environment / Character campaign R1 (public summary)

- **Campaign ID:** PE2003_WORLD_ROSETTA_NIF_ENV_CHARACTER_6H_R1_20261030
- **Target era:** Project Entropia 2003, ISO 5.1.0.0 disc image (PC Gamer cover-disc, Nov 2003)
- **Nature:** sanitized public projection. No game payloads, binaries or private
  absolute paths are included in this repository; the full evidence corpus is
  held in the internal frozen audit archive.
- **Publication job:** PUB_SANITIZED_PUBLICATION (attempt PUB_a1), 2026-10-30/31 UTC.

## Headline results (from the frozen campaign evidence archive)

1. **ISO 5.1.0.0 era established.** The recovered ISO-disc BUNT terrain
   container (`50.bnt`) was structurally confirmed at the 5.1.0.0 era:
   51,920 tile records after full decode. The ISO-era container differs from
   the earlier reference eras by a **+56 offset base** in the container
   header/index layout (offsetbase delta +56), recorded as an era marker for
   all downstream parsing.
2. **Rosetta Gamebryo reference bridge: 12/12 joins.** All 12 knowledge
   records of the campaign's reference bridge join cleanly between the
   project's era-declared structure model and the external Gamebryo-era
   reference stack (REFERENCE joins: 12/12).
3. **Oracle cross-validation:** **31/32** (era A) and **22/22** (era B)
   checks passed against the independent oracle helper suite. The single
   non-passing era-A check is documented in the internal archive with its
   exact predicate and is NOT counted as passing here.
4. **NIF inspector** (terrain/inspector.html + terrain/inspector.js): an
   in-browser block-level NIF inspector for the reference fixtures, with
   client-side SHA pinning of the inspected files.
5. **ISO world slice preview** (terrain/world_iso.html +
   terrain/world_iso.js): WebGL preview of the ISO-era terrain vertical
   slice (50.bnt), rendered from the decoded tile records via the
   src/peworld ISO environment/materials modules
   (IsoEnvironment.js, IsoMaterialsFixture.js, IsoPatchSelection.js).
6. **Environment preview:** era-labeled environment presets derived from the
   ISO-era material data; see docs/ENVIRONMENT.md.
7. **Character-creation schema: 40 fields.** A 40-field character-creation
   data schema was reverse-engineered and documented (docs/CHARACTER_CREATION.md).
8. **Performance measurements: NOT_PERFORMED.** No runtime performance
   benchmarking was executed in this campaign; any performance claims are
   explicitly out of scope.

## Status vocabulary

Results above use the project evidence vocabulary (CONFIRMED /
STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED / REJECTED). Item statuses are
carried from the frozen campaign evidence archive; this public file is a
projection only and is not itself the evidence.

## Related

- Rosetta Gamebryo bridge corrections R1:
  `pe2003/research/PE2003_ROSETTA_GAMEBRYO_BRIDGE_CORRECTIONS_R1_20261030/`
  — see the additive notice `NIGHT6H_R1_ADDITIVE_NOTICE.md` in that directory
  for the current seal state of that corrections run.
- Campaign runtime pages: `/terrain/world_iso.html`, `/terrain/inspector.html`
  (served by `server.mjs`, port 8140 default).
