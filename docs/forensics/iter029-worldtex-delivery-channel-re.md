# Global World-Data Texture Set — Ship Locations, Roles, Delivery Channel (ITER-29 / session ITER_043)

Era: PCG_9_3_5 (Entropia.exe 9.3.5.6746, SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`).
Cross-era: EU2008 corpus client = Entropia.exe **9.2.2.2** (FileVersion measured).
Evidence: `99_Audits/PE_MILESTONE_1_WORLD_SURFACE_R1/03_EVIDENCE/iter029_findings.json`, manifest `iter029_manifest.json` (47 entries). Ledger: `M1_LEDGER.md` ITER_029.

## Question

Where do the three global world-data textures (ids 429259 / 432502 / 459344) ship, what are their exact roles and channels, and what does the fetch/delivery chain prove about the delivery mechanism (local vs patcher vs server)?

## Result

### (a) id 429259 (0x68CCB, 257x257) — SHIPPED, exactly two era byte-states, IDENTICAL payload

| era | container | entry | payload SHA256 |
|---|---|---|---|
| PCG 9.3.5 | `Data\Textures\Textures.bnt` (SHA `61ACD13B...`, 8,381 entries) | `429259.dat` at index 71, offset 6,920,273, size 198,191 | `23D7742EBA6FFB1FDA2F8A58BD0EB95AFDBE055CE23437FF5B47C5A0163A1ED0` |
| EU2008 (=9.2.2.2) | `Data\textures\Textures.bnt` (SHA `2EAE1159...`, 8,095 entries) | `429259.dat` at index 2,785, offset 195,839,349, size 198,191 | identical |

- Absent from the JUL-2003 corpus (7 arks walked; no `429259.*` in any name form).
- Uncompressed TGA, 257x257, 24bpp; heights `(chan0-128)*5` -> [-640,+635] m, mean +79.17 m.
- **World extent (code-confirmed)**: the field covers the FULL 131,072-unit world at 512-unit texels, origin -65,536 (`FUN_009478e0` cell=(pos-origin)>>9 with the 0x100->0xFF edge clamp; `FUN_00949000` origin=-`FUN_00991790`(root); `FUN_009916b0` root size key 65,536; `FUN_00947a40` bilinear stride 0x101). The climate (65x65, 1024u cells) and 129x129 (512u cells) grids cover ONLY the CENTER 65,536-unit region (origin -32,768 = `FUN_00990940` = size/2).

### (b) The fetch chain and the miss path

```
FUN_00416390  { id[0]=runtime singleton+4, 429259, 432502, 459344 }
  -> FUN_0044d590 (gates id[0]!=0; stores ctx+0x24..0x30)
  -> FUN_0044d360 -> FUN_00938f50(ctx[10],ctx[11],ctx[12]) = the 3 hardcoded ids
       3x FUN_006ba110 (type-100) -> any-null => return 0
       dims 257/65/129 validated (pixeldata+0x38/+0x3c)
       bank alloc (0x24 = 9 pointers) -> FUN_0094aac0/ab50/ab90 fills -> 3x release
```

- The provider system = **ArkResourceManager** (DAT_00ba12f4, 0x98 B, `ArkResourceManager::vftable`; type map +0x04; known-missing RB-tree set +0x60). `FUN_00823c10` walks the type-100 provider list; on a **total miss** `FUN_008237d0` = lock -> STL RB-tree INSERT of the missing {type,id} into the known-missing set -> return 0. **No download, no socket, no HTTP, no retry — the resource system is LOCAL-ONLY.**
- The async fetch variant `FUN_008251a0` shares the same miss handler.
- **Failure propagation**: a fetch miss returns 0 up the chain to `FUN_004172a0` (the client init gate sequence): `if (...FUN_00416390() != 0)` — **the whole client init halts without the world-data textures.**
- **Type-100 providers**: `ArkClientGUIService` ctor `FUN_005b3fc0` mounts exactly `UI\ui.bnt` + `Textures\textures.bnt`. The full .bnt mount census of the binary adds terrain (Data\Terrain\), models, musdef, portals, EffectSequences, TerrainEditZones, VegetationClimates, volumes + Parameters VFS + the two TerrainImageCache VFS. **`Textures\Terrain.bnt` does not exist anywhere in the 9.3.5 binary.**

### (c) The 12-byte Terrain.bnt stub — the BNT2 writer's zero-entry output

- `[u32 count=0][u32 dir_off=0]["BNT2"]` — an EMPTY but VALID BNT2 archive (0 entries; no manifest/version/id list).
- Reader `FUN_00967680` (mode-1 open `FUN_00968330`): `fseek(-8,END)` -> magic `'BNT2'` = v2, **`'BUNT'` = v1 — the 2003-era footers parse in the same reader (format continuity)**; names are LOWERCASED at parse.
- Writer `FUN_00967d00` (flush/close `FUN_00967fe0`): count -> names+fields -> dir_off -> `"BNT2"`; the zero-entry output is byte-exactly the stub.
- **Orphan verdict**: no client path writes or opens `Textures\Terrain.bnt`; the patcher does not reference it; it exists in the never-run install => install-time placeholder (origin inferred, not byte-proven from the compressed installer). The iter028 "second provider" hypothesis is REJECTED for 9.3.5.

### (d) id 459344 (0x70060, 129x129) — the detail-texture-id selectors

`FUN_00938da0`: grid = `(pos+0x8000)>>9` (origin -32,768, 512u cells, the center region), index `gx*0x81+gy`, `out[i]` = **tables C/D/E[byte]** at mgr+0xC40/+0x1040/+0x1440 — the R/G/B channels are three per-cell DETAIL-TEXTURE-ID selector grids. Consumers: `FUN_00939900` (the detail-slot filler -> 3x `FUN_006ba110` -> the material's 3 detail slots; callsite 0x00939945; sole caller `FUN_0093f800`) and `FUN_0093eb50` (the CPU bake, x2). This **supersedes** iter027's "the 3 details from the material list": the ids come from the global world-data texture, not the TDF list.

### (e) Delivery-channel verdict

| id | verdict | evidence |
|---|---|---|
| 429259 | **LOCAL** | shipped in both 9.x-era Textures.bnt (identical payload); absent 2003 |
| 432502, 459344 | **PATCHER-delivered** | 178-container scan (89 BNT + 82 VFS + 7 ARK, 3 corpora) = 0 hits; the client fetch is local-only and a miss halts init; the in-client FTP subsystem (FileTransfer:FTP1/FTP2, `FUN_00836060/160/230`, `rp.entropiauniverse.com`) is the post-login content-transfer system, not the resource channel |

Patcher evidence (ClientLoader.exe 9.3.4.5963 + the EU2008-era ClientLoader): WinInet FTP API imports, `ftp.entropiauniverse.com`, `dumps.entropiauniverse.com`, `Index.ajp`/`Update.ajp` endpoints, ArkDownloadJob / DownloadThreadPool / ArkFTPCallbackInterface, CZipArchive + CWildcard (`.ark` packages), `Textures\` + `Textures.bnt` strings plus a "convert textures for 8.9 release" migration path, `Download.data` = `1 PE_PCG.ark`, `ClientFiles.txt` ark manifest.

**Clean-runtime implication (era-honest)**: the 257x257 height payload and the full mechanism chain are reproducible locally; the climate bytes (432502) and detail selectors (459344) are NOT locally available in any scanned container and must stay MISSING/ERA-BOUNDED in the clean runtime (no proxy as historical truth). Resume point: a patcher-updated Textures.bnt of the era, or a runtime capture (post-M1, human-gated).

### Secondary (bounded)

The field is a full-planet height model, mostly land everywhere (79.2% land >0m full-world, mean +79.2m; center region 77.1%/+73.2m; east band 92.6%/+137.1m; south band 66.4%/+22.5m) — the center region is not specially landy; the climate/detail grids covering only the center 65,536u is a mapping choice of the era's default world. The iter028 georef bound (r=0.527 saturation vs the 2003 map) stands.

## Honest bounds

bank[1]/bank[2] (the 257 G/B float decodes) and bank[5] (the 65x65 B selector) consumers unresolved; `FUN_00941f10`/`FUN_00941f90` +0x20 reads ambiguous (different base object); the stub's install-time writer inferred, not byte-proven; the runtime id[0] default (`FUN_0044c950`) not decompiled; the patcher-side write path into Textures.bnt not RE'd (strings/imports evidence is the bound). Both the 9.2.2.2 and 9.3.5 shipped containers lack the climate texture — both eras required the patcher-delivered ids to run.
