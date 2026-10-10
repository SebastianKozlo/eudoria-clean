// PecInstanceBuilder.js — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// The authored INSTANCE layer (contract §6): resource identity is separate
// from runtime instance identity. One shared ASSET (the SceneIR from
// PecAssetAdapter) backs N authored instances:
//   - unique authored instanceId (duplicates REJECTED loud);
//   - resource geometry SHARED between instances (the same geometry arrays /
//     THREE.BufferGeometry objects — the NiGeometry shared-model-data basis);
//   - object transforms and instance IDs INDEPENDENT (changing one instance's
//     authored transform must not move another);
//   - the instance WRAPPER owns its scene transform while the imported asset
//     hierarchy retains its serialized root/child transforms.
//
// VIEWER POLICY LABEL (must stay visible to consumers): this wrapper policy is
// NOT a reproduction of every SDK 2.6 root-replacement branch
// (NiSceneGraphComponent::Update applies the entity TRS to the RETRIEVED
// root's LOCAL transform) nor of the original PE placement mechanism. It is
// the authored viewer's documented choice.
//
// SETAT/REPARENT SEMANTICS (GB source contract, re-implemented): changing an
// instance's scene parent (or authored TRS) performs NO compensation — the
// local/authored values stay, the world position changes by composition at
// the next evaluation (NiNode SetAt/AttachChild: parent rebind only).
//
// ATTACHMENT SEPARATION: attachment/source-transform dependencies are kept
// SEPARATE from scene-parent links, so no transform is applied twice. Full
// attachment/animation/LOD execution is OUTSIDE this slice — requesting
// attachment resolution surfaces an explicit UNSUPPORTED diagnostic.

import { composeTrs, identityTrs, cloneTrs, trsDeepEqual } from './PecTransform.js';

export const PEC_INSTANCE_BUILDER_VERSION = 'pec-instance-builder-v1';

export const VIEWER_INSTANCE_WRAPPER_POLICY =
  'AUTHORED_VIEWER_INSTANCE_WRAPPER: the instance wrapper owns its scene transform; ' +
  'the imported asset hierarchy retains its serialized root/child transforms. NOT a ' +
  'reproduction of every SDK 2.6 NiSceneGraphComponent root-replacement branch or the ' +
  'original PE placement mechanism (HISTORICAL_WORLD_INSTANCE = NOT_ESTABLISHED).';

const INSTANCE_ERR = (msg) => new Error(`[PecInstanceBuilder] ${msg}`);

export class PecInstanceRegistry {
  /**
   * @param {object} asset — the SHARED asset record: { ir, worldTransforms } as
   *        returned by PecAssetAdapter.loadModel(). The IR is never mutated by
   *        the instance layer (asserted in tests via trsDeepEqual).
   */
  constructor(asset) {
    if (!asset?.ir) throw INSTANCE_ERR('asset record { ir, worldTransforms } required');
    this.asset = asset;
    this.instances = new Map(); // instanceId -> record
    this.diagnostics = [];
    this._seq = 0;
  }

  /**
   * createInstance — author a new runtime instance of the shared asset.
   * @param {object} spec — { instanceId?, authoredTrs?, sceneParentId?,
   *                          attachment?: { sourceInstanceId, attachmentPointName } }
   * @returns the instance record (see below)
   */
  createInstance(spec = {}) {
    const instanceId = spec.instanceId ?? `inst-${String(++this._seq).padStart(3, '0')}`;
    if (this.instances.has(instanceId)) {
      throw INSTANCE_ERR(`duplicate instanceId "${instanceId}" — REJECTED (instance identity must stay unique)`);
    }
    const sceneParentId = spec.sceneParentId ?? null;
    if (sceneParentId != null && !this.instances.has(sceneParentId)) {
      throw INSTANCE_ERR(`sceneParentId "${sceneParentId}" does not exist (DANGLING_SCENE_PARENT — REJECTED; no silent identity transform)`);
    }
    const authoredTrs = spec.authoredTrs ? cloneTrs(spec.authoredTrs) : identityTrs();
    const rec = {
      instanceId,
      assetCacheKey: this.asset.ir.cacheKey,
      authoredTrs,           // the wrapper's OWN scene transform (serialized TRS copy, owned here)
      sceneParentId,         // scene-parent link (an instanceId or null = scene root)
      children: [],          // instance-level children (authored scene graph)
      attachment: spec.attachment
        ? {
          kind: 'ATTACHMENT',
          sourceInstanceId: spec.attachment.sourceInstanceId ?? null,
          attachmentPointName: spec.attachment.attachmentPointName ?? null,
          dependencyClass: 'ATTACHMENT_SOURCE_TRANSFORM_DEPENDENCY (SEPARATE from scene-parent links; not auto-applied)',
        }
        : null,
      createdAt: this._seq,
    };
    if (rec.attachment) {
      if (!this.instances.has(rec.attachment.sourceInstanceId) && rec.attachment.sourceInstanceId != null) {
        throw INSTANCE_ERR(`attachment source "${rec.attachment.sourceInstanceId}" does not exist (MISSING_MASTER — REJECTED)`);
      }
      // Attachment is RECORDED but its transform resolution is NOT executed
      // (out of slice). If the same instance also carries a scene parent, the
      // two dependency classes are both reported — never silently preferred.
      this.diagnostics.push({
        class: 'ATTACHMENT_RECORDED_NOT_RESOLVED',
        instanceId,
        sourceInstanceId: rec.attachment.sourceInstanceId,
        attachmentPointName: rec.attachment.attachmentPointName,
        note: 'full attachment/animation execution outside this slice; the attachment dependency is NOT applied to any transform',
      });
      if (sceneParentId != null) {
        this.diagnostics.push({
          class: 'ATTACHMENT_AND_SCENE_PARENT_BOTH_PRESENT',
          instanceId,
          sceneParentId,
          note: 'both dependency classes recorded; NO silent preference, NO double application',
        });
      }
    }
    this.instances.set(instanceId, rec);
    if (sceneParentId != null) {
      const parent = this.instances.get(sceneParentId);
      // multi-parent guard: a child lists its parents explicitly
      rec.parents = sceneParentId != null ? [sceneParentId] : [];
      parent.children.push(instanceId);
    } else {
      rec.parents = [];
    }
    return rec;
  }

  /** attachChild — add a scene-parent link (SetAt semantics: NO local
   * compensation; multi-parent attempts are REJECTED with a report — never
   * silently last-link-wins). */
  attachChild(childId, parentId) {
    const child = this.instances.get(childId);
    if (!child) throw INSTANCE_ERR(`instance "${childId}" not found`);
    if (parentId != null && !this.instances.has(parentId)) {
      throw INSTANCE_ERR(`parent "${parentId}" does not exist (DANGLING_SCENE_PARENT — REJECTED)`);
    }
    if (child.parents.includes(parentId ?? null)) {
      throw INSTANCE_ERR(`instance "${childId}" already parented under "${parentId}" — MULTI_PARENT_REJECTED (reported, not silently re-linked)`);
    }
    if (child.parents.length > 0 && (parentId != null || child.parents[0] != null)) {
      const report = { instanceId: childId, parents: [...child.parents, parentId] };
      throw INSTANCE_ERR(`MULTI_PARENT: instance "${childId}" would have parents ${JSON.stringify(report.parents)} — REJECTED with report (no arbitrary selection)`);
    }
    child.parents.push(parentId);
    child.sceneParentId = parentId;
    if (parentId != null) this.instances.get(parentId).children.push(childId);
    return child;
  }

  /** setInstanceTransform — lazy LOCAL setter semantics: writes ONLY the
   * authored TRS (the world is derived at evaluation; no compensation). */
  setInstanceTransform(instanceId, trs) {
    const rec = this.instances.get(instanceId);
    if (!rec) throw INSTANCE_ERR(`instance "${instanceId}" not found`);
    rec.authoredTrs = cloneTrs(trs);
    return rec;
  }

  /** Scene-parent chain validation: cycles REJECTED loud. */
  validate() {
    const errors = [];
    // cycle detection over sceneParentId links
    const color = new Map();
    const visit = (id, path) => {
      color.set(id, 1);
      path.push(id);
      const rec = this.instances.get(id);
      const p = rec?.sceneParentId;
      if (p != null) {
        if (color.get(p) === 1) {
          errors.push({ class: 'INSTANCE_SCENE_CYCLE', path: [...path, p] });
        } else if (!color.has(p)) {
          visit(p, path);
        }
      }
      path.pop();
      color.set(id, 2);
    };
    for (const id of this.instances.keys()) {
      if (!color.has(id)) visit(id, []);
    }
    return { ok: errors.length === 0, errors, diagnostics: this.diagnostics };
  }

  /**
   * instanceSceneTransform — the instance's OWN authored scene transform
   * composed with its scene-parent chain (authored transforms only; the
   * ASSET's serialized hierarchy is composed on top by sceneWorldOfNode).
   * Cycles are REJECTED before composing.
   */
  instanceSceneTransform(instanceId) {
    const v = this.validate();
    if (!v.ok) {
      throw INSTANCE_ERR('scene cycle present — refusing to compose: ' + JSON.stringify(v.errors));
    }
    return this._sceneTransform(instanceId, new Set());
  }

  _sceneTransform(instanceId, visiting) {
    if (visiting.has(instanceId)) throw INSTANCE_ERR('internal: cycle in scene chain (should have been rejected)');
    visiting.add(instanceId);
    const rec = this.instances.get(instanceId);
    const parentT = rec.sceneParentId != null
      ? this._sceneTransform(rec.sceneParentId, visiting)
      : identityTrs();
    visiting.delete(instanceId);
    return composeTrs(parentT, rec.authoredTrs);
  }

  /**
   * sceneWorldOfNode — the COMPOSED world transform of an asset node inside
   * one instance (FILE_SCENE_SPACE of the asset composed under the instance's
   * authored scene transform). DISTINCT quantities:
   *   node worldInAsset (serialized hierarchy) — from asset.worldTransforms;
   *   instance scene transform — this.instanceSceneTransform(instanceId);
   *   node world in scene = sceneTransform * worldInAsset.
   * @param {string} instanceId
   * @param {number} blockIndex asset block index
   */
  sceneWorldOfNode(instanceId, blockIndex) {
    const nodeWorldInAsset = this.asset.worldTransforms.get(blockIndex);
    if (!nodeWorldInAsset) {
      throw INSTANCE_ERR(`asset block ${blockIndex} has no world transform (not a scene member?)`);
    }
    return composeTrs(this._sceneTransform(instanceId, new Set()), nodeWorldInAsset);
  }

  /** assetUnchanged — proof helper: the shared asset IR is never mutated by
   * the instance layer (tested). */
  assetUnchanged(snapshotFn) {
    return snapshotFn();
  }
}
