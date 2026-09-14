import fs from 'node:fs';
import assert from 'node:assert/strict';
export const exe=fs.readFileSync('D:/Eudoria_Reconstruction/pcg_install/Entropia.exe');
const pe=exe.readUInt32LE(0x3c),opt=pe+24;
export const base=exe.readUInt32LE(opt+28),sections=[];
for(let i=0;i<exe.readUInt16LE(pe+6);i++){let p=opt+exe.readUInt16LE(pe+20)+i*40;sections.push({name:exe.subarray(p,p+8).toString().replace(/\0.*$/,''),rva:exe.readUInt32LE(p+12),size:exe.readUInt32LE(p+16),raw:exe.readUInt32LE(p+20)});}
export const hx=n=>'0x'+n.toString(16).toUpperCase().padStart(8,'0');
export function off(va){const s=sections.find(s=>va-base>=s.rva&&va-base<s.rva+s.size);assert(s,hx(va));return s.raw+va-base-s.rva;}
export const bytes=(va,len)=>exe.subarray(off(va),off(va)+len);
export const u32=va=>bytes(va,4).readUInt32LE();
export function cstring(va){let o=off(va);return exe.subarray(o,exe.indexOf(0,o)).toString();}
export function dump(va,len){return Array.from({length:Math.ceil(len/16)},(_,i)=>hx(va+i*16)+' '+bytes(va+i*16,Math.min(16,len-i*16)).toString('hex').match(/../g).join(' ')).join('\n');}
export function calls(target,opcode=0xe8){const s=sections.find(s=>s.name==='.text'),b=exe.subarray(s.raw,s.raw+s.size),r=[];for(let i=0;i<=b.length-5;i++)if(b[i]===opcode&&base+s.rva+i+5+b.readInt32LE(i+1)===target)r.push(base+s.rva+i);return r;}
export function target(va){assert([0xe8,0xe9].includes(bytes(va,1)[0]));return va+5+bytes(va+1,4).readInt32LE();}
