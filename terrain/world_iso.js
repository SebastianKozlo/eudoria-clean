// world_iso.js — JOB W03_ISO_TERRAIN_VERTICAL_SLICE + W05_ISO_MATERIALS_SPLAT
// (2026-10-30, attempt W05_a1)
//
// W03 (unchanged core): does the CLEAN pipeline (Three r187) render a visible,
// explorable terrain patch from the REAL ISO 50.bnt (PE 5.1.0.0, PC Gamer
// Nov2003 ISO) through the full clean chain?
//   recovered ISO Data/Terrain/50.bnt ORIGINAL BYTES (SHA-pinned)
//     -> PESourceMount (era ISO_5_1_0_0 — NEW EXPLICIT ERA, never an alias
//        of JUL_2003/PCG_9_3_5; BUNT framing, byte-derived)
//     -> TerrainTile (RAW uint16 heights — IR numbers, NO conversion)
//     -> PETerrainRegion (FUN_0047fb20 identity-lerp height semantics)
//     -> Three.js r187 WebGLRenderer — fly controls + HUD provenance
//
// W05 (this job): replace the diagnostic flat-color material with the REAL
// ISO_5_1_0_0 terrain MATERIALS — material tail decode (per-tile layers,
// 16x16 weight masks, fixture-derived offsetbase +56), layer->texture join,
// runtime SPLAT (weights -> vertex attributes; textures -> DataTexture):
//   - tail decode is done OFFLINE in the Node fixture (w05_tail_fixture.mjs)
//     and uploaded here via src/peworld/IsoMaterialsFixture.js; the browser
//     additionally re-decodes the SAME tails live through the repo
//     TdfMaterialTailDecoder and CROSS-CHECKS mask/layer equality (loud on
//     any mismatch). Decode happens ONCE at load — never per frame; texture
//     objects and masks are cached per tile/per TexID.
//   - the ISO corpus ships NO texture container (fixture coverage analysis);
//     the layer->texture join closes against CD_JAN_2003 Textures.ark
//     (audited material-id -> texture-resource join, verified 12/12 in the
//     fixture). These textures are REFERENCE_RECONSTRUCTION assets, NOT ISO
//     truth — every joined layer is labeled REFERENCE on the HUD/result.
//   - splat model (audited TMF data model, STRONGLY_SUPPORTED):
//     position-0 named record = BASE (Stone04, all-255 in 9/9 tiles);
//     overlays are INDEPENDENT alpha weights (sums>255 tolerated as ORIGINAL
//     DATA, never renormalized): color = base; for each overlay:
//     color = mix(color, overlay, weight).
//
// DISPLAY SCALE (explicit): raw u16 heights kept as-is; the ONLY conversion is
// the labeled CURRENT_RUNTIME CALIBRATION u16/128 -> meters and 2 m/sample
// horizontal (PETerrainCore) — NOT historical engine facts.
//
// UV (explicit): world-space UV = worldPos.xz / uVRepeat (default 8 m per
// repeat — RECONSTRUCTION_CANDIDATE, ?uvRepeat= override), RepeatWrapping,
// Linear + mipmap filtering. Colorspace (explicit): textures are authored
// sRGB -> THREE.SRGBColorSpace (GPU decode to linear) -> lighting in LINEAR
// -> renderer output linear->sRGB. Alpha: TGA payloads are 24bpp opaque — no
// texture alpha; the ONLY blend alpha is the material weight.
//
// ENGINEERING PREVIEW: background color + strong light are EXPLICIT
// diagnostic presentation (badge on HUD) — not the original PE environment.
// W14 layered environment (sky/fog/light) — see src/peworld/IsoEnvironment.js
// for per-layer provenance: sky + light + fog VALUES are ENGINEERING_PREVIEW;
// the fog MODEL shape (linear z-fog) is source-backed gb12 NiFogProperty
// semantics (paraphrase, pinned in W14_ENVIRONMENT_SOURCE_MAP.md).
//
// W06 (this job, 2026-10-30 attempt W06_a1): MULTIPATCH STREAMING — expand
// the visible area from the fixture-pinned 3x3 core to a 5x5 window
// containing it (windowContainingCore, clamped to the 220x236 grid), with
// per-tile ASYNC decode + near-origin-first order + explicit ocean/nodata
// skip (>90% zero samples — the SAME W03/W05 census heuristic) + a
// name-keyed tile cache with explicit eviction/disposal. The fly/render
// loop starts on the core; ring tiles appear as they decode (non-blocking
// background task — the core 3x3 fallback keeps working if streaming
// fails). NOT implemented (backlog, ranked): LOD, frustum culling,
// workers, priority queue.
import { DEFAULT_ENV, ENV_LAYERS, GB12_FOG_MODEL, envConfigInvariant, fogRangeFromGb12, skyColorAt, layerTable } from '../src/peworld/IsoEnvironment.js';
import * as THREE from 'three';
import { PESourceMount } from '../src/pesource/PESourceMount.js';
import { ERAS } from '../src/pesource/PEProvenance.js';
import { decodeMaterialTail } from '../src/pesource/TdfMaterialTailDecoder.js';
import { decodeTga2 } from '../src/pesource/TgaDecoder.js';
import { PETerrainRegion, HEIGHT_QUERY } from '../src/peworld/PETerrainCore.js';
import { findFirstWorkingPatch, ISO_GRID, windowContainingCore, streamRingPlan, tileTerrainStats, isOceanNodataTile, OCEAN_SKIP_RULE } from '../src/peworld/IsoPatchSelection.js';
import { ISO_MATERIALS_FIXTURE, ISO_TEXTURE_PAYLOADS } from '../src/peworld/IsoMaterialsFixture.js';

const ERA = ERAS.ISO_5_1_0_0;
const TERRAIN_URL = '/iso/50.bnt';
const ISO_SHA256_PIN = 'A6E59EE07A51EAC06A3E75DA5421E5928D59EDED74F096DCAD04CE80ED01DA00';
const UV_REPEAT = (() => {
  const v = Number(new URLSearchParams(location.search).get('uvRepeat'));
  return Number.isFinite(v) && v > 0 ? v : 8; // m per texture repeat — RECONSTRUCTION_CANDIDATE
})();

const HUD = document.getElementById('hud');
const log = (m) => { HUD.textContent = m; console.log(m); };

// ---------- fatal-error tracking (before anything can fail) ----------
window.__W03_ERRORS__ = [];
window.__W05_ERRORS__ = window.__W03_ERRORS__; // same array — one census
window.addEventListener('error', (e) => {
  window.__W03_ERRORS__.push({ kind: 'error', text: String(e.message ?? e), source: e.filename });
});
window.addEventListener('unhandledrejection', (e) => {
  window.__W03_ERRORS__.push({ kind: 'unhandledrejection', text: String(e.reason ?? e) });
});

// ---------- browser I/O adapter (injected into PESourceMount) ----------
async function fetchBytes(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`fetch ${url}: HTTP ${res.status}`);
  return new Uint8Array(await res.arrayBuffer());
}
async function strictInflate(zlibBytes) {
  const ds = new DecompressionStream('deflate');
  const stream = new Blob([zlibBytes]).stream().pipeThrough(ds);
  const buf = await new Response(stream).arrayBuffer();
  return new Uint8Array(buf);
}
async function sha256Hex(bytes) {
  const d = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();
}
const io = { readFile: fetchBytes, inflate: strictInflate, sha256: sha256Hex };

// ---------- mount the ORIGINAL ISO container (hash-pinned, era-labeled) ----------
const mount = new PESourceMount(io);
log(`mounting ${ERA} 50.bnt from ${TERRAIN_URL} (118,016,977 B expected)…`);
const mountRec = await mount.mountEra({
  era: ERA,
  container: 'Terrain/50.bnt',
  path: TERRAIN_URL,
  format: 'BUNT',
  verifyHash: true,
});
const mountHashOk = mountRec.hashVerified && mountRec.actualSha256 === ISO_SHA256_PIN;
if (!mountHashOk) {
  throw new Error(`[W05] mount hash NOT verified: ${mountRec.actualSha256}`);
}
log(`mounted + SHA-verified (${mountRec.actualSha256.slice(0, 16)}…).`);

// ---------- DYNAMIC tile selection from the 50.bnt INDEX ----------
log('scanning index for the first working 3x3 patch…');
const patch = await findFirstWorkingPatch(mount, { era: ERA, n: 3 });
const tileNames = patch.tiles.flat().map((t) => t.name);
log(`patch ${patch.originGridX},${patch.originGridY} (${patch.patchesTried} tried): ${tileNames.join(' ')}`);

// The W05 material fixture is built for the deterministic first-working patch.
if (patch.originGridX !== ISO_MATERIALS_FIXTURE.patchOrigin.gridX ||
    patch.originGridY !== ISO_MATERIALS_FIXTURE.patchOrigin.gridY) {
  throw new Error(
    `[W05] fixture patch origin ${ISO_MATERIALS_FIXTURE.patchOrigin.gridX},${ISO_MATERIALS_FIXTURE.patchOrigin.gridY} ` +
    `!= runtime patch origin ${patch.originGridX},${patch.originGridY} — regenerate the fixture`);
}

// ---------- PE Runtime Core: canonical region + geometry ----------
const region = new PETerrainRegion(patch.tiles);
const geom = region.buildGeometry();
for (let i = 0; i < geom.positions.length; i++) {
  if (!Number.isFinite(geom.positions[i])) throw new Error(`[W05] NaN in geometry @${i}`);
}
log(`region built: ${geom.sampleGridX}x${geom.sampleGridY} samples, seams: E ${region.tileSeamDiagnostic.east.diffs}/${region.tileSeamDiagnostic.east.pairs}, S ${region.tileSeamDiagnostic.south.diffs}/${region.tileSeamDiagnostic.south.pairs} (ORIGINAL_DATA).`);

// ---------- Three r187 render (ENGINEERING PREVIEW presentation) ----------
const W = 1100, H = 820;
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H);
renderer.setClearColor(0x0a0a12, 1); // ENGINEERING_PREVIEW background (badge)
document.getElementById('view').appendChild(renderer.domElement);

const scene = new THREE.Scene();
const g = new THREE.BufferGeometry();
g.setAttribute('position', new THREE.BufferAttribute(geom.positions, 3));
g.setIndex(new THREE.BufferAttribute(geom.indices, 1));
g.computeVertexNormals();
// DIAGNOSTIC material (mode 'diagnostic'): flat color, no material semantics.
// W05 keeps it as the INITIAL mode; the material splat (mode 'splat') is the
// real ISO material reconstruction.
const material = new THREE.MeshLambertMaterial({ color: 0x9a8f7a, wireframe: false });
const mesh = new THREE.Mesh(g, material);
scene.add(mesh);

// (W14: sun/ambient moved into the layered-environment block below — the W03/W05
//  diagnostic values 2.5/1.0 are kept as explicit ENGINEERING_PREVIEW defaults.)

const box = new THREE.Box3().setFromBufferAttribute(g.getAttribute('position'));
const center = box.getCenter(new THREE.Vector3());
const size = box.getSize(new THREE.Vector3());
const camera = new THREE.PerspectiveCamera(55, W / H, 1, 50000);
camera.up.set(0, 1, 0);

// =====================================================================
// W14 — LAYERED ENVIRONMENT (sky / fog / light), per-layer provenance
// =====================================================================
let framesRendered = 0; // (moved up: applyEnv renders a frame before the fly-controls section)
const env = {
  sky: { ...DEFAULT_ENV.sky, zenith: [...DEFAULT_ENV.sky.zenith], horizon: [...DEFAULT_ENV.sky.horizon], ground: [...DEFAULT_ENV.sky.ground] },
  fog: { ...DEFAULT_ENV.fog, color: [...DEFAULT_ENV.fog.color], gb12: { ...DEFAULT_ENV.fog.gb12 } },
  light: { ...DEFAULT_ENV.light, sunDir: [...DEFAULT_ENV.light.sunDir] },
};
const envInvariant = envConfigInvariant(env, camera.near);
if (!envInvariant.ok) throw new Error(`[W14] env invariant failed: ${envInvariant.errors.join('; ')}`);

// ---- sky dome (ENGINEERING_PREVIEW procedural gradient — no ISO skydome) ----
const SKY_RADIUS = 24000;
const skyUniforms = {
  uZenith: { value: new THREE.Vector3(...env.sky.zenith) },
  uHorizon: { value: new THREE.Vector3(...env.sky.horizon) },
  uGround: { value: new THREE.Vector3(...env.sky.ground) },
};
const skyMat = new THREE.ShaderMaterial({
  uniforms: skyUniforms,
  side: THREE.BackSide,
  depthWrite: false,
  fog: false, // the sky is the fog backdrop — never fogged itself
  vertexShader: `
    varying vec3 vDir;
    void main() {
      vDir = position;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform vec3 uZenith;
    uniform vec3 uHorizon;
    uniform vec3 uGround;
    varying vec3 vDir;
    void main() {
      float d = normalize(vDir).y;             // +1 zenith, 0 horizon, -1 nadir
      vec3 c = d >= 0.0
        ? mix(uHorizon, uZenith, d)            // above horizon: horizon->zenith
        : mix(uHorizon, uGround, -d);          // below: horizon->ground haze
      gl_FragColor = vec4(c, 1.0);
      #include <colorspace_fragment>
    }
  `,
});
const skyDome = new THREE.Mesh(new THREE.SphereGeometry(SKY_RADIUS, 24, 16), skyMat);
skyDome.frustumCulled = false;
skyDome.renderOrder = -1;
scene.add(skyDome);

// ---- fog (SOURCE_BACKED MODEL gb12 FOG_Z_LINEAR, ENGINEERING_PREVIEW values) ----
const fogRange = fogRangeFromGb12(env.fog.gb12.depth, camera.near, env.fog.fullOcclusionDistance);
if (fogRange.disabled) throw new Error('[W14] default fog config resolves to disabled');
const fogColor = new THREE.Color(...env.fog.color);
scene.fog = new THREE.Fog(fogColor, fogRange.near, fogRange.far);
const fogState = { near: fogRange.near, far: fogRange.far, color: fogColor };

// ---- light (ENGINEERING_PREVIEW diagnostic — kept from W03/W05) ----
const SUN_DIR = new THREE.Vector3(...env.light.sunDir);
const sun = new THREE.DirectionalLight(0xffffff, env.light.sunIntensity);
sun.position.copy(SUN_DIR);
scene.add(sun);
const ambient = new THREE.AmbientLight(0xffffff, env.light.ambientIntensity);
scene.add(ambient);

function applyEnv() {
  skyDome.visible = env.sky.enabled;
  scene.fog = env.fog.enabled ? new THREE.Fog(fogState.color, fogState.near, fogState.far) : null;
  sun.intensity = env.light.sunIntensity;
  ambient.intensity = env.light.ambientIntensity;
  sun.position.set(...env.light.sunDir);
  skyUniforms.uZenith.value.set(...env.sky.zenith);
  skyUniforms.uHorizon.value.set(...env.sky.horizon);
  skyUniforms.uGround.value.set(...env.sky.ground);
  for (const rec of [...splatTiles, ...streamSplatTiles]) {
    const u = rec.mesh.material.uniforms;
    u.uFogColor.value.set(env.fog.enabled ? fogState.color.r : 0, env.fog.enabled ? fogState.color.g : 0, env.fog.enabled ? fogState.color.b : 0);
    u.uFogNear.value = env.fog.enabled ? fogState.near : Infinity;
    u.uFogFar.value = env.fog.enabled ? fogState.far : Infinity;
  }
  renderer.render(scene, camera);
  framesRendered++;
}

const cameraStart = new THREE.Vector3(
  center.x + size.x * 0.35, box.max.y + size.z * 0.45, center.z + size.z * 0.75);
camera.position.copy(cameraStart);
camera.lookAt(center.x, center.y, center.z);
scene.add(new THREE.AxesHelper(200));

// =====================================================================
// W05 — MATERIAL SPLAT BUILD (decode ONCE here, cache; never per frame)
// =====================================================================
const b64ToU8 = (b64) => {
  const s = atob(b64);
  const u = new Uint8Array(s.length);
  for (let i = 0; i < s.length; i++) u[i] = s.charCodeAt(i);
  return u;
};

// ---- 1. fixture masks + LIVE cross-check against the repo tail decoder ----
const fixtureTilesByName = new Map(ISO_MATERIALS_FIXTURE.tiles.map((t) => [t.name, t]));
let crossCheck = { tiles: 0, layers: 0, mismatches: [] };
for (let ty = 0; ty < patch.n; ty++) {
  for (let tx = 0; tx < patch.n; tx++) {
    const tile = patch.tiles[ty][tx];
    const fx = fixtureTilesByName.get(tile.name);
    if (!fx) throw new Error(`[W05] fixture has no tile ${tile.name}`);
    // LIVE decode through the repo format layer (cached data, same payload)
    const live = decodeMaterialTail(tile.tail);
    if (live.consumed !== tile.tail.byteLength) {
      throw new Error(`[W05] live tail decode consumption mismatch on ${tile.name}`);
    }
    if (live.namedMaterials.length !== fx.materials.length) {
      crossCheck.mismatches.push(`${tile.name}: layer count live=${live.namedMaterials.length} fixture=${fx.materials.length}`);
      continue;
    }
    crossCheck.tiles++;
    for (const lm of live.namedMaterials) {
      const position = live.records.indexOf(lm);
      const fm = fx.materials.find((m) => m.position === position);
      if (!fm) { crossCheck.mismatches.push(`${tile.name}: fixture layer @${position} missing`); continue; }
      const fxMask = b64ToU8(fm.maskB64);
      let eq = fm.id === lm.id && fm.name === lm.name &&
        ((fm.maskEncoding === 'raw') === (lm.maskEncoding === 'raw')) &&
        fxMask.length === lm.mask.length;
      for (let k = 0; eq && k < fxMask.length; k++) if (fxMask[k] !== lm.mask[k]) eq = false;
      if (eq) crossCheck.layers++;
      else crossCheck.mismatches.push(`${tile.name} layer ${lm.name}: mask/id/name mismatch (fixture vs live)`);
    }
  }
}
if (crossCheck.mismatches.length > 0) {
  throw new Error(`[W05] fixture/live cross-check FAILED:\n  ${crossCheck.mismatches.join('\n  ')}`);
}
log(`material cross-check: fixture == live tail decode on ${crossCheck.tiles}/9 tiles, ${crossCheck.layers} layers.`);

// ---- 2. textures: REFERENCE payloads -> DataTexture (cache per TexID) ----
// The ISO ships no texture container; joins close against CD_JAN_2003
// Textures.ark. REFERENCE — NOT ISO truth (HUD + result labels).
const texCache = new Map(); // texId -> {tex, entryName, payloadSha256, mode}
function getTexture(texId) {
  if (texCache.has(texId)) return texCache.get(texId);
  const join = ISO_MATERIALS_FIXTURE.textureJoin.perTexId.find((r) => r.texId === texId);
  if (!join || !join.joinClosed) {
    // STRICT_ISO diagnostic fallback for an unjoined TexID (explicit, loud on HUD)
    const c = new THREE.DataTexture(new Uint8Array([255, 80, 80, 255]), 1, 1, THREE.RGBAFormat);
    c.colorSpace = THREE.SRGBColorSpace;
    c.needsUpdate = true;
    const rec = { tex: c, entryName: null, payloadSha256: null, mode: 'STRICT_ISO_DIAGNOSTIC_COLOR' };
    texCache.set(texId, rec);
    return rec;
  }
  const payloadRec = ISO_TEXTURE_PAYLOADS[texId];
  const payload = b64ToU8(payloadRec.tgaB64);
  const decoded = decodeTga2(payload); // STRICT TGA 2.0 24bpp subset — loud failures
  const tex = new THREE.DataTexture(decoded.rgba, decoded.width, decoded.height, THREE.RGBAFormat);
  tex.colorSpace = THREE.SRGBColorSpace;          // authored sRGB — GPU decode to LINEAR
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;   // explicit tiling (world UV)
  tex.magFilter = THREE.LinearFilter;
  tex.minFilter = THREE.LinearMipmapLinearFilter; // mipmapped filtering (explicit)
  tex.generateMipmaps = true;
  tex.anisotropy = 4;
  tex.needsUpdate = true;
  const rec = { tex, entryName: payloadRec.entryName, payloadSha256: payloadRec.payloadSha256, mode: 'REFERENCE' };
  texCache.set(texId, rec);
  return rec;
}

// ---- 3. per-tile splat meshes: weights -> VERTEX ATTRIBUTES ----
const SUN_DIR_N = SUN_DIR.clone().normalize();
const splatGroup = new THREE.Group();
splatGroup.visible = false;
scene.add(splatGroup);
const splatTiles = [];
let maxOverlays = 0;

// =====================================================================
// W06 — MULTIPATCH STREAMING state (declared early: applyEnv + HUD read it;
// populated by the background stream task further below, never blocking init)
// =====================================================================
const WIN_N = 5;                        // expansion window size (contract §7)
const OVERLAY_CAP_RING = 13;            // position+normal+13 weight attrs = 15 vertex attributes (WebGL2 minimum guarantee 16 — a 15-cap hit 'Too many attributes' on real hardware); capped tiles reported
const MAX_STREAM_CACHE = 25;            // explicit cache limit; the 5x5 window never exceeds it (documented in the report)
const streamDiagGroup = new THREE.Group(); // ring tiles in DIAGNOSTIC mode (flat color, same as core region mesh)
scene.add(streamDiagGroup);
const streamDiagMaterial = new THREE.MeshLambertMaterial({ color: 0x9a8f7a, wireframe: false });
const streamSplatTiles = [];            // ring tile records (same shape as core splatTiles records)
const tileStreamCache = new Map();      // W06 cache: keyed by TILE NAME -> record
const w06StreamState = {
  job: 'W06_MULTIPATCH_STREAMING', attempt: 'W06_a1',
  startedUtc: null, complete: false, failed: false,
  window: null, planned: 0, decoded: 0, loaded: 0,
  oceanSkipped: [], errors: [], cappedOverlays: [],
  cacheEvictions: 0, firstTileVisibleAt: null, completedUtc: null,
  framesAtFirstTile: null, // framesRendered when the FIRST ring tile appeared — render-first proof
};

for (let ty = 0; ty < patch.n; ty++) {
  for (let tx = 0; tx < patch.n; tx++) {
    const tile = patch.tiles[ty][tx];
    const fx = fixtureTilesByName.get(tile.name);
    const base = fx.materials[0];        // position-0 named record = BASE (audited base-first rule)
    const overlays = fx.materials.slice(1);
    maxOverlays = Math.max(maxOverlays, overlays.length);

    // geometry: the tile's own 32x32 sample block (disjoint tiles — ORIGINAL_DATA
    // discipline; region seams already recorded by PETerrainRegion)
    const S = 32;
    const positions = new Float32Array(S * S * 3);
    for (let ly = 0; ly < S; ly++) {
      for (let lx = 0; lx < S; lx++) {
        const vx = tx * S + lx, vy = ty * S + ly;
        const raw = region.rawSample(vx, vy);
        const meters = raw / 128; // CURRENT_RUNTIME_CALIBRATION (PETerrainCore semantics)
        const i = (ly * S + lx) * 3;
        positions[i] = vx * 2; positions[i + 1] = meters; positions[i + 2] = vy * 2;
      }
    }
    const quads = (S - 1) * (S - 1);
    const indices = new Uint32Array(quads * 6);
    let q = 0;
    for (let ly = 0; ly < S - 1; ly++) {
      for (let lx = 0; lx < S - 1; lx++) {
        const a = ly * S + lx, b = a + 1, c = a + S, d = c + 1;
        indices[q++] = a; indices[q++] = c; indices[q++] = b;
        indices[q++] = b; indices[q++] = c; indices[q++] = d;
      }
    }
    const tg = new THREE.BufferGeometry();
    tg.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    tg.setIndex(new THREE.BufferAttribute(indices, 1));
    tg.computeVertexNormals();

    // per-vertex overlay weights from the 16x16 masks (2x2 height samples per
    // mask cell — audited materialX = heightX >> 1 mapping; NEAREST cell,
    // byte-faithful, no interpolation)
    const weightAttrs = [];
    overlays.forEach((ov, oi) => {
      const mask = b64ToU8(ov.maskB64);
      const w = new Float32Array(S * S);
      for (let ly = 0; ly < S; ly++) {
        for (let lx = 0; lx < S; lx++) {
          const cx = lx >> 1, cy = ly >> 1;
          w[ly * S + lx] = mask[cy * 16 + cx] / 255;
        }
      }
      tg.setAttribute(`wOv${oi}`, new THREE.BufferAttribute(w, 1));
      weightAttrs.push(`wOv${oi}`);
    });

    // ShaderMaterial: unrolled base->overlay mix chain (audited data model)
    const uniforms = {
      uBase: { value: getTexture(base.id).tex },
      uVRepeat: { value: UV_REPEAT },
      uSunDir: { value: SUN_DIR_N },
      uSunColor: { value: new THREE.Color(0xffffff).multiplyScalar(2.5) },
      uAmbient: { value: 1.0 },
      // W14 fog (gb12 FOG_Z_LINEAR model — linear blend toward fog color
      // between near and far, in VIEW distance; explicit because a custom
      // ShaderMaterial does not consume scene.fog automatically):
      uFogColor: { value: env.fog.enabled ? fogState.color.clone() : new THREE.Color(0, 0, 0) },
      uFogNear: { value: env.fog.enabled ? fogState.near : Infinity },
      uFogFar: { value: env.fog.enabled ? fogState.far : Infinity },
    };
    overlays.forEach((ov, oi) => { uniforms[`uOv${oi}`] = { value: getTexture(ov.id).tex }; });

    const varyingDecl = overlays.map((_, oi) => `varying float vW${oi};`).join('\n');
    const attrDecl = overlays.map((_, oi) => `attribute float wOv${oi};`).join('\n');
    const assignV = overlays.map((_, oi) => `vW${oi} = wOv${oi};`).join('\n');
    const mixChain = overlays.map((_, oi) =>
      `col = mix(col, texture2D(uOv${oi}, tuv).rgb, clamp(vW${oi}, 0.0, 1.0));`).join('\n');
    const uniformDecl = overlays.map((_, oi) => `uniform sampler2D uOv${oi};`).join('\n');

    const vert = `
      ${attrDecl}
      varying vec3 vWorldPos;
      varying vec3 vNormal;
      varying float vViewDist;
      ${varyingDecl}
      void main() {
        vWorldPos = position;
        vNormal = normal;
        vViewDist = -(modelViewMatrix * vec4(position, 1.0)).z; // view distance (fog)
        ${assignV}
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;
    const frag = `
      uniform sampler2D uBase;
      ${uniformDecl}
      uniform float uVRepeat;
      uniform vec3 uSunDir;
      uniform vec3 uSunColor;
      uniform float uAmbient;
      uniform vec3 uFogColor;
      uniform float uFogNear;
      uniform float uFogFar;
      varying vec3 vWorldPos;
      varying vec3 vNormal;
      varying float vViewDist;
      ${varyingDecl}
      void main() {
        vec2 tuv = vWorldPos.xz / uVRepeat;   // world-space UV (RECONSTRUCTION_CANDIDATE repeat)
        vec3 col = texture2D(uBase, tuv).rgb; // sRGB texture -> GPU decodes to LINEAR
        ${mixChain}
        float ndl = max(dot(normalize(vNormal), normalize(uSunDir)), 0.0);
        vec3 lit = col * (uAmbient + uSunColor * ndl);
        // W14 fog: gb12 FOG_Z_LINEAR semantics — linear view-distance blend
        // toward the fog color between uFogNear and uFogFar (near=Infinity
        // when the fog layer is toggled off -> factor stays 0).
        float fogF = clamp((vViewDist - uFogNear) / max(uFogFar - uFogNear, 1e-4), 0.0, 1.0);
        lit = mix(lit, uFogColor, fogF);
        gl_FragColor = vec4(lit, 1.0);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }
    `;
    const tmat = new THREE.ShaderMaterial({ uniforms, vertexShader: vert, fragmentShader: frag });
    const tmesh = new THREE.Mesh(tg, tmat);
    splatGroup.add(tmesh);
    splatTiles.push({
      name: tile.name,
      base: { id: base.id, name: base.name, mode: getTexture(base.id).mode },
      overlays: overlays.map((ov) => ({ id: ov.id, name: ov.name, mode: getTexture(ov.id).mode })),
      layerCount: fx.materials.length,
      mesh: tmesh,
    });
  }
}
const layerTotal = splatTiles.reduce((a, t) => a + t.layerCount, 0);
const joinedLayers = [...texCache.values()].filter((r) => r.mode === 'REFERENCE').length;
log(`splat built: ${splatTiles.length} tile meshes, ${layerTotal} layers, max ${maxOverlays} overlays/tile, ${joinedLayers} REFERENCE textures loaded.`);

// W14: apply the layered environment now that the splat uniforms exist
applyEnv();
log(`W14 env: sky=${env.sky.enabled ? 'ON' : 'OFF'} fog=${env.fog.enabled ? `ON(FOG_Z_LINEAR near ${fogState.near.toFixed(0)}m far ${fogState.far.toFixed(0)}m)` : 'OFF'} — all layers ENGINEERING_PREVIEW values (fog MODEL source-backed gb12)`);

// ---- 4. material mode switch (INITIAL=diagnostic, MATERIAL=splat) ----
let materialMode = 'diagnostic';
function setMaterialMode(mode) {
  if (mode !== 'diagnostic' && mode !== 'splat') throw new Error(`[W05] unknown material mode ${mode}`);
  materialMode = mode;
  mesh.visible = mode === 'diagnostic';
  splatGroup.visible = mode === 'splat';
  streamDiagGroup.visible = mode === 'diagnostic'; // W06: ring tiles follow the same mode toggle
  renderer.render(scene, camera);
  framesRendered++;
  return { mode, canvasStats: canvasStats(`mode_${mode}`) };
}

// ---------- fly controls (simple WSAD + mouse drag; own implementation) ----------
const keys = new Set();
let yaw = Math.atan2(center.x - camera.position.x, center.z - camera.position.z);
let pitch = -0.35;
let drag = false, lastX = 0, lastY = 0;
let movedDistance = 0, keyEvents = 0, manualMoves = 0; // framesRendered declared in the W14 block above

renderer.domElement.addEventListener('mousedown', (e) => { drag = true; lastX = e.clientX; lastY = e.clientY; });
window.addEventListener('mouseup', () => { drag = false; });
window.addEventListener('mousemove', (e) => {
  if (!drag) return;
  yaw -= (e.clientX - lastX) * 0.005;
  pitch = Math.max(-1.4, Math.min(1.4, pitch - (e.clientY - lastY) * 0.005));
  lastX = e.clientX; lastY = e.clientY; manualMoves++;
});
window.addEventListener('keydown', (e) => { keys.add(e.code); keyEvents++; });
window.addEventListener('keyup', (e) => keys.delete(e.code));

function applyLook() {
  const dir = new THREE.Vector3(Math.sin(yaw) * Math.cos(pitch), Math.sin(pitch), Math.cos(yaw) * Math.cos(pitch));
  const target = camera.position.clone().add(dir);
  camera.up.set(0, 1, 0);
  camera.lookAt(target);
}
const FLY_SPEED = 40; // m/s baseline (display-scale meters)
let lastT = performance.now(); // manual delta-time (THREE.Clock deprecated in r187)
function tick() {
  const now = performance.now();
  const dt = Math.min((now - lastT) / 1000, 0.1);
  lastT = now;
  const sp = FLY_SPEED * (keys.has('ShiftLeft') || keys.has('ShiftRight') ? 3 : 1) * dt;
  const fwd = new THREE.Vector3(Math.sin(yaw), 0, Math.cos(yaw));
  const right = new THREE.Vector3(Math.sin(yaw - Math.PI / 2), 0, Math.cos(yaw - Math.PI / 2));
  const before = camera.position.clone();
  if (keys.has('KeyW')) camera.position.addScaledVector(fwd, sp);
  if (keys.has('KeyS')) camera.position.addScaledVector(fwd, -sp);
  if (keys.has('KeyA')) camera.position.addScaledVector(right, -sp);
  if (keys.has('KeyD')) camera.position.addScaledVector(right, sp);
  if (keys.has('KeyR')) camera.position.y += sp;
  if (keys.has('KeyF')) camera.position.y -= sp;
  movedDistance += camera.position.distanceTo(before);
  applyLook();
  skyDome.position.copy(camera.position); // sky dome follows the camera (no parallax)
  renderer.render(scene, camera);
  framesRendered++;
  requestAnimationFrame(tick);
}
applyLook();
renderer.render(scene, camera);
framesRendered++;
requestAnimationFrame(tick);

// =====================================================================
// W06 — MULTIPATCH STREAMING (5x5 expansion, async per-tile decode)
// The fly loop above ALREADY renders the core 3x3; ring tiles below are
// decoded one by one in a background task (NOT awaited — no sync blocking)
// and appear in subsequent frames as they decode, near-origin-first.
// =====================================================================
w06StreamState.window = windowContainingCore(patch, WIN_N);
const ringPlan = streamRingPlan(patch, w06StreamState.window);
w06StreamState.planned = ringPlan.length;
log(`W06 stream: window ${w06StreamState.window.n}x${w06StreamState.window.n} @ grid ${w06StreamState.window.originX},${w06StreamState.window.originY} (${w06StreamState.window.rule}); ${ringPlan.length} ring candidates, near-origin-first; ocean skip rule: ${OCEAN_SKIP_RULE}`);

// ---- explicit cache eviction (never triggers for this 5x5 window; wired
// anyway): evict the stream tile FARTHEST from the camera, dispose geometry
// + materials, remove from scene groups and from the splat/fog registry.
function disposeStreamRecord(rec) {
  splatGroup.remove(rec.mesh);
  streamDiagGroup.remove(rec.diagMesh);
  rec.mesh.material.dispose();
  rec.geometry.dispose(); // shared between the splat + diag meshes — disposed ONCE
  streamSplatTiles.splice(streamSplatTiles.indexOf(rec), 1);
}
function evictIfNeeded() {
  while (tileStreamCache.size > MAX_STREAM_CACHE) {
    let far = null, farD = -1;
    for (const rec of tileStreamCache.values()) {
      const d = camera.position.distanceToSquared(rec.center);
      if (d > farD) { farD = d; far = rec; }
    }
    tileStreamCache.delete(far.name);
    disposeStreamRecord(far);
    w06StreamState.cacheEvictions++;
    log(`W06 stream: cache eviction ${far.name} (limit ${MAX_STREAM_CACHE})`);
  }
}

// ---- build ONE streamed ring tile: 32x32 RAW-height mesh + live tail
// decode -> splat ShaderMaterial (same audited template as the core; the
// W05 material fixture does NOT cover ring tiles — tails decode LIVE through
// the repo TdfMaterialTailDecoder; textures resolve through the SAME fixture
// join, unknown TexIDs fall back to the existing STRICT_ISO diagnostic color).
function buildStreamTile(tile, stats) {
  const S = 32;
  const lx0 = (tile.gridX - w06StreamState.window.originX) * S;
  const ly0 = (tile.gridY - w06StreamState.window.originY) * S;
  const positions = new Float32Array(S * S * 3);
  for (let ly = 0; ly < S; ly++) {
    for (let lx = 0; lx < S; lx++) {
      const raw = tile.heights[ly * S + lx];
      const i = (ly * S + lx) * 3;
      positions[i] = (lx0 + lx) * 2;          // 2 m/sample (CURRENT_RUNTIME_CALIBRATION)
      positions[i + 1] = raw / 128;           // u16/128 -> m (CURRENT_RUNTIME_CALIBRATION)
      positions[i + 2] = (ly0 + ly) * 2;
    }
  }
  const indices = new Uint32Array((S - 1) * (S - 1) * 6);
  let q = 0;
  for (let ly = 0; ly < S - 1; ly++) {
    for (let lx = 0; lx < S - 1; lx++) {
      const a = ly * S + lx, b = a + 1, c = a + S, d = c + 1;
      indices[q++] = a; indices[q++] = c; indices[q++] = b;
      indices[q++] = b; indices[q++] = c; indices[q++] = d;
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  g.setIndex(new THREE.BufferAttribute(indices, 1));
  g.computeVertexNormals();

  // LIVE material tail decode (repo decoder — same one the W05 cross-check uses)
  const live = decodeMaterialTail(tile.tail);
  if (live.consumed !== tile.tail.byteLength) {
    throw new Error(`[W06] live tail decode consumption mismatch on ${tile.name}`);
  }
  if (live.namedMaterials.length === 0) {
    throw new Error(`[W06] ${tile.name}: no named material records in tail`);
  }
  const base = live.namedMaterials[0];       // position-0 named record = BASE (audited rule)
  let overlays = live.namedMaterials.slice(1);
  if (overlays.length > OVERLAY_CAP_RING) {
    w06StreamState.cappedOverlays.push({
      tile: tile.name, liveLayers: live.namedMaterials.length,
      kept: OVERLAY_CAP_RING, dropped: live.namedMaterials.length - 1 - OVERLAY_CAP_RING,
    });
    overlays = overlays.slice(0, OVERLAY_CAP_RING); // explicit cap: 16 samplers = WebGL2 minimum guarantee
  }

  overlays.forEach((ov, oi) => {
    const w = new Float32Array(S * S);
    for (let ly = 0; ly < S; ly++) {
      for (let lx = 0; lx < S; lx++) {
        w[ly * S + lx] = ov.mask[(ly >> 1) * 16 + (lx >> 1)] / 255; // materialX = heightX>>1 (audited)
      }
    }
    g.setAttribute(`wOv${oi}`, new THREE.BufferAttribute(w, 1));
  });

  const uniforms = {
    uBase: { value: getTexture(base.id).tex },
    uVRepeat: { value: UV_REPEAT },
    uSunDir: { value: SUN_DIR_N },
    uSunColor: { value: new THREE.Color(0xffffff).multiplyScalar(2.5) },
    uAmbient: { value: 1.0 },
    uFogColor: { value: env.fog.enabled ? fogState.color.clone() : new THREE.Color(0, 0, 0) },
    uFogNear: { value: env.fog.enabled ? fogState.near : Infinity },
    uFogFar: { value: env.fog.enabled ? fogState.far : Infinity },
  };
  overlays.forEach((ov, oi) => { uniforms[`uOv${oi}`] = { value: getTexture(ov.id).tex }; });

  const varyingDecl = overlays.map((_, oi) => `varying float vW${oi};`).join('\n');
  const attrDecl = overlays.map((_, oi) => `attribute float wOv${oi};`).join('\n');
  const assignV = overlays.map((_, oi) => `vW${oi} = wOv${oi};`).join('\n');
  const mixChain = overlays.map((_, oi) =>
    `col = mix(col, texture2D(uOv${oi}, tuv).rgb, clamp(vW${oi}, 0.0, 1.0));`).join('\n');
  const uniformDecl = overlays.map((_, oi) => `uniform sampler2D uOv${oi};`).join('\n');
  const vert = `
    ${attrDecl}
    varying vec3 vWorldPos;
    varying vec3 vNormal;
    varying float vViewDist;
    ${varyingDecl}
    void main() {
      vWorldPos = position;
      vNormal = normal;
      vViewDist = -(modelViewMatrix * vec4(position, 1.0)).z;
      ${assignV}
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `;
  const frag = `
    uniform sampler2D uBase;
    ${uniformDecl}
    uniform float uVRepeat;
    uniform vec3 uSunDir;
    uniform vec3 uSunColor;
    uniform float uAmbient;
    uniform vec3 uFogColor;
    uniform float uFogNear;
    uniform float uFogFar;
    varying vec3 vWorldPos;
    varying vec3 vNormal;
    varying float vViewDist;
    ${varyingDecl}
    void main() {
      vec2 tuv = vWorldPos.xz / uVRepeat;
      vec3 col = texture2D(uBase, tuv).rgb;
      ${mixChain}
      float ndl = max(dot(normalize(vNormal), normalize(uSunDir)), 0.0);
      vec3 lit = col * (uAmbient + uSunColor * ndl);
      float fogF = clamp((vViewDist - uFogNear) / max(uFogFar - uFogNear, 1e-4), 0.0, 1.0);
      lit = mix(lit, uFogColor, fogF);
      gl_FragColor = vec4(lit, 1.0);
      #include <tonemapping_fragment>
      #include <colorspace_fragment>
    }
  `;
  const splatMesh = new THREE.Mesh(g, new THREE.ShaderMaterial({ uniforms, vertexShader: vert, fragmentShader: frag }));
  splatGroup.add(splatMesh);
  const diagMesh = new THREE.Mesh(g, streamDiagMaterial); // SHARED geometry — disposed once
  streamDiagGroup.add(diagMesh);
  const rec = {
    name: tile.name, gridX: tile.gridX, gridY: tile.gridY, tile,
    geometry: g, mesh: splatMesh, diagMesh,
    center: new THREE.Vector3(
      positions[0] + (positions[(S - 1) * 3] - positions[0]) / 2, 0,
      positions[2] + (positions[((S - 1) * S) * 3 + 2] - positions[2]) / 2),
    stats,
    liveLayers: live.namedMaterials.length,
    base: { id: base.id, name: base.name, mode: getTexture(base.id).mode },
    overlays: overlays.map((ov) => ({ id: ov.id, name: ov.name, mode: getTexture(ov.id).mode })),
    overlaysCapped: overlays.length < live.namedMaterials.length - 1,
  };
  rec.center.set((lx0 + S / 2) * 2, 0, (ly0 + S / 2) * 2);
  streamSplatTiles.push(rec);
  return rec;
}

async function streamExpandWindow() {
  w06StreamState.startedUtc = new Date().toISOString();
  for (const cand of ringPlan) { // near-origin-first order (streamRingPlan)
    w06StreamState.decoded++; // candidates processed (decoded or failed)
    try {
      const tile = await mount.getTerrainTile({ era: ERA, gridX: cand.gridX, gridY: cand.gridY });
      const stats = tileTerrainStats(tile.heights);
      if (isOceanNodataTile(stats)) {
        w06StreamState.oceanSkipped.push({ name: tile.name, ...stats, reason: 'OCEAN_NODATA (>90% zeros — explicit skip)' });
        log(`W06 stream: ${tile.name} SKIP ocean/nodata (${stats.zeros}/1024 zero samples)`);
        continue;
      }
      const rec = buildStreamTile(tile, stats);
      tileStreamCache.set(tile.name, rec);
      evictIfNeeded(); // explicit (no-op for this window: 12 loaded << limit 25)
      w06StreamState.loaded++;
      if (w06StreamState.loaded === 1) {
        w06StreamState.firstTileVisibleAt = new Date().toISOString();
        w06StreamState.framesAtFirstTile = framesRendered; // >0 proves frames were rendered BEFORE the first ring tile appeared
      }
      log(`W06 stream: ${tile.name} loaded (${w06StreamState.loaded}/${ringPlan.length} ring — ${stats.nonZero}/1024 nonZero, maxRaw ${stats.maxRawHeight}${rec.overlaysCapped ? `, overlays CAPPED ${OVERLAY_CAP_RING}/${rec.liveLayers - 1}` : ''})`);
    } catch (err) {
      w06StreamState.errors.push({ name: cand.name, error: String(err?.message ?? err) });
      log(`W06 stream: ${cand.name} FAILED (core 3x3 fallback unaffected): ${err?.message ?? err}`);
    }
  }
  // scene-size proof (contract §7 browser probe): core 3x3 vs expanded 5x5
  const expandedBox = new THREE.Box3().union(box); // start from the CORE region bounds
  for (const rec of streamSplatTiles) expandedBox.union(new THREE.Box3().setFromObject(rec.diagMesh));
  const coreVerts = geom.positions.length / 3;
  const ringVerts = streamSplatTiles.length * 32 * 32;
  const ext = (b) => ({ x: +(b.max.x - b.min.x).toFixed(1), y: +(b.max.y - b.min.y).toFixed(1), z: +(b.max.z - b.min.z).toFixed(1) });
  w06StreamState.sceneProof = {
    coreVertexCount: coreVerts,
    expandedVertexCount: coreVerts + ringVerts,
    coreWorldExtentM: ext(box),
    expandedWorldExtentM: ext(expandedBox),
    coreWorldBounds: { min: [box.min.x, box.min.y, box.min.z], max: [box.max.x, box.max.y, box.max.z] },
    expandedWorldBounds: { min: [expandedBox.min.x, expandedBox.min.y, expandedBox.min.z], max: [expandedBox.max.x, expandedBox.max.y, expandedBox.max.z] },
    largerThan3x3: (expandedBox.max.x - expandedBox.min.x) > (box.max.x - box.min.x) + 1 &&
      (expandedBox.max.z - expandedBox.min.z) > (box.max.z - box.min.z) + 1 &&
      (coreVerts + ringVerts) > coreVerts,
  };
  w06StreamState.complete = true;
  w06StreamState.completedUtc = new Date().toISOString();
  log(`W06 stream COMPLETE: ${w06StreamState.loaded}/${ringPlan.length} ring tiles loaded, ${w06StreamState.oceanSkipped.length} ocean-skipped, ${w06StreamState.errors.length} errors — visible tiles now ${9 + w06StreamState.loaded} (core 9 + ring ${w06StreamState.loaded}).`);
}
// NOT awaited — non-blocking background task; per-tile failures are caught
// above, so the fixture-pinned core 3x3 keeps rendering regardless (fallback).
const w06Task = streamExpandWindow();
w06Task.catch((e) => {
  w06StreamState.failed = true;
  w06StreamState.complete = true;
  w06StreamState.errors.push({ name: '__stream_task__', error: String(e?.message ?? e) });
});

// ---------- CANVAS PIXEL STATS (deterministic diversity stat) ----------
let statsCanvas = null, statsCtx = null;
function canvasStats(label) {
  if (!statsCanvas) {
    statsCanvas = document.createElement('canvas');
    statsCanvas.width = 110; statsCanvas.height = 82;
    statsCtx = statsCanvas.getContext('2d', { willReadFrequently: true });
  }
  statsCtx.drawImage(renderer.domElement, 0, 0, 110, 82);
  const d = statsCtx.getImageData(0, 0, 110, 82).data;
  let nonBg = 0, sumLum = 0;
  const colors = new Set();
  const buckets = new Map();      // 32-level quantized color buckets (all pixels)
  const bucketsNonBg = new Map();  // terrain pixels only — the background bucket
                                  // must NOT dominate the material-diversity stat
  for (let i = 0; i < d.length; i += 4) {
    const [r, g, b] = [d[i], d[i + 1], d[i + 2]];
    colors.add((r << 16) | (g << 8) | b);
    const isBg = Math.abs(r - 0x0a) <= 2 && Math.abs(g - 0x0a) <= 2 && Math.abs(b - 0x12) <= 2;
    if (!isBg) nonBg++;
    sumLum += 0.2126 * r + 0.7152 * g + 0.0722 * b;
    const key = ((r >> 5) << 10) | ((g >> 5) << 5) | (b >> 5);
    buckets.set(key, (buckets.get(key) ?? 0) + 1);
    if (!isBg) bucketsNonBg.set(key, (bucketsNonBg.get(key) ?? 0) + 1);
  }
  const px = d.length / 4;
  const topBucket = Math.max(...buckets.values());
  const topBucketNonBg = bucketsNonBg.size ? Math.max(...bucketsNonBg.values()) : 0;
  return {
    label, sampledPixels: px,
    nonBackgroundFraction: +(nonBg / px).toFixed(4),
    uniqueColors: colors.size,
    topBucketFraction: +(topBucket / px).toFixed(4),
    topBucketFractionNonBg: +(topBucketNonBg / Math.max(nonBg, 1)).toFixed(4),
    uniqueBucketsNonBg: bucketsNonBg.size,
    meanLuminance: +(sumLum / px).toFixed(2),
  };
}

// ---------- programmatic movement hook (BROWSER PROOF, CDP-driven) ----------
window.__w03MoveCamera = (dx, dy, dz) => {
  const before = { x: camera.position.x, y: camera.position.y, z: camera.position.z };
  camera.position.set(before.x + dx, before.y + dy, before.z + dz);
  applyLook();
  renderer.render(scene, camera); // synchronous fresh frame (headless rAF is idle)
  framesRendered++;
  const after = { x: camera.position.x, y: camera.position.y, z: camera.position.z };
  window.__W03_MOVEMENT__ = {
    requested: { dx, dy, dz },
    cameraBefore: before,
    cameraAfter: after,
    movedDistanceMeters: Math.hypot(dx, dy, dz),
    framesRenderedAtMove: framesRendered,
    canvasStatsAfterMove: canvasStats('after_move'),
    yaw, pitch,
  };
  return window.__W03_MOVEMENT__;
};

// ---------- W05 hooks (mode switch + material stats) ----------
window.__w05SetMaterialMode = (mode) => setMaterialMode(mode);
window.__w05MaterialStats = () => ({
  mode: materialMode,
  uvRepeatMeters: UV_REPEAT,
  layerTotal,
  tilesWithSplat: splatTiles.length,
  maxOverlaysPerTile: maxOverlays,
  referenceTextures: [...texCache.values()].filter((r) => r.mode === 'REFERENCE').length,
  strictIsoFallbackTextures: [...texCache.values()].filter((r) => r.mode === 'STRICT_ISO_DIAGNOSTIC_COLOR').length,
  textureSource: {
    era: 'CD_JAN_2003', container: 'Textures.ark',
    sha256Prefix: ISO_MATERIALS_FIXTURE.textureJoin.referenceContainer.sha256.slice(0, 16),
    pinOk: ISO_MATERIALS_FIXTURE.textureJoin.referenceContainer.pinOk,
    label: 'REFERENCE — NOT ISO truth (ISO ships no texture container)',
  },
  crossCheck: { tiles: crossCheck.tiles, layers: crossCheck.layers, mismatches: crossCheck.mismatches.length },
  perTile: splatTiles.map((t) => ({
    tile: t.name, layers: t.layerCount,
    base: t.base, overlays: t.overlays,
  })),
  canvasStats: canvasStats(`hook_${materialMode}`),
});

// ---------- W14 hooks (layered environment: sky / fog / light) ----------
window.__w14SetEnv = (patch) => {
  if (typeof patch !== 'object' || patch === null) throw new Error('[W14] patch must be an object');
  if (typeof patch.sky === 'boolean') env.sky.enabled = patch.sky;
  if (typeof patch.fog === 'boolean') env.fog.enabled = patch.fog;
  if (Number.isFinite(patch.fogNear)) fogState.near = patch.fogNear;
  if (Number.isFinite(patch.fogFar)) fogState.far = patch.fogFar;
  if (Number.isFinite(patch.sunIntensity)) env.light.sunIntensity = patch.sunIntensity;
  if (Number.isFinite(patch.ambientIntensity)) env.light.ambientIntensity = patch.ambientIntensity;
  const inv = envConfigInvariant(env, camera.near);
  if (!inv.ok) throw new Error(`[W14] patched env invalid: ${inv.errors.join('; ')}`);
  applyEnv();
  return window.__w14EnvStats();
};
window.__w14EnvStats = () => ({
  layers: layerTable(),
  gb12FogModel: GB12_FOG_MODEL,
  state: {
    sky: { enabled: env.sky.enabled, zenith: [...env.sky.zenith], horizon: [...env.sky.horizon], ground: [...env.sky.ground] },
    fog: { enabled: env.fog.enabled, near: fogState.near, far: fogState.far, color: [fogState.color.r, fogState.color.g, fogState.color.b], gb12: { ...env.fog.gb12 } },
    light: { sunIntensity: sun.intensity, ambientIntensity: ambient.intensity, sunDir: [sun.position.x, sun.position.y, sun.position.z] },
  },
  invariant: envConfigInvariant(env, camera.near),
  // orientation self-test of the preview sky gradient (pure math, no GPU):
  skyOrientation: {
    zenithSample: skyColorAt(1.0, env.sky.zenith, env.sky.horizon, env.sky.ground),
    horizonSample: skyColorAt(0.0, env.sky.zenith, env.sky.horizon, env.sky.ground),
    nadirSample: skyColorAt(-1.0, env.sky.zenith, env.sky.horizon, env.sky.ground),
    zenithIsZenith: JSON.stringify(skyColorAt(1.0, env.sky.zenith, env.sky.horizon, env.sky.ground)) === JSON.stringify(env.sky.zenith),
    horizonIsHorizon: JSON.stringify(skyColorAt(0.0, env.sky.zenith, env.sky.horizon, env.sky.ground)) === JSON.stringify(env.sky.horizon),
  },
  canvasStats: canvasStats(`env_sky${env.sky.enabled ? 1 : 0}_fog${env.fog.enabled ? 1 : 0}`),
  materialMode,
});

// ---------- W06 hooks (streaming stats + camera grid cell) ----------
window.__w06StreamStats = () => {
  const win = w06StreamState.window;
  const camGridX = Math.floor(camera.position.x / 64) + (win ? win.originX : 0);
  const camGridY = Math.floor(camera.position.z / 64) + (win ? win.originY : 0);
  const totalVisible = 9 + w06StreamState.loaded; // core 9 + loaded ring (all loaded tiles are visible — no culling, by scope)
  return {
    job: 'W06_MULTIPATCH_STREAMING', attempt: 'W06_a1',
    stream: {
      complete: w06StreamState.complete, failed: w06StreamState.failed,
      planned: w06StreamState.planned, decoded: w06StreamState.decoded,
      loaded: w06StreamState.loaded, oceanSkipped: w06StreamState.oceanSkipped,
      errors: w06StreamState.errors, cappedOverlays: w06StreamState.cappedOverlays,
      order: ringPlan.map((r) => r.name),
    },
    window: win,
    cache: {
      keyedBy: 'tile name', size: tileStreamCache.size, limit: MAX_STREAM_CACHE,
      evictions: w06StreamState.cacheEvictions,
      disposal: 'geometry disposed once (shared splat+diag), splat material disposed; evicts farthest-from-camera',
      note: 'limit 25 never reached for this 5x5 window (12 loaded ring tiles) — eviction wired but inactive, reported explicitly',
    },
    tiles: {
      core: 9, ringLoaded: w06StreamState.loaded, totalVisible,
      windowTiles: win ? win.n * win.n : null,
      oceanSkippedCount: w06StreamState.oceanSkipped.length,
    },
    renderedArea: win ? {
      gridXRange: [win.originX, win.originX + win.n - 1],
      gridYRange: [win.originY, win.originY + win.n - 1],
      worldMeters: { x: [0, win.n * 64], z: [0, win.n * 64] },
      tileCount: totalVisible,
    } : null,
    wholeMapAvailable: {   // SEPARATE (contract: rendered range vs whole-map availability)
      gridX: ISO_GRID.GRID_X, gridY: ISO_GRID.GRID_Y,
      regularTiles: patch.census.regularTiles, sentinel: patch.census.sentinelEntries,
      renderedHere: totalVisible,
      renderedFraction: +(totalVisible / patch.census.regularTiles).toFixed(5),
    },
    camera: {
      x: camera.position.x, y: camera.position.y, z: camera.position.z,
      gridCell: { gridX: camGridX, gridY: camGridY, tile: tileNameFromGridLocal(camGridX, camGridY) },
    },
    overlayCapRing: { cap: OVERLAY_CAP_RING, reason: 'position+normal+13 weight attributes = 15 vertex attributes (WebGL2 minimum 16; 15-cap failed with a real shader error)', cappedTiles: w06StreamState.cappedOverlays },
    canvasStats: canvasStats('w06_stream'),
    materialMode,
  };
};
function tileNameFromGridLocal(gx, gy) {
  if (gx < 0 || gx > 219 || gy < 0 || gy > 235) return null; // outside regular grid (camera can fly out)
  return gx.toString(16).padStart(4, '0') + gy.toString(16).padStart(4, '0') + '.tdf';
}

// ---------- HUD provenance (era, SHA prefix, tiles, counts, material modes) ----------
function updateHud() {
  const st = window.__w05MaterialStats();
  HUD.textContent =
`W05 ISO_MATERIALS_SPLAT — mode: ${materialMode.toUpperCase()} — ENGINEERING PREVIEW (light/background NOT original PE environment)
era: ${ERA} (PE 5.1.0.0, PC Gamer Nov2003 ISO) | terrain: STRICT_ISO (recovered 50.bnt via /iso/50.bnt, SHA ${mountRec.actualSha256.slice(0, 12)}… verified=${mountHashOk})
material mode per layer: ${st.referenceTextures}/${st.referenceTextures + st.strictIsoFallbackTextures} layers REFERENCE (CD_JAN_2003 Textures.ark, SHA ${st.textureSource.sha256Prefix}… pin=${st.textureSource.pinOk}) — textures NOT ISO truth
texture source: REFERENCE_RECONSTRUCTION CD_JAN_2003 (ISO corpus ships NO texture container; missing edge documented in W05_TAIL_FIXTURE.json)
counts: tiles ${st.tilesWithSplat}, layers ${st.layerTotal} (max ${st.maxOverlaysPerTile} overlays/tile), cross-check fixture==live: ${st.crossCheck.layers} layers / ${st.crossCheck.tiles} tiles, 0 mismatches
offsetbase: mask@record+56 (fixture-derived, evidence E1-E4) | weights: 16x16 masks -> vertex attrs, NEAREST cell (materialX = heightX>>1), sums>255 = ORIGINAL DATA
UV: world-space repeat ${st.uvRepeatMeters} m (RECONSTRUCTION_CANDIDATE), RepeatWrapping, mipmap linear | colorspace: sRGB textures -> linear lighting -> sRGB out | alpha: 24bpp opaque, weight = blend
patch 3x3 @ grid ${patch.originGridX},${patch.originGridY}: ${tileNames.join(' ')}
W06 STREAM: ${w06StreamState.complete ? (w06StreamState.failed ? 'FAILED' : 'COMPLETE') : 'STREAMING…'} — ring ${w06StreamState.loaded}/${w06StreamState.planned} loaded, ${w06StreamState.oceanSkipped.length} ocean-skipped (>90% zeros), ${w06StreamState.errors.length} errors, cache ${tileStreamCache.size}/${MAX_STREAM_CACHE} (evictions ${w06StreamState.cacheEvictions}), order near-origin-first
tiles visible: ${9 + w06StreamState.loaded} (core 9 + ring ${w06StreamState.loaded}; all loaded tiles drawn — no culling by scope)
RENDERED AREA (this page): grid x ${w06StreamState.window.originX}..${w06StreamState.window.originX + w06StreamState.window.n - 1} × y ${w06StreamState.window.originY}..${w06StreamState.window.originY + w06StreamState.window.n - 1} (${w06StreamState.window.n}x${w06StreamState.window.n} window = ${w06StreamState.window.n * 64}x${w06StreamState.window.n * 64} m @ 2 m/sample)
WHOLE MAP AVAILABLE (index census — NOT rendered here): ${ISO_GRID.GRID_X}x${ISO_GRID.GRID_Y} grid = ${patch.census.regularTiles} regular tiles (+${patch.census.sentinelEntries} sentinel) — this page draws ${((9 + w06StreamState.loaded) / patch.census.regularTiles * 100).toFixed(2)}% of the map
heights: RAW u16 max ${patch.patchStats.maxRawHeight} | zeros(nodata/water) ${patch.patchStats.zeroSamples}/${9 * 1024} | display: u16/128 -> m (CURRENT_RUNTIME_CALIBRATION), 2 m/sample
W14 ENVIRONMENT LAYERS (per-layer provenance + toggles — none is a recovered original effect):
  sky: ${env.sky.enabled ? 'ON' : 'OFF'} ENGINEERING_PREVIEW (procedural gradient; 0 cubemaps/skydomes recovered in ISO/CD corpus) — KeyN / __w14SetEnv
  fog: ${env.fog.enabled ? `ON near ${fogState.near.toFixed(0)}m far ${fogState.far.toFixed(0)}m` : 'OFF'} MODEL=SOURCE_BACKED (gb12 NiFogProperty FOG_Z_LINEAR), VALUES=ENGINEERING_PREVIEW (environmentzones PLAUSIBLE-UNVERIFIED excluded) — KeyB / __w14SetEnv
  light: ENGINEERING_PREVIEW sun ${sun.intensity.toFixed(1)} ambient ${ambient.intensity.toFixed(1)} (W03/W05 diagnostic, kept explicit) — KeyL / __w14SetEnv
camera: ${camera.position.x.toFixed(1)}, ${camera.position.y.toFixed(1)}, ${camera.position.z.toFixed(1)} | moved ${movedDistance.toFixed(1)} m | frames ${framesRendered}
controls: WASD move, mouse drag look, R/F up/down, Shift x3 | M mode toggle (M key: diagnostic/splat)`;
}
setInterval(updateHud, 500);
window.addEventListener('keydown', (e) => {
  if (e.code === 'KeyM') setMaterialMode(materialMode === 'diagnostic' ? 'splat' : 'diagnostic');
  if (e.code === 'KeyN') window.__w14SetEnv({ sky: !env.sky.enabled });
  if (e.code === 'KeyB') window.__w14SetEnv({ fog: !env.fog.enabled });
  if (e.code === 'KeyL') window.__w14SetEnv({ sunIntensity: env.light.sunIntensity > 2.5 ? 1.0 : (env.light.sunIntensity >= 1.0 ? 2.5 : env.light.sunIntensity + 0.75) });
});

// ---------- LIVE state hook (BROWSER PROOF) ----------
window.__w03State = () => ({
  framesRendered, movedDistanceMeters: movedDistance, keyEvents, manualLookMoves: manualMoves,
  camera: { x: camera.position.x, y: camera.position.y, z: camera.position.z },
  materialMode,
});

// ---------- results / provenance chain ----------
const provenance = region.provenanceList();
const result = {
  job: 'W05_ISO_MATERIALS_SPLAT',
  attempt: 'W05_a1',
  sourceLabel: 'STRICT_ISO',
  chain: 'ISO 50.bnt bytes -> PESourceMount(ISO_5_1_0_0, BUNT) -> TerrainTile -> PETerrainRegion -> Three r187 (+ W05 material splat: Node fixture tails -> vertex weights + REFERENCE textures)',
  era: ERA,
  mount: {
    path: TERRAIN_URL,
    physicalSource: mountRec.path,
    format: 'BUNT',
    hashVerified: mountHashOk,
    actualSha256: mountRec.actualSha256,
    expectedSha256Prefix: ISO_SHA256_PIN.slice(0, 16),
    bytesFetched: 118016977,
  },
  indexCensus: { ...patch.census, gridX: ISO_GRID.GRID_X, gridY: ISO_GRID.GRID_Y },
  patch: {
    originGridX: patch.originGridX, originGridY: patch.originGridY, n: patch.n,
    tileNames, patchesTried: patch.patchesTried,
    selectionRule: patch.selectionRule,
    patchStats: patch.patchStats,
  },
  region: {
    sampleGridX: geom.sampleGridX, sampleGridY: geom.sampleGridY,
    worldHeightMinM: box.min.y, worldHeightMaxM: box.max.y,
    rawHeightMin: patch.patchStats.minRawHeight, rawHeightMax: patch.patchStats.maxRawHeight,
    nodataZeroSamples: patch.patchStats.zeroSamples,
    seamDiagnostic: region.tileSeamDiagnostic,
  },
  displayScale: {
    u16PerMeter: 128, label: 'CURRENT_RUNTIME_CALIBRATION',
    meterPerSampleHorizontal: 2,
  },
  materials: {
    tailDecode: {
      source: 'Node fixture (w05_tail_fixture.mjs) via IsoMaterialsFixture.js; live cross-check via TdfMaterialTailDecoder',
      offsetbase: { maskStartRecordRelative: 56, provenance: 'fixture-derived evidence E1-E4 (W05_TAIL_FIXTURE.json)' },
      crossCheck: { tiles: crossCheck.tiles, layers: crossCheck.layers, mismatches: 0 },
      layerTotal, maxOverlaysPerTile: maxOverlays,
      baseRule: 'position-0 named record = BASE (Stone04 all-255 9/9 tiles)',
      weightSemantics: 'INDEPENDENT alpha overlays, sums>255 = ORIGINAL DATA (no renormalization)',
    },
    textureJoin: {
      isoTextureContainerExists: false,
      referenceContainer: ISO_MATERIALS_FIXTURE.textureJoin.referenceContainer,
      perTexId: ISO_MATERIALS_FIXTURE.textureJoin.perTexId,
      joinsClosed: ISO_MATERIALS_FIXTURE.textureJoin.joinsClosed,
      distinctTexIds: ISO_MATERIALS_FIXTURE.textureJoin.distinctTexIds,
      mode: 'REFERENCE_RECONSTRUCTION (CD_JAN_2003) — NOT ISO truth',
    },
    splat: {
      weightsTo: 'vertex attributes (per overlay per tile)',
      uv: { worldSpaceRepeatMeters: UV_REPEAT, label: 'RECONSTRUCTION_CANDIDATE', wrap: 'RepeatWrapping', filter: 'linear+mipmap' },
      colorspace: 'sRGB textures (GPU decode) -> LINEAR lighting -> sRGB output',
      alpha: 'TGA 24bpp opaque; material weight = blend alpha',
      cache: 'textures per TexID, masks decoded once at load (never per frame)',
    },
  },
  heightQuery: HEIGHT_QUERY,
  environment: {
    job: 'W14_ENVIRONMENT_SKY_FOG_LIGHT', attempt: 'W14_a1',
    layers: layerTable(),
    gb12FogModel: GB12_FOG_MODEL,
    sourceMap: {
      isoSkydomeRecovered: false,
      cdTexturesArkDdsCubemaps: 0,
      cdModelsArkNiFogProperty: 0,
      environmentzonesVerdict: 'PLAUSIBLE_NOT_VERIFIED (build/container + consumer unverified) -> NOT used as original fog',
      scanArtifact: '99_Audits/PE2003_WORLD_ROSETTA_NIF_ENV_CHARACTER_6H_R1_20261030/jobs/W14/W14_environment_scan.json',
    },
    defaults: {
      sky: { enabled: DEFAULT_ENV.sky.enabled, mode: 'ENGINEERING_PREVIEW' },
      fog: { enabled: DEFAULT_ENV.fog.enabled, near: fogState.near, far: fogState.far, mode: 'ENGINEERING_PREVIEW_VALUES__SOURCE_BACKED_MODEL' },
      light: { mode: 'ENGINEERING_PREVIEW' },
    },
    toggles: { sky: 'KeyN / __w14SetEnv({sky})', fog: 'KeyB / __w14SetEnv({fog})', light: 'KeyL / __w14SetEnv({sunIntensity,ambientIntensity})' },
    invariant: envInvariant,
  },
  engineeringPreview: {
    badge: 'ENGINEERING PREVIEW — diagnostic light + dark background are NOT the original PE environment',
  },
  w06: {
    job: 'W06_MULTIPATCH_STREAMING', attempt: 'W06_a1',
    stream: w06StreamState, // LIVE reference — the probe snapshots it after stream.complete
    window: w06StreamState.window,
    oceanSkip: { rule: OCEAN_SKIP_RULE, appliesTo: 'STREAMED ring tiles only (core 3x3 keeps its original all-9-tiles behavior — W05 fixture pin + 3x3 fallback)' },
    overlayCapRing: { cap: OVERLAY_CAP_RING, reason: 'position+normal+13 overlay weight attributes = 15 vertex attributes (WebGL2 minimum guarantee 16; a 15-cap produced a real Too-many-attributes shader error in the first probe run)', cappedTiles: w06StreamState.cappedOverlays },
    cache: { keyedBy: 'tile name', limit: MAX_STREAM_CACHE, eviction: 'farthest-from-camera + geometry/material disposal', evictions: w06StreamState.cacheEvictions, note: 'limit 25 never reached for this 5x5 window (12 loaded ring tiles) — eviction wired, inactive, reported explicitly' },
    streamingBehavior: {
      blocking: 'NONE — background async task, NOT awaited (contract: no sync blocking)',
      renderFirst: 'fly/render loop starts on the core 3x3 BEFORE streaming; ring tiles appear per-decode in near-origin-first order',
      initAwait: 'per-tile await only inside the background task',
    },
    flyControlsAcrossTiles: 'WSAD world-space movement — no per-tile dependence; camera grid cell reported by __w06StreamStats().camera.gridCell',
    renderedAreaVsWholeMap: 'HUD reports the RENDERED window range SEPARATELY from the whole-map availability (220x236 grid = 51920 regular tiles from the W03 index census)',
    backlog: [ // RANKED (not implemented by contract scope)
      { rank: 1, item: 'frustum culling', why: 'cheapest win: ~30-50% of 21 tiles culled per frame; per-mesh bounding spheres already exist' },
      { rank: 2, item: 'LOD (per-tile mesh resolution / quadtree)', why: 'vertex cost scales linearly with visible tiles; 33x33 -> 17x17 far-tile meshes halve far-terrain cost' },
      { rank: 3, item: 'decode workers (Web Worker per tile)', why: 'BUNT fetch+inflate+TDF decode runs on the main thread today; workers keep rAF smooth beyond ~50 tiles' },
      { rank: 4, item: 'priority queue (camera-relative re-planning)', why: 'matters once windows move with the camera; static window now — near-origin-first suffices' },
    ],
  },
  renderer: { threeRevision: THREE.REVISION, backend: 'WebGLRenderer', width: W, height: H },
  canvasStatsInitial: canvasStats('initial_diagnostic'),
  canvasStatsSplat: null, // filled by __w05SetMaterialMode('splat') during the probe
  flyControls: { keys: ['KeyW', 'KeyA', 'KeyS', 'KeyD', 'KeyR', 'KeyF'], look: 'mouse drag', sprint: 'Shift', modeToggle: 'KeyM / __w05SetMaterialMode' },
  movement: {
    cameraStart: { x: cameraStart.x, y: cameraStart.y, z: cameraStart.z },
    programmaticHook: '__w03MoveCamera(dx,dy,dz) -> __W03_MOVEMENT__',
    liveStateHook: '__w03State()',
    materialModeHook: '__w05SetMaterialMode(mode) / __w05MaterialStats()',
  },
  provenanceCount: provenance.length,
  provenanceSample: provenance[0],
  fatalErrors: () => window.__W03_ERRORS__.length,
};
window.__W03__ = result;   // W03 probe compatibility (shared fields)
window.__W05__ = result;   // W05 canonical
window.__W14__ = result;    // W14 canonical (environment section)
window.__W06__ = result;    // W06 canonical (multipatch streaming section)
window.__W03_MOVEMENT__ = null;
window.__W05_MATERIAL_MODE__ = materialMode;
log(`W05 READY — patch ${patch.originGridX},${patch.originGridY}, splat ${splatTiles.length} tiles / ${layerTotal} layers, joins ${ISO_MATERIALS_FIXTURE.textureJoin.joinsClosed}/${ISO_MATERIALS_FIXTURE.textureJoin.distinctTexIds} REFERENCE, cross-check ${crossCheck.layers} layers OK, THREE r${THREE.REVISION}, mountHashVerified=${mountHashOk} | W06 stream: window ${w06StreamState.window.n}x${w06StreamState.window.n} @ ${w06StreamState.window.originX},${w06StreamState.window.originY}, ${ringPlan.length} ring candidates streaming in background`);
