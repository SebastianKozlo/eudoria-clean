// rosettaRegistry.test.mjs — J5 (Wave B3+B4) integration proof for the
// gamebryoReference knowledge namespace. Parent RUN_ID:
//   PE2003_ROSETTA_GAMEBRYO_BRIDGE_CORRECTIONS_R1_20261030
//
// Executable proof that:
//  (a) the knowledge records load and are well-formed;
//  (b) a provenance lookup for "Textures.bnt 2EAE1159..." finds the EU_LATER
//      record and it is NOT served as ISO_5_1_0_0 (primary target) truth;
//  (c) an ISO_5_1_0_0 build query is EXPLICITLY REJECTED — no silent
//      substitution of SDK/PE42/EU_LATER records;
//  (d) the J4 transform adapter gates re-run PASS in this worktree
//      (correct adapter exit 0; wrong-transpose mutant exit non-zero).
//
// RESEARCH/REFERENCE ONLY — no runtime, no GUI, no game/SDK execution.
// Usage:  node tests/bridge/rosettaRegistry.test.mjs   (from the worktree root)

import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import process from 'node:process';

const HERE = dirname(fileURLToPath(import.meta.url));
const WORKROOT = join(HERE, '..', '..'); // worktree root (tests/bridge -> worktree)
const NS = join(WORKROOT, 'src', 'pe2003', 'rosetta', 'bridges', 'gamebryoReference');

const R = await import(
  (await import('node:url')).pathToFileURL(join(NS, 'rosettaReferenceRegistry.mjs')).href);

const ADAPTER = await import(
  (await import('node:url')).pathToFileURL(join(NS, 'niTransformAdapter.mjs')).href);

const results = [];
let failures = 0;
function gate(name, fn) {
  try {
    const detail = fn();
    results.push({ gate: name, status: 'PASS', detail });
    console.log(`GATE ${name}: PASS  ${detail ?? ''}`);
  } catch (e) {
    failures++;
    results.push({ gate: name, status: 'FAIL', error: String(e.message ?? e) });
    console.log(`GATE ${name}: FAIL  ${e.message ?? e}`);
  }
}
const expect = (cond, msg) => { if (!cond) throw new Error(msg); };
const sha256 = (p) => createHash('sha256').update(readFileSync(p)).digest('hex').toUpperCase();

// ---------------------------------------------------------------------------
// G-R0: J4 module copies are byte-identical (hash pins from the J4 contract)
// ---------------------------------------------------------------------------
gate('module_hashes_match_j4', () => {
  const pins = {
    'niTransformAdapter.mjs': '32D3DD4B6EA53E29EDB9953D0E79454E7D966F0F088A18651C8A69A6AB8B643F',
    'test_adapter.mjs': '8179AD185D05A7725F82B1601EC45F6E66F7055067CA885774361B5438559FA1',
    'mutant_wrong_transpose.mjs': '81F84F7C9B4E039A6D11A611EFEA3CCB710DE73B252A83B56813CBD2941298AC',
  };
  for (const [file, pin] of Object.entries(pins)) {
    const got = sha256(join(NS, file));
    expect(got === pin, `${file} sha256 ${got} != J4 pin ${pin}`);
  }
  return '3/3 module SHA256 == J4 contract pins (byte-identical copies)';
});

// ---------------------------------------------------------------------------
// G-R1: records loadable + well-formed (census level)
// ---------------------------------------------------------------------------
gate('records_loadable_and_wellformed', () => {
  const recs = R.loadRecords({ refresh: true });
  expect(recs.FORMAT_LOSS_MATRIX && recs.TEXTURE_ERA_RECORD &&
         recs.CLAIM_CORRECTIONS && recs.ROSETTA_INTEGRATION_MAP,
    'all four knowledge records must load');
  const flm = recs.FORMAT_LOSS_MATRIX;
  expect(Array.isArray(flm.rows) && flm.rows.length === 11, `FORMAT_LOSS_MATRIX must have 11 rows, got ${flm.rows?.length}`);
  const required = ['capability', 'status', 'evidence', 'correction', 'lab_only_flag'];
  for (const row of flm.rows) {
    for (const f of required) expect(row[f] !== undefined, `row ${row.capability} missing field ${f}`);
    expect(['SUPPORTED', 'PARTIAL', 'UNSUPPORTED', 'UNTESTED'].includes(row.status),
      `row ${row.capability} bad status ${row.status}`);
    expect(row.lab_only_flag && row.lab_only_flag.LAB_ADAPTED_ONLY === 'yes',
      `row ${row.capability} lab_only_flag must be LAB_ADAPTED_ONLY=yes`);
  }
  const caps = flm.rows.map((r) => r.capability);
  for (const c of ['transform_world', 'transform_view', 'hierarchy_reparent', 'billboard',
    'zbuffer_property', 'uv_animation', 'texture_rgb', 'texture_alpha',
    'skin', 'collision', 'niark_unknown']) {
    expect(caps.includes(c), `FORMAT_LOSS_MATRIX missing capability row ${c}`);
  }
  const ter = recs.TEXTURE_ERA_RECORD;
  const cmp = ter.per_member_comparison_vs_cd_jan_2003;
  expect(cmp.byte_identical_count === 16 && cmp.byte_different_count === 8 && cmp.absent_count === 0,
    `era comparison counts must be 16/8/0, got ${cmp.byte_identical_count}/${cmp.byte_different_count}/${cmp.absent_count}`);
  expect(cmp.byte_identical_ids.length === 16 && cmp.byte_different_ids.length === 8,
    'era comparison id lists must have 16+8 entries');
  expect(cmp.era_status_for_byte_different_members === 'NOT_ESTABLISHED',
    'era for the 8 byte-different members must be NOT_ESTABLISHED');
  expect(ter.era_verdict.SAME_ERA_WITH_PE42 === 'FALSE', 'SAME_ERA_WITH_PE42 must be FALSE');
  expect(ter.era_label_source.sha256 === 'E88B5104E2D902413357295507614C53AE1ABBB0383CF33C02C27BD903417799',
    'era label source must be PEProvenance.js (pinned hash)');
  const rim = recs.ROSETTA_INTEGRATION_MAP;
  expect(Array.isArray(rim.records) && rim.records.length === 7, `ROSETTA_INTEGRATION_MAP must have 7 records, got ${rim.records?.length}`);
  for (const m of rim.records) {
    expect(m.runtime_enabled === false, `integration-map record ${m.knowledge_record} must have runtime_enabled=false`);
    expect(typeof m.future_import === 'string' && m.future_import.length > 0,
      `integration-map record ${m.knowledge_record} missing future_import`);
    expect(typeof m.integration_pending === 'string' && m.integration_pending.includes('INTEGRATION_PENDING'),
      `integration-map record ${m.knowledge_record} missing INTEGRATION_PENDING note`);
  }
  return `4 records well-formed: FLM 11 rows (all LAB_ADAPTED_ONLY=yes), TER 16/8/0 + NOT_ESTABLISHED, RIM 7 records runtime_enabled=false`;
});

// ---------------------------------------------------------------------------
// G-R2: provenance lookup finds the EU_LATER record — NOT as ISO truth
// ---------------------------------------------------------------------------
gate('provenance_lookup_finds_eu_later_not_iso_truth', () => {
  const FULL = '2EAE115958D3157FA62F8CBFBAC6F4BFB5C38A820F1D05F9248C4200C0208A56';
  for (const q of [FULL, '2EAE1159', '2eae1159']) {
    const res = R.lookupByArchiveSha256(q);
    expect(res.status === 'FOUND', `lookup('${q}') must be FOUND, got ${res.status}: ${res.reason ?? ''}`);
    expect(res.era === 'EU_LATER', `lookup('${q}') era must be EU_LATER, got ${res.era}`);
    expect(res.record_id === 'EU_LATER:Textures.bnt', `unexpected record_id ${res.record_id}`);
    expect(res.usable_as === 'RE_EVIDENCE_ONLY', `usable_as must be RE_EVIDENCE_ONLY, got ${res.usable_as}`);
    expect(res.usable_as_primary_target_truth === false,
      'the EU_LATER record must NEVER be served as primary-target (ISO_5_1_0_0) truth');
    expect(res.primary_target_build === 'ISO_5_1_0_0',
      'record must name the primary target build it is NOT truth for');
    expect(res.same_era_with_pe42 === 'FALSE' || res.same_era_with_pe42 === false,
      'record must carry SAME_ERA_WITH_PE42=FALSE');
  }
  const miss = R.lookupByArchiveSha256('0000000000000000000000000000000000000000000000000000000000000000');
  expect(miss.status === 'NOT_FOUND', 'a sha miss must be NOT_FOUND, never invented');
  return `full+prefix+lowercase lookups of 'Textures.bnt 2EAE1159...' -> EU_LATER record, usable_as_primary_target_truth=false; miss -> NOT_FOUND`;
});

// ---------------------------------------------------------------------------
// G-R3: ISO_5_1_0_0 build query — explicit rejection, NO substitution
// ---------------------------------------------------------------------------
gate('iso51_query_rejects_substitution', () => {
  const res = R.lookupForBuild('ISO_5_1_0_0');
  expect(res.status === 'REJECTED',
    `ISO_5_1_0_0 query must be REJECTED, got ${JSON.stringify(res)}`);
  expect(res.build === 'ISO_5_1_0_0', 'rejection must name the queried build');
  expect(typeof res.reason === 'string' && /FORBIDDEN|substitution/i.test(res.reason),
    'rejection must state that cross-era substitution is forbidden');
  // no record payload may leak through a rejection
  expect(res.archive_sha256 === undefined && res.record_id === undefined && res.era === undefined,
    'a REJECTED result must carry no record payload');
  // the forbidden classes are exactly the records this namespace holds
  expect(R.ERAS_LOCAL.includes('EU_LATER') && !R.ERAS_LOCAL.includes('ISO_5_1_0_0'),
    'this namespace holds EU_LATER records only; none may serve as ISO_5_1_0_0');
  // negative probes: SDK / PE42 / unknown build queries also never substitute
  for (const b of ['SDK_1_2', 'PE42', 'JUL_2003', 'PCG_9_3_5', 'CD_JAN_2003']) {
    const r = R.lookupForBuild(b);
    expect(r.status === 'REJECTED' && r.archive_sha256 === undefined,
      `build query '${b}' must be REJECTED without payload, got ${JSON.stringify(r)}`);
  }
  // control: an era that DOES exist is found (proves rejection is scoping, not breakage)
  const eu = R.lookupForBuild('EU_LATER');
  expect(eu.status === 'FOUND' && eu.era === 'EU_LATER' && eu.usable_as_primary_target_truth === false,
    'EU_LATER query must FIND the EU_LATER record (still not primary-target truth)');
  return `ISO_5_1_0_0/SDK_1_2/PE42/JUL_2003/PCG_9_3_5/CD_JAN_2003 -> REJECTED (no payload); EU_LATER -> FOUND (RE_EVIDENCE_ONLY)`;
});

// ---------------------------------------------------------------------------
// G-R4: adapter math spot-check (in-process, from the worktree namespace)
// ---------------------------------------------------------------------------
gate('adapter_math_spotcheck', () => {
  const mod = ADAPTER; // imported at top level from the worktree namespace
  // canonical wrong-transpose counterexample: truth (50,0,18.5)
  const R90 = [[0, 0, 1], [0, 1, 0], [-1, 0, 0]];
  const ir = mod.makeIR({ scale: 1.5, rotate: R90, translate: [50, 0, 20] });
  const d3 = mod.d3dDeviceApply(mod.niToD3DWorld(ir), [1, 0, 0]);
  const th = mod.threeElementsApply(mod.niToThreeWorld(ir).columnMajorElements, [1, 0, 0]);
  const close = (a, b) => a.every((x, i) => Math.abs(x - b[i]) <= 1e-6);
  expect(close(d3, [50, 0, 18.5]), `d3d path ${d3} != ground truth (50,0,18.5)`);
  expect(close(th, [50, 0, 18.5]), `three path ${th} != ground truth (50,0,18.5)`);
  // camera mirror-fix spot: X must be col2, not norm(U x F)
  let threw = false;
  try { mod.cameraViewD3D(ir, {}); } catch (e) { threw = /convention/i.test(e.message); }
  expect(threw, 'cameraViewD3D without explicit convention must throw MissingConventionError');
  return 'rotY90/scale1.5 -> (50,0,18.5) on both device paths; convention parameter enforced';
});

// ---------------------------------------------------------------------------
// G-R5 + G-R6: adapter gates re-run PASS in the worktree; mutant MUST fail
// (each spawned process is bounded: timeout, own exit code recorded)
// ---------------------------------------------------------------------------
function runSuite(adapterArg) {
  const args = ['test_adapter.mjs'];
  if (adapterArg) args.push(`--adapter=${adapterArg}`);
  const t0 = Date.now();
  const cp = spawnSync(process.execPath, args, {
    cwd: NS,
    encoding: 'utf8',
    timeout: 120000,
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  return {
    command: `node ${args.join(' ')} (cwd=src/pe2003/rosetta/bridges/gamebryoReference)`,
    pid: cp.pid,
    status: cp.status,
    signal: cp.signal,
    timedOut: cp.error?.code === 'ETIMEDOUT' || cp.signal === 'SIGTERM',
    stdout: cp.stdout ?? '',
    stderr: cp.stderr ?? '',
    ms: Date.now() - t0,
  };
}

let suiteCorrect = null;
gate('adapter_gates_rerun_pass', () => {
  suiteCorrect = runSuite(null);
  expect(suiteCorrect.timedOut === false, 'correct-adapter suite timed out (bounded at 120s)');
  expect(suiteCorrect.status === 0,
    `correct adapter suite must exit 0, got ${suiteCorrect.status} (signal ${suiteCorrect.signal}); stdout tail: ${suiteCorrect.stdout.split('\n').slice(-6).join(' | ')}`);
  expect(/ALL_GATES_PASS/.test(suiteCorrect.stdout), 'suite stdout must contain ALL_GATES_PASS');
  const passCount = (suiteCorrect.stdout.match(/^\[PASS\]/gm) ?? []).length;
  expect(/GATE \w+: FAIL/.test(suiteCorrect.stdout) === false, 'no gate may FAIL on the correct adapter');
  const gates = [...suiteCorrect.stdout.matchAll(/^GATE (\w+): (PASS|SKIPPED)/gm)].map((m) => `${m[1]}=${m[2]}`);
  return `exit=0 pid=${suiteCorrect.pid} in ${suiteCorrect.ms}ms; gates: ${gates.join(', ')}; pass=${passCount}`;
});

gate('mutant_negative_control_fails', () => {
  const suiteMutant = runSuite('./mutant_wrong_transpose.mjs');
  expect(suiteMutant.timedOut === false, 'mutant suite timed out (bounded at 120s)');
  expect(suiteMutant.status !== 0 && suiteMutant.status !== null,
    `mutant suite must exit NON-ZERO, got ${suiteMutant.status}`);
  expect(/SUITE_FAIL/.test(suiteMutant.stdout), 'mutant stdout must contain SUITE_FAIL');
  return `exit=${suiteMutant.status} pid=${suiteMutant.pid} in ${suiteMutant.ms}ms (required negative control: non-zero)`;
});

// ---------------------------------------------------------------------------
// G-R7: claim corrections complete (all 6, old wordings preserved)
// ---------------------------------------------------------------------------
gate('claim_corrections_complete', () => {
  const cc = R.loadRecords().CLAIM_CORRECTIONS;
  expect(cc.corrections.length === 6, `must have 6 corrections, got ${cc.corrections.length}`);
  const byId = new Map(cc.corrections.map((c) => [c.id, c]));
  for (let i = 1; i <= 6; i++) {
    const c = byId.get(i);
    expect(c && c.old_wording && c.corrected_wording && c.source_finding && c.evidence_pointer,
      `correction #${i} must have old_wording/corrected_wording/source_finding/evidence_pointer`);
  }
  expect(byId.get(1).old_wording.includes('real 2003 textures'), 'correction #1 must preserve the rejected old wording');
  expect(byId.get(1).corrected_wording.includes('EU_LATER') &&
         byId.get(1).corrected_wording.includes('SAME_ERA_WITH_PE42=FALSE') &&
         byId.get(1).corrected_wording.includes('16/24') &&
         byId.get(1).corrected_wording.includes('NOT_ESTABLISHED'),
    'correction #1 corrected wording must carry the EU_LATER scoping');
  expect(byId.get(2).old_wording === 'lossless', 'correction #2 old wording must be the rejected blanket word');
  expect(byId.get(2).corrected_wording.includes('RGB lossless') &&
         byId.get(2).corrected_wording.includes('126773') && byId.get(2).corrected_wording.includes('126775') &&
         byId.get(2).corrected_wording.includes('X8R8G8B8'),
    'correction #2 corrected wording must scope RGB vs alpha loss');
  expect(byId.get(3).corrected_wording.includes('API-identity only') &&
         byId.get(3).corrected_wording.includes('PASS 8/8'),
    'correction #3 corrected wording must state API-identity only + 8/8 gates');
  expect(byId.get(4).corrected_wording.includes('PROVEN_BROKEN_FOR_7_OF_7') &&
         byId.get(4).corrected_wording.includes('4941.8') && byId.get(4).corrected_wording.includes('11291.1'),
    'correction #4 corrected wording must state the 7/7 break with delta range');
  expect(byId.get(5).old_wording.includes('54858') && byId.get(5).corrected_wording.includes('55304'),
    'correction #5 must record QC counter 54858 -> 55304');
  expect(byId.get(6).corrected_wording.includes('enumerated'),
    'correction #6 must record manifest incompleteness -> enumerated');
  return '6/6 corrections present with old wordings preserved verbatim and corrected wordings matching the R1 evidence';
});

// ---------------------------------------------------------------------------
// summary + exit code
// ---------------------------------------------------------------------------
console.log('--- REGISTRY GATE MATRIX ---');
for (const r of results) {
  console.log(`${r.status === 'PASS' ? '[PASS]' : `[${r.status}]`} ${r.gate}`);
}
if (failures === 0) {
  console.log(`ALL_REGISTRY_GATES_PASS (${results.length} pass, 0 fail) — namespace=src/pe2003/rosetta/bridges/gamebryoReference`);
  if (suiteCorrect) {
    console.log(`adapter_suite_command: ${suiteCorrect.command}`);
    console.log(`adapter_suite_exit_code: ${suiteCorrect.status}`);
  }
  process.exit(0);
} else {
  console.log(`REGISTRY_SUITE_FAIL: ${failures} gate(s) failed`);
  process.exit(1);
}
