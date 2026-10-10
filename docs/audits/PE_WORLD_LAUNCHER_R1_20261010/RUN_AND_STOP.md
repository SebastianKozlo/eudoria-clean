# RUN_AND_STOP.md — PE_WORLD_LAUNCHER_R1_20261010 — server run/stop commands

RUN_ID = PE_WORLD_LAUNCHER_R1_20261010
SCOPE = the world preview server the run leaves RUNNING for the user (contract §10) +
        the standing foreign servers (never touched by this run).

## 1. The world preview server (RUNNING now; the final code)

```text
URL           = http://127.0.0.1:8162/          ( /  -> 302 /launcher )
LAUNCHER      = http://127.0.0.1:8162/launcher
WORLD         = http://127.0.0.1:8162/world#tile=53,114&profile=0&seed=0&density=50
BIND          = 127.0.0.1 (loopback only; no LAN exposure)
PORT          = 8162 (contract §0 DEFAULT_PORT; env override PEWORLD_PORT=<port>)
PID           = 24964                     (node compat/server-world.mjs)
STARTED_AT    = 2026-10-10 (Etap E final code; NOT restarted after the U-19 fix —
                the server serves static client files FROM DISK, so the fixed
                compat/world-app.js is served by the same process; byte-identity
                verified: served == disk, SHA256
                15113B26B1F2AA53997BD5BFDE1D7B56EF53CCAF410426BB8BAB31BED599DB6A)
WORKDIR       = D:\Eudoria_Reconstruction\12_WebGame\pe-world-launcher-r1
```

### START (reproduce/replace)

```powershell
# from the worktree root (the branch codex/pe-world-launcher-r1-20261010 checkout):
Set-Location D:\Eudoria_Reconstruction\12_WebGame\pe-world-launcher-r1
npm run serve:world
# startup line (the PID is printed at startup):
#   world server http://127.0.0.1:8162/ pid=<PID> READY
# (optional) custom port:  $env:PEWORLD_PORT=8170; npm run serve:world
```

Startup behavior: fail-closed container pin verification (terrain.bnt + VegetationClimates
MOUNTED; Models.bnt + Textures.bnt stream-hash verified in background), index census
(58,451 entries = 51,920 regular + 6,530 special rows + 1 sentinel + 0 other), background
census of 51,920 regular tiles (~1.9 s; progress on /api/world/overview/progress), both
lazy indexes READY (models 5,596 entries; textures 8,381 entries), the vegetation support
census READY. Readiness: `READY` in the startup line; `/api/world/status` → `"ok": true`.

### STOP (own process only)

```powershell
Stop-Process -Id 24964        # the PID printed at startup; ONLY this process
```

The server prints its own PID + a stop line at startup (`STOP = terminate pid <PID> — only
this process`). NEVER kill by port ownership sweep: ports 8140/8161 belong to the standing
foreign servers (below). If you replaced the server with a new `npm run serve:world`, stop
THE PID IT PRINTED, not 24964.

## 2. Standing foreign servers (this run never touched them; leave them alone)

```text
PORT 8140 — PID 21288 — node compat/server-sceneir.mjs (the OLD 218757 viewer; the
           user's earlier URLs). Alive since 2026-10-10 01:39; untouched by this run.
PORT 8161 — PID 9588  — node server (the standing /catalog viewer). Alive since
           2026-10-10 04:18; untouched by this run.
```

The world server REFUSES 8140/8161 by construction (`PEWORLD_PORT` defaults to 8162; the
suites bound only their own free ports with port-freed proof at teardown). Historical
dev-server restarts inside this run stopped ONLY this run's own PIDs (ledger I-10/I-18/I-24:
13556 → 24412 → 24964, each with port-freed proof; the orphan debug-server cleanup PID 14820
is recorded in the ledger).

## 3. Test-suite servers (NOT running now — cleaned up, port-freed proof recorded)

Every test suite (world/materials/vegetation/headless-load batteries + the pixel runs)
started its own server on a suite-owned free port (8865, 8569, 8249, 8207, 8878, 8270…)
and stopped it at teardown with port-freed proof; raw lifecycle records are inside
TEST_RESULTS.json gate records. No test server is left behind (contract §10: „Nie
zostawiaj testowych serwerów”).

## 4. Status commands (verification)

```powershell
Invoke-RestMethod http://127.0.0.1:8162/api/world/status   # ok:true, pid, containers, census
Get-NetTCPConnection -LocalPort 8140,8161,8162 -State Listen
# 8162 -> OwningProcess 24964 ; 8140 -> 21288 ; 8161 -> 9588
```

If the world server ever dies: restart with §1 START (the census re-runs from the original
containers in ~2 s; nothing stateful is lost — every view is rebuilt from the original
bytes on demand).
