# 03_EVIDENCE — PE_935_SF_ARG2_PROVENANCE_R1_20260914

Evidence index for the run. `EVIDENCE_INDEX.csv` lists every raw/analysis/report
artifact with its generator, generator-hash pointer, executed command,
environment, exact counts, independent truth source, negative controls,
limitations and dependency links.

**Hash convention (no hand-copied hashes):** no hash string in this package is
hand-copied as evidence. All hashes are script-computed at measurement time
(hashlib inside the run scripts) and live in the canonical registries:

- `00_CONTROL/SCRIPT_SHA256.csv` — SHA256 of every run script (generator hashes).
- `06_REPORT/MANIFEST_SHA256.csv` — SHA256 of every package file.

The `generator_sha256` column of `EVIDENCE_INDEX.csv` is therefore a POINTER
(`<SCRIPT_SHA256.csv>` = resolve the generator's hash from the script registry;
`<MANIFEST_SHA256.csv>` = resolve the artifact's own hash from the manifest
registry). The three formalize-time 00_CONTROL files (RUN_CONTRACT.md,
SOURCE_IDENTITIES.json, GIT_OBSERVATIONS_AT_FORMALIZE.md) are IMMUTABLE INPUTS
from pe-master-auditor; their hashes are pinned in SOURCE_IDENTITIES.json (the
formalizer's own measurements).

**Environment:** interpreter
`D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe` (Python 3.12.7
measured at run time, recorded in every script header and every raw artifact);
capstone 5.0.7 measured (`capstone.__version__` + `capstone.__file__` recorded
per artifact; the 5.0.9 dist-info label is a known false label). Every script
was run with `-B` (no `__pycache__`, no `.pyc` in the package). Every script
fail-closed on the pinned EXE identity (SHA256+SIZE+PE32) before any analysis
byte read; the S0 PASS record is embedded in every raw artifact.

**Negative controls executed:** NC-1 (ABI pins, 9/9 byte-exact — PASS),
NC-2 (census rejects 5 non-SF slot-3 receivers — PASS), NC-3 (zero in-scope
literals; machinery demo on a known .rdata literal — recorded), NC-4 (vtable
entry dword — MATCH). Calibrations: CAL-1 (imm32 scanner — PASS), CAL-2 (E8
census — PASS), CAL-3 (receiver tracer known-answer — PASS, self-added).
