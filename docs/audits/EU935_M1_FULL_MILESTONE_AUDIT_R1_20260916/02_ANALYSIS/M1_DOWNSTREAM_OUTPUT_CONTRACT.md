# M1 DOWNSTREAM OUTPUT CONTRACT - binding for later milestones

PE-MASTER-issued contract content, persisted verbatim (formatted; no content
changes). Every later milestone consuming M1 surface output is bound by this
file. The authority status of all source verdicts is ADVISORY_PRE_QUALIFICATION
(PE-MASTER PROVISIONAL_UNTIL_QUALIFIED; CANONICAL_GATE_EFFECT=NONE).

## 1. COORDINATE SYSTEM

- Engine world = 131,072 units; tile = 128 units; m->cm x100 (FUN_0082b790).
- Consumer formula: out = f32(f32(W * 0.01) - S) with S a MUTABLE runtime
  singleton - later milestones MUST NOT assume S==0 and MUST NOT assume an
  unconditional W*0.01 (the zero-origin behavior is the special case
  CONDITIONAL; see RETRACTION_SUPERSESSION_LEDGER.csv rows 2-3).

## 2. TERRAIN COORDINATE FRAME

- Height field: origin -65,536, 512-unit texels, span 131,072; the +50.0 slot
  datum byte-locked (FADD [0x00A81D20], 2 .text sites).
- Filename-xy per-tile DATA key CONFIRMED both eras.
- Engine-side keying BLOCKED-UNKNOWN - MUST NOT be silently assumed.

## 3. SCALE BEHAVIOR

- Engine constants byte-pinned; runtime calibrations labeled
  CURRENT_RUNTIME_CALIBRATION (e.g. heightScale 128 u16/m; the P-UNITS 0.01
  bridge).

## 4. ORIGIN BEHAVIOR

- Initial zero CONFIRMED; mutation channel CONFIRMED (writer 0x00458E27;
  setter FUN_00458D90: S := f32(-(int32)in)); runtime value UNVERIFIED
  (STATIC-ONLY).

## 5. HEIGHT REPRESENTATION

- The (t-128)x5 m model is STRONGLY_SUPPORTED at data level with the 16-bit
  decode 79.606% reproduced (PE-MASTER land recomputation).
- u16 x 1/128 = the runtime calibration.
- The two models are reconciled as DECODE-MODEL VARIANTS - consumers MUST
  state which model they consume.

## 6. TERRAIN TEXTURE INPUTS / LIMITS

- ID-resolution 99.8613% (24,474/24,508, era 9.3.5; dangling 34 classified).
- Name-anchor 80.40% measured (OBSERVED class; [79.90,80.90]).
- Climate/detail grids 432502/459344 patcher-delivered MISSING (era-bounded
  placeholders [P1]/[P2]).
- WAVES/SKY plane textures missing ([P-WAVES]/[P-SKY]).

## 7. TILE / CELL INTERFACE

- TDF 52/64 offset spaces NEVER collapsed.
- Type census per V4 row 4 (layer TYPE census {0,2,3,6,7,9/0xa}).
- Special rows: structure-only (6,530 PCG tiles; no semantics claimed).

## 8. VEGETATION MECHANISM / LIMITS

- Mechanism CONFIRMED + byte-locked (iter035: the grid/cell-record/spawn-loop
  /RNG arithmetic; the three QWORD operands + the six FSTP f32 points).
- Cell content + climate selection RECONSTRUCTION-ONLY ([P-CELLSTREAM] /
  [P-CLIMATE]) - foliage is NOT 1:1.
- The engine-parity arithmetic is CONDITIONAL on the x87 model
  (PC in {53,64} + RC=nearest-even; the actual CW UNMEASURED).

## 9. BLOCKED UNKNOWNS later milestones MUST NOT silently assume

The OPEN_LIMITS list (01_RAW/OPEN_LIMITS.csv): cell byte-stream origin;
climate per-location selection; engine-side tile keying mechanism;
patcher-delivered grids 432502/459344; x87 actual CW; original-client visual
parity; WAVES/SKY plane textures; JUL-era runtime semantics (loader-absent
era fact); TDF min/max source; special-row tile semantics; dim2/dim4
semantics; >4-material reduction; rotation/variant candidates; p3 seed input;
clean pesource NIF path; P-UNITS bridge; noise seed [P4].

## 10. EVIDENCE VERSION / SOURCE PINS

The SOURCE_INDEX table (00_CONTROL/SOURCE_INDEX.md) is the pin record for
every physical source this contract builds on: Entropia.exe PCG_9_3_5
E7785430... (THE address-level binary; the different-era Entropia.exe
E706C715... is never to be used for 9.3.5 address claims); Models.bnt
C950A8C2...; Textures.bnt 61ACD13B...; terrain.bnt 95841761... (fresh pin,
F4); the Terrain.bnt stub FC0168D5... (byte-verified); VegetationClimates.bnt
7B858401... (both copies byte-identical); 50.bnt A6E59EE0...; JUL-era
Textures.bnt 2EAE1159... (era-labeled); the V4.1 package identities
EC04FC47... / 003056AC... / 9944925D....
