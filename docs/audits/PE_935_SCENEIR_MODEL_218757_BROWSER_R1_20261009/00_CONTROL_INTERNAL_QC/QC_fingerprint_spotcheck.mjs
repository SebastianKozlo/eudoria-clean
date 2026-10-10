// QC_fingerprint_spotcheck.mjs — PE_935_SCENEIR_MODEL_218757_BROWSER_R1 internal QC
// INDEPENDENT spot-check by pe-master-auditor (fresh session). NOT executor code.
//
// What this does (independent of the executor's reader implementation):
//  1. Loads the pinned 218757 payload copy (verifies SHA256 == pin first).
//  2. For two claimed NiTriShapeData block ranges [start,end) from the
//     executor's SceneIR dump, parses the block with THIS QC's OWN cursor
//     implementation of the documented NIF 10.1 NiTriShapeData layout
//     (preamble u32==0; numVertices u16; keep u8; compress u8; hasVertices u8
//     -> nV*3 f32; uv-info 2 bytes; hasNormals u8 -> nV*3 f32 (+tangent/
//     bitangent if (b2 & 0xF0)); center 3 f32; radius f32; hasVertexColors u8
//     -> nV*4 f32; uvSets (b1 & 63) x nV*2 f32; consistency u16; numTriangles
//     u16; numTrianglePoints u32; hasTriangles u8 -> numT*3 u16;
//     numMatchGroups u16 + groups).
//  3. STRUCTURAL CHECK: the QC cursor must consume EXACTLY the claimed end.
//  4. Hashes the EXACT raw byte slices of the f32-LE position array and the
//     u16-LE index array and compares against BOTH the executor's dump values
//     and the predecessor's independent Python-parser values.
// No payload bytes are written anywhere; outputs are counts/hashes only.
import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';

const PIN_COPY = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\\sandbox\\payloads\\218757.nif';
const PIN_SHA = '3e8a22c2213202207e374b55cd65b2c3be039ccdd1e8d01a07fcaf44de12cf36';
const DUMP = 'D:\\Eudoria_Reconstruction\\12_WebGame\\pe-sceneir-218757-r1\\docs\\audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\raw\\sceneir_dump_218757.json';

// (dataBlock, claimedRange, expected counts, executor hashes (from dump), predecessor hashes (from BASE RELATION_RESULTS))
const CASES = [
  {
    dataBlock: 20, mesh: 'B_Outpost_me01_Ext_sign:0', nV: 92, nT: 56,
    exec: { v: '3869b16b6ccb33f4d689dbf3e14b6eeb9695140f6d51e54e6cd458c2a4f68064', i: '568540599fd86e8164dfb9f701df06549ddab85fa6d0549be2e0eae27c98bdfd' },
    pred: { v: '3869B16B6CCB33F4D689DBF3E14B6EEB9695140F6D51E54E6CD458C2A4F68064', i: '568540599FD86E8164DFB9F701DF06549DDAB85FA6D0549BE2E0EAE27C98BDFD' },
  },
  {
    dataBlock: 47, mesh: 'dPVS_occ04:0', nV: 30, nT: 10,
    exec: { v: 'f8848efe7a1f985bc5a7ae9e87f6dc011ebbd38f46f9ee427c72702f458b9ff8', i: 'c933b00a5ea7b3b09cf20ee0d233e7929fa16c91b109160e843b6f2960fa59c1' },
    pred: { v: 'F8848EFE7A1F985BC5A7AE9E87F6DC011EBBD38F46F9EE427C72702F458B9FF8', i: 'C933B00A5EA7B3B09CF20EE0D233E7929FA16C91B109160E843B6F2960FA59C1' },
  },
];

const sha256 = (b) => createHash('sha256').update(b).digest('hex');
const payload = new Uint8Array(await readFile(PIN_COPY));
const payloadSha = sha256(payload);
if (payloadSha !== PIN_SHA) { console.error('QC ABORT: payload SHA mismatch'); process.exit(1); }
console.log(`QC payload pin verified: ${payloadSha} (${payload.length} B)`);

const dump = JSON.parse(await readFile(DUMP, 'utf8'));
const blocksByIndex = new Map(dump.blocks.map((b) => [b.index, b]));
const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);

for (const c of CASES) {
  const blk = blocksByIndex.get(c.dataBlock);
  const [start, end] = blk.byteRange;
  console.log(`\n== dataBlock ${c.dataBlock} (${c.mesh}) claimed byteRange [${start},${end}) len=${end - start} ==`);
  let p = start;
  const u32 = () => { const v = dv.getUint32(p, true); p += 4; return v; };
  const u16 = () => { const v = dv.getUint16(p, true); p += 2; return v; };
  const u8 = () => { const v = payload[p]; p += 1; return v; };
  const preamble = u32();
  if (preamble !== 0) { console.error(`QC FAIL: preamble ${preamble} != 0`); process.exit(1); }
  const nV = u16(); const keep = u8(); const compress = u8();
  const hasVertices = u8();
  if (hasVertices !== 1) { console.error('QC FAIL: hasVertices != 1'); process.exit(1); }
  const posStart = p;
  const n = nV * 3;
  for (let i = 0; i < n; i++) p += 4; // f32 LE
  const posEnd = p;
  const numUvSetsLo = u8(); const extraVecFlags = u8();
  const tangentFlag = (extraVecFlags & 0xf0) !== 0;
  const hasNormals = u8();
  let hasTangents = 0;
  if (hasNormals === 1) {
    for (let i = 0; i < nV * 3; i++) p += 4;
    if (tangentFlag) { for (let i = 0; i < nV * 3; i++) p += 4; for (let i = 0; i < nV * 3; i++) p += 4; hasTangents = 1; }
  }
  p += 12; // center 3 f32
  p += 4;  // radius
  const hasColors = u8();
  if (hasColors === 1) for (let i = 0; i < nV * 4; i++) p += 4;
  const uvSetCount = numUvSetsLo & 63;
  for (let s = 0; s < uvSetCount; s++) for (let i = 0; i < nV * 2; i++) p += 4;
  const consistency = u16(); const nT = u16(); const nTP = u32();
  const hasTriangles = u8();
  if (hasTriangles !== 1) { console.error('QC FAIL: hasTriangles != 1'); process.exit(1); }
  const idxStart = p;
  for (let i = 0; i < nT * 3; i++) p += 2; // u16 LE
  const idxEnd = p;
  const nMatchGroups = u16();
  let matchIndices = 0;
  for (let g = 0; g < nMatchGroups; g++) { const cnt = u16(); matchIndices += cnt; for (let i = 0; i < cnt; i++) p += 2; }

  const structuralExact = p === end;
  const vSha = sha256(payload.subarray(posStart, posEnd));
  const iSha = sha256(payload.subarray(idxStart, idxEnd));
  console.log(`QC counts: nV=${nV} (expected ${c.nV}) nT=${nT} (expected ${c.nT}) nTP=${nTP} uvSets=${uvSetCount} tangents=${hasTangents} colors=${hasColors} matchGroups=${nMatchGroups}(${matchIndices} idx) keep=${keep} compress=${compress} consistency=${consistency}`);
  console.log(`QC cursor end=${p} vs claimed end=${end} -> STRUCTURAL_CLOSURE_EXACT=${structuralExact}`);
  console.log(`QC posBytes [${posStart},${posEnd}) len=${posEnd - posStart} (expect ${c.nV * 12}) idxBytes [${idxStart},${idxEnd}) len=${idxEnd - idxStart} (expect ${c.nT * 6})`);
  console.log(`QC vertex sha256 = ${vSha}`);
  console.log(`QC index sha256 = ${iSha}`);
  console.log(`QC vs EXECUTOR dump: vertex MATCH=${vSha === c.exec.v} index MATCH=${iSha === c.exec.i}`);
  console.log(`QC vs PREDECESSOR : vertex MATCH=${vSha.toUpperCase() === c.pred.v} index MATCH=${iSha.toUpperCase() === c.pred.i}`);
  if (!structuralExact || vSha !== c.exec.v || iSha !== c.exec.i || nV !== c.nV || nT !== c.nT) {
    console.error(`QC VERDICT block ${c.dataBlock}: SPOTCHECK_FAIL`);
  } else {
    console.log(`QC VERDICT block ${c.dataBlock}: SPOTCHECK_PASS`);
  }
}
