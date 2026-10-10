// catalog-table.js — PE_CITY_ASSET_MAP_R1_20261010, phase 4 (contract §5)
// PURE catalog table rendering — no THREE, no DOM, no fetch (Node-testable:
// the UNKNOWN-handling gates import these exports directly).
// REUSE LABEL: the honesty conventions follow the SceneIR app's pure-mode
// export pattern (compat/asset-mode.js): browser rendering and Node tests
// share ONE implementation.
//
// UNKNOWN DISCIPLINE: an unmeasured field renders as an UNKNOWN badge —
// NEVER as 0 and never invented. Era badge on every row.

export const UNKNOWN_BADGE = 'UNKNOWN';

export function escapeHtml(s) {
  return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

export function fmtBytes(n) {
  return n == null ? UNKNOWN_BADGE : n.toLocaleString('en-US');
}

export function extentCell(row) {
  if (!row.sceneExtent || row.sceneExtent.unknown) return `<span class="unknown-badge">${UNKNOWN_BADGE}</span>`;
  const e = row.sceneExtent;
  const f = (v) => v.toLocaleString('en-US', { maximumFractionDigits: 2 });
  return `${f(e.maxAxisExtent)} <span class="wire-note">(fpX ${f(e.footprintX)}, fpZ ${f(e.footprintZ)})</span>`;
}

export function complexityCell(row) {
  if (!row.complexity || row.complexity.unknown) return `<span class="unknown-badge">${UNKNOWN_BADGE}</span>`;
  const c = row.complexity;
  const num = (v) => (v == null ? `<span class="unknown-badge">${UNKNOWN_BADGE}</span>` : v.toLocaleString('en-US'));
  return `${num(c.triangles)} / ${num(c.vertices)} / ${num(c.shapes)}`;
}

/** The catalog table body rows as HTML (one <tr> per row). PURE.
 * Columns: era | ID/entry | file size | scene extent | geometry tri/vert/shapes |
 * decode coverage | texture coverage | role hypothesis + evidence. */
export function rowsTableHtml(rows, { selectedId = null } = {}) {
  const trs = [];
  for (const row of rows) {
    const isSelected = selectedId != null && row.id === selectedId && row.previewable;
    const cls = [isSelected ? 'row-selected' : '', row.previewable ? 'clickable' : ''].filter(Boolean).join(' ');
    const hypothesis = row.roleHypothesis
      ? `<div class="wire-note">${escapeHtml(row.roleHypothesis)}</div><div class="wire-note">${escapeHtml(row.roleEvidence ?? '')}</div>`
      : '<span class="wire-note">- (no hypothesis recorded; node names are labels only, never classes)</span>';
    trs.push(
      `<tr data-era="${row.era}" data-id="${row.id ?? ''}" data-entry="${escapeHtml(row.entryName)}"${cls ? ` class="${cls}"` : ''}>` +
      `<td><span class="era-badge era-${row.era}">${row.era}</span></td>` +
      `<td class="mono">${row.id ?? UNKNOWN_BADGE}<br><span class="wire-note">${escapeHtml(row.entryName)}</span>${row.previewable ? '<br><span class="previewable-flag">PREVIEWABLE</span>' : ''}</td>` +
      `<td class="mono">${fmtBytes(row.sizeBytes)}</td>` +
      `<td class="mono">${extentCell(row)}</td>` +
      `<td class="mono">${complexityCell(row)}</td>` +
      `<td><span class="status-${row.decodeCoverage}">${row.decodeCoverage}</span><br><span class="wire-note">${escapeHtml(row.decodeReason ?? '')}</span></td>` +
      `<td class="wide">${escapeHtml(row.textureCoverage)}</td>` +
      `<td class="wide">${hypothesis}</td>` +
      '</tr>');
  }
  return trs.join('\n');
}

/** The coverage box HTML (per-era counts, decode distribution, measured lines).
 * PURE — the UI renders this verbatim. */
export function coverageBoxHtml(coverage, { overlapCount = null } = {}) {
  if (!coverage) return 'coverage: (unavailable)';
  const byDecode = Object.entries(coverage.byDecodeCoverage ?? {})
    .map(([k, v]) => `${k}=${v}`).join(' | ');
  return [
    `rows TOTAL ${coverage.totalRows} = CD_2003 ${coverage.byEra.CD_2003} + PCG_9_3_5 ${coverage.byEra.PCG_9_3_5}`,
    `decode coverage: ${byDecode}`,
    `scene extent: MEASURED ${coverage.sceneExtent.measured} / UNKNOWN ${coverage.sceneExtent.unknown} — ${coverage.sceneExtent.coverageLine}`,
    `same entry name in BOTH eras: LEGAL and era-separated${overlapCount != null ? ` (${overlapCount} names measured — two distinct assets by identity key)` : ''}`,
    'all tables LARGEST-MEASURED (coverage incomplete) — never "largest of all"',
  ].join('\n');
}
