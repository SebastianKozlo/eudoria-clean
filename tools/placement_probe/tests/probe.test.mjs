import test from 'node:test';
import assert from 'node:assert/strict';
import {analyzeBlob} from '../placement_probe.mjs';

function records({count=80,header=16,stride=32,poison=false}={}) {
  const b=Buffer.alloc(header+count*stride,0xff);
  for(let i=0;i<count;i++){
    const x=header+i*stride,id=i%2===0?4057:4058;
    b.writeUInt16LE(poison?49281:id,x);
    b.writeFloatLE(i*11.5+2,x+4);b.writeFloatLE(1000+i*2.1,x+8);b.writeFloatLE(i*4.5-80,x+12);
    b.writeFloatLE(0.5+(i%10)*0.15,x+16);b.writeFloatLE(1,x+20);
  }
  return b;
}
const sets={S_tpl:new Set([4057,4058]),S_model:new Set([218757])};
const config={minIdRate:0.5,maxStride:128,minPosRate:0.9,minDistinctId:2,top:50};

test('discovers known synthetic record layout without treating it as historical placement',()=>{
  const z=analyzeBlob(records(),sets,config);
  const c=z.candidates.find(x=>x.header===16&&x.stride===32&&x.idOffset===0&&x.idWidth===2&&x.xyzOffset===4&&x.idSetName==='S_tpl');
  assert.ok(c, 'positive synthetic record candidate must be present');
  assert.equal(c.rowCount,80);assert.equal(c.idRate,1);assert.equal(c.idDistinct,2);
  assert.equal(c.controls.permutationMembershipInvariant,true);
  assert.equal(c.controls.idShuffleMembershipRate,1);
  assert.equal(c.controls.independentAnchorJoint,null);
});
test('wrong IDs do not manufacture a template relation',()=>{
  const z=analyzeBlob(records({poison:true}),sets,config);
  assert.equal(z.candidates.filter(x=>x.idSetName==='S_tpl').length,0);
});
test('no file/geometry source is inferred from a matching ID alone',()=>{
  const b=Buffer.alloc(16+80*32);for(let i=0;i<80;i++){b.writeUInt16LE(i%2?4057:4058,16+i*32);} 
  const z=analyzeBlob(b,sets,config);
  assert.equal(z.candidates.length,0);
});
test('missing template set is a hard error',()=>{
  assert.throws(()=>analyzeBlob(records(),{S_tpl:new Set()},config),/template ID set required/);
});
test('truncated buffers and zero-row cases do not fabricate a pass',()=>{
  assert.equal(analyzeBlob(Buffer.alloc(7),sets,config).candidates.length,0);
});
test('independent aligned anchors enable a joint label-position permutation control',()=>{
  const b=records();
  const z=analyzeBlob(b,sets,{...config,anchors:[{definitionId:4057,position:[2,1000,-80],tolerance:0.01}]});
  const c=z.candidates.find(x=>x.header===16&&x.stride===32&&x.xyzOffset===4&&x.idOffset===0&&x.idWidth===2);
  assert.ok(c);assert.equal(c.controls.independentAnchorJoint.close,1);
  assert.equal(c.controls.permutationMembershipInvariant,true);
  assert.equal(c.controls.idShuffleMembershipRate,1);
});
