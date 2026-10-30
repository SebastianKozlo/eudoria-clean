# Public Report — PE2003 Gamebryo Local Toolkit Asset Bridge Lab R1 (2026-10-30)

RUN_ID: PE2003_GAMEBRYO_LOCAL_TOOLKIT_ASSET_BRIDGE_LAB_R1_20261030. Sanitized public report: conclusions, metrics and provenance hashes only — no SDK content, no proprietary source, no asset bytes, no screenshots.

## What was attempted
Authorized side-lab (does not modify the STATIC_ONLY R17 campaign): bring the local Gamebryo toolchain to a visible working application and attach our Project Entropia 2003 game assets; keep every success term separate and honest.

## Results

| Gate | Result |
|---|---|
| SDK_CONTROL_RENDERED | PASS — via our harness on the stock Gamebryo 1.2 source-built engine; the stock 1.1.2 evaluation viewers/printer are LICENSE_BLOCKED (expired evaluation timelock modal; no license check was bypassed or patched; the ndldevlock route was deliberately left to a human policy decision) |
| PE_ASSET_PARSED | PASS — both 2003 models fully block-walked, originals byte-verified unchanged |
| PE_ASSET_RENDERED_NATIVE | NO — both models require the NiArk strip (adaptation) |
| PE_ASSET_RENDERED_ADAPTED | 218757 PASS; 296445 PASS_PARTIAL (billboard behavior, UV-anim and NiArk extra data lost — disclosed in the transformation maps) |
| SCENE_ASSEMBLY_TEST | PASS — 3 instances under one root, requested-vs-read-back transforms maxDelta = 0.000e+00, 58 shapes / 2082 triangles |
| Textures | PASS — real 2003 BNT2 textures re-attached via the project's confirmed NiArkTextureExtraData→BNT2-texture-ID mechanism; 9/14 and 22/30 shapes textured, the rest have no BASE texture entry (occlusion meshes / unsourced); texture-vs-no-texture negative controls: identical pixel coverage, 18812 vs 40 and 5230 vs 13 distinct colors |
| ORIGINAL_GAME_LOGIC_RUNNING | NO / NOT_ESTABLISHED (no original client, no injection, no network) |
| HISTORICAL_PLACEMENT / WORLD_XYZ | NOT_ESTABLISHED / NO (assembly positions are synthetic SYNTHETIC_TEST_PLACEMENT) |
| CANONICAL_GATE_EFFECT | NONE |

## Compatibility conclusions
- Stock Gamebryo 1.1.2 Evaluation tools (VC71/VC60): expired-timelock blocked; nothing was patched.
- Stock Gamebryo 1.2 (source-built, zero engine edits, timelock dead in source): working.
- Gamebryo 2.3/2.6: not tested this run.
- Key supersession: PE NIF 4.1.0.12 loads natively in stock Gamebryo 1.2 after the NiArk class strip — superseding the wave-1 stock-eval-SDK prognosis (which remains valid for the eval SDK's NiStream version gate); matches the EU935 GB12 oracle canon.
- Renderer honesty: stock NiDX8/9 renderers are unbuildable on this machine (missing d3dx9 SDK headers/libs); rendering uses a minimal fixed-function D3D9 path over the real engine scene graph (PLAN_B) — geometry, transforms and counts are 100% stock-engine data; render-path parity is NOT claimed.

## Provenance (SHA256, independent QC re-verified)
- 218757.nif (original, unchanged): C13D08736D7E778803E20A3105067448007F32D15290AF168F836CD99248AD98
- 296445.nif (original, unchanged): 656795D8B3DDDF8F9192EE41C4710D592894860F6959B53B2C08036977E7B862
- Control BABYLENGUIN.NIF: A86C49384E62DF41339101B62E48BE6DCAE10E06B5F7CAC39DC627CF89635EA9 (census 121 == EU935 oracle)
- 218757 stripped (59 blocks; original EU935 strip tool; local crosscheck byte-identical): 13807FC14BDD45095043B3563F400E0B7B980220D070BDD5F082683DD6ADB947
- 296445 stripped (145 blocks; documented local strip extension after the original tool's verbatim ABORT): 23EC7FF06C27F871AFE004113060DC6DA6C93D9D5FAF0CAAE7EAA81EF403C656
- Harness actually executed: 17B1ECE70BBEC7AFBC71DEDE91E5C1B2418837D50BCDF8336E83C5AC92F64AED
- Engine libs byte-identical to the audited EU935_GB12_ORACLE_SKIN_DEFORM_R2 manifest (NiSystem edc36c24…, NiMain d8ff4197…, NiAnimation b7ef80a0…, NiParticle d8b7958c…)

## QC
Independent fresh-auditor QC from disk: QC_PASS_WITH_FINDINGS — 3×P2 + 1×P3 documentation/provenance findings (a one-hex transcription typo in a result-JSON expected-SHA field; one truncated experiment-ledger line; a strip-map tool-attribution wording inconsistency; a minor ledger description drift), none affecting a load-bearing claim; all pins, strip maps (100% of remap entries), texture lineage (31/31 rows), engine-lib provenance and launcher logic independently re-verified. Full QC detail lives in the private run package, not in this repo.

## Limits
Working installation and all payloads/screenshots stay private (local-only WORK + audit roots); only this sanitized report is public. Stock evaluation tools remain license-blocked; no license circumvention was performed. The 296445 model is an honest PARTIAL (stripped NiArk features documented per-block in the transformation maps).
