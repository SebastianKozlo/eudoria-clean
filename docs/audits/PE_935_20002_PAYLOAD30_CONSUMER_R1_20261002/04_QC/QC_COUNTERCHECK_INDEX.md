# QC_COUNTERCHECK_INDEX — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

Index of the internal-QC counterchecks (contract §C). QC wrote ONLY inside `04_QC\`.
All QC tools are the QC worker's own implementations (no code shared with the
executor's 03_SCRIPTS or with JOIN R1's vfs_common.py). Every result artifact carries
its own method + result fields; the report is `04_QC\QC_REPORT.md`.

## Tools (04_QC\qc_tools\)

| TOOL | SHA256 | SIZE (B) | PURPOSE |
|---|---|---|---|
| qc_tools\qc1_reparse_vfs.py | 04D6D62ED94DBA2309712B3D3C853A02BF3178E1730D90D129EF1DE823C28600 | 14,327 | Independent framing/TLV/census re-parse of 20002.vfs + full comparison vs executor artifacts (duty 2) |
| qc_tools\qc2_pinverify.py | 6AEA2E5C3232192E73F7C3EB75EF66BAFA001D85E038AF76C1BDBE731B30B4CC | 7,654 | Independent 45-pin byte verification + own PE32 VA→RVA→FO conversion + headline hand-decode (duty 3) |
| qc_tools\qc3_negcontrols.py | 9346DD61857BD70135CEC86467C3E1C1D42960A91C81F92AF62BBFFE09D552C8 | 10,526 | QC-crafted negative controls + independent imm32/mangling census (duty 5, dispatch probes) |
| qc_tools\qc4_rtti_edges.py | 633200D5A543063A7337212E2EBA420D8F4B24F5582ED2B35DA582BE23070173 | 8,961 | RTTI chain walk + independent call-edge census (E8 rel32) + EnvironmentZones string census + FUN_0070e810 probe (risk probes) |
| qc_tools\qc4b_canonconflict.py | 87EDBBF4913C192491DF42B4F713983F8D0817692FDC464425D5CBFD61180F21 | 6,374 | "textures" literal probe + family edge census + JOIN R1 claim-5 pin re-measurement (canon conflict) |
| qc_tools\qc5_denominators.py | 3050EEE704D71E40B6FDEB54214CE4567A9881567849CBFC29D004510F50FDAF | 9,480 | Denominator recomputation + manifest census/spot re-hash + EVIDENCE_INDEX census + JOIN R1 spot-check (duties 6, 8, 9) |

## Result artifacts (04_QC\)

| ARTIFACT | SHA256 | SIZE (B) | CONTENT |
|---|---|---|---|
| QC1_REPARSE_RESULT.json | 878F79177C7D1DA82F69D0A8F06F564D464FCCE5F32AE5EA80AA0AA5F848D48A | 3,500 | Independent walk: 1366 records, exact EOF (base tests incl. base=64 non-discriminating and base=256 divergence documented), full census (sizes {56}, ver {1}, crc {0} ×1366 — CRC-gate-skip re-derived; flags 0x80 ×1366; count 6 ×1366; u32@0 = 20002; u16@2E = 0x11 ×1366; zeros [1014,1015]; 142 distinct values), TLV grammar re-derivation (shape (1,12,13,14,16,17)+tail 0 in 1366/1366; tag-0x11 value at +0x30 in 1366/1366), anchors (record 0 + record 1014, payload hex), and the 1366-row field-by-field comparison vs the executor (ALL agree; anchor agreement incl. payload hex) |
| QC2_PINVERIFY_RESULT.json | A99CF4141383B245115B5630BB604B8B82046D8B18F736A2CAD1ED749165A965 | 18,775 | All 45 pins: own section table (.text/.rdata/.data vaddr==rawptr → fo==RVA; .tls/.rsrc differ — table emitted), per-pin FO-conversion verdict + measured bytes vs recorded bytes: 45/45 OK, 0 bad; headline read/store conversions + FUN_00412540 window hand-decode with the pure-copy verdict |
| QC3_NEGCONTROLS_RESULT.json | 19F042063089D68B75F587D1857B6B25475A2631D3E698D6AF79B402001D52FA | 4,966 | NCQ1a–e (own corruption classes: size→55 bounds-flag, ver→7 FAIL, magic-flip FAIL, truncate-100 FAIL, id-garbage non-failure control), NCQ2 wrong-displacement (+0x2C/+0x34 histograms vs +0x30), NCQ3 independent census (imm32 0x4E22 = 3 @ identical offsets; ASCII 20002 = 0; $0EOCC@/$0EOCG@ = 2/2; family identical), NCQ4 TLV-absence falsifier (count=5 → predicate FALSE) |
| QC4_RTTI_EDGES_RESULT.json | 9ED0A8C082B5C2F9F3D09740D0E04A908A2BBFE77710390176538EBA9B5BA553 | 9,726 | RTTI chains (0xA86FE0→…→`.?AV?$ArkObjectClassImpl@VArkParameterArmor@@$0EOCC@@@`; 0xA878BC→…→`.?AVArkParameterArmor@@` + vtable slots), independent call-edge census (FUN_0075f660=1, FUN_0070c180=202, FUN_0070c680=1@0x703EF0, family edges, FUN_0040e900 sites — none in FUN_0070e810), EnvironmentZones string census (1 string, 1 code ref), FUN_0070e810 window probe + JOIN R1 pin @0x70E841 re-measured |
| QC4B_CANONCONFLICT_PROBE.json | CDC6D48944BE7A780FFEE7829E3546068E320B7CEB68416D3F21A1ABC01558BB | 1,982 | "textures" @0xA86858 ref @0x70E4AE (inside FUN_0070e470); callers of FUN_0094b9e0 (0x94E05A ∈ FUN_0094dfc0), FUN_0094e470 (0x94EA9C ∈ FUN_0094e890), FUN_0094e390 (0x94E745 ∈ FUN_0094e610), FUN_004172A0 (0x40558B); JOIN R1 pins: 83 42 04 @0x94D9F5 OK, C7 44 24 1C 80 00 00 00 @0x70E841 (8-byte instruction; 6-byte historical citation = truncated transcription); "Data\Parameters\" @0xA97E58 |
| QC5_DENOMINATORS_RESULT.json | 69C473BA9CB480E99BCBCC250607BF454355EDD075AACFD103150307ADEDCA5B | 11,282 | All denominators recomputed from raw artifacts (1366/1366/45/202/2 all reproduce); package file census (364 outside 04_QC = 363 manifest rows + manifest; HANDOFF's 363/362 off-by-one → P3-4); manifest↔disk perfect (0 missing/0 stale); 14/14 spot re-hash OK; EVIDENCE_INDEX census (20 artifacts, 0 missing); JOIN R1 spot-check 10/10 SHA+size OK |
| QC_REPORT.md | 2D83DE3B290EDB3A50697E5B9B072B46CE18F13E76F976C52B25CA86668C2885 | 41,648 | The QC report: verdict PASS_WITH_FINDINGS; findings P2-1, P2-2, P3-1..P3-5 + limitations L-1/L-2; gate-strength audit S0–S8; risk-probe results; canon-conflict description; incident verification; taxonomy check; coverage/NOT_CHECKED |

## Key numbers (QC vs executor)

| QUANTITY | EXECUTOR | QC (independent) | AGREE |
|---|---|---|---|
| Record count / exact EOF | 1,366 / exact | 1,366 / exact (own walk; base from header; stride-sum check TRUE) | YES |
| Anchored record 0 +0x30 | fo 80, `BB 2E 00 00`, 11963 | fo 80, `bb2e0000`, 11963 (+ full payload hex equal) | YES |
| ANCHOR_ZERO | rec 1014, fo 129872, value 0 | rec 1014 (zeros exactly {1014,1015}), fo 129872, value 0 (+ payload hex equal) | YES |
| TLV walk | 1366/1366 shape {1,12,13,14,16,17}, tail 0, tag-0x11 value @ +0x30 | 1366/1366 identical (own grammar derivation, count-field-corrected V2 walk) | YES |
| crc fields | all 0 (gate skipped) | all 0 in 1366/1366 (own walk) + gate pins @0x971B4A/4C byte-verified | YES |
| Pins | 45/45 OK | 45/45 OK (own PE parser + own re-read; 0 mismatch) | YES |
| Descriptor-lookup call sites | 202 (0 static tag-0x11 readers; 2 false positives) | 202 by own E8-rel32 census; candidates 0x726A03 + 0x8AEAD5 as documented | YES |
| FUN_0075f660 callers | exactly 1 (0x726A1B) | exactly 1 (0x726A1B) | YES |
| imm32 0x4E22 census | 3 sites (fo 3375514/3384386/3406796) | 3 sites, identical offsets; ASCII 20002 = 0; manglings 2/2; family identical | YES |
| RTTI class identity | ArkObjectClassImpl<…,20002> / ArkParameterArmor | vtable→COL→TD chains byte-walked; names `.?AV?$ArkObjectClassImpl@VArkParameterArmor@@$0EOCC@@@` / `.?AVArkParameterArmor@@` | YES |
| Package file count | 363 (362+manifest) | 364 (363+manifest) — manifest itself consistent | NO → P3-4 |
| FUN_0070E810 attribution (BLAST_RADIUS item 6) | "builds '<classID>.vfs'-style names" → PRIOR_CLAIMS_CONFIRMED | FUN_0070E810 builds param+"textures"+".vfs" (string 0xA86858; no itoa; open @0x70E8B6); the classID mechanism is FUN_0070c680's | NO → P2-1 |

## Boundary statement

QC modified NOTHING outside `04_QC\`. The executor's artifacts, the JOIN R1 package,
the git tree (no stage/commit; HEAD == BASE_SHA == origin/master at QC end), and both
pinned binaries were accessed read-only. No client process was launched; no runtime
evidence produced; STATIC_ONLY discipline preserved end-to-end.
