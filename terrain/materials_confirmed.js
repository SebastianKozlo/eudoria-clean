// materials_confirmed.js — M1 ITER 044 / ledger ITER_030 (P0d WIRING)
// THE CONFIRMED 9.3.5 TERRAIN MATERIAL ARCHITECTURE, rendered through the
// clean pipeline for the proven region — with EXPLICIT era-bounded
// placeholders for the PATCHER-delivered inputs (labeled, NO fake truth),
// and a version-labeled side-by-side comparison vs the NAIVE page model
// (terrain/materials_wsum.js, the ITER_025/026 top-3-raw-mask model).
//
// CONFIRMED ARCHITECTURE (this iteration's consolidated spec,
// docs/forensics/iter030-material-pipeline-consolidation.md):
//   BASE   = CPU bake (FUN_0093eb50/FUN_00939c40) painting per-pixel from
//            the climate PALETTE: row = the ALTITUDE axis
//            (255*(1-(h-2)/512-noise2), clamped 0..254), col = the weight
//            axis (63*(noise1+accumulated roughness), clamped 0..62);
//            A=255. NOT a TDF material, NOT a per-tile file texture.
//   FACTOR = (S/4)x(S/4) ONE-HOT channel by the palette-ALPHA 3-band
//            partition (>=73 R, 53..73 G, <53 B; thresholds from the
//            binary _DAT_00a97c90/c98). NO normalization.
//   DETAILS= 3 slots from the 129x129 world-data selectors via tables
//            C/D/E (FUN_00938da0 -> FUN_00939900) — the SELECTORS are
//            PATCHER-DELIVERED and MISSING locally.
//   SHADER = Terrain_14 (0x3EA): D = d0*w0+d1*w1+d2*w2 (unrenormalized);
//            per-channel OVERLAY onto base keyed on D; SHADOW = the base
//            ALPHA modulation (mul r0, r0, r0.a); details repeat 32/32/16.
//
// ERA-BOUNDED PLACEHOLDERS (every one labeled; the MISSING inputs are
// PATCHER-delivered — iter029's 178-container negative; NO proxy is
// claimed as historical truth):
//   [P1] CLIMATE BYTE (65x65 grid, id 432502): MISSING -> constant byte 0
//        -> the engine's own table A[0] = palette 0x66DC6 (Textures.bnt
//        entry 421318.dat, LOCAL, fetched + provenance-carried at runtime).
//        The engine's own default for unmapped bytes is 0x66DC7 (table
//        A[17..255]); we choose A[0] because region A is mountainous and
//        0x66DC6's altitude structure (green lowland -> dark rock
//        highland) matches the region type. DOCUMENTED CHOICE.
//   [P2] DETAIL SELECTORS (129x129, id 459344): MISSING -> constant
//        selector byte 0 -> the engine's own table entries C[0]=D[0]=
//        0x70027 (458791) and E[0]=0x70028 (458792) — REAL era detail
//        textures from the local Textures.bnt. DOCUMENTED CHOICE.
//   [P3] THE LEAF TREE (ArkHeightTree midpoint-displacement recursion):
//        the leaf heights -> the direct GLOBAL-FIELD bilinear sample
//        (FUN_00947a40 semantics: (pos-origin)>>9, stride 0x101,
//        1/256 fractions), clamped [-20,+512]. The global field IS the
//        leaves' data source (iter028); the tree's Brownian refinement
//        is dropped (its input is the same field + noise). DOCUMENTED
//        SIMPLIFICATION of a CONFIRMED input chain.
//   [P4] THE NOISE TABLES t1/t2 (mgr+0x1864/0x2864): the engine builds
//        them per-session from its runtime RNG (FUN_00405920, a Java-LCG
//        0x5DEECE66D multiplier + 0xB increment, seeded at engine init).
//        Since iter036 (ledger ITER_036, THE FLOAT-CONSTANT LOCK SWEEP) the
//        page implements the engine arithmetic BYTE-EXACTLY: the constants
//        are the BINARY f64 slots (float32-literal widenings: 0.4/0.2/0.01/
//        0.005 as float32-then-widened, NOT the JS decimal literals), the
//        DRAW is the engine's exact construction ((state & 0xFFFFFFFFFFFF)
//        / 2^48, FUN_00405920's exponent stitch - 1.0), and the f32
//        rounding points (FSTP dword at the draw/product/accumulator/final
//        division) are replicated with Math.fround (FUN_0093cbf0
//        @0x0093CDC0..0x0093CE5C, 9 rounding points). The per-session SEED
//        remains the single era-bounded placeholder (runtime state,
//        unknowable from static data). DOCUMENTED DETERMINISM CHOICE.
//   [P5] THE ACCUMULATED LEAF ROUGHNESS (FUN_00991880's 12-slot slope
//        formula over the quadtree leaves): evaluated at the FACTOR-cell
//        scale (2-unit blocks) directly from the global field with the
//        CONFIRMED formula ((|d1|+|d2|)/sqrt(2) + 0.5*(|e1|+|e2|)) /
//        (4*size). DOCUMENTED SCALE SIMPLIFICATION.
//   NOT placeholder (LOCAL data): the tile heights (TDF, geometry), the
//   palette, the details, the global height field (id 429259), the
//   Terrain_14 ops (byte-extracted), the sampler states (iter024).
//
// COMPARISON: per tile TWO models side by side — LEFT = v_naive (the
// materials_wsum C1-raw model: base = the first TDF material texture,
// factor = the raw top-3 TDF mask weights), RIGHT = v_confirmed (this
// page's palette bake). Same tiles, same geometry, same renderer;
// per-model deterministic render hashes.

import * as THREE from 'three';
import { PESourceMount } from '../src/pesource/PESourceMount.js';
import { ERAS } from '../src/pesource/PEProvenance.js';
import { PETerrainRegion, PE_TERRAIN_METER_PER_SAMPLE, worldHeightMeters } from '../src/peworld/PETerrainCore.js';
import { decodeTga2, decodeTga2A32 } from '../src/pesource/TgaDecoder.js';

const HUD = document.getElementById('hud');
const log = (m) => { HUD.textContent = m; console.log(m); };

// ---------- browser I/O adapter (same chain as materials_wsum) ----------
async function fetchBytes(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`fetch ${url}: HTTP ${res.status}`);
  return new Uint8Array(await res.arrayBuffer());
}
async function strictInflate(zlibBytes) {
  const ds = new DecompressionStream('deflate');
  const stream = new Blob([zlibBytes]).stream().pipeThrough(ds);
  return new Uint8Array(await new Response(stream).arrayBuffer());
}
async function sha256Hex(bytes) {
  const d = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();
}
const io = { readFile: fetchBytes, inflate: strictInflate, sha256: sha256Hex };

// ---------- the era's RNG (Java-LCG, FUN_004058a0/00405920 semantics) ----------
// state * 0x5DEECE66D + 0xB (mod 2^64). THE DRAW (iter036 byte-lock,
// FUN_00405920 @0x00405930..0x0040595b): the engine packs the f64 with the
// exponent stitch (OR 0x3ff0000; <<4) whose mantissa = the LOW 48 BITS of
// the state shifted left 4, then FSUB qword [0x00a79818] (= 1.0 f64):
// draw = (1 + low48/2^48) - 1.0 = low48 / 2^48 EXACTLY (Sterbenz).
// The prior (state >> 11)/2^53 variant was a [P4] stand-in - SUPERSEDED.
// [P4]: FIXED SEED (the engine seeds per-session; the construction is exact).
const RNG_MUL = 0x5DEECE66Dn;
const RNG_ADD = 0xBn;
const RNG_MOD = 1n << 64n;
const DRAW_TWO48 = 281474976710656.0;   // 2^48
class EngineRng {
  constructor(seed = 0n) { this.s = seed & (RNG_MOD - 1n); }
  next() {
    this.s = (this.s * RNG_MUL + RNG_ADD) % RNG_MOD;
    // FUN_00405920: mantissa = (state & 0xFFFFFFFFFFFF) << 4; value = 1+m/2^52 - 1.0
    return Number(this.s & 0xFFFFFFFFFFFFn) / DRAW_TWO48;
  }
}

// ---------- the manager noise tables (FUN_0093cbf0 ctor semantics) ----------
// BYTE-LOCKED (iter036, ledger ITER_036): the constants are the BINARY f64
// QWORD slots - the FLOAT32-LITERAL WIDENINGS (the exact binary values, NOT
// the JS decimal literals which differ in the 8th+ significant digit):
const NOISE_C04   = 0.4000000059604644775390625;      // _DAT_00a7b308 FMUL qword @0x0093cde6
const NOISE_C02   = 0.20000000298023223876953125;     // _DAT_00a7b2d0 FSUB qword @0x0093cdf1
const NOISE_C001  = 0.00999999977648258209228515625;  // _DAT_00a7b360 FMUL qword @0x0093ce13
const NOISE_C0005 = 0.004999999888241291046142578125; // _DAT_00a81d18 FSUB qword @0x0093ce19
const NOISE_DIV20 = 20.0;                              // _DAT_00a7b9e0 (FDIV/FLD qword @0x0093ce4b)
// The engine's f32 rounding points (FSTP dword): the draw (P1/P4), the
// product (P2/P5), the accumulator (P3/P6), and the final division store
// (P8/P9) - all replicated with Math.fround (the 80-bit intermediates are
// exact in f64 here: the operands are <=48 significant bits).
function buildNoiseTables(rng) {
  const t1 = new Float32Array(1024);
  const t2 = new Float32Array(1024);
  for (let i = 0; i < 1024; i++) {
    let a = 0.0, b = 0.0;
    for (let k = 0; k < 20; k++) {
      const d1 = Math.fround(rng.next());            // P1: FSTP dword [ESP+0x1c] @0x0093cddc
      const p1 = Math.fround(d1 * NOISE_C04 - NOISE_C02);   // P2: FSTP dword [ESP+0x20] @0x0093cdf7
      a = Math.fround(a + p1);                        // P3: FSTP dword [EDI] @0x0093ce01
      const d2 = Math.fround(rng.next());            // P4: FSTP dword [ESP+0x1c] @0x0093ce0b
      const p2 = Math.fround(d2 * NOISE_C001 - NOISE_C0005); // P5: FSTP dword [ESP+0x1c] @0x0093ce1f
      b = Math.fround(b + p2);                       // P6: FSTP dword [ESP+0x1c] @0x0093ce2d (+P7 identity)
    }
    t1[i] = Math.fround(a / NOISE_DIV20);             // P8: FDIV qword + FSTP dword [EDI-0x4] @0x0093ce55
    t2[i] = Math.fround(b / NOISE_DIV20);             // P9: FDIVR + FSTP dword [EDI+0xffc] @0x0093ce5c
  }
  return { t1, t2 };
}

// ---------- mounts (SHA-pinned, era-labeled) ----------
const mount = new PESourceMount(io);
log('mounting PCG_9_3_5 terrain.bnt + Textures.bnt…');
await mount.mountEra({ era: ERAS.PCG_9_3_5, container: 'Terrain/terrain.bnt',
  path: '/pcg/Data/Terrain/terrain.bnt', format: 'BNT2_TERRAIN', verifyHash: true });
await mount.mountEra({ era: ERAS.PCG_9_3_5, container: 'Textures.bnt',
  path: '/pcg/Data/Textures/Textures.bnt', format: 'BNT2', verifyHash: true });
log('mounted + SHA-verified (terrain 95841761…, textures 61ACD13B…).');

// ---------- the proven 9-tile region A (mountains: palette 0x66DC6 fits) ----------
const ORIGIN_X = 56, ORIGIN_Y = 112, N = 3;
const TILE_WORLD = 128;          // 32 samples * 4 m (PE meters) = 128 units
const tiles = [];
for (let ty = ORIGIN_Y; ty < ORIGIN_Y + N; ty++) {
  const row = [];
  for (let tx = ORIGIN_X; tx < ORIGIN_X + N; tx++) {
    row.push(await mount.getTerrainTile({ era: ERAS.PCG_9_3_5, gridX: tx, gridY: ty }));
  }
  tiles.push(row);
}
const region = new PETerrainRegion(tiles);
log(`decoded 9 canonical tiles (${tiles[0][0].name} .. ${tiles[2][2].name}).`);

const tileMaterials = [];
for (let ty = 0; ty < N; ty++) {
  const row = [];
  for (let tx = 0; tx < N; tx++) {
    const dec = await mount.getTerrainMaterials({
      era: ERAS.PCG_9_3_5, gridX: ORIGIN_X + tx, gridY: ORIGIN_Y + ty });
    if (!dec.provenance.extra.tailConsumedExactly) throw new Error('tail not consumed exactly');
    row.push(dec);
  }
  tileMaterials.push(row);
}

// ---------- fetch the LOCAL inputs of the CONFIRMED architecture ----------
// palette 0x66DC6 = Textures.bnt id 421318 ([P1]: byte 0 -> A[0])
const PALETTE_ID = 421318;
const palRes = await mount.resolveTexture({ era: ERAS.PCG_9_3_5, container: 'Textures.bnt', textureId: PALETTE_ID });
const pal = decodeTga2A32(palRes.payload);
if (pal.width !== 64 || pal.height !== 256) throw new Error(`palette dims ${pal.width}x${pal.height} != 64x256`);
// details: [P2] selector byte 0 -> C[0]=D[0]=458791, E[0]=458792
const DETAIL_IDS = [458791, 458791, 458792];
// the global height field (id 429259, LOCAL: Textures.bnt idx 71)
const hfRes = await mount.resolveTexture({ era: ERAS.PCG_9_3_5, container: 'Textures.bnt', textureId: 429259 });
const hf = decodeTga2(hfRes.payload);
if (hf.width !== 257 || hf.height !== 257) throw new Error(`field dims ${hf.width}x${hf.height} != 257x257`);
log(`LOCAL inputs fetched: palette 421318 (64x256x32), field 429259 (257x257), details 458791/458792 (256x256x24).`);

// ---------- the global field sampler (FUN_00947a40/FUN_009478e0 semantics) ----------
// bank[0][i] = (texel.chan0 - 128) * 5 meters; the field covers the world
// [-65536, +65536] at 512-unit texels, origin -65536; bilinear, stride 0x101.
const HF_ORIGIN = -65536;
const HF_TEXEL = 512;
const fieldH = new Float32Array(257 * 257);
for (let i = 0; i < 257 * 257; i++) {
  fieldH[i] = (hf.rgba[i * 4] - 128) * 5.0;
}
function fieldSample(x, y) {
  // world meters (the runtime world units == meters here; the palette row
  // domain is the leaf heights in meters per iter028)
  const fx = (x - HF_ORIGIN) / HF_TEXEL;
  const fy = (y - HF_ORIGIN) / HF_TEXEL;
  const ix = Math.max(0, Math.min(255, Math.floor(fx)));
  const iy = Math.max(0, Math.min(255, Math.floor(fy)));
  const tx = fx - ix, ty = fy - iy;
  const X = Math.min(256, ix + 1), Y = Math.min(256, iy + 1);
  const a = fieldH[iy * 257 + ix], b = fieldH[iy * 257 + X];
  const c = fieldH[Y * 257 + ix], d = fieldH[Y * 257 + X];
  return (a * (1 - tx) + b * tx) * (1 - ty) + (c * (1 - tx) + d * tx) * ty;
}
const H_LO = -20.0, H_HI = 512.0;   // 0x00a97dc8 f32 / 0x00a97c88 f64

// ---------- the tile-height sampler ([P3b]: the row input) ----------
// Per tile: the 32x32 TDF u16 heights -> meters (the legacy
// worldHeightMeters calibration), bilinear within the tile.
function makeTileHeightSampler(tile) {
  const G = 32;
  const hm = new Float32Array(G * G);
  for (let i = 0; i < G * G; i++) hm[i] = worldHeightMeters(tile.heights[i]);
  return {
    G, hm,
    sample(fx, fy) { // fx,fy in [0,1] tile-local
      const x = Math.max(0, Math.min(G - 1, fx * (G - 1)));
      const y = Math.max(0, Math.min(G - 1, fy * (G - 1)));
      const ix = Math.floor(x), iy = Math.floor(y);
      const X = Math.min(G - 1, ix + 1), Y = Math.min(G - 1, iy + 1);
      const tx = x - ix, ty = y - iy;
      const a = hm[iy * G + ix], b = hm[iy * G + X];
      const c = hm[Y * G + ix], d = hm[Y * G + X];
      return (a * (1 - tx) + b * tx) * (1 - ty) + (c * (1 - tx) + d * tx) * ty;
    },
  };
}

// ---------- the roughness (FUN_00991880's 12-slot formula, [P5]) ----------
// Evaluated on the TILE height grid at the sample scale (4 units): two
// diagonals + two edge-midpoint triples, divided by (4*size).
const INV_SQRT2 = 1 / Math.SQRT2;   // _DAT_00ba9670 = 1/sqrt(2)
function tileRoughness(sampler, fx, fy) {
  const G = sampler.G;
  const s = (dx, dy) => sampler.sample(
    Math.max(0, Math.min(1, fx + dx / (G - 1))),
    Math.max(0, Math.min(1, fy + dy / (G - 1))));
  const size = TILE_WORLD / G;   // the 4-unit sample scale
  const s1 = s(0, 0), s2 = s(1, 1), s3 = s(1, 0), s4 = s(0, 1);
  const s5 = s(0.5, 0), s6 = s(0, 0.5), s7 = s(0.5, 1), s8 = s(1, 0.5);
  const s9 = s(0.25, 0.25), s10 = s(0.75, 0.25), s11 = s(0.75, 0.75), s12 = s(0.25, 0.75);
  const v = (INV_SQRT2 * Math.abs(s3 - s4) +
             INV_SQRT2 * Math.abs(s1 - s2) +
             0.5 * Math.abs(s7 + (s5 - s6) - s8) +
             0.5 * Math.abs(s11 + (s9 - s10) - s12)) / (4 * size);
  return Math.max(0.0, Math.min(1.0, v));
}

// ---------- texture helpers (CONFIRMED sampler states, iter024) ----------
function makeTexture(rgba, width, height, { wrap, mipmap }) {
  const tex = new THREE.DataTexture(rgba, width, height, THREE.RGBAFormat);
  tex.colorSpace = THREE.NoColorSpace;
  tex.generateMipmaps = true;
  tex.magFilter = THREE.LinearFilter;
  tex.minFilter = mipmap === 'point' ? THREE.LinearMipmapNearestFilter : THREE.LinearMipmapLinearFilter;
  tex.wrapS = wrap;
  tex.wrapT = wrap;
  tex.flipY = false;
  tex.needsUpdate = true;
  return tex;
}
function flipVertical(rgba, width, height) {
  const flipped = new Uint8Array(rgba.length);
  for (let y = 0; y < height; y++) {
    flipped.set(rgba.subarray((height - 1 - y) * width * 4, (height - y) * width * 4), y * width * 4);
  }
  return flipped;
}
// [r185] DataTexture flipY=false everywhere; the TGA rows are bottom-up so we
// flip to top-down for texture space coherence with the bake grid.

// ---------- [P3b] THE ROW-INPUT SUBSTITUTION (measured evidence) ----------
// The engine's leaf heights come from the GLOBAL 257x257 field (bank[0]).
// Today's probe (the paletteProbe below) MEASURES the cross-era
// contradiction iter028 left open: the field, sampled at the engine's own
// addressing (tile grid x 128 units, origin -65536) at region A, gives
// -130..-125 m — while the SAME tiles' TDF heights are +16..+487 m. The
// field-vs-tile georeferencing is UNPINNED (iter028: the best alignment
// saturates at r=0.53; no offset is proven). Using the field at the raw
// addressing would flatten every palette row to 254 (the probe's
// expectedRows both 254) — a silent WRONG input. The honest, local,
// same-terrain source for the ALTITUDE of the RENDERED tiles is the tiles'
// OWN TDF heights (u16 -> meters, the same [2,514]m row domain). The field
// stays fetched + provenance-carried (LOCAL, and the mechanism's real
// input); its USE for the rows is deferred until the georef is pinned.
// DOCUMENTED SUBSTITUTION — no historical-truth claim beyond the row
// FORMULA (which is byte-proven).

// ---------- THE CONFIRMED BAKE (per tile) ----------
// S = 256 (FUN_0093f1d0 base gate: square <= 0x100; mgr+0x1840 default 0x100)
const S = 256;
const S4 = S >> 2;               // the factor grid (FUN_0093eb50: S/4)
const DETAIL_REPEAT = [32.0, 32.0, 16.0];
const rng = new EngineRng(0x30303030n);           // [P4] fixed seed
const { t1, t2 } = buildNoiseTables(rng);
let cursor1 = 0, cursor2 = 0;                     // the bake cursors

function bakeTile(tileGridX, tileGridY, tile) {
  const hs = makeTileHeightSampler(tile);          // [P3b] the row input
  const basePixels = new Uint8Array(S * S * 4);
  const factorPixels = new Uint8Array(S4 * S4 * 4);
  const palette = pal.rgba;   // 64 wide (col) x 256 high (row), RGBA
  // BASE: per pixel row/col -> the palette texel (FUN_00939c40 base path).
  // row = the ALTITUDE axis; col = the weight axis. The heights = the tile's
  // own TDF heights in meters ([P3b]), clamped [-20, 512].
  for (let py = 0; py < S; py++) {
    for (let px = 0; px < S; px++) {
      const h = Math.max(H_LO, Math.min(H_HI, hs.sample((px + 0.5) / S, (py + 0.5) / S)));
      const noise2 = t2[cursor2++ & 0x3FF];
      const row = Math.max(0, Math.min(254, Math.round(255.0 * (1.0 - (h - 2.0) / 512.0 - noise2))));
      const d = (py * S + px) * 4;
      const o = (row * 64) * 4;
      basePixels[d] = palette[o];
      basePixels[d + 1] = palette[o + 1];
      basePixels[d + 2] = palette[o + 2];
      basePixels[d + 3] = 255;  // the bake writes A=255 (the shadow field starts clear)
    }
  }
  // FACTOR: the one-hot channel by the palette-ALPHA 3 bands at the column
  // (FUN_00939c40 marker path; thresholds 73/53 from the binary).
  for (let fy = 0; fy < S4; fy++) {
    for (let fx = 0; fx < S4; fx++) {
      const noise1 = t1[cursor1++ & 0x3FF];
      const acc = tileRoughness(hs, (fx + 0.5) / S4, (fy + 0.5) / S4);   // [P5]
      const col = Math.max(0, Math.min(62, Math.round(63.0 * (noise1 + acc))));
      const alpha = palette[(col * 4) + 3];            // the palette alpha column
      const d = (fy * S4 + fx) * 4;
      factorPixels[d] = alpha >= 73 ? 255 : 0;
      factorPixels[d + 1] = (alpha >= 53 && alpha < 73) ? 255 : 0;
      factorPixels[d + 2] = alpha < 53 ? 255 : 0;
      factorPixels[d + 3] = 255;
    }
  }
  return { basePixels, factorPixels };
}

// ---------- the naive comparison model (materials_wsum C1-raw) ----------
function selectTop3(overlays) {
  const idx = overlays.map((o, i) => ({ i, total: o.mask.reduce((s, v) => s + v, 0) }));
  idx.sort((a, b) => (b.total - a.total) || (a.i - b.i));
  return idx.slice(0, 3).map((e) => e.i);
}

// ---------- build the scene: per tile naive|confirmed side by side ----------
const scene = new THREE.Scene();
const COLUMN_X_OFFSET = 200;
const bindProvenance = [];
const tileResults = [];

async function buildTile(tx, ty, xOff) {
  const tile = tiles[ty][tx];
  const dec = tileMaterials[ty][tx];
  const tileGridX = ORIGIN_X + tx, tileGridY = ORIGIN_Y + ty;
  let material, info;
  if (xOff > 0) {
    // ---- v_confirmed ----
    const { basePixels, factorPixels } = bakeTile(tileGridX, tileGridY, tile);
    const baseTex = makeTexture(basePixels, S, S, { wrap: THREE.ClampToEdgeWrapping, mipmap: 'point' });
    const facTex = makeTexture(factorPixels, S4, S4, { wrap: THREE.ClampToEdgeWrapping, mipmap: 'point' });
    const detTex = [];
    for (const id of DETAIL_IDS) {
      const res = await mount.resolveTexture({ era: ERAS.PCG_9_3_5, container: 'Textures.bnt', textureId: id });
      const d = decodeTga2(res.payload);
      detTex.push(makeTexture(flipVertical(d.rgba, d.width, d.height), d.width, d.height,
        { wrap: THREE.RepeatWrapping, mipmap: 'linear' }));
      bindProvenance.push({ kind: 'detail', id, entry: res.provenance.entry,
        payloadSha256: await sha256Hex(res.payload) });
    }
    material = new THREE.ShaderMaterial({
      uniforms: {
        uBase: { value: baseTex }, uFactor: { value: facTex },
        uD0: { value: detTex[0] }, uD1: { value: detTex[1] }, uD2: { value: detTex[2] },
      },
      vertexShader: `
        varying vec2 vUv;
        void main() {
          vUv = uv;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }`,
      fragmentShader: `
        precision highp float;
        // TERRAIN_14 (era 9.3.5, iter024 byte-extract 0x3EA):
        //   D = d0*w0 + d1*w1 + d2*w2 (w = factor RGB u8/255, NO renormalization)
        //   overlay per channel on D; SHADOW = base-alpha modulate (mul r0,r0,r0.a)
        //   UNLIT calibration (light/fog stages NOT implemented - labeled).
        uniform sampler2D uBase, uFactor, uD0, uD1, uD2;
        varying vec2 vUv;
        void main() {
          vec3 w = texture2D(uFactor, vUv).rgb;
          vec3 d0 = texture2D(uD0, vUv * ${DETAIL_REPEAT[0].toFixed(1)}).rgb;
          vec3 d1 = texture2D(uD1, vUv * ${DETAIL_REPEAT[1].toFixed(1)}).rgb;
          vec3 d2 = texture2D(uD2, vUv * ${DETAIL_REPEAT[2].toFixed(1)}).rgb;
          vec3 D = d0 * w.r + d1 * w.g + d2 * w.b;
          vec4 b = texture2D(uBase, vUv);
          vec3 lo = clamp(b.rgb * D * 2.0, 0.0, 1.0);
          vec3 hi = 1.0 - clamp((1.0 - b.rgb) * (1.0 - D) * 2.0, 0.0, 1.0);
          vec3 o = mix(lo, hi, step(vec3(0.5), D));
          gl_FragColor = vec4(o * b.a, 1.0);   // shadow term
        }`,
    });
    info = { model: 'v_confirmed', tile: tile.name };
  } else {
    // ---- v_naive (the materials_wsum C1-raw model, unchanged semantics) ----
    const named = dec.materials;
    const base = named[0];
    const overlaysAll = named.slice(1);
    const sel = selectTop3(overlaysAll);
    const selOverlays = sel.map((i) => overlaysAll[i]);
    const facData = new Uint8Array(16 * 16 * 4);
    for (let p = 0; p < 256; p++) {
      facData[p * 4] = selOverlays[0] ? selOverlays[0].mask[p] : 0;
      facData[p * 4 + 1] = selOverlays[1] ? selOverlays[1].mask[p] : 0;
      facData[p * 4 + 2] = selOverlays[2] ? selOverlays[2].mask[p] : 0;
      facData[p * 4 + 3] = 255;
    }
    const detTex = [];
    for (const o of selOverlays) {
      const res = await mount.resolveTexture({ era: ERAS.PCG_9_3_5, container: 'Textures.bnt', textureId: o.id });
      const d = decodeTga2(res.payload);
      detTex.push(makeTexture(flipVertical(d.rgba, d.width, d.height), d.width, d.height,
        { wrap: THREE.RepeatWrapping, mipmap: 'linear' }));
    }
    const baseRes = await mount.resolveTexture({ era: ERAS.PCG_9_3_5, container: 'Textures.bnt', textureId: base.id });
    const baseDec = decodeTga2(baseRes.payload);
    const baseTex = makeTexture(flipVertical(baseDec.rgba, baseDec.width, baseDec.height),
      baseDec.width, baseDec.height, { wrap: THREE.ClampToEdgeWrapping, mipmap: 'point' });
    material = new THREE.ShaderMaterial({
      uniforms: {
        uBase: { value: baseTex },
        uFactor: { value: makeTexture(facData, 16, 16, { wrap: THREE.ClampToEdgeWrapping, mipmap: 'point' }) },
        uD0: { value: detTex[0] ?? baseTex }, uD1: { value: detTex[1] ?? baseTex }, uD2: { value: detTex[2] ?? baseTex },
      },
      vertexShader: `
        varying vec2 vUv;
        void main() {
          vUv = uv;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }`,
      fragmentShader: `
        precision highp float;
        // v_naive: the SAME Terrain_14 ops, NAIVE inputs (base = the first TDF
        // material TGA; factor = the raw top-3 TDF mask weights, unrenormalized).
        uniform sampler2D uBase, uFactor, uD0, uD1, uD2;
        varying vec2 vUv;
        void main() {
          vec3 w = texture2D(uFactor, vUv).rgb;
          vec3 d0 = texture2D(uD0, vUv * ${DETAIL_REPEAT[0].toFixed(1)}).rgb;
          vec3 d1 = texture2D(uD1, vUv * ${DETAIL_REPEAT[1].toFixed(1)}).rgb;
          vec3 d2 = texture2D(uD2, vUv * ${DETAIL_REPEAT[2].toFixed(1)}).rgb;
          vec3 D = d0 * w.r + d1 * w.g + d2 * w.b;
          vec4 b = texture2D(uBase, vUv);
          vec3 lo = clamp(b.rgb * D * 2.0, 0.0, 1.0);
          vec3 hi = 1.0 - clamp((1.0 - b.rgb) * (1.0 - D) * 2.0, 0.0, 1.0);
          vec3 o = mix(lo, hi, step(vec3(0.5), D));
          gl_FragColor = vec4(o * b.a, 1.0);
        }`,
    });
    info = { model: 'v_naive', tile: tile.name,
      base: { id: base.id, name: base.name },
      top3: selOverlays.map((o) => ({ id: o.id, name: o.name })) };
  }

  // geometry: the local TDF heights (32x32 u16, the canonical offset-64 space)
  const G = 32;
  const positions = new Float32Array(G * G * 3);
  const uvs = new Float32Array(G * G * 2);
  for (let y = 0; y < G; y++) {
    for (let x = 0; x < G; x++) {
      const i = (y * G + x) * 3;
      positions[i] = tileGridX * TILE_WORLD + x * PE_TERRAIN_METER_PER_SAMPLE + xOff;
      positions[i + 1] = worldHeightMeters(tile.heights[y * G + x]);
      positions[i + 2] = tileGridY * TILE_WORLD + y * PE_TERRAIN_METER_PER_SAMPLE;
      const u = (y * G + x) * 2;
      uvs[u] = x / (G - 1);
      uvs[u + 1] = y / (G - 1);
    }
  }
  const indices = new Uint32Array((G - 1) * (G - 1) * 6);
  let q = 0;
  for (let y = 0; y < G - 1; y++) {
    for (let x = 0; x < G - 1; x++) {
      const a = y * G + x, b = a + 1, c = a + G, d = c + 1;
      indices[q++] = a; indices[q++] = c; indices[q++] = b;
      indices[q++] = b; indices[q++] = c; indices[q++] = d;
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  g.setAttribute('uv', new THREE.BufferAttribute(uvs, 2));
  g.setIndex(new THREE.BufferAttribute(indices, 1));
  g.computeVertexNormals();
  scene.add(new THREE.Mesh(g, material));
  return info;
}

const rowsInfo = [];
for (let ty = 0; ty < N; ty++) {
  for (let tx = 0; tx < N; tx++) {
    rowsInfo.push(await buildTile(tx, ty, 0));
    rowsInfo.push(await buildTile(tx, ty, COLUMN_X_OFFSET));
  }
}
log('built 2x9 meshes: v_naive (left) | v_confirmed (right, palette bake).');

// ---------- r185 deterministic render ----------
const W = 1024, H = 768;
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H);
renderer.setClearColor(0x0a0a12, 1);
document.getElementById('view').appendChild(renderer.domElement);

const box = new THREE.Box3();
for (const m of scene.children) {
  const pos = m.geometry.getAttribute('position');
  for (let i = 0; i < pos.count; i++) box.expandByPoint(new THREE.Vector3().fromBufferAttribute(pos, i));
}
const center = box.getCenter(new THREE.Vector3());
const size = box.getSize(new THREE.Vector3());
const camera = new THREE.PerspectiveCamera(55, W / H, 1, 50000);
camera.up.set(0, 1, 0);
camera.position.set(center.x, box.max.y + size.x * 0.5, center.z + size.x * 1.05);
camera.lookAt(center.x, center.y, center.z);

renderer.render(scene, camera);
const png1 = renderer.domElement.toDataURL('image/png');
const hash1 = await sha256Hex(Uint8Array.from(atob(png1.split(',')[1]), c => c.charCodeAt(0)));
renderer.render(scene, camera);
const png2 = renderer.domElement.toDataURL('image/png');
const hash2 = await sha256Hex(Uint8Array.from(atob(png2.split(',')[1]), c => c.charCodeAt(0)));

// ---------- per-model pixel stats (exact split at the screen center) ----------
const probeCanvas = document.createElement('canvas');
probeCanvas.width = W; probeCanvas.height = H;
const pctx = probeCanvas.getContext('2d', { willReadFrequently: true });
pctx.drawImage(renderer.domElement, 0, 0);
const img = pctx.getImageData(0, 0, W, H).data;
function modelStats(key, lo, hi) {
  let n = 0, sr = 0, sg = 0, sb = 0, nw = 0;
  for (let y = 0; y < H; y++) {
    for (let x = lo; x <= hi; x++) {
      const p = (y * W + x) * 4;
      if (img[p] === 10 && img[p + 1] === 10 && img[p + 2] === 18) continue;
      n++; sr += img[p]; sg += img[p + 1]; sb += img[p + 2];
      if (img[p] >= 250 && img[p + 1] >= 250 && img[p + 2] >= 250) nw++;
    }
  }
  if (!n) return null;
  return { model: key, pixels: n,
    meanRgb: [Math.round(sr / n), Math.round(sg / n), Math.round(sb / n)],
    whitePct: (100 * nw) / n };
}
const SPLIT = W / 2;
const stats = {
  naive: modelStats('v_naive', 0, SPLIT - 1),
  confirmed: modelStats('v_confirmed', SPLIT, W - 1),
};

// ---------- the palette row sanity probe (region A: mountains) ----------
const tdfHeights = tiles.flat().map((t) => [...t.heights]);
const heightsMin = Math.min(...tdfHeights.map((a) => Math.min(...a)));
const heightsMax = Math.max(...tdfHeights.map((a) => Math.max(...a)));
const rowForM = (hM) => Math.max(0, Math.min(254, Math.round(255.0 * (1.0 - (hM - 2.0) / 512.0))));
const regionFieldHeights = [];
for (let ty = 0; ty < N; ty++) {
  for (let tx = 0; tx < N; tx++) {
    for (let k = 0; k < 4; k++) {
      const wx = (ORIGIN_X + tx) * TILE_WORLD + (k & 1) * TILE_WORLD;
      const wy = (ORIGIN_Y + ty) * TILE_WORLD + (k >> 1) * TILE_WORLD;
      regionFieldHeights.push(fieldSample(wx, wy));
    }
  }
}
const paletteProbe = {
  regionTdfHeightsU16: { min: heightsMin, max: heightsMax },
  regionTdfHeightsM: { min: worldHeightMeters(heightsMin), max: worldHeightMeters(heightsMax) },
  regionFieldHeightsM_atEngineAddressing: {
    min: Math.round(Math.min(...regionFieldHeights) * 10) / 10,
    max: Math.round(Math.max(...regionFieldHeights) * 10) / 10,
  },
  fieldVsTileContradiction: 'the field at the engine addressing says -130..-125 m; the tiles say +16..+487 m — the georef is UNPINNED (iter028 r=0.53) => [P3b] the row input = the tile heights',
  expectedRowsFromTileHeights: {
    atMax: rowForM(worldHeightMeters(heightsMax)),
    atMin: rowForM(worldHeightMeters(heightsMin)),
  },
  note: 'rows = the altitude axis (iter028): high mountains -> low row indices (the 0x66DC6 rock end)',
};

// ---------- result ----------
const result = {
  page: 'terrain/materials_confirmed.js — the CONFIRMED 9.3.5 architecture (ITER 030)',
  version: 'M1_ITER_044 wiring (ledger ITER_030)',
  chain: 'terrain.bnt+Textures.bnt bytes -> PESourceMount -> tiles + palette 421318 + field 429259 + details 458791/458792 -> the CONFIRMED bake -> r185 Terrain_14-style render',
  region: { originGridX: ORIGIN_X, originGridY: ORIGIN_Y, tilesX: N, tilesY: N },
  models: {
    v_naive: { position: 'left column', source: 'materials_wsum C1-raw (ITER_025/026 model)',
      inputs: { base: 'the first TDF named material TGA', factor: 'the raw top-3 TDF dim=16 mask weights' } },
    v_confirmed: { position: 'right column', source: 'this page — the iter030 consolidated spec',
      inputs: {
        base: 'CPU bake from palette 0x66DC6 (row = altitude 255*(1-(h-2)/512-noise2); col = 63*(noise1+roughness))',
        factor: 'one-hot by palette-alpha bands 73/53 at the column',
        details: 'C[0]/D[0]/E[0] = 458791/458791/458792 (selector byte 0)',
        heights: 'local TDF tile heights (the bake rows AND the geometry) + the global field 429259 fetched/carried (its use deferred: [P3b])',
      } },
  },
  eraBoundedPlaceholders: [
    '[P1] climate byte grid (id 432502): MISSING locally -> constant byte 0 -> palette 0x66DC6 (A[0]); documented choice (the engine default for unmapped bytes is 0x66DC7)',
    '[P2] detail selector grid (id 459344): MISSING locally -> constant byte 0 -> the engine tables C[0]=D[0]=458791, E[0]=458792',
    '[P3a] the ArkHeightTree leaf recursion -> the direct height sample + clamp (the leaves\' own data chain preserved in form)',
    '[P3b] the ROW-INPUT SUBSTITUTION: the engine uses the global field heights; the page uses the TILES\' OWN heights because the field-vs-tile georeferencing is UNPINNED (iter028 r=0.53 saturation; THIS SESSION measured the field at the engine addressing = -130..-125 m vs the tiles +16..+487 m — see paletteProbe)',
    '[P4] the manager noise tables: the SEED only (the engine seeds per-session) - since iter036 the DRAW, the constants, and the f32 rounding points are BYTE-EXACT vs the binary (FUN_00405920 + FUN_0093cbf0; the operand lock in NOISE_OPERAND_LOCK)',
    '[P5] the accumulated leaf roughness: the CONFIRMED 12-slot formula evaluated on the tile height grid at the 4-unit sample scale',
  ],
  // THE FLOAT-CONSTANT OPERAND LOCK (iter036, ledger ITER_036 - THE CENSUS):
  // every constant byte-locked from the sandbox binary (SHA E7785430...);
  // the ANTI-CIRCULAR reference derives its constants FROM THIS EXPORT.
  NOISE_OPERAND_LOCK: {
    binary: 'Entropia.exe 9.3.5.6746 (sandbox SHA E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31)',
    f64_slots: {
      C04:   { va: '0x00A7B308', file_offset: '0x67B308', bytes_le: '00 00 00 A0 99 99 D9 3F', value: NOISE_C04, origin: 'float32(0.4) widened (FMUL qword @0x0093cde6)' },
      C02:   { va: '0x00A7B2D0', file_offset: '0x67B2D0', bytes_le: '00 00 00 A0 99 99 C9 3F', value: NOISE_C02, origin: 'float32(0.2) widened (FSUB qword @0x0093cdf1)' },
      C001:  { va: '0x00A7B360', file_offset: '0x67B360', bytes_le: '00 00 00 40 E1 7A 84 3F', value: NOISE_C001, origin: 'float32(0.01) widened (FMUL qword @0x0093ce13)' },
      C0005: { va: '0x00A81D18', file_offset: '0x681D18', bytes_le: '00 00 00 40 E1 7A 74 3F', value: NOISE_C0005, origin: 'float32(0.005) widened (FSUB qword @0x0093ce19)' },
      DIV20: { va: '0x00A7B9E0', file_offset: '0x67B9E0', bytes_le: '00 00 00 00 00 00 34 40', value: NOISE_DIV20, origin: 'FDIV/FLD qword @0x0093ce4b/0x0093ce4b' },
    },
    rng: { mul: '0x5DEECE66D', add: '0xB', draw: '(state & 0xFFFFFFFFFFFF) / 2^48',
      evidence: 'FUN_00405920 @0x00405930..0x0040595b (OR 0x3ff0000 stitch, <<4, FSUB qword [0x00a79818]=1.0)' },
    rounding_points: ['P1 @0x0093cddc','P2 @0x0093cdf7','P3 @0x0093ce01','P4 @0x0093ce0b','P5 @0x0093ce1f','P6 @0x0093ce2d','P8 @0x0093ce55','P9 @0x0093ce5c'],
    loop: '20 accumulations per entry, 1024 entries; tables f32 at mgr+0x1864/0x2864',
    seed_placeholder: 'FIXED 0x30303030 ([P4]; the engine seed is per-session runtime state)',
  },
  notPlaceholder: [
    'the palette (Textures.bnt 421318.dat, fetched + SHA-provenance at runtime)',
    'the details (458791/458792, local)',
    'the global height field (429259, local)',
    'the TDF tile heights (terrain.bnt, local)',
    'the Terrain_14 ops + sampler states (iter024 byte-extract)',
  ],
  bindings: bindProvenance,
  renderQuality: stats,
  paletteProbe,
  noiseTables: { t1: Array.from(t1).map(x => Math.fround(x)), t2: Array.from(t2).map(x => Math.fround(x)), n: 1024 },
  renderer: { threeRevision: THREE.REVISION, backend: 'WebGLRenderer', width: W, height: H,
    colorSpace: 'NoColorSpace passthrough' },
  screenshotPngSha256: hash1, screenshotDeterministic: hash1 === hash2,
  tileBindings: rowsInfo,
};
window.__CONFIRMED__ = result;
window.__CONFIRMED_PNG__ = png1;
log(
`CONFIRMED-ARCHITECTURE RENDERED — 9 tiles x 2 models
naive mean RGB: ${stats.naive.meanRgb.join(',')} (white ${stats.naive.whitePct.toFixed(1)}%)
confirmed mean RGB: ${stats.confirmed.meanRgb.join(',')} (white ${stats.confirmed.whitePct.toFixed(1)}%)
screenshot sha256: ${hash1} (deterministic: ${hash1 === hash2})
era-bounded placeholders: P1 climate byte 0->0x66DC6, P2 selector byte 0->458791/458792, P3-P5 documented`);
