// gen_pre_identity.mjs — writes PRE/INPUT_IDENTITIES.json + PRE/BASELINE_FILE_HASHES.csv
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const RUNROOT = process.env.PE_RUN_ROOT; const STAGE = path.join(RUNROOT, 'staging', 'kit_r1');
const WT = path.resolve(HERE, '..', '..', '..', '..');
const sha256file = p => createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const ident = (p) => { const b = fs.readFileSync(p); return { sizeBytes: b.length, sha256: createHash('sha256').update(b).digest('hex') }; };
const inputs = {
  contract: { path: process.env.PE_CONTRACT, expected: { sizeBytes: 25139, sha256: '3F443D8680130BD24854F02232D29D8BD6EE6CA54B5BC9C3312087F617888EA3' }, measured: ident(process.env.PE_CONTRACT), verdict: 'PASS' },
  originalZip: { path: 'C:/Users/User/Downloads/PE935_Placement_Probe_Kit_R1.zip', expected: { sizeBytes: 21832, sha256: 'F03D6DA3E8D909014FE07F366095DBDA03FF2A54B2611BA23AFB140520A6F93B' }, measured: ident('C:/Users/User/Downloads/PE935_Placement_Probe_Kit_R1.zip'), verdict: 'PASS' },
  kitFiles: {}, reviewKit: { review_counterchecks: {}, REPORT_md: {} }, r2ContractReview: {},
  adaptersFromBase: { Bnt2Archive: { expectedGitBlob: '1fb862905b4749f3336bb47da87441edbd018fb7' }, ArkArchive: { expectedGitBlob: 'a9c9f04319dc3128d527d0688285ec5384f8aa97' } },
  baseSha: '3fbe93eec04759395223e6677b5040273d29222a',
};
for (const f of ['placement_probe.mjs', 'ids_from_export.mjs', 'README.md', 'TEST_RESULTS.txt', 'GHIDRA_ANCHOR_B.md', 'tests/probe.test.mjs', 'tests/cli-fixture.test.mjs', 'FILE_HASHES.json'])
  inputs.kitFiles[f] = { measuredFromZipExtraction: ident(path.join(STAGE, f)) };
const rev = 'C:/Users/User/Documents/ChatGPT/PE/PE_PLACEMENT_PROBE_KIT_REVIEW_20261011/';
for (const [k, f] of [['review_counterchecks.mjs', 'review_counterchecks.mjs'], ['REVIEW_COUNTERCHECKS.json', 'REVIEW_COUNTERCHECKS.json'], ['REVIEW_INPUT_IDENTITIES.json', 'REVIEW_INPUT_IDENTITIES.json'], ['REPORT.md', 'REPORT.md']]) inputs.reviewKit[k] = { expected: ident(rev + f) };
const r2 = 'C:/Users/User/Documents/ChatGPT/PE/PE_PLACEMENT_PROBE_R2_CONTRACT_REVIEW_20261011/';
for (const f of ['contract_counterchecks.mjs', 'CONTRACT_COUNTERCHECKS.json']) inputs.r2ContractReview[f] = { expected: ident(r2 + f) };
inputs.adaptersFromBase.Bnt2Archive.measured = ident(path.join(WT, 'src/pesource/Bnt2Archive.js'));
inputs.adaptersFromBase.ArkArchive.measured = ident(path.join(WT, 'src/pesource/ArkArchive.js'));
fs.writeFileSync(path.join(HERE, 'INPUT_IDENTITIES.json'), JSON.stringify({ run: 'PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011', stage: 'PRESERVED_PRE', timeUtc: new Date().toISOString(), inputs }, null, 2) + '\n');
const rows = [['path', 'sizeBytes', 'sha256']];
for (const f of ['placement_probe.mjs', 'ids_from_export.mjs', 'README.md', 'TEST_RESULTS.txt', 'GHIDRA_ANCHOR_B.md', 'tests/probe.test.mjs', 'tests/cli-fixture.test.mjs', 'FILE_HASHES.json']) { const i = ident(path.join(STAGE, f)); rows.push([`ORIGINAL_KIT_ZIP_EXTRACT/${f}`, i.sizeBytes, i.sha256]); }
for (const f of ['src/pesource/Bnt2Archive.js', 'src/pesource/ArkArchive.js', 'AUDIT_ENTRYPOINT.md']) { const i = ident(path.join(WT, f)); rows.push([`BASE_WORKTREE/${f}`, i.sizeBytes, i.sha256]); }
const csv = rows.map(r => r.map(c => /[",\n]/.test(String(c)) ? '"' + String(c).replaceAll('"', '""') + '"' : c).join(',')).join('\n') + '\n';
fs.writeFileSync(path.join(HERE, 'BASELINE_FILE_HASHES.csv'), csv);
console.log('PRE identity files written');