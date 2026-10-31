// av1_models_census.mjs — JOB AV-1 task 1+4 (loop 8ee81e37, era ISO_5_1_0_0).
// Read-only census of Models.ark (ArkVFS AK ZIP-clone, all STORED):
//   - full sequential local-header enumeration (name/offset/size)
//   - NIF version distribution (header text + u32 version per entry)
//   - block-type presence census via exact RTTI substring scan (animation,
//     skin, texture-chain block types) + numBlocks header read
// Writes MODELS_CENSUS.json (per-entry + aggregates) to the AV1_CENSUS SCI dir.
import { open } from 'node:fs/promises';

const ARK = 'D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Models.ark';
const OUT = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_ISO_ASSET_VIEWER_R1_20261031\\AV1_CENSUS\\MODELS_CENSUS.json';

// Block types counted per file via exact RTTI-name occurrence scan.
// NOTE: substring scan counts PRESENCE; a type name can also occur inside a
// payload string, but RTTI names are prefixed by i32 length in NIF 4.x —
// we therefore anchor on the 4-byte length prefix + name (len==name.length).
const BLOCK_TYPES = [
  'NiNode','NiTriShape','NiTriShapeData','NiTriStripsData','NiTexturingProperty',
  'NiMaterialProperty','NiAlphaProperty','NiZBufferProperty','NiVertexColorProperty',
  'NiStringExtraData','NiTextureEffect','NiUVController','NiUVData',
  'NiSourceTexture','NiArkTextureExtraData','NiArkAnimationExtraData',
  'NiArkImporterExtraData','NiArkViewportInfoExtraData','NiArkShaderExtraData',
  'NiKeyframeController','NiKeyframeData','NiTextKeyExtraData','NiFlipController',
  'NiSkinInstance','NiSkinData','NiSkinPartition','NiVisController','NiVisData',
  'NiCamera','NiPointLight','NiSpotLight','NiDirectionalLight','NiAmbientLight',
  'NiCollisionData','NiBillboardNode','NiArkBillboardNode','NiBSAnimationNode',
  'NiStencilProperty','NiSpecularProperty','NiShadeProperty','NiDitherProperty',
  'NiFogProperty','NiSortAdjustNode','NiLookAtController','NiIntegerExtraData',
  'NiBooleanExtraData','NiPosData','NiColorData','NiFloatData',
  'NiTextureTransformController','NiMorpherController','NiGeomMorpherController',
];

const enc = new TextEncoder();
function countRtti(hay, typeName) {
  // anchored: <i32 len LE><name bytes>  — an inline RTTI sized-string
  const nameB = enc.encode(typeName);
  const anchor = Buffer.alloc(4 + nameB.length);
  anchor.writeInt32LE(nameB.length, 0);
  nameB.copy ? null : null;
  Buffer.from(nameB).copy(anchor, 4);
  let count = 0, pos = 0;
  while (true) {
    const i = hay.indexOf(anchor, pos);
    if (i < 0) break;
    count++; pos = i + 1;
  }
  return count;
}

const fh = await open(ARK, 'r');
const stat = await fh.stat();
const sizeH = stat.size;
// sequential scan; read header region per entry, payload lazily in chunks.
// To keep it simple and fast: read whole file (129 MB) once.
const buf = Buffer.alloc(sizeH);
await fh.read(buf, 0, sizeH, 0);
await fh.close();

function readEntryAt(pos) {
  if (!(buf[pos]===0x41 && buf[pos+1]===0x4b && buf[pos+2]===0x03 && buf[pos+3]===0x04)) return null;
  const flags = buf.readUInt16LE(pos+6);
  const compression = buf.readUInt16LE(pos+8);
  const crc32 = buf.readUInt32LE(pos+14);
  const compSize = buf.readUInt32LE(pos+18);
  const uncompSize = buf.readUInt32LE(pos+22);
  const nameLen = buf.readUInt16LE(pos+26);
  const extraLen = buf.readUInt16LE(pos+28);
  const name = buf.toString('latin1', pos+30, pos+30+nameLen);
  const dataOffset = pos + 30 + nameLen + extraLen;
  return { entryIndex:-1, name, size: uncompSize, compSize, compression, flags, crc32, dataOffset };
}

const entries = [];
let pos = 0;
while (pos + 4 <= sizeH) {
  if (!(buf[pos]===0x41 && buf[pos+1]===0x4b && buf[pos+2]===0x03 && buf[pos+3]===0x04)) break;
  const e = readEntryAt(pos);
  e.entryIndex = entries.length;
  e.headerOffset = pos;
  entries.push(e);
  pos = e.dataOffset + e.compSize;
}
// EOCD cross-check
let eocd = -1;
for (let i = sizeH-22; i >= sizeH-22-65536 && i>=0; i--) {
  if (buf[i]===0x41&&buf[i+1]===0x4b&&buf[i+2]===0x05&&buf[i+3]===0x06){eocd=i;break;}
}
const eocdTotal = eocd>=0 ? buf.readUInt16LE(eocd+10) : -1;

const versionDist = {};
const perEntry = [];
const typeFileCounts = {};   // files containing >=1 occurrence
const typeTotalCounts = {};  // total anchored occurrences corpus-wide
for (const t of BLOCK_TYPES) { typeFileCounts[t]=0; typeTotalCounts[t]=0; }

for (const e of entries) {
  const p = buf.subarray(e.dataOffset, e.dataOffset + e.size);
  // header: text up to \n, then u32 version, u32 numBlocks
  const nl = p.indexOf(0x0a);
  const headerText = p.toString('latin1', 0, nl);
  const versionRaw = p.readUInt32LE(nl+1);
  const numBlocks = p.readUInt32LE(nl+5);
  const vs = `${versionRaw>>>24}.${(versionRaw>>>16)&0xff}.${(versionRaw>>>8)&0xff}.${versionRaw&0xff}`;
  versionDist[vs] = (versionDist[vs]||0)+1;
  const blockCount = {};
  for (const t of BLOCK_TYPES) {
    const c = countRtti(p, t);
    if (c>0) { blockCount[t]=c; typeFileCounts[t]++; typeTotalCounts[t]+=c; }
  }
  perEntry.push({ name:e.name, headerOffset:e.headerOffset, dataOffset:e.dataOffset, size:e.size, crc32:e.crc32, headerText, versionRaw:'0x'+versionRaw.toString(16).padStart(8,'0'), version:vs, numBlocksHeader:numBlocks, anchoredBlockCount:blockCount });
}

// animation/skin rollups
const animatedKf = perEntry.filter(x=>(x.anchoredBlockCount['NiKeyframeController']||0)>0);
const skinned = perEntry.filter(x=>['NiSkinInstance','NiSkinData','NiSkinPartition'].some(t=>(x.anchoredBlockCount[t]||0)>0));
const texProp = perEntry.filter(x=>(x.anchoredBlockCount['NiTexturingProperty']||0)>0);
const srcTex = perEntry.filter(x=>(x.anchoredBlockCount['NiSourceTexture']||0)>0);
const arkTex = perEntry.filter(x=>(x.anchoredBlockCount['NiArkTextureExtraData']||0)>0);

const result = {
  job:'AV1', loop:'8ee81e37', era:'ISO_5_1_0_0', generated:new Date().toISOString(),
  source:{ path:ARK, bytes:sizeH, sha256:'F660D055B4B9471B3B6E16B07F5368DBD6F2208DAB6B51BB9BDB9942BD73EA62' },
  ark:{ eocdOffset:eocd, eocdTotalEntries:eocdTotal, scannedEntries:entries.length, eocdMatch:eocdTotal===entries.length },
  versionDistribution:versionDist,
  blockTypeCensus:{ filesContaining:typeFileCounts, totalAnchoredOccurrences:typeTotalCounts },
  rollups:{
    filesTotal:entries.length,
    filesWithNiKeyframeController:animatedKf.length,
    filesWithNiKeyframeData:perEntry.filter(x=>(x.anchoredBlockCount['NiKeyframeData']||0)>0).length,
    filesWithNiTextKeyExtraData:perEntry.filter(x=>(x.anchoredBlockCount['NiTextKeyExtraData']||0)>0).length,
    filesWithNiSkinAny:skinned.length,
    filesWithNiTexturingProperty:texProp.length,
    filesWithNiSourceTexture:srcTex.length,
    filesWithNiArkTextureExtraData:arkTex.length,
    filesWithTextureEffect:perEntry.filter(x=>(x.anchoredBlockCount['NiTextureEffect']||0)>0).length,
  },
  entries:perEntry,
};
await (await import('node:fs/promises')).writeFile(OUT, JSON.stringify(result,null,1));
console.log('entries',entries.length,'eocd',eocdTotal,'match',eocdTotal===entries.length);
console.log('versions',versionDist);
console.log('rollups',result.rollups);
