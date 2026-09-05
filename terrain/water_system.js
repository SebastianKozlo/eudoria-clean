// water_system.js — ITER 031 (ledger ITER_031, Gate D vector e).
//
// The 9.3.5 WATER SYSTEM end-to-end page: the CONFIRMED Water technique
// (materials.vfs record 0x3eb, byte-faithful, era-identical JUL/PCG) applied
// as a SEPARATE WATER SURFACE over the proven water tiles, with the GROUND
// TERRAIN STILL VISIBLE UNDER WATER (charter Gate D architecture).
//
// CONFIRMED constants and ops are carried VERBATIM from the extracted .fx
// (iter031_fx_id_0x3eb_Water.hlsl, SHA 857dea6e...):
//   uniforms: LightSpecular=2.0 LightSpecularExp=75.0 ReflectSpecular=1.5
//     ReflectSpecularExp=10.0 ReflectHorizontal=1.5 ReflectionMin=0.4
//     ReflectionMax=0.9 WaveHeightX=1.1 WaveHeightY=0.7 WaveSpeedX=0.01
//     WaveSpeedY=0.001 WaveBlendSpeed=2.0 ReflectAdjust=0.5 WaveTileX=2.0
//     WaveTileY=1.0 Sky0Tile=0.5 Sky1Tile=1.0 WaterColorImpactInv=0.7
//     WaterColor=(0.1,0.2,0.25) WaterAlphaMin=0.6 WaterAlphaMax=0.9
//   VS: windSpeed = 3.0 - 2.0/(1.0 + g_WaterWind/2.0); time = fmod(g_Time,1800);
//       uv = (in.uv + time*WaveSpeed*windSpeed)*WaveTile; T = 4 sine phases.
//   PS: two wave normal maps blended by the 4 phases; N scaled by
//       WaveHeightX/Y * g_WaterWind; sun specular x2; reflection clamped
//       [ReflectionMin, ReflectionMax]; color = sky*reflection +
//       WaterColor*(1-reflection); alpha clamped [WaterAlphaMin, WaterAlphaMax].
//   states: AlphaBlend SrcAlpha/InvSrcAlpha (1Ark.fx macro), ZWrite=true,
//     ZEnable=true, CullMode=1, FogEnable=false.
//   CONFIRMED wind value path (FUN_009516f0): g_WaterWind =
//     0.5 + clamp(env.waterWind, 0, 1) * 1.5  ->  range [0.5, 2.0].
//
// ERA-BOUNDED PLACEHOLDERS (ALL LABELED, never silent approximations):
//   [P-WAVES] the historical wave normal maps (waves01.tga / waves02.tga,
//     referenced by ResourceName; the engine registers WAVES_01/02/03 BY NAME
//     as type-1000 resources, FUN_0048be10) are NOT PRESENT in any local
//     container (the corpus scan: only materials.vfs carries the names).
//     -> a SYNTHETIC sine-based normal field stands in, labeled.
//   [P-SKY] sky0.tga / sky1.tga: same status -> a SYNTHETIC vertical sky
//     gradient stands in, labeled.
//   [P-DATUM] the ENGINE water-plane elevation = 10.0f (world units of the
//     global height field; _DAT_00a7b128 = bytes 00 00 20 41; passed as
//     param_7 into FUN_0094a250 whose emitted vertices read z = param_7,
//     and the underwater test FUN_00853a80(x,y) < 10.0). The tile-datum
//     mapping is UNPINNED (iter028 [P3b]: the field at region A measures
//     -130..-125 m where the TDF tiles measure +16..+487 m). The page
//     therefore renders the surface at a DEMONSTRATIVE elevation control
//     (default 0.0 m = the iter023 surviving correlation: water materials
//     concentrate at tile-min 0), NOT as historical truth.

import * as THREE from 'three';
import { PESourceMount } from '../src/pesource/PESourceMount.js';
import { ERAS } from '../src/pesource/PEProvenance.js';
import { PETerrainRegion, worldHeightMeters } from '../src/peworld/PETerrainCore.js';

const HUD = document.getElementById('hud');
const LEGEND = document.getElementById('legend');
const log = (m) => { HUD.textContent = m; console.log(m); };

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

// ---------- mount (SHA-pinned, era-labeled) ----------
const mount = new PESourceMount(io);
await mount.mountEra({ era: ERAS.PCG_9_3_5, container: 'Terrain/terrain.bnt',
  path: '/pcg/Data/Terrain/terrain.bnt', format: 'BNT2_TERRAIN', verifyHash: true });
log('mounted PCG_9_3_5 terrain.bnt (SHA-verified).');

// ---------- the proven water window ----------
// the water tiles 0038006c/0038006d/0039006c/0039006d (grid 56-57 x 108-109,
// PCG census iter031) sit directly south of the proven region A window.
const ORIGIN_X = 56, ORIGIN_Y = 107, N = 4;
const TILE_WORLD = 128;                     // 32 samples * 4 m (page calibration)
const G = 32;
const tiles = [];
for (let ty = ORIGIN_Y; ty < ORIGIN_Y + N; ty++) {
  const row = [];
  for (let tx = ORIGIN_X; tx < ORIGIN_X + N; tx++) {
    row.push(await mount.getTerrainTile({ era: ERAS.PCG_9_3_5, gridX: tx, gridY: ty }));
  }
  tiles.push(row);
}
const region = new PETerrainRegion(tiles);
log(`decoded ${N * N} canonical tiles (${tiles[0][0].name} .. ${tiles[N - 1][N - 1].name}).`);

// ---------- the water material tiles (the CONFIRMED Water01-05 id set) ----------
const WATER_IDS = new Set([203650, 9088, 9102, 26950, 26951]); // iter023/031 dual-era census
const waterMask = [];
const waterIdSeen = new Set();
for (let ty = 0; ty < N; ty++) {
  const row = [];
  for (let tx = 0; tx < N; tx++) {
    const dec = await mount.getTerrainMaterials({
      era: ERAS.PCG_9_3_5, gridX: ORIGIN_X + tx, gridY: ORIGIN_Y + ty });
    if (!dec.provenance.extra.tailConsumedExactly) throw new Error('tail not consumed exactly');
    const ids = (dec.materials || []).map(m => m.id);
    const hit = ids.filter(id => WATER_IDS.has(id));
    hit.forEach(id => waterIdSeen.add(id));
    row.push(hit.length > 0 ? hit : null);
  }
  waterMask.push(row);
}
const waterTileCount = waterMask.flat().filter(v => v).length;
log(`water material tiles in window: ${waterTileCount} (ids: ${[...waterIdSeen].join(',')}).`);

// ---------- the GROUND terrain mesh (the ground STILL EXISTS under water) ----------
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a12);
const ground = new THREE.Group();
for (let ty = 0; ty < N; ty++) {
  for (let tx = 0; tx < N; tx++) {
    const tile = tiles[ty][tx];
    const geo = new THREE.PlaneGeometry(TILE_WORLD, TILE_WORLD, G - 1, G - 1);
    geo.rotateX(-Math.PI / 2);
    const pos = geo.attributes.position;
    const colors = new Float32Array(pos.count * 3);
    for (let y = 0; y < G; y++) {
      for (let x = 0; x < G; x++) {
        const i = y * G + x;
        const h = worldHeightMeters(tile.heights[y * G + x]);
        pos.setY(i, h);
        const t = Math.max(0, Math.min(1, (h + 20) / 220));
        const c = waterMask[ty][tx] ? [0.16 + 0.30 * t, 0.22 + 0.34 * t, 0.28 + 0.34 * t]
                                    : [0.30 + 0.40 * t, 0.30 + 0.36 * t, 0.24 + 0.26 * t];
        colors[i * 3] = c[0]; colors[i * 3 + 1] = c[1]; colors[i * 3 + 2] = c[2];
      }
    }
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geo.computeVertexNormals();
    const mesh = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ vertexColors: true }));
    mesh.position.set((ORIGIN_X + tx) * TILE_WORLD + TILE_WORLD / 2, 0,
                       (ORIGIN_Y + ty) * TILE_WORLD + TILE_WORLD / 2);
    ground.add(mesh);
  }
}
scene.add(ground);

// ---------- the WATER SURFACE (the CONFIRMED Water technique ops) ----------
// all constants VERBATIM from the extracted .fx defaults:
const FX = {
  LightSpecular: 2.0, LightSpecularExp: 75.0,
  ReflectSpecular: 1.5, ReflectSpecularExp: 10.0, ReflectHorizontal: 1.5,
  ReflectionMin: 0.4, ReflectionMax: 0.9,
  WaveHeightX: 1.1, WaveHeightY: 0.7, WaveSpeedX: 0.01, WaveSpeedY: 0.001,
  WaveBlendSpeed: 2.0, ReflectAdjust: 0.5, WaveTileX: 2.0, WaveTileY: 1.0,
  Sky0Tile: 0.5, Sky1Tile: 1.0, WaterColorImpactInv: 0.7,
  WaterColor: new THREE.Vector3(0.1, 0.2, 0.25),
  WaterAlphaMin: 0.6, WaterAlphaMax: 0.9,
};
const G_TIME_FIXED = 300.0;   // deterministic frame (the engine: fmod(g_Time, 1800))
const uniforms = {
  uWind: { value: 1.0 },      // g_WaterWind; CONFIRMED engine range [0.5, 2.0]
  uTime: { value: G_TIME_FIXED },
  uSunDir: { value: new THREE.Vector3(-0.35, -0.75, -0.55).normalize() }, // fixed sun
  uSunColor: { value: new THREE.Vector3(1.0, 0.95, 0.85) },
  uAmbient: { value: new THREE.Vector3(0.25, 0.27, 0.30) },   // AMBIENT stand-in
  uFogColor: { value: new THREE.Vector3(0.5, 0.5, 0.5) },
  ...Object.fromEntries(Object.entries(FX).filter(([k]) => typeof FX[k] === 'number')
    .map(([k, v]) => ['fx_' + k, { value: v }])),
  fx_WaterColor: { value: FX.WaterColor },
};

const waterMat = new THREE.ShaderMaterial({
  uniforms,
  transparent: true,             // CONFIRMED: AlphaBlendEnable=true (1Ark.fx macro)
  depthWrite: true,              // CONFIRMED: ZWriteEnable=true
  side: THREE.DoubleSide,        // DEMONSTRATIVE (CullMode=1 in the .fx; the
                                // label carries the exact state)
  vertexShader: /* glsl */`
    uniform float uWind, uTime, fx_WaveSpeedX, fx_WaveSpeedY, fx_WaveTileX, fx_WaveTileY,
                  fx_WaveBlendSpeed, fx_ReflectAdjust;
    varying vec2 vTexCoord; varying vec3 vWorld; varying vec4 vT; varying vec3 vE;
    void main() {
      // CONFIRMED VS ops (Water.fx): scroll + wind speed + the 4 sine phases
      float windSpeed = 3.0 - 2.0 / (1.0 + uWind / 2.0);
      float time = mod(uTime, 1800.0);
      vTexCoord = (uv + time * vec2(fx_WaveSpeedX, fx_WaveSpeedY) * windSpeed)
                  * vec2(fx_WaveTileX, fx_WaveTileY);
      float freq = time * fx_WaveBlendSpeed * windSpeed;
      const float PI_HALF = 1.570796327;
      vT = vec4( (sin(freq + PI_HALF * 0.0) + 1.0) * 0.5,
                 (sin(freq + PI_HALF * 1.0) + 1.0) * 0.5,
                 (sin(freq + PI_HALF * 2.0) + 1.0) * 0.5,
                 (sin(freq + PI_HALF * 3.0) + 1.0) * 0.5 );
      vec4 wp = modelMatrix * vec4(position, 1.0);
      vWorld = wp.xyz;
      gl_Position = projectionMatrix * viewMatrix * wp;
    }`,
  fragmentShader: /* glsl */`
    uniform float uWind, fx_WaveHeightX, fx_WaveHeightY, fx_LightSpecular,
                  fx_LightSpecularExp, fx_ReflectSpecular, fx_ReflectSpecularExp,
                  fx_ReflectHorizontal, fx_ReflectionMin, fx_ReflectionMax,
                  fx_WaterColorImpactInv, fx_Sky0Tile, fx_Sky1Tile,
                  fx_WaterAlphaMin, fx_WaterAlphaMax;
    uniform vec3 uSunDir, uSunColor, uAmbient, uFogColor;
    uniform vec3 fx_WaterColor;
    varying vec2 vTexCoord; varying vec3 vWorld; varying vec4 vT; varying vec3 vE;
    // [P-WAVES] SYNTHETIC wave normal field (the historical waves01/02.tga
    // are name-registered resources NOT present in the local corpus):
    vec4 synthWave(vec2 c) {
      vec2 k = c * 6.2831853;
      float a = sin(k.x) * cos(k.y * 0.63 + 1.7);
      float b = sin(k.y + 1.3) * cos(k.x * 0.81);
      float cc = sin((k.x + k.y) * 0.5 + 0.4);
      float d = sin((k.x - k.y) * 0.7 + 2.1);
      return clamp(vec4(a, b, cc, d) * 0.5 + 0.5, 0.0, 1.0);
    }
    // [P-SKY] SYNTHETIC sky gradient (sky0.tga/sky1.tga not local)
    vec3 synthSky(vec3 dir) {
      float h = clamp(dir.z * 0.5 + 0.5, 0.0, 1.0);
      return mix(vec3(0.28, 0.36, 0.52), vec3(0.62, 0.72, 0.86), h);
    }
    void main() {
      vec4 normal_1 = synthWave(vTexCoord) * 2.0 - 1.0;
      vec4 normal_2 = synthWave(vTexCoord * 1.7 + 3.1) * 2.0 - 1.0;
      vec2 normal_offset = vT.x * normal_1.xy + vT.y * normal_1.zw
                         + vT.z * normal_2.xy + vT.w * normal_2.zw;
      vec3 N = vec3(normal_offset.x * fx_WaveHeightX * uWind,
                    normal_offset.y * fx_WaveHeightY * uWind, 1.0);
      vec3 E = normalize(cameraPosition - vWorld);
      vec3 L = -normalize(uSunDir);
      vec3 H = normalize(E + L);
      float light_diffuse = 0.0, light_specular = 0.0, reflect_specular = 0.0;
      float NdotL = dot(N, L);
      if (NdotL > 0.0) {
        light_diffuse = NdotL;
        float NdotH = dot(N, H);
        if (NdotH > 0.0) {
          light_specular = pow(NdotH, fx_LightSpecularExp) * fx_LightSpecular;
          reflect_specular = pow(NdotH, fx_ReflectSpecularExp) * fx_ReflectSpecular;
        }
      }
      vec3 e_reflect = normalize(vec3(
        1.0 - 0.5 - (1.0 - E.x) * (1.0 - E.x) * 0.5,
        1.0 - 0.5 - (1.0 - E.y) * (1.0 - E.y) * 0.5,
        0.5 + E.z * E.z * 0.5));
      vec3 lookup = reflect(e_reflect, N);
      float reflect_horizon = min(pow(1.0 - E.z, 5.0) * fx_ReflectHorizontal, 1.0);
      float reflection = clamp(reflect_specular +
        reflect_horizon * fx_WaterColorImpactInv, fx_ReflectionMin, fx_ReflectionMax);
      vec3 sky1c = synthSky(lookup * fx_Sky1Tile);
      vec3 sky0c = synthSky(lookup * fx_Sky0Tile);
      vec3 color = sky0c * (1.0 - sky1c.r) + sky1c * sky1c.r; // two-sampler blend [P-SKY]
      color = color * reflection + fx_WaterColor * (1.0 - reflection);
      color *= max((light_diffuse + light_specular) * uSunColor, uAmbient);
      float alpha = clamp(reflect_specular + reflect_horizon,
                           fx_WaterAlphaMin, fx_WaterAlphaMax);
      gl_FragColor = vec4(color, alpha);
    }`,
});

// the surface covers the water tile bounding box (grid 56-57 x 108-109)
// ---------- [P-DATUM] the demonstrative elevation control ----------
// (the engine constant 10.0f is in the GLOBAL-FIELD datum; the tile-datum
// mapping is UNPINNED per iter028 [P3b]; default 0.0 m = the iter023
// surviving correlation: water materials concentrate at tile-min 0)
const LEVEL_DEFAULT = 0.0;
const waterUniformLevel = { value: LEVEL_DEFAULT };

const WX0 = 56, WY0 = 108, WN = 2;
const waterGeo = new THREE.PlaneGeometry(WN * TILE_WORLD, WN * TILE_WORLD, 64, 64);
waterGeo.rotateX(-Math.PI / 2);
const waterMesh = new THREE.Mesh(waterGeo, waterMat);
waterMesh.position.set((WX0 + WN / 2) * TILE_WORLD, waterUniformLevel.value, (WY0 + WN / 2) * TILE_WORLD);
scene.add(waterMesh);

// a light + fixed camera (deterministic)
const sun = new THREE.DirectionalLight(0xffffff, 1.0);
sun.position.set(-700, 900, -1100);
scene.add(sun);
scene.add(new THREE.AmbientLight(0x404050, 1.0));
const camera = new THREE.PerspectiveCamera(52, 16 / 9, 1, 20000);
camera.position.set(58 * TILE_WORLD, 260, 111 * TILE_WORLD);
camera.lookAt(57 * TILE_WORLD, 0, 109.5 * TILE_WORLD);

const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setSize(1280, 720);
document.getElementById('view').appendChild(renderer.domElement);

renderer.render(scene, camera);
const png1 = renderer.domElement.toDataURL('image/png');
renderer.render(scene, camera);
const png2 = renderer.domElement.toDataURL('image/png');
const deterministic = png1 === png2;
const enc = new TextEncoder();
const hash = await sha256Hex(enc.encode(png1));

const stats = (() => {
  const hmin = [], hmax = [];
  for (let ty = 0; ty < N; ty++) for (let tx = 0; tx < N; tx++) {
    if (!waterMask[ty][tx]) continue;
    let mn = 65535, mx = 0;
    for (let i = 0; i < 1024; i++) { const v = tiles[ty][tx].heights[i]; mn = Math.min(mn, v); mx = Math.max(mx, v); }
    hmin.push(worldHeightMeters(mn)); hmax.push(worldHeightMeters(mx));
  }
  return { waterTileCount, heightMinM: Math.min(...hmin), heightMaxM: Math.max(...hmax) };
})();

log(
`WATER SYSTEM page (ITER 031) - deterministic: ${deterministic}
render sha256: ${hash}
water material tiles in window: ${stats.waterTileCount}/16 (ids ${[...waterIdSeen].join(',') || 'none'})
water-tile terrain heights: ${stats.heightMinM.toFixed(1)}..${stats.heightMaxM.toFixed(1)} m (the ground exists under water)
surface elevation [P-DATUM]: ${waterUniformLevel.value} m (DEMONSTRATIVE; engine constant = 10.0 in the global-field datum, tile-datum UNPINNED iter028 [P3b])
g_WaterWind = ${uniforms.uWind.value} (CONFIRMED engine range [0.5, 2.0]: FUN_009516f0 remap of the env value)
g_Time = ${G_TIME_FIXED} (deterministic frame; the engine: fmod(g_Time, 1800))`);

LEGEND.textContent =
`ERA-BOUNDED PLACEHOLDERS (labeled, never silent approximations):
[P-WAVES] synthetic wave normals - the historical waves01/02.tga are name-registered resources (WAVES_01/02/03, FUN_0048be10) NOT in any local container
[P-SKY] synthetic sky gradient - sky0.tga/sky1.tga not local
[P-DATUM] surface elevation = DEMONSTRATIVE control (engine: 10.0f world units _DAT_00a7b128; the FUN_0094a250 plane vertices read z = param_7 = 10.0; the tile-datum georef UNPINNED)
CONFIRMED from the bytes: the Water technique 0x3eb (materials.vfs rec 1003, 7614 B, SHA 857dea6e..., BYTE-IDENTICAL JUL_2003 == PCG_9_3_5) - all 22 uniform defaults, the VS wind/scroll/sine ops, the PS normal blend + reflection [0.4,0.9] + WaterColor (0.1,0.2,0.25) + alpha [0.6,0.9], the states (SrcAlpha/InvSrcAlpha, ZWrite on, CullMode 1); the ARK_WATER_WIND binding chain (FUN_009512a0 table -> ArkFXPShared<float> @mgr+0x15c value @+0x184 <- FUN_009516f0 per frame <- env+0x14 clamp[0,1] remap[0.5,2.0])`;

window.__iter031_result = { deterministic, hash, stats };
