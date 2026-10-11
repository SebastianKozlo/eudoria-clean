#!/usr/bin/env node
// pcg935_png_decode.mjs — PRIVATE: minimal PNG decoder for screenshot pixel
// census (RGBA8, color types 0/2/6, filters 0-4). Returns {width,height,rgba}.
'use strict';
import fs from 'node:fs';
import zlib from 'node:zlib';

export function decodePng(buf) {
  if (buf.length < 8 || buf[0] !== 0x89 || buf[1] !== 0x50) throw new Error('not a PNG');
  let pos = 8;
  let width = 0; let height = 0; let bitDepth = 0; let colorType = 0;
  const idatChunks = [];
  while (pos < buf.length) {
    const len = buf.readUInt32BE(pos);
    const type = buf.toString('ascii', pos + 4, pos + 8);
    const data = buf.subarray(pos + 8, pos + 8 + len);
    if (type === 'IHDR') {
      width = data.readUInt32BE(0);
      height = data.readUInt32BE(4);
      bitDepth = data[8];
      colorType = data[9];
      if (bitDepth !== 8) throw new Error(`bit depth ${bitDepth} unsupported`);
      if (colorType !== 6 && colorType !== 2 && colorType !== 0) throw new Error(`color type ${colorType} unsupported`);
    } else if (type === 'IDAT') idatChunks.push(data);
    else if (type === 'IEND') break;
    pos += 12 + len;
  }
  const raw = zlib.inflateSync(Buffer.concat(idatChunks));
  const channels = colorType === 6 ? 4 : colorType === 2 ? 3 : 1;
  const stride = width * channels;
  const out = Buffer.alloc(width * height * 4);
  let prev = Buffer.alloc(stride);
  let src = 0;
  for (let y = 0; y < height; y++) {
    const filter = raw[src++];
    const line = raw.subarray(src, src + stride);
    src += stride;
    const cur = Buffer.alloc(stride);
    for (let x = 0; x < stride; x++) {
      const a = x >= channels ? cur[x - channels] : 0;
      const b = prev[x];
      const c = x >= channels ? prev[x - channels] : 0;
      let v = line[x];
      if (filter === 1) v = (v + a) & 0xff;
      else if (filter === 2) v = (v + b) & 0xff;
      else if (filter === 3) v = (v + ((a + b) >> 1)) & 0xff;
      else if (filter === 4) {
        const p = a + b - c;
        const pa = Math.abs(p - a); const pb = Math.abs(p - b); const pc = Math.abs(p - c);
        const pred = pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
        v = (v + pred) & 0xff;
      }
      cur[x] = v;
    }
    prev = cur;
    for (let x = 0; x < width; x++) {
      const o = (y * width + x) * 4;
      if (colorType === 6) {
        out[o] = cur[x * 4]; out[o + 1] = cur[x * 4 + 1]; out[o + 2] = cur[x * 4 + 2]; out[o + 3] = cur[x * 4 + 3];
      } else if (colorType === 2) {
        out[o] = cur[x * 3]; out[o + 1] = cur[x * 3 + 1]; out[o + 2] = cur[x * 3 + 2]; out[o + 3] = 255;
      } else {
        out[o] = out[o + 1] = out[o + 2] = cur[x]; out[o + 3] = 255;
      }
    }
  }
  return { width, height, rgba: new Uint8Array(out) };
}

if (process.argv[2]) {
  const img = decodePng(fs.readFileSync(process.argv[2]));
  let lit = 0;
  for (let i = 0; i < img.rgba.length; i += 4) {
    const r = img.rgba[i]; const g = img.rgba[i + 1]; const b = img.rgba[i + 2];
    if (!(Math.abs(r - 0x10) < 6 && Math.abs(g - 0x14) < 6 && Math.abs(b - 0x18) < 6)) lit++;
  }
  console.log(JSON.stringify({ w: img.width, h: img.height, litPixels: lit, total: img.width * img.height }));
}
