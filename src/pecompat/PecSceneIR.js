// PecSceneIR.js — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// The SceneIR: resource identity kept separate from runtime instance identity
// (contract §6). Schema records:
//   ASSET   — era/build, container/entry/hash, serialized block IDs, supported
//             types, source links, decode status per block;
//   NODE    — serialized local TRS, children, and SEPARATE resource (model
//             data), property and extra-data links;
//   INSTANCE— unique authored instance ID, asset reference, authored
//             transform, scene parent (see PecInstanceBuilder.js);
//   DIAGNOSTICS — opaque block count, unresolved bindings/dependencies,
//             unsupported features;
//   COMPUTED STATE — model/file-root transform, authored scene transform,
//             render transform and bounds as DISTINCT quantities. This module
//             computes the FILE_SCENE_SPACE world transform of every node
//             (model/file-root space). The authored scene transform belongs to
//             the instance layer; the render transform to PecRenderConvert.js.
//
// Coordinate discipline: every transform here is FILE_SCENE_SPACE — composed
// from serialized local TRS through parentWorld*local (PecTransform.composeTrs)
// to the proven file root. NO axis swap, unit conversion or x100 is imported.
// Any render-axis/unit conversion happens in PecRenderConvert.js EXACTLY ONCE
// and is labeled RENDER_ADAPTER_CHOICE / PE_UNITS_NOT_CONFIRMED.
//
// VALIDATION POLICY (contract §6):
//   - cycles in the scene-child graph: REJECTED (loud);
//   - dangling REQUIRED child links (children[], model-data refs): REJECTED;
//   - multiple parents: REPORTED with the full claim list — never silently
//     resolved (the native loader's last-AttachChild-wins behavior is a NATIVE
//     trait measured on synthetic controls, NOT reproduced silently here);
//   - property/extra-data links are NOT required-child links: dangling ones are
//     diagnostics (unresolved binding), not parse rejections.

import {
  composeTrs, identityTrs, cloneTrs, applyTrsPoint,
} from './PecTransform.js';

export const PEC_SCENEIR_SCHEMA_VERSION = 'pec-sceneir-v1';

/** Cache key = asset hash + adapter/schema version (contract §7). */
export function sceneCacheKey({ assetId, payloadSha256, adapterVersion }) {
  return `${assetId}:${payloadSha256.toLowerCase()}:${adapterVersion}:${PEC_SCENEIR_SCHEMA_VERSION}`;
}

// ---- decode statuses (per actual field coverage; 62+4=66 accounting for 218757) ----
export const DECODE_STATUS = {
  SUPPORTED: 'SUPPORTED',                 // full documented field coverage
  PARTIALLY_UNDERSTOOD: 'PARTIALLY_UNDERSTOOD', // some documented fields; rest raw (e.g. NiArkTextureExtraData entries; NiCamera TRS)
  OPAQUE: 'OPAQUE',                       // boundary + raw bytes only (e.g. NiArkAnimation/ViewportInfo ext)
};

const AV_OBJECT_TYPES = new Set(['NiNode', 'NiTriShape', 'NiCamera', 'NiDirectionalLight']);
export function isAVObjectType(type) { return AV_OBJECT_TYPES.has(type); }

/**
 * buildAssetIR — construct the ASSET record from a reader result.
 * @param {object} r — readNif10() output: { header, blocks, footer, closure, sourceName }
 * @param {object} meta — { assetId, era, build, container, entryName, payloadSha256,
 *                           sizeBytes, adapterVersion, physicalSource, extraProvenance? }
 */
export function buildAssetIR(r, meta) {
  const blocks = [];
  const meshAssociations = [];
  const typeCensus = new Map();
  for (const b of r.blocks) {
    typeCensus.set(b.type, (typeCensus.get(b.type) ?? 0) + 1);
    const rec = {
      index: b.index,
      type: b.type,
      decodeStatus: b.decodeStatus,
      name: b.name ?? null,
      byteStart: b.preambleOffset,
      payloadStart: b.payloadStart,
      byteEnd: b.blockEnd,
      // serialized local TRS — FILE_SCENE_SPACE local, kept bit-identical to the
      // decoded file values; never mutated by instance or render layers.
      localTrs: b.localTrs ?? null,
      localTrsBits: b.localTrsBits ?? null,
      // link classes kept SEPARATE (contract §6):
      children: b.children ?? null,        // scene-parent links (required)
      effects: b.effects ?? null,          // dynamic-effect links (not scene parents)
      dataRef: b.dataRef ?? null,          // RESOURCE link (shared NiGeometryData)
      skinRef: b.skinRef ?? null,
      propertyRefs: b.propertyRefs ?? null,// property links
      extraDataRefs: b.extraDataRefs ?? null, // extra-data links
      controllerRef: b.controllerRef ?? null,
      geometry: b.geometry ?? null,        // decoded arrays + byte ranges (NiTriShapeData)
      fields: b.fields ?? null,            // semantic fields (properties/extradata)
      opaque: b.opaque ?? null,            // raw ext/tail + boundary method (Ark/camera)
    };
    blocks.push(rec);
  }
  const byIndex = new Map(blocks.map((b) => [b.index, b]));
  for (const b of blocks) {
    if (b.type === 'NiTriShape') {
      const data = b.dataRef != null ? byIndex.get(b.dataRef) : null;
      meshAssociations.push({
        meshBlock: b.index,
        meshName: b.name,
        dataBlock: b.dataRef,
        numVertices: data?.geometry?.numVertices ?? null,
        numTriangles: data?.geometry?.numTriangles ?? null,
        vertexPositionsF32leSha256: data?.geometry?.vertexPositionsF32leSha256 ?? null,
        triangleIndicesU16leSha256: data?.geometry?.triangleIndicesU16leSha256 ?? null,
      });
    }
  }
  const decodeCensus = { SUPPORTED: 0, PARTIALLY_UNDERSTOOD: 0, OPAQUE: 0 };
  for (const b of blocks) decodeCensus[b.decodeStatus] = (decodeCensus[b.decodeStatus] ?? 0) + 1;

  const ir = {
    schemaVersion: PEC_SCENEIR_SCHEMA_VERSION,
    adapterVersion: meta.adapterVersion,
    cacheKey: sceneCacheKey({
      assetId: meta.assetId, payloadSha256: meta.payloadSha256, adapterVersion: meta.adapterVersion,
    }),
    asset: {
      assetId: meta.assetId,
      era: meta.era,
      build: meta.build,
      container: meta.container,
      entryName: meta.entryName,
      payloadSha256: meta.payloadSha256.toLowerCase(),
      sizeBytes: meta.sizeBytes,
      physicalSource: meta.physicalSource ?? null,
      nifVersion: r.header.versionString,
      nifVersionRaw: r.header.versionRaw,
      headerText: r.header.text,
      numBlocks: r.header.numBlocks,
      blockTypes: r.header.blockTypes,
      blockTypeIndex: r.header.blockTypeIndex,
      closure: {
        eofExact: r.closure.eofExact,
        numBlocksDecoded: r.closure.numBlocksDecoded,
        topObjects: r.footer?.topObjects ?? null,
        decisions: r.closure.decisions ?? [],
      },
    },
    blocks,
    blockTypeCensus: Object.fromEntries([...typeCensus.entries()].sort((a, b) => b[1] - a[1])),
    decodeCensus,
    meshAssociations,
    roots: [], // filled by computeRoots
    diagnostics: {
      opaqueBlockCount: decodeCensus.OPAQUE + decodeCensus.PARTIALLY_UNDERSTOOD,
      supportedBlockCount: decodeCensus.SUPPORTED,
      unresolvedBindings: [],
      unsupportedFeatures: [],
      notes: [],
    },
    computed: null, // filled on demand: { worldTransforms, bounds } (FILE_SCENE_SPACE)
  };
  ir.roots = computeRoots(ir, r.footer?.topObjects);
  return ir;
}

/** Scene-graph root determination. The TopObjects footer is the AUTHORITY for
 * the file's top-level roots; unclaimed scene blocks (AV-object types not
 * referenced as any node's child) are the fallback for synthetic graphs and a
 * cross-check for parsed files. Property/extra-data/geometry-data blocks are
 * REFERENCED RESOURCES — never roots. */
export function computeRoots(ir, footerTopObjects) {
  const avSceneTypes = new Set(['NiNode', 'NiTriShape', 'NiCamera', 'NiDirectionalLight']);
  const claimed = new Set();
  for (const b of ir.blocks) {
    for (const c of b.children ?? []) {
      if (c != null && c >= 0) claimed.add(c);
    }
  }
  const unclaimedScene = ir.blocks
    .filter((b) => avSceneTypes.has(b.type) && !claimed.has(b.index))
    .map((b) => b.index);
  const valid = (idx) => ir.blocks.some((b) => b.index === idx);
  if (footerTopObjects && footerTopObjects.length > 0) {
    for (const t of footerTopObjects) {
      if (!valid(t)) {
        throw new Error(`[PecSceneIR] footer top object ${t} is not a valid block — LOUD FAIL`);
      }
    }
    const match =
      unclaimedScene.length === footerTopObjects.length &&
      unclaimedScene.every((v, i) => v === footerTopObjects[i]);
    ir.diagnostics.notes.push({
      class: 'ROOT_DETERMINATION',
      authority: 'TOP_OBJECTS_FOOTER',
      footerTopObjects: [...footerTopObjects],
      unclaimedSceneBlocks: unclaimedScene,
      agree: match,
    });
    return [...footerTopObjects];
  }
  return unclaimedScene;
}

/**
 * validateSceneGraph — cycles/dangling REQUIRED links REJECTED; multiple
 * parents REPORTED (with the full claim list); dangling property/extra-data
 * links become diagnostics (unresolved bindings).
 * @returns {{ok:boolean, errors:Array, warnings:Array, multiParent:Array, parentOf:Map}}
 */
export function validateSceneGraph(ir) {
  const errors = [];
  const warnings = [];
  const multiParent = [];
  const parentOf = new Map();
  const byIndex = new Map(ir.blocks.map((b) => [b.index, b]));
  const numBlocks = ir.blocks.length;

  // parent claim census (children lists only — effects are NOT scene parents)
  const claims = new Map();
  for (const b of ir.blocks) {
    for (const c of b.children ?? []) {
      if (c == null || c < 0) continue;
      if (!claims.has(c)) claims.set(c, []);
      claims.get(c).push(b.index);
    }
  }
  for (const [child, parents] of claims) {
    if (!byIndex.has(child)) {
      errors.push({ class: 'DANGLING_CHILD_REF', child, parents });
      continue;
    }
    if (parents.length > 1) {
      multiParent.push({ child, parents: [...parents] });
    } else {
      parentOf.set(child, parents[0]);
    }
  }

  // dangling REQUIRED resource link: NiTriShape -> NiTriShapeData
  for (const b of ir.blocks) {
    if (b.type === 'NiTriShape') {
      if (b.dataRef == null || !byIndex.has(b.dataRef)) {
        errors.push({ class: 'DANGLING_MODEL_DATA_REF', meshBlock: b.index, dataRef: b.dataRef });
      } else if (byIndex.get(b.dataRef).type !== 'NiTriShapeData') {
        errors.push({ class: 'MODEL_DATA_REF_TYPE_MISMATCH', meshBlock: b.index, dataRef: b.dataRef, actualType: byIndex.get(b.dataRef).type });
      }
    }
    // non-required links: diagnostics only
    for (const [refs, cls] of [[b.propertyRefs, 'PROPERTY'], [b.extraDataRefs, 'EXTRA_DATA']]) {
      for (const ref of refs ?? []) {
        if (ref == null || ref < 0) continue;
        if (!byIndex.has(ref)) {
          warnings.push({ class: `DANGLING_${cls}_REF`, block: b.index, ref });
        }
      }
    }
    // NULL (-1) child slots are LEGAL NIF null links (measured on 218757: the
    // root NiNode carries 19 of them alongside 12 real children). They are
    // recorded as diagnostics and skipped in claims/composition — NOT errors.
    for (const b of ir.blocks) {
      let nullSlots = 0;
      for (const c of b.children ?? []) {
        if (c == null) continue;
        if (c < 0) { nullSlots++; continue; }
        if (c >= numBlocks) {
          errors.push({ class: 'CHILD_REF_OUT_OF_RANGE', block: b.index, child: c });
        }
      }
      if (nullSlots > 0) {
        warnings.push({
          class: 'NULL_CHILD_SLOTS', block: b.index, count: nullSlots,
          note: 'legal NIF NULL child links (-1); skipped in claims and composition',
        });
      }
    }
  }

  // cycle detection (iterative DFS with colors) over accepted parent edges
  const color = new Map(); // 0 white, 1 gray, 2 black
  const cycleErrors = [];
  const visit = (start) => {
    const stack = [[start, 0]];
    const path = [];
    while (stack.length) {
      const [node, ci] = stack[stack.length - 1];
      const kids = byIndex.get(node)?.children ?? [];
      if (ci === 0) { color.set(node, 1); path.push(node); }
      if (ci < kids.length) {
        stack[stack.length - 1][1]++;
        const k = kids[ci];
        if (k == null || k < 0) continue;
        if (!byIndex.has(k)) continue; // already reported as dangling
        const kc = color.get(k) ?? 0;
        if (kc === 1) {
          cycleErrors.push({ class: 'SCENE_GRAPH_CYCLE', path: [...path, k] });
        } else if (kc === 0) {
          stack.push([k, 0]);
        }
      } else {
        color.set(node, 2);
        path.pop();
        stack.pop();
      }
    }
  };
  for (const b of ir.blocks) {
    if ((color.get(b.index) ?? 0) === 0) visit(b.index);
  }
  errors.push(...cycleErrors);

  if (ir.roots.length === 0) errors.push({ class: 'NO_ROOT' });
  if (ir.roots.length > 1) warnings.push({ class: 'MULTIPLE_ROOTS', roots: [...ir.roots] });
  if (multiParent.length > 0) {
    // REPORTED, never silently selected (composeWorldTransforms refuses while unresolved)
    errors.push({ class: 'MULTI_PARENT_REPORT', multiParent });
  }
  return { ok: errors.length === 0, errors, warnings, multiParent, parentOf };
}

/**
 * composeWorldTransforms — FILE_SCENE_SPACE world transform per block.
 * world = parentWorld * local; root world == local (GB 1.2 contract).
 * REJECTS cycles/dangling/multi-parent (throws with the validation report —
 * never silently selects a parent).
 * @returns {Map<number, {translate,rotate,scale}>}
 */
export function composeWorldTransforms(ir) {
  const v = validateSceneGraph(ir);
  if (!v.ok) {
    const err = new Error('[PecSceneIR] scene graph invalid — refusing to compose: ' +
      JSON.stringify(v.errors));
    err.validation = v;
    throw err;
  }
  const byIndex = new Map(ir.blocks.map((b) => [b.index, b]));
  const world = new Map();
  const compute = (index, parentWorld) => {
    const b = byIndex.get(index);
    const local = b?.localTrs ?? identityTrs();
    const w = parentWorld ? composeTrs(parentWorld, local) : cloneTrs(local);
    world.set(index, w);
    for (const c of b?.children ?? []) {
      if (c != null && c >= 0) compute(c, w);
    }
  };
  for (const r of ir.roots) compute(r, null);
  // reachability: every scene-graph member must have been composed
  const members = new Set();
  const walk = (i) => {
    if (members.has(i)) return;
    members.add(i);
    for (const c of byIndex.get(i)?.children ?? []) {
      if (c != null && c >= 0 && byIndex.has(c)) walk(c);
    }
  };
  for (const r of ir.roots) walk(r);
  if (world.size !== members.size) {
    throw new Error('[PecSceneIR] composition did not reach every scene-graph member (unreachable blocks present)');
  }
  return world;
}

/** Scene-graph membership: blocks reachable via children links from roots
 * (properties/extradata/geometry-data blocks are NOT scene-graph members). */
export function isSceneGraphMember(ir, index) {
  const members = new Set();
  const byIndex = new Map(ir.blocks.map((b) => [b.index, b]));
  const walk = (i) => {
    if (members.has(i)) return;
    members.add(i);
    for (const c of byIndex.get(i)?.children ?? []) if (c != null && c >= 0 && byIndex.has(c)) walk(c);
  };
  for (const r of ir.roots) walk(r);
  return members.has(index);
}

/**
 * computeSceneBounds — FILE_SCENE_SPACE bbox over all mesh vertices transformed
 * by their composed world transforms (full-matrix point application, never
 * position sums). Returns {min, max, extents, meshCount}.
 */
export function computeSceneBounds(ir, worldTransforms) {
  const min = [Infinity, Infinity, Infinity];
  const max = [-Infinity, -Infinity, -Infinity];
  const byIndex = new Map(ir.blocks.map((b) => [b.index, b]));
  let meshCount = 0;
  for (const b of ir.blocks) {
    if (b.type !== 'NiTriShape') continue;
    // Geometry lives on the referenced NiTriShapeData block (shared resource):
    const data = b.dataRef != null ? byIndex.get(b.dataRef) : null;
    if (!data?.geometry) continue;
    meshCount++;
    const w = worldTransforms.get(b.index);
    const pos = data.geometry.positions;
    for (let i = 0; i < pos.length; i += 3) {
      const p = applyTrsPoint(w, [pos[i], pos[i + 1], pos[i + 2]]);
      for (let k = 0; k < 3; k++) {
        if (p[k] < min[k]) min[k] = p[k];
        if (p[k] > max[k]) max[k] = p[k];
      }
    }
  }
  return {
    min, max,
    extents: [max[0] - min[0], max[1] - min[1], max[2] - min[2]],
    meshCount,
    space: 'FILE_SCENE_SPACE',
  };
}

/**
 * FILE_SCENE_SPACE transform artifact for the app phase — transforms + names
 * ONLY, never raw arrays (bounded, non-payload).
 */
export function fileSceneSpaceArtifact(ir, worldTransforms) {
  return {
    schemaVersion: PEC_SCENEIR_SCHEMA_VERSION,
    assetId: ir.asset.assetId,
    payloadSha256: ir.asset.payloadSha256,
    cacheKey: ir.cacheKey,
    space: 'FILE_SCENE_SPACE',
    composedSemantics: 'world = parentWorld * local from serialized local TRS through complete SCENE_CHILD chains to the proven file root; NOT a PE world position; no axis swap / unit conversion imported',
    blocks: ir.blocks.map((b) => ({
      index: b.index,
      type: b.type,
      name: b.name,
      decodeStatus: b.decodeStatus,
      localTrs: b.localTrs ? { t: b.localTrs.translate, r: b.localTrs.rotate, s: b.localTrs.scale } : null,
      worldTrs: worldTransforms.has(b.index)
        ? { t: worldTransforms.get(b.index).translate, r: worldTransforms.get(b.index).rotate, s: worldTransforms.get(b.index).scale }
        : null,
    })),
  };
}

// ---- synthetic IR builder (authored tests; synthetic, NOT PCG data) ----

/**
 * makeSyntheticIR — build an authored synthetic asset IR for tests.
 * @param {object} spec — { assetId, blocks: [{index, type, name?, localTrs?, children?,
 *   dataRef?, propertyRefs?, geometry?: {positions: Array|Float32Array, indices: Array|Uint16Array}}] }
 * Blocks are trusted as-authored (tests construct valid/invalid graphs
 * deliberately); decodeStatus defaults to SUPPORTED.
 */
export function makeSyntheticIR(spec) {
  const rBlocks = spec.blocks.map((b) => ({
    index: b.index,
    type: b.type,
    decodeStatus: b.decodeStatus ?? DECODE_STATUS.SUPPORTED,
    name: b.name ?? null,
    preambleOffset: -1, payloadStart: -1, blockEnd: -1, // synthetic: no byte ranges
    localTrs: b.localTrs ?? null,
    children: b.children ?? null,
    effects: b.effects ?? null,
    dataRef: b.dataRef ?? null,
    propertyRefs: b.propertyRefs ?? null,
    extraDataRefs: b.extraDataRefs ?? null,
    geometry: b.geometry ? {
      positions: b.geometry.positions instanceof Float32Array ? b.geometry.positions : new Float32Array(b.geometry.positions),
      indices: b.geometry.indices instanceof Uint16Array ? b.geometry.indices : new Uint16Array(b.geometry.indices),
      numVertices: (b.geometry.positions.length) / 3,
      numTriangles: (b.geometry.indices.length) / 3,
      vertexByteRange: null, indexByteRange: null,
    } : null,
    fields: b.fields ?? null,
    opaque: b.opaque ?? null,
  }));
  const r = {
    header: { versionString: '10.1.0.0 (synthetic)', versionRaw: '0x0A010000', text: 'synthetic', numBlocks: rBlocks.length, blockTypes: [...new Set(rBlocks.map((b) => b.type))], blockTypeIndex: [] },
    blocks: rBlocks,
    footer: { topObjects: spec.topObjects ?? [] },
    closure: { eofExact: true, numBlocksDecoded: rBlocks.length, decisions: [] },
    sourceName: spec.assetId,
  };
  return buildAssetIR(r, {
    assetId: spec.assetId,
    era: 'SYNTHETIC',
    build: 'SYNTHETIC_TEST',
    container: 'synthetic',
    entryName: `${spec.assetId}.synthetic.nif`,
    payloadSha256: spec.payloadSha256 ?? '0'.repeat(64),
    sizeBytes: 0,
    adapterVersion: spec.adapterVersion ?? 'pec-nif101-adapter-v1',
    physicalSource: 'AUTHORED_SYNTHETIC (not PCG data; not a historical asset)',
  });
}
