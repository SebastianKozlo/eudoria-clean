# 8140 handoff — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010

Authorization: contract §10 — replace ONLY the verified old SceneIR listener.

Pre-handoff state (all measured):
- Staging server on 127.0.0.1:8164 (PID recorded at handoff time) serving
  the new viewer; all 11 gates PASS.
- Old viewer: 127.0.0.1:8140, PID 21288, cmdline
  node compat/server-sceneir.mjs (worktree pe-sceneir-218757-r1 @ 59641ca).
- Rollback: cd D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-218757-r1 &&
  node compat/server-sceneir.mjs   (immediately after stopping the new one).

Procedure executed:
1. Verify PID 21288 cmdline contains server-sceneir.mjs (never unknown PIDs).
2. Stop ONLY that PID.
3. Start the new server with PORT=8140:
   cd D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-pcg935-all-r1 &&
   set PORT=8140 && node compat/server-pcg935-viewer.mjs
4. Verify /, /app.js, /api/catalog, /api/asset/223534 (or 505775),
   /api/texture/223496 and /api/status identities match the published commit.
5. On ANY essential failure: stop the new server, restart the old one from
   the immutable worktree, report FINAL_8140_HANDOFF=FAILED_ROLLED_BACK.

Result: recorded in the final return (the handoff is executed AFTER the
publication step per the contract order; CORRECTION_ROUND1 restart note:
both servers restarted from the corrected commit, PIDs verified by cmdline
server-pcg935-viewer.mjs before any stop — never unknown PIDs).

## Terminal labels (contract-required)

```text
HISTORICAL_WORLD_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
INDEPENDENT_DESKTOP_POST_AUDIT = PENDING
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```
