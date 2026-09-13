// Independent Desktop audit. Originals and existing reports are read-only.
// Node built-ins only; no target execution, Ghidra, or imported executor parser.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
const output=path.dirname(fileURLToPath(import.meta.url));
const repo=process.env.EU935_AUDIT_REPO || 'D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean';
const game=process.env.EU935_AUDIT_GAME || 'D:/Eudoria_Reconstruction/pcg_install';
const audits=path.join(repo,'docs/audits');
const runs={join:'PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913',instance:'PE_935_STATIC_INSTANCE_TRACE_R1_20260913',source:'PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913',round:'PE_935_STATIC_PLACEMENT_ROUND1_20260913'};
const sha=b=>crypto.createHash('sha256').update(b).digest('hex').toUpperCase();
const json=p=>JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,''));
const hx=n=>'0x'+n.toString(16).toUpperCase().padStart(8,'0');
const result={generatedAt:new Date().toISOString(),scriptSHA256:sha(fs.readFileSync(fileURLToPath(import.meta.url))),scope:'Independent file/byte checks; not target runtime, not a full disassembly',inputs:[],checks:{}};
// Trust this explicitly selected repository for read-only Git commands, without persistent config changes.
const git=(...args)=>execFileSync('git',['-c','safe.directory='+repo,...args],{cwd:repo,encoding:'utf8',windowsHide:true});
result.snapshot={head:git('rev-parse','HEAD').trim(),status:git('status','--short').trim(),rangeCount:+git('rev-list','--count','7053654..2a2ba8d'),commits:git('log','--format=%h %ad','--date=iso-strict','7053654..2a2ba8d').trim().split('\n'),delta:git('diff','--shortstat','7053654..2a2ba8d').trim()};
assert.equal(result.snapshot.head,'2a2ba8ddc864d16b0b31e6ef7928e0e2af922633');
function readInput(relative,expected){const p=path.join(game,relative),b=fs.readFileSync(p),hash=sha(b);result.inputs.push({path:p,size:b.length,sha256:hash});if(expected)assert.equal(hash,expected);return b;}
const exe=readInput('Entropia.exe','E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31');
const vfs=readInput('Data/Parameters/templates.vfs','BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77');
const models=readInput('Data/Models/Models.bnt','C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0');
const volumes=readInput('Data/Volumes/Volumes.bnt','6AD8BA3C5AD6F7534F91C1956A0E36485A49BBEF3FFA918CBDDC0C68EDBABC09');
const portals=readInput('Data/Portals/Portals.bnt');
const crcTable=Array.from({length:256},(_,x)=>{for(let k=0;k<8;k++)x=x&1?(x>>>1)^0xEDB88320:x>>>1;return x>>>0;});
function crc32(b){let c=0xFFFFFFFF;for(const v of b)c=(c>>>8)^crcTable[(c^v)&255];return (c^0xFFFFFFFF)>>>0;}
assert.equal(crc32(Buffer.from('123456789')),0xCBF43926);
function bnt(b){assert.equal(b.subarray(-4).toString(),'BNT2');let index=b.readUInt32LE(b.length-8),n=b.readUInt32LE(index),p=index+4;const entries=[];for(let k=0;k<n;k++){const e=b.indexOf(10,p);assert(e>=p&&e+17<=b.length-8);const name=b.subarray(p,e).toString('ascii'),size=b.readUInt32LE(e+1),offset=b.readUInt32LE(e+5),crc=b.readUInt32LE(e+9);assert(offset+size<=index);entries.push({name,size,offset,crc});p=e+17;}assert.equal(p,b.length-8);assert.equal(new Set(entries.map(x=>x.name)).size,n);return {index,count:n,entries};}
const m=bnt(models),b=bnt(volumes),p=bnt(portals);
assert.equal(vfs.subarray(0,8).toString(),'ArkVFS02');const block=vfs.readUInt32LE(8);assert.equal(block,36);
let cursor=16,crcFailures=0;const records=[];
while(cursor<vfs.length){assert(cursor+16<=vfs.length);const id=vfs.readUInt32LE(cursor),size=vfs.readUInt32LE(cursor+4),crc=vfs.readUInt32LE(cursor+12),start=cursor+16;assert(size>=28&&start+size<=vfs.length);const payload=vfs.subarray(start,start+size);if(crc32(payload)!==crc)crcFailures++;assert.equal(payload.readUInt32LE(0),id);records.push({offset:cursor,id,A:payload.readUInt32LE(4),B:payload.readUInt32LE(8),C:payload.readUInt32LE(12)});cursor+=Math.ceil((16+size)/block)*block;}
assert.equal(cursor,vfs.length);assert.equal(crcFailures,0);
const aSet=new Set(records.map(x=>x.A).filter(Boolean)),bSet=new Set(records.map(x=>x.B).filter(Boolean)),mNames=new Set(m.entries.map(x=>x.name)),bNames=new Set(b.entries.map(x=>x.name));
const missingA=[...aSet].filter(x=>!mNames.has(x+'.nif')),missingB=[...bSet].filter(x=>!bNames.has(x+'.bvi'));
result.checks.join={block,records:records.length,crcFailures,uniqueA:aSet.size,uniqueB:bSet.size,zeroB:records.filter(x=>!x.B).length,models:m.count,volumes:b.count,missingA,missingB,unreferencedModels:m.count-aSet.size,unreferencedVolumes:b.count-bSet.size,modelCorpusCoveragePercent:100*aSet.size/m.count,anchors:records.filter(x=>[4508,4752,2249].includes(x.id)),negative:{AasBvi:bNames.has('296445.bvi'),BasNif:mNames.has('296446.nif'),nonexistent:mNames.has('999999999.nif')}};
const record4508=records.find(x=>x.id===4508);result.checks.join.template4508D={fileOffset:record4508.offset+32,rawBits:hx(vfs.readUInt32LE(record4508.offset+32)),float32:vfs.readFloatLE(record4508.offset+32),semanticRole:'UNKNOWN; an actual template value does not type every +0x10 getter receiver.'};
assert.equal(records.length,5438);assert.equal(aSet.size,3618);assert.equal(bSet.size,1666);assert.equal(missingA.length+missingB.length,0);
const anchors=[4508,4752,2249,296445,126740,278453,296446,20005,20006,20007,0xB9,0x6A4,0x6A8];
function pattern(n){const r=Buffer.alloc(4);r.writeUInt32LE(n);return r;}
function occurrences(buf,pat){const arr=[];let i=-1;while((i=buf.indexOf(pat,i+1))>=0)arr.push(i);return arr;}
const counts=Object.fromEntries(anchors.map(a=>[a,0]));let crcPRT=0;for(const e of p.entries){const payload=portals.subarray(e.offset,e.offset+e.size);if(crc32(payload)!==e.crc)crcPRT++;for(const a of anchors)counts[a]+=occurrences(payload,pattern(a)).length;}
result.checks.portals={entries:p.count,index:p.index,totalPayloadBytes:p.entries.reduce((s,e)=>s+e.size,0),uniqueNames:new Set(p.entries.map(x=>x.name)).size,crcFailures:crcPRT,window:p.entries.filter(e=>+e.name.split('.')[0]>=505000&&+e.name.split('.')[0]<=510000).map(e=>e.name).sort(),anchorCountsAllByteOffsets:counts,interpretation:'Only absence of these 13 raw LE32 values; no exclusion of indirect/compressed/differently encoded placement.'};
assert.equal(p.count,276);assert.equal(Object.values(counts).reduce((a,b)=>a+b),0);
const pe=exe.readUInt32LE(0x3c);assert.equal(exe.subarray(pe,pe+4).toString('hex'),'50450000');const opt=pe+24;assert.equal(exe.readUInt16LE(opt),0x10B);const base=exe.readUInt32LE(opt+28),secStart=opt+exe.readUInt16LE(pe+20),sections=[];
for(let i=0;i<exe.readUInt16LE(pe+6);i++){let s=secStart+i*40;sections.push({name:exe.subarray(s,s+8).toString().replace(/\0.*$/,''),virtualSize:exe.readUInt32LE(s+8),rva:exe.readUInt32LE(s+12),size:exe.readUInt32LE(s+16),raw:exe.readUInt32LE(s+20)});}
function off(va){const rva=va-base,s=sections.find(s=>rva>=s.rva&&rva<s.rva+s.size);assert(s,'VA not backed by file '+hx(va));return s.raw+rva-s.rva;}
function bytes(va,len){return exe.subarray(off(va),off(va)+len);}
function u32(va){return bytes(va,4).readUInt32LE();}
function cstring(va){const o=off(va);return exe.subarray(o,exe.indexOf(0,o)).toString();}
const evidence=json(path.join(audits,runs.source,'01_RAW/S14_VA_EVIDENCE.json')).evidence;
result.checks.vaEvidence={count:evidence.length,mismatches:evidence.filter(e=>off(Number(e.va))!==e.file_offset||bytes(Number(e.va),e.raw_bytes_hex.length/2).toString('hex')!==e.raw_bytes_hex.toLowerCase())};assert.equal(result.checks.vaEvidence.mismatches.length,0);
const t=sections.find(s=>s.name==='.text'),text=exe.subarray(t.raw,t.raw+t.size),tbase=base+t.rva;
function calls(target){const found=[];for(let i=0;i<=text.length-5;i++){if(text[i]===0xE8&&tbase+i+5+text.readInt32LE(i+1)===target)found.push(tbase+i);}return found;}
const callTargets={lookup:0x72F580,pump:0x6C9700,attributeSetter:0x845F70,positionSetter:0x730F90,rotationSetter:0x730FB0,extraSetter:0x730FD0,recordInit:0x730F60,recordCtor:0x730700,execute:0x4B2950,genericPlus8Getter:0x7CE1E0};
result.checks.callCandidates={method:'Raw E8 rel32 scan, NOT independently decoded instruction boundaries for all hits',targets:Object.fromEntries(Object.entries(callTargets).map(([k,v])=>[k,{target:hx(v),count:calls(v).length,sites:calls(v).map(hx)}]))};
const originalCallers=json(path.join(audits,runs.source,'01_RAW/ghidra_output/ZS3_CALLERS.json')).callers;
const key=Object.keys(originalCallers).find(k=>k.includes('00845f70'));
result.checks.callCandidates.attributeSetterRegistryAgreement=key?JSON.stringify(originalCallers[key].map(x=>x.from_va.toUpperCase()).sort())===JSON.stringify(calls(0x845F70).map(hx).map(x=>x.toUpperCase()).sort()):null;
result.checks.immediatePatterns=Object.fromEntries([4508,296445,20006].map(n=>[n,{LE:occurrences(text,pattern(n)).map(x=>hx(tbase+x)),BE:occurrences(text,Buffer.from(pattern(n)).reverse()).map(x=>hx(tbase+x))}]));
const vft=0xA86850,col=u32(vft-4),td=u32(col+12);
result.checks.receiverCounterexample={classVtable:hx(vft),COL:hx(col),typeDescriptor:hx(td),RTTI:cstring(td+8),factorySlot1:hx(u32(vft+4)),classCtorWrite:{va:hx(0x70CFB6),bytes:bytes(0x70CFB6,24).toString('hex')},getter:{va:hx(0x7CE1E0),bytes:bytes(0x7CE1E0,4).toString('hex')},objectCtor:{va:hx(0x726E9A),bytes:bytes(0x726E9A,41).toString('hex')},factoryBody:{va:hx(0x70BF50),bytes:bytes(0x70BF50,115).toString('hex')},interpretation:'ArkObjectClass virtual factory 0070BF50 passes its this as first argument to ArkObject ctor 00726E70. Shared getter +8 is not proof of templates.vfs field A.'};
assert.equal(cstring(td+8),'.?AVArkObjectClass@@');assert.equal(u32(vft+4),0x70BF50);assert.equal(bytes(0x7CE1E0,4).toString('hex'),'8b4108c3');
const slot=bytes(0x4B1B3C+(0xB9-0xA2),1)[0],dest=u32(0x4B1AE4+4*slot);const callSite=0x4B1A16;assert.equal(bytes(callSite,1)[0],0xE8);
result.checks.dispatchB9={slot,destination:hx(dest),callSite:hx(callSite),callTarget:hx(callSite+5+bytes(callSite+1,4).readInt32LE()),limit:'Dispatch edge only; producer and full message grammar not established by this probe.'};
result.checks.typos={vftAtPlusC:bytes(0x6FA8BC,7).toString('hex'),vftAtPlusD:bytes(0x6FA8BD,6).toString('hex'),model296445LE:pattern(296445).toString('hex')};
result.checks.fieldDSelector={regionVA:hx(0x8557D0),regionBytes:bytes(0x8557D0,0x64).toString('hex'),callsInRegion:calls(0x7CE1E0).filter(x=>x>=0x8557D0&&x<0x855834).map(hx),actualGetterOffset:8,claimedGetterOffset:16,interpretation:'The variant switch in 008553D0 calls the +8 getter, not +10. No template-record receiver provenance supplied.'};
result.checks.parameters={names:fs.readdirSync(path.join(game,'Data/Parameters')).filter(x=>x.toLowerCase().endsWith('.vfs')).sort(),limit:'File inventory, not a census of format families or semantic contents.'};
// Independent sanity counterexample to the logic "an attribute call => every transform originates in attributes".
// A fully valid x86 instruction sequence reads attributes, discards EAX, then supplies independent position.
let syn=Buffer.alloc(16,0x90),synVA=0x1000;syn[0]=0xE8;syn.writeInt32LE(0x846840-(synVA+5),1);syn[5]=0x68;syn.writeUInt32LE(0x2000,6);syn[10]=0xE8;syn.writeInt32LE(0x730F90-(synVA+15),11);syn[15]=0xC3;
result.checks.predicateCounterexample={bytes:syn.toString('hex'),attributeCallPresent:true,positionSetterCallPresent:true,transformSource:'independent pointer 0x2000; attribute result unused',type:'Logical counterexample to presence-only predicate, not a claim this exact snippet occurs in EU935.'};
function csvRows(file){const lines=fs.readFileSync(file,'utf8').replace(/^\uFEFF/,'').trim().split(/\r?\n/);const parse=line=>{const a=[];let x='',q=false;for(let i=0;i<line.length;i++){const ch=line[i];if(ch==='"'){if(q&&line[i+1]==='"'){x+='"';i++;}else q=!q;}else if(ch===','&&!q){a.push(x);x='';}else x+=ch;}a.push(x);return a;};const h=parse(lines.shift());return lines.filter(Boolean).map(l=>({...Object.fromEntries(parse(l).map((v,i)=>[h[i],v])),__cells:parse(l)}));}
result.checks.manifests=[];
for(const [name,rel,root] of [['round','MANIFEST_SHA256.csv',audits],['source','03_EVIDENCE/MANIFEST_SHA256.csv',path.join(audits,runs.source)],['instance','03_EVIDENCE/MANIFEST_SHA256.csv',path.join(audits,runs.instance)]]){
 const file=path.join(audits,runs[name],rel);if(!fs.existsSync(file)){result.checks.manifests.push({name,status:'MISSING_MANIFEST'});continue;}
 const rows=csvRows(file),mismatches=[],missing=[];let checked=0,comments=0,references=0;for(const row of rows){let r=row.relative_path||row.path,expected=row.sha256||row.SHA256;if(r.startsWith('#')){comments++;continue;}if(r==='REFERENCE-RUN-MANIFEST'){r=row.__cells[1];expected=row.__cells[2];references++;}const f=r==='AUDIT_ENTRYPOINT.md'?path.join(repo,r):path.resolve(root,r.replaceAll('\\','/'));assert(f.startsWith(path.resolve(repo)+path.sep));if(!fs.existsSync(f)){missing.push(r);continue;}checked++;const hash=sha(fs.readFileSync(f));if(hash!==expected.toUpperCase())mismatches.push({path:r,actual:hash,expected});}
 result.checks.manifests.push({name,rows:rows.length,checked,comments,references,missing,mismatches});
}
result.checks.manifestInterpretation={note:'Round manifest has 45 file rows, 4 reference rows with a third column and 4 comments; AUDIT_ENTRYPOINT is relative to repo root. Historical per-run hashes are overridden for amended files by the round manifest, which verifies. Initial generic CSV interpretation was corrected before this final execution.'};
result.selfCheck={tooling:'An intermediate run failed on Git ownership checks before byte verification; corrected with command-scoped safe.directory for the explicitly selected read-only repo. No persistent Git config changes. Final artifacts come from this completed execution.'};
fs.writeFileSync(path.join(output,'probe.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({inputs:result.inputs,join:result.checks.join,portals:result.checks.portals,VA:result.checks.vaEvidence,calls:Object.fromEntries(Object.entries(result.checks.callCandidates.targets).map(([k,v])=>[k,v.count])),receiver:result.checks.receiverCounterexample,dispatch:result.checks.dispatchB9,parameters:result.checks.parameters.names.length,manifests:result.checks.manifests},null,2));
