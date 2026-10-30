# Public Report — PE2003 Rosetta/Gamebryo Bridge Corrections R1 (2026-10-30)

RUN_ID: PE2003_ROSETTA_GAMEBRYO_BRIDGE_CORRECTIONS_R1_20261030. Sanitized public report:
conclusions, metrics and provenance hashes only — no SDK content, no proprietary source,
no asset bytes, no private or absolute filesystem paths.

## Context

Corrections run over the side-lab PE2003_GAMEBRYO_LOCAL_TOOLKIT_ASSET_BRIDGE_LAB_R1_20261030,
whose independent external post-audit verdict was **PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS**.
The lab's executed achievements stand; six material findings (GBL-1..GBL-6) were corrected
additively — the historical lab package is untouched, old wordings are preserved verbatim
inside the correction records.

## What was corrected

- **Texture era (GBL-1):** "real 2003 textures" is REJECTED. The 31-row texture lineage traces
  to the EU_LATER-era Textures.bnt (reverse-engineering evidence only; SAME_ERA_WITH_PE42 =
  FALSE). Bounded per-member comparison vs the CD Jan-2003 Textures.ark: 16/24 byte-identical,
  8/24 byte-different, 0 absent; per-member era for the 8 byte-different members is
  NOT_ESTABLISHED (pixel identity not evaluated).
- **Alpha (GBL-2):** RGB is hash-preserved on all 31 rows, but variable alpha is lost for 2/24
  textures at the 24-bpp BMP re-encode; the GPU path is alpha-less end-to-end
  (X8R8G8B8, forced-opaque load, ALPHAOP disabled).
- **Transform math (GBL-3):** the old harness computed world = R^T(s·p)+t (wrong transpose;
  deviations 3.0–9.0 units on 4 executed cases) and its view builder both wrote the basis as
  rows (eye 18.977674 from the view origin) and mirrored the view X axis vs the engine's own
  right vector. The projection matrix was confirmed CORRECT. Claim corrected to
  "API-identity only" for the historical path.
- **Graph bypass (GBL-4):** the NiArkBillboardNode bypass-splice is PROVEN_BROKEN_FOR_7_OF_7 —
  the removed node's local transform was never composed (deltas 4941.8–11291.1 magnitude units
  plus dropped 180°-Z rotations; the lab's own engine recount independently corroborates all 7
  quads collapsed at one point). Related: 7 orphan NiZBufferProperty blocks, cull-none masking
  the orientation flip; UV-animation inertia caused by the untextured render path, NOT block
  removal; 0 NiArk blocks left as NULL.
- **Process/ledger (GBL-5) and manifest/hygiene (GBL-6):** the old lab's experiment ledger was
  rewritten by fix helpers (its "append-only" claim is false; INTEGRITY_PARTIAL at
  CURRENT_SEALED_BYTES=PASS); launch-cap lower bound 36 markers/32 logs, exact total UNKNOWN;
  corrected QC counter read 55304; the "exit6 absent" finding retracted; the old publication
  manifest was incomplete (1 row for 3 changed paths) — this run's manifest enumerates every
  staged path.

## What was built (new reference namespace — REFERENCE ONLY, runtime_enabled=false)

`src/pe2003/rosetta/bridges/gamebryoReference/` plus `tests/bridge/rosettaRegistry.test.mjs`:

- **niTransformAdapter.mjs** — corrected NiTransform→D3D/Three world+view math with explicit
  handedness (MissingConventionError), NaN/Inf rejection at ingestion, and a compose()
  operator. Executed: 8/8 gates (7 PASS + 1 honest SKIP in a bare checkout; the three.js
  cross-check executed separately against three@0.185.0). Negative control: the
  wrong-transpose mutant suite exits 1 as required.
- **rosettaReferenceRegistry.mjs** — strict era-scoped lookup. ISO 5.1.0.0 (primary target)
  queries are REJECTED — never substituted with other-era data; EU_LATER is found only as
  RE_EVIDENCE_ONLY. Executed: 8/8 registry gates PASS (including SHA256 module pins).
- **Knowledge records:** FORMAT_LOSS_MATRIX.json (11 capability rows with evidence pointers),
  TEXTURE_ERA_RECORD.json (per-member 16/8/0 era comparison),
  CLAIM_CORRECTIONS.json (6 additive corrections, old wording preserved verbatim),
  ROSETTA_INTEGRATION_MAP.json (per-record integration state).

Integration state: **INTEGRATION_PENDING** — no runtime code imports this namespace yet; every
record has runtime_enabled=false; the adapter/registry are exercised only by the test suites.

## Honest limits (unchanged by these corrections)

- No runtime claims: no game/client execution in this run; no corrected-harness render was
  executed (no repaired NIF was produced).
- Era NOT_ESTABLISHED for the 8 byte-different texture members; pixel identity not evaluated.
- World placement NOT recovered; assembly positions in the old lab were
  SYNTHETIC_TEST_PLACEMENT.

## Terminal fields

| Field | Value |
|---|---|
| PE2003_WORLD_XYZ_RECOVERED | NO |
| HISTORICAL_PLACEMENT | NOT_ESTABLISHED |
| ORIGINAL_GAME_LOGIC_RUNNING | NO / NOT_ESTABLISHED |
| ISO_5_1_0_0_APPLICABILITY | NONE (era is identity, never a fallback; SDK 1.2 = reference other-build convention only) |
| CANONICAL_GATE_EFFECT | NONE (advisory pre-qualification context; publication is not scientific acceptance) |

Independent QC of the corrections run: SCIENCE=QC_PASS_WITH_FINDINGS (advisory);
PROCESS=PASS_WITH_DISCLOSED_CORRECTIONS; INTEGRITY=INTEGRITY_PARTIAL for the OLD LAB only,
CURRENT_SEALED_BYTES=PASS; REPORTED_PENDING_EXTERNAL_POSTAUDIT.
