# TERRAIN WORLD SURFACE AUDIT - EU935-M1 (per the V4.1 rows 1-6)

PE-MASTER in-session audit content, persisted verbatim (formatted; no content
changes). STATIC-ONLY - the client never ran.

## SOURCE BYTES (ORIGINAL, both eras)

- pcg_install\Data\Terrain\terrain.bnt - 125,064,817 B, fresh-pinned this audit:
  SHA256 95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990
  (audit finding F4, P3 - the full SHA256 was NOT_PROVIDED in the prior records;
  this audit records it as the fresh pin).
- 01_Original_Files\BNT\50.bnt (JUL_2003) - 118,016,977 B, fresh pin:
  SHA256 A6E59EE07A51EAC06A3E75DA5421E5928D59EDED74F096DCAD04CE80ED01DA00.
- Container handling: BNT2/BUNT VERSIONED decoders (BuntArchive JUL /
  Bnt2TerrainArchive PCG - never one interpretation forced across eras;
  BUNT_TRAILING_BYTES=8; the legacy BuntArchive never fed terrain.bnt).

## GRID

- 51,920 regular tiles + 6,530 special-row (y=0xff1a..0xffff;
  structure-censused ONLY - no semantics claimed) + sentinel (7ffe7ffe.tdf,
  EXPLICIT_NOT_ASSEMBLED).
- PCG BNT2 footer 58,451 entries; era-validation 0 walk failures;
  full-corpus walk exact consumption 51,920/51,920.

## HEIGHTS

- u16 identity + operation CONFIRMED (PE2003 FUN_0047fb20 = min +
  (max-min)*u16/65535; the 9.3.5 sibling FUN_00989e70 = clamp-65535; the
  full-lerp form in 9.3.5 itself remains open #9).
- 9/9 region tiles byte-faithful vs an INDEPENDENT second parser;
  9216/9216 samples identical vs the frozen r169 oracle; JUL full-map rebuild
  SHA reproduction; 773/51,920 PCG-vs-JUL era-divergent tiles recorded, never
  mixed.
- Height scale 128 u16/m = STRONGLY_SUPPORTED runtime calibration (not an
  engine-extracted constant).

## IMPLEMENTATION

- Deterministic clean pages; self-regression 5/5 EXACT (5/5 clean pages
  reproduce their recorded deterministic hashes on fresh headless-Chromium
  loads) - NOT original-client parity (the B1 honest limit; the
  historical-visual-parity claim is NOT made).

## TEXTURE RESOLUTION

- 99.8613% era-9.3.5 (24,474/24,508 binding-chain targets; the dangling 34
  classified) - binding-chain revalidation eabf6cf.
- Name-anchor 80.40% [79.90,80.90] measured (OBSERVED class) - texanchor
  census c380a26; slot-consistency 100%.

## BLEND SEMANTICS

- Terrain_14 CONFIRMED era 9.3.5 (byte-extracted .fx; the 53/73 thresholds
  byte-match the ORIGINAL palette alpha values {45,62,85} - the double
  data-side confirmation; 13 fail-closed negative controls: 8/8 noise
  mutations + 5/5 witness mutations FAIL, clean copies PASS; noise tables
  2048/2048 bit-exact; the naive 'sequential overlay mix' FALSIFIED iter024,
  superseded by the one-hot model).
- The era-divergent 2003 fixed-function blend RECORDED (never
  auto-propagated; open #22).

## COVERAGE REPORTING DISCIPLINE

CLIENT_KNOWLEDGE / RECONSTRUCTION_IMPLEMENTATION / HISTORICAL_GAME_RECOVERY
are reported per dimension SEPARATELY, with explicit denominators where they
exist and 'no defined denominator' wording where they do not - no invented
percentages (see M1_KNOWLEDGE_IMPLEMENTATION_RECOVERY_MATRIX.md).
