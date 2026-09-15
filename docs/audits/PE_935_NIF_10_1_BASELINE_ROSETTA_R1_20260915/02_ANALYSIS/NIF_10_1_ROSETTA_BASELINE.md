# NIF 10.1.0.0 ROSETTA BASELINE — PE_935_NIF_10_1_BASELINE_ROSETTA_R1

Model: ORIGINAL BYTE → NIF FIELD → STANDARD BASELINE → ENTROPIA OBSERVATION →
CURRENT PARSER → STRUCTURAL STATUS → SEMANTIC STATUS → ORIGINAL CLIENT
CONSUMER → EUDORIA RUNTIME STRUCTURE. No link skipped; unknown = UNKNOWN.

## A. File framing

| # | Original bytes | NIF field (engine) | Standard baseline | Entropia observation (this run) | Current parser (R61/JS) | Structural | Semantic | Original client consumer | Eudoria runtime |
|---|---|---|---|---|---|---|---|---|---|
| A1 | 0x0A-term line | HeaderString | Gamebryo 10.1.0.0 line | "Gamebryo File Format, Version 10.1.0.0" 4838/4838 | same | CONFIRMED | CONFIRMED | NiStream::Load | reader header |
| A2 | u32 @line-end | Version | 0x0A010000 | 4838/4838 | same | CONFIRMED | CONFIRMED | version gate | version gate |
| A3 | u32 | User Version | "for companies that modify the format" | 0 in 4838/4838 | reads UV | CONFIRMED | CONFIRMED=0 (MindArk did NOT use the user-version slot) | uv gate | uv gate |
| A4 | u32 x N | Block Type Index (RTTI) | u16 per block | in-range 364,062/364,062 census | same | CONFIRMED | CONFIRMED | object factory | type table |
| A5 | u32 | Num Groups | group count | 0 in 4838/4838 | reads it | CONFIRMED | CONFIRMED=0 | grouping | unused |
| A6 | u32 per block | **GroupID** (NiObject::LoadBinary) | ENGINE 5.0.0.6<=v<10.1.0.114; schemas miss/mis-version | 0 in 2343/2343 closure | "preamble==0 invariant" | CONFIRMED | CONFIRMED (group id; PE always null group) | object grouping | unused |
| A7 | u32+u32[] @EOF | TopObjects | engine LoadTopLevelObjects | count=1, ref=block0 NiNode 2343/2343 | tail raw "UNKNOWN" | CONFIRMED | CONFIRMED | scene roots | scene root |

## B. Scene graph

| B1 | NET Name SizedString | Name | "Scene Root" block0 2343/2343 | same | CONFIRMED | CONFIRMED | named lookup | node name
| B2 | u32+refs | Num Extra Data List + refs | 10.x num+array | closure-valid refs 0 OOR | same | CONFIRMED | CONFIRMED | extra-data attach | metadata list
| B3 | u16 | AV Flags | bitflags | values census captured (e.g. 16) | same | CONFIRMED | PARTIAL (bit meanings per standard) | visibility/frozen-ness | flags
| B4 | Vec3+Mat33+f32 | Translation/Rotation/Scale | transform | finite floats, closure | same (hex parity) | CONFIRMED | CONFIRMED (model-LOCAL only — world placement REJECTED per docs/nif/09) | local transforms | local matrix
| B5 | u32+refs | Num Properties + refs | property chain | refs→property blocks, 0 OOR | same | CONFIRMED | CONFIRMED | state application | property binding
| B6 | i32 | Collision Object Ref | >=10.0.1.0 | -1 mostly; 12 NiCollisionData in corpus | read (12 blocks validated) | CONFIRMED | PARTIAL (BV volumes per schema) | collision attach | optional

## C. Geometry (per NiTriShapeData)

| C1 | u16+u8+u8 | Num Vertices/Keep/Compress Flags | 10.1 fields | closure 16,958 blocks | same | CONFIRMED | PARTIAL (keep/compress bit meanings standard) | geometry upload | vertex count
| C2 | u8 | Has Vertices | bool | closure | same | CONFIRMED | CONFIRMED | vertex alloc | positions
| C3 | Vec3 x N | Vertices | local-space Z-up cm | closure (finite) | hex parity | CONFIRMED | CONFIRMED (units ≈ cm; world-scale claims separate) | vertex buffer | POSITION
| C4 | u8+u8 | Num UV Sets + Extra Vectors Flags | byte pair (10.x) | bit-identical to prior "u16 numUvSets" reading; flags=0 (8,206) / 48 (377) | u16 (equivalent) | CONFIRMED | CONFIRMED (uvcount=low6; tangent bit=0x10) | uv set alloc | TEXCOORD_n
| C5 | u8 | Has Normals | bool | closure | same | CONFIRMED | CONFIRMED | normal alloc | NORMAL
| C6 | Vec3 | Center + Radius | bound sphere | closure | hex parity | CONFIRMED | CONFIRMED | culling | bounding sphere
| C7 | u16+u32+u8 | Num Triangles/Num Triangle Points/Has Triangles | 10.1 fields | 3xN relation observed; closure | same | CONFIRMED | CONFIRMED | index alloc | INDEX
| C8 | u16+groups | Match Groups | part-welding groups | closure | same | CONFIRMED | PARTIAL (welding semantics standard) | part setup | unused/deferred
| C9 | u8 on NiTriShape | Has Shader (+Shader Name/Int if set) | 10.0.1.0..20.1.0.3 | =0 in 8,605/8,605 slice blocks | reads u8 (witness scope) | CONFIRMED | CONFIRMED=0 (PE never uses the shader-name path in slice) | shader hook | unused

## D. Materials & textures

| D1 | u32 | Apply Mode (TexProp) | ApplyMode enum | {0,2} observed (u32 enum-consistent; =MODULATE/HILIGHT) | reads u16+u16 (same 4 bytes) | CONFIRMED (width) | CONFIRMED (enum labels per baseline) | texture op | material mode
| D2 | u32 | Texture Count | 7 default | =7 in 7,088/7,088 slice blocks | same | CONFIRMED | CONFIRMED (era constant) | slot loop | slot loop
| D3 | per-slot u8+desc | Has + TexDesc | Source/Clamp/Filter/UVSet/PS2L/PS2K + HasTransform + 5-field transform (32B) | closure; source=-1 on BASE slots (era binding via ArkTexture) | reads tailA/tailB i16 + transform 32B raw | CONFIRMED | CONFIRMED (transform fields labeled per baseline) | texture stage setup | texture params
| D4 | u32 | Num Shader Textures | >=10.0.1.0 | =0 | reads "trailing u32" | CONFIRMED | CONFIRMED=0 | shader textures | unused
| D5 | 4xColor3+2xf32 | Material colors+gloss+alpha | Phong-era params | closure 8,146 | hex parity | CONFIRMED | CONFIRMED (GLOSS≠roughness per REJECTED overclaim) | D3D material | PBR-ish conversion needed (runtime choice)
| D6 | ArkTexture block | NiArkTextureExtraData (MindArk) | NO baseline (HIST stub partial) | name+3u32+u8+entries[SS+2xi32+ref+9B]; ref→NiTexturingProperty(10,610)/NiTextureEffect(1,105); count=(field2>>8)&0xFFFFFF — 100% in-slice (2343/2343; F-14/AMEND-009 retraction of the former "variant family" claim; corpus-wide outside slice OPEN) | numfield=3 claim + field2>>8 formula + "3 zero bytes" misattribution | CONFIRMED (custom layout, closure-derived) | PARTIAL (slot enum f1; 9-byte trailing = anim_flag+id+frame per prior claim) | ArkTexture → Textures.bnt binding | texture ID resolution
| D7 | importer block | NiArkImporterExtraData (MindArk) | no baseline | name+u32(=8)+SS version-string+41B tail(13B hdr+7xf32 bounds+pad) | 38B tail + 3 bytes re-attributed | CONFIRMED (custom layout, closure-derived) | STRONGLY_SUPPORTED (tail=model local bbox; prior ITER-10 + this-run byte-consistency) | model bounds/DPVS culling | bounding box
| D8 | shader block | NiArkShaderExtraData (MindArk) | HIST stub matches | name+u32(0)+SS(CRLF config) | same | CONFIRMED | PARTIAL (directive vocabulary = prior claims) | effect file assignment | deferred
| D9 | viewport block | NiArkViewportInfoExtraData (MindArk) | HIST stub (13B fixed — WRONG for variants) | name + variable ext (closure boundary) | boundary search | CONFIRMED (boundary) | PARTIAL (camera floats per prior claims) | camera/viewport config | deferred
| D10 | anim block | NiArkAnimationExtraData (MindArk) | HIST stub (4 ints + 37B — v4 only) | name + u1=5 + u2..u4 + ext variant zoo (closure boundary) | variant-limited (witness) | CONFIRMED (boundary/header) | PARTIAL (variant grammars = prior claims; u1=5 era marker observed) | per-node behavior config | deferred

## E. Lights

E1-E4 (NiLight dimmer+colors; Point attenuations; Spot cutoff/exponent;
Directional/Ambient): closure-validated; D3D8-era lighting; runtime = three.js
lights. CONFIRMED structure; semantics standard.

## F. Open links (honest UNKNOWNs at Rosetta level)

- F1 ArkTexture 9-byte trailing split (anim_flag/bnt2_id/frame): prior
  claim, NOT re-validated vs Textures.bnt here.
- F2 [RETRACTED — F-14/AMEND-009]: the former "ArkTexture f1=15/
  0x1000000 24-block variant family" was a decoder candidate-order
  artifact, not a corpus fact. Replacement OPEN item: ArkTexture count
  formula CORPUS-WIDE test outside the 2,363-file slice (in-slice the
  formula is 100% TRUE; raw scan observes 1,790 further zero-count-
  signature blocks outside the slice, unverified).
- F3 ArkViewportInfo ext per-field semantics: PLAUSIBLE (prior).
- F4 ArkAnimation TEXT/G3B/G3D semantics: prior claims (ITER-5..38).
- F5 NiSourceTexture/NiPixelData v10 layouts: schema-defined, deferred
  (45/1 blocks outside slice).
- F6 VertexColor internal split (u32x2 vs u16x2+u32): width-identical;
  semantic adjudication open.
- F7 Non-slice type layouts (45 types): prior-claim closure only.
- F8 Original client consumers for Ark semantics: engine evidence pending
  (M3-5B/runtime track).
