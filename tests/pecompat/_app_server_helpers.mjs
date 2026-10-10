// _app_server_helpers.mjs — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// Shared app-server lifecycle helpers for tests/pecompat T7/T9 (addition per
// the phase-3 dispatch; the phase-2 unit files are untouched). BOUNDED
// lifecycle: every server process started here is stopped here, with PID,
// port, lifetime and port-freed verification recorded. NEVER touches any
// other process or port.
import { spawn } from 'node:child_process';
import net from 'node:net';
import path from 'node:path';
import http from 'node:http';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const REPO_ROOT = path.resolve(HERE, '..', '..');
export const SERVER_SCRIPT = path.join(REPO_ROOT, 'compat', 'server-sceneir.mjs');

/** Bind+close probe: resolves true if the port is FREE on 127.0.0.1. */
export function checkPortFree(port, host = '127.0.0.1') {
  return new Promise((resolve) => {
    const probe = net.createServer();
    probe.once('error', () => resolve(false));
    probe.listen(port, host, () => probe.close(() => resolve(true)));
  });
}

/** Find a free loopback port (bind/close probe; caller binds the real server). */
export async function findFreePort(preferred) {
  if (preferred && (await checkPortFree(preferred))) return preferred;
  for (let i = 0; i < 40; i++) {
    const p = 8200 + Math.floor(Math.random() * 700);
    if (await checkPortFree(p)) return p;
  }
  throw new Error('[_app_server_helpers] no free port found in 8200..8899');
}

/** Start compat/server-sceneir.mjs as a bounded child process. Waits for the
 *  documented startup line (sceneir server http://127.0.0.1:PORT/ pid=<PID>).
 *  @returns {{ child, port, pid, stdout, stderr, startupLine, startedAtMs }} */
export async function startServer({ port, modelsBntPath, threeRoot, timeoutMs = 120000 }) {
  const env = {
    ...process.env,
    PORT: String(port),
  };
  if (modelsBntPath) env.PECOMPAT_MODELS_BNT = modelsBntPath;
  if (threeRoot) env.PECOMPAT_THREE_ROOT = threeRoot;
  const child = spawn(process.execPath, [SERVER_SCRIPT], {
    env, cwd: REPO_ROOT, stdio: ['ignore', 'pipe', 'pipe'], windowsHide: true,
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
    const m = /sceneir server http:\/\/127\.0\.0\.1:(\d+)\/ pid=(\d+)/.exec(rec.stdout);
    if (m && Number(m[1]) === port) {
      rec.startupLine = m[0];
      rec.startupElapsedMs = Date.now() - t0;
      // the startup line precedes in-memory readiness by microseconds; poll
      // /api/status until it answers (bounded).
      const ok = await waitForStatus(port, 15000);
      if (!ok) {
        await stopServer(rec);
        throw new Error(`[_app_server_helpers] server printed the startup line but /api/status never answered — stdout:\n${rec.stdout.slice(0, 4000)}\nstderr:\n${rec.stderr.slice(0, 2000)}`);
      }
      rec.exited = exited;
      return rec;
    }
    const { code } = await Promise.race([exited, new Promise((r) => setTimeout(() => r({}), 150))]);
    if (code !== undefined) {
      throw new Error(`[_app_server_helpers] server exited early (code ${code}) — stdout:\n${rec.stdout.slice(0, 4000)}\nstderr:\n${rec.stderr.slice(0, 2000)}`);
    }
  }
  child.kill();
  throw new Error(`[_app_server_helpers] server startup TIMEOUT (${timeoutMs} ms) — stdout:\n${rec.stdout.slice(0, 4000)}\nstderr:\n${rec.stderr.slice(0, 2000)}`);
}

async function waitForStatus(port, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      const r = await fetch(`http://127.0.0.1:${port}/api/status`);
      if (r.ok) return true;
    } catch { /* not up yet */ }
    await new Promise((r) => setTimeout(r, 120));
  }
  return false;
}

/** Stop a server started by startServer: kill, await exit (bounded), verify
 *  the port is FREED (rebind probe with bounded retries for OS release lag).
 *  @returns {{ killed, exitCode, signal, lifetimeMs, portFreed, freedAfterMs }} */
export async function stopServer(rec) {
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
    killed,
    exitCode: exitInfo.code,
    signal: exitInfo.signal,
    lifetimeMs: Date.now() - rec.startedAtMs,
    portFreed,
    freedAfterMs,
  };
}

/** RAW HTTP request (no client-side URL normalization — the path goes on the
 *  wire verbatim; this is how traversal/encoded paths are honestly tested).
 *  @returns {{ status, headers, bodyText, bytes }} */
export function rawRequest(port, method, rawPath, { timeoutMs = 15000 } = {}) {
  return new Promise((resolve, reject) => {
    const req = http.request(
      { host: '127.0.0.1', port, method, path: rawPath, headers: { Host: `127.0.0.1:${port}` } },
      (res) => {
        const chunks = [];
        res.on('data', (c) => chunks.push(c));
        res.on('end', () => {
          const buf = Buffer.concat(chunks);
          resolve({
            status: res.statusCode,
            headers: res.headers,
            bodyText: buf.subarray(0, 512).toString('utf8'), // bounded excerpt
            bytes: buf.length,
          });
        });
      },
    );
    req.setTimeout(timeoutMs, () => { req.destroy(new Error('client timeout')); });
    req.on('error', reject);
    req.end();
  });
}

export function parseJsonOrNone(text) {
  try { return JSON.parse(text); } catch { return null; }
}
