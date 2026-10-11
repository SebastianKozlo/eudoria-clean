# Skill update proposal — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010

Proposed lesson candidates for the pe-reconstruction/threejs skills (audit
required; nothing edited in-place by this run):

1. **NIF 4.x NiProperty double-flags trap**: the property base consumes the
   u16 flags; per-property parsers must not re-read them (the +2-byte shift
   broke the entire v4 corpus before the fix).
2. **NIF light version split**: 4.1.0.12 = dimmer+colors (no effect layer);
   4.0.0.2 = raw-ptr list + colors + trailing f32. Merging them broke 25 files.
3. **r185 AnimationMixer.setTime scrub pitfall**: setTime zeroes action times;
   paused actions never re-advance. Scrub = seek action.time + update(0).
4. **Pixel census discipline**: WebGL readPixels without preserveDrawingBuffer
   is invalid evidence; use screenshot PNG decode with drawer-closed crops.
5. **ArkTexture texprop-level binding**: PCG v10 texprop slots are EMPTY; the
   binding is the ArkTexture entry joined by texturingPropertyRef (with the
   dual tail controls; the 218757 universal interpretation stays retracted).
6. **TGA 24/32-bpp split**: decodeTga2 (24) vs decodeTga2A32Image (32) —
   dispatch by header bpp byte.
