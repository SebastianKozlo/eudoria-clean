// texture_chain.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 4 (W4/W6, contract §4+§7)
// THE era-scoped texture-name resolution + disposition logic of this run.
//
// DISPOSITION CLASSES (PREREGISTRATION §3, strictly increasing provenance):
//   NAME_FOUND -> REFERENCE_CONFIRMED -> CONTAINER_ENTRY_RESOLVED ->
//   IMAGE_DECODED -> MATERIAL_APPLIED -> BROWSER_OBSERVED.
// This module covers the NAME->CONTAINER stage only, ERA-SCOPED:
//   resolveNameInEra(name, catalog) resolves a texture name against ONE era's
//   container entry index. It can NEVER return an entry of another era (the
//   catalog is passed in era-scoped); a cross-era attempt is a CONTROLLED
//   refusal (WRONG_ERA_REFUSED), never a silent pass and never a resolution.
//
// HARD NEGATIVES enforced here (contract §4):
//   - no attribution by adjacent ID, color, similar name, or the other era's
//     version (exact-name matching only);
//   - a header sniff is NOT an image decode: IMAGE_DECODED is only produced
//     by a real pixel decode (nowhere in this run for these chains) — a
//     found entry gets imageDisposition IMAGE_SNIFFED_* or IMAGE_NOT_DECODED;
//   - a missing name is NAME_NOT_FOUND (explicit, never a fake PASS).
//
// REUSE LABEL: the sniff classification is tools/pecompat/catalog_sniff.mjs
// sniffPayload (phase-2, imported UNCHANGED — heuristic header classification,
// never presented as a decode).

'use strict';
import { sniffPayload } from './catalog_sniff.mjs';

export const TEXTURE_CHAIN_VERSION = 'pec-texture-chain-v1-phase4';

/** Build an era-scoped resolver over one container's entry index.
 * catalog = { era, container, entries: [{entryIndex, name, size, offset, crc32, ...}] }.
 * The resolver is era-bound BY CONSTRUCTION: it only ever sees the entries
 * passed to it. */
export function makeEraCatalog(catalog) {
  if (!catalog || !catalog.era || !Array.isArray(catalog.entries)) {
    throw new Error('[texture_chain] makeEraCatalog requires {era, entries[]}');
  }
  const byName = new Map();
  for (const e of catalog.entries) {
    if (!byName.has(e.name)) byName.set(e.name, e); // first entry per exact name (duplicates counted below)
    else byName.get(e.name).duplicateNameCount = (byName.get(e.name).duplicateNameCount ?? 1) + 1;
  }
  return {
    era: catalog.era,
    container: catalog.container ?? null,
    entryCount: catalog.entries.length,
    byName,
    hasExact(name) { return byName.has(name); },
    entry(name) { return byName.get(name) ?? null; },
  };
}

/** Resolve ONE texture name in ONE era's catalog. Controlled outcomes only.
 * @returns {{disposition, era, container, entry, note}} — disposition:
 *   NAME_FOUND_EXACT   — the name resolves to a same-era container entry
 *   NAME_NOT_FOUND     — no exact entry in this era (explicit, never a pass)
 * The wrong-era case is handled by the CALLER passing the correct era catalog;
 * resolveCrossEra() below records the controlled WRONG_ERA_REFUSED attempt. */
export function resolveNameInEra(name, eraCatalog) {
  const entry = eraCatalog.entry(name);
  if (!entry) {
    return {
      disposition: 'NAME_NOT_FOUND',
      era: eraCatalog.era,
      container: eraCatalog.container,
      entry: null,
      note: `no exact entry "${name}" in the ${eraCatalog.era} ${eraCatalog.container ?? 'container'} index (exact-name matching only; NOT resolved by similar name, adjacent ID, color, or the other era's version)`,
    };
  }
  return {
    disposition: 'NAME_FOUND_EXACT',
    era: eraCatalog.era,
    container: eraCatalog.container,
    entry: { entryIndex: entry.entryIndex, name: entry.name, sizeBytes: entry.size, duplicateNameCount: entry.duplicateNameCount ?? 1 },
    note: `exact entry in the SAME era (${eraCatalog.era}) container index; identity = era + container SHA + entry name + payload SHA`,
  };
}

/** The controlled WRONG-ERA attempt: resolving a name that exists in era A
 * against era B's catalog. MUST end NAME_NOT_FOUND in era B and record the
 * refused cross-era attempt — it can NEVER resolve across eras. */
export function resolveCrossEra(name, sourceEraCatalog, targetEraCatalog) {
  const inSource = resolveNameInEra(name, sourceEraCatalog);
  const inTarget = resolveNameInEra(name, targetEraCatalog);
  return {
    disposition: inTarget.disposition, // must be NAME_NOT_FOUND for a wrong-era name
    crossEraRefused: inTarget.disposition === 'NAME_NOT_FOUND' && inSource.disposition === 'NAME_FOUND_EXACT',
    source: { era: sourceEraCatalog.era, disposition: inSource.disposition },
    target: { era: targetEraCatalog.era, disposition: inTarget.disposition },
    note: 'cross-era resolution is REFUSED by construction (era-scoped catalogs); a name found in one era is NEVER resolved in the other era by this logic',
  };
}

/** Image disposition of a FOUND entry, from its payload bytes. A header sniff
 * is NEVER an image decode: IMAGE_DECODED requires a real pixel decode and is
 * not claimed anywhere in this chain. */
export function imageDispositionOf(payloadBytes) {
  const sniff = sniffPayload(payloadBytes);
  switch (sniff.sniffClass) {
    case 'DDS':
      return { imageDisposition: 'IMAGE_SNIFFED_DDS', sniff, note: 'DDS magic present — header classification ONLY; NOT an image decode' };
    case 'TGA_HEADER':
      return { imageDisposition: 'IMAGE_SNIFFED_TGA_HEADER', sniff, note: `plausible TGA header ${sniff.tgaWidth}x${sniff.tgaHeight}@${sniff.tgaBpp} — header classification ONLY; NOT an image decode` };
    case 'NIF':
      return { imageDisposition: 'IMAGE_NOT_DECODED', sniff, note: 'payload is a NIF, not an image — NOT decoded' };
    default:
      return { imageDisposition: 'IMAGE_NOT_DECODED', sniff, note: `${sniff.note ?? 'no recognized image header'} — content UNKNOWN, kept visible (never a fake IMAGE_DECODED)` };
  }
}

/** Aggregate dispositions for one model's recorded name edges (the phase-3
 * JSONL per-model aggregate used by the catalog rows + the gates). */
export function aggregateNameEdges(edges) {
  const agg = { nameEdges: 0, nameFound: 0, nameBase: 0, nameNotFound: 0, matEdges: 0 };
  for (const e of edges) {
    if (e.edge === 'SHAPE->NIMATERIALPROPERTY') agg.matEdges++;
    else {
      agg.nameEdges++;
      if (e.disposition === 'NAME_FOUND_EXACT') agg.nameFound++;
      else if (e.disposition === 'NAME_BASE_MATCH_EXTENSION_DIFF') agg.nameBase++;
      else if (e.disposition === 'NAME_NOT_FOUND') agg.nameNotFound++;
    }
  }
  return agg;
}
