# PLAYER_AND_ANIMATION_PIPELINE — GAME_CHARACTER_REF + clips strictly from the game (era PCG_9_3_5)

Public implementation doc · campaign PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031.

## 1. Identity: GAME_CHARACTER_REF 546608 = MOB_FAMILY (adjudicated, not assumed)

The rendered character is Models.bnt member **546608**, explicitly labeled `GAME_CHARACTER_REF` — **NOT claimed "player avatar"**:

- Skeleton signature: 52 NiNode — full 3ds Max Biped chain **plus non-humanoid extras: Tail/Tail1/Tail2, rot 1–3, flash 01–05, frontsupport l/r, cannon l/r, drillarm l/r(+l2/r2), drill l/r** → family-coherent with the clip rigs (jaccard 0.962–0.981, bone intersection 50–51/52).
- TriShape census: 50 small segmented armor/attachment part boxes ('Bip01 X:0', 24–130 verts) + 1 skinned body mesh ('Mesh:0', 11,161 verts); no head/face morphs → NOT the creator-avatar shape.
- The actual **creator avatars are 567279/576976** (head_up_BASE/BUMP morphs, character-creation section of templates.vfs) — and they carry **0 KF controllers** (no clip family in the corpus). The mob biped 546608+clips is the only fully animated character in Models.bnt; exact species name of template 13793 → UNRESOLVED.

## 2. Clips (GAME_ANIMATIONS_ONLY = YES)

- **idle = Models.bnt:546617** (dur 5.3333 s) and **walk = Models.bnt:546613** (dur 1.6667 s) — 44 tracks each, LINEAR (OBSERVED type 1), no resampling, source keytimes kept exactly. Both activated clips have full certs (container SHA + member SHA) — see ANIMATION_MANIFEST in the SCI seal package.
- Clip names "idle"/"walk" are **KINEMATIC_CLASSIFICATION** labels — the source data contains NO clip names (only mob 500078, DUNGMASTER, has named clips in the entire corpus: 11 names on a shared 20 s timeline).
- Cyclicality OBSERVED: walk first/last key identical (seamless 0.0); idle non-perfect (0.6006) — honest note, runtime LoopRepeat = ENGINEERING policy; crossfade 0.25 s = ENGINEERING; WASD switch threshold 0.2 = ENGINEERING.
- Zero synthetic keyframes, zero retargets, zero procedural bone motion (independently QC-verified by full read of `compat/world-player.js`: tracks built exclusively from `asset.clips`; no sin/cos bobbing; WASD only moves the root transform/yaw/clip-switch).

## 3. Skinning port (bind law, verified numerically)

- GB contract law `world = parentWorld*local, p' = (R*p)*s + t`; **W_i · SkinToBone_i = I for ALL 38 skin bones (rot dev 3.9e-7, translation spread 6e-4, common offset c=(0, 368.479, 0))**; boneInverses passed VERBATIM.
- Weights: per-vertex influence census {1: 10799, 2: 360, 3: 2} — **max 3 ≤ 4 supported: zero truncation, zero renormalization, 0 unweighted** (all 11,161 vertices).
- **Up-axis = −Y measured** (head-pelvis world delta (10, −736.9, 9.1) via GB-law chain math; the biped is authored Y-inverted) → root rotation.z = PI + scale 0.001125 (RUNTIME_CALIBRATION to 2.0 m) + feet shift −0.089 m; final world bbox 1.78×2.00×1.76 m.

## 4. Oracle: gb12 CPU vs THREE (independent verification)

- A Gamebryo 1.2 CPU oracle evaluates the original controllers; comparison against the Three.js playback: **idle max_rot 0.094°, walk 0.135°** — inside an ANALYTICALLY_DERIVED tolerance (0.20° rot / 0.20% trans; mechanism: gb12 FastNormalize ISQRT ~1.5e-3 non-orthonormality + lever-arm).
- **Negative control fired**: perturbed walk vs gb walk → Head deviation **4.50°** > tol → detected=true (the comparison catches real errors — not a default-success gate).

## 5. Run it

Staging `/world` (8171): the textured character spawns at the camera focus, feet on the shared height query (`queryHeightAtWorld`), 3rd-person camera cooperating with OrbitControls. WASD moves (idle↔walk by input speed), mouse-drag orbits around the character. Browser gates G1–G5 (render/clip-switch/bbox/texture/pause-seek-speed) — all PASS (W4_BROWSER_GATES.json).

## 6. Honest gaps

- 50 rigid part-box meshes (armor plates) NOT rendered (missing TriShape→parent edge in the cached graph — resume point).
- BUMP slot 546611 carried, unused (BASE only). Idle loop seam possible at wrap.
- A TRUE player avatar would need the 567279/576976 family — which has no clips; GAME_CHARACTER_REF is the honest compromise, explicitly labeled.

## Sources (file + SHA256)

- W4_REPORT.md, ANIMATION_MANIFEST.json (SHA256 1CA552E5569E68278C3E346E8B0A22C201C0FCB16D5E0A28893598F672FC2B59) + ANIMATION_MANIFEST_CLEAN.json (DD1B7F4F44F13B5A1BEBFB24D52DA0FD7D3EEB5C14D29CC29A47F5CD52B55C71), W4_BROWSER_GATES.json, ORACLE/compare_result.json — SCI W4_ANIMATIONS\.
- W3_PLAYER_ANIMATION_DATA_REPORT.md (288379D5F23DA6CD15CBF850A87E3F52438906405AB428978D086EADF6BB7F1F), W3_PLAYER_CLIP_CANDIDATES_REPORT.md (CFB977483800FF7E4C9AB9D3CF0B63AD7DD02B5E40CFD5A9318104446F0D7CD8), W3_PLAYER_AVATAR_CANDIDATES_REPORT.md (D8577B05DA1AD04B5A772ECDA2CED0EB3880013083E0BCC1B25676A7AC27FCDA) — SCI W3_PLAYER\.
- compat/world-player.js (deployed == NEW_WORK tools copy, hash-identical, QC-verified).
