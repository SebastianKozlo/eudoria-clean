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
    field_d       — u32   — equals CRC32(payload) in 3,435 entries; differs in
                           2,161 (UNKNOWN — REJECTED: crc32 of 2003-era file
                           (0 hits), crc32c, name-concats, halves, cross-entry
                           matches; possibly a checksum of another build)
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
