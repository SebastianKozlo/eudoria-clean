// IsoEnvironment.js — W14 ENVIRONMENT_SKY_FOG_LIGHT (attempt W14_a1, 2026-10-30)
//
// Layered environment for world_iso (ISO_5_1_0_0 track, Three r187) with
// EXPLICIT provenance per layer. No silent era substitution:
//   - sky  : ENGINEERING_PREVIEW procedural gradient dome. The W14 source
//     scan found NO recovered sky asset for this track: 0 DDS cubemaps in
//     CD Jan-2003 Textures.ark (1359 DDS scanned, caps2 cube bits all 0),
//     0 NiSourceCubeMap / NiBillboardNode in CD Models.ark NIFs, and the ISO
//     corpus ships no texture container at all (W05 fixture coverage).
//   - fog  : MODEL SOURCE_BACKED (gb12 Gamebryo reference source,
//     CoreLibs/NiMain/NiFogProperty.{h,cpp} — linear z-fog: enable flag,
//     FogFunction {FOG_Z_LINEAR, FOG_RANGE_SQ, FOG_VERTEX_ALPHA}, depth
//     float, NiColor; depth semantics: 0 = no fog, 1 = fog starts at the
//     camera near plane, >1 = starts in front of it). VALUES ENGINEERING_
//     PREVIEW — no fog values recovered for this era (0 NiFogProperty in
//     CD NIFs; environmentzones 24007 RGB/fog fields PLAUSIBLE but their
//     build/container and consumer are UNVERIFIED -> NOT used as original).
//   - light: ENGINEERING_PREVIEW diagnostic sun/ambient (kept from W03/W05).
//
// Pure functions only — node-unit-testable; world_iso.js owns all THREE
// object creation and consumes this module's tables/defaults.

export const GB12_FOG_MODEL = {
  label: 'SOURCE_BACKED_MODEL_gb12_NiFogProperty',
  source:
    'gb12 Gb12_Source/CoreLibs/NiMain/NiFogProperty.{h,cpp,inl} ' +
    '(NDL Gamebryo reference source; semantic anchor only — the consuming ' +
    'PE 5.1.0.0 binary code was not scanned in W14)',
  fogFunctions: ['FOG_Z_LINEAR', 'FOG_RANGE_SQ', 'FOG_VERTEX_ALPHA'],
  depthSemantics: {
    0: 'no fogging',
    1: 'fog starts at the near plane',
    gt1: 'fog starts in front of the near plane (front = near/depth)',
  },
  serializedFields: ['flags(enable bit0, function bits1-2)', 'depth:float', 'color:RGB floats'],
};

export const ENV_LAYERS = [
  {
    layer: 'sky',
    mode: 'ENGINEERING_PREVIEW',
    source:
      'procedural neutral gradient — NO ISO/CD skydome recovered (W14 scan: ' +
      '0 DDS cubemaps in Textures.ark, 0 NiSourceCubeMap/NiBillboardNode in Models.ark)',
    consumer: 'THREE.Mesh (SphereGeometry BackSide, fog:false) + gradient ShaderMaterial',
    toggle: "hook __w14SetEnv({sky:false}) / KeyN",
  },
  {
    layer: 'fog',
    mode: 'ENGINEERING_PREVIEW_VALUES__SOURCE_BACKED_MODEL',
    source:
      'model: gb12 NiFogProperty FOG_Z_LINEAR semantics (paraphrase, pinned); ' +
      'values: NOT recovered (environmentzones 24007 PLAUSIBLE/UNVERIFIED — excluded)',
    consumer: 'THREE.Fog (linear) on diagnostic material + explicit fog uniforms in splat shader',
    toggle: "hook __w14SetEnv({fog:false}) / KeyB",
  },
  {
    layer: 'light',
    mode: 'ENGINEERING_PREVIEW',
    source:
      'diagnostic sun (2.5) + ambient (1.0) kept from W03/W05; original PE ' +
      'sun/ambient params for this era NOT recovered',
    consumer: 'THREE.DirectionalLight + THREE.AmbientLight + splat shader uSun/uAmbient uniforms',
    toggle: "hook __w14SetEnv({light:{sunIntensity,ambient}}) / KeyL cycles intensity",
  },
];

// gb12 depth -> fog front plane distance from the camera (paraphrased semantics).
// depth<=0 -> no fog (Infinity front plane); depth=1 -> front at cameraNear;
// depth>1 -> front in FRONT of the near plane (near/depth < cameraNear).
export function gb12FogFrontPlane(depth, cameraNear) {
  if (!Number.isFinite(depth) || !Number.isFinite(cameraNear) || cameraNear <= 0) {
    throw new Error('gb12FogFrontPlane: depth and cameraNear must be finite, cameraNear > 0');
  }
  if (depth <= 0) return Infinity;
  return cameraNear / depth;
}

// Map gb12 semantics onto THREE.Fog(near, far): near = front plane (clamped to
// a minimum of cameraNear so the fog never starts behind the visible frustum),
// far = the distance where blend reaches 1 (ENGINEERING_PREVIEW value).
export function fogRangeFromGb12(depth, cameraNear, fullOcclusionDistance) {
  const front = gb12FogFrontPlane(depth, cameraNear);
  if (front === Infinity) return { near: Infinity, far: Infinity, disabled: true };
  return {
    near: Math.max(front, cameraNear),
    far: fullOcclusionDistance,
    disabled: false,
  };
}

// Sky gradient sample (ENGINEERING_PREVIEW orientation math).
// dirY = normalized direction Y component (+1 zenith, 0 horizon, -1 nadir).
// Above horizon: horizon -> zenith lerp; below: horizon -> ground haze lerp.
export function skyColorAt(dirY, zenith, horizon, ground) {
  const h = typeof ground === 'undefined' ? horizon : ground;
  if ([zenith, horizon, h].some((c) => !Array.isArray(c) || c.length !== 3 ||
      c.some((v) => !Number.isFinite(v) || v < 0 || v > 1))) {
    throw new Error('skyColorAt: colors must be [r,g,b] in [0,1]');
  }
  if (!Number.isFinite(dirY) || dirY < -1 || dirY > 1) {
    throw new Error('skyColorAt: dirY must be in [-1,1]');
  }
  const t = Math.abs(dirY);
  const from = dirY >= 0 ? horizon : h;
  const to = dirY >= 0 ? zenith : h;
  return [0, 1, 2].map((i) => from[i] + (to[i] - from[i]) * t);
}

// Neutral preview palette (NOT original PE colors — deliberately neutral to
// avoid implying recovered art direction).
export const DEFAULT_ENV = Object.freeze({
  sky: Object.freeze({
    enabled: true,
    zenith: [0.35, 0.47, 0.66],
    horizon: [0.72, 0.75, 0.78],
    ground: [0.55, 0.55, 0.58],
  }),
  fog: Object.freeze({
    enabled: true,
    mode: 'ENGINEERING_PREVIEW_VALUES__SOURCE_BACKED_MODEL',
    gb12: Object.freeze({ depth: 0.01, fogFunction: 'FOG_Z_LINEAR' }),
    // ENGINEERING_PREVIEW values, coherent with the scene: patch spans ~192 m,
    // camera looks across ~200-600 m; fog far < sky dome radius so the sky
    // stays visible above the fogged horizon.
    fullOcclusionDistance: 900,
    color: [0.72, 0.75, 0.78], // matches sky horizon (blending with the light)
  }),
  light: Object.freeze({
    sunIntensity: 2.5,     // kept W03/W05 diagnostic value (explicit)
    ambientIntensity: 1.0, // kept W03/W05 diagnostic value (explicit)
    sunDir: [0.5, 1, 0.35],
  }),
});

// Structural invariant used by the node unit test AND the browser probe.
export function envConfigInvariant(env, cameraNear) {
  const errors = [];
  const e = env ?? DEFAULT_ENV;
  if (!e.sky || !Array.isArray(e.sky.zenith) || !Array.isArray(e.sky.horizon)) {
    errors.push('sky colors missing');
  }
  if (!e.fog || !Number.isFinite(e.fog.fullOcclusionDistance) ||
      e.fog.fullOcclusionDistance <= 0) {
    errors.push('fog fullOcclusionDistance must be > 0');
  }
  if (Array.isArray(e.fog?.color) && e.fog.color.some((v) => v < 0 || v > 1)) {
    errors.push('fog color out of [0,1]');
  }
  if (e.fog?.enabled) {
    const r = fogRangeFromGb12(e.fog.gb12?.depth ?? 0.01, cameraNear ?? 1,
      e.fog.fullOcclusionDistance);
    if (r.disabled) errors.push('fog enabled but gb12 depth <= 0 disables it');
    else if (!(r.far > r.near)) errors.push(`fog far (${r.far}) must exceed near (${r.near})`);
  }
  if (!e.light || !Number.isFinite(e.light.sunIntensity) || e.light.sunIntensity < 0 ||
      !Number.isFinite(e.light.ambientIntensity) || e.light.ambientIntensity < 0) {
    errors.push('light intensities must be finite >= 0');
  }
  return { ok: errors.length === 0, errors };
}

export function layerTable() {
  return ENV_LAYERS.map(({ layer, mode, source, consumer, toggle }) =>
    ({ layer, mode, source, consumer, toggle }));
}
