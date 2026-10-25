# R6 — Loader/vtable/instance-join static reconstruction (ISO 5.1.0.0)

RUN_ID: PE2003_ISO_LOADER_VTABLE_INSTANCE_JOIN_STATIC_R6_20261025
Campaign: PE2003, wave R6 — loader/vtable/instance-join static reconstruction
Mode: STATIC_ONLY (no game execution, zero runtime)

## 1. Scope & provenance

- Client: ISO PC Gamer Nov 2003, Project Entropia client 5.1.0.0.
- Code source: statically unpacked image section1.bin
  (SHA256 D43A23B9EFCFC9BC4092B38FA3C73499DE7DE7B03B20F34478B9E81EE8893631).
- Unpack provenance: adler known-answer test PASS recorded in R3
  (PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025).
- Era ban on PE2_unpacked_out.exe remains in force: it is a DIFFERENT build
  (COT 3.4.3.1 lineage) and no VA transfer between the two images is allowed.
- All statements below are era-labelled to the 5.1.0.0 ISO static image.

## 2. Corrected vtable model

- 65B3F0 (the "W" wrapper) and 65B3BC (the comparison-test component) are
  SEPARATE ctor-backed vtables, not one table with drifting slots.
- 423280 is the +8 slot of 65B3F0 (W), not an independent loader table.
- 65B3F0 is the final vtable installed over base 65A980.
- 65BA0C is the final vtable for the reader subobject.

## 3. Loader identity

- The W (65B3F0) slot +8 opens a file whose name ends with `.nif` and returns
  the first NiPixelData object of the loaded file graph. The class key is
  resolved through the CRuntimeClass registry; the NiPixelData / NiNode /
  NiTriShape registrations were identified in the static image.
- Consequence: W is the texture/pixel path, NOT the model loader.
- D (65CBEC) replaces W as the runtime singleton installed at 0x6C3F34.

## 4. Entity chain

- name-source NS -> key -> hash lookup -> T
  -> P = [T+0xF8]
     (vptr 65C0DC; owner at +0x78; lazy H at +0x10; transform-partition
     float block)
  -> H (vptr 65E5B4; created via 0x5257C0; cached at [P+0x10])
  -> O fetched by name from the manager at [H+8] and class-checked
     against NiNode / NiTriShape
  -> comparison-test components attached at O+0xBC
- The handler is dispatched by VM opcode 0x1A456.

## 5. Status

- Model-instance binding for 296445 / 218757 remains OPEN: no per-model
  instance, no transform values, no frame data recovered.
- PE2003_WORLD_XYZ_RECOVERED=NO
- PE2003_HISTORICAL_PLACEMENT=NOT_ESTABLISHED
- CANONICAL_GATE_EFFECT=NONE
- EXTERNAL_POSTAUDIT=PENDING

## 6. Process

- 15 science native attempts plus closing; QC PASS and QC_PARTIAL resolved.
- Budget: 2706 of 24000 decoded rows consumed.
- STATIC_ONLY: no game execution, no original client runtime.
