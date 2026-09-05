#!/usr/bin/env python3
# -*- coding: ascii -*-
# v4_registry.py - the V4 era-bounded registry (19 entries) + the V4 known-open
# list (7 items) + the top-level matrix sections.
# REGISTRY RULE (W3): the era_statement for P-RNG-DIV and P-POS-SCALE (the
# fourth stale carrier) is COMPOSED from the current evidence (the
# CONSTANT_ADDRESS_LOCK byte locks) - never carried; every entry carries a
# v4_status; the other 17 entries carry the V3 status/fields verbatim (their
# content is current).

REGISTRY_V4 = [
 {"placeholder": "P1 (materials_confirmed)", "missing": "the 65x65 climate byte grid (texture id 432502)", "why": "NOT in any local container (178-container census); the client fetch is LOCAL-ONLY (a miss halts init); patcher-delivered (ClientLoader FTP)", "resume_path": "a patcher-updated Textures.bnt of the era, or a runtime capture", "era_statement": "constant byte 0 -> palette A[0]=0x66DC6 (documented choice; the engine default for unmapped bytes is 0x66DC7); NO historical climate-truth claim", "v4_status": "carried (open/era-bounded as in the ITER_048 basis; current per the V3)"},
 {"placeholder": "P2 (materials_confirmed)", "missing": "the 129x129 detail-selector grids (texture id 459344)", "why": "same delivery-channel verdict as P1", "resume_path": "same as P1", "era_statement": "constant byte 0 -> the engine tables C[0]=D[0]=458791, E[0]=458792 (the ACTUAL engine entries for byte 0; mechanics CONFIRMED, input bounded)", "v4_status": "carried (open/era-bounded as in the ITER_048 basis; current per the V3)"},
 {"placeholder": "P3a (materials_confirmed)", "missing": "the ArkHeightTree leaf recursion", "why": "the tree construction not RE'd (iter027 bound 1; leaves carry global-field samples, no tile linkage)", "resume_path": "the quadtree construction RE", "era_statement": "the leaf data chain preserved IN FORM (direct sample + clamp); the recursion is a labeled approximation", "v4_status": "carried (open/era-bounded as in the ITER_048 basis; current per the V3)"},
 {"placeholder": "P3b (materials_confirmed)", "missing": "the cross-era georeferencing (field vs tiles)", "why": "UNPINNED: r=0.527 saturation (iter028); the MEASURED contradiction: field at engine addressing -130..-125 m vs tiles +16..+487 m (iter030)", "resume_path": "the 2010-era local terrain, or runtime tracing", "era_statement": "the ROW INPUT uses the TILES' OWN heights (backed by the measured contradiction - an honest choice, NOT a historical claim)", "v4_status": "carried (open/era-bounded as in the ITER_048 basis; current per the V3)"},
 {"placeholder": "P4 (materials_confirmed)", "missing": "the per-session noise-table seeds", "why": "the engine seeds the manager RNG per-session (FUN_004058a0/00405920 Java-LCG decompiled); [P4] REDUCED TO THE SEED ONLY by iter036 (the draw construction is now exact)", "resume_path": "a runtime RNG capture", "era_statement": "FIXED-seed Java-LCG tables - deterministic reconstruction only", "v4_status": "carried (open/era-bounded as in the ITER_048 basis; current per the V3)"},
 {"placeholder": "P5 (materials_confirmed)", "missing": "the accumulated leaf roughness at the historical scale", "why": "the CONFIRMED 12-slot formula evaluated on the tile grid at the 4-unit sample scale; the historical leaf size/depth rule not pinned", "resume_path": "the quadtree RE (same as P3a)", "era_statement": "formula CONFIRMED, scale DOCUMENTED", "v4_status": "carried (open/era-bounded as in the ITER_048 basis; current per the V3)"},
 {"placeholder": "P-WAVES (water_system)", "missing": "waves01/02.tga (the plane wave textures)", "why": "name-registered (WAVES_01/02/03, type 1000) NOT in any local container", "resume_path": "a patched-era container or runtime capture", "era_statement": "SYNTHETIC normals - never claimed historical", "v4_status": "carried (open/era-bounded as in the ITER_048 basis; current per the V3)"},
 {"placeholder": "P-SKY (water_system)", "missing": "sky0/1.tga (the reflection textures)", "why": "same census negative", "resume_path": "same as P-WAVES", "era_statement": "SYNTHETIC gradient - never claimed historical", "v4_status": "carried (open/era-bounded as in the ITER_048 basis; current per the V3)"},
 {"placeholder": "P-DATUM (water_system)", "missing": "the water level in the TILE datum", "why": "the 10.0f constant is in the GLOBAL-FIELD datum; the field-vs-tile georef UNPINNED (same as P3b)", "resume_path": "the georef pin (P3b's closer)", "era_statement": "the page elevation = a demonstrative control (engine 10.0 field-datum; tile-datum UNPINNED; default 0.0 = the iter023 correlation)", "v4_status": "OPEN (not attempted in the repair run - the georef pin remains future work; current per the V3)"},
 {"placeholder": "P-CLIMATE (foliage_system)", "missing": "the per-location climate selection (which .vcl applies where)", "why": "the shared-selector hypothesis PLAUSIBLE-NOT-CONFIRMED (VCL ids vs palette ids DISJOINT; the .vcl fetch id source + type-id constant UNVERIFIED)", "resume_path": "the .vcl fetch-id RE + the cell-stream provider RE", "era_statement": "DOCUMENTED choice: climate index 0 - the page demonstrates the MECHANISM, not the historical placement", "v4_status": "OPEN (the cell-content origin remains open; the real-domain re-proof covers the sampler arithmetic only; current per the V3)"},
 {"placeholder": "P-CELLSTREAM (foliage_system)", "missing": "the historical cell byte-stream content", "why": "the DataSource/PatchSourceClient abstraction proven but the data origin NOT closed", "resume_path": "the cell-stream provider RE", "era_statement": "the local deterministic stand-in (round(col1) + the placement hash) is RECONSTRUCTION-ONLY", "v4_status": "OPEN (the cell-content origin remains open; the real-domain re-proof covers the sampler arithmetic only; current per the V3)"},
 {"placeholder": "P-RNG-DIV (foliage_system)", "missing": "the exact RNG normalization divisor", "why": "_DAT_00a7d7a8 reads 0.0 statically (runtime-initialized)", "resume_path": "runtime tracing (separate authorization)", "era_statement": "composed in V4 from the CONSTANT_ADDRESS_LOCK byte locks: the RNG normalization uses the BYTE-LOCKED operand 32767.0 f64 (_DAT_00a7d7a8, bytes 00 00 00 00 C0 FF DF 40, FDIV QWORD @0x0098CE5A) - rand01 = f32(r/32767.0) inclusive [0,1]; no candidate wording stands (the old registry era_statement was superseded per RETRACTIONS.md section 8)", "v4_status": "SUPERSEDED-LOCKED: _DAT_00a7d7a8 = 32767.0 f64 byte-locked (iter035; re-locked via the section map)"},
 {"placeholder": "P-RNG-P3 (foliage_system)", "missing": "p3 = *(impl+0x24) of the seed", "why": "UNVERIFIED; p2 = view band 10 STRONGLY_SUPPORTED not byte-pinned", "resume_path": "the impl-object RE", "era_statement": "p3 = 0 in the reconstruction - labeled", "v4_status": "carried (open/era-bounded as in the ITER_048 basis; current per the V3)"},
 {"placeholder": "P-POS-SCALE (foliage_system)", "missing": "the u16->world position divisor", "why": "_DAT_00a8c758 reads 0.0 statically (runtime-initialized)", "resume_path": "runtime tracing", "era_statement": "composed in V4 from the CONSTANT_ADDRESS_LOCK byte locks: the u16->node position normalization uses the BYTE-LOCKED operand 65535.0 f64 (_DAT_00a8c758, bytes 00 00 00 00 E0 FF EF 40, FLD QWORD @0x0095B2BC) - nodeX/Y = f32(u16/65535.0) node-local fractions [0,1]; no candidate wording stands (the old registry era_statement was superseded per RETRACTIONS.md section 8)", "v4_status": "SUPERSEDED-LOCKED: _DAT_00a8c758 = 65535.0 f64 byte-locked (iter035; re-locked via the section map)"},
 {"placeholder": "P-SCALE-FIELDS (foliage_system)", "missing": "the col2/col3 -> scale min/max field mapping", "why": "the census reading + the impl+0x40/+0x44 direction STRONGLY_SUPPORTED (not byte-pinned)", "resume_path": "the impl-object RE", "era_statement": "a documented reading of the records - labeled", "v4_status": "carried (open/era-bounded as in the ITER_048 basis; current per the V3)"},
 {"placeholder": "P-WINDOW (foliage_system)", "missing": "the historical generation window (grid extents)", "why": "the extents are settings-scaled, not statically pinneable", "resume_path": "the settings-source RE", "era_statement": "the window = the proven region - a demonstration window", "v4_status": "carried (open/era-bounded as in the ITER_048 basis; current per the V3)"},
 {"placeholder": "P-UNITS (foliage_system + water)", "missing": "the NIF cm->render-m bridge", "why": "the NIF corpus is cm-native; the m->cm x100 engine scale CONFIRMED but the GLB cache bridge is a reconstruction convention", "resume_path": "the clean pesource NIF path", "era_statement": "the 0.01 bridge - CURRENT_RUNTIME_CALIBRATION", "v4_status": "carried (open/era-bounded as in the ITER_048 basis; current per the V3)"},
 {"placeholder": "P-MATERIALS (foliage_system)", "missing": "the per-model materials", "why": "the materials come from the GENERATED_CACHE GLBs (export source corpus UNVERIFIED at file level); the 0x3EC technique informs the lighting only", "resume_path": "the clean pesource NIF parser (a JS NIF reader over era Models.bnt)", "era_statement": "GENERATED_CACHE assets + fixed deterministic lights - an era-bounded approximation, NEVER claimed byte-faithful (the single iter037 witness chain is the exception, proven original-direct)", "v4_status": "carried (open/era-bounded as in the ITER_048 basis; current per the V3)"},
 {"placeholder": "ROTATION (foliage - RE-faithful absence, not a placeholder)", "missing": "the rotation/variant derivation", "why": "NOT FOUND in the spawn loop (candidates FUN_0095ae20/FUN_0095b4f0 unread)", "resume_path": "the candidate-function RE", "era_statement": "identity rotation = the RE-faithful absence, recorded as such", "v4_status": "carried (open/era-bounded as in the ITER_048 basis; current per the V3)"}
]

KNOWN_OPEN_V4 = [
 {"item": "the scrambled-texture FALSIFICATION (ledger ENTRY #3 - the witness must be used to falsify the U1 SEVERE cases)", "status": "OPEN - explicitly NOT solved in the V4 package"},
 {"item": "the WITNESS MATRIX (known-good + mildly wrong + severely scrambled + v4 + v10 + character/clothing - ledger ENTRY #4 R4)", "status": "OPEN - not started"},
 {"item": "the georef pin / [P-DATUM] (field-vs-tile datum)", "status": "OPEN"},
 {"item": "the patcher-delivered world-data grids (65x65 climate / 129x129 details; [P1]/[P2])", "status": "OPEN - era-bounded placeholders stand"},
 {"item": "the cell-content origin (the historical cell byte stream; [P-CELLSTREAM])", "status": "OPEN - the placement stand-in stays RECONSTRUCTION-ONLY"},
 {"item": "the ORIGINAL-CLIENT visual parity (the regression sweep is vs OUR OWN recorded runtime; a server/original-client comparison is post-M1, human-gated)", "status": "OPEN - milestone-scope limit, stated"},
 {"item": "the actual x87 control word at chain-execution time (the PC/RC conditional model's SENSITIVITY is now measured on both domains - real 14,104/229,376 and synthetic 103,073/1,245,184, the latter double-confirmed by THIS run's re-measurement - but the ACTUAL client CW remains UNMEASURED; a runtime capture is the falsifier)", "status": "OPEN - the V4-composed update of the V3 item (composed from the pc24_synthetic_measurement.json disposition)"}
]

HEADER_MD = """# M1 GATE DELIVERABLE MATRIX V4 (the corrected, semantically clean consolidation)

- CREATED BY: PE_M1_GATE_V4_CORRECTION_R2_20260905_101327 (2026-09-05) - the corrected re-launch
  of the R1 correction mandate (R1 hard-stopped correctly on a pin transcription error; its
  evidence is preserved and untouched). EXECUTED per the PE-MASTER-refined 12-point mandate.
- CONSOLIDATES: the V3 basis (iter035/036/037 + the validator-coverage repair run) + THIS run's
  corrections: all 19 rows carry 9 FIELDS in BOTH formats; the MD renders the five charter
  section-13 labels per row (the V3 MD's verdict-only rendering was defect F1 - not repeated);
  the six old-matrix field gaps composed + labeled; the no-copy set (rows 6/8/10/11/19 + the
  registry era_statements for P-RNG-DIV/P-POS-SCALE) recomposed from CURRENT evidence; the
  corrected oracle counter split; the PC24 synthetic re-measurement (run-side double
  measurement: 103,073/1,245,184 CONFIRMED).
- SUPERSESSION: the V3 files (GATES\\M1_GATE_DELIVERABLE_MATRIX_V3.md/.json) are FROZEN HISTORY,
  superseded BY THIS V4 (new physical files; nothing edited); the old matrix copies stay FROZEN
  (SUPERSEDED-BY-V3 then -BY-V4, the full chain in GATES\\AMENDMENTS.md); the old
  EVIDENCE_MANIFEST.json is superseded by EVIDENCE_MANIFEST_V4.json (the append-only index mark;
  the file untouched).
- SCOPE: PASS of this V4-correction package = the matrix is semantically clean + internally
  consistent + the semantic gate passes with its negative controls. It does NOT close M1, does
  NOT unlock M2, does NOT change charter section 13. M1 remains PARTIAL; M2 remains HARD-STOPPED.
- TAXONOMY: CONFIRMED / STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED / REJECTED.

## THE 19 ROWS (charter section 13) - 9 fields per row, both formats; the five section-13 labels rendered
"""

SCOPE_STATEMENT = "PASS of the V4-CORRECTION package = the semantically clean, internally consistent matrix (19 rows x 9 fields in BOTH formats; the no-copy set honored; W4/W5/W6 content rules verified) + the semantic gate passing on the clean V4 and failing on all four negative fixtures + the corrected counter split + the PC24 synthetic re-measurement with the disposition applied + the V3 frozen marks appended. It does NOT close M1, does NOT unlock M2, does NOT change charter section 13. M1 closure remains the human's decision (the external auditor's charter ruling stands)."

HONEST_LIMITS = [
 "Self-regression + agreement of saved samples is NOT historical client fidelity.",
 "The engine-parity arithmetic claims are CONDITIONAL on the x87 model: RC=nearest-even (the documented Win32 default; NOT a measurement of the original client) and PC in {53,64} - PC=24 measured DIFFERENT on 14,104/229,376 REAL lerp values and 103,073/1,245,184 SYNTHETIC lerp values (the latter double-confirmed by this run's re-measurement), so the condition is load-bearing; the actual control word is UNMEASURED (a runtime capture remains the falsifier - explicitly not performed, no runtime experiments).",
 "The noise-table seed is the FIXED reconstruction seed 0x30303030 ([P4] reduced to the seed only); per-session engine seeding is runtime state, unknowable statically.",
 "The witness result covers ONE model + ONE texture (the 10-candidate census), NOT the era.",
 "The regression sweep compares OUR OWN recorded runtime, NOT the original client."
]
