#!/usr/bin/env node
// extract_218757.mjs — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// CLI extraction + identity print (contract §2 pins; the index and the exact
// payload hash are extraction authority; ordinal/offset/size are
// CROSS-CHECKS). Prints a bounded JSON verdict; exit 1 on any mismatch.
//
// Usage: node tools/pecompat/extract_218757.mjs [--models <Models.bnt path>]
import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { PecAssetAdapter, MODEL_218757_PINS } from '../../src/pecompat/PecAssetAdapter.js';

const args = process.argv.slice(2);
let modelsPath;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--models') modelsPath = args[++i];
}

const io = {
  readFile: async (p) => new Uint8Array(await readFile(p)),
  sha256: (b) => createHash('sha256').update(b).digest('hex'),
};

try {
  const adapter = new PecAssetAdapter(io, modelsPath ? { modelsBntPath: modelsPath } : {});
  const t0 = Date.now();
  const ex = await adapter.extractPinnedPayload(MODEL_218757_PINS.modelId);
  const elapsedMs = Date.now() - t0;
  const out = {
    run: 'PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009',
    tool: 'tools/pecompat/extract_218757.mjs',
    container: {
      path: adapter.modelsBntPath,
      sha256: ex.containerSha256,
      pinnedSha256: MODEL_218757_PINS.modelsBntSha256,
      match: ex.containerSha256 === MODEL_218757_PINS.modelsBntSha256,
    },
    entry: {
      name: ex.entryName,
      ordinal: ex.entry.entryIndex,
      offset: ex.entry.offset,
      size: ex.entry.size,
      crc32: ex.entry.crc32,
    },
    payload: {
      size: ex.payload.byteLength,
      sha256: ex.payloadSha256,
      pinnedSha256: MODEL_218757_PINS.payloadSha256,
      match: ex.payloadSha256 === MODEL_218757_PINS.payloadSha256,
    },
    crossChecks: ex.crossChecks,
    verdict: 'EXTRACTION_IDENTITY_VERIFIED',
    elapsedMs,
  };
  const allMatch = out.container.match && out.payload.match &&
    Object.values(ex.crossChecks).every((c) => c.match);
  if (!allMatch) {
    out.verdict = 'EXTRACTION_IDENTITY_MISMATCH';
    console.log(JSON.stringify(out, null, 2));
    process.exit(1);
  }
  console.log(JSON.stringify(out, null, 2));
} catch (e) {
  console.log(JSON.stringify({
    run: 'PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009',
    tool: 'tools/pecompat/extract_218757.mjs',
    verdict: 'EXTRACTION_FAILED_FAIL_CLOSED',
    error: String(e && e.message ? e.message : e),
  }, null, 2));
  process.exit(1);
}
