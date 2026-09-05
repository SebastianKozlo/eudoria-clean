# ITER-034: M1 Gate Regression Sweep (Milestone-Gate Preparation)

Session: M1 ITER_048 (ledger ITER_034), 2026-09-04. Scope: consolidation +
verification only — no code changes, no new forensics. This document records
the fresh regression sweep of every clean page at commit `b7d38ad` and the
evidence-SHA verification that backs the milestone-gate deliverable
(`02_ANALYSIS/M1_GATE_DELIVERABLE_MATRIX.md` + `.json` in the audit tree).

## Method

- Server: `node server.mjs` (PID 10584, port 8132), spawned and killed by the
  session; port 8132 closed and liveness verified at the end.
- Probe: `tools/cdp_probe.js` unchanged (raw CDP, headless Chromium; the
  proven route since ITER 031). One fresh page load per page, one fresh
  Chromium process per load; every process killed and liveness-verified.
- Executed script hashes (recorded before execution):
  - `server.mjs` 43404C17FEEF6BB3E529BFC8917A11B6F09AEA6FD0DFCA7A46E4C653D280B629
  - `tools/cdp_probe.js` 7052AE4167442F2EC3D943BEE36505CAD5A6775AC1060015F2DB22FCCE112195
  - `terrain/p0.js` BD019D56C3968664982321C1D6010EE49EB32529F03C008B8EDC290B096AB0F8
  - `terrain/materials.js` A42CE8356A14186001C1E243030D578D3BEC449C4099F1C0CB4BFEFE0023B39D
  - `terrain/materials_confirmed.js` 6CBEAF4FD1C7956ACEE5AB2BFECDA8E7CDC3B842FD861F254C27086AD1E129C4
  - `terrain/water_system.js` 92681C80CB6473A9AD2DE60A7AE245FB79887A951154E549E65ADCCB7F8BA0D0
  - `terrain/foliage_system.js` 011473ED90AEE99F55ECEE4ABADEBF9D637591A02CA9EB2435C11A32D3A66D93
    (identical to the iter033 manifest — the tree is unchanged since `b7d38ad`).

## Results — 5/5 pages reproduce their recorded deterministic hashes

| Page | Recorded hash (frozen evidence) | Fresh hash (this session) | Verdict |
|---|---|---|---|
| heights (`terrain/p0.html`) | `50BD7F9E4B715DB4972C65B068585696E8FEBC0E360FDABE4E941C6A6EBE33BC` | `50BD7F9E4B715DB4972C65B068585696E8FEBC0E360FDABE4E941C6A6EBE33BC` | MATCH |
| materials (`terrain/materials.html`) | `5F4677E6D7EB2EF2DABBAD7D52400A7412C7309E423C6059BFCDB01A22D336EC` | `5F4677E6D7EB2EF2DABBAD7D52400A7412C7309E423C6059BFCDB01A22D336EC` | MATCH |
| materials_confirmed (`terrain/materials_confirmed.html`) | `3C7855818B658B03E12132B31E4084A63194AC1F83C6F0568EB92EA886B8318F` | `3C7855818B658B03E12132B31E4084A63194AC1F83C6F0568EB92EA886B8318F` | MATCH |
| water_system (`terrain/water_system.html`) | `D7C13F1F128EEA1C096C6CEC00854D4D77DCD915F0FB219A554278FEBDFE3F44` | `D7C13F1F128EEA1C096C6CEC00854D4D77DCD915F0FB219A554278FEBDFE3F44` | MATCH |
| foliage (`terrain/foliage_system.html`) | `A79CB65C1852E8893E1346905D2F29BCBAC0C076D3EA6491AC1E2A7BDD92929F` | `A79CB65C1852E8893E1346905D2F29BCBAC0C076D3EA6491AC1E2A7BDD92929F` | MATCH |

Behavioral stats also reproduced exactly: materials_confirmed naive-vs-
confirmed white saturation 43.36% vs 0.0%; water page waterTileCount 5 with
water-tile heights 7.3..120.0 m; foliage 76/76 instances rendered from
4 distinct models with 0 NOT_FOUND and the foliage layer visible.
Zero deltas, zero root-cause investigations needed.

## Evidence-SHA verification

Every evidence file cited by the 19-row gate matrix was re-hashed on disk
during this session and compared with its ledger/manifest-recorded value:
12 ledger-recorded files, 5/5 (iter030) + 6/6 (iter031 spot-check) +
5/5 (iter032 spot-check) + 4/4 evidence and 7/7 repo runtime files
(iter033) manifest entries — **0 mismatches**. The consolidated list lives
in `03_EVIDENCE/iter034_regression_sweep.json` in the audit tree.

## Process discipline

Server PID 10584 and Chromium PIDs 12264, 10252, 14656, 14248, 6024 were
all spawned by this session, all killed, and all liveness-verified dead
(0 orphans). Pre-existing node/chrome processes from other sessions were
not touched (identity not provably this session's).

The full milestone-gate deliverable (the 19-row final matrix, the
era-bounded registry, the known-open list) is in the audit tree:
`99_Audits/PE_MILESTONE_1_WORLD_SURFACE_R1/02_ANALYSIS/
M1_GATE_DELIVERABLE_MATRIX.md` (+ `.json`, validated). The next step is the
master auditor's FULL_MILESTONE_AUDIT.
