# SOURCE_COVERAGE_SUMMARY — PE2003_MODEL_INSTANCE_PLACEMENT_STATIC_R1_20261024

Local 2003 source coverage for the placement question (full private tables: LOCAL_SOURCE_COVERAGE.csv, LOCAL_SOURCE_COVERAGE_FILE_CLASSES.csv, CORPUS_INSTANCE_CENSUS.json).

| Channel | Denominator | Verdict |
|---|---|---|
| Decoded script corpus (Scripts.ark DLOB) | 1936/1936 members full literal census (independently rescanned) | ZERO external references to defs 4508/4057 or resource ids 296445/296446/218757/218758; self-only |
| Definitions' own bytecode incl. EXTN fixup path | 4508+4057+1796+4751+477+343 = 7134 dwords whole-file | 0 positional f32-triples; 0 dispatch-B placement calls |
| EXE static writers (transform fields) | full-image census + blind spots (LEA-indirect, rep/memcpy, EBP-held) | writer set = {default reset, default-init ctors, GCE sub-model setters, FUN_005030c0 (network-source, record[6] entities)}; no local statics' world-position writer |
| Terrain 50.bnt | 51921/51921 members at consumer-code level; 75/75 residues chunk-decoded (exact EOF) | terrain-only (height + material chunks incl. new type-3 gradient layer); zero id/transform structures |
| Install file classes | 704 files, all classes | zero unexamined class with placement potential |
| 2234.obj plaintext | 2607/2607 records | crafting recipes; unrelated; closed |
| Volumes .bvi (296446/218758) | scan coverage: 526 raw slot+4 sites ABI-filtered, 47 lower_bound callers, 4 negative scans | volume consumer NOT FOUND within coverage (bounded negative); dead-registration hypothesis needs runtime |
| UDP wire format | transport module 0x5BB000-0x5C7000 full census | definitions carried as records 0x1C; TLV tag0/tag3 floats = generic definition fields, NOT root positions; root positions = struct 0x48 (record[6] entities) |

LOCAL_SOURCE_EXHAUSTED = NO (global claim not made): static branches exhausted; server/runtime channel remains (out of this campaign's scope by human order).
