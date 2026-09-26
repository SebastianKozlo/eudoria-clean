# GEOREF / ORIGIN / SCALE AUDIT - EU935-M1

PE-MASTER in-session audit content, persisted verbatim (formatted; no content
changes).

## WORLD / SCALE CONSTANTS

- World = 131,072 units; tile = 128 units (the >>7 math); m->cm x100
  (FUN_0082b790).
- Height field = FULL world at 512-unit texels, origin -65,536
  (FUN_009478e0 + the georef run CONFIRMED at world-datum level):
  the +50.0 slot datum byte-locked - instruction bytes DC 05 20 1D A8 00
  (FADD [0x00A81D20]) at exactly 2 .text sites 0x00948378 / 0x00949162; the
  packer 2xf32 {value,format} verified.
- Water level = 10.0f field-datum (bytes 00 00 20 41 @0x00A7B128).
- Per-tile DATA-level key = filename-xy CONFIRMED both eras (PE-MASTER name
  census 58,451 entries); ENGINE-side keying = BLOCKED-UNKNOWN.

## ORIGIN (the S singleton)

- ORIGIN_INITIAL_ZERO: CONFIRMED.
- ORIGIN_MUTATION_CHANNEL_EXISTS: CONFIRMED (writer 0x00458E27 - 3 f32
  stores; setter FUN_00458D90: S := f32(-(int32)in)).
- Runtime mutated value: UNVERIFIED (STATIC-ONLY).
- OUTPUT formula: out[i] = f32(f32(W[i]*(double)(float)0.01) - S[i])
  CONFIRMED; the zero-origin behavior is the special case CONDITIONAL.
- ORIGIN_PERMANENT_ZERO and unconditional W*0.01 stay REJECTED / SUPERSEDED
  (do not resurrect - see RETRACTION_SUPERSESSION_LEDGER.csv rows 2-3).

## REMAINING UNKNOWNS - CLASSIFICATION

- Engine-side keying = accepted bounded limitation (honest BLOCKED-UNKNOWN).
- Runtime origin value = later-milestone dependency (runtime capture).
- Neither is an M1 closure blocker per the V4.1 honest-limits contract.
