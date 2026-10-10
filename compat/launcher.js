// launcher.js — PE_WORLD_LAUNCHER_R1_20261010, ETAP C (contract §4)
// THE /launcher app: original-data connection state + the heightmap overview
// from the REAL terrain.bnt index (server-side census of every regular tile,
// explicitly downsampled to 1 px/tile on screen) + vegetation profile
// selection + the entry button „Uruchom podgląd świata” + the honest
// gaps/unsupported panel. Vanilla ES module — no framework, no Three.js here.
//
// HONESTY CONTRACT in this UI (mirrors the server):
//   - raw u16 = 0 is DATA (not NODATA); NODATA tiles are visible as NODATA;
//   - the overview is a labeled DOWNSAMPLE (tile mean); the RAW uint16 is
//     shown on hover (tile stats) and per-sample in the selected tile
//     preview (fetched from the tile API — real decoded bytes);
//   - era PCG_9_3_5; calibration labels are CURRENT_RUNTIME_CALIBRATION.
'use strict';

const $ = (id) => document.getElementById(id);
const GRID_W = 220, GRID_H = 236, TILE_N = GRID_W * GRID_H;

const state = {
  status: null,
  overview: null,          // {mean,min,max,status} typed arrays
  overviewVersion: -1,     // measured count of the last rendered overview
  selection: null,         // anchor tile {gx,gy} (4x4 patch clamped inside)
  tileDetail: null,        // {gx,gy,heights,meta}
  climates: null,
  climatesError: null,
  gaps: null,
  loopTimer: null,
  bootErrors: [],
};

function hud(msg) { $('hud-line').textContent = msg; }
function banner(msg) {
  const b = $('error-banner');
  if (msg) { b.textContent = msg; b.hidden = false; } else { b.hidden = true; }
}
function setLoadStatus(status) {
  $('diagnostics').setAttribute('data-load-status', status);
  $('diag-boot').textContent = `data-load-status = ${status}`;
}
function setOverviewStatus(status) {
  $('panel-map').setAttribute('data-overview-status', status);
}

async function fetchJson(url) {
  const r = await fetch(url, { cache: 'no-store' });
  const text = await r.text();
  let j = null;
  try { j = JSON.parse(text); } catch { j = null; }
  if (!r.ok) {
    const err = (j && (j.error || j.message)) || `HTTP ${r.status}`;
    throw new Error(`${url} -> ${err}`);
  }
  return j;
}

// ---- palette (RECONSTRUCTION_PREVIEW visualization only; heights are raw) ----
const STOPS = [
  [0.00, 14, 34, 56],
  [0.35, 30, 95, 79],
  [0.55, 107, 122, 69],
  [0.75, 138, 122, 95],
  [1.00, 232, 228, 216],
];
function rawToColor(v, min, max) {
  const t = (max > min) ? (v - min) / (max - min) : 0.5;
  for (let i = 1; i < STOPS.length; i++) {
    if (t <= STOPS[i][0] || i === STOPS.length - 1) {
      const [t0, r0, g0, b0] = STOPS[i - 1];
      const [t1, r1, g1, b1] = STOPS[i];
      const f = Math.min(1, Math.max(0, (t - t0) / (t1 - t0)));
      return `rgb(${Math.round(r0 + f * (r1 - r0))},${Math.round(g0 + f * (g1 - g0))},${Math.round(b0 + f * (b1 - b0))})`;
    }
  }
}
const COLOR_NODATA = '#b03050', COLOR_PENDING = '#2a3546', COLOR_FAILED = '#d65f2e';

// ---- Panel 1: original-data connection state + loading stages ----
function renderDataPanel() {
  const s = state.status;
  $('data-era').textContent =
    `era świata: ${s.era} | kalibracja: ${s.calibration.label} (u16/${s.calibration.u16PerMeter}, ` +
    `${s.calibration.meterPerSample} jedn./próbkę, identity min/max) | indeks: ${s.terrainIndex.totalEntries} wpisów = ` +
    `${s.terrainIndex.regular} zwykłych + ${s.terrainIndex.specialRows} specjalnych + ${s.terrainIndex.sentinel} sentinel`;
  const tbody = $('data-containers').querySelector('tbody');
  const rows = [
    ['terrain.bnt (TEREN — montowany, dekodowany)', s.containers.terrain, 'wyłączone pobieranie kontenera'],
    ['VegetationClimates.bnt (profile .vcl)', s.containers.vegetationClimates, ''],
    ['Models.bnt (tylko weryfikacja SHA)', s.containers.models, 'nie montowany w Etapie C'],
    ['Textures.bnt (tylko weryfikacja SHA)', s.containers.textures, 'nie montowany w Etapie C'],
  ];
  tbody.innerHTML = '';
  for (const [label, c, note] of rows) {
    const tr = document.createElement('tr');
    const stateOk = c.state === 'VERIFIED';
    tr.innerHTML = `<td>${label}${note ? ` <span class="small">(${note})</span>` : ''}</td>` +
      `<td class="mono">${c.sizeBytes ?? '—'}</td>` +
      `<td class="sha-cell mono">${c.sha256 ?? '…'}</td>` +
      `<td class="${stateOk ? '' : 'untextured'} mono">${c.state}</td>`;
    tbody.appendChild(tr);
  }
  renderStages();
}

function renderStages() {
  const s = state.status;
  const c = s.census;
  const cv = s.containers;
  const lines = [
    `etap 1 · montowanie terrain.bnt + VegetationClimates.bnt (piny SHA, fail-closed): ${cv.terrain.state === 'VERIFIED' ? 'OK' : cv.terrain.state}`,
    `etap 2 · weryfikacja SHA Models.bnt + Textures.bnt (strumieniowo, bez montowania): models=${cv.models.state.split(' ')[0]}, textures=${cv.textures.state.split(' ')[0]}`,
    `etap 3 · indeks BNT2 terrain.bnt: ${s.terrainIndex.totalEntries} wpisów (zwykłe ${s.terrainIndex.regular})`,
    `etap 4 · census wysokości (każdy zwykły kafel z oryginalnych bajtów): ${c.measured + c.missing + c.failed}/${c.total}${c.ready ? ' GOTOWE' : ' w toku'}`,
    `etap 5 · profile klimatu .vcl: ${s.containers.vegetationClimates.profiles?.decoded ?? '…'}/32 zdekodowane` +
      (s.containers.vegetationClimates.profiles?.unsupported?.length ? `, UNSUPPORTED: ${s.containers.vegetationClimates.profiles.unsupported.join(', ')}` : ''),
  ];
  $('data-stages').textContent = lines.join('\n');
  const pct = c.total ? Math.min(100, (100 * (c.measured + c.missing + c.failed)) / c.total) : 0;
  $('census-bar').style.width = `${pct.toFixed(1)}%`;
  $('census-progress').textContent =
    `przegląd wysokości (census): ${c.measured} zmierzonych / ${c.missing} brakujących / ${c.failed} błędów — ` +
    `${(c.measured + c.missing + c.failed).toLocaleString('pl-PL')}/${c.total.toLocaleString('pl-PL')} (${pct.toFixed(2)}%)${c.ready ? ' — GOTOWE' : ''}`;
}

// ---- Panel 2: overview map from the real tile census ----
function renderMap() {
  const ov = state.overview;
  const canvas = $('view-canvas');
  const ctx = canvas.getContext('2d');
  const s = state.status;
  const min = s.census.globalMin ?? 0, max = s.census.globalMax ?? 1;
  for (let gy = 0; gy < GRID_H; gy++) {
    for (let gx = 0; gx < GRID_W; gx++) {
      const i = gy * GRID_W + gx;
      const st = ov.status[i];
      let color;
      if (st === 1) color = rawToColor(ov.mean[i], min, max);
      else if (st === 2) color = COLOR_NODATA;
      else if (st === 3) color = COLOR_FAILED;
      else color = COLOR_PENDING;
      ctx.fillStyle = color;
      ctx.fillRect(gx, gy, 1, 1);
    }
  }
  renderCoverage();
  renderLegend();
  renderSelectionBox();
  setOverviewStatus(s.census.ready ? 'READY' : 'PARTIAL');
  $('map-refresh-state').textContent =
    `przegląd: ${s.census.ready ? 'pełny' : 'częściowy (odświeżanie asynchroniczne trwa)'} — wersja ${state.overviewVersion} zmierzonych kaflach`;
}

function renderCoverage() {
  const c = state.status.census;
  const pct = c.total ? (100 * c.measured) / c.total : 0;
  const nodataPct = c.total ? (100 * (c.missing + c.failed)) / c.total : 0;
  $('map-coverage').textContent =
    `pokrycie: zmierzono ${c.measured.toLocaleString('pl-PL')} / ${c.total.toLocaleString('pl-PL')} zwykłych kafli ` +
    `(${pct.toFixed(3)}% mianownika 51 920) | NODATA: ${c.missing} brakujących + ${c.failed} błędów = ` +
    `${nodataPct.toFixed(4)}% | wiersze specjalne: ${state.status.terrainIndex.specialRows} (wykluczone, semantyka UNRESOLVED) | ` +
    `sentinel: ${state.status.terrainIndex.sentinel} (wykluczony) | kafle surowe=0 (to DANE): ${c.zeroTiles ?? '…'}`;
}

function renderLegend() {
  const c = state.status.census;
  const canvas = $('legend-canvas');
  const ctx = canvas.getContext('2d');
  const min = c.globalMin ?? 0, max = c.globalMax ?? 65535;
  for (let y = 0; y < 180; y++) {
    const v = min + ((max - min) * y) / 179;
    ctx.fillStyle = rawToColor(Math.round(v), min, max);
    ctx.fillRect(0, y, 24, 1);
  }
  const m = (v) => (v / 128).toFixed(1);
  $('legend-labels').innerHTML =
    `<span>raw u16 ${max} (${m(max)} m)</span>` +
    `<span>surowa wartość uint16 → kolor (DOWNSAMPLE podglądu)</span>` +
    `<span>raw u16 ${min} (${m(min)} m)</span>`;
}

function patchRect(anchor) {
  // the 4x4 patch anchored at the selection (clamped so the whole patch stays
  // inside the 220x236 regular grid)
  const gx = Math.min(Math.max(anchor.gx, 0), GRID_W - 4);
  const gy = Math.min(Math.max(anchor.gy, 0), GRID_H - 4);
  return { gx, gy, w: 4, h: 4 };
}

function renderSelectionBox() {
  if (!state.selection) { $('map-selection-box').hidden = true; return; }
  const r = patchRect(state.selection);
  const canvas = $('view-canvas');
  const rect = canvas.getBoundingClientRect();
  const sx = rect.width / GRID_W, sy = rect.height / GRID_H;
  const box = $('map-selection-box');
  box.hidden = false;
  box.style.left = `${r.gx * sx}px`;
  box.style.top = `${r.gy * sy}px`;
  box.style.width = `${r.w * sx}px`;
  box.style.height = `${r.h * sy}px`;
  updateLaunchTarget();
}

function tileName(gx, gy) {
  return gx.toString(16).padStart(4, '0') + gy.toString(16).padStart(4, '0') + '.tdf';
}

function mapTileFromEvent(ev) {
  const canvas = $('view-canvas');
  const rect = canvas.getBoundingClientRect();
  const gx = Math.floor(((ev.clientX - rect.left) / rect.width) * GRID_W);
  const gy = Math.floor(((ev.clientY - rect.top) / rect.height) * GRID_H);
  if (gx < 0 || gy < 0 || gx >= GRID_W || gy >= GRID_H) return null;
  return { gx, gy };
}

function onMapHover(ev) {
  const t = mapTileFromEvent(ev);
  if (!t) { $('map-hover').textContent = 'hover: poza siatką'; return; }
  const ov = state.overview;
  if (!ov) { $('map-hover').textContent = 'hover: przegląd jeszcze niezaładowany'; return; }
  const i = t.gy * GRID_W + t.gx;
  const st = ov.status[i];
  const s = state.status.calibration;
  if (st !== 1) {
    $('map-hover').textContent =
      `hover: kafel ${tileName(t.gx, t.gy)} (gx=${t.gx}, gy=${t.gy}) — ${st === 2 ? 'NODATA (brak wpisu w indeksie)' : st === 3 ? 'NODATA (błąd dekodowania)' : 'oczekuje na census'} — NIE jest to wysokość 0`;
    return;
  }
  $('map-hover').textContent =
    `hover: kafel ${tileName(t.gx, t.gy)} (gx=${t.gx}, gy=${t.gy}) — surowe uint16 kafla: min=${ov.min[i]} · średnia=${ov.mean[i]} (ta mapa = DOWNSAMPLE do średniej) · max=${ov.max[i]} ` +
    `| metry (÷${s.u16PerMeter}, CURRENT_RUNTIME_CALIBRATION): min=${(ov.min[i] / s.u16PerMeter).toFixed(1)} max=${(ov.max[i] / s.u16PerMeter).toFixed(1)}`;
}

async function onMapClick(ev) {
  const t = mapTileFromEvent(ev);
  if (!t) return;
  state.selection = { gx: t.gx, gy: t.gy };
  renderSelectionBox();
  hud(`wybrano kafel ${tileName(t.gx, t.gy)} — fragment 4×4 do podglądu świata`);
  await loadTileDetail(t.gx, t.gy);
}

async function loadTileDetail(gx, gy) {
  const box = $('tile-detail');
  box.hidden = false;
  $('tile-detail-head').textContent = `wybrany kafel ${tileName(gx, gy)} — pobieram surowe próbki (2048 B, uint16 LE)…`;
  try {
    const [r, meta] = await Promise.all([
      fetch(`/api/world/tile/${gx}/${gy}`, { cache: 'no-store' }),
      fetchJson(`/api/world/tile/${gx}/${gy}/meta`),
    ]);
    if (!r.ok) throw new Error(`tile HTTP ${r.status}`);
    const buf = await r.arrayBuffer();
    if (buf.byteLength !== 2048) throw new Error(`tile bytes ${buf.byteLength} != 2048`);
    const heights = new Uint16Array(buf);
    state.tileDetail = { gx, gy, heights, meta };
    const c = state.status.calibration;
    const mn = meta.stats.min, mx = meta.stats.max, mean = meta.stats.mean;
    $('tile-detail-head').textContent =
      `wybrany kafel ${tileName(gx, gy)} — 1024 surowych próbek uint16 (offset 64..2111, bez normalizacji) | min=${mn} średnia=${mean} max=${mx} (metry ÷${c.u16PerMeter}: ${(mn / c.u16PerMeter).toFixed(1)}..${(mx / c.u16PerMeter).toFixed(1)})`;
    // draw the per-sample raw preview (nearest-neighbor upscale by CSS)
    const tc = $('tile-canvas');
    const tctx = tc.getContext('2d');
    const gmin = state.status.census.globalMin ?? 0, gmax = state.status.census.globalMax ?? 65535;
    for (let y = 0; y < 32; y++) {
      for (let x = 0; x < 32; x++) {
        tctx.fillStyle = rawToColor(heights[y * 32 + x], gmin, gmax);
        tctx.fillRect(x, y, 1, 1);
      }
    }
    const p = meta.provenance;
    $('tile-meta').textContent =
      `provenance: era=${p.era} kontener=${p.container} wpis=${p.entry} offset=${p.offset} dekoder=${p.decoderVersion} ` +
      `SHA kontenera=${String(state.status.containers.terrain.sha256 ?? '').slice(0, 16)}… | cache=${meta.cache.state} ` +
      `| polityka NODATA: brakujący/błędny kafel = NODATA (nigdy wysokość 0); surowe 0 = DANE`;
  } catch (e) {
    state.tileDetail = null;
    $('tile-detail-head').textContent = `błąd pobierania kafla ${tileName(gx, gy)}: ${e.message} (uczciwy błąd — bez zmyślonych danych)`;
    banner(`tile detail: ${e.message}`);
  }
}

function onTileCanvasHover(ev) {
  if (!state.tileDetail) return;
  const canvas = $('tile-canvas');
  const rect = canvas.getBoundingClientRect();
  const x = Math.floor(((ev.clientX - rect.left) / rect.width) * 32);
  const y = Math.floor(((ev.clientY - rect.top) / rect.height) * 32);
  if (x < 0 || y < 0 || x >= 32 || y >= 32) return;
  const v = state.tileDetail.heights[y * 32 + x];
  const c = state.status.calibration;
  $('tile-hover').textContent =
    `surowa wartość uint16 w próbce (x=${x}, y=${y}) = ${v}  |  ${(v / c.u16PerMeter).toFixed(2)} m (÷${c.u16PerMeter}, CURRENT_RUNTIME_CALIBRATION)`;
}

// ---- Panel 3: vegetation profile + seed + density + entry (ETAP E) ----
// The profile picker shows the REAL model IDs/scales read from the correctly
// decoded records (contract §6.1); the DEFAULT selection is the MEASURED
// choice from the server's support census (status.vegetation.defaultProfile —
// profile 0: DECODED, 12 non-empty records, contains the witness model 457485
// whose NIF the EXISTING qualified importer was cross-validated for) —
// NEVER a "historical biome" claim. 25.vcl stays visible + UNSUPPORTED with
// its reason (never comma-converted, never selectable).
function renderVegPanel() {
  const cl = state.climates;
  const sel = $('veg-profile');
  sel.innerHTML = '';
  if (!cl) {
    sel.innerHTML = '<option>błąd ładowania profili</option>';
    $('veg-profile-status').textContent = state.climatesError ?? '…';
    return;
  }
  for (const p of cl.profiles) {
    const o = document.createElement('option');
    o.value = String(p.index);
    const label = p.status === 'DECODED'
      ? `profil ${p.index} — ${p.recordCount} rekordów, ${p.models?.length ?? 0} modeli (zdekodowany)`
      : `profil ${p.index} — UNSUPPORTED (strict decoder; bez konwersji przecinków)`;
    o.textContent = label;
    if (p.status !== 'DECODED') o.disabled = true;
    sel.appendChild(o);
  }
  // DEFAULT = the MEASURED server choice (status.vegetation.defaultProfile),
  // fallback: the first DECODED profile. Never "the historical biome". The
  // selection is set ONLY on the first render (a later refresh keeps the
  // user's selection — the census landing just updates the status text).
  const svDefault = state.status?.vegetation?.defaultProfile?.index;
  const firstDecoded = cl.profiles.find((p) => p.status === 'DECODED');
  const chosen = sel.options.length > 0 && sel.value !== ''
    ? Number(sel.value)
    : (svDefault !== undefined && svDefault !== null ? svDefault : (firstDecoded?.index ?? 0));
  sel.value = String(chosen);
  const sv = state.status?.vegetation;
  const counts = sv?.supportCensus?.counts;
  $('veg-profile-status').textContent =
    `domyślnie: profil ${chosen} (WYBÓR POMIAROWY — NIE „historyczny biom”${sv?.defaultProfile ? `: ${sv.defaultProfile.measuredJustification}` : ''}) | ` +
    `zdekodowane: ${cl.decoded}/32, UNSUPPORTED: ${(cl.unsupported ?? []).join(', ') || 'brak'}${counts ? ` | census wsparcia (profil ${sv.defaultProfile.index}): modele ${counts.distinctModels} — wsparte z teksturami ${counts.supported}, geometryjnie bez tekstur ${counts.supportedUntextured}, UNSUPPORTED ${counts.unsupported}` : ''} | VEGETATION_MODE = RECONSTRUCTION_PREVIEW`;
  void loadVegModels(chosen);
  updateLaunchTarget();
}

/** Load + render the REAL model IDs/scales of the selected profile (the
 * per-record summaries served from the correctly decoded records; col
 * semantics labels follow the decoder header — col1 role PLAUSIBLE,
 * col4/col5 carried raw UNVERIFIED). UNSUPPORTED profiles show the honest
 * refusal reason — never converted records. */
async function loadVegModels(profileIdx) {
  const box = $('veg-models');
  try {
    const c = await fetchJson(`/api/world/climate/${profileIdx}`);
    if (c.status !== 'DECODED' || !Array.isArray(c.modelSummary)) {
      box.textContent = `profil ${profileIdx}: UNSUPPORTED (strict decoder) — ${c.error ?? 'rekordy niedostępne'} (zero instancji w /world; bez konwersji przecinków)`;
      return;
    }
    const lines = c.modelSummary.map((m) =>
      `  model ${m.id} · gęstość(col1) ${m.density} · skala ${m.scaleMin}..${m.scaleMax} (col2/col3, census-measured)`);
    box.textContent =
      [`profil ${profileIdx}: ${c.recordCount} rekordów 12-wartościowych (FUN_0083a7d0); modele+skale Z REKORDÓW (col4/col5 surowe — semantyka UNVERIFIED):`,
       ...lines].join('\n');
  } catch (e) {
    box.textContent = `profil ${profileIdx}: błąd pobierania (${e.message}) — uczciwie pokazany`;
  }
}

function readHashTarget() {
  const anchor = state.selection ? patchRect(state.selection) : null;
  if (!anchor) return null;
  const profile = $('veg-profile').value || '0';
  const seed = String(Math.max(0, Math.floor(Number($('veg-seed').value) || 0)));
  const density = String(Math.max(0, Math.min(100, Number($('veg-density').value) || 0)));
  return `/world#tile=${anchor.gx},${anchor.gy}&profile=${profile}&seed=${seed}&density=${density}`;
}

function updateLaunchTarget() {
  const t = readHashTarget();
  $('launch-target').textContent = t ? `cel: ${t}` : 'cel: wybierz kafel na mapie (domyślny wybór pojawi się po census)';
}

async function onLaunch() {
  let target = readHashTarget();
  if (!target) {
    // default anchor = the highest measured tile (data-derived; never a city-name guess)
    const mm = state.status?.census?.maxMeanTile;
    const anchor = mm ? { gx: mm.gridX, gy: mm.gridY } : { gx: 108, gy: 116 };
    state.selection = anchor;
    renderSelectionBox();
    target = readHashTarget();
  }
  hud(`przejście do widoku świata: ${target}`);
  location.href = target;
}

// ---- Panel 4: catalog link + gaps ----
function renderGapsPanel() {
  const g = state.gaps;
  if (!g) { $('gaps-list').textContent = 'panel braków: błąd ładowania (uczciwie pokazany)'; return; }
  $('catalog-link').href = g.catalog.url;
  $('catalog-note').textContent = ` (${g.catalog.note})`;
  const wrap = $('gaps-list');
  wrap.innerHTML = '';
  for (const gap of g.gaps) {
    const div = document.createElement('div');
    div.className = 'gap-row';
    div.innerHTML = `<b>${gap.label}</b> — <span class="gap-state">${gap.state}</span><br>${gap.detail}`;
    wrap.appendChild(div);
  }
}

// ---- Panel 5: evidence panel ----
function renderEvidence() {
  const s = state.status;
  const fixed = [
    '=== DANE TECHNICZNE (panel dowodów — poza głównym flow) ===',
    `era: ${s.era} (era CD w warstwie źródeł = CD_JAN_2003 — jawne mapowanie, nigdy JUL_2003)`,
    `terrain.bnt: ${s.containers.terrain.path} — SHA256 ${s.containers.terrain.sha256} (pin: ${s.containers.terrain.pin}, ${s.containers.terrain.state})`,
    `VegetationClimates.bnt: ${s.containers.vegetationClimates.path} — SHA256 ${s.containers.vegetationClimates.sha256}`,
    `Models.bnt: ${s.containers.models.path} — SHA256 ${s.containers.models.sha256 ?? 'weryfikacja w toku'} (pin: ${s.containers.models.pin}; ${s.containers.models.state})`,
    `Textures.bnt: ${s.containers.textures.path} — SHA256 ${s.containers.textures.sha256 ?? 'weryfikacja w toku'} (pin: ${s.containers.textures.pin}; ${s.containers.textures.state})`,
    '',
    'TDF (kafel terenu): 32×32 uint16 LE; wysokości = payload offset 64..2111 (2048 B = 1024 próbki);',
    '  bajty 52..63 = ODRĘBNY subheader (NIE wysokości — odczyt od 52 to znany błędny wariant);',
    '  TAIL od 2112 = materiały (Etap D); indeks BNT2: nazwa = współrzędne siatki (filename-xy).',
    `indeks terrain.bnt: ${s.terrainIndex.totalEntries} wpisów = ${s.terrainIndex.regular} zwykłych (220×236) + ${s.terrainIndex.specialRows} wierszy specjalnych (gridY 0xff5a..0xffff, semantyka UNRESOLVED — wykluczone głośnie) + ${s.terrainIndex.sentinel} sentinel (7ffe7ffe.tdf — NIE zwykły kafel)`,
    '',
    `kalibracja (CURRENT_RUNTIME_CALIBRATION — preset runtime z provenance, NIE fakt historyczny):`,
    `  u16PerMeter=${s.calibration.u16PerMeter}; meterPerSample=${s.calibration.meterPerSample}; min/max=${s.calibration.minMax}`,
    `  odwracalność: ${s.calibration.reversibility}`,
    '',
    `overview API: ${JSON.stringify(s.overviewLayout)}`,
    `cache tożsamości (CAM-C3 dla każdej paczki cache): era+kontener+SHA kontenera+nazwa wpisu+SHA payloadu+wersja dekodera; mismatch = kontrolowana odmowa + regeneracja z oryginalnych bajtów; odmowy: ${JSON.stringify(s.tileCache.lastRefusalReasons)}`,
    `statystyka cache kafla: ${JSON.stringify(s.tileCache)}`,
  ];
  $('evidence-content').textContent = fixed.join('\n') + '\n\n=== /api/world/status (pełny snapshot) ===\n' + JSON.stringify(s, null, 1);
}

// ---- async overview refresh with progress ----
async function refreshOverviewLoop() {
  if (state.loopTimer) { clearTimeout(state.loopTimer); state.loopTimer = null; }
  try {
    const p = await fetchJson('/api/world/overview/progress');
    const s = state.status;
    s.census.measured = p.measured; s.census.missing = p.missing;
    s.census.failed = p.failed; s.census.pending = p.pending; s.census.ready = p.ready;
    renderStages();
    const measuredNow = p.measured + p.missing + p.failed;
    if (state.overviewVersion !== measuredNow) {
      state.overviewVersion = measuredNow;
      const r = await fetch('/api/world/overview', { cache: 'no-store' });
      if (!r.ok) throw new Error(`overview HTTP ${r.status}`);
      const buf = new Uint8Array(await r.arrayBuffer());
      if (buf.length !== TILE_N * 7) throw new Error(`overview bytes ${buf.length} != ${TILE_N * 7}`);
      const dv = new DataView(buf.buffer);
      const mean = new Uint16Array(TILE_N), min = new Uint16Array(TILE_N), max = new Uint16Array(TILE_N), status = new Uint8Array(TILE_N);
      for (let i = 0; i < TILE_N; i++) {
        mean[i] = dv.getUint16(i * 7, true);
        min[i] = dv.getUint16(i * 7 + 2, true);
        max[i] = dv.getUint16(i * 7 + 4, true);
        status[i] = buf[i * 7 + 6];
      }
      state.overview = { mean, min, max, status };
      renderMap();
      // default selection = the highest measured tile (data-derived spawn; no city-name guessing)
      if (!state.selection && s.census.ready && s.census.maxMeanTile) {
        state.selection = { gx: s.census.maxMeanTile.gridX, gy: s.census.maxMeanTile.gridY };
        renderSelectionBox();
        hud(`domyślny wybór (pomiarowy): kafel ${tileName(state.selection.gx, state.selection.gy)} — najwyższa zmierzona średnia; kliknij dowolny kafel, aby zmienić`);
      }
    }
    if (!p.ready) {
      state.loopTimer = setTimeout(refreshOverviewLoop, 450);
    } else {
      const st = await fetchJson('/api/world/status');
      state.status = st;
      renderDataPanel();
      renderEvidence();
      setOverviewStatus('READY');
      $('map-refresh-state').textContent = `przegląd: pełny (census GOTOWE w ${st.census.elapsedMs} ms)`;
      // ETAP E: the measured default-profile support census runs in the
      // background (after BOTH lazy indexes are READY) — refresh the veg
      // panel once it lands so the MEASURED justification + per-model support
      // counts are shown (the selection itself is NOT changed under the user)
      if (st.vegetation?.supportCensusState === 'READY' && !state.vegCensusShown) {
        state.vegCensusShown = true;
        renderVegPanel();
      }
    }
  } catch (e) {
    setOverviewStatus('ERROR');
    banner(`odświeżanie przeglądu: ${e.message}`);
    $('map-refresh-state').textContent = `błąd odświeżania: ${e.message}`;
    state.loopTimer = setTimeout(refreshOverviewLoop, 2500);
  }
}

// ---- boot ----
async function boot() {
  setLoadStatus('LOADING');
  hud('łączę z serwerem świata (era PCG_9_3_5)…');
  try {
    state.status = await fetchJson('/api/world/status');
  } catch (e) {
    setLoadStatus(`ERROR_STATUS_FETCH: ${e.message}`);
    banner(`KRYTYCZNY BŁĄD: ${e.message}`);
    hud('błąd połączenia z serwerem świata');
    return;
  }
  renderDataPanel();
  renderEvidence();
  try {
    state.climates = await fetchJson('/api/world/climates');
  } catch (e) {
    state.climatesError = String(e.message);
    banner(`profile klimatu: ${e.message}`);
  }
  renderVegPanel();
  try {
    state.gaps = await fetchJson('/api/world/gaps');
  } catch (e) {
    banner(`panel braków: ${e.message}`);
  }
  renderGapsPanel();
  setLoadStatus('READY');
  hud(`połączono: era ${state.status.era} — census wysokości w toku (asynchronicznie, z postępem)`);
  void refreshOverviewLoop();

  $('view-canvas').addEventListener('mousemove', onMapHover);
  $('view-canvas').addEventListener('click', onMapClick);
  $('tile-canvas').addEventListener('mousemove', onTileCanvasHover);
  $('btn-refresh-overview').addEventListener('click', () => {
    setOverviewStatus('REFRESHING');
    hud('ręczne odświeżenie przeglądu (async)…');
    void refreshOverviewLoop();
  });
  $('veg-profile').addEventListener('change', () => {
    const p = state.climates?.profiles?.find((x) => String(x.index) === $('veg-profile').value);
    $('veg-profile-status').textContent = p
      ? `profil ${p.index}: ${p.status}${p.status === 'DECODED' ? `, ${p.recordCount} rekordów` : ` — ${p.error ?? 'strict decoder'}`}`
      : '…';
    void loadVegModels(Number($('veg-profile').value));
    updateLaunchTarget();
  });
  $('veg-seed').addEventListener('input', updateLaunchTarget);
  $('veg-density').addEventListener('input', () => {
    $('veg-density-value').textContent = `${$('veg-density').value}%`;
    updateLaunchTarget();
  });
  $('btn-launch').addEventListener('click', onLaunch);
  window.addEventListener('resize', renderSelectionBox);
}

boot().catch((e) => {
  setLoadStatus(`ERROR_BOOT: ${e.message}`);
  banner(`KRYTYCZNY BŁĄD BOOT: ${e.message}`);
});
