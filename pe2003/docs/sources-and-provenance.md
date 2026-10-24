# Sources and provenance — PE 2003 campaign

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024.
Sanitized public summary of the private provenance manifests
(`PE2003\01_Source_Manifests\{SOURCE_CATALOG, BUILD_IDENTITY, MEDIA_INTEGRITY,
BINARY_PROVENANCE_GRAPH}.json`). Hashes and relations only — no game payloads.

## Corpus identities (SHA256)

| Corpus | Kind | Size (B) | SHA256 | Status |
|---|---|---|---|---|
| pe42_en.exe | installer (CAB MSZip) | 525 581 323 | 80553A75EED5117B194BD3382727F993970336607F62DE8A3807427DCA99F27B | PASS — 711 files, 841 093 330 B uncompressed, every file hashed |
| PE.exe (PE42 install) | client, UPX-packed | 753 664 | 53A6F341BF75E6F16439DD290DC14BECCFD294AB1AE520E2398428074DC1C01 | primary client (4.02.0000 COT, 2003-01-30 12:33:07 UTC) |
| PE_CD.exe | client (comparative copy) | 753 664 | 53A6F341… (same) | IDENTICAL_BYTES to PE42 PE.exe |
| PE2_unpacked_out.exe | client, unpacked | 2 207 744 | 56178993692A7409C8963398089E482EDDF96177666BACB91A8CC1A638D9A0650 | `upx -d` product of PE42 PE.exe == pre-existing unpacked image (established causally by the R1a upx experiment); all static RE ran on this build |
| Models.ark | game archive | 128 742 137 | F660D055B4B9471B3B6E16B07F5368DBD6F2208DAB6B51BB9BDB9942BD73EA62 | HASH_EQUAL_COPY across 3 physical locations |
| Textures.ark | game archive | 289 585 581 | D611D1257D2E5433B6DF218D671AA60D003C5C6587858757C7AF3219BB739B80 | HASH_EQUAL_COPY ×3 |
| Scripts.ark | game archive | 5 662 913 | 1701D696A5A211146F33C253B89E6EA5E501E1C2405AF1816A4BEA07BABA85AE | HASH_EQUAL_COPY ×3 |
| Volumes.ark | game archive | 416 728 | 68EFF073917510B19163F00EDF25FEDA3BBC0EF057C55924D1295A53057A0FC2 | HASH_EQUAL_COPY ×3 |
| 50.bnt (PE42 version) | terrain | 116 528 920 | 8E43CD143BC44E62A5BF79B46F7D339D976803158D3AC85F82E0C6ED84A76665 | catalogued, NOT decoded |
| 50.bnt (other copy) | terrain | 118 016 977 | A6E59EE07A51EAC06A3E75DA5421E5928D59EDED74F096DCAD04CE80ED01DA00 | DIFFERENT VERSION — era split, do not mix |
| Project Entropia.msi | installer metadata | 40 293 888 | CD6FDDE33F1AC0FD0863F4C2756066C594BBD33976A14400BB8B1CF13F951514 | ProductVersion 4.02.0000, MindArk |
| PC Gamer November 2003.iso | media container | 670 306 304 | 884692A8ECE40EB9862F60AA87DA0BFB25769E9048F6584DFB2BA5073E38C41C | MEDIA_CONTAINER_INTEGRITY=DEGRADED (7z listing exit 2: "Unexpected end of archive"; truncated ~744 KB vs volume descriptor) |
| ProjectEntropia.zip (ISO member) | zip payload | 157 622 829 | 4AB9AD40BB8481026C562C9C93E3F7DF3D0034D6DFB371BFEFD0F06077B37737 | SELECTED_PAYLOAD_INTEGRITY=PASS (7z t exit 0) |
| PE_PCG.exe (PCG demo) | NSIS installer | 157 629 853 | F74BE3ACD2D8894ECB815C6AC3AB28D724646CE384F31430F055D51130F26F75 | NSIS_EXTRACT_BLOCKED at data block #40 (0x1D7A238); 40/40 parsed blocks clean; inner content UNVERIFIED vs PE42 corpus |

## Provenance graph (relations)

- ISO NOV2003 → CONTAINS_MEMBER → ProjectEntropia.zip → CONTAINS_FILE →
  PE_PCG.exe → EXTRACTION_BLOCKED (NSIS block #40).
- pe42_en.exe (CAB) → CONTAINS → PE.exe + 4 ARK archives + Terrain\50.bnt
  (+ 706 further files, all in INSTALL_MANIFEST.csv).
- PE.exe == PE_CD.exe (IDENTICAL_BYTES, both re-hashed).
- PE.exe --upx -d--> PE2_unpacked_out.exe (causal relation established R1a;
  the earlier UNVERIFIED_RELATION record in BINARY_PROVENANCE_GRAPH is
  superseded — see CORRECTION_LEDGER CLR-09 in the private run package).
- ARK corpus: three independent physical copies (PE42 install /
  pre-existing ARK folder / pre-existing pcg2003_install folder) are
  byte-identical (HASH_EQUAL_COPY) — one corpus, three locations.

## Separation statements

- Container-level truncation (ISO DEGRADED) is INDEPENDENT of payload-level
  verification (member ZIP PASS). No inference between the two.
- Client-binary identity (53A6F341 ↔ 56178993) is a byte/hash + causal-experiment
  relation, not an assumption; the 9.3.5-era VA base applies to build 56178993.
- manifest_2003.csv is a MIXED_CORPUS_LOCATOR, not an era proof: its row for
  218757 carries the 9.3.5 payload (57 316 B, 3E8A22C2…, NIF 10.1.0.0), while
  the physical 2003 corpus holds a different payload (56 535 B, C13D0873…,
  NIF 4.1.0.12) — the row for 296445 happens to match. Verified physically.

## Source-material status summary

| Item | Status |
|---|---|
| pe42_en.exe CAB extraction | PASS (primary researched corpus) |
| ISO NOV2003 | DEGRADED container; member ZIP PASS; PCG demo inner content UNVERIFIED (frontier item) |
| PE42 client binary chain | CONFIRMED (MSI Property table + PE header + upx experiment) |
| ARK corpus identity | CONFIRMED (3-location hash equality) |
| Terrain | TWO versions catalogued; NOT decoded (explicit authorization required) |
