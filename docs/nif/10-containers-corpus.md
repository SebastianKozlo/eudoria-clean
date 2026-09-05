# 10 — Containers (BNT2) and corpus manifests

## BNT2 archive format — CONFIRMED (both Models.bnt eras + Textures.bnt)

```
[payload 0][payload 1]...[payload N-1]
[index]
[u32 index_start]   <- last 8 bytes
"BNT2"              <- last 4 bytes

index:
  u32 count
  count × entry:
    name          — variable-length ASCII, 0x0A-terminated (e.g. "23225.nif\n")
    packed_size   — u32   (byte length of the payload)
    offset        — u32   (absolute file offset of the payload)
    field_c       — u32   — **= CRC32(payload) — CONFIRMED 5,596/5,596 (100%, ITER-3)**
    field_d       — u32   — == CRC32(payload) in 3,435 entries; differs in 2,161.
                           REJECTED: crc32 of the 2003-era file (0/2,161), crc32c,
                           name-concats, halves, bitwise-not, crop-variants.
                           LEADING HYPOTHESIS (STRONGLY_SUPPORTED by correlation):
                           d = CRC32 of the file's FIRST-INSERTED version in the
                           archive lineage (build-history marker). Correlations:
                           era-CHANGED files 85% d≠c (182/214); era-IDENTICAL 37%
                           (1,944 — implies pre-2003 content versions we do not
                           have on disk); NEW-ONLY (59xxxx) 80% d==c (139/174).
```

Validated on PCG 9.3.5 Models.bnt: 5,596 entries, index consumed
byte-exact (150,133/150,133), adjacency holds for EVERY entry
(`offset_{i+1} = offset_i + size_i`), zero anomalies. NIF payloads are
stored **uncompressed** (raw NIF bytes, first entry at offset 0).
**field_c gives free per-payload integrity checking for any tool.**

SHA256 (9.3.5 Models.bnt):
`c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0`

IMPORTANT (BNT/BUNT quirk, different family): for the zlib-compressed BNT
terrains, each entry's packedSize spans exactly 8 bytes into the next
entry's record header — strict inflate rejects trailing bytes. This does
NOT affect Models.bnt (payloads uncompressed), but hits any tool that
assumes "packedSize = exact zlib stream length" across BNT families.

## Corpus manifests (machine-generated, this repo)

`corpus/pcg953_nif_manifest.csv` — **one row for every NIF in the 9.3.5
corpus** (5,596 rows), produced by deep-parsing each file with the frozen
R61 parser. Columns:

| Column | Meaning |
|---|---|
| name / size / sha256 | identity (sha256 = payload hash) |
| version / parse_status / num_blocks | structure |
| num_meshes / total_vertices / total_triangles / max_uv_sets | geometry |
| skinned_meshes / max_bones | skinning |
| num_materials / materials | NiMaterialProperty names (`;`-joined) |
| num_textures / textures | ArkTexture + NiSourceTexture names (`;`-joined, deduped) |
| keyframe_controllers / num_text_keys / text_keys | animation |
| ark_anim_variant | NiArkAnimationExtraData variant |
| num_lights / particle_systems / texture_effects / morph_blocks / cameras | content classes |
| block_histogram | JSON: block type → count |

Provenance:
- Generator: `99_Audits\PE_PCG935_NIF_DEEP_DUMP_R1_20260904_114352\01_source\deep_dump_pcg953_r1.py` (SHA256 `8252E5C8...`, hashed before execution)
- Parser: frozen R61 (hashes verified 10/10 before use)
- Full-detail JSONL (every block's parsed fields): stays in the audit dir
  (`02_results\pcg953_nif_full.jsonl`) — too large for this repo.
- Full-corpus parse audit: `99_Audits\PE_PCG935_NIF_CORPUS_AUDIT_R1_20260904_113907\` (5596/5596 PASS, block census 77 types).

Regeneration rule: the manifest is derived documentation — regenerate via
the deep-dump driver after any corpus/parser change (revalidation triggers:
parser change, new corpus, era change, exporter bug discovery).

## Era drift census (ITER-2) — CONFIRMED

Comparing the 5,422 names shared by the 2003 extracted corpus and the 9.3.5
Models.bnt payloads (SHA256 per file):

| Class | Count | % |
|---|---|---|
| byte-identical (same SHA256) | 5,208 | 96.05% |
| re-exported within v10.1.0.0 | 211 | 3.9% |
| upgraded v4.1.0.12 → v10.1.0.0 | 3 | 0.06% |

Evidence: `99_Audits\PE_NIF_ERA_DRIFT_R2_20260904_115051\02_results\`
(ERA_DRIFT_2003_VS_PCG953.csv — one row per shared name;
ERA_DRIFT_SUMMARY.json; driver SHA256 recorded, hashed before execution).

## Cross-era grammar validation (ITER-35) — the FORMAT EVOLUTION TABLE

All grammars confirmed on the 9.3.5 corpus were re-validated byte-exact on
the 2003 corpus (5,426/5,426 parse closure; run
`PE_NIF_CROSS_ERA_R35_20260904_170224`; claim table in
`02_results\FORMAT_EVOLUTION.json`):

**21 claims → 19 ERA-STABLE / 2 EVOLVED / 0 ABSENT / 0 falsifications.**

| Grammar family | 2003 result | Verdict |
|---|---|---|
| G3B record grammar | 1,650/1,650 binary exact (100%); variable-length histogram IDENTICAL incl. the 392 B block; same flag/class enums | ERA-STABLE (ITER-6-rule failure profile EVOLVED: 180 vs 182, same 3 classes) |
| Rare variants (G9_RTTI/G3E/BINARY/SHORT28/G3A_PREAMBLE) | identical block counts (10/4/4/35/6), 100% exact fits both eras | ERA-STABLE |
| Texture slots (40 slots, f1 enum, ANIM frame==slot) | formula 4,665/4,665; v4 decode 761/761; all 40 slots shared; 0/23,488 exceptions; ANIM frame==slot 1,149/1,149 | ERA-STABLE |
| Shader directives (17-name vocabulary) | CRLF grammar 1,741/1,741 CONFIRMED; vocabulary 16/17 — `BaseTexture` ABSENT-in-2003; effect files 10/11 (`1027_BaseBSRGSkin` absent) | **EVOLVED** (content-level) |
| Morph (real-sparse var-k + quantization) | var-k 2,061 spans exact; real-record 1,180/1,457 (81.0% vs 86.2%); strict-00 signature 99.31% with the same gridk profile (2⁻¹⁵..2⁻²²) | ERA-STABLE |
| Importer (version-routed layout + exporter strings) | constants 100%; 14 exact/10 masked patterns count-identical; same 4-string exporter vocabulary; v4 link chain 38/38 NiStringExtraData | ERA-STABLE |

**Conclusion (CONFIRMED): the NIF extension formats are era-stable at the
byte level — across a half-decade corpus gap every byte-exact grammar
reproduces at 100% and the rare-family and importer pattern censuses are
count-identical. The era drift is CONTENT (which directive/effect names
and which records appear), never GRAMMAR.**
