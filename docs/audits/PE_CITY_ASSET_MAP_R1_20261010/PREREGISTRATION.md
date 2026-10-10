# PREREGISTRATION.md — PE_CITY_ASSET_MAP_R1_20261010

Registered BEFORE the later phases (catalog, 4-model deep analysis, texture chains, /catalog viewer) execute. These acceptance shapes are frozen now so no gate can be reshaped after seeing results. Phase-1 (T9) acceptance is recorded at the bottom as ALREADY-EXECUTED with its own frozen predicate (the contract §0 text).

## 1. Catalog acceptance shape (contract §2)

- Inventory = a CENSUS, not understanding: every physical file under both `Data` roots gets relative path, size, extension, era, SHA256. For Models/Textures containers (ARK/BNT) the entry catalog additionally gets: entry boundaries, original name, stored size, unpacked size, compression method, extracted-entry SHA where safely readable. Index verification covers boundaries and duplicates; accidental magic matches are NEVER called "a full index".
- Asset identity key everywhere: `ERA + CONTAINER_SHA + ENTRY_NAME + PAYLOAD_SHA`. A numeric ID alone is never treated as globally unique.
- Every record carries field-level coverage and explicit error/unknown; UNSUPPORTED/FAILED entries are KEPT in the catalog. Missing values are `UNKNOWN` (never 0, never invented).
- Coverage reporting is MANDATORY and numeric per era and per container: total entries / catalogued / metadata-measured / decoded-where-attempted / unsupported / failed. No aggregate hides a per-era count.
- Rankings (each descending, each with explicit units and coverage line "measured N of M"):
  1. `PAYLOAD_SIZE` — unpacked model size (bytes).
  2. `SCENE_EXTENT` — AABB from correctly composed ORIGINAL file hierarchy (extent per axis + footprint, in the file's own units — original units are NOT silently meters; no volume as the sole measure for flat models). `UNKNOWN` for undecoded models.
  3. `COMPLEXITY` — triangles / vertices / shapes+nodes as EXPLICIT separate unit columns.
- Big-file ≠ biggest-city ≠ largest-extent: never conflate; never claim "largest overall" from a measured subset. Undecoded models stay `UNKNOWN` in rankings (visible, sortable as UNKNOWN, never 0).
- Decoding policy: prefer header/index reads with identity-key caching; batch-decode only available supported formats; the FIRST systematic parser error stops expansion for that input (recorded) — no boundless parser repair. No new format support beyond the four PRIMARY models' needs.
- Acceptance (per era): census complete (100% of physical files measured); container entry counts independently reconciled against index structure; coverage line present on every ranking; no unknown silently zeroed. Missing texture/container = LOCAL status for that asset+era, never a global BLOCKED; a REQUIRED input identity mismatch blocks work on THAT input only.

## 2. Four-model deep-analysis gates (contract §3; PRIMARY_IDS = 192374, 193207, 193313, 193684, ERA=CD2003; first deep case 193313)

Per-model status classes (exactly one terminal class per model, with reasons):
- `DECODED_PARTIAL` — original hierarchy recovered with explicit PARTIAL flags for every fallback (identity-transform fallback REQUIRES an explicit PARTIAL marker; no silent identity);
- `CATALOG_ONLY` — entry-level metadata only (no honest hierarchy recovery within scope);
- `UNSUPPORTED` — format/feature outside the supported surface (named);
- `FAILED` — attempted and failed (error preserved verbatim).
Gate items per model: roots; typed links; parent/child; names; local TRS; composed FILE-scene transforms (no double-composition — applied exactly once); shape→data verified by actual references (never order-only pairing); geometry where available; properties; opaque blocks preserved opaque. The Desktop name reads (193313: Outpost39_proxymesh, MSC, signs, build, MAC; 193684: signs, mlti, wall, signs01, mac, build, cont, forts; 192374: Box01, MSC, MAC, signs; 193207: Box06, Object01) must be REPRODUCED from the originals — and remain NAMES/HYPOTHESES: no collision/dPVS/LOD role and no city name is claimed without proof. MSC/MAC are never promoted to game classes/terms.
- GLB comparison (old viewer, secondary material): lineage established from actual conversion provenance, not assumed; geometry compared ONLY after an explicitly established axis/transform conversion (counts alone are insufficient); flat-GLB gray materials / zero images prove NOTHING about original textures.
- Bounds: original origin/bounds preserved; any centering/fitting only in a presentation wrapper; connected components are NEVER reported as building counts; layout attribution (transforms vs vertices vs both) must be MEASURED, not assumed.
- ID/name search in both eras' existing indices: absence of a literal ID is NOT proof of absence of a counterpart; candidate listing only, no automatic Port Atlantis/Hadesheim identification. WORLD placement is OUT OF SCOPE (HISTORICAL_PLACEMENT = NOT_ESTABLISHED for this run).
- Acceptance: each of the 4 models has an honest terminal class + reasons; at least the 193313 deep case reproduces the Desktop name reads from the original container; original-coordinates evidence (private projections) exists for every DECODED_PARTIAL model; no role/city claim without proof.
- Independent countercheck: original-hierarchy→computed-bounds must be cross-verified by an implementation INDEPENDENT of the primary parser (not the same parser run twice).

## 3. Texture-chain disposition classes (contract §4)

Edge classes in strictly increasing provenance order — an edge is listed with the HIGHEST proven class ACHIEVED, and every lower class it actually passed:
- `NAME_FOUND` — a texture reference/name exists in model data;
- `REFERENCE_CONFIRMED` — the reference is a real, resolved property/binding reference (slot, UV set, alpha/wrap recorded where proven);
- `CONTAINER_ENTRY_RESOLVED` — the name resolves to an entry in the SAME-ERA container (entry identity: ERA + CONTAINER_SHA + ENTRY_NAME + PAYLOAD_SHA);
- `IMAGE_DECODED` — the entry payload decodes to an image (dimensions/format recorded);
- `MATERIAL_APPLIED` — the image is applied in the reconstruction's material for that shape;
- `BROWSER_OBSERVED` — the applied texture is observed in a REAL browser render (only after actual render — never assumed).
Hard negatives: NO texture attribution by adjacent ID, color, similar name, or the other era's version; NO 9-byte Ark-tail interpretation transferred between models; NO detail-texture stitching to a proxy without a confirmed model/part join; a missing texture is an EXPLICIT visual fallback, never a fake textured PASS; unresolved dependencies stay visible in the catalog. If the original proxy genuinely lacks bindings/UV within the investigated format, that absence is RECORDED as a format-scoped fact.
Acceptance: every edge of the 4 primary models + all correctly-read models is cataloged with its class; wrong-ID / wrong-era / missing-image controlled negatives produce CONTROLLED results (not crashes, not silent passes).

## 4. Regression gates (contract §7; must hold at every later phase)

- 218757 asset/scene viewer: NO regression — 14 mesh/data associations with fingerprints preserved; two-instance independence (change A leaves B bit-identical; geometry shared; wrappers/conversions independent); no double-centering and no double conversion (RENDER_ADAPTER_CHOICE applied exactly once); unit harness `run_tests.mjs` stays 24/24; T7/T8 app gates stay green; the fixed T9 gate semantics (below) are preserved.
- Archive reading: bounded reads only (no whole-container loads into memory without size bounds); CRC/hash verified; duplicate IDs BETWEEN ERAS are reported (never merged); corrupt/truncated input = controlled negative result, not a crash.
- Rankings/UI: UNKNOWN sorts/filters visibly (never as 0); explicit units everywhere.
- Server: loopback only; free-port probe; NEVER binds 8140 or kills foreign processes; only configured assets/indexed reads; no whole-corpus static route, no arbitrary-path routes.
- No product-source change may relabel historical captures or historical packages (READ_ONLY).

## 5. Honest browser labels (contract §0/§5/§7)

- `LOAD` — real headless-browser DOM capture through the FIXED 5-conjunct gate (exitCode===0 AND nonempty DOM AND canvas AND diagnostics AND data-load-status READY). Each missing conjunct FAILs with its own name. Aggregate 13-PASS-style claims are BANNED: the aggregate never substitutes for the conjunct-level truth.
- `PIXEL_RENDER` — a real rendered pixel image of the app, captured by headless Edge `--screenshot`, stored in PRIVATE_OUTPUT ONLY (never the repo, never base64/JSON-encoded), non-triviality verified by the OWN bounded PNG check (file size + full decode + unique-color census + luminance statistics + canvas-region thresholds — an honest heuristic, labeled as such). A DOM-READY page with a dead WebGL canvas still FAILS the canvas-region thresholds.
- `INTERACTIVE` — automation-driven user input (orbit/instance select/sort/fit/wireframe/part toggle in /catalog). If no automation tool is available (current state: automation daemon down — ECONNREFUSED on both 127.0.0.1:9222 and [::1]:9222, re-confirmed by this executor), INTERACTIVE = `NOT_PERFORMED_<reason>` — NEVER reported as PASS and never faked.
- Promotion rule: `BROWSER_VERIFIED` for the whole catalog requires ALL THREE gates actually executed and passed; otherwise the catalog ships with the honest per-gate labels. Texture `BROWSER_OBSERVED` only after a real render.
- A stand-in executable (env-override binary class) is NOT a browser test: its records carry `STAND_IN_PROCESS` labels and can never serve as a positive control; the positive control is always an ACTUAL browser binary.

## 6. Phase-1 (T9) acceptance — predicate frozen from the contract BEFORE execution; ALREADY EXECUTED

- PRE: the defective gate reproduced the false-PASS against the controlled negative `PECOMPAT_BROWSER_BIN=node.exe` (exit 9, 0-byte DOM, no markers, NOT_PRESENT → old status PASS; aggregate 13 PASS / exit 0). Raw: `raw/T9/PRE*`.
- POST: fixed gate, real Edge — asset mode AND #scene mode each PASS with ALL FIVE conjuncts (exit 0, ~21 KB / ~9.3 KB captured DOM, READY). Raw: `raw/T9/POST*`.
- Per-conjunct negatives (synthetic inputs through the SAME production gate): bad exit code → FAIL `EXIT_CODE_ZERO`; empty DOM → FAIL `DOM_NONEMPTY(+CANVAS_PRESENT+DIAGNOSTICS_PRESENT+STATUS_READY cascade)`; missing canvas → FAIL `CANVAS_PRESENT`; missing diagnostics → FAIL `DIAGNOSTICS_PRESENT`; status ERROR → FAIL `STATUS_READY`; status LOADING → FAIL `STATUS_READY`. All six behave exactly as specified.
- Stand-in negative through the REAL test path: both modes FAIL with all five named missing conjuncts + `STAND_IN_PROCESS` labeling; harness exit **1** (nonzero-on-FAIL aggregator verified).
- Side-error separation verified: raw persistence + server lifecycle are separate records; a server-startup failure path produces NOT_PERFORMED loads + its own FAIL record (never a fake conjunct result).
- Product source untouched by the fix (git diff = the two test files + new tools only). Unit regression 24/24. Historical captures NOT relabeled.
