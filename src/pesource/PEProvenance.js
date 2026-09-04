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
  EU_LATER: 'EU_LATER',         // later EU-runtime corpora — RE evidence ONLY,
                                // never silently JUL-2003 truth
};

// Known canonical containers with their audited SHA256 (charter §1 + FULL_SYNC §02
// + ITER_010 container census 2026-09-04 — EU_LATER Textures.bnt byte-identical in
// both physical copies; CD Textures.ark per iter010a census).
export const KNOWN_HASHES = {
  'JUL_2003:Terrain/50.bnt': 'A6E59EE07A51EAC06A3E75DA5421E5928D59EDED74F096DCAD04CE80ED01DA00',
  // EU-runtime texture corpus (8,095 BNT2 entries; M3-2-R1 8,095/8,095 raw payloads).
  'EU_LATER:Textures.bnt': '2EAE115958D3157FA62F8CBFBAC6F4BFB5C38A820F1D05F9248C4200C0208A56',
  // Jan-2003 CD texture corpus (4,833 ArkVFS entries; F-107 canon).
  'CD_JAN_2003:Textures.ark': 'D611D1257D2E5433B6DF218D671AA60D003C5C6587858757C7AF3219BB739B80',
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
