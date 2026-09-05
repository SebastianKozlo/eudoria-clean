// PEProvenance.js — PE MILESTONE 1 ITER 001 (PE_WORLD_SURFACE_FIDELITY_R1)
// Provenance records + evidence-status taxonomy for the PESourceMount layer.
// The charter (NEXT_PROMPT.md §7) requires every resource result to carry:
//   era / container / entry name/id / physical source / offset where
//   meaningful / decoder version / evidence status.
// NO renderer semantics here. NO silent cross-era substitution — the era is
// part of the resource identity, never a fallback.

export const EVIDENCE_STATUS = {
  CONFIRMED: 'CONFIRMED',
  STRONGLY_SUPPORTED: 'STRONGLY_SUPPORTED',
  PLAUSIBLE: 'PLAUSIBLE',
  UNVERIFIED: 'UNVERIFIED',
  REJECTED: 'REJECTED',
};

export const ERAS = {
  CD_JAN_2003: 'CD_JAN_2003',   // Jan-2003 CD installer corpora (comparison/RE evidence)
  JUL_2003: 'JUL_2003',         // PRIMARY HISTORICAL TARGET (charter §1)
  PCG_9_3_5: 'PCG_9_3_5',       // 9.3.5 installed client (pcg_install) — the CLEAN
                                // RUNTIME primary era (ledger ENTRY #1/#6); never
                                // silently mixed with JUL_2003 historical truth
  EU_LATER: 'EU_LATER',         // later EU-runtime corpora — RE evidence ONLY,
                                // never silently JUL-2003 truth
};

// Known canonical containers with their audited SHA256 (charter §1 + FULL_SYNC §02
// + ITER_010 container census 2026-09-04 — EU_LATER Textures.bnt byte-identical in
// both physical copies; CD Textures.ark per iter010a census).
export const KNOWN_HASHES = {
  'JUL_2003:Terrain/50.bnt': 'A6E59EE07A51EAC06A3E75DA5421E5928D59EDED74F096DCAD04CE80ED01DA00',
  // PCG_9_3_5 terrain container (era-validated ITER 019: BNT2 framing, 58,451
  // entries; 51,920 regular 220x236 filename-xy + 6,530 special rows + sentinel).
  'PCG_9_3_5:Terrain/terrain.bnt': '95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990',
  // EU-runtime texture corpus (8,095 BNT2 entries; M3-2-R1 8,095/8,095 raw payloads).
  'EU_LATER:Textures.bnt': '2EAE115958D3157FA62F8CBFBAC6F4BFB5C38A820F1D05F9248C4200C0208A56',
  // PCG_9_3_5 texture corpus (SAME-ERA container for the clean runtime primary
  // era; BNT2 framing verified in-session ITER 020; 973,942,771 bytes).
  'PCG_9_3_5:Textures.bnt': '61ACD13B140E130647EEE24C1E2669D3734990B76CF74897DDD3BA0F4EA61393',
  // Jan-2003 CD texture corpus (4,833 ArkVFS entries; F-107 canon).
  'CD_JAN_2003:Textures.ark': 'D611D1257D2E5433B6DF218D671AA60D003C5C6587858757C7AF3219BB739B80',
  // PCG_9_3_5 vegetation climate corpus (BNT2 framing, 32 .vcl entries;
  // iter032k census; byte-identical in all 3 corpus copies incl. JUL_2003 —
  // the DATA is 2003-era, the 9.3.5 loader is later-generation, era-labeled).
  'PCG_9_3_5:VegetationClimates/VegetationClimates.bnt':
    '7B858401C3EEBDA574DF4B4517E7FB2A8149C283885F27187682AA1239C745F4',
};

export function makeProvenance(fields) {
  if (!fields.era) throw new Error('[PESourceMount] provenance requires era (NO silent era)');
  if (!fields.container) throw new Error('[PESourceMount] provenance requires container');
  if (!fields.evidenceStatus) throw new Error('[PESourceMount] provenance requires evidenceStatus');
  return {
    era: fields.era,
    container: fields.container,
    entry: fields.entry ?? null,          // entry name and/or numeric id
    physicalSource: fields.physicalSource ?? null, // absolute path / URL of the original bytes
    offset: fields.offset ?? null,        // byte offset where meaningful
    decoderVersion: fields.decoderVersion ?? null,
    evidenceStatus: fields.evidenceStatus,
    extra: fields.extra ?? null,
  };
}
