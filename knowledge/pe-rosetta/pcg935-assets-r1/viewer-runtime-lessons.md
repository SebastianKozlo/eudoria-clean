---
run_id: PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010
card: viewer-runtime-lessons
status: MEASURED_IN_BROWSER
sources:
  - module: compat/pcg935-viewer.js (the app)
  - evidence: PRIVATE_OUTPUT_ROOT/tests/browser_battery.json + browser/*.png
classification: INTERNAL_QC_ONLY_PENDING_DESKTOP
created: 2026-10-11
---

# Viewer runtime lessons (measured in headless Chrome via raw CDP)

## Latest-wins generation identity

Every selection increments a generation token; a stale fetch response is
dropped (checked AFTER await). Rapid A->B selection leaves exactly B loaded
(measured: 505775 -> 360268, final shows 360268, gen 9).

## Disposal on asset change

group removal + per-mesh geometry/material/texture dispose + mixer teardown.
LRU caches on the server are bounded (assets 6, textures 128) — measured
max 6 held during the 5,596-entry sweep.

## Drift-free looping

THREE.AnimationMixer + action.setLoop(LoopRepeat) — deterministic mixer
time. Evidence: after >2× duration (3.33 s clip played 8.1 s) the action
time wrapped to 1.44/3.33 (cycle 2 in progress), display derived from
action.time only. No wall-clock accumulation anywhere.

## The r185 scrub pitfall (REAL BUG FOUND AND FIXED)

`AnimationMixer.setTime(t)` ZEROES every action's time, and a paused action
never re-advances (`_effectiveTimeScale = 0`) — so the naive
`action.time = t; mixer.setTime(t)` sequence displays 0.00 and never applies
the scrub pose. Correct scrub: un-pause + ensure running +
`action.time = t` + `mixer.update(0)` (zero-delta apply). Measured fix:
scrub 600/1000 on 360268 (5.00 s) -> "3.00 / 5.00".

## Pixel evidence discipline

`canvas.getContext('webgl2')` + `readPixels` is INVALID for census when
`preserveDrawingBuffer=false` (returns zeros). Honest pixel evidence =
Page.captureScreenshot PNG decoded server-side, with drawers CLOSED and a
central crop census; the census discriminates assets (505775: 42.35% lit /
128 color varieties vs 223534: 5.24%/55; wireframe: 0.94%) — proving the
canvas renders the SELECTED asset, not a static page.

## Runtime hazards (recorded, bounded)

A few closure-heavy entries take minutes in the boundary search (the
known-FAIL files above plus at least one slow-but-passing entry in the
extent rank ~2000-2500 window; the sweep is checkpoint-resumable). The
server's per-asset JSON ceiling (96 MB) and truthful 413/422 keep the API
bounded.
