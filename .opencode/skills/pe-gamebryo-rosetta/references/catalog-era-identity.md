# Catalog / era identity / texture provenance — PE_CITY_ASSET_MAP_R1 measured chapter

Status: MEASURED in PE_CITY_ASSET_MAP_R1_20261010 (phases 2-4; all values below
were re-measured by that run's tools — sources and scope named per claim; no
"engine known 100%" claims anywhere). Gamebryo SDK sources serve FORMAT/MECHANISM
comparison only; they never establish a PE role. No historical placement, no
world coordinates (HISTORICAL_PLACEMENT = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO).

## 1. Era identity (scope: the two owned corpora, nothing else)

- `CD_2003` = the 2003 CD-installer corpus: Models.ark (128,742,137 B, SHA256
  f660d055...) and Textures.ark (289,585,581 B, d611d125...). `PCG_9_3_5` = the
  PCG 9.3.5 installation: Models.bnt (395,412,868 B, c950a8c2..., REQUIRED pin)
  and Textures.bnt (973,942,771 B, 61acd13b...). Other installations (e.g. any
  EU2008-era copy with 8,095 texture entries) are DIFFERENT-ERA files — never
  mixed (source: INPUT_IDENTITIES.json, re-measured fail-closed at every load).
- Asset identity = `ERA + CONTAINER_SHA256 + ENTRY_NAME + PAYLOAD_SHA256`. A
  numeric ID alone is NEVER globally unique: **2,177 entry names exist in BOTH
  era model containers** (e.g. 266865.nif, 65678.nif — verified present in both
  phase-2 model catalogs) — each is TWO distinct
  assets with different container+payload SHAs (source: the regenerated catalog
  overlap census; era separation asserted by the catalog gates).
- Whole-corpus facts (source: full entry catalogs regenerated from the pinned
  originals; per-entry CRC32 + payload SHA256 recomputed 100%):
  - CD_2003 Models.ark: 2,492 entries, all STORED, all NIF (4.1.0.12 × 1,815,
    4.0.0.2 × 440, 4.0.0.0 × 237 — header sniff only, never a decode).
  - PCG_9_3_5 Models.bnt: 5,596 entries, RAW 1:1 payloads (the "zlib-compressed
    entries" skill note describes a DIFFERENT-ERA file and does NOT apply);
    4,838 Gamebryo 10.1.0.0 + 757 NetImmerse 4.1.0.12 + 1 4.0.0.2.
  - BNT2 directory pad semantics: trailing u32 == crc32 for only 3,435/5,596
    Models.bnt entries — the "CRC stored twice" claim is MEASURED_PARTIAL, not
    universal (source: phase-2 catalog, recorded raw).
- Bounded index reads are the ONLY safe way to touch the big containers:
  BNT2 tail(8)+directory, .ark EOCD window + central directory (standard-ZIP
  layout — dual-index-verified on both real .ark containers; the alternative
  skill-documented CD layout FAILED 100% on these files). Byte budgets
  measured: 0.02-0.16% of the file sizes (source: catalog_archive_safety gates).

## 2. Catalog coverage (scope: exactly what was decoded, honestly labeled)

- DECODE status taxonomy (per row, never merged): `DECODED_FULL_CLOSURE` (the
  four CD_2003 primaries, live-decoded by the bounded NIF-4.1 reader: all
  blocks + TopObjects footer + EOF exact), `DECODED` (1,551 PCG935 NIF-10.1
  batch rows with FILE_SCENE_SPACE bounds), `DECODED_NO_MESH` (17 — REAL
  measured 0 triangles, extent UNKNOWN never 0), `FAILED` (3,270 — loud
  unregistered-block-type errors preserved verbatim; top: NiTextKeyExtraData,
  NiKeyframeController), `VERSION_GATED` (758 PCG935 4.x rows — never
  attempted), `CATALOG_ONLY` (2,488 CD_2003 non-primaries — no decoder
  authorized in that run; the bounded NIF-4.1 reader covers ONLY the four
  pinned primaries).
- UNKNOWN discipline: every unmeasured field is `UNKNOWN` (badge) — never 0,
  never invented; sort rule everywhere: measured largest→smallest, UNKNOWN
  always LAST. All tables are LARGEST-MEASURED with a numeric coverage line
  (e.g. extent measured 1,555 of 8,088) — "largest of all" claims are FORBIDDEN
  (big file ≠ biggest extent ≠ most complex; separate metrics, never merged).
- Measured axes/units: FILE_SCENE_SPACE — the file's own x/y/z labels, NO axis
  swap, NO unit conversion, axis semantics (e.g. up-axis) NOT established by the
  reader; ORIGINAL file units everywhere — never called meters;
  SOURCE_FILE_SCENE_SPACE ≠ WORLD_PLACEMENT.

## 3. Proxy vs render role (scope: the four primaries' measured structure)

- The four CD_2003 primaries (192374, 193207, 193313, 193684; NIF 4.1.0.12)
  share a uniform structure: `Scene Root` + named NiNodes each with exactly one
  NiTriShape `<name>:0`; every shape has one VERIFIED NiMaterialProperty ref;
  every model carries the same root extra-data chain
  NiArkAnimationExtraData (OPAQUE) → NiArkTextureExtraData (numTex=0) →
  NiArkImporterExtraData ("4.1.0.12") + NiVertexColorProperty +
  NiZBufferProperty (source: phase-3 reader full closure + Python dual-decode
  agreement; block dumps in PRIVATE_OUTPUT).
- The "no Ark classes expected" hypothesis is REFUTED by measurement: all four
  contain MindArk NiArk* classes; the stock NiTexturingProperty/NiSourceTexture
  chain is entirely ABSENT.
- Placement is in VERTICES (measured on all four: every local TRS identity;
  vertex arrays already span the scene; spread growth 1.0) — the layout is
  stored in vertex coordinates, transforms contribute nothing. Connected
  components (596/670/600/419) are NOT building counts.
- Node names (Outpost39_proxymesh, MSC, signs, build, MAC; signs, mlti, wall,
  signs01, mac, build, cont, forts; Box01; Box06, Object01) are byte-level
  REPRODUCED NiNode names — NAMES/HYPOTHESES ONLY: NOT game classes, NOT city
  names; MSC/MAC are not promoted to any class without proof. The Desktop name
  reads were the hypothesis; the byte-level reproduction is the evidence.
- Extents (FILE_SCENE_SPACE, original units; source: the composed bounds
  counterchecked by an INDEPENDENT raw-byte vertex scan + the phase-3 frozen
  values, agreement 0.01 tolerance): 193313 maxAxis 31,765.85; 193684 33,739.21;
  192374 32,789.15; 193207 26,940.91.

## 4. Texture provenance (scope: exactly the measured edges)

- Disposition order (frozen BEFORE measurement): NAME_FOUND →
  REFERENCE_CONFIRMED → CONTAINER_ENTRY_RESOLVED → IMAGE_DECODED →
  MATERIAL_APPLIED → BROWSER_OBSERVED — an edge is listed with the HIGHEST class
  ACHIEVED and every lower class it passed.
- The four primaries: UNTEXTURED_PROXY_MESH — 0 NiTexturingProperty, 0
  NiSourceTexture, ArkTexture numTex=0, 0 UV sets on every mesh (explicit visual
  fallback, NEVER a textured PASS). Their 19 material edges are
  REFERENCE_CONFIRMED (verified block refs) and — after the phase-4 real-browser
  PIXEL_RENDER of the /catalog previews — MATERIAL_APPLIED=YES (the diffuse
  color is applied to that shape's material in the preview) +
  BROWSER_OBSERVED=PIXEL_RENDER (per-model PNG SHA256 recorded in
  TEXTURE_LINK_DISPOSITIONS.csv). Texture classes stay 0 — untextured is the
  measured fact.
- PCG_9_3_5 batch (1,551 decoded models): all carry ArkTexture DESCRIPTIVE
  names; 3,357 name edges ALL `NAME_NOT_FOUND` (the same-era Textures.bnt
  catalog is numeric-named `<id>.dat`); 794 material edges REFERENCE_CONFIRMED;
  NAME_FOUND_EXACT 0 — an honest negative, visible. The per-entry 9-byte Ark
  tail stays RAW_ONLY (the 218757 textureId retraction stands; NO
  interpretation transferred between models or eras).
- Hard negatives enforced: exact-name matching only (no adjacent-ID/color/similar-
  name/other-era attribution); a header sniff is NOT an image decode
  (IMAGE_SNIFFED_DDS / IMAGE_SNIFFED_TGA_HEADER / IMAGE_NOT_DECODED —
  IMAGE_DECODED claimed nowhere in this chain); cross-era resolution is REFUSED
  by construction (wrong-era → controlled NAME_NOT_FOUND + refused marker);
  missing texture = explicit visual fallback.

## 5. Cross-era candidates (pointers only — NO identification)

- The literal IDs 192374/193207/193313/193684 have NO exact-name match in the
  PCG_9_3_5 catalog (absence of the literal ID is NOT proof of absence of a
  counterpart). Size-proximate NIF-4.1 candidates are CANDIDATE_ONLY (e.g.
  193313 ← 333375.nif Δ11 B; bounded probe: 2 decoded with generic names — no
  name kinship; 7 exceeded the bounded reader, honestly PROBE_FAILED).
- No city/place identification anywhere; no silhouette-matching as proof.

## 6. Reuse map (what exists — reuse before writing parallel code)

- `tools/pecompat/catalog_data.mjs` — the era-aware catalog data model
  (regeneration-first from the pinned originals; identity-keyed measured
  caches; the two bounded index readers; pure sort/filter rows helpers).
- `tools/pecompat/texture_chain.mjs` — era-scoped resolution + disposition
  logic (the gates' subject).
- `compat/server-catalog.mjs` — the /catalog bounded loopback server (extends
  the sceneir server design: allowlist statics, jailed three subtree,
  DENIED_EXPLICIT negatives, verified-free port, refuses 8140 by construction).
- `compat/catalog.html|catalog-app.js|catalog-table.js|catalog-preview.js|catalog.css`
  — the /catalog mode: era-separated paged table, UNKNOWN badges, honest state
  rows, the four-primary preview (hierarchy tree, per-shape isolation,
  wireframe, fit/reset, original-coordinates view beside fit-to-view —
  centering EXACTLY ONCE at the presentation wrapper, NO axis swap/NO unit
  conversion, client-side composition + fingerprint cross-check fail-closed).
- Gates: `tests/pecompat/run_catalog_tests.mjs` (33 records: archive safety,
  independent bounds countercheck, texture gates, UNKNOWN handling, preview
  math, T7-style denial, T9-style real-browser LOAD through the FIXED 5-conjunct
  gate imported unchanged from the sceneir T9 suite) + `tools/pecompat/
  catalog_pixel_render.mjs` (calibrated PIXEL_RENDER, PRIVATE_OUTPUT only).
