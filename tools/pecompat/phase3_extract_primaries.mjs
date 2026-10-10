// phase3_extract_primaries.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 3 (W3, contract §3)
// Bounded extraction of the FOUR primary CD_2003 models from Models.ark into
// PRIVATE_OUTPUT, with fail-closed identity verification.
//
// REUSE LABEL: the sequential local-header index + EOCD cross-check come from
// src/pesource/ArkArchive.js — the base repo's era-validated ArkVFS reader
// (imported and used unchanged, as in phase 2's ark_index.mjs).
//
// IDENTITY POLICY (contract §1/§2): each payload is verified against the
// pinned SHA256 + size from the phase-2 catalog AND the dispatch list. Any
// mismatch BLOCKS work on that entry (fail-closed, era-labelled).
//
// OUTPUT: PRIVATE_OUTPUT/PHASE3_MODELS/<name> only (never the repo). The four
// payload SHA256s are re-hashed at write time and printed in the summary.

import fs from 'node:fs';
import crypto from 'node:crypto';
import { ArkArchive } from '../../src/pesource/ArkArchive.js';

const PINNED = {
  '192374.nif': { entryIndex: 888, sizeBytes: 66759, sha256: '08d80c67bb87caf6a1c00bf8c034e329484e25a6a588da411079bb6f682de8c1' },
  '193207.nif': { entryIndex: 908, sizeBytes: 47167, sha256: '220f549b311563a1a6506cacefcebb8911ee4770cf72b85f2f635146c111adbb' },
  '193313.nif': { entryIndex: 910, sizeBytes: 66726, sha256: '02fc860a840e9cdb948f04daff2691bb37baf9e0da8dbadc8f77773c517beef2' },
  '193684.nif': { entryIndex: 913, sizeBytes: 75805, sha256: '4cc5f9203280c26fc2020bb6c432e2bcf4e5db4ec2f47be3df573e537660901f' },
};

const CONTAINER = {
  path: 'D:\\Eudoria_Reconstruction\\pcg2003_install\\Data\\Models\\Models.ark',
  sha256: 'f660d055b4b9471b3b6e16b07f5368dbd6f2208dab6b51bb9bdb9942bd73ea62',
  sizeBytes: 128742137,
};

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) args[key] = true;
      else { args[key] = next; i++; }
    }
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv);
  const outDir = args['out-dir'];
  const arkPath = args.ark ?? CONTAINER.path;
  if (!outDir) throw new Error('--out-dir <dir> required');
  fs.mkdirSync(outDir, { recursive: true });

  const buf = fs.readFileSync(arkPath);
  const bytes = new Uint8Array(buf);
  const containerSha = crypto.createHash('sha256').update(bytes).digest('hex');
  if (containerSha !== CONTAINER.sha256) {
    throw new Error(`[phase3_extract] container SHA256 ${containerSha} != pinned ${CONTAINER.sha256} — BLOCKED`);
  }
  if (bytes.length !== CONTAINER.sizeBytes) {
    throw new Error(`[phase3_extract] container size ${bytes.length} != pinned ${CONTAINER.sizeBytes} — BLOCKED`);
  }

  const arch = new ArkArchive(bytes);
  const entries = arch.entries();
  const byName = new Map(entries.map((e) => [e.name, e]));

  const records = [];
  for (const [name, pin] of Object.entries(PINNED)) {
    const e = byName.get(name);
    if (!e) throw new Error(`[phase3_extract] entry ${name} NOT FOUND in Models.ark — BLOCKED`);
    if (e.entryIndex !== pin.entryIndex) {
      throw new Error(`[phase3_extract] entry ${name}: index ${e.entryIndex} != pinned ${pin.entryIndex} — BLOCKED`);
    }
    const { payload } = arch.readEntry(e);
    if (payload.length !== pin.sizeBytes) {
      throw new Error(`[phase3_extract] entry ${name}: size ${payload.length} != pinned ${pin.sizeBytes} — BLOCKED`);
    }
    const sha = crypto.createHash('sha256').update(payload).digest('hex');
    if (sha !== pin.sha256) {
      throw new Error(`[phase3_extract] entry ${name}: SHA256 ${sha} != pinned ${pin.sha256} — BLOCKED`);
    }
    const outPath = `${outDir}\\${name}`;
    fs.writeFileSync(outPath, payload);
    records.push({
      era: 'CD_2003', name, entryIndex: e.entryIndex,
      sizeBytes: payload.length, payloadSha256: sha,
      pinnedSha256Match: true, writtenPath: outPath,
    });
  }

  const summary = {
    artifact: 'PHASE3_PRIMARY_EXTRACTION',
    runId: 'PE_CITY_ASSET_MAP_R1_20261010',
    phase: 'FOUR_MODELS_DEEP_ANALYSIS (phase 3)',
    era: 'CD_2003',
    container: { path: arkPath, sizeBytes: bytes.length, sha256: containerSha, pin: 'MATCH' },
    entries: records,
    elapsedMs: 0,
  };
  summary.elapsedMs = 0;
  process.stdout.write(JSON.stringify(summary, null, 1) + '\n');
}

main().catch((err) => {
  console.error('[phase3_extract] FATAL:', err?.stack ?? err);
  process.exitCode = 1;
});
