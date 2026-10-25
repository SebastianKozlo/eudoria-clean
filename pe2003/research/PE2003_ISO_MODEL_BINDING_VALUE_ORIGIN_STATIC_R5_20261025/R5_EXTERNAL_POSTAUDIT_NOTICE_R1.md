# R5 External Postaudit Notice — R1 (issued by R6)

RUN_ID: PE2003_ISO_LOADER_VTABLE_INSTANCE_JOIN_STATIC_R6_20261025
This is an ADDITIVE notice placed next to the historical R5 report
(PE2003_ISO_MODEL_BINDING_VALUE_ORIGIN_STATIC_R5_20261025). The R5 files are
byte-untouched; nothing in the R5 package is edited or retracted silently.

The R6 static wave confirmed and corrected the following R5 statements:

1. **Vtable boundary / loader-class.** 65B3BC (comparison-test component)
   and 65B3F0 (W wrapper) are separate ctor-backed vtables. 423280 is the +8
   slot of 65B3F0. The old "+3C census" is not a loader-caller set.
2. **Receiver.** H = [ [ [T+0xF8] ] + 0x10 ]; the first argument of the
   helper is a name source (NS), resolving through a hash lookup into T.
3. **Reader subobject.** 65BA0C is the final vtable of the reader subobject
   (base chain resolved in R6).
4. **Texture path, not model loader.** The wrapper (65B3F0) slot +8 opens a
   file whose name ends `.nif` and returns the first NiPixelData object of
   the file graph; therefore the wrapper is the texture/pixel path, not the
   model loader. D (65CBEC) replaces W as the runtime singleton at 0x6C3F34.
5. **Wrapper-inner (4983D0 svc+38).** Unchanged / carried forward from R5.
6. **Image geometry.** Runtime-initialized globals are zero in the static
   image; their roles are resolved via registration evidence, not via
   absence in the static image. Absence remains a scoped negative only.

**Still open after R6:** per-model binding (296445 / 218757), name producers,
transform writers.

Full R6 report:
`pe2003/research/PE2003_ISO_LOADER_VTABLE_INSTANCE_JOIN_STATIC_R6_20261025/REPORT.md`

Status carried: PE2003_WORLD_XYZ_RECOVERED=NO;
PE2003_HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CANONICAL_GATE_EFFECT=NONE;
EXTERNAL_POSTAUDIT=PENDING.
