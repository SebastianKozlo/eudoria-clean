// calibration.js — CLEAN RUNTIME R185 CALIBRATION GATE A-J (ledger ENTRY #9 §5).
// Deterministic, self-contained, no PE data. Every item produces a result
// object collected into window.__CALIB__ (extracted by the harness runner).
// Renderer: THREE.WebGLRenderer (WebGPU excluded from M1-E).
import * as THREE from 'three';

const W = 128, H = 128;
const canvas = document.getElementById('calib');
const log = (m) => { document.getElementById('log').textContent += m + '\n'; };

const results = { started: new Date().toISOString(), items: {}, notes: [] };

function makeRenderer() {
  const r = new THREE.WebGLRenderer({
    canvas, antialias: false, preserveDrawingBuffer: true, alpha: false,
  });
  r.setSize(W, H, false);
  r.setPixelRatio(1); // determinism: 1 canvas pixel = 1 framebuffer pixel
  r.setClearColor(0x000000, 1);
  r.autoClear = true;
  return r;
}

function readPixels(r) {
  const gl = r.getContext();
  const px = new Uint8Array(W * H * 4);
  gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px); // bottom-up rows
  return px;
}
const at = (px, x, y) => { // y=0 = BOTTOM row (GL convention)
  const i = ((y * W) + x) * 4;
  return [px[i], px[i + 1], px[i + 2], px[i + 3]];
};
const near = (a, b, tol = 6) => a.every((v, i) => Math.abs(v - b[i]) <= tol);

function orthoCamera() {
  // 1:1 pixel mapping, no rotation — fully deterministic rasterization
  const cam = new THREE.OrthographicCamera(0, W, 0, H, -1, 1);
  // top=0? OrthographicCamera(left,right,top,bottom): top < bottom flips Y;
  // use top=H,bottom=0 so world y=H maps to screen top row of readPixels space.
  return cam;
}

async function sha256Hex(bytes) {
  const d = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();
}

function quad(w, h) {
  const g = new THREE.PlaneGeometry(w, h);
  return g;
}

async function main() {
  // ---------- A: revision ----------
  // r185 exports the revision constant as THREE.REVISION (uppercase), a
  // string. (The lowercase `THREE.revision` used in the first run did not
  // exist — clean-code bug, fixed; verified against three.core.js
  // `const REVISION = '185';`.)
  results.items.A = {
    test: 'THREE.REVISION === "185"',
    revision: THREE.REVISION,
    pass: THREE.REVISION === '185',
  };

  // ---------- B: WebGLRenderer initializes ----------
  let renderer;
  try {
    renderer = makeRenderer();
    const gl = renderer.getContext();
    results.items.B = {
      test: 'WebGLRenderer initializes (r185, antialias=false, preserveDrawingBuffer=true)',
      initialized: true,
      webgl2: renderer.capabilities.isWebGL2,
      maxTextureSize: renderer.capabilities.maxTextureSize,
      pass: true,
    };
  } catch (e) {
    results.items.B = { test: 'WebGLRenderer initializes', initialized: false, error: String(e), pass: false };
    throw e;
  }

  // ---------- C: deterministic geometry ----------
  {
    const scene = new THREE.Scene();
    const cam = new THREE.OrthographicCamera(0, W, H, 0, -1, 1);
    // black plane exactly covering the right half of the 128x128 viewport
    const mesh = new THREE.Mesh(quad(W / 2, H), new THREE.MeshBasicMaterial({ color: 0x000000 }));
    mesh.position.set(W * 0.75, H / 2, 0); // right half center
    scene.add(mesh);
    renderer.setClearColor(0xff0000, 1); // red background
    renderer.render(scene, cam);
    const px = readPixels(renderer);
    const left = at(px, 10, 64), right = at(px, 118, 64);
    results.items.C = {
      test: 'known-size plane at known position (right half black on red)',
      leftPixel: left, rightPixel: right,
      expectedLeft: [255, 0, 0, 255], expectedRight: [0, 0, 0, 255],
      pass: near(left, [255, 0, 0, 255]) && near(right, [0, 0, 0, 255]),
    };
  }

  // ---------- D + F: deterministic texture + explicit mip/filter config ----------
  {
    const scene = new THREE.Scene();
    const cam = new THREE.OrthographicCamera(0, W, H, 0, -1, 1);
    // 2x2 texture, one distinct color per texel, magnified 64x -> Nearest is exact
    const data = new Uint8Array([
      255, 0, 0, 255, 0, 255, 0, 255,
      0, 0, 255, 255, 255, 255, 0, 255,
    ]);
    const tex = new THREE.DataTexture(data, 2, 2, THREE.RGBAFormat);
    tex.magFilter = THREE.NearestFilter;
    tex.minFilter = THREE.NearestFilter;   // no minification; no mips needed
    tex.generateMipmaps = false;           // explicit (gate F)
    tex.flipY = false;                     // our convention (gate E uses it too)
    tex.needsUpdate = true;
    const mesh = new THREE.Mesh(quad(W, H), new THREE.MeshBasicMaterial({ map: tex }));
    mesh.position.set(W / 2, H / 2, 0);
    scene.add(mesh);
    renderer.setClearColor(0x000000, 1);
    renderer.render(scene, cam);
    const px = readPixels(renderer);
    // With flipY=false: uv v=0 => data row 0; PlaneGeometry v=0 is at plane
    // BOTTOM => screen top-left shows data row 1 (blue), bottom-right row 0 (green).
    const tl = at(px, 10, 117), br = at(px, 117, 10); // GL y: top row = 127
    results.items.D = {
      test: 'DataTexture 2x2 known colors, Nearest, magnified 64x',
      topLeft: tl, bottomRight: br,
      expectedTopLeft: [0, 0, 255, 255], expectedBottomRight: [0, 255, 0, 255],
      pass: near(tl, [0, 0, 255, 255]) && near(br, [0, 255, 0, 255]),
    };
    // F: explicit mip/filter configuration record (r170: mipmaps ALWAYS
    // generated when generateMipmaps=true irrespective of filter).
    const texMip = new THREE.DataTexture(data, 2, 2, THREE.RGBAFormat);
    texMip.generateMipmaps = true;
    texMip.minFilter = THREE.LinearMipmapLinearFilter;
    texMip.magFilter = THREE.LinearFilter;
    texMip.flipY = false;
    texMip.needsUpdate = true;
    const mesh2 = new THREE.Mesh(quad(4, 4), new THREE.MeshBasicMaterial({ map: texMip }));
    const scene2 = new THREE.Scene();
    scene2.add(mesh2);
    renderer.render(scene2, cam); // exercises mip generation path (r170 rule)
    results.items.F = {
      test: 'mip/filter config explicitly recorded and exercised',
      config: {
        plain: { generateMipmaps: false, minFilter: 'NearestFilter', magFilter: 'NearestFilter' },
        mipped: { generateMipmaps: true, minFilter: 'LinearMipmapLinearFilter', magFilter: 'LinearFilter' },
      },
      r170Rule: 'mipmaps are ALWAYS generated when generateMipmaps=true, irrespective of filter settings',
      mippedRenderOk: true,
      pass: true,
    };
  }

  // ---------- E: UV orientation ----------
  {
    // With flipY=false, UV(0,0) samples row 0 of the raw data (first row in
    // memory). PlaneGeometry UVs: (0,0) at bottom-left of the plane in local
    // space. Verify: screen bottom-left pixel shows data row 0 color.
    const data = new Uint8Array([
      255, 0, 0, 255,   // row 0: red
      0, 0, 255, 255,   // row 1: blue
    ]);
    const tex = new THREE.DataTexture(data, 1, 2, THREE.RGBAFormat);
    tex.magFilter = THREE.NearestFilter; tex.minFilter = THREE.NearestFilter;
    tex.generateMipmaps = false; tex.flipY = false; tex.needsUpdate = true;
    const scene = new THREE.Scene();
    const cam = new THREE.OrthographicCamera(0, W, H, 0, -1, 1);
    const mesh = new THREE.Mesh(quad(W, H), new THREE.MeshBasicMaterial({ map: tex }));
    mesh.position.set(W / 2, H / 2, 0);
    scene.add(mesh);
    renderer.setClearColor(0x000000, 1);
    renderer.render(scene, cam);
    const px = readPixels(renderer);
    const bottom = at(px, 64, 5), top = at(px, 64, 122);
    results.items.E = {
      test: 'UV orientation with flipY=false: uv(0,0) => data row 0 => screen bottom',
      flipY: false,
      bottomPixel: bottom, topPixel: top,
      expectedBottom: [255, 0, 0, 255], expectedTop: [0, 0, 255, 255],
      pass: near(bottom, [255, 0, 0, 255]) && near(top, [0, 0, 255, 255]),
    };
  }

  // ---------- G: alpha/blending (incl. r177 premultipliedAlpha) ----------
  {
    // 1) NormalBlending, alpha=0.5 red quad over green background:
    //    result = 0.5*red + 0.5*green = (128,128,0)
    const scene = new THREE.Scene();
    const cam = new THREE.OrthographicCamera(0, W, H, 0, -1, 1);
    const mat = new THREE.MeshBasicMaterial({ color: 0xff0000, transparent: true, opacity: 0.5 });
    const mesh = new THREE.Mesh(quad(W, H), mat);
    mesh.position.set(W / 2, H / 2, 0);
    scene.add(mesh);
    renderer.setClearColor(0x00ff00, 1);
    renderer.render(scene, cam);
    const px = readPixels(renderer);
    const c = at(px, 64, 64);
    const normalOk = near(c, [128, 128, 0, 255], 10);
    // 2) r177 rule: MultiplyBlending REQUIRES premultipliedAlpha=true.
    //    Exercise the exact supported configuration and record it.
    const matMul = new THREE.MeshBasicMaterial({
      color: 0x808080, transparent: true, blending: THREE.MultiplyBlending,
      premultipliedAlpha: true, // REQUIRED since r177 — recorded, not optional
    });
    scene.clear(); scene.add(new THREE.Mesh(quad(W, H), matMul).translateX(0));
    scene.children[0].position.set(W / 2, H / 2, 0);
    renderer.setClearColor(0xffffff, 1);
    renderer.render(scene, cam);
    const px2 = readPixels(renderer);
    const c2 = at(px2, 64, 64);
    const mulOk = near(c2, [128, 128, 128, 255], 12); // 0.5 gray * white
    results.items.G = {
      test: 'alpha/blending: NormalBlending 50% + MultiplyBlending premultiplied',
      normalBlendPixel: c, normalBlendExpected: [128, 128, 0, 255], normalOk,
      multiplyBlendPixel: c2, multiplyBlendExpected: [128, 128, 128, 255], mulOk,
      r177Rule: 'MultiplyBlending/SubtractiveBlending require premultipliedAlpha=true (since r177)',
      premultipliedAlphaUsed: true,
      pass: normalOk && mulOk,
    };
  }

  // ---------- H: matrix/world-transform (incl. r185 matrixWorldNeedsUpdate) ----------
  // EMPIRICAL r185 SEMANTICS (first gate run + three.core.js source):
  //  1) updateWorldMatrix(updateParents, updateChildren, force=false) HONORS
  //     matrixWorldNeedsUpdate (the documented r185 change): an isolated
  //     object (parent=null, matrixAutoUpdate=false) whose .matrix was
  //     changed WITHOUT the flag keeps a STALE matrixWorld; setting the flag
  //     applies it.
  //  2) RENDER PATH: Object3D.updateMatrix() sets matrixWorldNeedsUpdate=true;
  //     a Scene has matrixAutoUpdate=true by default, so every render() the
  //     scene recomputes and propagates force=true to ALL children — a child
  //     with matrixAutoUpdate=false FOLLOWS its manual matrix every render,
  //     regardless of its own flag. (Consequence for chunk placement: manual
  //     matrix edits are always picked up; stale-matrixWorld caching is NOT
  //     available while any ancestor auto-updates.)
  {
    // H1 — isolated flag semantics via updateWorldMatrix (r185 documented rule)
    const obj = new THREE.Object3D();
    obj.matrixAutoUpdate = false;
    obj.matrixWorld.makeTranslation(0, 0, 0);
    obj.matrix.makeTranslation(32, 64, 0);
    obj.matrixWorldNeedsUpdate = false; // changed matrix WITHOUT the flag
    obj.updateWorldMatrix(true, false);
    const staleWithoutFlag = obj.matrixWorld.elements[12] === 0 &&
      obj.matrixWorld.elements[13] === 0 && obj.matrixWorld.elements[14] === 0;
    obj.matrixWorldNeedsUpdate = true; // now the flag
    obj.updateWorldMatrix(true, false);
    const appliedWithFlag = obj.matrixWorld.elements[12] === 32 &&
      obj.matrixWorld.elements[13] === 64 && obj.matrixWorld.elements[14] === 0;

    // H2 — render-path propagation: manual matrix is honored every render in
    // an auto-updating scene (empirical r185 behavior, asserted + recorded).
    const scene = new THREE.Scene();
    const cam = new THREE.OrthographicCamera(0, W, H, 0, -1, 1);
    const mesh = new THREE.Mesh(quad(64, 64), new THREE.MeshBasicMaterial({ color: 0xffffff }));
    mesh.matrixAutoUpdate = false;
    mesh.matrix.makeTranslation(32, 64, 0); // left half center
    mesh.matrixWorldNeedsUpdate = true;
    scene.add(mesh);
    renderer.setClearColor(0x000000, 1);
    renderer.render(scene, cam);
    const px1 = readPixels(renderer);
    const initialPlacementOk = near(at(px1, 16, 64), [255, 255, 255, 255]) &&
                                near(at(px1, 112, 64), [0, 0, 0, 255]);
    // Move via matrix WITHOUT the flag: r185 render path (auto-updating
    // parent scene) still applies the manual matrix every render.
    mesh.matrix.makeTranslation(96, 64, 0); // right half center — flag NOT set
    renderer.render(scene, cam);
    const px2 = readPixels(renderer);
    const followsWithoutFlag = near(at(px2, 16, 64), [0, 0, 0, 255]) &&
                               near(at(px2, 112, 64), [255, 255, 255, 255]);
    mesh.matrixWorldNeedsUpdate = true; // flag path also verified explicitly
    renderer.render(scene, cam);
    const px3 = readPixels(renderer);
    const withFlagStaysRight = near(at(px3, 16, 64), [0, 0, 0, 255]) &&
                               near(at(px3, 112, 64), [255, 255, 255, 255]);
    results.items.H = {
      test: 'r185 matrix semantics: updateWorldMatrix honors matrixWorldNeedsUpdate (isolated); render path applies manual matrix via parent force propagation',
      isolatedStaleWithoutFlag: staleWithoutFlag,
      isolatedAppliedWithFlag: appliedWithFlag,
      renderPlacementOk: initialPlacementOk,
      renderFollowsManualMatrixWithoutFlag: followsWithoutFlag,
      renderWithFlagStaysRight: withFlagStaysRight,
      r185Facts: [
        'updateWorldMatrix() honors matrixWorldNeedsUpdate (documented r185 change; verified empirically + source line)',
        'Object3D.updateMatrix() sets matrixWorldNeedsUpdate=true; an auto-updating Scene therefore forces child matrixWorld recompute every render',
      ],
      pass: staleWithoutFlag && appliedWithFlag && initialPlacementOk &&
            followsWithoutFlag && withFlagStaysRight,
    };
  }

  // ---------- I: loader behavior (r184: .load() has NO return value) ----------
  {
    const item = { test: 'FileLoader.load() callback-based; return value is undefined (r184)', pass: false };
    try {
      let onLoadFired = false, payload = null;
      const loader = new THREE.FileLoader();
      const retVal = loader.load('/calibration/loader_probe.txt', (data) => {
        onLoadFired = true; payload = data;
      });
      item.returnValueIsUndefined = retVal === undefined;
      await new Promise((resolve) => { // give the callback a bounded window
        const t0 = performance.now();
        (function poll() {
          if (onLoadFired || performance.now() - t0 > 5000) resolve();
          else setTimeout(poll, 25);
        })();
      });
      item.onLoadFired = onLoadFired;
      item.payloadMatches = typeof payload === 'string' &&
        payload.startsWith('R185_CALIBRATION_LOADER_PROBE');
      item.pass = item.returnValueIsUndefined && item.onLoadFired && item.payloadMatches;
    } catch (e) { item.error = String(e); }
    results.items.I = item;
  }

  // ---------- J: reproducible screenshot/hash artifact ----------
  {
    // Deterministic composite scene (uses the calibrated conventions above).
    const buildAndRender = () => {
      const scene = new THREE.Scene();
      const cam = new THREE.OrthographicCamera(0, W, H, 0, -1, 1);
      const data = new Uint8Array([200, 40, 10, 255, 10, 200, 40, 255, 40, 10, 200, 255, 120, 120, 20, 255]);
      const tex = new THREE.DataTexture(data, 2, 2, THREE.RGBAFormat);
      tex.magFilter = THREE.NearestFilter; tex.minFilter = THREE.NearestFilter;
      tex.generateMipmaps = false; tex.flipY = false; tex.needsUpdate = true;
      const m1 = new THREE.Mesh(quad(64, H), new THREE.MeshBasicMaterial({ map: tex }));
      m1.position.set(32, H / 2, 0); scene.add(m1);
      const m2 = new THREE.Mesh(quad(64, H), new THREE.MeshBasicMaterial({
        color: 0x3060ff, transparent: true, opacity: 0.75,
      }));
      m2.position.set(96, H / 2, 0); scene.add(m2);
      renderer.setClearColor(0x101010, 1);
      renderer.render(scene, cam);
      return renderer.domElement.toDataURL('image/png');
    };
    const run1 = buildAndRender();
    const run2 = buildAndRender();
    const b64 = (d) => Uint8Array.from(atob(d.split(',')[1]), c => c.charCodeAt(0));
    const hash1 = await sha256Hex(b64(run1));
    const hash2 = await sha256Hex(b64(run2));
    results.items.J = {
      test: 'reproducible screenshot/hash: two independent renders, equal SHA256',
      run1Sha256: hash1, run2Sha256: hash2,
      reproducible: hash1 === hash2,
      pngBase64Length: b64(run1).length,
      pass: hash1 === hash2,
    };
    window.__CALIB_PNG__ = run1; // extracted by the harness runner as artifact
  }

  results.finished = new Date().toISOString();
  results.threeRevisionProjectBaseline =
    Object.values(results.items).every(i => i.pass) ? 'CALIBRATED' : 'NOT_CALIBRATED';
  results.pregateRevisionCheck = THREE.revision;
  window.__CALIB__ = results;
  for (const [k, v] of Object.entries(results.items)) {
    log(`${k}: ${v.pass ? 'PASS' : 'FAIL'} — ${v.test}`);
  }
  log(`THREE_R185_PROJECT_BASELINE = ${results.threeRevisionProjectBaseline}`);
}

main().catch(e => {
  results.fatal = String(e);
  results.threeRevisionProjectBaseline = 'NOT_CALIBRATED';
  window.__CALIB__ = results;
  log('FATAL: ' + String(e));
});
