// gen_pre.mjs — PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011 (extra PRE harness, censused)
// Writes PRE/BOOT_INPUT_IDENTITIES.json, PRE/BASELINE_FILE_HASHES.csv, PRE/SOURCE_PACKAGE_FREEZE.json.
// PROVENANCE: run-local instrument. Measures every input independently with node:crypto
// (Get-Item/Get-FileHash bootstrapping with explicit if-conditions was ALSO performed in the
// invoking PowerShell session and recorded in the run ledger — the JSON below documents both).
// Expected size/SHA256 are FROZEN CONSTANTS (from the human-authorized contract and
// INPUT_PINS.json identity pins); they are NEVER regenerated from the measured files.
import fs from 'node:fs'; import path from 'node:path'; import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url'; import { createHash } from 'node:crypto';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const arg = (k, d) => { const i = process.argv.indexOf(k); return i >= 0 ? process.argv[i + 1] : d; };
const WORKTREE = path.resolve(arg('--worktree'));
const CONTRACT = path.resolve(arg('--contract'));
const PINS = path.resolve(arg('--pins'));
const FROZEN = {
  runId: 'PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011',
  contract: { sizeBytes: 23496, sha256: '38205CE52733E3F1AEC707B9921BF7DABFDD5DC80F9A4F15B0DFAF3A43F67F5C' },
  inputPins: { sizeBytes: 4550, sha256: 'F39541326226531F9C0F0806B30CE029BB5DD54403B50C82691AEABFEB043711' },
  expectedBaseSha: '938aa9462560873126f1e9114dba0319062772f1',
  sourceRef: 'refs/heads/research/pe935-placement-probe-correction-r1-20261011',
  resultRef: 'refs/heads/research/pe935-placement-probe-census-postaudit-r1-20261011',
  expectedMasterSha: '3fbe93eec04759395223e6677b5040273d29222a',
  gitBlobs: {
    'tools/placement_probe/placement_probe.mjs': '6dc5844a6e6f75ad47d01e4583d58d0a16f73d60',
    'docs/audits/PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011/PRE/gen_pre_identity.mjs': '9c57e2bc9c75e596d76cea9d8200cb31808c2719',
    'src/pesource/Bnt2Archive.js': '1fb862905b4749f3336bb47da87441edbd018fb7',
    'src/pesource/ArkArchive.js': 'a9c9f04319dc3128d527d0688285ec5384f8aa97',
  },
  zip: { path: 'C:\\Users\\User\\Downloads\\PE935_Placement_Probe_Kit_R1.zip', sizeBytes: 21832, sha256: 'F03D6DA3E8D909014FE07F366095DBDA03FF2A54B2611BA23AFB140520A6F93B' },
};
const sha = b => createHash('sha256').update(b).digest('hex');
const ident = p => { const b = fs.readFileSync(p); return { sizeBytes: b.length, sha256: sha(b) }; };
const cmpPin = (frozen, measured) => {
  const sizeOk = measured.sizeBytes === frozen.sizeBytes;
  const shaOk = measured.sha256.toUpperCase() === frozen.sha256.toUpperCase();
  return { sizeOk, shaOk, match: sizeOk && shaOk };
};

// ---- 1. contract + INPUT_PINS identity (fail-closed bootstrap of THIS run) ----
const contractIdent = ident(CONTRACT);
const contractCheck = cmpPin(FROZEN.contract, contractIdent);
const pinsIdent = ident(PINS);
const pinsCheck = cmpPin(FROZEN.inputPins, pinsIdent);
if (!(contractCheck.match && pinsCheck.match)) {
  console.error('BLOCKED_INPUT_IDENTITY: contract/InputPins pin mismatch');
  process.exit(3);
}

// ---- 2. all 16 pinned inputs from INPUT_PINS.json ----
const pinsJson = JSON.parse(fs.readFileSync(PINS, 'utf8'));
const inputResults = [];
for (const inp of pinsJson.inputs) {
  let measured = null, exists = fs.existsSync(inp.path), check = { sizeOk: false, shaOk: false, match: false }, err = null;
  try { if (exists) { measured = ident(inp.path); check = cmpPin(inp, measured); } } catch (e) { err = String(e); }
  inputResults.push({ path: inp.path, expected: { sizeBytes: inp.sizeBytes, sha256: inp.sha256 }, measured, exists, compareResult: !exists ? 'MISSING' : check.match ? 'MATCH' : 'MISMATCH', ...check, error: err });
}

// ---- 3. git state: SOURCE_REF == BASE, RESULT_REF absent, master separate, HEAD == BASE ----
const git = (args) => { const r = spawnSync('git', ['-C', WORKTREE, ...args], { encoding: 'utf8' }); return { out: r.stdout.trim(), err: r.stderr.trim(), code: r.status }; };
const sourceRefSha = git(['rev-parse', FROZEN.sourceRef]).out;
const resultRefLocal = git(['rev-parse', '--verify', FROZEN.resultRef]);
const masterSha = git(['rev-parse', 'refs/heads/master']).out;
const headSha = git(['rev-parse', 'HEAD']).out;
const remoteRefs = spawnSync('git', ['-C', WORKTREE, 'ls-remote', 'origin', FROZEN.sourceRef, FROZEN.resultRef, 'refs/heads/master'], { encoding: 'utf8' }).stdout.trim().split('\n').filter(Boolean).map(l => l.split('\t'));
const remoteResultRef = remoteRefs.find(r => r[1] === FROZEN.resultRef);
const gitChecks = {
  sourceRefEqualsBase: sourceRefSha === FROZEN.expectedBaseSha,
  sourceRefSha,
  resultRefLocalAbsent: resultRefLocal.code !== 0,
  resultRefRemoteAbsent: remoteResultRef === undefined,
  masterEqualsExpected: masterSha === FROZEN.expectedMasterSha,
  masterIsNotBase: masterSha !== FROZEN.expectedBaseSha,
  worktreeHeadEqualsBase: headSha === FROZEN.expectedBaseSha,
  headSha,
};

// ---- 4. the four pinned Git blobs at BASE ----
const blobChecks = [];
for (const [p, expectedBlob] of Object.entries(FROZEN.gitBlobs)) {
  const actual = git(['rev-parse', FROZEN.expectedBaseSha + ':' + p]).out;
  blobChecks.push({ path: p, expectedBlob, measuredBlob: actual, match: actual === expectedBlob });
}

// ---- 5. ZIP + its 7 FILE_HASHES.json members (measured from the pinned ZIP itself) ----
const zipIdent = ident(FROZEN.zip.path);
const zipCheck = cmpPin(FROZEN.zip, zipIdent);

// ---- verdict ----
const allInputsOk = inputResults.every(r => r.compareResult === 'MATCH');
const boot = {
  runId: FROZEN.runId, stage: 'PRESERVED_PRE_BOOT', timeUtc: new Date().toISOString(), node: process.version,
  independentMeasurement: 'node:crypto sha256 + fs.statSync size; expected values are frozen constants from the human-authorized contract + INPUT_PINS.json; never derived from measured files. A second independent PowerShell Get-Item/Get-FileHash bootstrap with explicit if-conditions was performed by the executor before this script ran (see FINAL_REPORT BOOT section).',
  contract: { path: CONTRACT, expected: FROZEN.contract, measured: contractIdent, ...contractCheck, compareResult: contractCheck.match ? 'MATCH' : 'MISMATCH' },
  inputPins: { path: PINS, expected: FROZEN.inputPins, measured: pinsIdent, ...pinsCheck, compareResult: pinsCheck.match ? 'MATCH' : 'MISMATCH' },
  pinnedInputs: { count: inputResults.length, allMatch: allInputsOk, results: inputResults },
  git: gitChecks,
  gitBlobs: { allMatch: blobChecks.every(b => b.match), results: blobChecks },
  originalKitZip: { path: FROZEN.zip.path, expected: { sizeBytes: FROZEN.zip.sizeBytes, sha256: FROZEN.zip.sha256 }, measured: zipIdent, ...zipCheck, compareResult: zipCheck.match ? 'MATCH' : 'MISMATCH' },
};
boot.verdict = (contractCheck.match && pinsCheck.match && allInputsOk && gitChecks.sourceRefEqualsBase && gitChecks.resultRefLocalAbsent && gitChecks.resultRefRemoteAbsent && gitChecks.masterEqualsExpected && gitChecks.worktreeHeadEqualsBase && gitChecks.masterIsNotBase && boot.gitBlobs.allMatch && zipCheck.match) ? 'BOOT_PASS' : 'BLOCKED_INPUT_IDENTITY';
fs.writeFileSync(path.join(HERE, 'BOOT_INPUT_IDENTITIES.json'), JSON.stringify(boot, null, 2) + '\n');

// ---- BASELINE_FILE_HASHES.csv (BASE worktree bytes before any correction) ----
const rows = [['path', 'sizeBytes', 'sha256']];
for (const f of ['tools/placement_probe/placement_probe.mjs', 'tools/placement_probe/ids_from_export.mjs', 'tools/placement_probe/README.md', 'tools/placement_probe/tests/fixtures.mjs', 'tools/placement_probe/tests/probe.test.mjs', 'tools/placement_probe/tests/cli-fixture.test.mjs', 'tools/placement_probe/tests/budget.test.mjs', 'tools/placement_probe/tests/census_extra.test.mjs', 'tools/placement_probe/tests/correction_matrix.test.mjs', 'src/pesource/Bnt2Archive.js', 'src/pesource/ArkArchive.js', 'AUDIT_ENTRYPOINT.md']) {
  const p = path.join(WORKTREE, f); const i = ident(p); rows.push([`BASE_WORKTREE/${f}`, i.sizeBytes, i.sha256]);
}
const csv = rows.map(r => r.map(c => /[",\n]/.test(String(c)) ? '"' + String(c).replaceAll('"', '""') + '"' : c).join(',')).join('\n') + '\n';
fs.writeFileSync(path.join(HERE, 'BASELINE_FILE_HASHES.csv'), csv);

// ---- SOURCE_PACKAGE_FREEZE.json: all Git blobs of the frozen 938aa946 package ----
const ls = spawnSync('git', ['-C', WORKTREE, 'ls-tree', '-r', '--format=%(objectname) %(path)', FROZEN.expectedBaseSha, '--', 'docs/audits/PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011'], { encoding: 'utf8' });
const blobs = ls.stdout.trim().split('\n').map(l => { const i = l.indexOf(' '); return { blob: l.slice(0, i), path: l.slice(i + 1) }; });
const freeze = {
  runId: FROZEN.runId, stage: 'PRESERVED_PRE_SOURCE_PACKAGE_FREEZE', timeUtc: new Date().toISOString(),
  sourcePackage: 'docs/audits/PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011',
  policy: 'READ_ONLY — the whole historical 938aa946 package (including the incorrect PRE identity generator and old verdicts/timestamps) is preserved unchanged; nothing of it is overwritten in this run.',
  blobCount: blobs.length, expectedBlobCount: 37, allPresent: blobs.length === 37, blobs,
};
fs.writeFileSync(path.join(HERE, 'SOURCE_PACKAGE_FREEZE.json'), JSON.stringify(freeze, null, 2) + '\n');
console.log(JSON.stringify({ verdict: boot.verdict, pinnedInputs: inputResults.length, allInputsOk, blobs: blobs.length }));
process.exit(boot.verdict === 'BOOT_PASS' ? 0 : 3);
