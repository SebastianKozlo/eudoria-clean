// av1_crosscheck_anim.mjs — manifest cross-check (100 overlapping v4.1 files)
// + NiKeyframeData keytime readability observation on 206264.nif.
import fs from 'node:fs';

// ---- manifest cross-check ----
const manLines = fs.readFileSync('D:/Eudoria_Reconstruction/12_WebGame/pe-world-launcher-r1/docs/nif/corpus/manifest_2003.csv','utf8').split('\n');
const hdr = manLines[0].split(',');
const iKf = hdr.indexOf('keyframe_controllers'), iHist = hdr.indexOf('block_histogram');
// CSV parse honoring quoted fields
function parseCsv(line) {
  const out=[]; let cur='', inQ=false;
  for (let i=0;i<line.length;i++){
    const c=line[i];
    if (inQ) { if (c==='"') { if (line[i+1]==='"'){cur+='"';i++;} else inQ=false; } else cur+=c; }
    else { if (c==='"') inQ=true; else if (c===',') { out.push(cur);cur=''; } else cur+=c; }
  }
  out.push(cur); return out;
}
const man = new Map();
for (const line of manLines.slice(1)) { if (!line.trim()) continue; const c=parseCsv(line); if (c[0]) man.set(c[0], c); }
const cens = JSON.parse(fs.readFileSync('D:/Eudoria_Reconstruction/99_Audits/PE_ISO_ASSET_VIEWER_R1_20261031/AV1_CENSUS/MODELS_CENSUS.json','utf8'));
let checked=0, kfAgree=0, histAgree=0, texAgree=0;
for (const e of cens.entries) {
  if (checked>=100) break;
  if (e.version!=='4.1.0.12') continue;
  const c = man.get(e.name); if (!c) continue;
  checked++;
  if (parseInt(c[iKf]||'0') === (e.anchoredBlockCount['NiKeyframeController']||0)) kfAgree++;
  try {
    const hist = JSON.parse(c[iHist]);
    let agree=true;
    for (const [t,n2] of Object.entries(e.anchoredBlockCount)) if ((hist[t]||0)!==n2) agree=false;
    if (agree) histAgree++;
  } catch {}
  if (histAgree+kfAgree>0) {} // noop
}
console.log(JSON.stringify({crossChecked:checked, kfControllerAgree:kfAgree, blockHistogramAgree:histAgree}));

// ---- keyframe readability: 206264.nif NiKeyframeData + NiArkAnimationExtraData ----
const b = fs.readFileSync('D:/Eudoria_Reconstruction/01_Original_Files/ARK/Models.ark');
let pos=0,n=0,target=null;
while (n<2500 && pos+4<=b.length && b[pos]===0x41&&b[pos+1]===0x4b) {
  const cs=b.readUInt32LE(pos+18),nl=b.readUInt16LE(pos+26),el=b.readUInt16LE(pos+28);
  const name=b.toString('latin1',pos+30,pos+30+nl),doff=pos+30+nl+el;
  if (name==='206264.nif') target={p:b.subarray(doff,doff+b.readUInt32LE(pos+22))};
  pos=doff+cs;n++;
}
const p=target.p;
function anchored(type){const nb=Buffer.from(type);const a=Buffer.alloc(4+nb.length);a.writeInt32LE(nb.length,0);nb.copy(a,4);return p.indexOf(a);}
const ikd=anchored('NiKeyframeData');
console.log('206264 NiKeyframeData @',ikd,'payload hex[0:48]:',p.subarray(ikd+18,ikd+18+48).toString('hex'));
// v4 NiKeyframeData starts: numRotationKeys u32 + rotationType u32 + keys...
const numRotKeys=p.readUInt32LE(ikd+18), rotType=p.readUInt32LE(ikd+22);
console.log('numRotationKeys',numRotKeys,'rotationType',rotType);
// first rotation key (QUADRATIC type 2: time,fwd,bwd? rotation keys are quats — variant; dump)
let q=ikd+26;
console.log('first key hex:',p.subarray(q,q+28).toString('hex'));
// count NiKeyframeController occurrences
let cnt=0,pp=0; const kc=Buffer.alloc(4+21);kc.writeInt32LE(21,0);Buffer.from('NiKeyframeController').copy(kc,4);
while(true){const i=p.indexOf(kc,pp);if(i<0)break;cnt++;pp=i+4;}
console.log('206264 NiKeyframeController count',cnt);
const iaa=anchored('NiArkAnimationExtraData');
console.log('206264 NiArkAnimationExtraData @',iaa,'hex[0:48]:',p.subarray(iaa+27,iaa+27+48).toString('hex'));
