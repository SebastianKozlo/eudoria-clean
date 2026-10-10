# PREREGISTRATION — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009

Written BEFORE the adapter/app implementation and BEFORE the transform science.
The acceptance shape below is registered up front so later phases cannot quietly
weaken a gate after seeing results. Sources: contract §5–§8.

## 1. Registered app capabilities (the deliverable, contract §7 item 3)

One single app (one HTML page + ES modules) under `compat/` offering:

1. ASSET MODE: model 218757 loaded from pinned Models.bnt bytes, orbit camera,
   fit-to-bounds action, solid/wireframe toggle, axes helper, hierarchy
   inspector (block list with types, links, decode status).
2. AUTHORED SCENE MODE: exactly TWO separate instances of the same 218757
   resource; changing one instance's transform must NOT move the other; each
   instance independently selectable/inspectable; all coordinates labeled
   AUTHOR_PLACED_LAB (NOT historical Eudoria positions).
3. Free camera controls + a discoverable reset/fit action.
4. Diagnostics panel: original asset identity (container/entry/hash), imported
   vs rendered mesh counts, supported/opaque block coverage, material/texture
   status, and original serialized transforms vs computed world transforms as
   DISTINCT quantities (local / file-root / scene / render).

Acceptance predicates (measured, not vibes):
- A1 asset mode loads 218757 through the BNT2 index entry; extraction SHA256 ==
  pin 3E8A22C2...12CF36 (loud fail otherwise).
- A2 imported mesh count == 14 (the 14 mesh/data associations preserved,
  including helper candidates; total imported vs currently visible reported
  separately with exclusion reasons).
- A3 two instances: changing instance X's authored transform leaves instance
  Y's world matrix unchanged (within exact authored-arithmetic tolerance);
  resource geometry shared, instance IDs and transforms independent.
- A4 unknown/missing textures produce a LABELED untextured material +
  diagnostic; geometry viewing remains possible; no false binding.
- A5 browser smoke test executed in a real browser/automation: page load,
  orbit/free-camera/reset and inspector behaviors actually observed. HTTP 200,
  a build, a screenshot name or unit tests do NOT substitute. If browser
  execution is unavailable: BROWSER_VERIFICATION=NOT_PERFORMED and the slice is
  NOT called ACCEPTED_RUNNABLE_VERIFIED.

## 2. Registered transform contract (contract §6)

- Composition law (GB 1.2 source-qualified, re-implemented independently):
  world.scale = parent.scale * local.scale;
  world.rotate = parent.rotate * local.rotate;
  world.translate = parent.translate + parent.scale * (parent.rotate * local.translate);
  root world = local. Point map: (R*p)*s + t. NEVER flatten by summing positions.
- Resource identity separate from runtime instance identity (assetId vs
  instanceId); node TRS separate from property/extra-data links; attachment /
  source-transform dependencies separate from scene-parent links (no transform
  applied twice).
- Render-axis/unit conversion (if any) applied EXACTLY ONCE, labeled
  RENDER_ADAPTER_CHOICE / PE_UNITS_NOT_CONFIRMED; serialized values kept
  intact; comparisons use full matrices or transformed points with tolerances.
- Cycles, dangling required child links REJECTED (loud); multiple parents
  reported, never silently resolved.
- The viewer's instance-wrapper policy is NOT a reproduction of every SDK2.6
  root-replacement branch or the original PE placement mechanism (labeled in
  the app).

## 3. Registered test classes (contract §8; executed in later phases)

- T1 NATIVE_TRANSFORM_CONTROLS: independently implemented IR/Three.js
  composition vs the native Control B ground truth captured this phase —
  ROTATED_SCALED_PARENT probe world position expected (96,202,306);
  THREE_LEVEL_SOCKET probe expected (58,221,363). Comparison = composed camera
  world translate, tolerance-based (e.g. 1e-4 per component), never rendered
  similarity. If IR execution fails: NOT_PERFORMED recorded honestly.
- T2 NONIDENTITY_ROOT: an authored synthetic asset with a NON-identity root +
  parent rotate/scale; conversion applied once; child world position computed
  by the composition law (not position sums).
- T3 REPARENTING: parent change under constant local transform changes world
  position per the law (the GB source does no compensation — reproduced, not
  invented).
- T4 TWO_INSTANCES: shared resource geometry, independent transforms (A3).
- T5 INVALID_LINKS: dangling child link / missing master → controlled loud
  failure with explicit diagnostics; never a silent identity transform.
- T6 MISSING_TEXTURE: missing/unknown texture → labeled untextured material +
  diagnostic, no fabricated binding, no cross-era substitution.
- T7_218757_EXTRACTION: pinned extraction (A1) + ALL 14 mesh/data association
  checks: per-mesh vertex count, triangle count, f32le vertex-array SHA256 and
  u16le index-array SHA256 recomputed from actual decoded arrays and compared
  against the predecessor's MODEL_218757_RELATION_RESULTS.json values
  (e.g. mesh 18 B_Outpost_me01_Ext_sign:0 92 verts / 56 tris, vertex SHA
  3869B16B..., index SHA 56854059...). Any mismatch = loud failure, not a
  weakened gate.
- T8_457485_WITNESS_REGRESSION: run ONLY IF the witness code path
  (src/pesource/NifModelReader.js) is touched; preserves the witness
  regression. Planned adapter design: NifModelReader.js NOT modified (new code
  under src/pecompat/), so T8 is expected NOT_APPLICABLE with the reason
  recorded — if a compatible fix becomes necessary under src/pesource/, T8
  becomes MANDATORY before that change is accepted.
- T9_BROWSER_SMOKE: real local API-to-browser load + orbit/free-camera/reset +
  inspector behavior (A5), plus synthetic path-denial requests against the
  server (traversal attempts return 403/404 — never original bytes outside the
  configured roots).

## 4. Registered Control A expectations (metadata/link control)

- Ten pillar instance→master links in terrain.gsa, all resolving to one master
  definition `[TerrainSample]pillar` in TerrainSample.pal; every instance
  TemplateID equal to the master's TemplateID; instance identity = distinct
  per-instance LinkIDs + per-instance serialized Local TRS (TemplateID is NOT
  instance identity).
- NIF path inheritance: 0/10 instance scene-graph components carry their own
  NIF File Path; the master component's path (`.\..\NIFs\smallpillar.nif`) is
  inherited (NiSceneGraphComponent.inl:31 mechanism).
- Dependencies explicit: scene palette dependency `.\Palettes\TerrainSample.pal`;
  flattened-extraction relative-path status NOT_ESTABLISHED; missing masters
  listed if any (expected: none).
- smallpillar.nif = NIF 20.5.0.4 recorded; NO 20.5 reader attempted; the GB 1.2
  tool does NOT support it (no pretending).
- Coordinate label: GB26_SDK_SAMPLE_VALUES (never PE coordinates).

Measured outcome (this phase): 10/10 links resolved, 10/10 template matches,
0 missing masters/components, 0 unresolved refs; two distinct instance
transforms captured (pillar 04, pillar 05). See CONTROLS_A.json.

## 5. Registered Control B expectations (native transform controls)

- Both fixtures re-measured (327 B / 430 B + SHAs) before execution.
- ORIGINAL stock printer (fd693af2...) executed headlessly with sandbox-local
  VC71 DLLs via child PATH; per-process timeout; raw stdout/stderr/exit
  captured verbatim.
- Expected native probe world-bound centers (source-qualified for THESE
  CONTROLS ONLY; camera bound centers, NOT geometry pivots):
  ROTATED_SCALED_PARENT → (96,202,306); THREE_LEVEL_SOCKET → (58,221,363).
- The IR/Three.js comparison vs these values is a NEXT-PHASE gate (T1); native
  capture alone is NOT parity. If native execution were unavailable the honest
  class is NOT_PERFORMED (it was available: both runs exit 0).

Measured outcome (this phase): both fixtures exit 0; observed probe centers
(96,202,306) and (58,221,363) — both MATCH the expected values. See
CONTROLS_B.json + raw/CONTROL_B/.

## 6. Registered honest-failure classes

- NOT_PERFORMED — a registered test could not be executed; recorded with the
  blocker; NEVER silently skipped or converted into a pass.
- BROWSER_VERIFICATION=NOT_PERFORMED — fallback when browser/automation is
  unavailable; the run is then NOT ACCEPTED_RUNNABLE_VERIFIED.
- PARTIAL — some gates pass, others blocked; final report carries the honest
  per-gate table.
- BLOCKED_<reason> — the run stops at a measured blocker (e.g.
  BLOCKED_WORKTREE_COLLISION / BLOCKED_BASELINE per contract §2 — both
  pre-verified ABSENT in this phase).

## 7. Registered non-goals (unchanged from contract §1/§9)

- No historical placement claims; no Entropia.exe execution; no master
  changes; no new EXE function bodies; no corpus search beyond the named
  inputs; no new nine-byte-tail semantics; no NIF 20.5 reader; no full 2.6
  engine port; no full animation/attachment/LOD execution (unsupported cases
  surfaced as diagnostics).
- HISTORICAL_PLACEMENT = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO;
  CANONICAL_GATE_EFFECT = NONE at every phase boundary.
