# SOURCE INDEX - EU935_M1_FULL_MILESTONE_AUDIT_R1_20260916

All physical payloads are LOCAL-ONLY (under `D:\Eudoria_Reconstruction` and the
repo working tree); they are represented here by identity metadata only and are
never committed. Rows 1-5 and 7-9 carry PE-MASTER's fresh session re-hashes
persisted verbatim from the audit contract. Row 6 was recomputed at this
persistence per the contract's explicit instruction (byte content verified).
Row 10's three repo files were independently re-hashed at this persistence by
pe-master-auditor: all three MATCH.

| # | PHYSICAL_SOURCE | ERA | SIZE (B) | SHA256 | CANONICAL_PRIOR_RECORD | FRESH_REHASH_RESULT | NOTE |
|---|---|---|---|---|---|---|---|
| 1 | pcg_install\Entropia.exe | PCG_9_3_5 (9.3.5.6746) | 8,015,872 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | matches all M1 static-run pins (LINK30/SLOT-CENSUS/GEOREF reviews) | MATCH | THE 9.3.5 address-level binary. |
| 2 | 01_Original_Files\Binary\Entropia.exe (== 01_Original_Files\EntropiaUniverse_Runtime\Binaries\Entropia.exe) | DIFFERENT-ERA binary | 8,445,952 | E706C7152FB4874AB73779AC5F18E1259BB4373EFC5235E9F4FCB32FF1A6243B | documented in georef PE_MASTER_REVIEW as never-to-be-used for 9.3.5 address claims | MATCH (with the documented era warning) | recorded to prevent accidental cross-era use. |
| 3 | pcg_install\Data\Models\Models.bnt | PCG_9_3_5 | 395,412,868 | C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0 | canonical pin (assignment §0B) | MATCH | |
| 4 | pcg_install\Data\Textures\Textures.bnt | PCG_9_3_5 | 973,942,771 | 61ACD13B140E130647EEE24C1E2669D3734990B76CF74897DDD3BA0F4EA61393 | V4 matrix row 8 pin | MATCH | |
| 5 | pcg_install\Data\Terrain\terrain.bnt | PCG_9_3_5 | 125,064,817 | 95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990 | size pin in georef report (125,064,817 B); full SHA256 NOT_PROVIDED in the records read -> THIS AUDIT RECORDS IT AS THE FRESH PIN (audit finding F4, P3) | FRESH PIN | |
| 6 | pcg_install\Data\Textures\Terrain.bnt (12-byte stub) | PCG_9_3_5 | 12 | FC0168D5B7E993098B97812B4EDAAD51B578AEEC47F0E29605B494E09540171D | RUN-4/cellstream review byte-exact record | RECOMPUTED AT THIS PERSISTENCE (per the contract's explicit instruction): byte content verified == 00 00 00 00 00 00 00 00 42 4E 54 32; SHA256 recorded as the fresh pin | BNT2 writer's zero-entry stub (install-time orphan); row 18 second-provider REJECTION record. |
| 7 | pcg915_install\Data\vegetationclimates\VegetationClimates.bnt AND 01_Original_Files\BNT_Models\VegetationClimates.bnt | PCG_9_3_5 + JUL_2003 copies | 25,346 each | 7B858401C3EEBDA574DF4B4517E7FB2A8149C283885F27187682AA1239C745F4 (BOTH, byte-identical) | V4 row 7 pin + JUL==PCG byte-identity claim | MATCH (byte-identity independently re-verified) | |
| 8 | 01_Original_Files\BNT\50.bnt | JUL_2003 | 118,016,977 | A6E59EE07A51EAC06A3E75DA5421E5928D59EDED74F096DCAD04CE80ED01DA00 | (no prior full-hash pin relied on) | FRESH PIN (no truncated-hash reliance) | recorded. |
| 9 | 01_Original_Files\BNT_Models\Textures.bnt | JUL_2003-era corpus copy | 850,681,602 | 2EAE115958D3157FA62F8CBFBAC6F4BFB5C38A820F1D05F9248C4200C0208A56 | (no prior full-hash pin relied on) | FRESH PIN | recorded (era-labeled). |
| 10 | V4.1 package identities (repo files, this session): GATES\M1_GATE_DELIVERABLE_MATRIX_V4.md; GATES\M1_GATE_DELIVERABLE_MATRIX_V4.json; EVIDENCE_MANIFEST_V4.json (paths under docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/) | repo (multi-era content) | 68,176 / 78,096 / 134,472 | EC04FC471C55450DF060E5E3441A92584BB0CB7C4C63ED1E223C20F0BE732552 / 003056AC0210A7E0C33F304232F2F366D45D4E94B04D9984FA03B62D06CB4A95 / 9944925D1489771B9D5EA99A8AF834E363FBFF9BC49D73BB0999DC8706217D90 | the V4.1 LIVE deliverable matrix + evidence manifest (shorthand identifiers in prior records) | MATCH - all three shorthand identifiers RESOLVED to real full hashes; independently re-hashed at this persistence by pe-master-auditor: all three byte-identical to the contract pins | the LIVE Gate-B deliverable lineage objects. |

## PERSISTENCE-LEVEL HASH VERIFICATION NOTE

At this persistence, pe-master-auditor independently re-hashed every REPO-file
row above (row 10: all three MATCH) and recomputed row 6's stub hash after
byte-content verification. Rows 1-5, 7-9 (LOCAL-ONLY physical payloads) carry
PE-MASTER's fresh session re-hashes persisted verbatim; their sizes were
independently re-checked at persistence and match the recorded SIZE column
(8,015,872 / 8,445,952 / 395,412,868 / 973,942,771 / 125,064,817 / 12 /
25,346 / 25,346 / 118,016,977 / 850,681,602 bytes - all confirmed on disk).
