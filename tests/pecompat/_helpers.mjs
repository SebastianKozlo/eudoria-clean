// _helpers.mjs — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// Shared helpers for tests/pecompat (an implementation-detail module under the
// allowed tests/pecompat/ area — noted in IMPLEMENTATION_NOTES.md; the planned
// test file names from PLAN_AND_PATH_ALLOWLIST.md are all present unchanged).
//
// ZERO new dependencies: node builtins only; THREE is resolved from the
// EXISTING canonical checkout node_modules (three 0.185.0 — the pinned
// package version; the worktree itself carries no node_modules).
import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { existsSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

export const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');

export async function readFileBytes(p) {
  return new Uint8Array(await readFile(p));
}

// ---- Control B fixture inputs (phase-1 byte-identical local copies) ----
export const CONTROL_B_FIXTURES = {
  ROTATED_SCALED_PARENT: {
    path: 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\controlB_work\\ROTATED_SCALED_PARENT.nif',
    sizeBytes: 327,
    sha256: '56fe7fec78c229acc9919735078b4f48b1c44b74bce01bca7814db023f4d5a19',
    expectedWorldTranslate: [96, 202, 306],
  },
  THREE_LEVEL_SOCKET: {
    path: 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\\controlB_work\\THREE_LEVEL_SOCKET.nif',
    sizeBytes: 430,
    sha256: '0c71d5fdd4a70dd17b38ee49c3279747c772a0f96fe02a02c90aac716b441873',
    expectedWorldTranslate: [58, 221, 363],
  },
};

// ---- THREE resolution (the pinned 0.185.0 from the canonical checkout) ----
export const DEFAULT_THREE_MODULE =
  'D:\\Eudoria_Reconstruction\\12_WebGame\\eudoria-clean\\node_modules\\three\\build\\three.module.js';
export const DEFAULT_THREE_PACKAGE_JSON =
  'D:\\Eudoria_Reconstruction\\12_WebGame\\eudoria-clean\\node_modules\\three\\package.json';
export const PINNED_THREE_VERSION = '0.185.0';

/** Resolve the three module for tests: env PECOMPAT_THREE_MODULE, else the
 * canonical checkout default. Returns { THREE, modulePath, packageVersion }. */
export async function loadThree() {
  const modulePath = process.env.PECOMPAT_THREE_MODULE || DEFAULT_THREE_MODULE;
  if (!existsSync(modulePath)) {
    throw new Error(`[tests/pecompat/_helpers] three module not found at ${modulePath} (set PECOMPAT_THREE_MODULE)`);
  }
  const pkgPath = path.join(path.dirname(path.dirname(modulePath)), 'package.json');
  let packageVersion = null;
  if (existsSync(pkgPath)) {
    const pkg = JSON.parse(await readFile(pkgPath, 'utf8'));
    packageVersion = pkg.version;
  }
  if (packageVersion && packageVersion !== PINNED_THREE_VERSION) {
    throw new Error(`[tests/pecompat/_helpers] three version ${packageVersion} != pinned ${PINNED_THREE_VERSION} — refusing (retention pin)`);
  }
  const THREE = await import(pathToFileURL(modulePath).href);
  return { THREE, modulePath, packageVersion };
}

// ---- synthetic IR conveniences (AUTHORED synthetic data; NOT PCG assets) ----
export const RZ90 = [[0, -1, 0], [1, 0, 0], [0, 0, 1]];
export const IDENT3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
export const trs = (t, r = IDENT3, s = 1) => ({ translate: [...t], rotate: r.map((x) => [...x]), scale: s });

export function record(id, name, status, extra = {}) {
  return {
    id,
    name,
    status, // PASS | FAIL | NOT_PERFORMED
    ...extra,
  };
}
