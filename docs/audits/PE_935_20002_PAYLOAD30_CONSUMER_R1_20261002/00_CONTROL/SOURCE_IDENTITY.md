# SOURCE_IDENTITY — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

ERA = EU 9.3.5 / PCG 9.3.5 (PCG_9_3_5 corpus; "pcg_install")
BUILD = Entropia Universe 9.3.5.6746 (FileVersion/ProductVersion from the pinned EXE; LastWriteTime 2008-09-17)

## Pinned physical inputs (S0-measured; see 00_CONTROL\PREFLIGHT.md)

| ROLE | PATH | SIZE (B) | SHA256 |
|---|---|---|---|
| CLIENT BINARY (static analysis target; NEVER launched) | D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8015872 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 |
| DATA FILE (the traced VFS) | D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs | 174864 | C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4 |
| REPO HEAD (read-only; no commit/stage/push) | D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean @ HEAD 9203b6d1ad5025f4158d5165863594132aaac49f | — | — |

## Ghidra binary-identity chain (per PREFLIGHT_EXPECTED.md requirement)

Ghidra headless (if/when used) imports a COPY of the pinned EXE; the executor records the
imported copy's SHA256 and asserts copy SHA256 == pinned SHA256 before using any Ghidra
output. Every load-bearing instruction claim in this run is byte-pinned by reading the
PINNED physical EXE at its FILE_OFFSET directly (independent of Ghidra); see
01_RAW\CLIENT_READ_BYTES.* and 03_SCRIPTS byte-pin scripts.

## Prior-evidence inputs (READ-ONLY reference; LEADS_TO_REVERIFY, not truth)

- docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928\04_TOOLS\vfs_common.py
  (prior ArkVFS reader; used ONLY as cross-validation of the executor's own in-run framing parse)
- docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928\03_COUNTERCHECKS\AMEND_R2\AMEND_R2_ID2_MEMBERSHIP_20002_48.json
  (prior +0x30/-as-+48 id2-domain membership observation; CONTEXT ONLY)
- docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928\01_RAW\GHIDRA_OUT\* (prior decompilations; candidate leads)
- D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs (prior-evidence context; bounded reads)

STATIC_ONLY = YES; RUNTIME_EXECUTION_PERFORMED = NO (the client is never launched; no hooks; no instrumentation).
