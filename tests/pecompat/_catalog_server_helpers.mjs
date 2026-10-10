// _catalog_server_helpers.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 4 (W6)
// Shared bounded lifecycle helpers for the CATALOG server tests
// (catalog_api_denial.test.mjs, catalog_headless_load.test.mjs and the
// pixel/interactive runs). REUSE LABEL: checkPortFree/findFreePort/rawRequest/
// parseJsonOrNone are imported UNCHANGED from tests/pecompat/
// _app_server_helpers.mjs (the sceneir T7/T9 helpers); the start/stop
// lifecycle below follows the SAME bounded pattern (PID, startup line,
// bounded timeout, port-freed proof) adapted to compat/server-catalog.mjs.
// NEVER touches any other process or port (8140 is never used).
import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  checkPortFree, findFreePort, rawRequest, parseJsonOrNone,
} from './_app_server_helpers.mjs';

export { checkPortFree, findFreePort, rawRequest, parseJsonOrNone };

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const REPO_ROOT = path.resolve(HERE, '..', '..');
export const CATALOG_SERVER_SCRIPT = path.join(REPO_ROOT, 'compat', 'server-catalog.mjs');

/** Start compat/server-catalog.mjs as a bounded child process. Waits for the
 *  documented startup line (catalog server http://127.0.0.1:PORT/ pid=<PID>)
 *  + /api/catalog/status readiness. Uses PECATALOG_PORT (never PORT, never
 *  8140). @returns {{ child, port, pid, stdout, stderr, startupLine, startedAtMs }} */
export async function startCatalogServer({ port, timeoutMs = 180000, env = {} } = {}) {
  if (port === 8140) throw new Error('[_catalog_server_helpers] port 8140 is the foreign reference server — REFUSED');
  const child = spawn(process.execPath, [CATALOG_SERVER_SCRIPT], {
    env: { ...process.env, ...env, PECATALOG_PORT: String(port) },
    cwd: REPO_ROOT,
    stdio: ['ignore', 'pipe', 'pipe'],
    windowsHide: true,
  });
  const rec = { child, port, pid: child.pid, stdout: '', stderr: '', startupLine: null, startedAtMs: Date.now() };
  const t0 = Date.now();
  child.stdout.setEncoding('utf8');
  child.stderr.setEncoding('utf8');
  child.stdout.on('data', (d) => { rec.stdout += d; });
  child.stderr.on('data', (d) => { rec.stderr += d; });
  const exited = new Promise((resolve) => child.once('exit', (code, signal) => resolve({ code, signal })));

  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const m = /catalog server http:\/\/127\.0\.0\.1:(\d+)\/ pid=(\d+)/.exec(rec.stdout);
    if (m && Number(m[1]) === port) {
      rec.startupLine = m[0];
      rec.startupElapsedMs = Date.now() - t0;
      const ok = await waitForCatalogStatus(port, 15000);
      if (!ok) {
        await stopCatalogServer(rec);
        throw new Error(`[_catalog_server_helpers] server printed the startup line but /api/catalog/status never answered — stdout:\n${rec.stdout.slice(0, 4000)}\nstderr:\n${rec.stderr.slice(0, 2000)}`);
      }
      rec.exited = exited;
      return rec;
    }
    const { code } = await Promise.race([exited, new Promise((r) => setTimeout(() => r({}), 150))]);
    if (code !== undefined) {
      throw new Error(`[_catalog_server_helpers] server exited early (code ${code}) — stdout:\n${rec.stdout.slice(0, 4000)}\nstderr:\n${rec.stderr.slice(0, 2000)}`);
    }
  }
  child.kill();
  throw new Error(`[_catalog_server_helpers] server startup TIMEOUT (${timeoutMs} ms) — stdout:\n${rec.stdout.slice(0, 4000)}\nstderr:\n${rec.stderr.slice(0, 2000)}`);
}

async function waitForCatalogStatus(port, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      const r = await fetch(`http://127.0.0.1:${port}/api/catalog/status`);
      if (r.ok) return true;
    } catch { /* not up yet */ }
    await new Promise((r) => setTimeout(r, 150));
  }
  return false;
}

/** Stop a server started by startCatalogServer: kill, await exit (bounded),
 *  verify the port is FREED (rebind probe with bounded retries). */
export async function stopCatalogServer(rec) {
  const t0 = Date.now();
  let killed = false;
  if (rec.child.exitCode === null && rec.child.signalCode === null && !rec.child.killed) {
    rec.child.kill();
    killed = true;
  }
  let exitInfo = { code: rec.child.exitCode, signal: rec.child.signalCode };
  if (rec.child.exitCode === null && rec.child.signalCode === null) {
    exitInfo = await Promise.race([
      new Promise((resolve) => rec.child.once('exit', (code, signal) => resolve({ code, signal }))),
      new Promise((resolve) => setTimeout(() => resolve({ code: null, signal: 'TIMEOUT' }), 10000)),
    ]);
  }
  let portFreed = false;
  let freedAfterMs = null;
  const freeDeadline = Date.now() + 15000;
  while (Date.now() < freeDeadline) {
    if (await checkPortFree(rec.port)) { portFreed = true; freedAfterMs = Date.now() - t0; break; }
    await new Promise((r) => setTimeout(r, 250));
  }
  return {
    killed, exitCode: exitInfo.code, signal: exitInfo.signal,
    lifetimeMs: Date.now() - rec.startedAtMs, portFreed, freedAfterMs,
  };
}
