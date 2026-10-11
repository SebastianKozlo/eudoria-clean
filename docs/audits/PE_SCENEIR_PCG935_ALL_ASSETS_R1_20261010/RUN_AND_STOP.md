# Run and stop — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010

## Staging (8164)
START:  cd D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-pcg935-all-r1
        node compat/server-pcg935-viewer.mjs            (PORT env, default 8164)
STOP:   stop the node process serving 8164 (identify via
        netstat -ano | findstr :8164 — never by name alone)

## Production (8140)
START:  cd D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-pcg935-all-r1
        set PORT=8140 && node compat/server-pcg935-viewer.mjs
ROLLBACK (old viewer): cd D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-218757-r1
        node compat/server-sceneir.mjs

Environment overrides: PECOMPAT_MODELS, PECOMPAT_TEXTURES, PECOMPAT_CATALOG,
PECOMPAT_THREE_ROOT (all fail-closed SHA-verified at startup).

## Tests
node tests/pecompat/run_pcg935_viewer_tests.mjs [--sweep]
