// api_path_denial.test.mjs — T7 (APP_SERVER_TESTS phase) — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// REAL local HTTP requests against the RUNNING compat/server-sceneir.mjs
// (dispatch T7): app loads; the SceneIR endpoint serves the bounded
// regenerated data; SYNTHETIC malicious paths (../, absolute, encoded
// traversal, unconfigured root, unknown route, non-GET methods) are DENIED
// with explicit status/errors — every request+response recorded to
// raw/HTTP_TRANSCRIPTS.json. The suite owns the server lifecycle (start/stop,
// PID/port/lifetime/port-freed proof).
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import {
  startServer, stopServer, findFreePort, rawRequest, parseJsonOrNone,
} from './_app_server_helpers.mjs';

const PIN = {
  payloadSha256: '3e8a22c2213202207e374b55cd65b2c3be039ccdd1e8d01a07fcaf44de12cf36',
  containerSha256: 'c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0',
};

function rec(id, name, status, extra = {}) {
  return { id, name, status, ...extra };
}

export async function run(ctx) {
  const rawDir = ctx.rawDir;
  await mkdir(rawDir, { recursive: true });
  const transcript = [];
  const lifecycle = {};
  const records = [];

  const T = (entry) => { transcript.push(entry); return entry; };
  const ok = (b) => (b ? 'PASS' : 'FAIL');

  const port = await findFreePort(8140);
  let server;
  try {
    server = await startServer({
      port,
      modelsBntPath: ctx.modelsPath,
      threeRoot: ctx.threeRoot,
      timeoutMs: 180000, // includes the 395 MB container SHA verification
    });
  } catch (e) {
    return [rec('T7_SERVER_START', 'server starts (verified-free port, loopback bind, fail-closed SceneIR regeneration)', 'FAIL', {
      measuredQuantity: 'server startup line + /api/status readiness',
      measured: String(e?.message ?? e).slice(0, 2000),
      failureCaseDetected: 'server failed to start or the startup line never appeared',
    })];
  }
  lifecycle.startupLine = server.startupLine;
  lifecycle.pid = server.pid;
  lifecycle.port = port;
  lifecycle.startupElapsedMs = server.startupElapsedMs;

  const base = `http://127.0.0.1:${port}`;

  // ---- T7-1 server startup + loopback + free-port verification ----
  {
    const status = await (await fetch(`${base}/api/status`)).json();
    const startupOk = server.startupLine.includes(`http://127.0.0.1:${port}/`) &&
      server.startupLine.includes(`pid=${server.pid}`);
    const measured = {
      startupLine: server.startupLine,
      statusBind: status.bind, statusPort: status.port, statusPid: status.pid,
      sceneirModel: status.sceneir?.modelId, cacheKey: status.sceneir?.cacheKey,
      counts: status.sceneir?.counts, threeVersion: status.three?.version,
      startupElapsedMs: server.startupElapsedMs,
    };
    records.push(rec('T7_SERVER_START', 'server starts on a verified-free loopback port with fail-closed regenerated SceneIR', ok(
      startupOk && status.bind === '127.0.0.1' && status.port === port && status.pid === server.pid &&
      status.sceneir?.modelId === 218757 && status.readOnly === true &&
      status.sceneir?.counts?.meshes === 14 && status.three?.version === '0.185.0',
    ), {
      measuredQuantity: 'startup line + /api/status fields (bind/port/pid/modelId/counts/three pin)',
      measured,
      independentSourceOfTruth: 'the child process stdout startup line and the live /api/status response — neither is produced by the test code',
      whyNonCircular: 'the test only observes what the server itself prints and serves',
      failureCaseDetected: 'bind not loopback / pid mismatch / SceneIR not regenerated / three pin broken',
    }));
    lifecycle.statusSnapshot = measured;
  }

  // ---- T7-2 app static surface loads ----
  {
    const reqs = await Promise.all([
      fetch(`${base}/`), fetch(`${base}/compat/app.js`), fetch(`${base}/compat/compat.css`),
      fetch(`${base}/src/pecompat/PecRenderConvert.js`),
      fetch(`${base}/node_modules/three/build/three.module.js`),
    ]);
    const bodies = await Promise.all(reqs.map((r) => r.text()));
    const idxHtml = bodies[0];
    const checks = {
      root: reqs[0].status === 200 && reqs[0].headers.get('content-type')?.includes('text/html') &&
        idxHtml.includes('id="view-canvas"') && idxHtml.includes('id="diagnostics"'),
      appJs: reqs[1].status === 200 && bodies[1].includes('mountAssetMode'),
      css: reqs[2].status === 200,
      pecModule: reqs[3].status === 200 && bodies[3].includes('buildRenderModel'),
      three: reqs[4].status === 200 && bodies[4].length > 100000 && bodies[4].includes('REVISION'),
    };
    for (const [url, r, body] of [
      ['/', reqs[0], idxHtml], ['/compat/app.js', reqs[1], bodies[1]], ['/compat/compat.css', reqs[2], bodies[2]],
      ['/src/pecompat/PecRenderConvert.js', reqs[3], bodies[3]], ['/node_modules/three/build/three.module.js', reqs[4], bodies[4]],
    ]) {
      T({ kind: 'positive', method: 'GET', url, status: r.status, contentType: r.headers.get('content-type'), bytes: body.length });
    }
    records.push(rec('T7_APP_STATIC_LOADS', 'app static surface loads (index/app/css/pec module/pinned three)', ok(Object.values(checks).every(Boolean)), {
      measuredQuantity: 'HTTP statuses + body markers (canvas/diagnostics ids, module exports, three module size)',
      measured: checks,
      independentSourceOfTruth: 'real local HTTP responses over the wire',
      whyNonCircular: 'the served bytes are compared against expectations fixed before the request',
      failureCaseDetected: 'any static file missing, wrong type, or the three pin route broken',
    }));
  }

  // ---- T7-3 SceneIR endpoint serves the bounded regenerated data ----
  {
    const r = await fetch(`${base}/api/sceneir/218757`);
    const wire = await r.json();
    const bound = (wire.textureBindings ?? []).filter((b) => b.status === 'TEXTURE_NAME_BOUND').length;
    const untextured = (wire.textureBindings ?? []).filter((b) => String(b.status).startsWith('UNTEXTURED')).length;
    const geoBlocks = wire.blocks.filter((b) => b.geometry).length;
    const firstGeo = wire.blocks.find((b) => b.geometry)?.geometry ?? null;
    const measured = {
      status: r.status,
      payloadSha256: wire.provenance?.payloadSha256,
      containerSha256: wire.provenance?.containerSha256,
      cacheKey: wire.cacheKey,
      blocks: wire.blocks?.length,
      meshAssociations: wire.meshAssociations?.length,
      decodeCensus: wire.decodeCensus,
      textureBound: bound, textureUntextured: untextured,
      geometryBlocks: geoBlocks,
      firstGeoSanity: firstGeo
        ? { positionsLen: firstGeo.positions.length, expectedPos: firstGeo.numVertices * 3,
            indicesLen: firstGeo.indices.length, expectedIdx: firstGeo.numTriangles * 3,
            vertexSha: firstGeo.vertexPositionsF32leSha256 }
        : null,
      headersPayloadSha: r.headers.get('X-PE-Payload-Sha256'),
      adapterLoadElapsedMs: wire.provenance?.elapsedMs,
    };
    T({ kind: 'positive', method: 'GET', url: '/api/sceneir/218757', status: r.status, contentType: r.headers.get('content-type'), bytes: Number(r.headers.get('content-length') ?? 0), measured });
    const expect = measured.payloadSha256 === PIN.payloadSha256 && measured.containerSha256 === PIN.containerSha256 &&
      measured.blocks === 66 && measured.meshAssociations === 14 &&
      measured.decodeCensus?.SUPPORTED === 62 && measured.decodeCensus?.PARTIALLY_UNDERSTOOD === 2 &&
      measured.decodeCensus?.OPAQUE === 2 && bound === 9 && untextured === 5 &&
      geoBlocks === 14 && measured.firstGeoSanity?.positionsLen === measured.firstGeoSanity?.expectedPos &&
      measured.firstGeoSanity?.indicesLen === measured.firstGeoSanity?.expectedIdx &&
      measured.cacheKey?.includes(PIN.payloadSha256);
    records.push(rec('T7_SCENEIR_ENDPOINT', 'SceneIR endpoint serves the bounded index-derived regenerated data (pins + 62+4=66 + 14 associations + 9/5 texture statuses)', ok(expect), {
      measuredQuantity: 'served wire payload fields vs the run pins and the phase-2 measured accounting',
      measured,
      independentSourceOfTruth: 'the pinned SHA256 identities + the predecessor-measured 62+4=66 / 14 / 9+5 accounting',
      whyNonCircular: 'the endpoint content is compared to externally pinned hashes and counts, not to its own claim',
      failureCaseDetected: 'stale/unpinned data, wrong counts, wire geometry inconsistent with its own counts',
    }));
  }

  // ---- T7-4 path-denial battery (RAW paths on the wire — no client normalization) ----
  {
    const denyCases = [
      // [id, rawPath, expectedClass-ish] — all must be non-2xx with explicit JSON error
      ['TRAVERSAL_COMPAT', '/compat/../server.mjs'],
      ['TRAVERSAL_COMPAT_DECODED', '/compat/%2e%2e/server.mjs'],
      ['TRAVERSAL_COMPAT_ENCODED_SLASH', '/compat/..%2f..%2fsrc%2fpesource%2fNifModelReader.js'],
      ['UNCONFIGURED_ROOT_PESOURCE', '/src/pesource/NifModelReader.js'],
      ['UNCONFIGURED_PEC_ESCAPE', '/src/pecompat/../pesource/Bnt2Archive.js'],
      ['UNALLOWLISTED_PEC_MODULE', '/src/pecompat/PecAssetAdapter.js'],
      ['THREE_ESCAPE_PARENT', '/node_modules/three/../package.json'],
      ['THREE_ESCAPE_GRANDPARENT', '/node_modules/three/../../server.mjs'],
      ['THREE_ESCAPE_ENCODED_BACKSLASH', '/node_modules/three/build/..%5C..%5Cpackage.json'],
      ['ABSOLUTE_DRIVE_PATH', '/D:/Eudoria_Reconstruction/pcg_install/Data/Models/Models.bnt'],
      ['ABSOLUTE_DRIVE_PATH_DBL', '//D:/Eudoria_Reconstruction/pcg_install/Data/Models/Models.bnt'],
      ['RAW_DOTDOT_ROOT', '/..'],
      ['RAW_TRAVERSAL_UP', '/../'],
      ['UNKNOWN_ASSET_ID', '/api/sceneir/999999'],
      ['NONEXISTENT_ARCHIVE_ROUTE', '/api/archive/Models.bnt/entry/218757.nif'],
      ['UNCONFIGURED_DOCS_ROOT', '/docs/audits/PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009/PLAN_AND_PATH_ALLOWLIST.md'],
      ['UNCONFIGURED_TOOLS_ROOT', '/tools/pecompat/sceneir_dump.mjs'],
      ['UNCONFIGURED_SERVER_FILE', '/compat/server-sceneir.mjs'],
    ];
    const results = [];
    for (const [id, rawPath] of denyCases) {
      const r = await rawRequest(port, 'GET', rawPath);
      const body = parseJsonOrNone(r.bodyText);
      const explicit = !!body?.error && body.ok === false;
      const noLeak = !/NetImmerse|Gamebryo File Format/i.test(r.bodyText);
      const verdict = (r.status >= 400 && explicit && noLeak) ? 'DENIED_EXPLICIT' : 'NOT_DENIED_OR_IMPLICIT';
      results.push({ id, rawPath, status: r.status, errorClass: body?.error ?? null, message: body?.message?.slice(0, 200) ?? null, bytes: r.bytes, verdict });
      T({ kind: 'denial', method: 'GET', rawPath, status: r.status, errorClass: body?.error ?? null, message: body?.message?.slice(0, 220) ?? null, bytes: r.bytes, verdict, noPayloadLeak: noLeak });
    }
    const allDenied = results.every((x) => x.verdict === 'DENIED_EXPLICIT');
    records.push(rec('T7_PATH_DENIAL_BATTERY', 'synthetic malicious paths (../, absolute, encoded traversal, unconfigured root, unknown route) all DENIED with explicit errors', ok(allDenied), {
      measuredQuantity: 'per-request status + explicit error class + no NIF/BNT payload markers in the body',
      measured: results,
      independentSourceOfTruth: 'the wire responses themselves (raw paths sent un-normalized over real HTTP)',
      whyNonCircular: 'the server code under test is exercised through its public socket; denial classes are read from its own JSON errors',
      failureCaseDetected: results.filter((x) => x.verdict !== 'DENIED_EXPLICIT').map((x) => x.id),
    }));

    // malformed URL + null byte + non-GET method
    const malformed = [];
    for (const [id, method, rawPath] of [
      ['MALFORMED_PERCENT', 'GET', '/compat/%zz'],
      ['NULL_BYTE', 'GET', '/compat/%00index.html'],
      ['POST_METHOD', 'POST', '/api/sceneir/218757'],
      ['PUT_METHOD', 'PUT', '/api/sceneir/218757'],
    ]) {
      const r = await rawRequest(port, method, rawPath);
      const body = parseJsonOrNone(r.bodyText);
      const verdict = r.status >= 400 && !!body?.error ? 'DENIED_EXPLICIT' : 'NOT_DENIED';
      malformed.push({ id, method, rawPath, status: r.status, errorClass: body?.error ?? null, verdict });
      T({ kind: 'denial', method, rawPath, status: r.status, errorClass: body?.error ?? null, verdict });
    }
    records.push(rec('T7_MALFORMED_AND_METHOD_DENIAL', 'malformed percent/null-byte URLs refused; non-GET methods refused (read-only API)', ok(malformed.every((x) => x.verdict === 'DENIED_EXPLICIT')), {
      measuredQuantity: 'status + explicit error class per request',
      measured: malformed,
      independentSourceOfTruth: 'raw wire responses',
      whyNonCircular: 'the requests exercise the server parser and method gate directly',
      failureCaseDetected: malformed.filter((x) => x.verdict !== 'DENIED_EXPLICIT').map((x) => x.id),
    }));
  }

  // ---- lifecycle stop + port-freed proof ----
  const stop = await stopServer(server);
  lifecycle.stop = stop;
  await writeFile(path.join(rawDir, 'HTTP_TRANSCRIPTS.json'), JSON.stringify({
    run: 'PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009',
    suite: 'tests/pecompat/api_path_denial.test.mjs (T7)',
    port, pid: server.pid, base,
    lifecycle,
    transcript,
  }, null, 1) + '\n', 'utf8');

  records.push(rec('T7_SERVER_LIFECYCLE', 'bounded server lifecycle: own PID/port recorded, process stopped, port FREED', ok(stop.portFreed && stop.exitCode !== undefined), {
    measuredQuantity: 'exit code + port rebind probe after kill',
    measured: { pid: server.pid, port, ...stop },
    independentSourceOfTruth: 'child exit event + a fresh bind/close probe of the same port',
    whyNonCircular: 'port freeness is measured by the OS accept path, not by trust in the kill call',
    failureCaseDetected: stop.portFreed ? 'none' : 'PORT NOT FREED — untracked writer left behind',
  }));

  return records;
}
