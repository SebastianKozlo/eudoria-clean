// PecRenderConvert.js — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// The RENDER conversion layer (contract §6/§7): SceneIR (FILE_SCENE_SPACE) ->
// THREE r185 objects. THREE is INJECTED by the caller (buildRenderModel takes
// the THREE module as its first argument) so this module carries no import
// side effects in Node tests (zero new dependencies; the app phase injects
// its importmap-resolved three 0.185.0).
//
// RENDER_ADAPTER_CHOICE (applied EXACTLY ONCE, original values intact):
//   axis map (x, z, -y), unit scale 0.01  — the same labeled display class the
//   old compat app used. PE_AXES_AND_UNITS = UNVERIFIED_FROM_ENGINE; this is
//   a RENDER_ADAPTER_CHOICE / PE_UNITS_NOT_CONFIRMED convenience mapping, NOT
//   evidence of PE axes or units. Serialized TRS values in the IR are NEVER
//   mutated: the conversion exists as exactly ONE matrix at the render-space
//   root group; all scene-space composition below it is untouched. Render
//   bounds are derived from the SAME single conversion.
//
// GEOMETRY SHARING (NiGeometry SetModelData basis): BufferGeometry objects
// are cached per data block on the ASSET — two instances of one asset share
// the SAME BufferGeometry instances (object identity), while their object
// transforms and instance IDs stay independent (tested in T3).
//
// MATERIALS: this run resolves NO texture bytes (container resolution
// NOT_ESTABLISHED for 218757). Meshes get a PLAIN labeled material:
//   - TEXTURE_NAME_BOUND meshes: MeshStandardMaterial with the texture NAMES
//     carried in userData (no texture bound — no false binding);
//   - UNTEXTURED_* meshes: MeshBasicMaterial-style plain material, labeled.
// Geometry stays viewable in both cases.

import { trsToColumnMajor4 } from './PecTransform.js';

export const PEC_RENDER_CONVERT_VERSION = 'pec-renderconvert-v1';

export const RENDER_ADAPTER_CHOICE = Object.freeze({
  id: 'PE_ZUP_CM_TO_THREE_YUP_M_V1',
  axisMap: '(x, z, -y)',
  unitScale: 0.01,
  labels: ['RENDER_ADAPTER_CHOICE', 'PE_UNITS_NOT_CONFIRMED'],
  note: 'PE axes/units are UNVERIFIED_FROM_ENGINE; this display conversion is a RENDER_ADAPTER_CHOICE applied exactly once at the render-space root, leaving all serialized values intact. NOT evidence of PE axes or units.',
});

/** Convert ONE point from FILE_SCENE_SPACE to render space (the single
 * conversion law; also used by tests to verify the tree applies it exactly
 * once). p -> [p.x*u, p.z*u, -p.y*u] */
export function convertPointSceneToRender(p, choice = RENDER_ADAPTER_CHOICE) {
  const u = choice.unitScale;
  return [p[0] * u, p[2] * u, -p[1] * u];
}

/** The conversion as a THREE.Matrix4 (THREE's .set() takes ROW-major args):
 * x' = 0.01x, y' = 0.01z, z' = -0.01y. */
export function conversionMatrix(THREE, choice = RENDER_ADAPTER_CHOICE) {
  const u = choice.unitScale;
  const m = new THREE.Matrix4();
  m.set(
    u, 0, 0, 0,
    0, 0, u, 0,
    0, -u, 0, 0,
    0, 0, 0, 1,
  );
  return m;
}

/** Render-space bounds from FILE_SCENE_SPACE bounds: convert all 8 corners
 * through the SINGLE conversion law, take min/max (axis flip handled by
 * corner conversion, not by guessing component swaps). */
export function convertBoundsSceneToRender(bounds, choice = RENDER_ADAPTER_CHOICE) {
  const corners = [];
  for (const x of [bounds.min[0], bounds.max[0]]) {
    for (const y of [bounds.min[1], bounds.max[1]]) {
      for (const z of [bounds.min[2], bounds.max[2]]) {
        corners.push(convertPointSceneToRender([x, y, z], choice));
      }
    }
  }
  const min = [Infinity, Infinity, Infinity];
  const max = [-Infinity, -Infinity, -Infinity];
  for (const c of corners) {
    for (let k = 0; k < 3; k++) {
      if (c[k] < min[k]) min[k] = c[k];
      if (c[k] > max[k]) max[k] = c[k];
    }
  }
  return { min, max, extents: [max[0] - min[0], max[1] - min[1], max[2] - min[2]], space: 'RENDER_SPACE' };
}

/**
 * buildRenderModel — build the THREE object tree for an asset, optionally
 * wrapped by an authored instance.
 * @param {*} THREE — the injected three module (0.185.0)
 * @param {object} asset — { ir, worldTransforms } (from PecAssetAdapter.loadModel)
 * @param {object} opts — { instance?: {instanceId, sceneTrs}, materialChoice?,
 *                          conversionCountHook?: (n)=>void, geometryCache?: Map }
 *   instance: when given, an instance wrapper group is created that OWNS the
 *   instance's composed scene transform; the asset hierarchy below it keeps
 *   its serialized local transforms (viewer wrapper policy).
 *   geometryCache: pass ONE cache for multiple instances of the same asset to
 *   share BufferGeometry objects (resource geometry shared; transforms not).
 * @returns {{ root: THREE.Group, renderSpaceRoot: THREE.Group, assetRoot: THREE.Group,
 *             instanceWrapper: THREE.Group|null, meshObjects: Array, geometryCache: Map,
 *             conversion: {appliedOnce: true, applications: number} }}
 */
export function buildRenderModel(THREE, asset, opts = {}) {
  const { ir, worldTransforms } = asset;
  // Caller-owned geometry cache: when the same asset is instantiated TWICE,
  // the caller passes ONE cache so both instances share the SAME
  // BufferGeometry objects (resource-geometry sharing; transforms stay
  // independent). Per-call fallback cache otherwise.
  const geometryCache = opts.geometryCache ?? new Map(); // dataBlock -> THREE.BufferGeometry
  let conversionApplications = 0;

  const root = new THREE.Group();
  root.name = 'pec-render-root';

  // THE single render-space conversion: one matrix at one node.
  const renderSpaceRoot = new THREE.Group();
  renderSpaceRoot.name = 'render-space [' + RENDER_ADAPTER_CHOICE.labels.join('|') + '] ' + RENDER_ADAPTER_CHOICE.axisMap + ' x' + RENDER_ADAPTER_CHOICE.unitScale;
  renderSpaceRoot.matrixAutoUpdate = false;
  renderSpaceRoot.matrix.copy(conversionMatrix(THREE));
  conversionApplications += 1;
  if (typeof opts.conversionCountHook === 'function') opts.conversionCountHook(conversionApplications);
  root.add(renderSpaceRoot);

  let instanceWrapper = null;
  let attachUnder = renderSpaceRoot;
  if (opts.instance) {
    instanceWrapper = new THREE.Group();
    instanceWrapper.name = `instance-wrapper:${opts.instance.instanceId}`;
    instanceWrapper.matrixAutoUpdate = false;
    instanceWrapper.matrix.fromArray(trsToColumnMajor4(opts.instance.sceneTrs));
    renderSpaceRoot.add(instanceWrapper);
    attachUnder = instanceWrapper;
  }

  // material factory: plain labeled materials ONLY (no texture bytes resolved
  // in this run — container resolution NOT_ESTABLISHED; no false binding).
  const bindings = new Map((ir.diagnostics.textureBindings ?? []).map((b) => [b.meshBlock, b]));
  const makeMaterial = (meshBlock, meshName) => {
    const b = bindings.get(meshBlock);
    const mat = new THREE.MeshStandardMaterial({ color: 0xb0b0b8, roughness: 0.9, metalness: 0.0 });
    if (b) {
      mat.userData.textureBindingStatus = b.status;
      mat.userData.textureNames = b.textureNames;
      mat.userData.containerResolution = b.containerResolution;
    } else {
      mat.userData.textureBindingStatus = 'SYNTHETIC_NO_BINDING';
    }
    mat.userData.meshName = meshName;
    mat.userData.materialClass =
      b?.status === 'TEXTURE_NAME_BOUND'
        ? 'PLAIN_LABELED (texture names recorded; container resolution NOT_ESTABLISHED — no texture bytes bound in this run)'
        : 'UNTEXTURED_LABELED (diagnostic recorded; geometry viewable)';
    return mat;
  };

  const getGeometry = (dataBlock) => {
    if (geometryCache.has(dataBlock)) return geometryCache.get(dataBlock);
    const dataRec = ir.blocks.find((b) => b.index === dataBlock);
    const g = dataRec?.geometry;
    if (!g) throw new Error(`[PecRenderConvert] data block ${dataBlock} has no geometry — LOUD FAIL`);
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(g.positions, 3));
    if (g.normals) geo.setAttribute('normal', new THREE.BufferAttribute(g.normals, 3));
    if (g.uvSets && g.uvSets.length > 0) geo.setAttribute('uv', new THREE.BufferAttribute(g.uvSets[0], 2));
    if (g.colors) geo.setAttribute('color', new THREE.BufferAttribute(g.colors, 4));
    geo.setIndex(new THREE.BufferAttribute(g.indices, 1));
    if (!g.normals) geo.computeVertexNormals();
    geo.userData = {
      dataBlock,
      numVertices: g.numVertices,
      numTriangles: g.numTriangles,
      vertexPositionsF32leSha256: g.vertexPositionsF32leSha256 ?? null,
      triangleIndicesU16leSha256: g.triangleIndicesU16leSha256 ?? null,
    };
    geometryCache.set(dataBlock, geo);
    return geo;
  };

  // Build the asset hierarchy below `attachUnder` using LOCAL transforms —
  // THREE composes them; the scene-space world matrices therefore equal the
  // FILE_SCENE_SPACE composition law (asserted by tests).
  const byIndex = new Map(ir.blocks.map((b) => [b.index, b]));
  const sceneMembers = new Set();
  const walk = (i) => {
    if (sceneMembers.has(i)) return;
    sceneMembers.add(i);
    for (const c of byIndex.get(i)?.children ?? []) {
      if (c != null && c >= 0) walk(c);
    }
  };
  for (const r of ir.roots) walk(r);

  const meshObjects = [];
  const nodeGroups = new Map();
  const buildNode = (blockIndex, threeParent) => {
    const b = byIndex.get(blockIndex);
    if (!b || !sceneMembers.has(blockIndex)) return null;
    if (nodeGroups.has(blockIndex)) {
      // multi-parent would land here; the IR validator already rejects it —
      // reaching this branch means a bug upstream.
      throw new Error(`[PecRenderConvert] block ${blockIndex} built twice — MULTI_PARENT must have been rejected upstream (LOUD FAIL)`);
    }
    const group = new THREE.Group();
    group.name = `[${blockIndex}] ${b.type}:${b.name ?? ''}`;
    if (b.localTrs) {
      group.matrixAutoUpdate = false;
      group.matrix.fromArray(trsToColumnMajor4(b.localTrs));
    }
    threeParent.add(group);
    nodeGroups.set(blockIndex, group);
    if (b.type === 'NiTriShape') {
      const geo = getGeometry(b.dataRef);
      const mat = makeMaterial(blockIndex, b.name);
      const mesh = new THREE.Mesh(geo, mat);
      mesh.name = `mesh[${blockIndex}] ${b.name ?? ''}`;
      mesh.userData = {
        meshBlock: blockIndex, dataBlock: b.dataRef, meshName: b.name,
        decodeStatus: b.decodeStatus,
        dPVSHeuristicHint: /dpvs|occ/i.test(b.name ?? '')
          ? 'dPVS_NAME_HEURISTIC_HINT (name hint only; runtime role NOT proven; mesh stays addressable and rendered)'
          : null,
      };
      const wire = new THREE.LineSegments(
        new THREE.WireframeGeometry(geo),
        new THREE.LineBasicMaterial({ color: 0x404048, transparent: true, opacity: 0.35 }),
      );
      wire.visible = false;
      wire.name = `wire[${blockIndex}]`;
      mesh.add(wire);
      group.add(mesh);
      meshObjects.push(mesh);
    }
    for (const c of b.children ?? []) {
      if (c != null && c >= 0) buildNode(c, group);
    }
    return group;
  };
  const assetRoot = new THREE.Group();
  assetRoot.name = `asset:${ir.asset.assetId}`;
  attachUnder.add(assetRoot);
  for (const r of ir.roots) buildNode(r, assetRoot);

  root.updateMatrixWorld(true);

  return {
    root,
    renderSpaceRoot,
    assetRoot,
    instanceWrapper,
    meshObjects,
    geometryCache,
    conversion: {
      appliedOnce: conversionApplications === 1,
      applications: conversionApplications,
      choice: RENDER_ADAPTER_CHOICE,
    },
  };
}

/** Render-space bounds of a built model (uses the SAME single conversion —
 * THREE's own world matrices already include it exactly once). */
export function computeRenderBounds(THREE, renderModel) {
  const box = new THREE.Box3();
  const tmp = new THREE.Box3();
  for (const mesh of renderModel.meshObjects) {
    tmp.setFromObject(mesh);
    box.union(tmp);
  }
  return box;
}
