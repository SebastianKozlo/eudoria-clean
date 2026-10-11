import test from 'node:test';
import assert from 'node:assert/strict';
import os from 'node:os';
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const tool=path.join(path.dirname(fileURLToPath(import.meta.url)),'..','placement_probe.mjs');
function records(){const b=Buffer.alloc(16+32*96,255);for(let i=0;i<96;i++){const base=16+i*32;b.writeUInt16LE(i%2?4058:4057,base);b.writeFloatLE(i*4+2,base+4);b.writeFloatLE(400+i*2,base+8);b.writeFloatLE(i*3-10,base+12);}return b;}
function bntFixture(data){const name=Buffer.from('sample.rec\n'),dir=Buffer.alloc(4+name.length+16),footer=Buffer.alloc(8);dir.writeUInt32LE(1,0);name.copy(dir,4);dir.writeUInt32LE(data.length,4+name.length);dir.writeUInt32LE(0,4+name.length+4);footer.writeUInt32LE(data.length,0);footer.write('BNT2',4);return Buffer.concat([data,dir,footer]);}
function arkFixture(data){const name=Buffer.from('sample.rec'),local=Buffer.alloc(30),eocd=Buffer.alloc(22);local.write('AK\x03\x04','latin1');local.writeUInt32LE(0,4);local.writeUInt16LE(0,8);local.writeUInt32LE(data.length,18);local.writeUInt32LE(data.length,22);local.writeUInt16LE(name.length,26);eocd.write('AK\x05\x06','latin1');eocd.writeUInt16LE(1,8);eocd.writeUInt16LE(1,10);eocd.writeUInt32LE(local.length+name.length+data.length,16);return Buffer.concat([local,name,data,eocd]);}
const shimBnt=`export class Bnt2Archive { constructor(b){this.b=b;this.d=b.readUInt32LE(b.length-8);if(b.toString('ascii',b.length-4)!=='BNT2')throw Error('BAD_MAGIC');} entries(){let p=this.d+4,n=this.b.readUInt32LE(this.d),out=[];for(let i=0;i<n;i++){let end=this.b.indexOf(10,p),name=this.b.toString('ascii',p,end);p=end+1;out.push({entryIndex:i,name,size:this.b.readUInt32LE(p),offset:this.b.readUInt32LE(p+4)});p+=16;}if(p!==this.b.length-8)throw Error('BAD_INDEX');return out;} readEntry(e){return {payload:this.b.subarray(e.offset,e.offset+e.size)}}}`;
const shimArk=`export class ArkArchive {constructor(b){this.b=b;if(b.toString('latin1',b.length-22,b.length-18)!=='AK\\x05\\x06')throw Error('BAD_EOCD');}entries(){let p=0,out=[];while(this.b.toString('latin1',p,p+4)==='AK\\x03\\x04'){let comp=this.b.readUInt32LE(p+18),size=this.b.readUInt32LE(p+22),nl=this.b.readUInt16LE(p+26),e=this.b.readUInt16LE(p+28),name=this.b.toString('ascii',p+30,p+30+nl),dataOffset=p+30+nl+e;out.push({entryIndex:out.length,name,size,compSize:comp,compression:this.b.readUInt16LE(p+8),dataOffset});p=dataOffset+comp;}return out;}readEntry(e){if(e.compression!==0)throw Error('UNSUPPORTED');return {payload:this.b.subarray(e.dataOffset,e.dataOffset+e.size)}}}`;
test('CLI probes RAW, BNT2, Ark payload via locally imported compatible readers',()=>{
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'pe-probe-'));
 try{
  const repo=path.join(root,'repo'),out=path.join(root,'out');fs.mkdirSync(path.join(repo,'src/pesource'),{recursive:true});
  fs.writeFileSync(path.join(repo,'package.json'),'{"type":"module"}');
  fs.writeFileSync(path.join(repo,'src/pesource/Bnt2Archive.js'),shimBnt);
  fs.writeFileSync(path.join(repo,'src/pesource/ArkArchive.js'),shimArk);
  const raw=records();const inputFiles=['raw.vfs','test.bnt','test.ark'];
  for(const [n,data] of [['raw.vfs',raw],['test.bnt',bntFixture(raw)],['test.ark',arkFixture(raw)]])fs.writeFileSync(path.join(root,n),data);
  const ids=path.join(root,'ids.json');fs.writeFileSync(ids,JSON.stringify({S_tpl:[4057,4058],S_model:[218757]}));
  const args=['--repo',repo,'--ids',ids,'--out',out,...inputFiles.flatMap(n=>['--input',path.join(root,n)]),'--max-stride','64','--min-id-rate','0.5'];
  const res=spawnSync(process.execPath,[tool,...args],{encoding:'utf8'});
  assert.equal(res.status,0,`stdout=${res.stdout}\nstderr=${res.stderr}`);
  const sources=JSON.parse(fs.readFileSync(path.join(out,'sources.json'))),summary=JSON.parse(fs.readFileSync(path.join(out,'SUMMARY.json')));
  assert.equal(sources.length,3);assert.equal(summary.sourceCount,3);assert.ok(summary.candidateCount>=3);
  const candidates=fs.readFileSync(path.join(out,'placement_candidates.csv'),'utf8');
  assert.match(candidates,/test\.bnt/);assert.match(candidates,/test\.ark/);assert.match(candidates,/raw\.vfs/);
  assert.match(candidates,/CANDIDATE_ONLY_NOT_PLACEMENT_PROOF/);
 }finally{fs.rmSync(root,{recursive:true,force:true});}
});
