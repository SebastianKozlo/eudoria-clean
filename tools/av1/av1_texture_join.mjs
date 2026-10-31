// av1_texture_join.mjs — JOB AV-1 task 3: NiArkTextureExtraData string census
// (corpus-wide, from raw bytes) and join against Textures.ark entry names.
import { open } from 'node:fs/promises';

const ARK='D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Models.ark';
const TEX='D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Textures.ark';
const OUT='D:\\Eudoria_Reconstruction\\99_Audits\\PE_ISO_ASSET_VIEWER_R1_20261031\\AV1_CENSUS\\TEXTURE_JOIN.json';

const fh=await open(ARK,'r'); const st=await fh.stat();
const buf=Buffer.alloc(st.size); await fh.read(buf,0,st.size,0); await fh.close();
const entries=[];
{ let pos=0;
  while (pos+4<=buf.length && buf[pos]===0x41&&buf[pos+1]===0x4b&&buf[pos+2]===0x03&&buf[pos+3]===0x04) {
    const compSize=buf.readUInt32LE(pos+18), nameLen=buf.readUInt16LE(pos+26), extraLen=buf.readUInt16LE(pos+28);
    entries.push({name:buf.toString('latin1',pos+30,pos+30+nameLen),dataOffset:pos+30+nameLen+extraLen,size:buf.readUInt32LE(pos+22)});
    pos=pos+30+nameLen+extraLen+compSize;
  } }

const ANCHOR=Buffer.alloc(4+21); ANCHOR.writeInt32LE(21,0); Buffer.from('NiArkTextureExtraData').copy(ANCHOR,4);

// extract candidate sized-strings in the 256B window after each anchor.
// OBSERVED structure (samples 16424/246842): ... i32s ... <len u32><name bytes> [00]
const nameCount=new Map(); const filesUsing=new Map();
const variantFieldA={}, variantFieldC={};
let anchorsTotal=0, filesWithAnchor=0, filesWithTexname=0;
for (const e of entries) {
  const p=buf.subarray(e.dataOffset,e.dataOffset+e.size);
  const vnl=p.indexOf(0x0a); const ver=p.readUInt32LE(vnl+1);
  if (ver!==0x0401000C) continue;
  let pos=0, had=false, hadTex=false;
  while (true) {
    const i=p.indexOf(ANCHOR,pos); if (i<0) break;
    anchorsTotal++; had=true;
    const fA=p.readInt32LE(i+25), fB=p.readInt32LE(i+29), fC=p.readInt32LE(i+33), fD=p.readInt32LE(i+37);
    const key=fA+'/'+fC+'/'+fD; variantFieldA[key]=(variantFieldA[key]||0)+1;
    // scan window for sized strings
    for (let w=i+21; w<Math.min(i+21+300,p.length-4); w++) {
      const len=p.readInt32LE(w);
      if (len>=4 && len<=64 && w+4+len<=p.length) {
        const s=p.toString('latin1',w+4,w+4+len);
        let ok=s.length>0; for (let c=0;c<s.length;c++){const ch=s.charCodeAt(c); if(ch<33||ch>126){ok=false;break;}}
        if (ok && /[a-z]/i.test(s)) {
          // texture-name filter: exclude RTTI noise (types of FOLLOWING blocks
          // caught by the 300B window) and morph labels; texnames OBSERVED end
          // with a slot suffix (_BASE/_DETAIL/_GLOW/_DECALn/_SPECULAR...).
          const isRtti = s.startsWith('Ni');
          const isMorph = s.startsWith('morph:');
          const looksTex = /_[A-Z0-9]+$/.test(s) && /[a-z]/.test(s) && !isRtti && !isMorph;
          if (looksTex) {
            nameCount.set(s,(nameCount.get(s)||0)+1);
            if (!filesUsing.has(s)) filesUsing.set(s,e.name);
            if (!hadTex) { hadTex=true; filesWithTexname++; }
          }
          w=w+4+len; // continue after this string (may be several)
        }
      }
    }
    pos=i+4;
  }
  if (had) filesWithAnchor++;
}
// Textures.ark
const ft=await open(TEX,'r'); const ts=await ft.stat();
const tb=Buffer.alloc(ts.size); await ft.read(tb,0,ts.size,0); await ft.close();
const texEntries=[]; { let pos=0;
  while (pos+4<=tb.length && tb[pos]===0x41&&tb[pos+1]===0x4b&&tb[pos+2]===0x03&&tb[pos]===0x03) break;
}
{ let pos=0;
  while (pos+4<=tb.length && tb[pos]===0x41&&tb[pos+1]===0x4b&&tb[pos+2]===0x03&&tb[pos+3]===0x04) {
    const compSize=tb.readUInt32LE(pos+18), nameLen=tb.readUInt16LE(pos+26), extraLen=tb.readUInt16LE(pos+28);
    texEntries.push(tb.toString('latin1',pos+30,pos+30+nameLen));
    pos=pos+30+nameLen+extraLen+compSize;
  } }
const texLower=new Set(texEntries.map(n=>n.toLowerCase()));
const texStem=new Set(); // numeric stems
const nonNumeric=[];
for (const n of texEntries) { const m=n.match(/^(\d+)\.[^.]+$/i); if(m) texStem.add(parseInt(m[1],10)); else nonNumeric.push(n); }
// join attempts
let resolveName=0, resolveTga=0, resolveDds=0, numericLike=0, unresolvable=0;
const unresSample=[];
for (const [s] of nameCount) {
  if (texLower.has(s.toLowerCase())) resolveName++;
  else if (texLower.has((s+'.tga').toLowerCase())) resolveTga++;
  else if (texLower.has((s+'.dds').toLowerCase())) resolveDds++;
  else {
    unresolvable++;
    if (unresSample.length<40) unresSample.push(s);
  }
  if (/^\d+$/.test(s)) numericLike++;
}
const out={
  job:'AV1',loop:'8ee81e37',era:'ISO_5_1_0_0',generated:new Date().toISOString(),
  anchorsTotal, filesWithAnchor4v1:filesWithAnchor, filesWithTexname,
  uniqueStrings:nameCount.size,
  variantSignatureCensus:variantFieldA,
  join:{
    resolveExactEntryName:resolveName, resolvePlusTga:resolveTga, resolvePlusDds:resolveDds,
    unresolvable:unresolvable, numericLikeStrings:numericLike,
    unresolvableSample:unresSample,
  },
  texturesArk:{ entries:texEntries.length, allNumericStemNames:texStem.size===texEntries.length, nonNumericNames:nonNumeric.slice(0,10), nonNumericCount:nonNumeric.length },
  topNames:[...nameCount.entries()].sort((a,b)=>b[1]-a[1]).slice(0,40),
};
await (await import('node:fs/promises')).writeFile(OUT,JSON.stringify(out,null,1));
console.log(JSON.stringify({anchorsTotal,filesWithAnchor,unique:nameCount.size,variant:variantFieldA,join:out.join,texArk:out.texturesArk,top:[...nameCount.entries()].sort((a,b)=>b[1]-a[1]).slice(0,10)},null,1));
