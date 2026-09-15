// WORK-AUDIT probe3 — wlasny spacer PE import directory (IAT 0xA75064/0xA7506C), selektor FUN_008553D0, FUN_00934540, FUN_00934670, FUN_00755F90
import {bytes,u32,cstring,hx,dump,exe,base,sections,off} from './pe.mjs';
const L=[];const log=s=>{L.push(s);console.log(s);};
// PE import walk
const opt=exe.readUInt32LE(exe.readUInt32LE(0x3c)+24);
const ddir=opt+96+8*1; // DataDirectory[1] = Import Table
const impRva=exe.readUInt32LE(ddir), impSize=exe.readUInt32LE(ddir+4);
log('ImportTable RVA='+hx(base+impRva)+' size='+impSize);
const impOff=off(base+impRva);
let n=0;
for(let d=impOff;;d+=20){
  const of = u32(base+exe.readUInt32LE(d+12)+12); // OriginalFirstThunk -> hint/name rvas
  const nameRva=exe.readUInt32LE(d+12);
  const ftRva=exe.readUInt32LE(d+16);
  if(nameRva===0)break;
  const dll=cstring(base+nameRva); n++;
  if(/kernel32/i.test(dll)){
    log('DLL: '+dll+' FirstThunk VA='+hx(base+ftRva));
    for(let t=0;;t++){
      const val=exe.readUInt32LE(off(base+ftRva)+t*4);
      if(val===0)break;
      const va=base+ftRva+t*4;
      if(va===0xA75064||va===0xA7506C||(val>=0x0076A9A0&&val<=0x0076AA00)){
        const hn=base+val;
        log('  IAT '+hx(va)+' -> '+hx(val)+' hint='+exe.readUInt16LE(off(hn))+' name='+JSON.stringify(cstring(hn+2)));
      }
    }
  }
}
log('import descriptors: '+n);
log('=== FUN_008553D0 head (selektor — co czyta: +0x78?) ==='); log(dump(0x008553D0,0x60));
log('=== FUN_00934540 head (slot+4 MaTerrainManagerRuntime) ==='); log(dump(0x00934540,0x50));
log('=== FUN_00934670 (tag 0x6E?) ==='); log(dump(0x00934670,0x50));
log('=== FUN_00755F90 head (filter AABB) ==='); log(dump(0x00755F90,0x40));
import fs from 'node:fs';
fs.writeFileSync('probe3.log',L.join('\n'));log('saved');
