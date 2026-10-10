# RUN_AND_STOP — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010

Serwer świata pozostaje URUCHOMIONY po tym runie, serwując DOKŁADNIE
opublikowany kod (weryfikacja tożsamości served↔published poniżej).

## Live (stan na koniec RUNDU KOREKTY 2026-10-10)

- URL launcher: `http://127.0.0.1:8163/launcher`
- URL świata: `http://127.0.0.1:8163/world`
- URL Asset Lab: `http://127.0.0.1:8163/assetlab`
- Bind: `127.0.0.1:8163` (loopback ONLY; brak publicznych portów/firewalla).
- Proces: `node.exe compat/server-world.mjs` — PID node: **23232**
  (start rundy korekty; węzeł cmd-wrapper: PID **29328**). CWD serwera:
  `D:\Eudoria_Reconstruction\12_WebGame\pe-world-continuous-r2`
  (worktree RESULT_BRANCH). Logi serwera (append):
  `D:\Eudoria_Reconstruction\99_Audits\PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010\server-run.log`
  (stdout) i `server-err.log` (stderr).

## Historia restartów (uczciwa — [POPRAWIONE w rundzie korekty: pierwotny
## zapis PIN 33876 był martwy w momencie QC])

Plik server-run.log pokazuje pełny łańcuch własnych restartów tego runu
(każdy poprzedni proces zatrzymany zanim następny wystartował; port 8163
nigdy nie był udostępniany publicznie; obce standing serwery
8140/8161/8162/9350 nietknięte):

```text
32048 → 35384 → 32592 → 35452 → 33876 → 5780 (live w czasie QC)
→ 23232 (restart RUNDY KOREKTY na kodzie korekty — serwuje DOKŁADNIE
   nowy opublikowany kod; weryfikacja served↔published poniżej)
```

Start wrapperów tej serii używał różnych wariantów startu (powershell/cmd
z env); wszystkie z CWD = worktree RESULT_BRANCH i pinem
PEWORLD_THREE_ROOT na node_modules THIS worktree.

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
Stop-Process -Id 23232 -Force   # PID node (własny serwer tego runu)
# (ewentualnie także wrapper-rodzica 29328, jeśli wciąż żyje)
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
