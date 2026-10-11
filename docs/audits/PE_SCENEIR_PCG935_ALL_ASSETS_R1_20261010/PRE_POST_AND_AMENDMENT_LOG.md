# Pre/post and amendment log — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010

## Preflight (pre)
- Contract identity verified (33060 B / 12183200…7F31E).
- Worktree pe-sceneir-pcg935-all-r1 created from e9bb1f5; branch
  codex/pe-sceneir-pcg935-all-assets-r1-20261010.
- Inputs SHA-verified (Models c950a8c2…, Textures 61acd13b…).
- Donor DdsDecoder.js extracted byte-exact (7535 B / 12323655…).
- 8164 free; 8140 (PID 21288) + 8161/8162/8163/9350 untouched throughout.

## Execution (in-run amendments, all recorded)
1. v4 reader layout corrections (double-flags fix, ArkTexture i32,
   4.0.0.2 gates, lights version-split) — measured on-corpus, 757/757+1/1.
2. Mesh/tri counting fix for v10 (geometry lives on the dataRef target).
3. Texture chain v10 extension (texprop-level ArkTexture binding) after the
   probe showed empty texprop slots in the PCG corpus.
4. TGA 24-bpp dispatch added (decodeTga2) after the A32-only call failed.
5. Scrub bug found in browser testing (r185 mixer.setTime zeroing) — fixed
   and re-verified (3.00/5.00).
6. Sweep made resumable + SKIPPED_KNOWN_FAIL category after a crash near the
   rank-2000 slow entry; end-of-run stale-reference bug fixed; re-run clean.
7. Camera-up/space conventions follow the old viewer (default Y-up, raw
   FILE_SCENE_SPACE rendering, AABB fit on updateMatrixWorld(true)).

## Post
- All 11 gates PASS (STAGE_ACCEPTANCE_GATES.csv; TEST_RESULTS.json).
- Package finalized; MANIFEST generated last.
