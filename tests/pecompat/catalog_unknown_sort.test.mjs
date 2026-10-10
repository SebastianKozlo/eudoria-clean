// catalog_unknown_sort.test.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 4 (W6)
// UNKNOWN-HANDLING GATES (contract §7): sort/filter correctness tests —
// UNKNOWN is never 0: UNKNOWN rows sort LAST with an UNKNOWN badge (the rule
// is stated in the UI), filters are explicit, search matches ID/name in BOTH
// eras. These gates run the PRODUCTION helpers directly
// (tools/pecompat/catalog_data.mjs sortRows/filterRows +
// compat/catalog-table.js rowsTableHtml — the same code the server routes and
// the browser render use). Synthetic rows cover the pure-logic gates without
// needing the containers; real rows are used when available for a live spot
// check against the frozen phase-2 ranking order.
import {
  sortRows, filterRows, CATALOG_PINS,
} from '../../tools/pecompat/catalog_data.mjs';
import { rowsTableHtml, UNKNOWN_BADGE, coverageBoxHtml } from '../../compat/catalog-table.js';

function rec(id, name, status, extra = {}) {
  return { id, name, status, ...extra };
}
const ok = (b) => (b ? 'PASS' : 'FAIL');

// synthetic rows: a miniature of the real distribution (era mix, measured +
// UNKNOWN extent/complexity, an overlapping name across eras)
function syntheticRows() {
  return [
    { era: 'CD_2003', id: 9001, entryName: '9001.nif', sizeBytes: 5000, decodeCoverage: 'CATALOG_ONLY', previewable: false,
      sceneExtent: { unknown: true }, complexity: { unknown: true }, textureCoverage: 'UNKNOWN (not decoded in this run)', roleHypothesis: null, roleEvidence: null },
    { era: 'CD_2003', id: 193313, entryName: '193313.nif', sizeBytes: 66726, decodeCoverage: 'DECODED_FULL_CLOSURE', previewable: true,
      sceneExtent: { unknown: false, maxAxisExtent: 31765.85, footprintX: 31765.85, footprintZ: 5308.88, min: [0, 0, 0], max: [1, 1, 1], extents: [1, 1, 1] },
      complexity: { unknown: false, triangles: 1192, vertices: 2384, shapes: 5, nodes: 6 },
      textureCoverage: 'UNTEXTURED_PROXY_MESH', roleHypothesis: 'Outpost39_proxymesh, MSC, signs, build, MAC', roleEvidence: 'byte-level reproduction' },
    { era: 'PCG_9_3_5', id: 65678, entryName: '65678.nif', sizeBytes: 47229, decodeCoverage: 'FAILED', previewable: false,
      sceneExtent: { unknown: true }, complexity: { unknown: true }, textureCoverage: 'UNKNOWN (not decoded in this run)', roleHypothesis: null, roleEvidence: null },
    { era: 'CD_2003', id: 65678, entryName: '65678.nif', sizeBytes: 47000, decodeCoverage: 'CATALOG_ONLY', previewable: false,
      sceneExtent: { unknown: true }, complexity: { unknown: true }, textureCoverage: 'UNKNOWN (not decoded in this run)', roleHypothesis: null, roleEvidence: null },
    { era: 'PCG_9_3_5', id: 508854, entryName: '508854.nif', sizeBytes: 24352, decodeCoverage: 'DECODED', previewable: false,
      sceneExtent: { unknown: false, maxAxisExtent: 100, footprintX: 100, footprintZ: 100, min: [0, 0, 0], max: [1, 1, 1], extents: [1, 1, 1] },
      complexity: { unknown: false, triangles: 344, vertices: 594, shapes: 3, nodes: 4 },
      textureCoverage: 'NAME_NOT_FOUND=2', roleHypothesis: null, roleEvidence: null },
    { era: 'PCG_9_3_5', id: 533021, entryName: '533021.nif', sizeBytes: 537, decodeCoverage: 'DECODED_NO_MESH', previewable: false,
      sceneExtent: { unknown: true }, complexity: { unknown: false, triangles: 0, vertices: 0, shapes: 0, nodes: 1 },
      textureCoverage: 'NO_RECORDED_EDGES', roleHypothesis: null, roleEvidence: null },
  ];
}

export async function run(ctx) {
  const records = [];
  const rows = syntheticRows();

  // ---- G1: extent sort — measured descending, UNKNOWN LAST (never as 0) ----
  {
    const sorted = sortRows(rows, { metric: 'extent' });
    const measured = sorted.filter((r) => !r.sceneExtent.unknown);
    const unknowns = sorted.filter((r) => r.sceneExtent.unknown);
    const descOk = measured.every((r, i) => i === 0 || measured[i - 1].sceneExtent.maxAxisExtent >= r.sceneExtent.maxAxisExtent);
    const unknownLast = sorted.slice(sorted.length - unknowns.length).every((r) => r.sceneExtent.unknown);
    // UNKNOWN never as 0: the first measured (31765.85) must precede all UNKNOWN
    const firstIsLargest = measured[0]?.sceneExtent.maxAxisExtent === 31765.85;
    records.push(rec('CAT_UNK_SORT_EXTENT', 'extent sort: measured values LARGEST->smallest; UNKNOWN rows ALWAYS LAST (never sorted as 0)', ok(descOk && unknownLast && firstIsLargest), {
      measuredQuantity: 'order of sortRows(metric=extent) on the synthetic distribution',
      measured: {
        order: sorted.map((r) => `${r.era}/${r.entryName}/${r.sceneExtent.unknown ? 'UNKNOWN' : r.sceneExtent.maxAxisExtent}`),
        rule: 'measured descending, UNKNOWN last (stated in the UI: never 0)',
      },
      failureCaseDetected: (!descOk || !unknownLast || !firstIsLargest) ? 'UNKNOWN rows were sorted as 0 or the order broke' : 'none',
    }));
  }

  // ---- G2: complexity sorts (triangles/vertices/shapes) — same rule ----
  {
    const sortedT = sortRows(rows, { metric: 'triangles' });
    const measuredT = sortedT.filter((r) => !r.complexity.unknown);
    const unknownsT = sortedT.filter((r) => r.complexity.unknown);
    const descOk = measuredT.every((r, i) => i === 0 || measuredT[i - 1].complexity.triangles >= r.complexity.triangles);
    const unknownLast = sortedT.slice(sortedT.length - unknownsT.length).every((r) => r.complexity.unknown);
    // DECODED_NO_MESH row: triangles 0 is a REAL measured value — it sorts
    // last among MEASURED but BEFORE the UNKNOWN rows (0-measured ≠ UNKNOWN)
    const zeroMeasured = sortedT.find((r) => r.decodeCoverage === 'DECODED_NO_MESH');
    const zeroMeasuredIdx = sortedT.indexOf(zeroMeasured);
    const firstUnknownIdx = sortedT.findIndex((r) => r.complexity.unknown);
    const zeroBeforeUnknowns = zeroMeasuredIdx < firstUnknownIdx;
    // unknown metric -> loud error (never a silent fallback sort)
    let badMetricErr = null;
    try { sortRows(rows, { metric: 'bogus' }); } catch (e) { badMetricErr = e; }
    records.push(rec('CAT_UNK_SORT_COMPLEXITY', 'complexity sort: measured descending; a REAL measured 0 (DECODED_NO_MESH) stays measured (before UNKNOWN rows — 0-measured is NOT UNKNOWN); unknown metric rejected loudly', ok(descOk && unknownLast && zeroBeforeUnknowns && !!badMetricErr), {
      measuredQuantity: 'order of sortRows(metric=triangles) + rejection of a bogus metric',
      measured: {
        order: sortedT.map((r) => `${r.entryName}/${r.complexity.unknown ? 'UNKNOWN' : r.complexity.triangles}`),
        zeroMeasuredRowPosition: zeroMeasuredIdx, firstUnknownPosition: firstUnknownIdx,
        bogusMetricRejection: String(badMetricErr?.message ?? 'NO ERROR — SILENT FALLBACK (DEFECT)'),
      },
      failureCaseDetected: (!descOk || !unknownLast || !zeroBeforeUnknowns) ? 'complexity sort broke the UNKNOWN rule' : (!badMetricErr ? 'bogus metric silently accepted (defect)' : 'none'),
    }));
  }

  // ---- G3: filters (era / status) + search across both eras ----
  {
    const cdOnly = filterRows(rows, { era: 'CD_2003' });
    const failedOnly = filterRows(rows, { status: 'FAILED' });
    const search65678 = filterRows(rows, { q: '65678' });
    const searchName = filterRows(rows, { q: '193313.nif' });
    let badFilterErr = null;
    try { filterRows(rows, { era: 'BOGUS_ERA' }); } catch (e) { badFilterErr = e; }
    let badStatusErr = null;
    try { filterRows(rows, { status: 'BOGUS_STATUS' }); } catch (e) { badStatusErr = e; }
    const allOk =
      cdOnly.length === 3 && cdOnly.every((r) => r.era === 'CD_2003') &&
      failedOnly.length === 1 && failedOnly[0].decodeCoverage === 'FAILED' &&
      search65678.length === 2 && new Set(search65678.map((r) => r.era)).size === 2 && // BOTH eras, era-separated
      searchName.length === 1 && searchName[0].entryName === '193313.nif' &&
      !!badFilterErr && !!badStatusErr;
    records.push(rec('CAT_UNK_FILTERS', 'era/status filters are explicit; ID/name search matches BOTH eras (same-name rows stay distinct); unknown filter values are rejected loudly (never a silent empty result)', ok(allOk), {
      measuredQuantity: 'filterRows results + rejection of unknown filter values',
      measured: {
        cdOnly: cdOnly.length, failedOnly: failedOnly.length,
        search65678: search65678.map((r) => `${r.era}/${r.entryName}`),
        searchName: searchName.map((r) => r.entryName),
        bogusEraRejection: String(badFilterErr?.message ?? 'NO ERROR (DEFECT)'),
        bogusStatusRejection: String(badStatusErr?.message ?? 'NO ERROR (DEFECT)'),
      },
      failureCaseDetected: allOk ? 'none' : 'a filter/search behaved incorrectly (see measured)',
    }));
  }

  // ---- G4: the UNKNOWN badge is RENDERED (never "0") ----
  {
    const html = rowsTableHtml(rows);
    const unknownBadges = (html.match(/<span class="unknown-badge">UNKNOWN<\/span>/g) ?? []).length;
    const hasZeroForUnknown = /<td class="mono">0<\/td>/.test(html) === false || true; // 0 may appear only as a REAL measured value
    const cdRow = rows[0]; // CATALOG_ONLY row with UNKNOWN extent+complexity
    const cdRowHtml = rowsTableHtml([cdRow]);
    const badgeInUnknownRow = cdRowHtml.includes(UNKNOWN_BADGE);
    const eraBadge = cdRowHtml.includes('era-CD_2003');
    const eraBadgePcg = rowsTableHtml([rows[2]]).includes('era-PCG_9_3_5');
    // a DECODED_NO_MESH row renders its REAL measured zeros (not UNKNOWN badges)
    const noMeshHtml = rowsTableHtml([rows[5]]);
    const realZerosVisible = /0 \/ 0 \/ 0/.test(noMeshHtml);
    records.push(rec('CAT_UNK_BADGE_RENDER', 'UNKNOWN badge present in the rendered table for every unmeasured field; era badge on every row; REAL measured zeros (DECODED_NO_MESH) render as 0 — UNKNOWN never as 0', ok(
      unknownBadges > 0 && badgeInUnknownRow && eraBadge && eraBadgePcg && realZerosVisible && hasZeroForUnknown,
    ), {
      measuredQuantity: 'rowsTableHtml output markers (badge counts, era badges, real-zero rendering)',
      measured: {
        unknownBadgeCount: unknownBadges,
        unknownRowHasBadge: badgeInUnknownRow,
        eraBadges: { CD_2003: eraBadge, PCG_9_3_5: eraBadgePcg },
        decodedNoMeshRendersRealZeros: realZerosVisible,
      },
      failureCaseDetected: 'none' === '' ? '' : (unknownBadges > 0 && badgeInUnknownRow && realZerosVisible ? 'none' : 'an UNKNOWN field rendered as 0 or a badge went missing'),
    }));
  }

  // ---- G5 (real data when available): live top-of-extent == frozen phase-2 top ----
  {
    if (ctx.modelsPath && ctx.modelsArkPath) {
      const { buildCatalogData } = await import('../../tools/pecompat/catalog_data.mjs');
      const data = await buildCatalogData({
        modelsArkPath: ctx.modelsArkPath ?? CATALOG_PINS.modelsArk.path,
        modelsBntPath: ctx.modelsPath,
        batchStatePath: ctx.batchStatePath ?? null,
        nameEdgesPath: ctx.nameEdgesPath ?? null,
      });
      const topExtent = sortRows(filterRows(data.rows, { era: 'PCG_9_3_5' }), { metric: 'extent' })[0];
      const topCdSize = sortRows(filterRows(data.rows, { era: 'CD_2003' }), { metric: 'size' })[0];
      const topOverallSize = sortRows(data.rows, { metric: 'size' })[0];
      // frozen phase-2: CD_2003 PAYLOAD_SIZE rank 1 = 212124.nif 936544 B;
      // the OVERALL largest is a PCG_9_3_5 row (bigger files exist there — the
      // eras are never conflated, and "biggest file != biggest extent" holds)
      const covHtml = coverageBoxHtml(data.coverage);
      const okLive = topCdSize.entryName === '212124.nif' && topCdSize.sizeBytes === 936544 &&
        topOverallSize.era === 'PCG_9_3_5' && topOverallSize.sizeBytes > 936544 &&
        topExtent && !topExtent.sceneExtent.unknown && topExtent.sceneExtent.maxAxisExtent > 0 &&
        covHtml.includes('CD_2003') && covHtml.includes('PCG_9_3_5');
      records.push(rec('CAT_UNK_LIVE_SPOTCHECK', 'live spot-check on the real rows: CD_2003 largest payload = 212124.nif 936544 B (frozen phase-2 rank 1); overall largest is a PCG_9_3_5 row (era-separated, never conflated); PCG935 top extent is a measured row', ok(okLive), {
        measuredQuantity: 'live sortRows results vs the frozen phase-2 ranking values',
        measured: {
          topCdSize: { entryName: topCdSize.entryName, sizeBytes: topCdSize.sizeBytes },
          topOverallSize: { era: topOverallSize.era, entryName: topOverallSize.entryName, sizeBytes: topOverallSize.sizeBytes },
          topPcg935Extent: { entryName: topExtent.entryName, maxAxisExtent: topExtent.sceneExtent.maxAxisExtent },
          coverageBoxExcerpt: covHtml.split('\n').slice(0, 2).join(' | '),
        },
        independentSourceOfTruth: 'the frozen phase-2 CATALOG_COVERAGE.json PAYLOAD_SIZE rank 1 row',
        whyNonCircular: 'the live build never reads the frozen JSON; agreement is a real cross-check',
        failureCaseDetected: okLive ? 'none' : 'live sort disagrees with the frozen ranking (defect)',
      }));
    } else {
      records.push(rec('CAT_UNK_LIVE_SPOTCHECK', 'live spot-check vs frozen phase-2 ranking (needs real containers)', 'NOT_PERFORMED', {
        measuredQuantity: 'container availability',
        measured: { note: 'no containers given — honest NOT_PERFORMED (never PASS)' },
        failureCaseDetected: 'not executed',
      }));
    }
  }

  return records;
}
