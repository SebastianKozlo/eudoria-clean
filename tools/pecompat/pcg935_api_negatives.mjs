#!/usr/bin/env node
// pcg935_api_negatives.mjs — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 (Wave 9)
// Gate 7: API negatives against the LIVE server on 127.0.0.1:8164 — every
// probe records the actual response; assertions on truthful denials.
'use strict';
import fs from 'node:fs';
import path from 'node:path';

const BASE = process.env.PCG935_URL_BASE || 'http://127.0.0.1:8164';
const PRIVATE = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010';
const OUT = path.join(PRIVATE, 'tests');

const probes = [
  // traversal attempts
  { m: 'GET', p: '/api/asset/..%2f..%2fserver-pcg935-viewer.mjs', wantStatus: 400, wantCode: 'MALFORMED_ASSET_ID' },
  { m: 'GET', p: '/api/texture/..%5c..%5cModels.bnt', wantStatus: 400, wantCode: 'BACKSLASH_IN_URL' },
  { m: 'GET', p: '/node_modules/three/../server-pcg935-viewer.mjs', wantStatus: 403, wantCode: 'ONLY_THREE_ALLOWED' },
  { m: 'GET', p: '/node_modules/other/package.js', wantStatus: 403, wantCode: 'ONLY_THREE_ALLOWED' },
  { m: 'GET', p: '/%2e%2e/compat/server-pcg935-viewer.mjs', wantStatus: 404 },
  // foreign ids
  { m: 'GET', p: '/api/asset/9999999', wantStatus: 404, wantCode: 'ASSET_ID_NOT_IN_INDEX' },
  { m: 'GET', p: '/api/texture/9999999', wantStatus: 404, wantCode: 'TEXTURE_ID_NOT_IN_INDEX' },
  // malformed
  { m: 'GET', p: '/api/asset/12x34', wantStatus: 400 },
  { m: 'GET', p: '/api/asset/', wantStatus: 400 },
  { m: 'GET', p: '/api/texture/-1', wantStatus: 400 },
  { m: 'GET', p: '/api/asset/%00', wantStatus: 400 },
  // unknown routes
  { m: 'GET', p: '/nope', wantStatus: 404, wantCode: 'ROUTE_NOT_FOUND' },
  { m: 'GET', p: '/api/nope', wantStatus: 404, wantCode: 'ROUTE_NOT_FOUND' },
  // read-only enforcement
  { m: 'POST', p: '/api/asset/223534', wantStatus: 405, wantCode: 'METHOD_NOT_ALLOWED_READ_ONLY' },
  { m: 'DELETE', p: '/api/asset/223534', wantStatus: 405 },
  { m: 'PUT', p: '/app.js', wantStatus: 405 },
  // parse-failed entry returns TRUTHFUL 422 with the real error (592605 = known FAIL)
  { m: 'GET', p: '/api/asset/592605', wantStatus: 422, wantCode: 'PARSE_FAILED_TRUTHFUL' },
  // known-failing texture decode? (jpeg id from the census: find via probe below — skipped here)
];

const results = [];
for (const pr of probes) {
  const res = await fetch(BASE + pr.p, { method: pr.m });
  const text = await res.text();
  let code = null;
  try { code = JSON.parse(text).error ?? null; } catch { }
  const result = { ...pr, gotStatus: res.status, gotCode: code, ok: res.status === pr.wantStatus && (!pr.wantCode || code === pr.wantCode) };
  results.push(result);
  console.log(`${result.ok ? 'ok  ' : 'FAIL'} ${pr.m} ${pr.p.slice(0, 60)} -> ${res.status} ${code ?? ''}${result.ok ? '' : ` (wanted ${pr.wantStatus} ${pr.wantCode ?? ''})`}`);
}
const all = results.every((r) => r.ok);
fs.writeFileSync(path.join(OUT, 'api_negatives.json'), JSON.stringify({ runId: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010', generated: new Date().toISOString(), results, pass: all }, null, 1));
console.log('API NEGATIVES:', all ? 'PASS' : 'NON-PASS');
