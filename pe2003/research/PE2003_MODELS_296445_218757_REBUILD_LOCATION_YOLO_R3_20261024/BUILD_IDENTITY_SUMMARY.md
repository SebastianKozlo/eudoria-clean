# BUILD_IDENTITY_SUMMARY — PE 2003 client build identity (sanitized)

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024.
Source manifests (private): PE2003\01_Source_Manifests\{BUILD_IDENTITY,
SOURCE_CATALOG, MEDIA_INTEGRITY, BINARY_PROVENANCE_GRAPH}.json.

## Client product identity

- Product: **Project Entropia 4.02.0000** (MSI Property table: ProductName
  "Project Entropia", Manufacturer MindArk; corroborated by the read-me and
  conditions-of-use files dated 2003-01-23) — the "Commercial Open Trial"
  distribution.
- PE header (PE.exe, 753 664 B, SHA256 53A6F341…): PE32 i386, image base
  0x00400000, entry RVA 0x00226C50, linker 6.0, sections UPX0/UPX1/.rsrc,
  TimeDateStamp 1043929987 = 2003-01-30 12:33:07 UTC.

## Binary relations (physically established)

1. PE42 PE.exe == PE_CD.exe — IDENTICAL_BYTES (both re-hashed; the PE42
   download client IS the CD trial client binary).
2. PE42 PE.exe --upx -d (UPX 1.20 payload; tool upx 4.2.4) ==>
   PE2_unpacked_out.exe (2 207 744 B, SHA256 56178993…) — IDENTICAL_BYTES.
   Established causally by the R1a experiment; supersedes the earlier
   UNVERIFIED_RELATION record (correction CLR-09). All static RE of the
   campaign ran on this unpacked build; the 9.3.5-era VA base applies to it.
3. ARK corpus: three physical copies hash-equal (one corpus, three
   locations).
4. manifest_2003.csv row for 218757 = the 9.3.5 payload (57 316 B /
   3E8A22C2… / NIF 10.1.0.0), while the physical 2003 corpus holds
   C13D0873… / 56 535 B / NIF 4.1.0.12 — the manifest is a
   MIXED_CORPUS_LOCATOR, not an era proof (CS06). Row 296445 happens to
   match (656795D8…).

## Media chain

- pe42_en.exe (CAB MSZip): extraction PASS — the primary researched corpus.
- ISO NOV2003: container DEGRADED (truncated ~744 KB vs volume descriptor);
  member ProjectEntropia.zip integrity PASS; inner PE_PCG.exe
  NSIS extraction BLOCKED at data block #40 (40/40 parsed blocks clean) —
  the PCG demo inner content remains UNVERIFIED against the PE42 corpus.
- Terrain 50.bnt: TWO versions (8E43CD14… vs A6E59EE0…); version/era split
  recorded; NOT decoded.

## Standing consequences

- "The 2003 build" in all published VA references means unpacked build
  56178993… of client 4.02.0000 COT.
- No cross-era transfer: 9.3.5 relations are oracles only.
