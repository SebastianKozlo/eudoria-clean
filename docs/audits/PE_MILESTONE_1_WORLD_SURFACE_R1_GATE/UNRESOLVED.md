# UNRESOLVED — the consolidated open-items record of the M1 gate package

- PURPOSE (per `GATE_INDEX.md`): the 27 known-open items + the 5 honest limits (V2
  section 2), consolidated — PLUS the V3 open set (7 items, added by the
  validator-coverage repair run; the AUDIT_ENTRYPOINT Open P0 #2 export).
- CREATED BY: PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816 (mechanical consolidation;
  items quoted from the frozen records cited per section; nothing re-derived here).
- READING RULE: check any claim that sounds too strong against this file. NONE of the
  items below blocks the charter's gate DEFINITION (the frozen matrix PART 4 verdict),
  but several are expected work packages for the human to direct (see HANDOFF.md).

## A. THE 27 KNOWN-OPEN ITEMS (frozen matrix PART 4; 02_ANALYSIS\M1_GATE_DELIVERABLE_MATRIX.md — quoted)

1. **TDF sub-header (52..63) min/max source** — UNRESOLVED. 386/400 sampled tiles read
   all-zero, 14 nonzero; NO probed encoding carries the per-tile min/max (iter020 P1).
   Resume: the FUN_0047fb20 min/max RE path.
2. **TDF payload header-xy mismatch** — 0/400 header-xy == filename-xy (consistent; values
   small ints); semantics UNRESOLVED (iter020 P2; the 65x65 climate-cell candidate was
   REJECTED — values vary within single cells).
3. **The shared climate selector** (.vcl fetch id source + type-id constant) — UNVERIFIED
   (iter032 bound 1). The [P-CLIMATE] closer.
4. **The 65x65 climate grid (432502) + 129x129 detail selectors (459344)** — MISSING
   locally (patcher-delivered; the 178-container census + the local-only fetch + the
   init-halt gate — iter029). Acquisition = a patcher-updated era container or a runtime
   capture. [P1]/[P2].
5. **The cross-era georeferencing [P3b]** — UNPINNED (r=0.527 saturation, iter028; the
   measured -130..-125 m vs +16..+487 m contradiction, iter030). Needs the 2010-era local
   terrain or runtime tracing.
6. **Special-row tiles (6,530 PCG, y=0xff1a..0xffff)** — structure-censused (dominant
   2,386 B payload, ds=2100 dim=32; LOD-skirt candidate) but semantics UNRESOLVED.
7. **dim=2 record semantics** — TEMPLATE/PARAMETER role CONFIRMED (75.72% the identical
   (256,227,376,227) template, id=18093; 21 deviant ids); semantics UNRESOLVED.
8. **dim=4 record semantics** — U16-PER-PIXEL structure CONFIRMED (size 84, region 32 B
   = 16 px x 2 B, id=6 constant); semantic role UNVERIFIED.
9. **The height-form full-lerp in 9.3.5** — FUN_00989e70 = the clamp-to-65535 sibling;
   the full lerp form + the min/max source in 9.3.5 itself UNRESOLVED (iter024f).
   PE2003 FUN_0047fb20 identity+operation CONFIRMED.
10. **Cross-file skeleton pairing** — OUT OF M1 SCOPE (charter S11); recorded as an M2
    lead (the single-model witness + witness-matrix rules gate any model work — ENTRY #3/#4).
11. **The type-2/sub-0 zone scratch reader** — written + cleared + dirty-flagged, NO
    reader located in the 838-function census (iter030). Resume: the zone-apply vtable owner.
12. **The zone-apply vtable owner** — the ptr scans hit Jython API failures; the object
    family identified from the mode/grid fields (iter030 honest bound).
13. **The env object's +0x14 water-wind WRITER** — the last wind link
    (EnvironmentZones/ArkScript/server candidates — iter031 NEXT 1).
14. **'Geowater:0' family consumer + the 0xb7dc gate** — a second name-registered water
    family, UNRESOLVED (iter031).
15. **The bank[1]/bank[2]/bank[5] consumers** — the 257 G/B float fields + the 65x65 B
    selector of the world-data bank (candidates: water/min-height) — UNRESOLVED (iter029).
16. **The runtime world-id singleton (id[0])** — per-planet set-swap question UNRESOLVED
    (iter029).
17. **VCL cols 6-11 semantics** — UNVERIFIED (iter032 bound 4; candidacy only).
18. **The cell byte-stream origin** — the DataSource/PatchSourceClient abstraction proven;
    the provider NOT closed (iter032 bound 3). The [P-CELLSTREAM] closer.
19. **The rotation/variant derivation** — candidates FUN_0095ae20/FUN_0095b4f0 unread
    (iter032 bound 5); identity rotation = the RE-faithful absence.
20. **The elevation-band filter rule** — UNVERIFIED; the foliage census MEASURES the bands
    instead of assuming (62 within / 14 outside — iter033).
21. **The clean pesource NIF path** — the GENERATED_CACHE GLB dependency's replacement
    (a JS NIF parser over era Models.bnt) — queued future work (iter033 NEXT 2; partially
    delivered by the iter037 witness reader — the MATRIX of witnesses remains open).
22. **The JUL_2003-era terrain material RUNTIME semantics** — the PE2 2003 client = D3D8
    fixed-function (era-divergent from the 9.3.5 HLSL Terrain_14); the 2003-era blend was
    NOT re-RE'd (iter024f era table; the era drift = CONTENT never GRAMMAR per iter030).
23. **The JUL-era texture version choice** — 110/175 ids era-stable; for the 61 divergent
    ids, which version matches JUL_2003 is UNDECIDABLE from bytes (PLAUSIBLE: CD closest
    in time; UNVERIFIED — iter010/011).
24. **Region-B observations** — Grassmix04 duplicate id (108727 AND 88103, aliasing
    semantics UNRESOLVED); UNNAMED dim=16 records with 512-byte non-RAW/non-RLE regions
    (system records, 6/9 tiles — recorded, carried raw by the decoder) — iter021.
25. **The >4-material reduction mechanism** (top-4 pre-bake vs multipass) — UNRESOLVED
    (iter024/025; C1 top-3 capture measured 93-99%/77-95% vs UB; C2 record-order
    unreliable) — the 3+1 per-pass cap is source-anchored.
26. **The 2xxxx cross-container resource-id space hypothesis** — PLAUSIBLE, no semantics
    claimed (iter022: .tez d 20068-20641 + template B-space runs + ArkScript chat slots +
    20001..20043.vfs share the numeric family; the d<->B crossing = d 20070 == B(template
    1969), 1/7, role UNVERIFIED).
27. **Era divergence census** (recorded, not open per se) — PCG-vs-JUL: heights differ on
    773/51,920 tiles; Water03 +167 tiles; region-B tails diverge in the UNNAMED system
    records (named records era-identical on the sample — iter025); ALL recorded with era
    provenance, never mixed.

(Frozen source: PART 4 of the old matrix — SHA256 F0C7D0F29EEE32F156D4BBF9565724009188BBE8C1C9B0F4CA0BBEC4184D76E1;
   the V3 carries the same open items implicitly via the rows' honest bounds + the registry.)

## B. THE 5 HONEST LIMITS (REPORT_V2_REJUDGMENT.md section 2 — quoted)

1. **The regression sweep (5/5) compares OUR OWN recorded runtime, NOT the original
   client.** An original-client comparison requires a server (the emulator/protocol track
   = post-M1, human-gated). A MILESTONE-SCOPE LIMIT, stated as such — the
   deterministic-reproducibility claim stands; the historical-visual-parity claim is NOT
   made.
2. **The water page datum [P-DATUM]**: the engine level 10.0f is in the GLOBAL-FIELD
   datum; the field-vs-tile georeferencing is UNPINNED ([P3b], the measured contradiction
   preserved as evidence). The page's 0.0 demonstrative control stays labeled.
3. **The foliage cell-content origin**: the placementHash/round(density) stand-in + the
   cell-stream origin + the per-location climate choice = RECONSTRUCTION-ONLY (labeled;
   no historical-truth claims).
4. **The patcher-delivered world-data grids** (65x65 climate / 129x129 details): MISSING
   locally (the 178-container census; the client fetch is local-only + init-halts on
   miss) — [P1]/[P2] era-bounded placeholders; acquisition = a patcher-updated era
   container or a runtime capture (post-M1).
5. **The witness MATRIX is NOT executed** (one model proven original-direct per the
   witness rule; the matrix = the next work package if the human directs it).

## C. THE V3 OPEN SET (the validator-coverage repair run's explicit open list — 7 items)

Quoted from the V3 `known_open_list_v3` (GATES\M1_GATE_DELIVERABLE_MATRIX_V3.json; the
live matrix):

1. **The scrambled-texture FALSIFICATION** (ledger ENTRY #3 — the witness must be used to
   falsify the U1 SEVERE cases) — OPEN — explicitly NOT solved in the repair package.
2. **The WITNESS MATRIX** (known-good + mildly wrong + severely scrambled + v4 + v10 +
   character/clothing — ledger ENTRY #4 R4) — OPEN — not started.
3. **The georef pin / [P-DATUM]** (field-vs-tile datum) — OPEN.
4. **The patcher-delivered world-data grids** (65x65 climate / 129x129 details; [P1]/[P2])
   — OPEN — era-bounded placeholders stand.
5. **The cell-content origin** (the historical cell byte stream; [P-CELLSTREAM]) — OPEN —
   the placement stand-in stays RECONSTRUCTION-ONLY.
6. **The ORIGINAL-CLIENT visual parity** (the regression sweep is vs OUR OWN recorded
   runtime; a server/original-client comparison is post-M1, human-gated) — OPEN —
   milestone-scope limit, stated.
7. **The actual x87 control word at chain-execution time** (the PC/RC conditional model is
   measurement-free; a runtime capture is the falsifier) — OPEN — added by the repair run
   (conditional-model honesty). NOTE the PE-MASTER independent confirmation (advisory):
   PC=24 breaks 14,104/229,376 REAL-domain lerp values (and 103,073/1,245,184 on the
   labeled synthetic domain — auditor-side measurement), so the PC condition is
   LOAD-BEARING, not cosmetic.

## D. The era-bounded registry (19 labeled placeholders — pointer)

The full registry (P1, P2, P3a, P3b, P4, P5, P-WAVES, P-SKY, P-DATUM, P-CLIMATE,
P-CELLSTREAM, P-RNG-DIV*, P-RNG-P3, P-POS-SCALE*, P-SCALE-FIELDS, P-WINDOW, P-UNITS,
P-MATERIALS, ROTATION) with the missing-what / why-evidence / resume-path / era-honest
statement per placeholder lives in the V3 copies (GATES\M1_GATE_DELIVERABLE_MATRIX_V3.*)
and in EVIDENCE_MANIFEST.json (`era_bounded_registry`). *Two of them are
SUPERSEDED-LOCKED (byte-locked constants), retained as registry history.

## E. Binding scope statement

This file EXPORTS the open state; it does not solve anything. M1 closure remains the
human's decision (charter section 13; the external V2 audit verdict DIRECT; the V2
re-judgment PARTIAL_PASS_CORRECTED PROPOSED). No witness matrix, no georef pin, no
patcher-era container hunt, no cell-stream RE, no original-client parity run, no x87 CW
runtime capture is authorized by this package — each is an open item awaiting a
commission.
