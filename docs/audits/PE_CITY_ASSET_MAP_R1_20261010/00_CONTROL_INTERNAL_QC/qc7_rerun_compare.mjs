// QC7 — rerun summary comparison (UTF-16 redirect artifact handled) + published-values check.
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve, join } from 'node:path';

const PKG = resolve(process.argv[2]);
const rerunPath = join(PKG, '00_CONTROL_INTERNAL_QC/raw/PHASE3_RERUN/RERUN_SUMMARY.json');
let text = readFileSync(rerunPath, 'utf16le');
// strip possible BOM chars after utf16le decode
text = text.replace(/^\uFEFF/, '').replace(/^\uFFFD/, '');
const j = JSON.parse(text);
const expected = {
  '192374.nif': { blocks: 22, tri: 1200, vert: 2400, shapes: 4, nodes: 5, maxAxis: 32789.15, placement: 'VERTICES', texEdges: 0, names: ['Box01', 'MSC', 'MAC', 'signs'] },
  '193207.nif': { blocks: 14, tri: 864, vert: 1698, shapes: 2, nodes: 3, maxAxis: 26940.91, placement: 'VERTICES', texEdges: 0, names: ['Box06', 'Object01'] },
  '193313.nif': { blocks: 26, tri: 1192, vert: 2384, shapes: 5, nodes: 6, maxAxis: 31765.85, placement: 'VERTICES', texEdges: 0, names: ['Outpost39_proxymesh', 'MSC', 'signs', 'build', 'MAC'] },
  '193684.nif': { blocks: 38, tri: 1340, vert: 2680, shapes: 8, nodes: 9, maxAxis: 33739.21, placement: 'VERTICES', texEdges: 0, names: ['signs', 'mlti', 'wall', 'signs01', 'mac', 'build', 'cont', 'forts'] },
};
const out = { qcStep: 'QC7_RERUN_COMPARISON', rows: [] };
for (const r of j.rows) {
  const e = expected[r.model];
  const blockTotal = Object.values(r.blockCensus).reduce((a, b) => a + b, 0);
  const namesPresent = r.roots ? true : false;
  const row = {
    model: r.model, status: r.status,
    blocks_measured: blockTotal, blocks_claimed: e.blocks, blocks_ok: blockTotal === e.blocks,
    triangles: r.complexity.triangles, triangles_claimed: e.tri, tri_ok: r.complexity.triangles === e.tri,
    vertices: r.complexity.vertices, vertices_claimed: e.vert, vert_ok: r.complexity.vertices === e.vert,
    shapes: r.complexity.shapes, shapes_claimed: e.shapes, shapes_ok: r.complexity.shapes === e.shapes,
    nodes: r.complexity.nodes, nodes_claimed: e.nodes, nodes_ok: r.complexity.nodes === e.nodes,
    maxAxisExtent: r.bounds.maxAxisExtent, maxAxis_claimed: e.maxAxis,
    maxAxis_ok: Math.abs(r.bounds.maxAxisExtent - e.maxAxis) < 0.005,
    extents: r.bounds.extents, min: r.bounds.min, max: r.bounds.max,
    placementFinding: r.placementFinding, placement_ok: r.placementFinding === e.placement,
    textureEdgeCount: r.textureEdgeCount, texEdges_ok: r.textureEdgeCount === e.texEdges,
    standardChain: r.standardChainPresent,
    roots: r.roots, namesPresent
  };
  out.rows.push(row);
}
// full dump of hierarchy names from the rerun (compare against DEEP_ANALYSIS names)
const dumps = {};
for (const m of ['192374', '193207', '193313', '193684']) {
  const d = JSON.parse(readFileSync(join(PKG, `00_CONTROL_INTERNAL_QC/raw/PHASE3_RERUN/${m}_blocks.json`), 'utf8'));
  dumps[m] = { roots: d.roots, hierarchyNames: d.hierarchyRows.map(h => ({ block: h.block, name: h.name, type: h.type })), trsCoverage: d.trsCoverage, validation: d.validation, textureEdges: d.textureEdges.length, standardChainPresent: d.standardChainPresent, connectedComponents: d.connectedComponents.total };
}
out.dumps = dumps;
writeFileSync(join(PKG, '00_CONTROL_INTERNAL_QC/QC7_RERUN_COMPARISON.json'), JSON.stringify(out, null, 1));
for (const row of out.rows) {
  console.log(`${row.model}: blocks ${row.blocks_ok} tri ${row.tri_ok} vert ${row.vert_ok} shapes ${row.shapes_ok} nodes ${row.nodes_ok} maxAxis ${row.maxAxis_ok} (${row.maxAxisExtent}) placement ${row.placement_ok} texEdges ${row.texEdges_ok}`);
}
for (const [m, d] of Object.entries(dumps)) {
  const names = d.hierarchyNames.map(h => h.name).filter(Boolean);
  const exp = expected[m + '.nif'].names;
  const namesOk = exp.every(n => names.includes(n));
  console.log(`${m}: names_ok=${namesOk} validation=${JSON.stringify(d.validation)} cc_total=${d.connectedComponents} trs=${JSON.stringify(d.trsCoverage)}`);
}
