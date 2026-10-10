#!/usr/bin/env node
// sceneir_dump.mjs — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// CLI SceneIR build + bounded diagnostics dump (counts, block coverage,
// recomputed fingerprints) — NO payloads (no vertex/index arrays, no raw
// ext bodies larger than bounded hex windows). Optionally emits the bounded
// FILE_SCENE_SPACE transform artifact for the app phase (transforms + names
// only, never raw arrays).
//
// Usage:
//   node tools/pecompat/sceneir_dump.mjs [--models <Models.bnt>]
//        [--emit-file-scene-space <out.json>] [--json <out.json>]
import { readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { PecAssetAdapter, MODEL_218757_PINS } from '../../src/pecompat/PecAssetAdapter.js';
import { fileSceneSpaceArtifact } from '../../src/pecompat/PecSceneIR.js';

const args = process.argv.slice(2);
let modelsPath, emitFileSceneSpace, jsonOut;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--models') modelsPath = args[++i];
  else if (args[i] === '--emit-file-scene-space') emitFileSceneSpace = args[++i];
  else if (args[i] === '--json') jsonOut = args[++i];
}

const io = {
  readFile: async (p) => new Uint8Array(await readFile(p)),
  sha256: (b) => createHash('sha256').update(b).digest('hex'),
};

try {
  const adapter = new PecAssetAdapter(io, modelsPath ? { modelsBntPath: modelsPath } : {});
  const m = await adapter.loadModel(MODEL_218757_PINS.modelId);
  const ir = m.ir;

  const dump = {
    run: 'PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009',
    tool: 'tools/pecompat/sceneir_dump.mjs',
    provenance: m.provenance,
    asset: {
      assetId: ir.asset.assetId,
      era: ir.asset.era,
      nifVersion: ir.asset.nifVersion,
      numBlocks: ir.asset.numBlocks,
      closure: {
        eofExact: ir.asset.closure.eofExact,
        numBlocksDecoded: ir.asset.closure.numBlocksDecoded,
        topObjects: ir.asset.closure.topObjects,
        decisions: ir.asset.closure.decisions,
      },
    },
    blockTypeCensus: ir.blockTypeCensus,
    decodeCensus: ir.decodeCensus,
    decodeAccounting: {
      total: ir.blocks.length,
      supported: ir.decodeCensus.SUPPORTED,
      arkBlocks: ir.decodeCensus.PARTIALLY_UNDERSTOOD + ir.decodeCensus.OPAQUE,
      note: '62 supported + 4 Ark blocks (2 PARTIALLY_UNDERSTOOD + 2 OPAQUE per actual field coverage) — the 62+4=66 ceiling preserved; no silent Ark semantic decodes',
    },
    roots: ir.roots,
    blocks: ir.blocks.map((b) => ({
      index: b.index,
      type: b.type,
      name: b.name,
      decodeStatus: b.decodeStatus,
      byteRange: [b.byteStart, b.byteEnd],
      children: b.children ?? null,
      propertyRefs: b.propertyRefs ?? null,
      extraDataRefs: b.extraDataRefs ?? null,
      dataRef: b.dataRef ?? null,
      opaqueBoundary: b.opaque
        ? { extStart: b.opaque.extStart, extEnd: b.opaque.extEnd, extLength: b.opaque.extLength, boundaryMethod: b.opaque.boundaryMethod }
        : null,
    })),
    meshAssociations: ir.meshAssociations.map((x) => ({
      meshBlock: x.meshBlock,
      meshName: x.meshName,
      dataBlock: x.dataBlock,
      numVertices: x.numVertices,
      numTriangles: x.numTriangles,
      vertexPositionsF32leSha256: x.vertexPositionsF32leSha256,
      triangleIndicesU16leSha256: x.triangleIndicesU16leSha256,
    })),
    textureBindings: ir.diagnostics.textureBindings.map((t) => ({
      meshBlock: t.meshBlock,
      meshName: t.meshName,
      status: t.status,
      texturePropertyRefs: t.texturePropertyRefs,
      textureNames: t.textureNames,
      containerResolution: t.containerResolution,
    })),
    sceneBounds_FILE_SCENE_SPACE: m.sceneBounds,
    validation: {
      ok: m.validation.ok,
      errorCount: m.validation.errors.length,
      warnings: m.validation.warnings,
    },
    diagnosticsNotes: ir.diagnostics.notes,
  };

  if (emitFileSceneSpace) {
    const artifact = fileSceneSpaceArtifact(ir, m.worldTransforms);
    await writeFile(emitFileSceneSpace, JSON.stringify(artifact, null, 1) + '\n', 'utf8');
    dump.emittedFileSceneSpaceArtifact = emitFileSceneSpace;
  }
  const text = JSON.stringify(dump, null, 1) + '\n';
  if (jsonOut) {
    await writeFile(jsonOut, text, 'utf8');
    console.log(`sceneir_dump: wrote ${jsonOut} (${text.length} B)`);
  } else {
    console.log(text);
  }
} catch (e) {
  console.log(JSON.stringify({
    run: 'PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009',
    tool: 'tools/pecompat/sceneir_dump.mjs',
    verdict: 'DUMP_FAILED_FAIL_CLOSED',
    error: String(e && e.message ? e.message : e),
  }, null, 2));
  process.exit(1);
}
