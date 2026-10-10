# Integration invariants

- A serialized link graph, a class inheritance graph and a scene hierarchy are
  distinct.
- NiStream custom-class registration and link resolution must be respected.
  Stock rejection of NiArk is not proof of a corrupt PE NIF (measured: ALL
  4838 NIF-10.1 entries in PE Models.bnt declare NiArk*; stock-only readers
  are corpus-proven unusable for them).
- Preserve root/local matrices; derive world from parent world × local
  (MEASURED native agreement: probe world bound centers (96,202,306) /
  (58,221,363) reproduced independently by IR math and THREE.Matrix4). Keep
  source coordinates immutable. Convert display axes/units ONCE with a
  documented reversible mapping, labeled RENDER_ADAPTER_CHOICE /
  PE_UNITS_NOT_CONFIRMED — never as PE axis/unit evidence.
- THREE `Object3D.attach` preserves world transform. Do not select it merely
  because an SDK method is called AttachChild. Reconstruct local hierarchy
  intentionally and control matrixAutoUpdate. Reparenting performs NO local
  compensation (measured native trait — world position changes by composition).
- Shared NiGeometryData/BufferGeometry does not mean a shared world instance or
  shared animation state. Reference-count resources used by more than one
  scene instance; keep authored instance IDs and transforms independent.
- Bounds and pivots are not placement coordinates. Auto-centering is a viewer
  operation, not original data.
- Optimizers can remove nodes, propagate transforms and merge geometry.
  Missing named NiNode is insufficient negative evidence for a building's
  geometry or placement record.
- PE textures can bind via NiArk extra data even when a stock texture
  reference is NULL. Follow the actual property/reference pair, not the first
  material in the file. Measured for 218757: 9 name-bound + 5
  UNTEXTURED_NO_TEXPROP; container resolution NOT_ESTABLISHED; the per-entry
  nine-byte tail stays UNRESOLVED — no new tail semantics.
- Parse coverage, semantic coverage, implementation coverage and executed
  verification are different statuses. dPVS/occluder-like NAMES are hints, not
  proven runtime roles — keep such meshes addressable with a clearly labeled
  heuristic visibility toggle and an honest imported-vs-visible ledger.
- Authored laboratory transforms (AUTHOR_PLACED_LAB) and inferred calibration
  stay separate from historical records. Same model ID or mesh pointer does
  not establish instance identity. The viewer's instance-wrapper policy is
  NOT a reproduction of every SDK 2.6 root-replacement branch or the original
  PE placement mechanism.
- Scene-parent links and attachment/source-transform dependencies are SEPARATE
  dependency classes — no transform may be applied twice; unresolved
  attachment execution surfaces an UNSUPPORTED diagnostic, never a silent
  skip. Cycles/dangling required links REJECT loud; multiple parents are
  reported with the full claim list, never silently resolved.
- Gamebryo source helps predict mechanisms; exact PCG offsets/semantics
  require separate PE evidence. A skill or successful screenshot does not
  promote that evidence.

These notes derive from local SDK documentation, prior code inspection and
the MEASURED controls of PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
(native printer comparisons, authored synthetic IR controls, the 218757
adapter battery, and the local browser app gates T7/T8/T9). Reproduce relevant
controls before claiming correctness of a new implementation.
