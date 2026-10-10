// QC12 — non-triviality check of MY fresh /catalog screenshot using the bounded
// png_nontrivial analyzer (my measurement: the fresh capture in QC11).
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { analyzePng } from '../../../../tools/pecompat/png_nontrivial.mjs';

const PKG = resolve(process.argv[2]);
const PNG = process.argv[3];
const buf = readFileSync(PNG);
const r = analyzePng(buf, { canvas: { x: 0, y: 0, width: 1280, height: 800 } });
const out = { qcStep: 'QC12_SCREENSHOT_NONTRIVIALITY', png: PNG, bytes: buf.length, analysis: r };
writeFileSync(join(PKG, '00_CONTROL_INTERNAL_QC', 'QC12_SCREENSHOT_NONTRIVIALITY.json'), JSON.stringify(out, null, 1));
console.log(JSON.stringify(r, null, 1).slice(0, 1500));
