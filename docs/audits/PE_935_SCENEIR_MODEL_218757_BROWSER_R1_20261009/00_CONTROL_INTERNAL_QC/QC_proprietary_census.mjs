// QC_proprietary_census.mjs — internal QC (pe-master-auditor). NOT executor code.
// Scans THIS RUN's changed text files for embedded original-asset content:
//  - bulk NIF header strings in a DATA context ("NetImmerse File Format" as data lines)
//  - long vertex-array-like f32 number sequences (>= 30 consecutive decimals with f32 magnitude)
//  - base64 blobs (>= 200 consecutive base64 chars)
//  - serialized f32-LE vertex byte patterns as hex (long hex strings >= 200 hex chars)
// Bounded control values/names/hashes are allowed (contract §9).
import { readFile } from 'node:fs/promises';
import path from 'node:path';

const ROOT = 'D:\\Eudoria_Reconstruction\\12_WebGame\\pe-sceneir-218757-r1';
const PKG = path.join(ROOT, 'docs', 'audits', 'PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009');

const FILES = [
  'src\\pecompat\\PecAssetAdapter.js', 'src\\pecompat\\PecInstanceBuilder.js',
  'src\\pecompat\\PecNif10Reader.js', 'src\\pecompat\\PecRenderConvert.js',
  'src\\pecompat\\PecSceneIR.js', 'src\\pecompat\\PecTransform.js',
  'compat\\api.js', 'compat\\app.js', 'compat\\asset-mode.js', 'compat\\compat.css',
  'compat\\index.html', 'compat\\scene-mode.js', 'compat\\server-sceneir.mjs',
  'tools\\pecompat\\controlB_compare.mjs', 'tools\\pecompat\\extract_218757.mjs',
  'tools\\pecompat\\sceneir_dump.mjs',
  'tests\\pecompat\\_app_server_helpers.mjs', 'tests\\pecompat\\_helpers.mjs',
  'tests\\pecompat\\api_path_denial.test.mjs', 'tests\\pecompat\\app_integration.test.mjs',
  'tests\\pecompat\\headless_load.test.mjs', 'tests\\pecompat\\instance_separation.test.mjs',
  'tests\\pecompat\\invalid_links.test.mjs', 'tests\\pecompat\\missing_texture.test.mjs',
  'tests\\pecompat\\model_218757.test.mjs', 'tests\\pecompat\\run_app_tests.mjs',
  'tests\\pecompat\\run_tests.mjs', 'tests\\pecompat\\transform_composition.test.mjs',
  'tests\\pecompat\\witness_457485_regression.test.mjs',
  'package.json',
  '.opencode\\skills\\pe-gamebryo-rosetta\\SKILL.md',
  '.opencode\\skills\\pe-gamebryo-rosetta\\references\\integration-rules.md',
  '.opencode\\skills\\pe-gamebryo-rosetta\\references\\source-locations.md',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\AUTHORIZATION_AND_PREFLIGHT.md',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\APP_AND_SERVER_NOTES.md',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\CONTROLS_A.json',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\CONTROLS_B.json',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\IMPLEMENTATION_NOTES.md',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\INPUT_IDENTITIES.json',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\INTERVENTION_LEDGER.md',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\PLAN_AND_PATH_ALLOWLIST.md',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\PREREGISTRATION.md',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\SMOKE_CHECKLIST.md',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\SOURCE_IDENTITIES.json',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\TEST_RESULTS_APP.json',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\TEST_RESULTS_UNIT.json',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\raw\\APP_INTEGRATION_MEASURED.json',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\raw\\FILE_SCENE_SPACE_TRANSFORMS_218757.json',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\raw\\HEADLESS_DOM_DUMP.html',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\raw\\HEADLESS_RUN.json',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\raw\\HTTP_TRANSCRIPTS.json',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\raw\\TESTS_APP_MACHINE_SUMMARY.json',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\raw\\TESTS_CONSOLE_OUTPUT.txt',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\raw\\TESTS_MACHINE_SUMMARY.json',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\raw\\sceneir_dump_218757.json',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\raw\\extract_218757.stdout.txt',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\raw\\controlB_compare_ROTATED_SCALED_PARENT.json',
  'docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\raw\\controlB_compare_THREE_LEVEL_SOCKET.json',
];

const findings = [];
function scan(relPath, text) {
  // 1. NIF header strings in a DATA context (not a prose/negation mention)
  const nifHdr = text.match(/["'`][^"'`\n]{0,40}NetImmerse File Format[^"'`\n]{0,60}["'`]/g);
  if (nifHdr) findings.push({ file: relPath, kind: 'NIF_HEADER_STRING_IN_QUOTES', count: nifHdr.length, sample: nifHdr[0].slice(0, 100) });
  const gbHdr = text.match(/["'`][^"'`\n]{0,40}Gamebryo File Format[^"'`\n]{0,60}["'`]/g);
  if (gbHdr) findings.push({ file: relPath, kind: 'GB_HEADER_STRING_IN_QUOTES', count: gbHdr.length, sample: gbHdr[0].slice(0, 100) });
  // 2. long vertex-array-like f32 sequences: >= 40 consecutive "-?d+(\.\d+)?([eE][-+]?\d+)?," numbers
  const arrSeq = text.match(/-?\d+(?:\.\d+)?(?:e[-+]?\d+)?(?:\s*,\s*-?\d+(?:\.\d+)?(?:e[-+]?\d+)?){39,}/gi);
  if (arrSeq) findings.push({ file: relPath, kind: 'LONG_FLOAT_ARRAY_SEQUENCE', count: arrSeq.length, len: arrSeq[0].length, sample: arrSeq[0].slice(0, 90) });
  // 3. base64 blobs >= 200 chars
  const b64 = text.match(/[A-Za-z0-9+/]{200,}={0,2}/g);
  if (b64) findings.push({ file: relPath, kind: 'BASE64_BLOB', count: b64.length, len: b64[0].length });
  // 4. long hex dumps >= 200 hex chars (potential raw byte payload)
  const hex = text.match(/\b[0-9a-fA-F]{200,}\b/g);
  if (hex) findings.push({ file: relPath, kind: 'LONG_HEX_BLOB', count: hex.length, len: hex[0].length });
  // 5. BNT2/BNT marker strings in a data context
  const bnt = text.match(/["'`]BNT2?["'`]/g);
  if (bnt) findings.push({ file: relPath, kind: 'BNT_MARKER_STRING', count: bnt.length, sample: 'BNT marker literal (check context)' });
}

for (const rel of FILES) {
  const p = path.join(ROOT, rel);
  let text;
  try { text = await readFile(p, 'utf8'); } catch { try { text = (await readFile(p)).toString('utf16le'); } catch { findings.push({ file: rel, kind: 'READ_FAIL' }); continue; } }
  scan(rel, text);
}

console.log('=== QC PROPRIETARY CENSUS (this run\'s changed files) ===');
if (findings.length === 0) {
  console.log('CLEAN: no embedded original-asset content patterns found.');
} else {
  for (const f of findings) console.log(JSON.stringify(f));
}
// special structural checks:
const dump = JSON.parse(await readFile(path.join(PKG, 'raw', 'sceneir_dump_218757.json'), 'utf8'));
let geometryArrayFields = 0;
for (const b of dump.blocks) if (b.geometry || b.positions || b.indices) geometryArrayFields++;
console.log(`sceneir_dump_218757.json: blocks with geometry-array fields = ${geometryArrayFields} (expected 0; bounded dump)`);
const fss = JSON.parse(await readFile(path.join(PKG, 'raw', 'FILE_SCENE_SPACE_TRANSFORMS_218757.json'), 'utf8'));
const fssBad = fss.blocks.filter((b) => b.positions || b.indices || b.geometry).length;
console.log(`FILE_SCENE_SPACE_TRANSFORMS_218757.json: entries=${fss.blocks.length}, with-array-fields=${fssBad} (expected 0)`);
const domText = await readFile(path.join(PKG, 'raw', 'HEADLESS_DOM_DUMP.html'), 'utf8');
const domFloatSeq = domText.match(/-?\d+(?:\.\d+)?(?:\s*,\s*-?\d+(?:\.\d+)?){39,}/g);
console.log(`HEADLESS_DOM_DUMP.html: long float array sequences = ${domFloatSeq ? domFloatSeq.length : 0} (expected 0; DOM text only)`);
