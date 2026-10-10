# LIMITATIONS.md — PE_CITY_ASSET_MAP_R1_20261010

Honest scope boundaries of this run. None of these is hidden elsewhere; each is also visible in
the artifacts it concerns. (Sources: phase reports, REVIEW.md §5 NOT_CHECKED, QC observations,
AMEND_LOG.md.)

## 1. Decoder and format scope

- The NIF-4.1 deep reader (`tools/pecompat/nif41_deep.mjs`) is bounded to the four CD_2003
  primaries' needs (contract §3); unknown block types loud-fail. It is NOT a general NIF parser
  claim — the PCG935 candidate probe demonstrated the loud-fail honestly (7/9 PROBE_FAILED).
- PCG_9_3_5 decode coverage is bounded: 3,270 Models.bnt entries FAILED (loud, verbatim errors
  preserved; the parser surface was deliberately NOT expanded after the first systematic
  failures), 758 VERSION_GATED (NIF 4.x never attempted), 17 DECODED_NO_MESH (genuinely zero
  geometry — REAL zeros, never UNKNOWN-as-0), 1,551 DECODED with mesh bounds.
- CD_2003 non-primaries: 2,488 of 2,492 remain CATALOG_ONLY (header-sniffed, never decoded) —
  extent/complexity UNKNOWN for them (never 0).
- NiArkAnimationExtraData (33 B tail) and NiArkImporterExtraData (13 B + 7 f32 tail) remain
  OPAQUE / PARTIALLY_UNDERSTOOD (raw bytes recorded in the private dumps).
- The per-entry 9-byte ArkTexture tail is RAW_ONLY everywhere (the 218757 textureId retraction
  stands; no interpretation transferred between models or eras). For the four primaries the
  non-transfer rule holds vacuously (numTex=0 — no tails exist).
- VFS files (textures/materials/templates .vfs): bounded header/string inspection ONLY —
  **record layouts NOT established** (honest; resolving the PCG935 texture-name gap may need
  them).
- 41 CD_2003 Textures.ark entries (4–96 B, *.tga names) and 19 PCG_9_3_5 Textures.bnt OTHER
  entries are tiny data stubs with no image header: content UNKNOWN (CRC-verified only).

## 2. Measurements and their boundaries

- Models.bnt has 150,133 B of tail slack between the last payload end and the directory start.
  The boundary census is exact (0 overlaps / 0 gaps BETWEEN payloads; monotonic), but the slack
  semantics are UNKNOWN (OBS-1) — recorded, not interpreted.
- BNT2 directory trailing pad u32 == crc32 for only 3,435/5,596 Models.bnt entries
  (MEASURED_PARTIAL; the universal "CRC stored twice" reading is refuted).
- Extents/complexity are FILE_SCENE_SPACE (the file's own x/y/z labels, NO axis swap, NO unit
  conversion); axis semantics (up-axis) NOT established; units are ORIGINAL file units, never
  called meters; SOURCE_FILE_SCENE_SPACE ≠ WORLD_PLACEMENT. Extent/complexity rankings are
  LARGEST-MEASURED with numeric coverage lines; "largest of all" is never claimed.
- Connected components (596/670/600/419) are triangle-index-graph components, NOT building
  counts. Node names are byte-level reproduced hypotheses — NOT game classes, NOT city names.
- Native vendor cross-check unavailable for the four primaries: the stock Gamebryo 1.2
  SceneGraphPrinter refuses them (4× NATIVE_LOAD_REJECTED "Error loading stream."). The executed
  independent cross-checks are the Python dual-decode + the independent raw-byte bounds
  counterchecks (suite + QC's own zero-import reader).
- GLB comparison: NO GLB exists for the four primaries (NO_GLB_PRESENT_FOR_THESE_IDS) — numeric
  comparison skipped honestly; the executor's depth-6 search was not re-executed by QC (bounded
  v4-tree re-search: 16 other CD2003 GLBs, 0 primary GLBs).
- Cross-era candidate pointers are CANDIDATE_ONLY (2 probe-decoded with generic names — no
  kinship; 7 PROBE_FAILED). No city/place identification anywhere in this run
  (HISTORICAL_PLACEMENT = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO).

## 3. Browser / automation

- INTERACTIVE = NOT_PERFORMED (automation daemon down: ECONNREFUSED on 127.0.0.1:9222 and
  [::1]:9222, incl. one session automation navigation attempt; honestly never faked).
  Consequently **BROWSER_VERIFIED is not claimed** (the §5 promotion rule requires LOAD +
  PIXEL_RENDER + INTERACTIVE). LOAD and PIXEL_RENDER are executed and verified.
- PIXEL_RENDER non-triviality is an honest bounded heuristic (file size + full PNG decode +
  color/luma census + region thresholds), labeled as such.
- Six raw console .txt captures (raw/T9/*CONSOLE.txt) are UTF-16LE+BOM (PowerShell redirect
  class); the authoritative machine records are the UTF-8 JSONs (OBS-2; no repair needed).
- Denial probes issued through WHATWG fetch get client-side dot-segment normalization (OBS-3);
  the server's OWN refusals were confirmed with raw-socket probes (PATH_TRAVERSAL_BLOCKED /
  STATIC_FILE_NOT_ALLOWEDLISTED). All 18 QC probes refused; 0 leaks.

## 4. QC and persistence-phase repairs (findings fixed here — record kept)

- P2-1: TEXTURE_LINK_DISPOSITIONS.csv had 1,545 unquoted `container_entry` values (8-field
  mis-splits against the 7-field schema) — FIXED at persistence (RFC4180 quoting; sums
  unchanged; strict parse revalidated 1,587 × 7). PRE/POST hashes in AMEND_LOG.md.
- P3-1: INTERVENTION_LEDGER F12 said 1,588 data rows (actual 1,587; the file is UTF-8, not
  ASCII-only) — FIXED by an append-only correction row C1 (history preserved byte-identically).
- P3-2: the skill chapter used the nonexistent example "656865.nif" (present in NEITHER era
  catalog) — FIXED to the verified "266865.nif" (re-verified against BOTH phase-2 catalogs).
- P3-3: the private PHASE3_NativeControl/run_records.json carried a UTF-8 BOM (strict
  JSON.parse failed; the only BOM-bearing JSON of 21 censused) — FIXED at persistence by
  stripping the BOM (content byte-identical after the 3-byte removal; strict parse now
  succeeds). **Limitation note kept here deliberately:** PowerShell-written artifacts on this
  host can carry UTF-8/UTF-16 BOMs — any strict parser consuming private artifacts should
  tolerate or explicitly reject BOMs by policy (QC5 census remains the reference list).
- OBS-4: the rows-API default size sort returns the CROSS-era largest first (225492.nif,
  PCG_9_3_5); era-scoped statements (CD_2003 largest 212124.nif) are a different, also-correct
  scope — recorded to prevent misreading.

## 5. Not checked by the fresh internal QC (REVIEW.md §5 — bounded verification disclosure)

- NOT full-read to EOF (verified behaviorally instead): `tools/pecompat/catalog_data.mjs` (39.7
  KB), 6 of the 7 catalog suites (catalog_bounds_countercheck.test.mjs WAS read fully and
  confirmed genuinely independent), `compat/catalog-*` app files, phase-2 tool bodies (outputs
  independently re-derived by QC's own readers), phase-3 tools other than nif41_deep.mjs,
  phase-4 tools, the full body of t9_pixel_render.mjs and png_nontrivial.mjs.
- NOT re-executed by QC: the cross-era candidate probe (honest PROBE_FAILED records retained),
  the executor's 5-shot PIXEL gate as-is (fresh single-shot capture + non-triviality instead),
  the full depth-6 GLB search (bounded re-search instead).
- The 4,151-row JSONL and 4,838-row batch state: full parse + count + histogram (no per-row
  semantic re-derivation).
- The 3,270 PCG FAILED entries beyond the recorded failure class (loud, not re-attempted —
  correct per contract); the 41/19 tiny TGA/OTHER stubs' content; VFS record layouts; interactive
  browser behaviors.
- Historical SceneIR packages, EU2008-era copies, the canonical eudoria-clean tree beyond the
  recorded status, and all original containers beyond bounded reads: untouched.
- Remaining ARK/BNT entries beyond the 31-entry QC re-hash sample + boundary walks are covered
  by the executor's 100% hash census + QC sampling + dual-index walks — not per-entry re-hashed
  by QC.

## 6. Standing scope flags

HISTORICAL_PLACEMENT = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO;
CANONICAL_GATE_EFFECT = NONE; NEXT_EXPERIMENT_AUTHORIZED = NO; HARD_STOP = YES.

- This fresh internal QC is NOT an independent Desktop post-audit; DESKTOP_POST_AUDIT remains
  PENDING (human decision).
- PE-MASTER's MASTER_ACCEPTED is advisory (ADVANCED authority status: ADVISORY_PRE_QUALIFICATION);
  no canonical promotion, no milestone effect.
- The catalog server is loopback-only; the foreign 8140 reference (218757 viewer) stays the
  only server-sceneir process and was never touched.
