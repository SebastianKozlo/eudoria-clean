// WORK-AUDIT (audytor: Work-Audit, audyt: audyt-eu935-position-construction-6465019) — wlasna sonda bajtowa
// Weryfikuje nośne twierdzenia runu PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1 (commit 6465019)
// + trzy zarzuty przerwanej sesji Desktop (F-a: +0x78 vs +0x88/+0x8C; F-b: sloty vtable SF; F-c: interpretacja).
import {bytes,u32,cstring,hx,dump,calls,target,exe} from './pe.mjs';
const L=[];
const log=(...a)=>{L.push(a.join(' '));console.log(a.join(' '));};

// [V1] RTTI: vtable -> COL -> TD -> nazwa (wlasny chod)
function rtti(vt){const col=u32(vt-4),td=u32(col+12);return {vt:hx(vt),col:hx(col),td:hx(td),name:cstring(td+8)};}
log('=== V1 RTTI (wlasny spacer COL->TD->name) ===');
for(const v of [0x00A7F430,0x00A7F420,0x00A7BA54,0x00A7BA48,0x00A7D458,0x00A91E4C,0x00A7DCB0]) log(JSON.stringify(rtti(v)));

// [V2] vtable SceneFeederObject 0x00A7D458 — sloty +0..+0x1C (zarzut F-b)
log('=== V2 SF vtable slots ===');
for(let i=0;i<8;i++) log('slot+'+(i*4).toString(16).padStart(2,'0')+' = '+hx(u32(0x00A7D458+i*4)));

// [V3] x87 CREATE window 0x004C4770..0x479F (T-26: FSTP [ESP+0x18] @0x004C478A)
log('=== V3 CREATE x87 window ==='); log(dump(0x004C4770,0x30));

// [V4] EXISTING FUN_0085B3E0 — FSTP [ESP+0x24] @0x0085B439, JNE @0x0085B43F; step [0xA7AF80]
log('=== V4 EXISTING window + step const ==='); log(dump(0x0085B420,0x40)); log('step qword @0xA7AF80:'); log(dump(0xA7AF80,8));

// [V5] FUN_005094C0 — kopia [SF+0x34..0x3C] + flag +0x28=1
log('=== V5 FUN_005094C0 ==='); log(dump(0x005094C0,0x28));

// [V6] FUN_0085B1B0 — co pisze +0x78 / +0x88 / +0x8C? (zarzut F-a)
log('=== V6 FUN_0085B1B0 hexdump (0x0085B1B0..0x0085B3A0) ===');
for(let a=0x0085B1B0;a<0x0085B3A0;a+=0x30) log(dump(a,0x30));

// [V7] cell_id FUN_00936A60: SHL 0x10 / AND 0xFFFF / OR
log('=== V7 FUN_00936A60 window (szukam c1 e6 10 / 25 ff / 09) ===');
for(let a=0x00936A60;a<0x00936B60;a+=0x30) log(dump(a,0x30));

// [V8] FUN_00538B70: zapisy vtable 0x00A7F430/0x00A7F420 (piny 0x00538BA9/BAF, koniec BB5)
log('=== V8 FUN_00538B70 vtable writes ==='); log(dump(0x00538B90,0x30));

// [V9] thunke CS: FUN_00413440/FUN_00413450 + IAT 0xA75064/0xA7506C
log('=== V9 CS thunks + IAT ==='); log(dump(0x00413440,0x11)); log(dump(0x00413450,0x11)); log('IAT 0xA75064 = '+hx(u32(0xA75064))+' 0xA7506C = '+hx(u32(0xA7506C)));

// [V10] fallback constant 10.0f @0xA7B128 i -1000.0f @0xA7B270
log('=== V10 fallback consts ==='); log(dump(0xA7B128,4)); log(dump(0xA7B270,4));

// [V11] census: 15 call-site FUN_00853A80 (E8 aligned)
const c853a80=calls(0x00853A80);
log('=== V11 calls to FUN_00853A80: n='+c853a80.length+' ==='); log(c853a80.map(hx).join(' '));

// [V12] confirm FUN_00853A80 RET 0x10 (C2 10 00 na koncu) — window okolicy konca
log('=== V12 FUN_00853A80 tail ==='); log(dump(0x00853B40,0x25));

// [V13] Z2 slot5: vtable MovableObject 0x00A91E4C slot +0x14 = FUN_0085B010?
log('=== V13 MovableObject vtable slot+0x14 ==='); log('slot+0x14 = '+hx(u32(0x00A91E4C+0x14)));

fs: {
const fs=await import('node:fs');
fs.writeFileSync('probe1.log',L.join('\n'));
log('saved probe1.log, lines='+L.length);
}
