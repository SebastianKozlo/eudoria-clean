# FORMAT_SUPPORT — container/formats decoded by this project (era PCG_9_3_5)

Public implementation doc · campaign PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031.

## 1. NIF 10.1.0.0 (Models.bnt members) — parsed with closure-exact block observer

- Models.bnt (SHA256 C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0, 5,596 entries, all .nif) — parsed by a **closure-exact parser** (`w3_kf_player_clips.py`, strict closure wrapper over the parser base): block boundaries are proven by span/consumption evidence, heuristics only where explicitly labeled (tail NiNode/ArkViewport boundary — accepted residual, disclosed).
- Blocks OBSERVED: NiNode, NiTriShape(+Data), NiSkinInstance, NiSkinData, NiSkinPartition (546608 = the only corpus file with it), NiKeyframeController, NiKeyframeData, NiTextKeyExtraData, NiArkAnimationExtraData (5-byte descriptor, format HYPOTHESIS — exporter metadata), NiTexturingProperty/NiArkTextureExtraData.
- **Known-answer validation (500078 DUNGMASTER): 11/11 clips** byte-decoded exactly (Idle_02@0.0 … die@20.0, tol 0.01); NiTextKeyExtraData consumed 25/25 records exactly to end-of-block; negative controls: truncated→reject, wrong-endian→reject (version 0x0000010A ≠ 0x0A010000), absurd num_block_types→reject.

## 2. .vcl (VegetationClimates.bnt) — text

- 32 profiles, whitespace 12-column records; 31/32 DECODE_OK, 25.vcl UNSUPPORTED (comma tokens, locale unknown — no normalization without proof). See BIOME_AND_VEGETATION_PROVENANCE.

## 3. TDF material tails (terrain.bnt)

- Per tile, per layer: 16×16 = **256 B mask, u8 RAW or RLE (count,value)** — mask@record+56, material id@+16; corpus 448,384 records / **0 decode failures** on the pinned PCG_9_3_5 terrain.bnt (iter019 canon); 3-tile physical check (50/111: 12 materials, 51/112: 13, 49/110: 12) — every mask exactly 256 B.

## 4. DDS DXT1 (Textures.bnt entries)

- Strict top-mip decode via the production `decodeDds` chain (same decoder as vegetation textures); the player texture 546609 is DXT1 1024×1024 — gate G4: 1,011,377/1,048,576 non-black texels, 8,740 distinct colors.

## 5. TGA2 24bpp

- Strict decode (`decodeTga2`) for terrain material textures → RGBA.

## 6. Animation keyframe data (KF closures-exact)

- NiKeyframeController/NiKeyframeData layouts decoded in the closure-exact parser (validated on 500078 known-answer first); per-bone key counts recorded per clip (W4_CLIP_KEYCOUNTS.json); interpolation OBSERVED LINEAR (type 1); keytime format [float32 time][uint32 len][string] byte-exact.

## 7. NOT supported here (explicit)

- ISO2003 / PE42 / eu2008 profiles are era-gated separately — no mixing by numeric ID; `PESourceMount` fails closed on any container SHA mismatch. Old BUNT/TDF-era 2003 pipeline rules do not apply to this runtime.
- 25.vcl comma records, NiArkAnimationExtraData payload semantics, non-`start -name` textkeys of the other 1,023 textkey-bearing files — OPEN (see RESEARCH_BACKLOG in the SCI seal package).

## Sources (file + SHA256)

- W3_PLAYER_CLIP_CANDIDATES_REPORT.md (CFB97748…) + w3_kf_player_clips.py (1CE0743BA006526BDD86EE03F0B5B95DDC88523001290FEC0D9332EF01395E94) — SCI W3_PLAYER\.
- W3_PLAYER_ANIMATION_DATA_REPORT.md (288379D5…) — 500078 textkeys + census.
- VCL_CENSUS.md (SHA256 see VCL_CENSUS.json per-file SHAs) — SCI W2_BIOME_VEGETATION\.
- W1-3_REPORT.md + MASK_RESOLUTION_EVIDENCE.json — SCI W1_TERRAIN_MATERIALS\W1-3\.
- W4_REPORT.md — SCI W4_ANIMATIONS\.
