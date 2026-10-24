# PUBLIC_SOURCE_SUMMARY — what sources the campaign used (sanitized)

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024.

## Primary corpus (private, physical provenance)

- **PE42_EN_80553A75**: pe42_en.exe installer (CAB MSZip, 525 581 323 B,
  SHA256 80553A75…), fully extracted: 711 files / 841 093 330 B, every file
  hashed into INSTALL_MANIFEST.csv. Client PE.exe (4.02.0000 COT,
  53A6F341…, UPX) — byte-identical to the pre-existing PE_CD.exe; its
  `upx -d` product is byte-identical to the pre-existing unpacked image
  (56178993…), on which all static RE ran.
- ARK corpus: Models.ark (2492 members, all NIF), Textures.ark (4833),
  Scripts.ark (1937), Volumes.ark (831 .bvi = 7032 records × 48 B) —
  byte-identical across 3 physical copies.
- Terrain: 50.bnt PE42 version (8E43CD14…, 116 528 920 B); a second,
  different 50.bnt version (A6E59EE0…, 118 016 977 B) exists in a
  comparative copy — era split, neither decoded.

## Comparative corpora

- ISO NOV2003 (884692A8…): container DEGRADED (truncated ~744 KB);
  member ProjectEntropia.zip (4AB9AD40…) PASS; inner PE_PCG.exe
  (F74BE3AC…) NSIS_EXTRACT_BLOCKED at data block #40 — PCG demo content
  UNVERIFIED against the PE42 corpus.
- 9.3.5-era history (oracles only, era transfer NOT claimed): templates.vfs
  template facts for definitions 4508/4057, the 10.1.0.0 variant of model
  218757, GAMEBRYO oracle rules. One 9.3.5 primary history report is a
  MISSING_HISTORY_ARTIFACT (flagged honestly; 2003-side re-derivation closed
  the affected pairing independently via E18).

## What is published here and what is not

Published: own documentation, hashes, offsets/VAs, structural facts, own
parser code (path-parameterized). NOT published (see EXCLUDED_ARTIFACTS.md):
game binaries, installers, ARK/NIF/BVI payloads, terrain, decoded Scripts
blobs, raw disassembly, keys, dumps, DB, authoring prompts.
