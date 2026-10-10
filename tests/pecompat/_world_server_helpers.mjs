// _world_server_helpers.mjs — PE_WORLD_LAUNCHER_R1_20261010, ETAP C
// Shared bounded lifecycle helpers for the WORLD server tests
// (world_server.test.mjs, world_headless_load.test.mjs, world_pixel_render).
// REUSE LABEL: follows tests/pecompat/_catalog_server_helpers.mjs (same
// bounded pattern: PID, startup line, bounded timeout, port-freed proof);
// checkPortFree/findFreePort/rawRequest/parseJsonOrNone imported UNCHANGED
// from tests/pecompat/_app_server_helpers.mjs. NEVER touches any other
// process or port (8140/8161 are refused, never bound over).
import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import http from 'node:http';
import {
  checkPortFree, findFreePort, rawRequest, parseJsonOrNone,
} from './_app_server_helpers.mjs';

export { checkPortFree, findFreePort, rawRequest, parseJsonOrNone };

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const REPO_ROOT = path.resolve(HERE, '..', '..');
export const WORLD_SERVER_SCRIPT = path.join(REPO_ROOT, 'compat', 'server-world.mjs');

/** Raw HTTP request that keeps the FULL body (rawRequest in
 * _app_server_helpers truncates to a 512-byte excerpt; binary endpoints need
 * the whole body). Same bounded-timeout pattern. */
export function rawRequestFull(port, rawPath, { timeoutMs = 20000, method = 'GET' } = {}) {
  return new Promise((resolve, reject) => {
    const req = http.request(
      { host: '127.0.0.1', port, method, path: rawPath, headers: { Host: `127.0.0.1:${port}` } },
      (res) => {
        const chunks = [];
        res.on('data', (c) => chunks.push(c));
        res.on('end', () => {
          const buf = Buffer.concat(chunks);
          resolve({ status: res.statusCode, headers: res.headers, body: buf });
        });
      },
    );
    req.setTimeout(timeoutMs, () => { req.destroy(new Error('client timeout')); });
    req.on('error', reject);
    req.end();
  });
}

/** Wait until the world server reports the census READY + both background
 * container verifications done (models/textures stream-hash ~seconds) + the
 * ETAP D lazy Textures.bnt index READY + the ETAP E lazy Models.bnt index
 * READY + the measured vegetation support census READY (it runs once BOTH
 * lazy indexes are READY — the bounded default-profile measurement). */
export async function waitForWorldReady(port, timeoutMs = 90000) {
  const deadline = Date.now() + timeoutMs;
  let last = null;
  while (Date.now() < deadline) {
    try {
      const r = await rawRequestFull(port, '/api/world/status');
      const j = parseJsonOrNone(r.body.toString('utf8'));
      last = j;
      if (j && j.census?.ready === true
        && String(j.containers?.models?.state ?? '').startsWith('VERIFIED')
        && String(j.containers?.textures?.state ?? '').startsWith('VERIFIED')
        && j.containers?.textures?.indexState === 'READY'
        && j.containers?.models?.indexState === 'READY'
        && j.vegetation?.supportCensusState === 'READY') {
        return j;
      }
    } catch { /* not up yet */ }
    await new Promise((r) => setTimeout(r, 400));
  }
  return null;
}

/** Start compat/server-world.mjs as a bounded child process. Waits for the
 *  documented startup line (world server http://127.0.0.1:PORT/ pid=<PID>
 *  READY) + status readiness. Uses PEWORLD_PORT (never 8140/8161).
 *  @returns {{ child, port, pid, stdout, stderr, startupLine, startedAtMs }} */
export async function startWorldServer({ port, timeoutMs = 120000, env = {} } = {}) {
  if (port === 8140 || port === 8161) {
    throw new Error('[_world_server_helpers] ports 8140/8161 belong to the foreign standing servers — REFUSED');
  }
  const child = spawn(process.execPath, [WORLD_SERVER_SCRIPT], {
    env: { ...process.env, ...env, PEWORLD_PORT: String(port) },
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
    const m = /world server http:\/\/127\.0\.0\.1:(\d+)\/ pid=(\d+) READY/.exec(rec.stdout);
    if (m && Number(m[1]) === port) {
      rec.startupLine = m[0];
      rec.startupElapsedMs = Date.now() - t0;
      const ok = await waitForWorldReady(port, 90000);
      if (!ok) {
        await stopWorldServer(rec);
        throw new Error(`[_world_server_helpers] server printed the startup line but readiness (census + container verification) never completed — stdout:\n${rec.stdout.slice(0, 4000)}\nstderr:\n${rec.stderr.slice(0, 2000)}`);
      }
      rec.readyStatus = ok;
      rec.exited = exited;
      return rec;
    }
    const { code } = await Promise.race([exited, new Promise((r) => setTimeout(() => r({}), 150))]);
    if (code !== undefined) {
      throw new Error(`[_world_server_helpers] server exited early (code ${code}) — stdout:\n${rec.stdout.slice(0, 4000)}\nstderr:\n${rec.stderr.slice(0, 2000)}`);
    }
  }
  child.kill();
  throw new Error(`[_world_server_helpers] server startup TIMEOUT (${timeoutMs} ms) — stdout:\n${rec.stdout.slice(0, 4000)}\nstderr:\n${rec.stderr.slice(0, 2000)}`);
}

/** Stop a server started by startWorldServer: kill, await exit (bounded),
 *  verify the port is FREED (rebind probe with bounded retries). */
export async function stopWorldServer(rec) {
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
