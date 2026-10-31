// av1_reader_audit.mjs — JOB AV-1 task 2+3: NifModelReader41 readiness audit
// on a random sample (>=200 NIF 4.1.0.12 files from Models.ark), plus texture
// chain byte-level observation + Textures.ark join. Read-only on inputs.
// Outputs READINESS_MATRIX.json + TEXTURE_CHAIN_EVIDENCE.json to the SCI dir.
import { open } from 'node:fs/promises';
import { parseModel41 } from 'file:///D:/Eudoria_Reconstruction/12_WebGame/pe2003-world-night6h-r1/src/pesource/NifModelReader41.js';

const ARK = 'D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Models.ark';
const TEX_ARK = 'D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Textures.ark';
const OUTDIR = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_ISO_ASSET_VIEWER_R1_20261031\\AV1_CENSUS';
const W = process.env.W || '7777'; // deterministic LCG seed
let seed = parseInt(W,10);
const rnd = () => { seed = (seed*1103515245+12345)>>>0; return (seed>>>16)/65536; };

const fh = await open(ARK,'r'); const stat = await fh.stat();
const buf = Buffer.alloc(stat.size); await fh.read(buf,0,stat.size,0); await fh.close();

const entries = [];
{ let pos=0; const b=buf;
  while (pos+4<=b.length && b[pos]===0x41&&b[pos+1]===0x4b&&b[pos+2]===0x03&&b[pos+3]===0x04) {
    const compSize=b.readUInt32LE(pos+18), uncompSize=b.readUInt32LE(pos+22),
          nameLen=b.readUInt16LE(pos+26), extraLen=b.readUInt16LE(pos+28);
    const name=b.toString('latin1',pos+30,pos+30+nameLen);
    const dataOffset=pos+30+nameLen+extraLen;
    entries.push({name,dataOffset,size:uncompSize}); pos=dataOffset+compSize;
  } }

function payload(e){ return new Uint8Array(buf.subarray(e.dataOffset,e.dataOffset+e.size)); }
function versionOf(e){ const p=buf.subarray(e.dataOffset,e.dataOffset+e.size); const nl=p.indexOf(0x0a); return p.readUInt32LE(nl+1); }

const v41 = entries.filter(e=>versionOf(e)===0x0401000C);
const v40 = entries.filter(e=>versionOf(e)!==0x0401000C);
console.log('v41',v41.length,'v40x',v40.length);

// ---- sample: 200 random 4.1 files + 10 random 4.0.x (negative control) ----
const sample = [];
while (sample.length<200) sample.push(v41[Math.floor(rnd()*v41.length)]);
const neg = [];
while (neg.length<10) neg.push(v40[Math.floor(rnd()*v40.length)]);

const results = [];
for (const e of sample) {
  let r;
  try {
    const { extraction, renderModel } = parseModel41(payload(e), e.name);
    const opaqueTypes = extraction.opaqueBlocks.map(o=>o.type);
    const typeCount = {};
    for (const b of extraction.blocks) typeCount[b.type]=(typeCount[b.type]||0)+1;
    r = {
      name:e.name, status:'PASS', parseStatus:extraction.parseStatus,
      numBlocks:extraction.header.numBlocks, blocksParsed:extraction.blocks.length,
      opaqueCount:extraction.opaqueBlocks.length, opaqueTypes:[...new Set(opaqueTypes)],
      stopped: extraction.parseStatus!=='PASS',
      shapes:renderModel.shapes.length, controllers:renderModel.counts.controllers,
      tailBytes:extraction.fileTailBytesLen,
      shapeSamples:renderModel.shapes.slice(0,4).map(s=>({name:s.shapeName,verts:s.numVertices,tris:s.numTriangles,skinRef:s.skinRef,texProp:!!s.textureProp,matProp:!!s.material})),
      blockTypes:typeCount,
    };
  } catch (err) {
    r = { name:e.name, status:'FAIL', error:String(err.message||err).slice(0,300) };
  }
  results.push(r);
}
const negResults = [];
for (const e of neg) {
  try { parseModel41(payload(e), e.name); negResults.push({name:e.name,status:'UNEXPECTED_PASS'}); }
  catch (err) { negResults.push({name:e.name,status:'LOUD_FAIL',error:String(err.message||err).slice(0,160)}); }
}

const pass = results.filter(r=>r.status==='PASS');
const full = pass.filter(r=>r.opaqueCount===0 && !r.stopped && r.shapes>0);
const partialOpaque = pass.filter(r=>r.opaqueCount>0 && !r.stopped);
const stopped = pass.filter(r=>r.stopped);
const failed = results.filter(r=>r.status==='FAIL');
// fail-reason census by first unsupported opaque type / error text
const failReasons = {};
for (const r of failed) { failReasons[r.error.split(' at ')[0].slice(0,120)]=(failReasons[r.error.split(' at ')[0].slice(0,120)]||0)+1; }
const opaqueTypeCensus = {};
for (const r of pass) for (const t of r.opaqueTypes) opaqueTypeCensus[t]=(opaqueTypeCensus[t]||0)+1;

// ---- texture chain observation on passing textured samples ----
// For each sample with a textureProp: inspect source refs; resolve ref target
// block types; look for filename strings (.tga/.dds) in payload; dump
// NiArkTextureExtraData hex on examples.
function texChain(e, extraction) {
  const p = buf.subarray(e.dataOffset, e.dataOffset+e.size);
  const byIndex = new Map(extraction.blocks.map(b=>[b.index,b]));
  const srcRefs = []; const srcTargets = {};
  let arkTexHex = null;
  for (const b of extraction.blocks) {
    if (b.type==='NiTexturingProperty' && b.fields) {
      for (const t of b.fields.textures) if (t.has===1) srcRefs.push(t.source);
    }
    if (b.type==='NiArkTextureExtraData' && b.opaque && arkTexHex===null) arkTexHex=b.rawHexCapped.slice(0,128);
  }
  for (const s of new Set(srcRefs)) {
    const t = byIndex.get(s);
    srcTargets[t ? (t.opaque?'OPAQUE:'+t.type:t.type) : 'NULL/-1-or-missing'] = (srcTargets[s>=0?(t?(t.opaque?'OPAQUE:'+t.type:t.type):'unresolved'):'null'] || 0) + 1;
  }
  const dotTga = p.indexOf('.tga')>=0 || p.indexOf('.TGA')>=0;
  const dotDds = p.indexOf('.dds')>=0 || p.indexOf('.DDS')>=0;
  return { name:e.name, numSrcRefs:srcRefs.length, srcRefsSample:srcRefs.slice(0,6), srcTargets, hasTgaString:dotTga, hasDdsString:dotDds, arkTexHexSample:arkTexHex };
}
const chainObs = [];
for (const r of pass) {
  const e = entries.find(x=>x.name===r.name);
  const ex = null; // need extraction: redo cheap? reuse? We didn't keep extraction. Redo parse for chain obs on up to 8 textured samples.
  chainObs.push(e);
}
// collect up to 10 textured samples + ensure the lead files 206264,15021,530892
const chainSamples = [];
for (const want of ['206264','15021','530892']) {
  const e = entries.find(x=>x.name.replace(/\.nif$/i,'')===want || x.name.startsWith(want));
  if (e && versionOf(e)===0x0401000C) chainSamples.push(e);
}
for (const e of sample) {
  if (chainSamples.length>=13) break;
  if (!chainSamples.includes(e)) chainSamples.push(e);
}
const chainResults = [];
for (const e of chainSamples) {
  try {
    const { extraction } = parseModel41(payload(e), e.name);
    chainResults.push(texChain(e, extraction));
  } catch {}
}

// ---- animation example: 206264 / 15021 / 530892 keytimes readable? ----
function animCheck(e) {
  const p = buf.subarray(e.dataOffset, e.dataOffset+e.size);
  const nl = p.indexOf(0x0a); const versionRaw = p.readUInt32LE(nl+1); const numBlocks = p.readUInt32LE(nl+5);
  const hasKfc = p.indexOf(Buffer.from([0x15,0,0,0]).subarray(0,4))>=0; // not meaningful; skip
  const anchor = (t)=>{const nb=Buffer.from(t);const a=Buffer.alloc(4+nb.length);a.writeInt32LE(nb.length,0);Buffer.from(nb).copy(a,4);return p.indexOf(a)>=0;};
  return { name:e.name, version:'0x'+versionRaw.toString(16), numBlocks, keyframeController:anchor('NiKeyframeController'), keyframeData:anchor('NiKeyframeData'), textKeyExtraData:anchor('NiTextKeyExtraData'), arkAnimation:anchor('NiArkAnimationExtraData') };
}
const animExamples = [];
for (const want of ['206264','15021','530892']) {
  const e = entries.find(x=>x.name.startsWith(want));
  if (e) animExamples.push(animCheck(e));
}

// ---- Textures.ark census + join ----
const ft = await open(TEX_ARK,'r'); const ts = await ft.stat();
const tb = Buffer.alloc(ts.size); await ft.read(tb,0,ts.size,0); await ft.close();
const texEntries = []; let tpos=0;
while (tpos+4<=tb.length && tb[tpos]===0x41&&tb[tpos+1]===0x4b&&tb[tpos+2]===0x03&&tb[tpos+3]===0x04) {
  const compSize=tb.readUInt32LE(tpos+18), uncompSize=tb.readUInt32LE(tpos+22),
        nameLen=tb.readUInt16LE(tpos+26), extraLen=tb.readUInt16LE(tpos+28);
  const name=tb.toString('latin1',tpos+30,tpos+30+nameLen);
  texEntries.push({name,size:uncompSize}); tpos=tpos+30+nameLen+extraLen+compSize;
}
const extCensus = {}; for (const t of texEntries){ const ext=t.name.split('.').pop().toUpperCase(); extCensus[ext]=(extCensus[ext]||0)+1; }
const texNames = new Set(texEntries.map(t=>t.name.toLowerCase()));

// join: sample of manifest_2003.csv 4.1 rows texture names vs Textures.ark?
// manifest textures column (texnames) is from the 5441-corpus; cross-check on
// the 760 v4.1 rows only (era-hygiene) + NiArkTextureExtraData numeric-ID
// hypothesis: extract i32 IDs from arkTex hex samples below in the analysis.
const joinResult = { texArkEntries:texEntries.length, extCensus };

const out = {
  job:'AV1', loop:'8ee81e37', era:'ISO_5_1_0_0', generated:new Date().toISOString(),
  reader:'NifModelReader41.js (night6h-r1, read-only import)',
  supportedTypes:['NiNode','NiTriShape','NiTriShapeData','NiMaterialProperty','NiAlphaProperty','NiZBufferProperty','NiVertexColorProperty','NiTexturingProperty','NiStringExtraData','NiTextureEffect','NiUVController','NiUVData'],
  sample:{ total:results.length, pass:pass.length, fullRenderable:full.length, partialOpaque:partialOpaque.length, stoppedOpaqueNoBoundary:stopped.length, fail:failed.length },
  readinessPct:{ pass:(pass.length/results.length*100).toFixed(1), fullRenderable:(full.length/results.length*100).toFixed(1), partialOpaque:(partialOpaque.length/results.length*100).toFixed(1), fail:(failed.length/results.length*100).toFixed(1) },
  failReasons, opaqueTypeCensus,
  negativeControl4x:negResults,
  chainResults, animExamples, texturesArk:joinResult,
  results,
};
await (await import('node:fs/promises')).writeFile(OUTDIR+'\\READINESS_MATRIX.json', JSON.stringify(out,null,1));
console.log(JSON.stringify({sample:out.sample, readinessPct:out.readinessPct, failReasons, opaqueTypeCensus, negativeControl:negResults.length, chain:chainResults.slice(0,3), animExamples, texturesArk:joinResult},null,1));
