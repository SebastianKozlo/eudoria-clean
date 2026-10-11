// gen_evidence_index.mjs — EVIDENCE_INDEX.md generated from the actual package files.
import fs from 'node:fs'; import path from 'node:path'; import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const PKG = path.resolve(HERE, '..');
const WT = path.resolve(PKG, '..', '..', '..');
const shaF = p => createHash('sha256').update(fs.readFileSync(p)).digest('hex');
let out = '';
out += '# EVIDENCE_INDEX — PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011\n\n';
out += 'Generated from the actual package bytes (path | size | sha256). Self and MANIFEST_SHA256.csv are excluded from this index (the manifest is generated LAST and covers them per the publication pipeline).\n\n';
out += '## Pinned external inputs (READ_ONLY, not in this package)\n';
const ext = [
  ['Contract OPENCODE_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R2_COMPLETE.md', 'C:/Users/User/Documents/ChatGPT/PE/PE_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R2_PROMPT_20261011/OPENCODE_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R2_COMPLETE.md', '25139', '3F44D8680130BD24854F02232D29D8BD6EE6CA54B5BC9C3312087F617888EA3'],
  ['Original ZIP PE935_Placement_Probe_Kit_R1.zip', 'C:/Users/User/Downloads/PE935_Placement_Probe_Kit_R1.zip', '21832', 'F03D6DA3E8D909014FE07F366095DBDA03FF2A54B2611BA23AFB140520A6F93B'],
  ['Review REVIEW_COUNTERCHECKS.json', 'C:/Users/User/Documents/ChatGPT/PE/PE_PLACEMENT_PROBE_KIT_REVIEW_20261011/REVIEW_COUNTERCHECKS.json', '3987', '9285636C4629F12787059948D71AE10CCEAB6C515356E5D55F6376705EC09944'],
  ['R2 contract review CONTRACT_COUNTERCHECKS.json', 'C:/Users/User/Documents/ChatGPT/PE/PE_PLACEMENT_PROBE_R2_CONTRACT_REVIEW_20261011/CONTRACT_COUNTERCHECKS.json', '1054', '4076B5131DE4CF9507E9720B9B8CA8543FA889C26F6F2810C4633E81E60EE602'],
];
out += '| item | path | bytes | sha256 |\n| --- | --- | ---: | --- |\n';
for (const [n, p, s, h] of ext) out += `| ${n} | ${p} | ${s} | ${h} |\n`;
out += '\nFull pinned input set with measured identities: PRE/INPUT_IDENTITIES.json; baseline hashes: PRE/BASELINE_FILE_HASHES.csv.\n\n';
out += '## Package files (walked from disk at generation time)\n\n';
out += '| path | bytes | sha256 |\n| --- | ---: | --- |\n';
const walk = d => { let r = []; for (const e of fs.readdirSync(d, { withFileTypes: true })) { const p = path.join(d, e.name); if (e.isDirectory()) r.push(...walk(p)); else r.push(p); } return r; };
const files = walk(PKG).filter(p => !p.endsWith('EVIDENCE_INDEX.md') && !p.endsWith('MANIFEST_SHA256.csv')).sort();
for (const f of files) out += '| ' + path.relative(WT, f).split(path.sep).join('/') + ' | ' + fs.statSync(f).size + ' | ' + shaF(f) + ' |';
out += '\n## Corrected tool files (outside the package, in the publication allowlist)\n\n';
out += '| path | bytes | sha256 |\n| --- | ---: | --- |\n';
const toolDir = path.join(WT, 'tools/placement_probe');
for (const f of walk(toolDir).sort()) out += '| ' + path.relative(WT, f).split(path.sep).join('/') + ' | ' + fs.statSync(f).size + ' | ' + shaF(f) + ' |';
fs.writeFileSync(path.join(PKG, 'EVIDENCE_INDEX.md'), out);
console.log('EVIDENCE_INDEX.md written; package files listed: ' + files.length + '; tool files: ' + walk(toolDir).length);
