---
run_id: PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010
card: ark-texture-tail-controls
status: MEASURED_ON_CORPUS
sources:
  - path: D:/Eudoria_Reconstruction/pcg_install/Data/Textures/Textures.bnt
    sha256: 61acd13b140e130647eee24c1e2669d3734990b76cf74897ddd3ba0f4ea61393
  - module: src/pecompat/PecTextureChain.js (pec-texture-chain-pcg935-r1)
corpus_scope: 3761/5596 catalog entries carry ArkTexture data
classification: INTERNAL_QC_ONLY_PENDING_DESKTOP
created: 2026-10-11
---

# ArkTexture 9-byte tail: the controlled binding chain

## The chain (era PCG 9.3.5, measured)

`mesh -> texturing property -> (slot sourceRef or texprop-level) ArkTexture
entry -> 9-byte tail -> [controls] -> Textures.bnt entry id -> decode`.

- **v4**: texturing-property slots carry `sourceRef = -1` (era NULL); the
  binding lives in the ArkTexture extra-data entries.
- **v10**: the slots of NiTexturingProperty are EMPTY in this corpus (mapSlots
  counted 0 for e.g. 505775); the same ArkTexture entries bind at the
  TEXPROP level. The chain therefore resolves the ArkTexture entry by
  `texturingPropertyRef == mesh's texprop` (name-prefix matching is a fallback
  only, never the primary join).

## The two independent controls (both must pass)

The tail `[anim_flag u8][frame_index i32][bnt2_id u32]` is interpreted ONLY
when BOTH pass (the 218757 universal interpretation stays RETRACTED):

1. **byte-shape control**: anim_flag ∈ {0x00, 0x01}; frame_index == -1 or
   0..0xFFFF; 0 < bnt2_id < 0x1000000.
2. **reference control**: bnt2_id EXISTS as a same-era Textures.bnt entry.

A slot resolved through the controls is labelled `ARK_TAIL_CONTROLLED`; the
first-decodable-slot fallback survives ONLY as `RENDER_RECONSTRUCTION` (never
TEXTURED_EXACT, never universal).

## Witness (byte-verified)

223534.nif slot Base: tail hex `00ffffffff08690300` → anim=0, frame=-1,
id = 0x00036908 = 223496 → Textures.bnt entry 223496 = DDS DXT1 256×256 →
decode OK → TEXTURED_EXACT. 505775.nif: 18 meshes, 13 exact + 5 honest
unresolved (controls failed), no fallback needed.

## Texture payload formats (Textures.bnt, 8381 entries)

TGA type 2 (uncompressed truecolor) 5,580 · DDS 2,752 · JPEG 19 ·
TGA type 3 (grayscale) 13 · TGA type 10 (RLE) 16 · TGA type 1 (colormap) 1.
Decoded in this run: DDS DXT1/DXT5 (strict donor DdsDecoder, top-mip
ceiling), TGA2 24bpp (`decodeTga2` CONFIRMED subset) and 32bpp
(`decodeTga2A32Image`). JPEG and TGA types 1/3/10 = UNSUPPORTED_FORMAT
(truthful 415), 19+30 entries affected.
