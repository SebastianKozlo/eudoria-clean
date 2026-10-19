# HANDOFF — P08 (Front D1, saved-evidence assimilation)

```text
RUN_ID = PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018
PACKAGE_ID = P08
FRONT = D (saved-evidence availability; DOCUMENT ASSIMILATION)
RUN_STATUS = COMPLETED (bounded assimilation package complete; frozen for parent review)
RUN_TYPE = corpus documents only; admitted_regions = []; 0 bodies / 0 rows / 0 CALL
STARTED_UTC = 2026-10-18T23:02:25Z
COMPLETED_UTC = see MANIFEST.json clock (real tool clock)
PACKAGE_HARD_STOP_UTC = 2026-10-19T00:00:00Z (respected)
CONTRACT = CONTROL/CONTRACTS/P08.json SHA256 12092315AF035249DD11DBA2319B7F03A6290007B0281836155BDE02881ABF4A (verified; copy in package)
QUESTION_D1 = does the saved corpus contain HISTORICAL world-instance placement values
  (transform values with concrete instance identity + byte/source provenance) for the
  studied objects?
D1_VERDICT = SCOPED_NEGATIVE_WITH_BOUNDS: NO historical world-instance placement values
  in the assimilated corpus for any studied object (296445 / 218757 / deep-inspected NIFs).
  All transform-like values classify as model-internal NIF node transforms (M1/M2/M3/M4),
  default zeros (Z), synthetic SDK controls (I), mechanism-knowledge-without-values (R),
  non-placement payload fields (P: PARAM=124.941 UNKNOWN semantics; empty list2 for 4508),
  or unlinked zone coordinates (E). None carries concrete world-instance identity + world
  frame/origin/scale.
STANDING_PRESERVED = WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED;
  CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE; no candidate promotion.
PRIMARY_EVIDENCE_PATHS =
  packages/P08_EXEC_R1/CHECKED_SOURCES.json   (5 sources, fresh SHA vs catalog pins, 5/5 MATCH)
  packages/P08_EXEC_R1/CLAIMS.json            (6 claims with evidence/premises/countermodel/evidence_level + 9-class transform table)
  packages/P08_EXEC_R1/REPORT.md              (per-source classification table, scoped verdict, bounds, remaining edge)
  packages/P08_EXEC_R1/BARRIER_BACKLOG.json   (P08-B1..B5)
SOURCES_READ (catalog roles) =
  PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z  (DRAFT_FINAL_REPORT.md, full; PLACEMENT_XYZ_RECOVERED=NO standing; list2 vec3 -> slot-position lerp of unknown class; 4508 payload list2_count=0)
  PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009 (HANDOFF.md full + FINAL_REPORT.md relevant sections; WORLD_XYZ_RECOVERED=NO; PE_WORLD_ROOT_IDENTITY=NOT_ESTABLISHED; MODEL_GEOMETRY_MATCHES=0; composed FILE_SCENE_SPACE only)
  PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912        (TRANSFORM_TABLE_CORRECTED.csv full + 00_RAPORT_CORRECTED.md full; model-internal transforms; own-parser recompute provenance; NOT_FOUND_IN_SEARCHED_SCOPE with bounds)
PREMISES_PRESERVED = all four contract premises applied and mapped in CLAIMS.json
  (three-documents-one-source -> P08-CL4; SDK-scope -> P08-CL2/CL3; movable channel -> R class;
  identity+frame test -> all classes)
COUNTERS = 0 bodies / 0 instruction_rows / 0 CALL / 0 admit / 0 variants;
  5 documents read (4 full, 1 relevant-sections); 5 catalog pins SHA_MATCH; 0 EXE bytes;
  0 payload files; 0 VFS/BNT parses; 0 Ghidra exports; 0 old scripts; 0 git ops; 0 config changes
REMAINING_EDGE (precise) = historical placement VALUES are server-session-delivered per
  PE2/2003 canon (byte-evidenced in PE2_unpacked_out.exe only) and session records do not
  exist in the corpus (FIRST_PEINST 0/6, no cache, servers unreachable) -> not recoverable
  within the closed corpus; unsearched value-carrier classes remain (Strings/*.bnt
  encrypted interiors, .prt interiors) as data barriers, not known carriers; the 9.3.5
  consumer MECHANISM (P0 design PE_935_TEMPLATE_CONSUMER_TRACE_R1) would close Fronts B/C
  mechanism knowledge but cannot produce historical values.
NEXT_STEP_FOR_PARENT = parent QC + assimilate D1 verdict into campaign synthesis; D1 is
  closed negative for the corpus; Front B/C mechanism work per BARRIER_BACKLOG P08-B3/B4/B5.
HARD_STOP = YES (package scope exhausted; frozen for parent; no further expansion)
QC_ORIGIN = SELF_CHECK only (this package); independent QC belongs to the parent's reviewer.
```
