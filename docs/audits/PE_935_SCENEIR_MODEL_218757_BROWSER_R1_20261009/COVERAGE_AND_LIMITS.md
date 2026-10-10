# COVERAGE_AND_LIMITS — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009

Honest coverage statement for the delivered slice. Coverage claims use explicit
denominators (no "fully"/"complete" without the counted set and the read/test
mode). Companion artifacts: FINAL_REPORT.md (all measured fields),
TEST_RESULTS.json (consolidated gates), EVIDENCE_INDEX.md (per-file census).

## 1. What this slice DOES cover (with denominators)

1. **218757 single-asset bounded viewer (1 model of the 5,596-entry Models.bnt
   corpus)** — asset mode: orbit camera, fit bounds, solid/wireframe, axes,
   hierarchy inspector (66 rows: type:name, decode status, serialized local TRS
   vs computed FILE_SCENE world TRS); diagnostics with the original asset
   identity (era PCG_9_3_5, container, entry, payload SHA256, pin-verified),
   block coverage 66 = 62 SUPPORTED + 2 PARTIALLY_UNDERSTOOD + 2 OPAQUE, and the
   imported/visible mesh ledger (14/14 by default; 14/9 with the labeled dPVS
   heuristic toggle, 5 explicit exclusions).
2. **The transform contract of the GB 1.2 source references** —
   world = parentWorld * local (s=ps*ls, R=pr*lr, t=pt+ps*(pr*lt)); tested on
   translation, parent rotation, uniform scale, a nonidentity asset root and
   reparenting-without-compensation; native ground truth from 2/2 original
   stock printer runs (verbatim `C <96,202,306>, R 0` / `C <58,221,363>, R 0`,
   tol 1e-4, dual-engine IR+THREE parity).
3. **Instance separation (contract §6)** — two independently authored instances
   of the one shared 218757 resource: unique instance IDs, shared geometry,
   independent authored/scene transforms; changing one leaves the other
   bit-identical (trsDeepEqual; re-verified through the app's own builder path
   and visible in the real-browser scene-mode ledger 28 = 2×14); invalid
   instance graphs (duplicate ID, cycle, missing master, dangling parent,
   multi-parent) are loudly rejected, never silently repaired.
4. **Path-denial discipline of the local service (contract §8)** — read-only
   loopback server (127.0.0.1 hardcoded bind, verified-free-port probe, PID
   printed, port-freed proof); 22/22 synthetic denials by the executor + 10/10
   QC-subset, all with explicit error classes and no NIF/BNT payload markers in
   any denial body; static routes are exact allowlist maps (URL never becomes a
   filesystem path); the whole BNT/source trees have NO route; GET/HEAD only.
5. **Real-browser load verification (contract §8 browser rule, honestly
   applied)** — 3 independent real-browser loads to data-load-status=READY
   (executor T9 one-shot ×2 incl. the #scene deep-link; PE-MASTER headless
   loads of BOTH modes; QC's own headless load), each showing canvas + the
   rendered diagnostics (payload SHA, 62+4 accounting, 14/14 ledger, 9+5
   textures) and the labels AUTHOR_PLACED_LAB / RENDER_ADAPTER_CHOICE /
   PE_UNITS_NOT_CONFIRMED in the DOM. Client-side fail-closed pin + transform
   cross-checks + 14/14 fingerprint re-hashes executed in the real browser.
6. **Predecessor continuity** — all 14 NiTriShape/NiTriShapeData associations
   and all 28 vertex/index fingerprints recomputed from the pinned bytes and
   matched to the predecessor's independent Python parser; the 62+4=66 ceiling
   and the FC-C1/C2/C3 supersessions preserved untouched.

## 2. What this slice does NOT cover (explicit)

1. **Interactive smoke — NOT performed.** Orbit/pan/zoom/fit/reset/wireframe/
   dPVS-toggle/instance-select/apply/independence-line are NOT interactively
   observed by anyone in this environment (automation daemon unavailable:
   playwright ECONNREFUSED ::1:9222, confirmed by QC's own retry). Coverage is
   INDIRECT ONLY (the Node app-integration suite through the app's own builder
   path + the window.__pecApp automation surface). Therefore
   BROWSER_VERIFICATION = REAL_BROWSER_LOAD_VERIFIED__INTERACTIVE_NOT_PERFORMED
   and ACCEPTED_RUNNABLE_VERIFIED = NO. SMOKE_CHECKLIST.md is the open gate.
2. **No historical placement.** HISTORICAL_PLACEMENT = NOT_ESTABLISHED;
   MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO. Scene
   coordinates are AUTHOR_PLACED_LAB by construction; the viewer instance
   wrapper policy is explicitly NOT a reproduction of every SDK 2.6
   root-replacement branch or the original PE placement mechanism.
3. **No texture container resolution.** Texture status is name/property
   binding level only: 9 TEXTURE_NAME_BOUND + 5 UNTEXTURED_NO_TEXPROP;
   container resolution NOT_ESTABLISHED everywhere; no texture bytes are
   bound; materials are plain labeled materials. The nine-byte Ark texture
   tail stays RAW_ONLY_UNRESOLVED_FOR_218757 — no new tail semantics derived in
   this run.
4. **No Ark tail/semantic claims.** 4 of 66 blocks remain 2
   PARTIALLY_UNDERSTOOD (NiArkImporterExtraData, NiArkTextureExtraData) + 2
   OPAQUE (NiArkAnimationExtraData, NiArkViewportInfoExtraData); raw bytes are
   recorded with boundaries + decisions, never interpreted beyond that.
5. **NIF 20.5.0.4 not supported.** The reader supports NIF 10.1.0.0 exactly
   (loud gate otherwise). smallpillar.nif (Control A) was header-line recorded
   only; NO NIF 20.5 reader was attempted and none is claimed. The stock GB 1.2
   printer rejects PE Ark content (predecessor standing fact) — no claim of a
   general PE loader.
6. **Terrain not integrated.** The scene grid is an EXPLICITLY AUTHORED lab
   GridHelper; no Eudoria terrain/placement success is manufactured or
   implied.
7. **Single-model scope.** One model (218757), one app, one
   instance/transform path. No corpus expansion (5,595 other Models.bnt
   entries untouched by this slice), no multi-model scene, no animation/LOD/
   attachment execution (surfaced as diagnostics, not implemented), no physics,
   no gameplay, no MMO login, no VM.
8. **Renderer pinned.** three 0.185.0 retained from the pinned base; no
   framework migration, no dependency update. (The 457485 witness reader
   src/pesource/NifModelReader.js is byte-identical to BASE — its single-mesh
   path still does not support 218757 and is not claimed to.)
9. **Original client never executed.** No Entropia.exe run, no EXE bodies, no
   network producer trace, no new corpus search (standing limits of contract §1
   all preserved).
10. **Runtime evidence is instrumented where applicable.** All interventions
    (native printer child processes, Node test/tool runs, loopback servers,
    headless Edge runs) are inventoried with classes and boundaries in
    INTERVENTION_LEDGER.md; INSTRUMENTED_BEHAVIOR != ORIGINAL_CLIENT_BEHAVIOR
    is respected (no original-client behavior claim exists in this run).

## 3. Review-coverage statement (who checked what — no absolutes)

- Executor: built and measured everything (all raw/ artifacts are its own
  executions).
- Fresh internal QC (REVIEW.md §1–§8): re-executed unit 24/24 + app 13/13 + a
  10-request denial subset + its own headless load + a 2-block third-implementation
  raw-byte fingerprint spot-check; read all 29 changed code files to EOF + all
  package artifacts; proprietary census CLEAN; allowlist census compliant.
  NOT_CHECKED by QC: REVIEW.md §10 (Control-A parser re-run, DLL re-hashes,
  native printer re-run, SDK source re-hashes, interactive browser behaviors,
  machine-summary field-by-field re-diff, compat.css full read, predecessor
  file to EOF, historical BASE packages).
- PE-MASTER (PE_MASTER_REVIEW.md): full read of the governing contract, the QC
  review and the phase artifacts; independent re-execution of the unit suite +
  negative control, both-mode headless loads, own server lifecycle and own git
  censuses; NOT_CHECKED by PE-MASTER: Control-A parser re-execution, interactive
  browser behaviors, DLL re-hashes, 12 of 14 fingerprints not spot-recomputed
  itself.
- DESKTOP_POST_AUDIT = PENDING (a separate human gate; not claimed here).
