# BASELINE PIN — EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926

Executor: pe-reconstruction. Dispatcher: PE-MASTER (direct dispatch, NO_NESTED_TASKS).
RUN_CLASS: LOAD_BEARING; RUN_TYPE: GATE_C_FINDINGS_CORRECTION_REVALIDATION; STATIC-ONLY
(the client never ran; no GPU/physical-console experiment; no new corpus; no patching).

## GIT PIN (verified at run start 2026-09-26, by this executor)

- BASE_SHA = HEAD at run start = `cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d`
  - `git rev-parse HEAD` = cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d — MATCH
  - `git rev-parse origin/master` = cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d — MATCH
  - `git ls-remote origin master` = cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d refs/heads/master — MATCH
  - Commit chain verified: 0187e18 -> e077562 -> 7ebe717 -> cc747df (the M1 audit lineage)
- Working tree at start: EXACTLY the 2 pre-existing untracked roots
  (`?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/`, `?? experiments/`);
  ZERO tracked modifications. READ-ONLY context; untouched by this run.
- This run is PRE-PERSISTENCE: NO git add / commit / push / staging performed.
  HEAD at run end MUST remain cc747df (see 06_REPORT modification control).

## HASH PINS (each re-verified by this executor with a fresh SHA256 computation)

| Pin | Expected | This run's fresh value | Result |
|---|---|---|---|
| Desktop pre-registered baseline `M1_BASELINE_AUDIT_20260926.md` | BF867E820AF6FFCF836E5B1810CEF2739D0043452597C52EE79B4FC8283E3FB1 | BF867E820AF6FFCF836E5B1810CEF2739D0043452597C52EE79B4FC8283E3FB1 | MATCH |
| VegetationClimates.bnt (pcg_install, 25,346 B) | 7B858401C3EEBDA574DF4B4517E7FB2A8149C283885F27187682AA1239C745F4 | 7B858401C3EEBDA574DF4B4517E7FB2A8149C283885F27187682AA1239C745F4 | MATCH |
| 25.vcl payload (BNT offset 17286, size 1030, sliced from raw bytes) | 89ACABE78A812F344F03F5FEB48BECA529D9B2545682CD77505675C21B513E45 | 89ACABE78A812F344F03F5FEB48BECA529D9B2545682CD77505675C21B513E45 (re-derived independently: [System.IO.File] slice + SHA256; re-confirmed by the F02 census probe) | MATCH |
| M1_GATE_DELIVERABLE_MATRIX_V4.md | EC04FC47... (prefix pin) | EC04FC471C55450DF060E5E3441A92584BB0CB7C4C63ED1E223C20F0BE732552 | MATCH |
| M1_GATE_DELIVERABLE_MATRIX_V4.json | 003056AC... (prefix pin) | 003056AC0210A7E0C33F304232F2F366D45D4E94B04D9984FA03B62D06CB4A95 | MATCH |
| EVIDENCE_MANIFEST_V4.json | 9944925D... (prefix pin) | 9944925D1489771B9D5EA99A8AF834E363FBFF9BC49D73BB0999DC8706217D90 | MATCH |
| Entropia.exe PCG_9_3_5 (8,015,872 B) | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (F05 probe re-hash) | MATCH |

## DESKTOP ARTIFACT INTEGRITY (cross-checked against GATEC_ARTIFACT_SHA256.csv)

All 9 Desktop artifacts re-hashed by this executor; all MATCH the CSV's listed values
(GATEC_REPORT 506391CD..., gatec_checks.mjs ECA9B3B9..., gatec_terrain_and_records.mjs
6704DDB1..., gatec_supplement.mjs E3DE566B..., GATEC_PHYSICAL_CHECKS.json 5A19CAE4...,
GATEC_TERRAIN_RECORD_CHECKS.json E353F924..., GATEC_SUPPLEMENT.json F1174ECF...,
GATEC_V4_SOURCE_HASHES.json 1EC1EA54..., GATEC_CORRECTIVE_PROMPT_20260926.txt
492EB4F4...). GATEC_ARTIFACT_SHA256.csv itself hashes FA7D4755C5A7DB77598292AD9BBDAAA6
897C4106059E9DDD517A26D0C9B1806 (not self-listed; recorded here).

## INDEPENDENCE NOTE

Desktop's scripts/outputs were READ as claims; every load-bearing number in this
package was RE-DERIVED from physical sources with this run's own probes
(03_EVIDENCE/scripts/r1_*.mjs + the python RUN copy), then cross-compared (agreement
and differences recorded per finding — see FINDINGS.csv and the 02_ANALYSIS files).

## TOOLING PIN

- node = repo runtime: v22.22.0 (process.version recorded in every probe output)
- python (historical-generator behavior test) = D:\Eudoria_Reconstruction\10_Scripts\
  python_env\python.exe = Python 3.12.7 (the historical generator copy run)
- PowerShell 5.1 orchestration; no packages installed; no source files modified
  beyond the three authorized paths (see MODIFIED_PATHS.csv).
