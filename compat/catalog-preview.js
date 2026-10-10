// catalog-preview.js — PE_CITY_ASSET_MAP_R1_20261010, phase 4 (contract §5)
// THE /catalog PREVIEW for the FOUR pinned CD_2003 primaries (safe import
// established by the phase-3 bounded NIF-4.1 reader; DECODED_FULL_CLOSURE).
//
// REUSE LABEL: the preview follows the SceneIR app's proven patterns
// (compat/asset-mode.js + compat/api.js) — THREE INJECTED via ctx (this
// module imports NO renderer dependency at module level, so Node tests can
// import the pure exports); client-side world-transform composition via
// src/pecompat/PecSceneIR.js composeWorldTransforms with a fail-closed
// cross-check against the SERVER-shipped composed bounds; fit/reset actions;
// solid/wireframe toggle; picking. It deliberately does NOT reuse
// PecRenderConvert's (x,z,-y)×0.01 render conversion: the catalog preview
// shows ORIGINAL FILE coordinates (SOURCE_FILE_SCENE_SPACE) with NO axis swap
// and NO unit conversion. The ONLY presentation-space operation is the optional
// CENTERING, applied EXACTLY ONCE at the presentation wrapper (the
// "fit-to-view" mode); the "original coords" mode keeps the wrapper at
// identity and moves the CAMERA instead. Original vertex values stay intact
// in BOTH modes.
//
// POLICY (never removed in this UI):
//   SOURCE_FILE_SCENE_SPACE ≠ WORLD_PLACEMENT; ORIGINAL file units (unit
//   semantics NOT established — never called meters); the four primaries are
//   UNTEXTURED_PROXY_MESH — the preview applies ONLY the verified
//   NiMaterialProperty diffuse colors (material preview); NO fake textures.

import { composeWorldTransforms } from '../src/pecompat/PecSceneIR.js';

export const PREVIEW_VIEW_MODES = Object.freeze({
  CENTERED: 'CENTERED',       // fit-to-view: wrapper offset = -center (applied EXACTLY ONCE)
  ORIGINAL: 'ORIGINAL',       // original coordinates: wrapper identity; camera looks at the center
});
export const PREVIEW_WRAPPER_POLICY =
  'presentation wrapper: centering ONLY in the CENTERED view mode, applied EXACTLY ONCE at the wrapper; NO unit conversion, NO axis swap, NO double-centering; original vertex values intact; the ORIGINAL coords mode keeps the wrapper at identity (the camera moves instead)';

/** The AABB center of the shipped bounds (FILE_SCENE_SPACE). PURE. */
export function wrapperCenter(bounds) {
  if (!bounds || bounds.unknown) return null;
  return [
    (bounds.min[0] + bounds.max[0]) / 2,
    (bounds.min[1] + bounds.max[1]) / 2,
    (bounds.min[2] + bounds.max[2]) / 2,
  ];
}

/** Wrapper offset for a view mode — the ONLY presentation-space transform. PURE. */
export function wrapperOffsetFor(mode, bounds) {
  const c = wrapperCenter(bounds);
  if (mode === PREVIEW_VIEW_MODES.ORIGINAL || !c) return [0, 0, 0];
  return [-c[0], -c[1], -c[2]]; // centering applied EXACTLY ONCE (never twice)
}

/** file -> rendered: v + offset (component-wise identity map — no swap/scale). PURE. */
export function fileSpaceToRendered(v, offset) {
  return [v[0] + offset[0], v[1] + offset[1], v[2] + offset[2]];
}

/** rendered -> file: the exact inverse of fileSpaceToRendered. PURE. */
export function applyWrapperToFileSpace(v, offset) {
  return [v[0] - offset[0], v[1] - offset[1], v[2] - offset[2]];
}

/** Row-major NIF 4.1 rotation (p' = R·p) -> renderer basis columns.
 * For a column-major M with v' = M·v, the basis vectors are R's COLUMNS. PURE. */
export function localTrsToColumns(localTrs) {
  if (!localTrs) return null;
  const R = localTrs.rotate;
  return {
    basisX: [R[0][0], R[1][0], R[2][0]],
    basisY: [R[0][1], R[1][1], R[2][1]],
    basisZ: [R[0][2], R[1][2], R[2][2]],
    translate: [...localTrs.translate],
    scale: localTrs.scale,
  };
}

export function boundsEqualWithin(a, b, tol) {
  if (!a || !b || a.unknown || b.unknown) return false;
  for (let k = 0; k < 3; k++) {
    if (Math.abs(a.min[k] - b.min[k]) > tol) return false;
    if (Math.abs(a.max[k] - b.max[k]) > tol) return false;
  }
  return true;
}

/** Build the preview scene objects from the wire. THREE injected (Node tests
 * may pass a stub — the returned graph is only walked by the browser path). */
export function buildPreviewObjects(THREE, wire, { geometryCache } = {}) {
  const byIndex = new Map(wire.blocks.map((b) => [b.index, b]));
  const materialsByShape = new Map(wire.materials.map((m) => [m.shapeBlock, m]));
  const nodes = new Map();      // block index -> Object3D (NiNode / NiTriShape)
  const meshObjects = [];
  const materialApplications = []; // MATERIAL_APPLIED evidence rows (measured)

  const setLocalTrs = (obj, local) => {
    if (!local) return;
    const cols = localTrsToColumns(local);
    obj.position.fromArray(cols.translate);
    obj.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(
      new THREE.Vector3().fromArray(cols.basisX),
      new THREE.Vector3().fromArray(cols.basisY),
      new THREE.Vector3().fromArray(cols.basisZ),
    ));
    obj.scale.setScalar(cols.scale);
  };

  for (const b of wire.blocks) {
    if (b.type === 'NiNode') {
      const g = new THREE.Group();
      g.name = `node[${b.index}] ${b.name ?? ''}`;
      setLocalTrs(g, b.localTrs);
      nodes.set(b.index, g);
    }
  }
  for (const b of wire.blocks) {
    if (b.type !== 'NiTriShape') continue;
    const data = b.dataRef != null ? byIndex.get(b.dataRef) : null;
    if (!data?.geometry) continue;
    const g = data.geometry;
    let geometry = geometryCache?.get(b.dataRef);
    if (!geometry) {
      geometry = new THREE.BufferGeometry();
      geometry.setAttribute('position', new THREE.BufferAttribute(Float32Array.from(g.positions), 3));
      if (g.normals) geometry.setAttribute('normal', new THREE.BufferAttribute(Float32Array.from(g.normals), 3));
      if (g.indices?.length) geometry.setIndex(new THREE.BufferAttribute(Uint16Array.from(g.indices), 1));
      if (!g.normals) geometry.computeVertexNormals();
      geometryCache?.set(b.dataRef, geometry);
    }
    const mat = materialsByShape.get(b.index);
    const material = new THREE.MeshStandardMaterial({
      color: new THREE.Color().fromArray(mat?.diffuse ?? [0.75, 0.75, 0.75]),
      roughness: 0.72, metalness: 0.08,
      ...(mat?.alpha != null && mat.alpha < 1 ? { transparent: true, opacity: mat.alpha } : {}),
    });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.name = `shape[${b.index}] ${b.name ?? ''}`;
    mesh.userData = {
      meshBlock: b.index, dataBlock: b.dataRef,
      meshName: b.name,
      materialBlock: mat?.materialBlock ?? null,
      uvSets: g.uvSets?.length ?? 0,
      numTriangles: g.numTriangles, numVertices: g.numVertices,
    };
    setLocalTrs(mesh, b.localTrs);
    if (mat && mat.materialBlock != null) {
      materialApplications.push({
        shapeBlock: b.index, shapeName: b.name,
        materialBlock: mat.materialBlock, materialName: mat.materialName,
        referenceClass: mat.referenceClass,
        diffuse: mat.diffuse,
        applied: true, // the diffuse color IS applied to this mesh's material
        note: 'NiMaterialProperty diffuse color applied (material preview); UNTEXTURED_PROXY_MESH — no texture image applied',
      });
    }
    nodes.set(b.index, mesh);
    meshObjects.push(mesh);
  }
  // attach children to parents (verified children refs; unparented scene
  // objects go under the root group)
  const rootGroup = new THREE.Group();
  rootGroup.name = 'preview-root (FILE_SCENE_SPACE)';
  const claimed = new Set();
  for (const other of wire.blocks) {
    for (const c of other.children ?? []) {
      if (c == null || c < 0) continue;
      const child = nodes.get(c);
      const parent = nodes.get(other.index);
      if (child && parent) { parent.add(child); claimed.add(c); }
    }
  }
  for (const [idx, obj] of nodes) {
    if (!claimed.has(idx)) rootGroup.add(obj);
  }
  return { rootGroup, nodes, meshObjects, materialApplications };
}

/** Wire -> IR-like shape for composeWorldTransforms (the client-side
 * independent composition used by the fail-closed cross-check). */
function wireToCompositionIR(wire) {
  const blocks = wire.blocks.map((b) => ({
    index: b.index, type: b.type,
    localTrs: b.localTrs
      ? { translate: [...b.localTrs.translate], rotate: b.localTrs.rotate.map((r) => [...r]), scale: b.localTrs.scale }
      : null,
    children: b.children ?? null,
    dataRef: b.dataRef ?? null,
    geometry: b.geometry ? { positions: Float32Array.from(b.geometry.positions), numVertices: b.geometry.numVertices } : null,
    decodeStatus: b.decodeStatus, name: b.name,
  }));
  return {
    blocks,
    roots: wire.roots,
    meshAssociations: wire.meshRows.map((m) => ({ meshBlock: m.shapeBlock, dataBlock: m.dataBlock })),
  };
}

/** Verify the served wire client-side (fail-closed): recompose the world
 * transforms + bounds INDEPENDENTLY and compare with the SERVER-shipped
 * values; re-hash geometry fingerprints when crypto.subtle is available
 * (honest NOT_PERFORMED_SUBTLE_UNAVAILABLE otherwise — never a silent pass). */
export async function verifyWireClientSide(wire, { tol = 1e-4 } = {}) {
  const problems = [];
  const ir = wireToCompositionIR(wire);
  let worldTransforms;
  try {
    worldTransforms = composeWorldTransforms(ir);
  } catch (e) {
    return { ok: false, problems: [`client-side composition failed: ${e.message}`], fingerprintCheck: null };
  }
  for (const b of wire.blocks) {
    if (!b.localTrs) continue;
    const w = worldTransforms.get(b.index);
    if (!w) { problems.push(`block ${b.index}: composition did not reach an AVObject with localTrs`); continue; }
    for (let k = 0; k < 3; k++) {
      if (Math.abs(w.translate[k] - b.localTrs.translate[k]) > tol) {
        problems.push(`block ${b.index}: composed translate[${k}] ${w.translate[k]} != local ${b.localTrs.translate[k]} (unexpected non-identity composition)`);
      }
    }
  }
  let minX = Infinity, minY = Infinity, minZ = Infinity;
  let maxX = -Infinity, maxY = -Infinity, maxZ = -Infinity;
  let any = false;
  for (const b of ir.blocks) {
    if (!b.geometry?.positions) continue;
    const w = worldTransforms.get(b.index);
    if (!w) continue;
    any = true;
    const p = b.geometry.positions;
    for (let i = 0; i < p.length; i += 3) {
      const x = p[i], y = p[i + 1], z = p[i + 2];
      const rx = w.rotate[0][0] * x + w.rotate[0][1] * y + w.rotate[0][2] * z;
      const ry = w.rotate[1][0] * x + w.rotate[1][1] * y + w.rotate[1][2] * z;
      const rz = w.rotate[2][0] * x + w.rotate[2][1] * y + w.rotate[2][2] * z;
      const wx = rx * w.scale + w.translate[0];
      const wy = ry * w.scale + w.translate[1];
      const wz = rz * w.scale + w.translate[2];
      if (wx < minX) minX = wx; if (wx > maxX) maxX = wx;
      if (wy < minY) minY = wy; if (wy > maxY) maxY = wy;
      if (wz < minZ) minZ = wz; if (wz > maxZ) maxZ = wz;
    }
  }
  const sb = wire.sceneBounds_FILE_SCENE_SPACE;
  if (any) {
    const tolB = 1e-3;
    for (let k = 0; k < 3; k++) {
      if (Math.abs(minX - sb.min[0]) > tolB && k === 0) problems.push(`bounds cross-check FAILED on axis 0: client [${minX}, ${maxX}] vs shipped [${sb.min[0]}, ${sb.max[0]}] — refusing (wire corruption cannot silently render)`);
      if (k === 1 && (Math.abs(minY - sb.min[1]) > tolB || Math.abs(maxY - sb.max[1]) > tolB)) problems.push(`bounds cross-check FAILED on axis 1: client [${minY}, ${maxY}] vs shipped [${sb.min[1]}, ${sb.max[1]}] — refusing`);
      if (k === 2 && (Math.abs(minZ - sb.min[2]) > tolB || Math.abs(maxZ - sb.max[2]) > tolB)) problems.push(`bounds cross-check FAILED on axis 2: client [${minZ}, ${maxZ}] vs shipped [${sb.min[2]}, ${sb.max[2]}] — refusing`);
    }
  }
  let fingerprintCheck = { status: 'NOT_PERFORMED_SUBTLE_UNAVAILABLE', verified: 0, mismatches: [] };
  if (typeof crypto !== 'undefined' && crypto?.subtle?.digest) {
    fingerprintCheck = { status: 'OK', verified: 0, mismatches: [] };
    const sha = async (bytes) => {
      const d = await crypto.subtle.digest('SHA-256', bytes);
      return [...new Uint8Array(d)].map((x) => x.toString(16).padStart(2, '0')).join('');
    };
    for (const b of wire.blocks) {
      if (!b.geometry?.positions) continue;
      const pos = Float32Array.from(b.geometry.positions);
      const idx = Uint16Array.from(b.geometry.indices ?? []);
      const vSha = await sha(new Uint8Array(pos.buffer, pos.byteOffset, pos.byteLength));
      const iSha = await sha(new Uint8Array(idx.buffer, idx.byteOffset, idx.byteLength));
      if (vSha === b.geometry.vertexPositionsF32leSha256 && iSha === b.geometry.triangleIndicesU16leSha256) fingerprintCheck.verified++;
      else fingerprintCheck.mismatches.push({ block: b.index });
    }
    if (fingerprintCheck.mismatches.length > 0) {
      fingerprintCheck.status = 'FINGERPRINT_MISMATCH';
      problems.push(`geometry fingerprint mismatch on ${fingerprintCheck.mismatches.length} block(s) — refusing`);
    }
  }
  return { ok: problems.length === 0, problems, fingerprintCheck, worldTransforms };
}

// ---------------------------------------------------------------------------
// browser mount (all DOM/THREE wiring lives below — Node imports never run it)
// ---------------------------------------------------------------------------
export function mountCatalogPreview(ctx) {
  const T = ctx.THREE; // THREE INJECTED (Node-testable module discipline)
  const { scene, wire, ui, hud, observable } = ctx;
  const controls = ctx.controls;

  const { rootGroup, nodes, meshObjects, materialApplications } =
    buildPreviewObjects(T, wire, { geometryCache: ctx.geometryCache });

  // ---- the ONE presentation wrapper (centering only, applied once) ----
  const wrapper = new T.Group();
  wrapper.name = 'presentation-wrapper (centering ONLY in CENTERED mode; NO unit conversion; NO axis swap; SOURCE_FILE_SCENE_SPACE != WORLD_PLACEMENT)';
  wrapper.add(rootGroup);
  scene.add(wrapper);

  const sb = wire.sceneBounds_FILE_SCENE_SPACE;
  const state = {
    viewMode: PREVIEW_VIEW_MODES.CENTERED,
    wireframe: false,
    selectedShape: null,
    hiddenShapes: [],
    wrapperOffset: [0, 0, 0],
    wire, meshObjects, materialApplications,
  };

  // axes helper at the FILE-space origin (the ORIGINAL origin stays visible)
  const axesSize = Math.max(...sb.extents) * 0.06;
  const axes = new T.AxesHelper(axesSize);
  axes.name = 'file-space origin axes (AUTHORED aid; ORIGINAL coordinates)';
  rootGroup.add(axes);

  // bounds box helper (FILE_SCENE_SPACE AABB — lives INSIDE the wrapper so it
  // receives the same single centering as the geometry)
  const boundsBox = new T.Box3(
    new T.Vector3(sb.min[0], sb.min[1], sb.min[2]),
    new T.Vector3(sb.max[0], sb.max[1], sb.max[2]),
  );
  const boxHelper = new T.Box3Helper(boundsBox, 0x335577);
  boxHelper.name = 'scene bounds (FILE_SCENE_SPACE)';
  wrapper.add(boxHelper);

  function applyViewMode() {
    const off = wrapperOffsetFor(state.viewMode, sb);
    state.wrapperOffset = [...off];
    wrapper.position.fromArray(off); // centering applied EXACTLY ONCE here
    if (state.viewMode === PREVIEW_VIEW_MODES.ORIGINAL && controls) {
      // camera looks at the ORIGINAL bounds center (geometry untouched)
      const c = wrapperCenter(sb);
      controls.target.set(c[0], c[1], c[2]);
    }
    if (ui?.btnOrigcoords) ui.btnOrigcoords.classList.toggle('active', state.viewMode === PREVIEW_VIEW_MODES.ORIGINAL);
    if (observable?.previewState) {
      observable.previewState.viewMode = state.viewMode;
      observable.previewState.wrapperOffset = [...off];
    }
    renderWrapperDiagnostics();
  }

  function fitToBounds() {
    const box = new T.Box3();
    const tmp = new T.Box3();
    let any = false;
    for (const mesh of meshObjects) {
      if (!mesh.visible) continue;
      tmp.setFromObject(mesh);
      box.union(tmp);
      any = true;
    }
    if (!any) return;
    const camera = ctx.camera;
    const center = box.getCenter(new T.Vector3());
    const sphere = box.getBoundingSphere(new T.Sphere());
    const fovRad = (camera.fov * Math.PI) / 180;
    const dist = (sphere.radius / Math.sin(fovRad / 2)) * 1.15;
    const dirV = camera.position.clone().sub(controls.target).normalize();
    if (dirV.lengthSq() < 1e-8) dirV.set(0, 0.5, 1).normalize();
    controls.target.copy(center);
    camera.position.copy(center).addScaledVector(dirV, dist);
    controls.update();
  }

  function setWireframe(on) {
    state.wireframe = on;
    for (const mesh of meshObjects) mesh.material.wireframe = on;
    if (observable?.previewState) observable.previewState.wireframe = on;
  }

  function setPartVisible(shapeBlock, visible) {
    const mesh = meshObjects.find((m) => m.userData.meshBlock === shapeBlock);
    if (mesh) mesh.visible = visible;
    state.hiddenShapes = meshObjects.filter((m) => !m.visible).map((m) => m.userData.meshBlock);
    if (observable?.previewState) observable.previewState.hiddenShapes = [...state.hiddenShapes];
  }

  function renderWrapperDiagnostics() {
    if (!ui?.diagWrapper) return;
    const c = wrapperCenter(sb);
    ui.diagWrapper.innerHTML =
      `<div>view mode: ${state.viewMode === PREVIEW_VIEW_MODES.CENTERED ? 'CENTERED (fit-to-view)' : 'ORIGINAL coordinates'}` +
      ` — wrapper offset [${state.wrapperOffset.map((v) => v.toFixed(2)).join(', ')}]` +
      (state.viewMode === PREVIEW_VIEW_MODES.ORIGINAL
        ? ' (wrapper identity — camera moved instead; centering NOT applied)'
        : ` (centering applied EXACTLY ONCE = -center [${c.map((v) => v.toFixed(2)).join(', ')}])`) +
      `</div>` +
      `<div class="policy">${PREVIEW_WRAPPER_POLICY}</div>`;
  }

  if (ctx.canvas && ctx.pickHandler) {
    ctx.canvas.addEventListener('pointerdown', (ev) => ctx.pickHandler(ev, meshObjects, (mesh) => {
      state.selectedShape = mesh.userData.meshBlock;
      if (observable?.previewState) observable.previewState.selectedShape = mesh.userData.meshBlock;
    }));
  }

  applyViewMode();
  return {
    kind: 'catalog-preview',
    wire, state, wrapper, nodes, meshObjects, materialApplications,
    fitToBounds, setWireframe, setPartVisible, applyViewMode, renderWrapperDiagnostics,
    setViewMode(mode) { state.viewMode = mode; applyViewMode(); },
    dispose() {
      scene.remove(wrapper);
      // geometries are cached per data block at app level; disposed by app teardown
    },
  };
}
