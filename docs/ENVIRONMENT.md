# ENVIRONMENT — sky / fog / light layers and their honest modes

Bottom line first: **no original sky, fog, or light VALUES are recoverable in the
era-consistent corpus.** The runtime renders an explicit ENGINEERING_PREVIEW environment.
What *is* source-backed is the fog *model* (semantics shape) — nothing more.

## Layer → mode table

| Layer | Mode | Source | Consumer (Three r187) |
|---|---|---|---|
| **sky** | ENGINEERING_PREVIEW | procedural neutral gradient — no skydome/cubemap recovered anywhere in the corpus (0 cubemaps in CD Textures.ark DDS scan; 0 `NiSourceCubeMap` / `NiBillboardNode` in CD Models.ark NIF block scan) | gradient ShaderMaterial, BackSide dome r=24000, `fog:false`, follows camera; uniforms `uZenith/uHorizon/uGround` + orientation self-test |
| **fog** | ENGINEERING_PREVIEW **values** + SOURCE_BACKED **model** | gb12 `NiFogProperty.{h,cpp,inl}` (Gamebryo 1.2 reference source, read-only): enable flag + FogFunction `{FOG_Z_LINEAR, FOG_RANGE_SQ, FOG_VERTEX_ALPHA}` + depth float + NiColor; depth 0=no fog, 1=starts at near plane, >1=in front (front = near/depth); serialized order flags→depth→color. Values near=100 m / far=900 m are PREVIEW (derived from depth 0.01 @ near 1), not recovered. | `THREE.Fog` + explicit `uFog` uniforms in the splat shader (custom ShaderMaterial ignores `scene.fog`) |
| **light** | ENGINEERING_PREVIEW | W03/W05 diagnostic values kept explicit — the corpus has light *block censuses* but no recoverable scene-light parameters | DirectionalLight 2.5 + AmbientLight 1.0, dir (0.5, 1, 0.35) + splat uniforms |

## Corpus qualification (what was searched and ruled out)

| Candidate | Method | Verdict |
|---|---|---|
| CD Jan-2003 Textures.ark DDS payloads (1,359 DDS) | header scan for cube bits | **0 cubemaps** — no skybox faces |
| CD Models.ark NIFs (4.1.0.12: 1815, 4.0.0.2: 440, 4.0.0.0: 237) | block-type string scan | **NiFogProperty 0, NiSourceCubeMap 0, NiBillboardNode 0**; lights exist only as block censuses (NiDirectionalLight 1, NiAmbientLight 20, NiTextureEffect 105, NiFlipController 13) |
| `environmentzones_semantic` (24,007 records) | report review + consumer hunt | **PLAUSIBLE, NOT VERIFIED** — container unidentified, no consumer evidence → **excluded** as a fog source (explicit gate in the browser proof) |
| gb12 NiFogProperty source | direct read | EXISTS — the fog model above (paraphrase; source file pinned in the read-only lab tree). The ISO-era PE 5.1.0.0 consumer binary was **not** scanned (out of scope) |
| VM-era sky corpus (834 sky NIFs, cubemaps, ARK_FOG_*) | provenance check | **DIFFERENT ERA** — recorded as candidate only, no substitution |

## Toggles & hooks

- **KeyN** sky · **KeyB** fog · **KeyL** light (defaults restored after probes).
- Console: `__w14SetEnv`, `__w14EnvStats`.
- HUD shows a per-layer provenance table; the badge carries the global honesty statement.

## Verification

- 18/18 node unit gates (incl. the `SOURCE_BACKED_MODEL_gb12_NiFogProperty` label check
  and the environmentzones-excluded check) and 15/15 browser gates, including
  toggle pixel-difference controlled tests (sky ΔmeanLuminance 125.34; fog Δ16.41) and a
  W05 regression re-check (hash verified, 52-layer cross-check 0 mismatches).
- Screenshots exist but were **NOT_VISUALLY_REVIEWED** (session had no image input) —
  visual proof is the deterministic canvas statistics.

## Next steps (ranked backlog — none started)

1. Verify the environmentzones 24,007 container + a binary consumer (Ghidra trace in the
   PE 5.1.0.0 binary); if confirmed, promote zone fog colors/density from PLAUSIBLE.
2. Era-gated VM-corpus sky extraction as REFERENCE_RECONSTRUCTION under an explicit era
   contract.
3. Sky orientation visual test with a real recovered skydome (mandatory once one exists).
4. Clouds (billboard + NiTextureTransformController scroll), UV animation, day/night
   cycle, water — each its own job.
