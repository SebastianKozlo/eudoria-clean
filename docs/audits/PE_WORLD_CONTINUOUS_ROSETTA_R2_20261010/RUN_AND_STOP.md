# RUN_AND_STOP — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010

Serwer świata pozostaje URUCHOMIONY po tym runie, serwując DOKŁADNIE
opublikowany kod (weryfikacja tożsamości served↔published poniżej).

## Live (stan na koniec runu)

- URL launcher: `http://127.0.0.1:8163/launcher`
- URL świata: `http://127.0.0.1:8163/world`
- URL Asset Lab: `http://127.0.0.1:8163/assetlab`
- Bind: `127.0.0.1:8163` (loopback ONLY; brak publicznych portów/firewalla).
- Proces: `node.exe compat/server-world.mjs` — PID node: **33876**;
  rodzic (wrapper powershell z env): PID **30780**. CWD serwera:
  `D:\Eudoria_Reconstruction\12_WebGame\pe-world-continuous-r2`
  (worktree RESULT_BRANCH). Logi serwera (append):
  `D:\Eudoria_Reconstruction\99_Audits\PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010\server-run.log`.

## Start (jeśli trzeba odtworzyć)

```powershell
$env:PEWORLD_PORT='8163'
$env:PEWORLD_THREE_ROOT='D:\Eudoria_Reconstruction\12_WebGame\pe-world-continuous-r2\node_modules\three'
Set-Location 'D:\Eudoria_Reconstruction\12_WebGame\pe-world-continuous-r2'
node compat/server-world.mjs
```

(Zajęty 8163 = LOUD FAIL — serwer nigdy nie zastępuje obcego procesu;
standing serwery 8140/8161/8162/9350 pozostają nietknięte.)

## Stop (tylko WŁASNY proces)

```powershell
Stop-Process -Id 33876 -Force   # PID node (własny serwer tego runu)
# (ewentualnie także wrapper-rodzica 30780, jeśli wciąż żyje)
```

## Tożsamość served↔published

1. `compat/server-world.mjs` (oraz wszystkie allowlistowane statiki) są
   serwowane Z DYSKU WORKTREE — żaden build/kopia pośrednia; publikowany
   commit zawiera TE SAME pliki (manifest weryfikuje pakiety audytów;
   changed-path census porównuje dysk↔git blob przed commitem).
2. Po push: `local RESULT_BRANCH == origin/RESULT_BRANCH == fresh
   ls-remote` (zapisane w HANDOFF) — kod serwowany z checkoutu tego
   worktree = opublikowany blob (żaden „gotowy serwer” po błędzie
   bindowania: start ma fail-closed na port + pin weryfikacji).
3. Three.js: `PEWORLD_THREE_ROOT` wskazuje node_modules THIS worktree
   (three@0.185.0 pinned; retention gate przy starcie serwera).

## Uwaga operacyjna

- Census/far po starcie: background; far route 503 + progress aż READY
  (~10–120 s z ciepłym FS cache). Klient pokazuje PENDING uczciwie.
- Cztery pinned archiwa + Models.ark (Asset Lab) muszą pozostać na swoich
  ścieżkach (piny fail-closed przy starcie/Asset Lab lazy load).
