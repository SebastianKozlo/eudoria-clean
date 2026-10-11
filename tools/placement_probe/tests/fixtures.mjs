// fixtures.mjs — PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011
// Synthetic byte builders shared by PRE (original R1 kit) and POST (corrected kit).
// PROVENANCE: authored in this correction run; 100% synthetic bytes; no proprietary
// game payloads. Provenance of every builder is asserted by the run package.
import { createHash } from 'node:crypto';
export const sha256 = b => createHash('sha256').update(b).digest('hex');

// --- record tables -----------------------------------------------------------
// §7 XYZ fixture: 80 rows, header=16, stride=32; u16 ID 4057/4058 at +0;
// f32 base value row*3+axis*100+1 at +4/+8/+12; 8 NaN per axis in rows 0..7/8..15/16..23.
export function xyzFixture80() {
  const rows = 80, header = 16, stride = 32;
  const b = Buffer.alloc(header + rows * stride, 0xff);
  for (let i = 0; i < rows; i++) {
    const x = header + i * stride;
    b.writeUInt16LE(i % 2 === 0 ? 4057 : 4058, x);
    for (let a = 0; a < 3; a++) {
      const nanRows = a === 0 ? [0, 7] : a === 1 ? [8, 15] : [16, 23];
      const isNan = i >= nanRows[0] && i <= nanRows[1];
      if (isNan) b.writeFloatLE(NaN, x + 4 + a * 4);
      else b.writeFloatLE(i * 3 + a * 100 + 1, x + 4 + a * 4);
    }
  }
  return b;
}

// Generic 80-row record table (original positive shape): ID 4057/4058 at +0,
// floats at +4/+8/+12 (+16/+20 filler floats).
export function records80() {
  const rows = 80, header = 16, stride = 32;
  const b = Buffer.alloc(header + rows * stride, 0xff);
  for (let i = 0; i < rows; i++) {
    const x = header + i * stride;
    b.writeUInt16LE(i % 2 === 0 ? 4057 : 4058, x);
    b.writeFloatLE(i * 11.5 + 2, x + 4); b.writeFloatLE(1000 + i * 2.1, x + 8); b.writeFloatLE(i * 4.5 - 80, x + 12);
    b.writeFloatLE(0.5 + (i % 10) * 0.15, x + 16); b.writeFloatLE(1, x + 20);
  }
  return b;
}

// §7 LAYOUT fixture: 10007 bytes of 0xFF (10007 is prime — no stride 12..512 divides it).
export function layoutBuffer10007() { return Buffer.alloc(10007, 0xff); }

// SAMPLE_VS_CENSUS fixture: 4800 rows, header 16, stride 32; 16+4800*32 = 153616 B.
// Only rows i%4===2 carry valid IDs (4057/4058); all other rows carry poison ID 49281.
// The original R1 sampler picks indices floor((j+0.5)*n/rows) = 4j+2 (i%4===2), so the
// 1200-row sample sees a 100% valid ID column while the whole table is 25% valid.
// XYZ floats are finite everywhere. By construction, sample != census.
export function poisoned4800() {
  const rows = 4800, header = 16, stride = 32;
  const b = Buffer.alloc(header + rows * stride, 0xff);
  for (let i = 0; i < rows; i++) {
    const x = header + i * stride;
    b.writeUInt16LE(i % 4 === 2 ? (i % 8 === 2 ? 4057 : 4058) : 49281, x);
    b.writeFloatLE(i * 0.25 + 1, x + 4); b.writeFloatLE(i * 0.5 - 20, x + 8); b.writeFloatLE(i * 0.125 + 3, x + 12);
  }
  return b;
}

// SINGLE_DEFINITION_TABLE: all rows carry the same ID 4057.
export function singleIdTable(count = 80) {
  const header = 16, stride = 32;
  const b = Buffer.alloc(header + count * stride, 0xff);
  for (let i = 0; i < count; i++) {
    const x = header + i * stride;
    b.writeUInt16LE(4057, x);
    b.writeFloatLE(i * 11.5 + 2, x + 4); b.writeFloatLE(1000 + i * 2.1, x + 8); b.writeFloatLE(i * 4.5 - 80, x + 12);
  }
  return b;
}

// INTEGER_COUNTERS_AS_FLOATS: u32 counters at +4/+8/+12 (i+1, 1000+i, 5000+i),
// which as f32 are subnormal (~1e-44..1e-41). ID 4057/4058 at +0.
export function countersAsFloats() {
  const rows = 80, header = 16, stride = 32;
  const b = Buffer.alloc(header + rows * stride, 0xff);
  for (let i = 0; i < rows; i++) {
    const x = header + i * stride;
    b.writeUInt16LE(i % 2 === 0 ? 4057 : 4058, x);
    b.writeUInt32LE(i + 1, x + 4); b.writeUInt32LE(1000 + i, x + 8); b.writeUInt32LE(5000 + i, x + 12);
  }
  return b;
}

// --- containers in the REAL adapter formats (src/pesource Bnt2Archive/ArkArchive) ---
export function realBnt2(entries) { // entries: [{name, data}]
  const dir = Buffer.alloc(4), parts = [];
  let offset = 0; const dirEntries = [];
  for (const e of entries) { parts.push(e.data); dirEntries.push({ name: e.name, size: e.data.length, offset }); offset += e.data.length; }
  const dirStart = offset;
  let dirBuf = Buffer.alloc(4);
  dirBuf.writeUInt32LE(entries.length, 0);
  for (const e of dirEntries) {
    const nb = Buffer.from(e.name + '\n', 'ascii');
    const meta = Buffer.alloc(16);
    meta.writeUInt32LE(e.size, 0); meta.writeUInt32LE(e.offset, 4);
    dirBuf = Buffer.concat([dirBuf, nb, meta]);
  }
  const footer = Buffer.alloc(8);
  footer.writeUInt32LE(dirStart, 0); footer.write('BNT2', 4, 'ascii');
  return Buffer.concat([...parts, dirBuf, footer]);
}

export function realArk(entries) { // STORED entries only
  const parts = [];
  for (const e of entries) {
    const name = Buffer.from(e.name, 'ascii');
    const lh = Buffer.alloc(30);
    lh.write('AK\x03\x04', 0, 'latin1');
    lh.writeUInt16LE(0, 6);  // flags
    lh.writeUInt16LE(0, 8);  // compression STORED
    lh.writeUInt32LE(0, 14); // crc32 (not checked by reader)
    lh.writeUInt32LE(e.data.length, 18); // compSize
    lh.writeUInt32LE(e.data.length, 22); // uncompSize
    lh.writeUInt16LE(name.length, 26); lh.writeUInt16LE(0, 28); // extraLen
    parts.push(lh, name, e.data);
  }
  const dataLen = parts.reduce((a, p) => a + p.length, 0);
  const eocd = Buffer.alloc(22);
  eocd.write('AK\x05\x06', 0, 'latin1');
  eocd.writeUInt32LE(0, 4);
  eocd.writeUInt16LE(entries.length, 8); eocd.writeUInt16LE(entries.length, 10);
  eocd.writeUInt32LE(0, 12); eocd.writeUInt32LE(0, 16);
  return Buffer.concat([...parts, eocd]);
}

// --- shim adapters (the ORIGINAL kit tests' placeholder readers; NOT the
// actual-project-adapter test) — kept for census mechanics cases --------------
export const shimBntSrc = `export class Bnt2Archive { constructor(b){this.b=b;this.d=b.readUInt32LE(b.length-8);if(b.toString('ascii',b.length-4)!=='BNT2')throw Error('BAD_MAGIC');} entries(){let p=this.d+4,n=this.b.readUInt32LE(this.d),out=[];for(let i=0;i<n;i++){let end=this.b.indexOf(10,p),name=this.b.toString('ascii',p,end);p=end+1;out.push({entryIndex:i,name,size:this.b.readUInt32LE(p),offset:this.b.readUInt32LE(p+4)});p+=16;}if(p!==this.b.length-8)throw Error('BAD_INDEX');return out;} readEntry(e){return {payload:this.b.subarray(e.offset,e.offset+e.size)}}}`;
export const shimArkSrc = `export class ArkArchive {constructor(b){this.b=b;if(b.toString('latin1',b.length-22,b.length-18)!=='AK\\\\x05\\\\x06')throw Error('BAD_EOCD');}entries(){let p=0,out=[];while(this.b.toString('latin1',p,p+4)==='AK\\\\x03\\\\x04'){let comp=this.b.readUInt32LE(p+18),size=this.b.readUInt32LE(p+22),nl=this.b.readUInt16LE(p+26),e=this.b.readUInt16LE(p+28),name=this.b.toString('ascii',p+30,p+30+nl),dataOffset=p+30+nl+e;out.push({entryIndex:out.length,name,size,compSize:comp,compression:this.b.readUInt16LE(p+8),dataOffset});p=dataOffset+comp;}return out;}readEntry(e){if(e.compression!==0)throw Error('UNSUPPORTED');return {payload:this.b.subarray(e.dataOffset,e.dataOffset+e.size)}}}`;

// --- ids_from_export inputs --------------------------------------------------
export const idsCsv = (colName = 'templateId') =>
  'rowId,' + colName + '\n' + Array.from({ length: 4 }, (_, i) => `${i + 1},${4057 + i}`).join('\n') + '\n';
// POST-only small multi-ID table (8 rows, header 16, stride 32; 272 B) for the
// SYNTHETIC_INPUTS budget test — two distinct IDs so the default minDistinctId=2 gate passes.
export function recordsTwoIdSmall() {
  const rows = 8, header = 16, stride = 32;
  const b = Buffer.alloc(header + rows * stride, 0xff);
  for (let i = 0; i < rows; i++) {
    const x = header + i * stride;
    b.writeUInt16LE(i % 2 === 0 ? 4057 : 4058, x);
    b.writeFloatLE(i * 11.5 + 2, x + 4); b.writeFloatLE(1000 + i * 2.1, x + 8); b.writeFloatLE(i * 4.5 - 80, x + 12);
  }
  return b;
}

// POST-only headerless table (80 rows, header 0, stride 32; 2560 B) for the legal
// maxHeader=0 boundary positive control.
export function records80Headerless() {
  const rows = 80, stride = 32;
  const b = Buffer.alloc(rows * stride, 0xff);
  for (let i = 0; i < rows; i++) {
    const x = i * stride;
    b.writeUInt16LE(i % 2 === 0 ? 4057 : 4058, x);
    b.writeFloatLE(i * 11.5 + 2, x + 4); b.writeFloatLE(1000 + i * 2.1, x + 8); b.writeFloatLE(i * 4.5 - 80, x + 12);
  }
  return b;
}

// --- PA-1 regression fixtures (contract section F, byte-exact pinned builders) ---
// PA1-A: the EXACT original sparse builder from the pinned review_counterchecks.mjs
// (lines 54-60). 4800 rows, header 16, stride 32; only rows i=4j+2 (j=0..1199, the
// rows the 1200-row sampler picks) carry a valid u16 ID 4057/4058 and finite f32
// xyz (j*2 + k*100 at +4/+8/+12); everything else stays 0xFF. The original fixture
// does NOT have valid IDs everywhere: sample sees 100%, the whole table is 25%.
// Bytes=153616; SHA256=9AB2D32A1DE4DB50E0496F5364C1EE694A08D3D2B3B82A7E65B460EBB52681C7.
export function pa1A() {
  const b = Buffer.alloc(16 + 4800 * 32, 0xff);
  for (let j = 0; j < 1200; j++) {
    const i = Math.floor((j + 0.5) * 4800 / 1200);
    const p = 16 + i * 32;
    b.writeUInt16LE(j % 2 ? 4058 : 4057, p);
    [4, 8, 12].forEach((o, k) => b.writeFloatLE(j * 2 + k * 100, p + o));
  }
  return b;
}
// PA1-B: from A change ONLY the IDs of the unsampled rows (i%4 !== 2) to i%2?4058:4057,
// without touching XYZ. Sample XYZ stays 1.0, full XYZ stays 0.25, full ID becomes 1.0.
// SHA256=2E8520FF73690D5ED44026A568C9438CA4625ED85DA9A433169B1143B5153622.
export function pa1B() {
  const b = pa1A();
  for (let i = 0; i < 4800; i++) {
    if (i % 4 !== 2) b.writeUInt16LE(i % 2 ? 4058 : 4057, 16 + i * 32);
  }
  return b;
}
// PA1-C: from B change ONLY the unsampled f32 xyz (+4/+8/+12) to i*2 + k*100.
// Sample XYZ 1.0, full XYZ 1.0, full ID 1.0.
// SHA256=20258A0CD3D93B2FD2C496AAC32F1655E7A45768450177A3F6E764B2D7EA926B.
export function pa1C() {
  const b = pa1B();
  for (let i = 0; i < 4800; i++) {
    if (i % 4 !== 2) [4, 8, 12].forEach((o, k) => b.writeFloatLE(i * 2 + k * 100, 16 + i * 32 + o));
  }
  return b;
}
export const PA1_PINS = {
  A: { sizeBytes: 153616, sha256: '9AB2D32A1DE4DB50E0496F5364C1EE694A08D3D2B3B82A7E65B460EBB52681C7', SAMPLE_XYZ_FINITE_RATE: 1.0, FULL_XYZ_FINITE_RATE: 0.25, FULL_ID_HIT_RATE: 0.25 },
  B: { sizeBytes: 153616, sha256: '2E8520FF73690D5ED44026A568C9438CA4625ED85DA9A433169B1143B5153622', SAMPLE_XYZ_FINITE_RATE: 1.0, FULL_XYZ_FINITE_RATE: 0.25, FULL_ID_HIT_RATE: 1.0 },
  C: { sizeBytes: 153616, sha256: '20258A0CD3D93B2FD2C496AAC32F1655E7A45768450177A3F6E764B2D7EA926B', SAMPLE_XYZ_FINITE_RATE: 1.0, FULL_XYZ_FINITE_RATE: 1.0, FULL_ID_HIT_RATE: 1.0 },
};