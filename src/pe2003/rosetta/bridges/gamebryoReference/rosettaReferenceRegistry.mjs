// rosettaReferenceRegistry.mjs — J5 (Wave B3+B4) consumer lookup API for the
// gamebryoReference knowledge namespace. Parent RUN_ID:
//   PE2003_ROSETTA_GAMEBRYO_BRIDGE_CORRECTIONS_R1_20261030
//
// REFERENCE ONLY (runtime_enabled=false for every record — see
// ROSETTA_INTEGRATION_MAP.json). No archive I/O, no texture decoding, no
// runtime mounting. The ONLY job of this module is strict, era-scoped lookup
// over the four machine-readable knowledge records that live beside it:
//   FORMAT_LOSS_MATRIX.json / TEXTURE_ERA_RECORD.json /
//   CLAIM_CORRECTIONS.json / ROSETTA_INTEGRATION_MAP.json
//
// CORE RULE (PEProvenance.js charter): era is part of the resource identity,
// NEVER a fallback. lookupForBuild() NEVER substitutes an EU_LATER / SDK /
// PE42 record for a different build (e.g. the ISO_5_1_0_0 primary target) —
// it returns an explicit REJECTED result instead.

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));

/** Eras that actually have records in THIS namespace (never extended by guess). */
export const ERAS_LOCAL = Object.freeze(['EU_LATER']);

/** Build identifiers this registry knows about (records exist only for EU_LATER). */
export const BUILD_IDS = Object.freeze({
  PRIMARY_TARGET: 'ISO_5_1_0_0',       // primary target build — NO record here is its truth
  REFERENCE_OTHER_BUILD: 'SDK_1_2',   // Gamebryo 1.2 SDK — convention reference only
  MODELS: 'PE42',                      // PE42 model corpus (NIF 4.1.0.12) — not same-era with the textures
});

const RECORD_FILES = Object.freeze({
  FORMAT_LOSS_MATRIX: 'FORMAT_LOSS_MATRIX.json',
  TEXTURE_ERA_RECORD: 'TEXTURE_ERA_RECORD.json',
  CLAIM_CORRECTIONS: 'CLAIM_CORRECTIONS.json',
  ROSETTA_INTEGRATION_MAP: 'ROSETTA_INTEGRATION_MAP.json',
});

let cache = null;

/** Load (and memoize) the four knowledge records. Throws on missing/malformed JSON. */
export function loadRecords({ refresh = false } = {}) {
  if (cache && !refresh) return cache;
  const out = {};
  for (const [key, file] of Object.entries(RECORD_FILES)) {
    out[key] = JSON.parse(readFileSync(join(HERE, file), 'utf8'));
  }
  cache = out;
  return out;
}

/** Record ids (era:container keys) available for lookup. */
export function listRecordIds() {
  return loadRecords().TEXTURE_ERA_RECORD.records.map((r) => r.record_id);
}

/**
 * Look up a texture-era record by archive SHA256 (full hash or unambiguous
 * prefix, min 8 hex chars, case-insensitive). Returns a FROZEN result:
 *   { status: 'FOUND', record, era, usable_as_primary_target_truth, ... }
 * or { status: 'NOT_FOUND', reason } — never throws for a miss, never invents.
 * The returned record ALWAYS carries its era; callers must not strip it.
 */
export function lookupByArchiveSha256(sha) {
  if (typeof sha !== 'string' || !/^[0-9a-fA-F]{8,64}$/.test(sha)) {
    return { status: 'NOT_FOUND', reason: `invalid sha256 query: ${String(sha)}` };
  }
  const needle = sha.toLowerCase();
  const recs = loadRecords().TEXTURE_ERA_RECORD.records;
  const hits = recs.filter((r) =>
    typeof r.archive_sha256 === 'string' &&
    r.archive_sha256.toLowerCase().startsWith(needle));
  if (hits.length === 0) {
    return {
      status: 'NOT_FOUND',
      reason: `no record in this reference namespace matches archive sha256 prefix '${needle}'`,
    };
  }
  if (hits.length > 1) {
    return { status: 'NOT_FOUND', reason: `ambiguous sha256 prefix '${needle}' matches ${hits.length} records` };
  }
  const r = hits[0];
  return Object.freeze({
    status: 'FOUND',
    record_id: r.record_id,
    era: r.era,                                  // era is part of the identity — never stripped
    container: r.container,
    archive_sha256: r.archive_sha256,
    same_era_with_pe42: r.same_era_with_pe42,
    usable_as: r.usable_as,                     // 'RE_EVIDENCE_ONLY'
    usable_as_primary_target_truth: r.usable_as_primary_target_truth, // false
    primary_target_build: r.primary_target_build,
    evidence_pointer: r.evidence_pointer,
  });
}

/**
 * Strict build-scoped query. NEVER substitutes: if this namespace holds no
 * record whose era matches the requested build, the result is an explicit
 * REJECTED naming the forbidden substitution classes. A caller asking for
 * the ISO_5_1_0_0 primary target can therefore NEVER silently receive an
 * EU_LATER / SDK_1_2 / PE42 record.
 */
export function lookupForBuild(buildId) {
  const recs = loadRecords().TEXTURE_ERA_RECORD.records;
  if (buildId === BUILD_IDS.PRIMARY_TARGET) {
    // The primary target build has NO record in this reference namespace.
    const eraRecord = recs.find((r) => r.era === BUILD_IDS.PRIMARY_TARGET);
    if (!eraRecord) {
      return Object.freeze({
        status: 'REJECTED',
        build: buildId,
        reason: 'no ISO_5_1_0_0-era records exist in this reference namespace; ' +
          'cross-era substitution of EU_LATER / SDK_1_2 (REFERENCE_OTHER_BUILD) / ' +
          'PE42 records as ISO_5_1_0_0 truth is FORBIDDEN (era is identity, never a fallback)',
      });
    }
  }
  const hit = recs.find((r) => r.era === buildId);
  if (!hit) {
    return Object.freeze({
      status: 'REJECTED',
      build: String(buildId),
      reason: `no record with era '${String(buildId)}' exists in this reference namespace; ` +
        `available eras: ${ERAS_LOCAL.join(', ')}; no substitution performed`,
    });
  }
  return Object.freeze({
    status: 'FOUND',
    build: buildId,
    era: hit.era,
    record_id: hit.record_id,
    archive_sha256: hit.archive_sha256,
    usable_as: hit.usable_as,
    usable_as_primary_target_truth: hit.usable_as_primary_target_truth,
  });
}

/** Look up one capability row of FORMAT_LOSS_MATRIX.json by name. */
export function lookupCapability(name) {
  const rows = loadRecords().FORMAT_LOSS_MATRIX.rows;
  const hit = rows.find((r) => r.capability === name);
  if (!hit) {
    return { status: 'NOT_FOUND', reason: `no capability row '${String(name)}'`, available: rows.map((r) => r.capability) };
  }
  return { status: 'FOUND', row: hit };
}

/** Look up one claim correction by id (1..6). */
export function lookupCorrection(id) {
  const hit = loadRecords().CLAIM_CORRECTIONS.corrections.find((c) => c.id === id);
  if (!hit) {
    return { status: 'NOT_FOUND', reason: `no correction #${String(id)}` };
  }
  return { status: 'FOUND', correction: hit };
}
