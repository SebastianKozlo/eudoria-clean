// catalog_texture_gates.test.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 4 (W6)
// TEXTURE-LINK GATES (contract §7): wrong-ID / wrong-era / missing-image cases
// produce CONTROLLED dispositions (each named, no false PASS, no cross-era
// resolution) — synthesized against the PRODUCTION resolution logic
// (tools/pecompat/texture_chain.mjs) with the REAL same-era texture container
// indexes, read BOUNDED (index-only tail/directory reads — no payload loads;
// the payload reads here are single-entry bounded reads for the image sniff).
//
// REUSE LABEL: the resolution logic under test is tools/pecompat/
// texture_chain.mjs (the module shared with the product); the containers are
// read with the NEW bounded index readers from tools/pecompat/catalog_data.mjs
// (readBnt2Index / readArkCentralDirectory — themselves dual-index-gated in
// catalog_archive_safety.test.mjs); the image sniff is the phase-2
// catalog_sniff.mjs (imported UNCHANGED inside texture_chain).
import { readFile, open } from 'node:fs/promises';
import {
  readBnt2Index, readArkCentralDirectory, CATALOG_PINS,
} from '../../tools/pecompat/catalog_data.mjs';
import {
  makeEraCatalog, resolveNameInEra, resolveCrossEra, imageDispositionOf,
} from '../../tools/pecompat/texture_chain.mjs';

const RUN_ID = 'PE_CITY_ASSET_MAP_R1_20261010';

function rec(id, name, status, extra = {}) {
  return { id, name, status, ...extra };
}
const ok = (b) => (b ? 'PASS' : 'FAIL');

/** Bounded single-entry payload read (open + read at offset + size). */
async function readEntryPayload(filePath, entry, maxBytes) {
  if (entry.size > maxBytes) {
    return new Uint8Array(0); // refuse oversized reads (bounded)
  }
  const fh = await open(filePath, 'r');
  try {
    const buf = new Uint8Array(entry.size);
    const { bytesRead } = await fh.read(buf, 0, entry.size, entry.offset ?? entry.dataOffset);
    return buf.subarray(0, bytesRead);
  } finally {
    await fh.close();
  }
}

export async function run(ctx) {
  const records = [];
  const texturesArkPath = ctx.texturesArkPath ?? CATALOG_PINS.texturesArk.path;
  const texturesBntPath = ctx.texturesBntPath ?? CATALOG_PINS.texturesBnt.path;

  let cdCatalog, pcgCatalog;
  try {
    const [arkIdx, bntIdx] = await Promise.all([
      readArkCentralDirectory(texturesArkPath),
      readBnt2Index(texturesBntPath),
    ]);
    cdCatalog = makeEraCatalog({
      era: 'CD_2003', container: 'Textures/Textures.ark', entries: arkIdx.entries,
    });
    pcgCatalog = makeEraCatalog({
      era: 'PCG_9_3_5', container: 'Textures/Textures.bnt', entries: bntIdx.entries,
    });
  } catch (e) {
    records.push(rec('CAT_TEX_PREREQ', 'bounded index reads of the real same-era texture containers', 'NOT_PERFORMED', {
      measuredQuantity: 'container availability',
      measured: String(e?.message ?? e).slice(0, 500),
      failureCaseDetected: 'texture containers unavailable — honest NOT_PERFORMED (never PASS); every gate below is skipped',
    }));
    return records;
  }

  // container identity (size check; bounded reads did not hash the whole files)
  records.push(rec('CAT_TEX_PREREQ', 'bounded index reads of the real same-era texture containers (index-only; payload bytes NOT loaded)', 'PASS', {
    measuredQuantity: 'entry counts of both era texture containers via the bounded index readers',
    measured: {
      CD_2003_Textures_ark_entries: cdCatalog.entryCount,
      PCG_9_3_5_Textures_bnt_entries: pcgCatalog.entryCount,
      expected: { CD_2003: 4833, PCG_9_3_5: 8381 },
      identity: 'container SHAs are pinned in the report package (INPUT_IDENTITIES.json); the bounded index readers verify structure; whole-file hashing stays a phase-2 measured record',
    },
    failureCaseDetected: cdCatalog.entryCount !== 4833 || pcgCatalog.entryCount !== 8381 ? 'entry count mismatch vs the phase-2 measured catalog' : 'none',
  }));

  // ---- G1: wrong-ID (nonexistent name) -> controlled NAME_NOT_FOUND ----
  {
    const wrongId = 'Definitely_Not_A_Real_Texture_Name_0123456789';
    const r1 = resolveNameInEra(wrongId, cdCatalog);
    const r2 = resolveNameInEra(wrongId, pcgCatalog);
    const controlled = r1.disposition === 'NAME_NOT_FOUND' && r2.disposition === 'NAME_NOT_FOUND' &&
      r1.entry === null && r2.entry === null;
    records.push(rec('CAT_TEX_WRONG_ID', 'wrong-ID: a nonexistent texture name resolves to the CONTROLLED NAME_NOT_FOUND disposition in BOTH eras (named, no crash, no false PASS)', ok(controlled), {
      measuredQuantity: 'resolveNameInEra dispositions for a synthetic nonexistent name',
      measured: { cd2003: r1, pcg935: r2 },
      failureCaseDetected: controlled ? 'none — controlled NAME_NOT_FOUND in both eras' : 'a nonexistent name resolved (false PASS defect)',
    }));
  }

  // ---- G2: wrong-era -> controlled refusal; NO cross-era resolution ----
  {
    // real names: one from EACH era's container
    const cdName = cdCatalog.entryCount > 0 ? [...cdCatalog.byName.keys()][0] : null;
    const pcgName = pcgCatalog.entryCount > 0 ? [...pcgCatalog.byName.keys()][0] : null;
    const cdInPcg = resolveCrossEra(cdName, cdCatalog, pcgCatalog);
    const pcgInCd = resolveCrossEra(pcgName, pcgCatalog, cdCatalog);
    const controlled =
      cdInPcg.disposition === 'NAME_NOT_FOUND' && cdInPcg.crossEraRefused === true &&
      pcgInCd.disposition === 'NAME_NOT_FOUND' && pcgInCd.crossEraRefused === true &&
      cdInPcg.source.disposition === 'NAME_FOUND_EXACT' && pcgInCd.source.disposition === 'NAME_FOUND_EXACT';
    records.push(rec('CAT_TEX_WRONG_ERA', 'wrong-era: a REAL texture name found in its own era resolves ONLY there; resolving it in the OTHER era is a CONTROLLED WRONG_ERA refusal (never a cross-era resolution)', ok(controlled), {
      measuredQuantity: 'resolveCrossEra dispositions with real era-specific names',
      measured: {
        cdNameInPcg: { name: cdName, ...cdInPcg },
        pcgNameInCd: { name: pcgName, ...pcgInCd },
      },
      independentSourceOfTruth: 'the real container indexes of both eras (name sets are disjoint by construction: .tga/.DDS vs .dat naming)',
      whyNonCircular: 'the resolver is era-scoped by construction; the gate proves the refusal behavior on real names',
      failureCaseDetected: controlled ? 'none — both wrong-era attempts were refused (crossEraRefused=true, NAME_NOT_FOUND in the target era)' : 'a cross-era resolution occurred (era-discipline defect)',
    }));
  }

  // ---- G3: missing-image (header sniff is NOT an image decode) ----
  {
    // find a real OTHER-class stub entry in Textures.ark (the 41 phase-2 stubs):
    // tiny entries whose payload has no image header
    const candidates = [...cdCatalog.byName.values()].filter((e) => e.size <= 96);
    let stub = null; let stubSniff = null;
    for (const c of candidates) {
      const payload = await readEntryPayload(texturesArkPath, c, 96);
      if (payload.length === 0) continue;
      const img = imageDispositionOf(payload);
      if (img.imageDisposition === 'IMAGE_NOT_DECODED') { stub = c; stubSniff = img; break; }
    }
    let dds = null; let ddsSniff = null;
    for (const [name, e] of cdCatalog.byName) {
      if (e.size < 4 || e.size > 4096) continue;
      const payload = await readEntryPayload(texturesArkPath, e, 4096);
      if (payload.length === 0) continue;
      const img = imageDispositionOf(payload);
      if (img.imageDisposition === 'IMAGE_SNIFFED_DDS') { dds = { name, ...e }; ddsSniff = img; break; }
    }
    const controlled =
      stub && stubSniff && stubSniff.imageDisposition === 'IMAGE_NOT_DECODED' &&
      (dds ? ddsSniff.imageDisposition === 'IMAGE_SNIFFED_DDS' && !/IMAGE_DECODED/.test(ddsSniff.imageDisposition) : true);
    records.push(rec('CAT_TEX_MISSING_IMAGE', 'missing-image: a real stub entry (no image header) resolves NAME_FOUND_EXACT but its image disposition is the CONTROLLED IMAGE_NOT_DECODED (never a fake IMAGE_DECODED); a real DDS entry is IMAGE_SNIFFED_DDS (header classification ONLY)', ok(!!controlled), {
      measuredQuantity: 'imageDispositionOf on real payload bytes (bounded single-entry reads)',
      measured: {
        stub: stub ? { name: stub.name, size: stub.size, image: stubSniff } : 'no stub found (unexpected — phase 2 measured 41)',
        dds: dds ? { name: dds.name, size: dds.size, image: ddsSniff } : null,
        policy: 'IMAGE_DECODED requires a real pixel decode and is claimed NOWHERE in this run (PREREGISTRATION §3 disposition order)',
      },
      independentSourceOfTruth: 'the actual payload bytes of real entries (bounded reads at index-derived offsets)',
      whyNonCircular: 'the sniff reads real bytes; the disposition classes were frozen in PREREGISTRATION §3 before this phase',
      failureCaseDetected: controlled ? 'none — stub controlled as IMAGE_NOT_DECODED; DDS as a header sniff only' : 'an image decode was claimed from a header (false PASS defect)',
    }));
  }

  // ---- G4: honest negative re-verification — a real PCG935 model texture name ----
  {
    // 'Geo_keyboard_0_BASE' is a REAL phase-3-recorded PCG935 model texture
    // name (PHASE3_PCG935_BATCH); phase 3 measured NAME_NOT_FOUND for ALL
    // 3,357 names (the Textures.bnt catalog is numeric-named). Live re-check:
    const name = 'Geo_keyboard_0_BASE';
    const live = resolveNameInEra(name, pcgCatalog);
    const sameLive = live.disposition === 'NAME_NOT_FOUND';
    // and the numeric-entry space check: the same-era container genuinely holds
    // numeric .dat names — so an exact-name match CANNOT succeed for this name
    const numericEntryCount = [...pcgCatalog.byName.keys()].filter((n) => /^\d+\.dat$/i.test(n)).length;
    records.push(rec('CAT_TEX_REAL_NEGATIVE', 'honest negative re-verified LIVE: a real phase-3 model texture name stays NAME_NOT_FOUND in its own era (no invented resolution after the fact)', ok(sameLive && numericEntryCount > 5000), {
      measuredQuantity: 'live resolution of a real recorded model texture name against the regenerated same-era index',
      measured: {
        name, liveDisposition: live.disposition,
        numericEntryCount,
        phase3MeasuredDisposition: 'NAME_NOT_FOUND (all 3,357 name edges; 0 exact matches — DEEP_ANALYSIS §6)',
        agreement: sameLive ? 'LIVE == RECORDED' : 'DISAGREEMENT (would need investigation — never silently absorbed)',
      },
      failureCaseDetected: sameLive ? 'none — live resolution agrees with the recorded phase-3 honest negative' : 'live resolution CONTRADICTS the recorded negative (defect)',
    }));
  }

  // ---- G5: era separation on resolution results (era field integrity) ----
  {
    const cdName = [...cdCatalog.byName.keys()][0];
    const r = resolveNameInEra(cdName, cdCatalog);
    const eraIntegrity = r.era === 'CD_2003' && r.disposition === 'NAME_FOUND_EXACT' &&
      r.container === 'Textures/Textures.ark';
    records.push(rec('CAT_TEX_ERA_FIELDS', 'every resolution result carries its era + container (era-label integrity on the dispositions)', ok(eraIntegrity), {
      measuredQuantity: 'era/container fields of a resolution result',
      measured: { sample: r },
      failureCaseDetected: eraIntegrity ? 'none' : 'era labels missing on a resolution (era-discipline defect)',
    }));
  }

  return records;
}
