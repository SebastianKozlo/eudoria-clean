# Formats — PE 2003 corpus (sanitized structural facts, no payloads)

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024.
Structural/empirical findings about the container and asset formats of the
2003 corpus. Field layouts only — no game data payloads are included.

## ARK game archives — ZIP-like with `AK` magic

Models.ark / Textures.ark / Scripts.ark / Volumes.ark are ZIP-clone containers
("AK" instead of "PK"):

- Local file header: magic `AK\x03\x04`, then STANDARD ZIP local-header layout
  (30 B fixed): version_needed u16@4, flags u16@6, compression u16@8,
  mod_time u16@10, mod_date u16@12, crc32 u32@14, comp u32@18, uncomp u32@22,
  name_len u16@26, extra_len u16@28. Members are STORED (comp == uncomp).
- Central directory: magic `AK\x01\x02` entries (48 B fixed incl. name at +46).
- End of central directory: magic `AK\x05\x06` (22 B).
- Local-scan chain == EOCD count == central-directory count for all 4 archives
  (Models 2492, Textures 4833, Scripts 1937, Volumes 831 members); CRC32
  verified per member (2492/2492, 831/831 etc.).
- Decoder: `tools/ark_vfs_decoder_f1.py` (own code, QUALIFIED_WITH_CAVEAT
  noted for the older skill parser's u32 name_len@26 read; this decoder
  implements the standard-ZIP layout exactly and cross-checks local chain vs
  central directory vs EOCD). Negative tests 4/4.

## Scripts.ark members — Blowfish-CBC encoded DLOB bytecode

- Scripts.ark holds 1937 members: 1 plaintext script, 10 stubs, 1936 binary
  DLOB objects (disjoint classification of the 1937 vs 1+10+1936 split is an
  honest unresolved bookkeeping question — supersession CS14).
- Binary members are Blowfish-CBC encoded; the client ingest path is
  FUN_005235E0 (code-pinned). Decoded-corpse canon (1936/1936 decoded, prior
  campaign) was reused read-only; no re-decode performed this campaign and
  no key material is published.
- Decoded `.obj` members are DLOB object-type definitions: chunk-dispatch
  format (chunk-size field = BYTE LENGTH, established empirically in W1),
  parsed by FUN_00453860, linked with EXTN patch (E15) and fed into a VM
  engine class (E13/E16/E17). The CODE region carries `0x7700xxxx`-prefixed
  opcodes; the client parses+links them but has no interpreter for the
  `0x7700xxxx` token family (E19, negative with denominators 5776 indirect
  CALL sites / 576 444 instructions; partial revision: `0x7fffec7x` runtime
  opcodes ARE consumed). Server-side execution suspected — open frontier.

## .bvi paired volumes — 12 × big-endian f32 records

- Volumes.ark = 831 `.bvi` members = 7032 records × 48 B (12 big-endian f32
  each): model-LOCAL collision volumes with an extent-mirror structure.
- Paired members for the two target models: `296446.bvi` (1008 B = 21 records,
  CRC 27EE4229), `218758.bvi` (864 B = 18 records, CRC 5DD32B83).
- `open_bvi_by_id` (VA 0x520D80) returns the raw buffer in the open path; no
  parse in the open path. Zero model IDs inside the .bvi corpus (negative,
  denominator 831 members) — .bvi is NOT an instance/placement source.

## NIF 4.1.0.12 (0x0401000C) model files

- Header: raw ASCII `"NetImmerse File Format, Version 4.1.0.12\n"` (NO length
  prefix), then u32 version 0x0401000C, u32 num_blocks; blocks follow, each
  preceded by its INLINE type SizedString (u32 len + name). NO block-size
  table — block ends are resolved by strict field parse validated against the
  next block's inline type string (anchor scan seeds the chain only).
- Footer: u32 num_roots + root refs (cross-checked against the computed
  hierarchy in the inspector).
- Ark-specific block types observed: NiArkBillboardNode,
  NiArkTextureExtraData, NiArkAnimationExtraData, NiArkImporterExtraData,
  NiArkViewportInfoExtraData, NiArkShaderExtraData.
- Empirical single-instance fits (field-level status UNVERIFIED, retained in
  the inspector's `fit_calibration`): NiTextureEffect (296445 block 13),
  NiUVController (block 33), NiUVData (block 34).
- The 9.3.5-era variant of model 218757 is NIF 10.1.0.0 — a different file
  format generation; the cross-variant structural diff was NOT executed.

## Terrain 50.bnt

- Two distinct versions exist (8E43CD14… / A6E59EE0… — see
  sources-and-provenance.md). Neither was decoded in this campaign; terrain
  work requires explicit authorization.

## Boundary honesty

- No third-parser cross-check was available for the NIF inspector (PyFFI
  cannot parse NiArk* 4.1.0.12); boundary validation is
  downstream-alignment + census-match based, with explicit per-block
  parse statuses (FIELDS_CONFIRMED / PARTIAL_FIELDS_OPAQUE_TAIL /
  UNKNOWN_TYPE / TRUNCATED).
