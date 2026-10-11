// census_extra.test.mjs — the defined-but-not-yet-tested census categories from
// fresh internal QC finding F10: ENTRY_TOO_LARGE, INPUT_TOO_LARGE, UNSUPPORTED
// (container-level framing failure), PAYLOAD_SIZE_MISMATCH (plus reservation refund).
import test from 'node:test';
import assert from 'node:assert/strict';
import os from 'node:os';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import * as FX from './fixtures.mjs';

const TOOL = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'placement_probe.mjs');
function mkRepo(root, bntSrc = FX.shimBntSrc) { const repo = path.join(root, 'repo'); fs.mkdirSync(path.join(repo, 'src/pesource'), { recursive: true }); fs.writeFileSync(path.join(repo, 'package.json'), '{"type":"module"}'); fs.writeFileSync(path.join(repo, 'src/pesource/Bnt2Archive.js'), bntSrc); fs.writeFileSync(path.join(repo, 'src/pesource/ArkArchive.js'), FX.shimArkSrc); fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058] })); return repo; }
function cli(root, repo, inputs, args) {
  const out = path.join(root, 'out');
  const res = spawnSync(process.execPath, [TOOL, '--repo', repo, '--ids', path.join(root, 'ids.json'), '--out', out, ...inputs.flatMap(n => ['--input', path.join(root, n)]), ...args], { encoding: 'utf8' });
  let summary = null; try { summary = JSON.parse(fs.readFileSync(path.join(out, 'SUMMARY.json'), 'utf8')); } catch {}
  return { exitCode: res.status, stderr: res.stderr, summary };
}
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'pe-t-cx-'));
const small16 = () => { const b = Buffer.alloc(16 + 8 * 16, 0xff); for (let i = 0; i < 8; i++) { const x = 16 + i * 16; b.writeUInt16LE(i % 2 === 0 ? 4057 : 4058, x); b.writeFloatLE(i * 11.5 + 2, x + 4); b.writeFloatLE(1000 + i * 2.1, x + 8); b.writeFloatLE(i * 4.5 - 80, x + 12); } return b; };

test('CX1: ENTRY_TOO_LARGE disposition with lowered per-entry cap (legal boundary: small entry still scanned)', () => {
  const root = tmp(); try {
    const repo = mkRepo(root);
    fs.writeFileSync(path.join(root, 'c.bnt'), FX.realBnt2([{ name: 'small.rec', data: small16() }, { name: 'big.rec', data: FX.records80() }]));
    const r = cli(root, repo, ['c.bnt'], ['--max-payload-mib', '0.001']); // 1048.576B cap
    assert.equal(r.exitCode, 0, r.stderr);
    const c = r.summary.exclusionCensus[0];
    assert.equal(c.dispositionCounts.SCANNED, 1, 'the 144B entry fits the cap');
    assert.equal(c.dispositionCounts.ENTRY_TOO_LARGE, 1, 'the 2576B entry exceeds the cap');
    assert.equal(c.dispositionTotal, 2); assert.equal(c.censusOk, true);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('CX2: INPUT_TOO_LARGE container-level refusal (declared unit accounted, no invented entries)', () => {
  const root = tmp(); try {
    const repo = mkRepo(root);
    fs.writeFileSync(path.join(root, 'a.vfs'), FX.records80()); // 2576 B
    const r = cli(root, repo, ['a.vfs'], ['--max-input-mib', '0.001']); // 1048.576B cap
    assert.equal(r.summary.exclusionCensus[0].parseStatus, 'INPUT_TOO_LARGE');
    assert.equal(r.summary.exclusionCensus[0].declaredEntryCount, null, 'no payload read, no invented entry count');
    assert.equal(r.summary.candidateCount, 0);
    assert.equal(r.summary.budgets.used.scannedBytes, 0, 'refused before the read: no bytes charged');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('CX3: UNSUPPORTED container-level framing failure (bad BNT2 footer) is not a fabricated entry census', () => {
  const root = tmp(); try {
    const repo = mkRepo(root);
    const bogus = Buffer.alloc(64, 0x41); bogus.write('XXXX', 60, 'ascii');
    fs.writeFileSync(path.join(root, 'bad.bnt'), bogus);
    const r = cli(root, repo, ['bad.bnt'], []);
    assert.equal(r.exitCode, 2, 'CONTAINER_PARSE_FAILED is in the nonzero-exit set');
    const c = r.summary.exclusionCensus[0];
    assert.equal(c.parseStatus, 'UNSUPPORTED');
    assert.equal(c.declaredEntryCount, null, 'entry count unknown — never invented');
    assert.equal(c.dispositionTotal, 0);
    const skips = fs.readFileSync(path.join(root, 'out', 'scan_skips.csv'), 'utf8');
    assert.ok(skips.includes('CONTAINER_PARSE_FAILED'));
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('CX4: PAYLOAD_SIZE_MISMATCH is PARSE_FAILED with the reservation refunded', () => {
  const root = tmp(); try {
    // truncated-payload shim: directory declares N bytes, readEntry returns N-4
    const truncShim = FX.shimBntSrc.replace('readEntry(e){return {payload:this.b.subarray(e.offset,e.offset+e.size)}}', 'readEntry(e){return {payload:this.b.subarray(e.offset,Math.max(0,e.offset+e.size-4))}}');
    assert.notEqual(truncShim, FX.shimBntSrc, 'shim must actually be truncated');
    const repo = mkRepo(root, truncShim);
    fs.writeFileSync(path.join(root, 'c.bnt'), FX.realBnt2([{ name: 'x.rec', data: FX.recordsTwoIdSmall() }]));
    const r = cli(root, repo, ['c.bnt'], []);
    const c = r.summary.exclusionCensus[0];
    assert.equal(c.dispositionCounts.PARSE_FAILED, 1, 'declared 272B vs actual 268B is a parse failure, not a scan');
    assert.equal(c.censusOk, true);
    assert.equal(r.summary.budgets.used.scannedBytes, 0, 'the reservation was refunded — the payload was never scanned');
    assert.equal(r.summary.budgets.used.syntheticInputs, 0);
    assert.equal(r.summary.candidateCount, 0);
    const skips = fs.readFileSync(path.join(root, 'out', 'scan_skips.csv'), 'utf8');
    assert.ok(skips.includes('PAYLOAD_SIZE_MISMATCH'));
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});