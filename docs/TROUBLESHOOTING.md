# TROUBLESHOOTING

## Wrong era / hash mismatch

**Symptom**: mount refuses the archive, or the page refuses to render with a SHA
message.

By design: `PESourceMount` verifies `KNOWN_HASHES` at the mount boundary and refuses on
mismatch. Check that your `50.bnt` matches the era ISO_5_1_0_0 pin
(SHA256 `A6E59EE0…01DA00`, 118,016,977 B). A byte-identical file from another physical
source is fine *as a byte coincidence* — the era label lives in `PEProvenance.js`, not
in the file.

## Missing textures / flat colors

**Symptom**: terrain renders in diagnostic flat colors; HUD says
`STRICT_ISO_DIAGNOSTIC_COLOR`.

The ISO corpus ships **no texture container** (documented missing edge). Textures come
from REFERENCE mode: configure a route to the CD Jan-2003 `Textures.ark`
(SHA256 `D611D125…39B80`) and the 12/12 TexID join resolves. If the reference archive is
absent, the page degrades to diagnostic colors on purpose — it never substitutes random
textures from other eras.

## Shader errors

**Symptom**: console errors from `ShaderMaterial` / splat compile.

The splat is a custom `ShaderMaterial` — `scene.fog` does **not** reach it; fog is
injected via explicit `uFog` uniforms. If you edit the shader, keep the uniform contract
(`uFog` etc.) in sync with `src/peworld/IsoEnvironment.js`. Colorspace contract: sRGB
textures → linear lighting → sRGB out; changing texture colorspace without updating the
shader produces washed/dark output, not a bug in three.

## Model won't load: NIF 4.1 vs 10

**Symptom**: terminal error `version 0x0401000c NOT implemented` (or similar).

That is the **era gate working as designed** — the witness reader implements only NIF
10.1.0.0 and 4.1 loud-fails so no fake 4.1 IR exists. The inspector shows the 4.1 assets
as `ERA_GATE_LOUD_FAIL BY DESIGN` with the engine-oracle comparison available as
REFERENCE. The 4.1 adapter is backlog; do not "fix" by weakening the gate.

Related honest terminal states in the inspector:
- `WITNESS_CHAIN_LOUD_FAIL` — Ark-stripped adapted copy (built for the engine oracle)
  is withheld from IR by the fail-closed contract.
- `WITNESS_SCOPE_LOUD_FAIL` — a block type outside the witness scope (e.g.
  `NiSourceTexture` in BABYLENGUIN) stops the parse loudly; the engine census is shown
  as REFERENCE only.

## Server port occupied

`server.mjs` binds 127.0.0.1:8140 and **falls back to 8141** automatically; the chosen
port is written to the lease file together with the PID and a stop command. If both are
occupied, set `PORT` env var. URLs in this doc assume 8140 — check the lease if you get
connection refused.

## Preview vs. original params (reading the screen honestly)

The HUD/badge is the contract:

- `ENGINEERING PREVIEW` on the badge → sky/fog/light values are invented-but-explicit
  previews; only the fog **model** (semantics) is source-backed. `environmentzones` data
  was excluded as unverified.
- `REFERENCE` → texture pixels are CD Jan-2003, not ISO truth.
- `CURRENT_RUNTIME_CALIBRATION` (u16/128 → m, 2 m/sample) → display scale is a runtime
  calibration, not a recovered unit.
- Seams/zero-tiles labelled ORIGINAL DATA are intentionally unrepaired.

If something looks "wrong" but is labelled as one of the above, it is not a bug — it is
the honest ceiling of the recovered data (see `CAPABILITY_MATRIX.json`).

## Tests

```bash
node tests/bridge/rosettaRegistry.test.mjs     # 8 gates incl. J4 module hashes + mutant negative control
pushd src/pe2003/rosetta/bridges/gamebryoReference; node test_adapter.mjs; popd   # MUST run from that dir (relative imports)
```

The adapter suite must be run from its own directory. The mutant run
(`--adapter=./mutant_wrong_transpose.mjs`) failing is the **pass** condition of the
negative control.
