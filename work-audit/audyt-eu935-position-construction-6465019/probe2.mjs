// WORK-AUDIT probe2 — semantyka FUN_00746550/60/70 (F-a), piny D-3, importy IAT, region 0x00413340
import {bytes,u32,cstring,hx,dump,exe} from './pe.mjs';
const L=[];const log=s=>{L.push(s);console.log(s);};
log('=== FUN_00746550 ==='); log(dump(0x00746550,0x10));
log('=== FUN_00746560 ==='); log(dump(0x00746560,0x10));
log('=== FUN_00746570 ==='); log(dump(0x00746570,0x10));
log('=== FUN_004123D0 ==='); log(dump(0x004123D0,0x8));
log('=== D-3: epilogi FUN_007343E0 (0x00734590-0x007345BA) ==='); log(dump(0x00734590,0x2C));
log('=== import hint/names ==='); log('0x0076A9AE+2 = '+JSON.stringify(cstring(0x0076A9AE+2))); log('0x0076A9E2+2 = '+JSON.stringify(cstring(0x0076A9E2+2)));
log('=== region 0x00413340 (claim: nie jest startem funkcji) ==='); log(dump(0x00413330,0x40));
log('=== FUN_004154F0 head (lazy singleton 0x8C) ==='); log(dump(0x004154F0,0x30));
log('=== FUN_00855340: MOV [EBX+0x4C],EAX @0x0085536D? ==='); log(dump(0x00855340,0x50));
log('=== [mgr1+0x4C] writer census: 89/8B z disp 0x4C w okolicy 0x00855340 ===');
import fs from 'node:fs';
fs.writeFileSync('probe2.log',L.join('\n'));log('saved');
