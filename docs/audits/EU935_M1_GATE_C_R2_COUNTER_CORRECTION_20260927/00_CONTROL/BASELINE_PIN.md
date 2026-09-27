# BASELINE PIN — EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927

Git pin at run start (re-verified by the executor at S0, 2026-09-27):

- Repo: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean; branch master.
- BASE_SHA = HEAD = origin/master (local tracking ref) =
  cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d.
- Staged: NONE. Tracked modified EXACTLY 3:
  AUDIT_ENTRYPOINT.md (+1/-0), src/pesource/VegetationClimateDecoder.js
  (+30/-6), src/peworld/PEFoliageCore.js (+20/-5).
- Untracked roots: the R1 predecessor package (49 files),
  docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/ (DO NOT TOUCH),
  experiments/ (DO NOT TOUCH).
- This run performed NO git add/commit/push/stash/checkout/reset. HEAD remains
  cc747df at handoff. Persistence is a LATER, separate phase (another worker).

## Hash-pin table (expected vs the executor's FRESH value at S0)

| Pin | Expected | Fresh (measured) | MATCH/DIFF |
|---|---|---|---|
| Contract file SHA256 | E0FFAB0C1BB8B5F4455948C2B52297A95D14026C02555BFD5A34F665F205A77F | E0FFAB0C1BB8B5F4455948C2B52297A95D14026C02555BFD5A34F665F205A77F (20165 B) | MATCH |
| F03_TERRAIN_TEXTURE_SCOPE.md | 5704D1C8F8166FE5BF1B88B0E8D0B13E7A0DE3AC83463BDAF920831E863489DF, 9807 B | 5704D1C8F8166FE5BF1B88B0E8D0B13E7A0DE3AC83463BDAF920831E863489DF, 9807 B | MATCH |
| EVIDENCE_INDEX.csv | 02E03B7D073E5579123A95B03383BAC26CEBFF46E83A24B36A1693CAEDD05B08, 7536 B | 02E03B7D073E5579123A95B03383BAC26CEBFF46E83A24B36A1693CAEDD05B08, 7536 B | MATCH |
| MANIFEST_SHA256.csv | 3A91F3A3505F6F3D46EDEE246FF91E26B373586D32803E57E18D6DA4D1C46462, 8520 B | 3A91F3A3505F6F3D46EDEE246FF91E26B373586D32803E57E18D6DA4D1C46462, 8520 B | MATCH |
| AUDIT_ENTRYPOINT.md | 8EEC84E65C19B56705B023AADAB27B5AD0A05E03686E5992F4C47A4836BEE45E, 113685 B | 8EEC84E65C19B56705B023AADAB27B5AD0A05E03686E5992F4C47A4836BEE45E, 113685 B | MATCH |
| DIFF_PEFoliageCore.js.patch | 27DEE19810FDED98FBE37E2013B742DA500BCD107AD0C85FEAFBCCDBF1EA96DD, 3377 B | 27DEE19810FDED98FBE37E2013B742DA500BCD107AD0C85FEAFBCCDBF1EA96DD, 3377 B | MATCH |
| DIFF_VegetationClimateDecoder.js.patch | 5978FF6B3CD9C787284B829E59D8CCCF18D14D0FA956B6D760D86C4278728723, 3389 B | 5978FF6B3CD9C787284B829E59D8CCCF18D14D0FA956B6D760D86C4278728723, 3389 B | MATCH |
| terrain.bnt | 95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990, 125064817 B | 95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990, 125064817 B | MATCH |
| VegetationClimates.bnt | 7B858401C3EEBDA574DF4B4517E7FB2A8149C283885F27187682AA1239C745F4, 25346 B | 7B858401C3EEBDA574DF4B4517E7FB2A8149C283885F27187682AA1239C745F4, 25346 B | MATCH |
| live git diff == DIFF_PEFoliageCore.js.patch bytes | 27DEE198... (byte-identical) | raw buffer SHA256 27dee19810fded98fbe37e2013b742da500bcd107ad0c85feafbccdbf1ea96dd, 3377 B | MATCH |
| live git diff == DIFF_VegetationClimateDecoder.js.patch bytes | 5978FF6B... (byte-identical) | raw buffer SHA256 5978ff6b3cd9c787284b829e59d8cccf18d14d0fa956b6d760d86c4278728723, 3389 B | MATCH |
| R1 package file count | 49 files | 49 files | MATCH |

## Deviation record (S0)

- The live network fetch of remote master (git ls-remote github.com) FAILED in
  this environment (no outbound connectivity; connection timeout). The pinned
  local tracking ref origin/master = cc747df = HEAD matched exactly. NO
  fetch/push/pull was attempted at any point of this run, so the remote cannot
  have drifted due to this run. Recorded as an environment deviation, NOT a
  state mismatch. Persistence/remote verification belongs to the LATER
  persistence phase (another worker).
- The verbatim contract source file uses ONE final CRLF as its last line
  terminator (byte 20164 of 20165); 00_CONTROL/RUN_CONTRACT.md materializes
  the contract body VERBATIM and therefore preserves that single CRLF. All
  other package files are LF-only.
