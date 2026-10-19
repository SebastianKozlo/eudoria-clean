# REPORT — P08 (Front D1, saved-evidence assimilation) — PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018

```text
RUN_ID = PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018
PACKAGE = P08 (Front D, DOCUMENT ASSIMILATION; no body admission)
EXECUTOR_ROLE = pe-reconstruction (child; child scope only)
STARTED_UTC = 2026-10-18T23:02:25Z (real clock, RUN_STARTED.json materialized first)
PACKAGE_HARD_STOP_UTC = 2026-10-19T00:00:00Z
CONTRACT_SHA256 = 12092315AF035249DD11DBA2319B7F03A6290007B0281836155BDE02881ABF4A (verified)
QUESTION (D1) = does the saved corpus contain HISTORICAL world-instance placement values
  (transform values with concrete instance identity + byte/source provenance) for the
  studied objects?
SCOPED_VERDICT = SCOPED_NEGATIVE_WITH_BOUNDS: NO
COUNTERS = 0 bodies / 0 instruction rows / 0 CALL (document assimilation; 5 documents read)
FORBIDDEN_TOUCHED = NONE (no EXE/payload/runtime, no VFS/BNT parsing, no Ghidra, no old
  writer scripts, no config/skills/frozen-root/repo writes)
```

## 1. What was assimilated (checked-sources census)

All five files are corpus documents of the closed SAVED_TEXT_CATALOG (967 files,
CLOSED_SAVED_TEXT_ONLY). Fresh disk SHA256 recomputed for each; all match catalog pins.

| # | Source (role in catalog) | Size | SHA256 (fresh == pin) | Read mode | What it contributes to D1 |
|---|---|---|---|---|---|
| S1 | `PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/06_REPORT/DRAFT_FINAL_REPORT.md` | 15,414 B | 2910289F…B3974 | full | Standing `PLACEMENT_XYZ_RECOVERED=NO` for the FAMILY-T chain (record 4508 → A=296445); documents what transform data WAS found: template payload **list2 (3×vec3) → runtime slot-position lerp** of unknown slot class; placement-record setters as runtime transport; world-instance identity from a physical record NOT ESTABLISHED (CONTROL-2 FAIL → UNKNOWN) |
| S2a | `PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009/HANDOFF.md` | 14,053 B | 0F3082FB…E19C67 | full | Standing `WORLD_XYZ_RECOVERED=NO`, `PE_WORLD_ROOT_IDENTITY=NOT_ESTABLISHED`, `MODEL_GEOMETRY_MATCHES=0` (218757 vs 423020); post-load/post-Update native state NOT_MEASURED |
| S2b | `…SCENE_INSPECTION…/FINAL_REPORT.md` (51,369 B) | — | 8DC5C3CB…498E60 | **relevant sections only** (scope notes; §4.6 scene structure; §4.7 comparison; §5 ceiling; final block) | The only transform values that run produced are **composed FILE_SCENE_SPACE** transforms of 218757.nif internal blocks (e.g. `B_Outpost_me01_Ext_sign:0 → world translate (0, −1030, 820)`), explicitly labeled NOT a placement / NOT world XYZ; classification SINGLE_MODEL, `NO_WORLD_PLACEMENT_EVIDENCE_FOUND`; §5 ceiling verbatim preserved |
| S3a | `PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912/01_CORRECTED/TRANSFORM_TABLE_CORRECTED.csv` | 10,095 B | 4802B9BC…A18664B | full (30 data rows) | The only concrete transform **numbers** for the studied object 296445 in the assimilated set: per-mesh `local_T` (parent-relative), `world_T` (root-relative, tool-composed), superseded R1 column, bboxes — all **model-internal** |
| S3b | `…ERRATA…/01_CORRECTED/00_RAPORT_CORRECTED.md` | 37,893 B | 4B37E2E0…3E9380 | full | **Value provenance** of S3a: own R1 block-map (BLOCKMAP_V2.json, 155/155 blocks byte-exact) mechanically recomputed by errata `analyze_tree_v2.py` (convention `world[i]=parent_world∘local_i` incl. mesh's own transform; root parent=identity; gate G1 with 16/30 unchanged rows as negative control). §3C: **no world placement inside the NIF** ("BRAK W PLIKU"). Ustalenie 9: `NOT_FOUND_IN_SEARCHED_SCOPE` (bounded negative: u32LE+u32BE full Data, decompressed terrain, decoded scripts, VFS both eras). Ustalenie 10: historical position unreachable from the corpus (FIRST_PEINST 0/6; no cache; servers unreachable). PE2/2003 mechanism CONFIRMED **in its own binary only**; 9.3.5 UNVERIFIED ([E-A1]) |

Catalog roles (as pinned): `PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z`,
`PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009`,
`PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912`.

## 2. Transform-like value classification (the D1 core)

Every transform-like value found in the assimilated documents, classified per the
contract's three-way test (**model-internal NIF node transform** vs **world-instance
placement** vs **SDK/control/default zeros**), with provenance and frame:

| Class | Values | Provenance | Frame / identity | Classification |
|---|---|---|---|---|
| M1-LOCAL | 296445.nif per-mesh `local_T`, 30 rows (e.g. GeoTexanim01:0 (−513.24, 36.74, −1053.36); glowsak (401.14, −1611.45, −368.00); Object06 (−10591.81, −839.70, 1536.75); DoorComputer (14.19, 0, −229.71); Object07 (−2039.12, ~0, −65.0); 7×lens (0,0,−534.63); dPVS_occ02/03 z=4420/7720) | serialized in the 296445.nif payload (SHA 656795d8…); read by own parser with Gb12-verified layouts; errata recompute | parent-relative; identity = mesh name inside the model | **MODEL-INTERNAL NIF node transform** (rest pose). NOT world-instance placement |
| M2-WORLD-COMPOSED | 296445.nif `world_T` column; 218757.nif composed transforms (28 blocks; e.g. (0, −1030, 820)); composed scene bbox ~5000×5000×15620 model units; 218757 extents [2500, 3350, 1250] | **computed by our own tools** (analyze_tree_v2.py; s17) from serialized locals under stated conventions; 218757 cross-checked 5/5 vs independent s2 parser | file scene space (root-relative); model units, **not** game meters | **MODEL-INTERNAL, tool-composed FILE_SCENE_SPACE**. Both source runs explicitly deny placement semantics ("Macierz world NIF ≠ placement świata"; "NOT a placement, NOT world XYZ"). NOT SDK/native runtime values (native load of these assets is corpus-proven impossible). NOT world-instance placement |
| M3-SUPERSEDED | `world_T_r1_superseded` column (14 changed rows) | R1 bugged convention (parent-only); superseded errata B1–B3 | — | MODEL-INTERNAL tool artifact (superseded). NOT placement |
| M4-BOUNDS | bboxes; importer 7-float tail (−3447.685 … 15620.0, 0.0) | byte-derived extrema of RAW vertex arrays from DIFFERENT local frames ([E-B4]); 7th float semantics UNKNOWN | — | MODEL-INTERNAL geometry metadata; "NO historical location derived from them". NOT placement |
| Z-DEFAULT | Scene Root identity; 16/30 rows with `local_T=[0,0,0]` and `world_T=[0,0,0]`; 218757 zero root transform | serialized identity/default zeros | — | **DEFAULT ZEROS** — not placement evidence |
| I-SYNTHETIC-CONTROL | SDK synthetic controls (e.g. TRANSLATED_PARENT local (1,2,3) vs composed (101,202,303)); SDK sample scenes | invented test values of the SDK qualification package | synthetic scenes | **SDK/CONTROL values** — not PE data; saved evidence only in tool-qualification scope; NOT client-runtime values |
| R-MECHANISM-NO-VALUES | placement-record setters +0x08/+0x14/+0x20/+0x24 (record ≠ NiAVObject); movable channel rec+38/rot+44/+50..58; PE2/2003 network create-object handler FUN_005977b0 (records 0x1C + f32 XYZ @+0x2c/+0x30/+0x34; SetPosition vtable[0x50]) | byte-evidenced static RE: bridge chain in Entropia.exe 9.3.5; PE2 canon byte-evidenced **in PE2_unpacked_out.exe only** (era-scoped) | transport fields; runtime values from message (0xA2..0xC7) / attribute (class-20006 tag 6) / hardcoded drivers — none reads templates.vfs | **MECHANISM KNOWLEDGE WITHOUT VALUES**. PE2 session values do not exist in corpus (FIRST_PEINST 0/6); 9.3.5 mechanism UNVERIFIED ([E-A1]); movable channel is NOT static-building evidence (parent premise) |
| P-PAYLOAD-NONPLACEMENT | template 4508 PARAM D_f32=124.94100189208984; list2 (3×vec3)→slot-position lerp | physical record bytes (bridge own walk C1; errata LE+BE scans) | template definition registry | **NOT PLACEMENT**: PARAM semantics UNKNOWN (candidate scale/radius; explicitly not a coordinate pair); lerp mechanism has UNKNOWN slot class, no instance identity, and **record 4508's own list2 is empty** (list2_count=0) — no vec3 values exist for the studied object |
| E-ZONE-COORDS | EnvironmentZones.vfs zone records (centers ±30k; r=rec32+26.0) | PE_PLACEMENT_ENCODING_CENSUS_R1 canon (supported, not repeated) | zone definitions | COORDINATE-LIKE BUT NOT INSTANCE PLACEMENT: **0 template↔zone links** (verified) |

**Result: no value in the assimilated corpus attaches a concrete world-instance identity
to a transform with world-frame provenance.** The D1 4-part test (instance identity,
model identity, byte/source provenance, transform type + parent/origin/scale) fails for
every class above — strongest candidates fail at identity (M1/M2 are per-mesh intra-file)
or at frame (R has no values; P is not a coordinate; E has no linkage).

## 3. Scoped verdict (Front D1)

**SCOPED_NEGATIVE_WITH_BOUNDS: the saved corpus contains NO historical world-instance
placement values for the studied objects (296445 / 218757 / the four deep-inspected NIFs).**

- Standing negatives assimilated verbatim: `PLACEMENT_XYZ_RECOVERED=NO` (S1);
  `WORLD_XYZ_RECOVERED=NO`, `PE_WORLD_ROOT_IDENTITY=NOT_ESTABLISHED`,
  `HISTORICAL_WORLD_INSTANCE=NOT_ESTABLISHED`, `PE_AXES_AND_UNITS=UNVERIFIED`,
  `MODEL_GEOMETRY_MATCHES=0` (S2); `NOT_FOUND_IN_SEARCHED_SCOPE` for the world-instance
  placement of 296445/family with explicit search bounds (S3).
- What the corpus DOES contain: byte-proven model-internal transforms (M1/M4),
  tool-composed file-scene-space values (M2), defaults (Z), synthetic controls (I),
  mechanism knowledge without values (R), non-placement payload fields (P),
  unlinked zone coordinates (E). Per parent contract §10: "Jeśli dowód pochodzi z
  kontrolnego modelu SDK, współczesnej mapy, ręcznej rekonstrukcji lub domyślnych zer,
  nie nazywaj go historyczną instancją klienta 9.3.5" — none of these is a historical
  client-9.3.5 instance value.
- Epistemic weight (premise applied): the three runs are separate instruments but share
  underlying sources (Models.bnt C950A8C2…; 296445.nif payload 656795d8…; templates.vfs
  record 4508; same client era). Their agreement is **corroboration, not three
  independent confirmations** (P08-CL4). The independent within-corpus lines are the
  errata's G2 offset-exact scan reproductions, the bridge's CONTROL-4 (962/962 bytes,
  113/113 targets recomputed without Ghidra), and the scene inspection's s17-vs-s2 5/5
  transform cross-check.

### Bounds of the negative

1. **Searched and clean** (documented by S3, supported by canon): all pcg_install/Data
   files (u32LE full corpus + u32BE full Data, 0 BE hits for 296445/296446), decompressed
   terrain tiles, decoded 2003 scripts (1,936 .obj.dec — 296445/296446 only in
   4508.obj.dec as VM immediates, i.e. definition linkage, not placement), VFS both eras
   at field level, placement-encoding census (23 encodings × 29 anchors × 5 corpora,
   PASS-NEGATIVE on coordinate pairs; no spawn table in 2,712-position scripts).
2. **Unsearched value-carrier classes remain** (explicit bounds, S3 §6/§8): Strings/*.bnt
   encrypted interiors (blob-448, location class; decoder exists as a lead, not used),
   .prt portal interiors (undecoded), media interiors (pattern-only). None is a known
   placement carrier for 296445.
3. **Values-provenance bound**: per the PE2/2003 canon the placement source is
   SERVER-DELIVERED (network session stream, byte-evidenced in PE2_unpacked_out.exe
   only); session records do not exist in the corpus (FIRST_PEINST 0/6; no client cache;
   servers unreachable). The 9.3.5 mechanism is UNVERIFIED (transfer hypothesis [E-A1]).
4. **Frame bound**: PE_WORLD_ROOT_IDENTITY=NOT_ESTABLISHED and PE_AXES_AND_UNITS=UNVERIFIED —
   even a value candidate could not be interpreted without a world frame/origin/scale.

### Precise remaining edge

The historical placement channel (2003 canon) is a server-session-delivered record
consumed by the client's create-object handler; the VALUES were never persisted in any
searched client-side file, and session records do not exist in the corpus. Therefore,
within the closed corpus, D1 is closed as a scoped negative: recovering historical
values would require (a) an external archived session record (none known), (b) an
independent external source (out of corpus), or (c) runtime capture (forbidden in this
campaign). Separately, the **mechanism** (9.3.5 consumer chain: A-field → resolver →
model → instance creation → transform source) remains the designed P0 experiment
(PE_935_TEMPLATE_CONSUMER_TRACE_R1 design, [E-V2R007]) — it would close Front B/C
mechanism knowledge but cannot produce historical values (see BARRIER_BACKLOG P08-B1/B3).

## 4. Premises preserved (explicit application)

- *Three documents copying one source are not three independent confirmations* → P08-CL4:
  shared source identities documented; corroboration weight rests on within-run
  independent reproductions.
- *SDK-controlled parse values are saved evidence only in their scope* → applied to
  I-SYNTHETIC-CONTROL; additionally the 296445/218757 transform tables are NOT even SDK
  parses — they are own-parser byte data + stated arithmetic conventions (P08-CL3), and
  no native/SDK runtime values for these assets exist anywhere (native load
  corpus-proven impossible).
- *Movable rec+38/rot+44 channel is not static-building evidence* → applied in the
  R-MECHANISM class; not counted as placement evidence for static buildings.
- *Transform values without instance identity + frame/origin/scale are not historical
  placement* → applied to every class; this is the operative reason each class fails
  the D1 test.

## 5. SELF_CHECK (executor's own — NOT independent PE-MASTER audit)

- [x] Contract SHA256 verified before start (12092315…abf4a); CONTRACT.json copied into
      the package with identical hash.
- [x] RUN_STARTED.json materialized FIRST (23:02:25Z) with accepted scope; science
      executed in the same task.
- [x] All 5 sources catalog-pinned; fresh disk SHA256 == catalog pin for all 5
      (5/5 SHA_MATCH); FINAL_REPORT.md read only in relevant sections per contract
      (whole 51KB not re-read).
- [x] Body admission respected: 0 bodies / 0 rows / 0 CALL; admitted_regions=[] held;
      no campaign-control tool invoked, no parent CONTROL writes.
- [x] Forbidden list respected: no EXE/game payload/runtime opened, no VFS/BNT parsing,
      no Ghidra export, no old writer script, no config/skills/frozen-root/repo writes,
      no new catalog expansion (only catalog JSON read for pin verification).
- [x] Every transform-like value class in the assimilated documents is classified
      (9 classes) with provenance and frame; no class promoted to placement.
- [x] Negative is scoped with bounds (searched clean / unsearched classes /
      values-provenance / frame) and a precise remaining edge; no default-success
      fallback; standing statuses unchanged (WORLD_XYZ_RECOVERED=NO,
      HISTORICAL_PLACEMENT=NOT_ESTABLISHED, CURSOR_SOURCE_MEDIUM=UNKNOWN,
      CANONICAL_GATE_EFFECT=NONE).
- [x] Counters real (COUNTERS.json); clock real ([DateTime]::UtcNow); package hard stop
      2026-10-19T00:00:00Z respected.
