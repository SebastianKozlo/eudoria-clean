// QC_t7_subset.mjs — internal QC (pe-master-auditor, fresh session). NOT executor code.
// Re-issues a subset of the T7 denial battery + positive requests against the
// QC's OWN server instance (port 8146, pid recorded separately).
// Verifies: DENIED_EXPLICIT semantics (status + explicit error class), no
// NIF/BNT payload markers in denial bodies, and the three positive endpoints.
import http from 'node:http';

const PORT = 8146;
function req(method, rawPath) {
  return new Promise((resolve, reject) => {
    const r = http.request({ host: '127.0.0.1', port: PORT, method, path: rawPath, setHost: true, timeout: 5000 }, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => resolve({ method, rawPath, status: res.statusCode, headers: res.headers, body: Buffer.concat(chunks).toString('utf8') }));
    });
    r.on('timeout', () => { r.destroy(); reject(new Error('timeout')); });
    r.on('error', (e) => reject(e));
    r.end();
  });
}

const MARKERS = ['NetImmerse', 'Gamebryo File Format'];
const results = [];

async function denial(method, path, expectStatus, expectClass) {
  try {
    const r = await req(method, path);
    let cls = null;
    try { cls = JSON.parse(r.body).error ?? null; } catch { /* non-JSON body */ }
    const leak = MARKERS.some((m) => r.body.includes(m));
    const ok = r.status === expectStatus && cls === expectClass && !leak;
    results.push({ kind: 'DENIAL', method, path, status: r.status, errorClass: cls, noPayloadLeak: !leak, expect: { status: expectStatus, class: expectClass }, ok });
    console.log(`${ok ? 'QC_PASS' : 'QC_FAIL'} ${method} ${JSON.stringify(path)} -> ${r.status} cls=${cls} noLeak=${!leak}`);
  } catch (e) {
    results.push({ kind: 'DENIAL', method, path, error: String(e), ok: false });
    console.log(`QC_FAIL ${method} ${path} -> ERROR ${e}`);
  }
}

async function main() {
  console.log(`== QC T7 subset against 127.0.0.1:${PORT} (own instance) ==`);
  // 8 required denial classes + 2 extras
  await denial('GET', '/compat/../server-sceneir.mjs', 404, 'STATIC_FILE_NOT_ALLOWEDLISTED');          // traversal ../
  await denial('GET', '/compat/%2e%2e/server.mjs', 404, 'STATIC_FILE_NOT_ALLOWEDLISTED');           // %2e%2e
  await denial('GET', '/D:/Eudoria_Reconstruction/pcg_install/Data/Models/Models.bnt', 404, 'ROUTE_NOT_FOUND'); // absolute path
  await denial('GET', '/src/pesource/NifModelReader.js', 404, 'ROUTE_NOT_FOUND');                   // unconfigured root
  await denial('GET', '/api/sceneir/999999', 404, 'UNKNOWN_ASSET_ID');                              // unknown asset
  await denial('GET', '/compat/%00index.html', 400, 'NULL_BYTE_IN_URL');                            // malformed %00
  await denial('POST', '/api/sceneir/218757', 405, 'METHOD_NOT_ALLOWED_READ_ONLY');                 // POST method
  await denial('GET', '/some/unknown/route', 404, 'ROUTE_NOT_FOUND');                              // unknown route
  await denial('GET', '/node_modules/three/../../package.json', 403, 'PATH_TRAVERSAL_BLOCKED');     // three jail escape (extra)
  await denial('GET', '/compat/..%2f..%2fsrc%2fpesource%2fNifModelReader.js', 404, 'STATIC_FILE_NOT_ALLOWEDLISTED'); // encoded (extra)

  // positives
  const pos = [];
  try {
    const r = await req('GET', '/');
    const hasCanvas = r.body.includes('id="view-canvas"') || r.body.includes('view-canvas');
    const hasDiag = r.body.includes('diagnostics') && r.body.includes('data-load-status');
    pos.push({ id: 'APP_HTML', status: r.status, chars: r.body.length, hasCanvas, hasDiagRoot: hasDiag, ok: r.status === 200 && hasCanvas && hasDiag });
    console.log(`QC_APP_HTML status=${r.status} chars=${r.body.length} canvas=${hasCanvas} diagRoot=${hasDiag}`);
  } catch (e) { pos.push({ id: 'APP_HTML', error: String(e), ok: false }); console.log(`QC_FAIL APP_HTML ${e}`); }
  try {
    const r = await req('GET', '/api/status');
    const j = JSON.parse(r.body);
    const ok = j.bind === '127.0.0.1' && j.port === PORT && typeof j.pid === 'number'
      && j.sceneir.counts.blocks === 66 && j.sceneir.counts.meshes === 14
      && j.sceneir.counts.supported === 62 && j.sceneir.counts.partiallyUnderstood === 2
      && j.sceneir.counts.opaque === 2 && j.sceneir.modelId === 218757
      && j.three.version === '0.185.0' && j.readOnly === true
      && j.sceneir.payloadSha256 === '3e8a22c2213202207e374b55cd65b2c3be039ccdd1e8d01a07fcaf44de12cf36';
    pos.push({ id: 'API_STATUS', status: r.status, bind: j.bind, port: j.port, pid: j.pid, counts: j.sceneir.counts, three: j.three.version, readOnly: j.readOnly, ok });
    console.log(`QC_API_STATUS status=${r.status} bind=${j.bind} port=${j.port} pid=${j.pid} blocks=${j.sceneir.counts.blocks} meshes=${j.sceneir.counts.meshes} sup=${j.sceneir.counts.supported} pu=${j.sceneir.counts.partiallyUnderstood} op=${j.sceneir.counts.opaque} three=${j.three.version} ok=${ok}`);
  } catch (e) { pos.push({ id: 'API_STATUS', error: String(e), ok: false }); console.log(`QC_FAIL API_STATUS ${e}`); }
  try {
    const r = await req('GET', '/api/sceneir/218757');
    const j = JSON.parse(r.body);
    const blocks = Array.isArray(j.blocks) ? j.blocks.length : null;
    const assoc = Array.isArray(j.meshAssociations) ? j.meshAssociations.length : null;
    const dc = j.decodeCensus ?? {};
    const hdrPayload = r.headers['x-pe-payload-sha256'] ?? r.headers['X-PE-Payload-Sha256'] ?? null;
    const hdrCache = r.headers['x-pe-cache-key'] ?? null;
    const ok = r.status === 200 && blocks === 66 && assoc === 14
      && dc.SUPPORTED === 62 && dc.PARTIALLY_UNDERSTOOD === 2 && dc.OPAQUE === 2
      && hdrPayload === '3e8a22c2213202207e374b55cd65b2c3be039ccdd1e8d01a07fcaf44de12cf36'
      && (j.provenance?.payloadSha256 === '3e8a22c2213202207e374b55cd65b2c3be039ccdd1e8d01a07fcaf44de12cf36');
    pos.push({ id: 'API_SCENEIR', status: r.status, chars: r.body.length, blocks, assoc, decodeCensus: dc, hdrPayloadSha256: hdrPayload, hdrCacheKey: hdrCache, ok });
    console.log(`QC_API_SCENEIR status=${r.status} chars=${r.body.length} blocks=${blocks} assoc=${assoc} decode=${JSON.stringify(dc)} hdrPayload=${hdrPayload?.slice(0, 16)}... ok=${ok}`);
  } catch (e) { pos.push({ id: 'API_SCENEIR', error: String(e), ok: false }); console.log(`QC_FAIL API_SCENEIR ${e}`); }

  const denOk = results.filter((x) => x.kind === 'DENIAL').every((x) => x.ok);
  const denCount = results.filter((x) => x.ok).length;
  const totalCount = results.length;
  console.log(`\nQC_T7_SUBSET: denials ${denCount}/${totalCount} explicit-clean; positives ${pos.filter((p) => p.ok).length}/${pos.length}`);
  console.log(`QC_T7_SUBSET_VERDICT: ${denOk && pos.every((p) => p.ok) ? 'PASS' : 'FAIL'}`);
}
main().catch((e) => { console.error('QC harness error', e); process.exit(1); });
