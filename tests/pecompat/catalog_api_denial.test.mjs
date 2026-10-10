// catalog_api_denial.test.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 4 (W6)
// T7-STYLE API/PATH-DENIAL gates for the NEW catalog server
// (contract §5/§7): positives (app statics, catalog APIs, ONE model wire via
// the index-derived route) and SYNTHETIC negatives (traversal, absolute,
// encoded, backslash, NUL, unconfigured roots, unknown assets, non-GET
// methods, the SceneIR route NOT served by this server, whole-corpus
// attempts) — every request+response recorded to the raw HTTP transcript.
// REUSE LABEL: the pattern follows tests/pecompat/api_path_denial.test.mjs
// (the sceneir T7 suite — rawRequest over the wire, lifecycle owned by the
// suite); the server lifecycle helpers are _catalog_server_helpers.mjs
// (which reuse _app_server_helpers.mjs unchanged for the generic parts).
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import {
  startCatalogServer, stopCatalogServer, findFreePort, rawRequest, parseJsonOrNone,
} from './_catalog_server_helpers.mjs';
import { PRIMARY_PINS, CATALOG_PINS } from '../../tools/pecompat/catalog_data.mjs';

const RUN_ID = 'PE_CITY_ASSET_MAP_R1_20261010';

function rec(id, name, status, extra = {}) {
  return { id, name, status, ...extra };
}
const ok = (b) => (b ? 'PASS' : 'FAIL');

export async function run(ctx) {
  const rawDir = ctx.rawDir;
  await mkdir(rawDir, { recursive: true });
  const transcript = [];
  const records = [];
  const T = (entry) => { transcript.push(entry); return entry; };

  const port = await findFreePort(8161); // NEVER 8140 (foreign reference server)
  let server;
  try {
    server = await startCatalogServer({ port, timeoutMs: 180000 });
  } catch (e) {
    return [rec('CAT_T7_SERVER_START', 'catalog server starts (verified-free port, loopback bind, fail-closed regeneration)', 'FAIL', {
      measuredQuantity: 'server startup line + /api/catalog/status readiness',
      measured: String(e?.message ?? e).slice(0, 2000),
      failureCaseDetected: 'server failed to start or the startup line never appeared',
    })];
  }
  const base = `http://127.0.0.1:${port}`;

  // ---- CAT-T7-1: startup + loopback + identity snapshot ----
  {
    const status = await (await fetch(`${base}/api/catalog/status`)).json();
    const startupOk = server.startupLine.includes(`http://127.0.0.1:${port}/`) &&
      server.startupLine.includes(`pid=${server.pid}`);
    const measured = {
      startupLine: server.startupLine,
      startupElapsedMs: server.startupElapsedMs,
      bind: status.bind, port: status.port, pid: status.pid, readOnly: status.readOnly,
      threeVersion: status.three?.version,
      rows: status.coverage?.totalRows,
      byEra: status.coverage?.byEra,
      byDecode: status.coverage?.byDecodeCoverage,
      extentMeasured: status.coverage?.sceneExtent?.measured,
      overlapSameNameBothEras: status.overlapSameNameBothEras?.count,
      modelsBntPin: status.containers?.PCG_9_3_5_Models_bnt?.pin,
      modelsBntSha: status.containers?.PCG_9_3_5_Models_bnt?.sha256,
      modelsArkSha: status.containers?.CD_2003_Models_ark?.sha256,
      crc32: {
        cd: [status.containers?.CD_2003_Models_ark?.crc32Verified, status.containers?.CD_2003_Models_ark?.crc32Mismatch],
        pcg: [status.containers?.PCG_9_3_5_Models_bnt?.crc32Verified, status.containers?.PCG_9_3_5_Models_bnt?.crc32Mismatch],
      },
    };
    T({ kind: 'positive', method: 'GET', url: '/api/catalog/status', status: 200, bytes: JSON.stringify(status).length });
    records.push(rec('CAT_T7_SERVER_START', 'catalog server starts on a verified-free loopback port with fail-closed regenerated catalogs (both container pins + per-entry CRC verified)', ok(
      startupOk && status.bind === '127.0.0.1' && status.port === port && status.pid === server.pid &&
      status.readOnly === true && status.three?.version === '0.185.0' &&
      status.coverage?.totalRows === 8088 && status.coverage?.byEra?.CD_2003 === 2492 &&
      status.coverage?.byEra?.PCG_9_3_5 === 5596 &&
      status.coverage?.sceneExtent?.measured === 1555 &&
      status.containers?.PCG_9_3_5_Models_bnt?.sha256 === CATALOG_PINS.modelsBnt.sha256 &&
      status.containers?.CD_2003_Models_ark?.sha256 === CATALOG_PINS.modelsArk.sha256 &&
      status.containers?.CD_2003_Models_ark?.crc32Mismatch === 0 &&
      status.containers?.PCG_9_3_5_Models_bnt?.crc32Mismatch === 0,
    ), {
      measuredQuantity: 'startup line + /api/catalog/status fields (bind/port/pid/rows/coverage/pins/CRC)',
      measured,
      independentSourceOfTruth: 'the child process stdout startup line and the live /api/catalog/status response',
      whyNonCircular: 'the test only observes what the server itself prints and serves',
      failureCaseDetected: 'bind not loopback / pin mismatch / coverage wrong / CRC mismatch present',
    }));
  }

  // ---- CAT-T7-2: app static surface loads ----
  {
    const reqs = await Promise.all([
      fetch(`${base}/catalog`), fetch(`${base}/compat/catalog-app.js`),
      fetch(`${base}/compat/catalog-preview.js`), fetch(`${base}/compat/catalog-table.js`),
      fetch(`${base}/compat/catalog.css`), fetch(`${base}/src/pecompat/PecSceneIR.js`),
      fetch(`${base}/node_modules/three/build/three.module.js`),
    ]);
    const bodies = await Promise.all(reqs.map((r) => r.text()));
    const checks = {
      catalogHtml: reqs[0].status === 200 && bodies[0].includes('id="view-canvas"') && bodies[0].includes('id="diagnostics"') && bodies[0].includes('data-load-status'),
      catalogApp: reqs[1].status === 200 && bodies[1].includes('mountCatalogPreview'),
      catalogPreview: reqs[2].status === 200 && bodies[2].includes('wrapperOffsetFor'),
      catalogTable: reqs[3].status === 200 && bodies[3].includes('rowsTableHtml'),
      css: reqs[4].status === 200,
      pecModule: reqs[5].status === 200 && bodies[5].includes('composeWorldTransforms'),
      three: reqs[6].status === 200 && bodies[6].length > 100000 && bodies[6].includes('REVISION'),
    };
    for (const [i, url] of ['/catalog', '/compat/catalog-app.js', '/compat/catalog-preview.js', '/compat/catalog-table.js', '/compat/catalog.css', '/src/pecompat/PecSceneIR.js', '/node_modules/three/build/three.module.js'].entries()) {
      T({ kind: 'positive', method: 'GET', url, status: reqs[i].status, bytes: bodies[i].length });
    }
    records.push(rec('CAT_T7_APP_STATICS', 'catalog app static surface loads (catalog.html with the T9 gate markers, app/preview/table modules, css, the client composition module, pinned three)', ok(Object.values(checks).every(Boolean)), {
      measuredQuantity: 'HTTP statuses + body markers',
      measured: checks,
      failureCaseDetected: 'any catalog static missing or a marker absent',
    }));
  }

  // ---- CAT-T7-3: rows API — sorting/UNKNOWN rule/coverage + cross-checks ----
  {
    const r1 = await (await fetch(`${base}/api/catalog/rows?era=CD_2003&pageSize=5&sort=size`)).json();
    const r2 = await (await fetch(`${base}/api/catalog/rows?sort=extent&pageSize=10`)).json();
    const r3 = await (await fetch(`${base}/api/catalog/rows?era=PCG_9_3_5&sort=extent&pageSize=5`)).json();
    const r4 = await (await fetch(`${base}/api/catalog/rows?q=193313&pageSize=10`)).json();
    const r5 = await (await fetch(`${base}/api/catalog/rows?q=65678&pageSize=10`)).json();
    const badFilter = await rawRequest(port, 'GET', '/api/catalog/rows?era=BOGUS');
    const badSort = await rawRequest(port, 'GET', '/api/catalog/rows?sort=bogus');
    // cross-checks vs frozen/known values:
    const topCdSize = r1.rows[0]; // frozen phase-2: 212124.nif 936544 B
    const extentRows = r2.rows;
    const unknownLast = extentRows.filter((r) => r.sceneExtent.unknown).length === 0 ||
      extentRows.every((r, i) => !r.sceneExtent.unknown || extentRows.slice(i).every((x) => x.sceneExtent.unknown));
    const measuredDesc = extentRows.filter((r) => !r.sceneExtent.unknown)
      .every((r, i, arr) => i === 0 || arr[i - 1].sceneExtent.maxAxisExtent >= r.sceneExtent.maxAxisExtent);
    const primSearch = r4.rows.find((x) => x.era === 'CD_2003' && x.entryName === '193313.nif');
    const overlapRows = r5.rows.filter((x) => x.entryName === '65678.nif');
    const allOk =
      r1.total === 2492 && topCdSize.entryName === '212124.nif' && topCdSize.sizeBytes === 936544 &&
      r2.sortRule.includes('UNKNOWN') && unknownLast && measuredDesc &&
      r3.rows.every((x) => x.era === 'PCG_9_3_5') &&
      primSearch && primSearch.decodeCoverage === 'DECODED_FULL_CLOSURE' && primSearch.previewable === true &&
      primSearch.sceneExtent.maxAxisExtent === 31765.8515625 &&
      overlapRows.length === 2 && new Set(overlapRows.map((x) => x.era)).size === 2 &&
      badFilter.status === 400 && badSort.status === 400;
    T({ kind: 'positive', method: 'GET', url: '/api/catalog/rows?era=CD_2003&pageSize=5&sort=size', status: 200 });
    T({ kind: 'negative', method: 'GET', url: '/api/catalog/rows?era=BOGUS', status: badFilter.status, error: parseJsonOrNone(badFilter.bodyText)?.error });
    T({ kind: 'negative', method: 'GET', url: '/api/catalog/rows?sort=bogus', status: badSort.status, error: parseJsonOrNone(badSort.bodyText)?.error });
    records.push(rec('CAT_T7_ROWS_API', 'rows API: totals + frozen-phase-2 cross-check (212124.nif rank 1), UNKNOWN-last sort rule, era separation of the overlapping 65678 rows, previewable primary with frozen bounds, bogus filter/sort rejected 400', ok(allOk), {
      measuredQuantity: 'rows API responses (order, coverage, search, filters) + denial statuses',
      measured: {
        cdTotal: r1.total, topCdSize: { name: topCdSize.entryName, sizeBytes: topCdSize.sizeBytes },
        sortRule: r2.sortRule, unknownLast, measuredDesc,
        primarySearchRow: { era: primSearch?.era, decodeCoverage: primSearch?.decodeCoverage, previewable: primSearch?.previewable, maxAxisExtent: primSearch?.sceneExtent?.maxAxisExtent },
        overlap65678: overlapRows.map((x) => x.era),
        badFilter: { status: badFilter.status, error: parseJsonOrNone(badFilter.bodyText)?.error },
        badSort: { status: badSort.status, error: parseJsonOrNone(badSort.bodyText)?.error },
      },
      independentSourceOfTruth: 'the frozen phase-2 PAYLOAD_SIZE rank 1 + the frozen phase-3 primary bounds (values fixed before this phase)',
      whyNonCircular: 'the live server never reads those frozen artifacts; agreement is a real cross-check',
      failureCaseDetected: allOk ? 'none' : 'a rows-API behavior deviates (see measured)',
    }));
  }

  // ---- CAT-T7-4: ONE model wire via the index-derived route (positive) ----
  {
    const res = await fetch(`${base}/api/catalog/model/CD_2003/193313`);
    const wire = await res.json();
    const checks = {
      status200: res.status === 200,
      pins: wire.pins.payloadSha256 === PRIMARY_PINS['193313'].sha256 &&
        wire.pins.containerSha256 === CATALOG_PINS.modelsArk.sha256,
      bounds: wire.sceneBounds_FILE_SCENE_SPACE.maxAxisExtent === 31765.8515625,
      untextured: wire.textureDiagnostics.disposition === 'UNTEXTURED_PROXY_MESH' &&
        wire.textureDiagnostics.uvSets === 0 && wire.textureDiagnostics.arkTextureNumTex === 0,
      materials: wire.materials.length === 5 && wire.materials.every((m) => m.referenceClass.startsWith('REFERENCE_CONFIRMED')),
      meshes: wire.meshRows.length === 5,
      headerPayloadSha: res.headers.get('x-pe-payload-sha256') === PRIMARY_PINS['193313'].sha256,
    };
    T({ kind: 'positive', method: 'GET', url: '/api/catalog/model/CD_2003/193313', status: res.status, bytes: JSON.stringify(wire).length });
    records.push(rec('CAT_T7_MODEL_WIRE', 'the bounded preview wire for 193313 serves via the index-derived route (pins in headers+body, frozen bounds, UNTEXTURED_PROXY_MESH diagnostics, 5 verified material edges)', ok(Object.values(checks).every(Boolean)), {
      measuredQuantity: 'wire pins/bounds/diagnostics/materials + response headers',
      measured: checks,
      independentSourceOfTruth: 'the phase-3 frozen primary measurements (payload SHA + bounds) and the live re-decode',
      whyNonCircular: 'expected values were frozen in the phase-3 checkpoint before this phase',
      failureCaseDetected: 'wire identity or measured values deviate from the checkpoint',
    }));
  }

  // ---- CAT-T7-5: SYNTHETIC denial battery (traversal/absolute/encoded/...) ----
  {
    const negatives = [
      ['TRAVERSAL_RELATIVE', '/compat/../server-catalog.mjs'],
      ['TRAVERSAL_ABSOLUTE', '/C:/Windows/system32/drivers/etc/hosts'],
      ['TRAVERSAL_ENCODED', '/compat/%2e%2e/%2e%2e/src/pesource/ArkArchive.js'],
      ['TRAVERSAL_SRC', '/src/pecompat/../../../package.json'],
      ['BACKSLASH', '/compat/..\\..\\package.json'],
      ['UNCONFIGURED_ROOT', '/pcg/Models.bnt'],
      ['WHOLE_CORPUS_ATTEMPT', '/Models.bnt'],
      ['UNKNOWN_ASSET_ID', '/api/catalog/model/CD_2003/999999999'],
      ['NOT_PREVIEWABLE_REAL_ENTRY', '/api/catalog/model/CD_2003/65678'],
      ['PCG_NO_PREVIEW_ROUTE', '/api/catalog/model/PCG_9_3_5/218757'],
      ['SCENEIR_ROUTE_NOT_SERVED', '/api/sceneir/218757'],
      ['UNKNOWN_ROUTE', '/definitely/not/a/route'],
      ['UNALLOWLISTED_COMPAT', '/compat/app.js'],
    ];
    const results = [];
    let allDenied = true;
    for (const [label, rawPath] of negatives) {
      const r = await rawRequest(port, 'GET', rawPath);
      const body = parseJsonOrNone(r.bodyText);
      const denied = (r.status === 403 || r.status === 400 || r.status === 404 || r.status === 405) &&
        body && typeof body.error === 'string' && body.error.length > 0;
      // special expectations:
      let expectationMet = denied;
      if (label === 'SCENEIR_ROUTE_NOT_SERVED') expectationMet = denied && body.error === 'ROUTE_NOT_FOUND';
      if (label === 'NOT_PREVIEWABLE_REAL_ENTRY') expectationMet = denied && body.error === 'PREVIEW_NOT_ESTABLISHED' && /CATALOG_ONLY/.test(body.message ?? '');
      if (label === 'PCG_NO_PREVIEW_ROUTE') expectationMet = denied && body.error === 'UNKNOWN_ASSET_ROUTE';
      if (label === 'UNALLOWLISTED_COMPAT') expectationMet = denied && body.error === 'STATIC_FILE_NOT_ALLOWEDLISTED' && /not in the catalog allowlist/.test(body.message ?? '');
      results.push({ label, rawPath, status: r.status, error: body?.error, messageExcerpt: String(body?.message ?? '').slice(0, 120), denied, expectationMet });
      if (!expectationMet) allDenied = false;
      T({ kind: 'negative', method: 'GET', url: rawPath, status: r.status, error: body?.error, messageExcerpt: String(body?.message ?? '').slice(0, 160) });
    }
    // non-GET method
    const post = await rawRequest(port, 'POST', '/api/catalog/rows');
    const postDenied = post.status === 405 && parseJsonOrNone(post.bodyText)?.error === 'METHOD_NOT_ALLOWED_READ_ONLY';
    T({ kind: 'negative', method: 'POST', url: '/api/catalog/rows', status: post.status, error: parseJsonOrNone(post.bodyText)?.error });
    if (!postDenied) allDenied = false;
    records.push(rec('CAT_T7_DENIALS', 'synthetic denial battery: traversal/absolute/encoded/backslash/unconfigured-root/whole-corpus/unknown-asset/non-previewable/SceneIR-route/unknown-route/unallowlisted-static all DENIED_EXPLICIT; POST refused 405', ok(allDenied && postDenied), {
      measuredQuantity: 'raw HTTP statuses + named error bodies for every negative request',
      measured: { negatives: results, post: { status: post.status, error: parseJsonOrNone(post.bodyText)?.error } },
      independentSourceOfTruth: 'raw sockets over the wire (no client-side URL normalization)',
      whyNonCircular: 'the paths go on the wire verbatim; the server must refuse them by construction',
      failureCaseDetected: allDenied && postDenied ? 'none — every negative was refused with a named error' : 'a negative request was NOT denied as specified (DEFECT)',
    }));
  }

  // ---- lifecycle stop + transcript persistence ----
  const stop = await stopCatalogServer(server);
  records.push(rec('CAT_T7_SERVER_LIFECYCLE', `suite-owned bounded catalog server lifecycle (pid ${server.pid}, port ${port}; stop + port-freed proof)`, stop.portFreed ? 'PASS' : 'FAIL', {
    measuredQuantity: 'start/stop/PID/lifetime/port-freed proof',
    measured: {
      pid: server.pid, port, lifetimeMs: stop.lifetimeMs,
      killed: stop.killed, exitCode: stop.exitCode, signal: stop.signal,
      portFreed: stop.portFreed, freedAfterMs: stop.freedAfterMs,
    },
    failureCaseDetected: stop.portFreed ? 'none — server stopped, port freed, nothing left running' : 'port NOT freed after the suite (LIFECYCLE BREACH)',
  }));
  await writeFile(path.join(rawDir, 'CATALOG_HTTP_TRANSCRIPTS.json'), JSON.stringify({
    run: RUN_ID,
    suite: 'tests/pecompat/catalog_api_denial.test.mjs',
    port, pid: server.pid,
    transcript,
  }, null, 1) + '\n', 'utf8').catch(() => {});

  return records;
}
