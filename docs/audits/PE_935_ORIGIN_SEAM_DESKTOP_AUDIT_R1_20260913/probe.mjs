// Independent Desktop audit: Node built-ins; original EXE is never executed.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {exe,base,sections,hx,bytes,u32,cstring,dump,calls,target} from './pe.mjs';
const out=path.dirname(fileURLToPath(import.meta.url));
const repo='D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean';
const A='PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913';
const B='PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913';
const ap=path.join(repo,'docs/audits',A),bp=path.join(repo,'docs/audits',B);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex').toUpperCase();
const read=p=>fs.readFileSync(p,'utf8').replace(/^\uFEFF/,'');
const json=p=>JSON.parse(read(p));
const git=(...a)=>execFileSync('git',['-c','safe.directory='+repo,...a],{cwd:repo,windowsHide:true,encoding:'utf8',maxBuffer:20e6}).trim();
const r={timestamp:new Date().toISOString(),method:'Independent raw PE checks and bounded instruction decoding; raw E8/E9 scans are candidate counts, not complete instruction-boundary proofs.',scriptSHA256:sha(fs.readFileSync(fileURLToPath(import.meta.url))),helperSHA256:sha(fs.readFileSync(path.join(out,'pe.mjs'))),snapshot:{head:git('rev-parse','HEAD'),status:git('status','--short'),range:'24d7669..78cd153',diff:git('diff','--shortstat','24d7669..78cd153')}};
assert.equal(r.snapshot.head,'78cd1535e6a35330bde7460c24e98db272acdbd3');
assert.equal(sha(exe),'E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31');
r.inputs={exeSHA256:sha(exe),exeSize:exe.length,base:hx(base)};
const changed=git('diff','--name-only','24d7669..78cd153').split('\n');
r.persistence={changed:changed.length,outsideTwoPackages:changed.filter(p=>!p.startsWith('docs/audits/'+A+'/')&&!p.startsWith('docs/audits/'+B+'/')),commits:[]};
assert.deepEqual(r.persistence.outsideTwoPackages,['AUDIT_ENTRYPOINT.md']);
for(const c of ['5d0edde','78cd153'])r.persistence.commits.push({commit:git('rev-parse',c),paths:git('diff-tree','--no-commit-id','--name-only','-r',c).split('\n').length,entrypoint:git('diff',c+'^',c,'--numstat','--','AUDIT_ENTRYPOINT.md')});
// Every indexed payload is hashed independently. Metadata comments are not file rows.
r.manifests=[];
for(const [name,root,sep] of [[A,ap,','],[B,bp,'\t']]){let lines=read(path.join(root,'MANIFEST_SHA256.csv')).trim().split(/\r?\n/).slice(1),checked=0,errors=[];for(const l of lines){if(!l||l.startsWith('#'))continue;const v=l.split(sep),rel=sep===','?v[0]:v[1],expected=sep===','?v[1]:v[0];if(!/^[a-f\d]{64}$/i.test(expected)){errors.push({line:l,error:'unrecognized row'});continue;}const f=sep===','?path.join(repo,'docs/audits',rel):path.join(root,rel);try{const b=fs.readFileSync(f);checked++;if(sha(b)!==expected.toUpperCase())errors.push({rel,error:'HASH'});if(sep==='\t'&&b.length!==+v[2])errors.push({rel,error:'SIZE'});}catch(e){errors.push({rel,error:e.code});}}
r.manifests.push({name,checked,errors});assert.equal(errors.length,0);}
const classEvidence=json(path.join(ap,'03_EVIDENCE/QC_F1_CLASSID.json'));
const actualClassCalls=calls(0x70cf80);assert.deepEqual(actualClassCalls,[...classEvidence.registrations.map(x=>+x.call_site)].sort((a,b)=>a-b));
r.classRegistrations={rawCalls:actualClassCalls.length,immediates:[],lazy:[],mangling:[]};
for(const x of classEvidence.registrations){if(x.imm32_arg1===null){r.classRegistrations.lazy.push({call:x.call_site,context:dump(+x.call_site-16,21)});continue;}assert.equal(bytes(+x.push_at,1)[0],0x68);assert.equal(u32(+x.push_at+1),x.imm32_arg1);r.classRegistrations.immediates.push({call:x.call_site,push:x.push_at,id:u32(+x.push_at+1)});}
for(const x of classEvidence.correlation.filter(x=>x.impl_rtti)){const v=+x.impl_rtti.vtable,col=u32(v-4),td=u32(col+12),s=cstring(td+8),m=s.match(/\$0([A-P]+)@/);assert(m);const n=[...m[1]].reduce((n,c)=>16*n+c.charCodeAt(0)-65,0);assert.equal(n,x.imm32);assert.equal(s,x.impl_rtti.rtti);assert(bytes(+x.impl_rtti.at,12).includes(Buffer.from(U32(v))));r.classRegistrations.mangling.push({vtable:hx(v),td:hx(td),rtti:s,decoded:n});}
function U32(n){const b=Buffer.alloc(4);b.writeUInt32LE(n);return b;}
assert.equal(r.classRegistrations.immediates.length,54);assert.equal(r.classRegistrations.mangling.length,36);
r.rtti=[0xa86850,0xa91e4c,0xa7dcb0,0xa7c1fc].map(v=>{const col=u32(v-4),td=u32(col+12);return{vtable:hx(v),COL:hx(col),TD:hx(td),name:cstring(td+8),slot0:hx(u32(v)),slot1:hx(u32(v+4))};});
const targets={classCtor:0x70cf80,plus8:0x7ce1e0,plus10:0x48ada0,processor:0x4c47f0,creator:0x4c46c0,insert:0x856190,baseCtor:0x85b1b0,derivedCtor:0x528e50,recordCtor:0x730700,position:0x730f90,attributeWriter:0x845f70,keyProducer:0x457930,dispatcher:0x4b18d0,builder:0x567770,driver:0x567c50,auxiliaryDecoder:0x7343e0};
r.calls=Object.fromEntries(Object.entries(targets).map(([k,v])=>[k,{target:hx(v),E8:calls(v).map(hx),E9:calls(v,0xe9).map(hx)}]));
assert.equal(r.calls.plus8.E8.length,808);assert.equal(r.calls.plus8.E9.length,9);assert.equal(r.calls.plus10.E8.length,116);assert.equal(r.calls.plus10.E9.length,1);
assert.deepEqual(calls(0x4c47f0),[0x457594,0x4b0b47,0x4b171a,0x4b1dbc]);assert.deepEqual(calls(0x856190),[0x4c47da]);
r.dispatch=[0xb0,0xb2,0xb9,0xc6,0xc7].map(n=>{let s=bytes(0x4b1b3c+n-0xa2,1)[0];return{type:hx(n),slot:s,destination:hx(u32(0x4b1ae4+s*4))};});
r.dispatchCardinality={lowest:0xa2,highest:0xc7,inclusive:0xc7-0xa2+1,reportedHexCount:0x25};
// Recheck all printed bytes, including complete context rows beyond the declared pin length.
let pins=json(path.join(bp,'01_RAW/T6_BYTE_PINS.json')).pins,byteCount=0,pinErrors=[];
for(const [name,p] of Object.entries(pins)){for(const l of p.hexdump.split('\n')){const m=l.match(/^([a-f\d]{8})\s{2}((?:[a-f\d]{2} ){0,15}[a-f\d]{2})(?:\s{2}|$)/i);assert(m,'pin format '+name);const b=Buffer.from(m[2].replaceAll(' ',''),'hex');byteCount+=b.length;if(!bytes(parseInt(m[1],16),b.length).equals(b))pinErrors.push(name);}}
r.T6={pins:Object.keys(pins).length,printedBytes:byteCount,errors:pinErrors};assert.equal(pinErrors.length,0);
// F1: first argument ESI is cursor; second EDI is destination. Both returns MOV EAX,ESI.
const must=(va,hex)=>{assert.equal(bytes(va,hex.length/2).toString('hex'),hex);return{va:hx(va),hex};};
r.auxiliaryDecoder={start:hx(0x7343e0),endInclusive:hx(0x7345b9),pins:[must(0x7343e0,'53568b74240c'),must(0x734416,'8b7c2414'),must(0x73459b,'5f8bc65e5bc3'),must(0x7345b4,'5f8bc65e5bc3'),must(0x745414,'8d570c5255'),must(0x74541e,'8bf083c408')],returnValue:'same input cursor; no nested cursor allocation',destination:'rec+0x0C',writesRelativeToDestination:[0,8,12,16,20,24,28,32],untouchedRelativeSlot:4,remainingMaskAt:36,conditionalPairs:[{offset:0,zero:2,one:4},{offset:8,zero:8,one:16},{offset:12,zero:32,one:64},{offset:16,zero:128,one:256},{offset:20,zero:512,one:1024}],unconditionalFloatOffsets:[24,28,32],warning:'Field meanings and why offset +4 is omitted are not established; this is not yet a semantic transform decoder.'};
// Instruction-derived arithmetic witnesses ONLY. These do not execute the target or parse real packets.
function consumption(mask){let flags=mask&65535,bytes=14,values=[];for(const p of r.auxiliaryDecoder.conditionalPairs){if(flags&p.zero){flags&=~p.zero;values.push(0);}else if(flags&p.one){flags&=~p.one;values.push(1);}else{bytes+=4;values.push('read f32');}}return{mask:hx(mask),consumedBytes:bytes,residualMask:flags,conditionalValues:values};}
r.auxiliaryDecoder.syntheticWitnesses=[consumption(0),consumption(0x2aa),consumption(0x554),consumption(0x7fe)];
assert.equal(r.auxiliaryDecoder.syntheticWitnesses[0].consumedBytes,34);assert.equal(r.auxiliaryDecoder.syntheticWitnesses[1].consumedBytes,14);assert.equal(r.auxiliaryDecoder.syntheticWitnesses[3].residualMask,0x554);
r.positionAdjustment={pins:[must(0x4c4706,'8b4810'),must(0x4c4710,'894c2418'),must(0x4c473d,'83fe06'),must(0x4c4773,'d95c2444d9442418d9442444d8d1dfe0ddd9f6c4417506d95c2418')],helperCall:{va:hx(0x4c476e),target:hx(target(0x4c476e))},variants:[3,4,5,6,7],semantics:'For finite inputs: z_final=max(z_input,f32(helper(x,y,0,0))) in a local record copy before constructor. Caller record itself is not written back.',provider:'00853A80 uses mgr+0x4C and mgr+0 virtual slot 1; actual provider identities/terrain role remain UNKNOWN.',alreadyInExecutorAnalysis:'02_ANALYSIS/SEAM_FLOW_MAP.md section 3',missingInFinalSummary:true};
assert.equal(target(0x4c476e),0x853a80);assert.equal(target(0x4c47c1),0x528e50);
r.positionAdjustment.syntheticWitnesses=[[3,10,20,20],[3,30,20,30],[2,10,20,10]].map(([variant,zInput,helper,expected])=>{let zFinal=zInput;if([3,4,5,6,7].includes(variant)&&Math.fround(helper)>zInput)zFinal=Math.fround(helper);assert.equal(zFinal,expected);return{variant,zInput,helper,zFinal};});
r.existingPath={guard:{site:hx(0x4c4878),target:hx(target(0x4c4878))},positionUpdate:{site:hx(0x4c488a),target:hx(target(0x4c488a))},rotation:{site:hx(0x4c4896),target:hx(target(0x4c4896))},reportedWrongSite:hx(0x4c4875)};
assert.equal(target(0x4c488a),0x85b3e0);
// Original VFS independent count/CRC and actual numeric field. No importer/engine code reused.
const vf=fs.readFileSync('D:/Eudoria_Reconstruction/pcg_install/Data/Parameters/templates.vfs');assert.equal(sha(vf),'BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77');
const table=Array.from({length:256},(_,x)=>{for(let i=0;i<8;i++)x=x&1?(x>>>1)^0xedb88320:x>>>1;return x>>>0;});
function crc(b){let c=0xffffffff;for(const x of b)c=table[(c^x)&255]^(c>>>8);return(c^0xffffffff)>>>0;}
assert.equal(crc(Buffer.from('123456789')),0xcbf43926);let pos=16,n=0,bad=0,anchor;
assert.equal(vf.subarray(0,8).toString(),'ArkVFS02');assert.equal(vf.readUInt32LE(8),36);
while(pos<vf.length){let id=vf.readUInt32LE(pos),s=vf.readUInt32LE(pos+4);assert(pos+16+s<=vf.length);if(crc(vf.subarray(pos+16,pos+16+s))!==vf.readUInt32LE(pos+12))bad++;if(id===4508)anchor={id,offset:pos,A:vf.readUInt32LE(pos+20),D: vf.readFloatLE(pos+32),bits:hx(vf.readUInt32LE(pos+32)),semanticRole:'UNKNOWN'};pos+=36*Math.ceil((16+s)/36);n++;}
assert.equal(n,5438);assert.equal(bad,0);assert.equal(pos,vf.length);r.vfs={sha256:sha(vf),records:n,crcFailures:bad,eof:pos,anchor};
const regions=[[0x7343e0,0x210],[0x7453d0,0x150],[0x4c46c0,0x350],[0x853a80,0xe1],[0x70cfb6,0x18],[0x726e9a,0x29],[0x8557d0,0x64],[0x7262a0,0x25],[0x4c32f0,0x80]];
// Resolve scalar reader from actual CALL; avoid guessing helper addresses.
r.auxiliaryDecoder.scalarReader=hx(target(0x73443b));regions.pop();regions.push([target(0x73443b),0x70]);
fs.writeFileSync(path.join(out,'independent_hexdumps.txt'),regions.map(([va,n])=>dump(va,n)).join('\n\n')+'\n');
// Independently rehash the complete historical local corpus declared by GB6.
const historical=json(path.join(bp,'01_RAW/GB6_IMMUTABLE_CENSUS_after.json')).packages;
const before=json(path.join(bp,'01_RAW/GB6_IMMUTABLE_CENSUS_before.json')).packages;
const historicNames={RUN1_TEMPLATE_CONSUMER_TRACE:'PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912',RUN2_EXTERNAL_SOURCES_MATRIX:'PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913',RUN3_STATIC_INSTANCE_TRACE:'PE_935_STATIC_INSTANCE_TRACE_R1_20260913',RUN4_PLACEMENT_SOURCE_TRACE:'PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913',ROUND_CLOSURE:'PE_935_STATIC_PLACEMENT_ROUND1_20260913',JOIN_ERRATA_R2:'PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913',DESKTOP_AUDIT:'PE_935_STATIC_PLACEMENT_DESKTOP_AUDIT_R1_20260913',PKG_A_RECEIVER_PROVENANCE:A};
function walk(root,rel=''){let a=[];for(const e of fs.readdirSync(path.join(root,rel),{withFileTypes:true})){const p=rel?rel+'/'+e.name:e.name;if(e.isDirectory())a.push(...walk(root,p));else a.push(p);}return a.sort();}
r.historical=[];
for(const [name,h] of Object.entries(historical)){const root=path.join('D:/Eudoria_Reconstruction/99_Audits',historicNames[name]),actual=walk(root),expected=h.files.map(x=>x.path).sort(),errors=[];assert.deepEqual(actual,expected);assert.deepEqual(h,before[name]);for(const f of h.files){const b=fs.readFileSync(path.join(root,f.path));if(b.length!==f.size||sha(b)!==f.sha256.toUpperCase())errors.push(f.path);}r.historical.push({name,files:actual.length,beforeEqualsAfter:true,errors});assert.equal(errors.length,0);}
r.executionLimitations=['No client execution, Ghidra session, packet replay or full 0xC0 model trace.','Synthetic witnesses derive from inspected instructions and are not engine/runtime oracle results.','Historical rehash proves equality to saved snapshots, not that files were never temporarily modified between them.','Raw call enumeration is not by itself dataflow or a negative FILE/network proof.'];
r.selfCheck='Preparation runs stopped on several hand-transcribed instruction addresses (off by one); corrected against original bytes and E8 targets before the completed run. An earlier guessed evidence-directory path was corrected. No PASS artifact was emitted by failed runs.';
fs.writeFileSync(path.join(out,'probe.json'),JSON.stringify(r,null,2)+'\n');
console.log(JSON.stringify({snapshot:r.snapshot,persistence:r.persistence,manifests:r.manifests,registrations:{calls:actualClassCalls.length,imm:r.classRegistrations.immediates.length,mangling:r.classRegistrations.mangling.length},T6:r.T6,auxiliary:r.auxiliaryDecoder,adjustment:r.positionAdjustment,existing:r.existingPath,vfs:r.vfs},null,2));
