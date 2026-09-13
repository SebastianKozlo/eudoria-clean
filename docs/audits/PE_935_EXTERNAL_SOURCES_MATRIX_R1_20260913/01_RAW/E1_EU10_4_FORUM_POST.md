# E1 — Entropia Universe Forum: "Verification data for Entropia Universe 10.4.0.36604"

- URL: https://forum.entropiauniverse.com/t/verification-data-for-entropia-universe-10-4-0-36604/144631
- Read date: 2026-09-13 (live fetch, HTTP 200)
- AUTHOR: forum user **"Wody"** (https://forum.entropiauniverse.com/u/Wody), posted **November 25, 2009, 2:56pm**. NOT a MindArk official account — a player-generated SFV (QuickSFV v2.36, generated 2009-11-25 on the poster's own installation) for install-integrity checking after the 10.4.0.36604 update problems.
- Thread: Planet Calypso → technical; Discourse forum ("Powered by Discourse").

## Claimed values — VERIFIED VERBATIM from the SFV listing

| Claimed | Source value | Match |
|---|---|---|
| data\client\shared\platform\Parameters\templates.vfs = 610,576 B | `; 610576 01:16.16 2009-11-25 data\client\shared\platform\Parameters\templates.vfs` | EXACT |
| Sectors.xbc = 129 B | `; 129 02:47.33 2009-11-17 data\client\Sectors.xbc` | EXACT |
| ResourcePaths.xbc present | `; 64028 01:13.06 2009-11-17 data\client\shared\platform\ResourcePaths.xbc` | YES (64,028 B) |
| Objects.pak present | `data\client\shared\calypsoshared\Objects.pak` (75,091,884 B), `...\item\Objects.pak` (58,448,644), `...\platform\Objects.pak` (65,028,231), `...\territories\calypsosystem\Objects.pak` (119,935,055) | YES (4 instances) |
| Parameters.pak present | calypsoshared (7,896), item (40,766), platform (2,264), sectors\0001_CalypsoSystem (680), territories\calypsosystem (46,740) | YES (5 instances) |
| Terrain0.pak | `...territories\calypsosystem\Terrain0.pak` = 1,197,363,457 B | YES |
| Terrain1.pak | `...territories\calypsosystem\Terrain1.pak` = 1,252,214,116 B | YES |
| Planets.pak | `...territories\calypsosystem\Planets.pak` = 11,608,310 B | YES |
| textures.vfs present | `Parameters\textures.vfs` = 1,552 B | YES |
| videos.vfs present | `Parameters\videos.vfs` = 3,856 B | YES |
| names.vfs present | `Strings\English\names.vfs` = 499,216 B (+ French/German/Spanish) | YES |
| strings.vfs present | `Strings\English\strings.vfs` = 422,608 B (+ French/German/Spanish) | YES |

Additional files in the same listing (context): Entropia.exe 15,452,312 B (bin32, 2009-11-25, CRC 82C6F7CE), GameData.pak / Sounds.pak / Textures.pak / Music.pak / Shaders.pak / ShaderCache.pak / UI.pak / Animations.pak per layer; Parameters\20001-20043.vfs series + hierarchy.vfs + sids.vfs (157,968 B); sector dir `sectors\0001_CalypsoSystem\Parameters.pak`.

## E2 — LIMITATIONS (mandated by the contract)

1. **Sectors.xbc = 129 bytes is NOT proof of a complete placement table.** A 129-byte file cannot hold a world placement table; the size alone proves only the file existed with that size in this install. No content semantics are evidenced.
2. **Filename continuity ≠ format/ID/semantics continuity.** The fact that `Parameters\templates.vfs` exists in 10.4 (610,576 B) and existed in 9.3.5 does NOT prove the record layout, the field-A meaning, or the ID space are the same across versions. Cross-build structural comparison remains UNVERIFIED.
3. **A user post is not an official specification.** The SFV listing is a player's CRC manifest for install verification; it carries no MindArk statement about file roles, formats, or data semantics.

## E3 — EU1030 boundary

Per contract E3: no interaction with EU1030 session work — none performed. This run read ONLY the public forum page; no local files of the 10.x corpus were touched.
