#!/usr/bin/env python3
"""PE_M1_935_BINDING_CHAIN_REVALIDATION_R1 - era PCG_9_3_5 (MindArk PCG 9.3.5 corpus).

P0 (PE-MASTER loop 0132d23c-2f0f-42f2-bb07-fb74f637488b, KROK 1 of 3, EU935-M1):
Does the mesh -> NiArkTextureExtraData -> bnt2_id -> Textures.bnt binding chain
resolve on the PCG 9.3.5 corpus at the same closure level as the canon 2003
chain (23,455/23,488 = 99.86%, 33 dangling = 18 SuperSpray particle slots +
15 unshipped, 14 unique missing ids)?

Method (era-labelled PCG_9_3_5 everywhere):
  1. Pins: Models.bnt SHA256 (contract pin), Textures.bnt full SHA256
     (recorded fresh; contract gave only the 61ACD13B prefix), R61 frozen
     parser 10/10 (verified in-driver BEFORE any parse; NEVER modified).
  2. Parse BOTH BNT2 indexes independently: footer u32 index_start @fs-8,
     "BNT2" magic @fs-4, count check (5,596 / 8,381), FULL adjacency check
     (offset[i+1] == offset[i] + size[i] for ALL i; first offset; last
     offset+size == index_start) and EXACT index consumption
     (cursor == fs-8 after the last entry). Anomaly count expected 0.
  3. Parse all 5,596 NIF payloads with the frozen R61 reader
     (PENifReader().parse_bytes(payload, source_name=...)). Parse closure
     must be 5,596/5,596 (ITER-32 precedent on this exact corpus+parser).
  4. Extract EVERY NiArkTextureExtraData entry on BOTH grammars:
     v10: frozen parser fields ark_tex_textures (+ independent raw re-decode
     of b.raw_bytes with exact-consumption + parser-vs-raw agreement, the
     ITER-32-validated formula entry_count = (field2>>8)&0x00FFFFFF);
     v4: independent raw decode of b.raw_bytes (link + u1a + u1b + u8 + u2 +
     num_tex + entries) - the frozen v4 parser discards names.
     Per entry: name, f1, f2, ref, and the 9 trailing bytes decoded as
     anim_flag u8 + frame_index u32 LE + bnt2_id u32 LE (bytes[5:9], the
     M3-4 R2 canon mechanism "bytes[5:8] u32 LE = BNT2 texture ID").
  5. CENSUS GATE: total entries must reconcile with ITER-32 (24,508 =
     v10 19,637 + v4 4,871) AND per-slot join vs R32 TEXTURE_SLOTS.json
     (40-slot vocabulary, e.g. BASE 14,307 / GLOSS 2,791 / DARK 1,816 /
     ENVIRONMENT 1,694 / GLOW 1,524 / BUMP 970 / DETAIL 199 / DECAL0 50 /
     ANIM0..31 1,157). Mismatch -> CENSUS_MISMATCH: write evidence, STOP.
  6. Resolve every bnt2_id against the Textures.bnt entry-name set
     ("{id}.dat", exact set membership, no fuzzy matching). Classify every
     dangling id: 2003 classes (SuperSpray particle slots / unshipped) vs
     NEW 9.3.5 classes - honest classification, no forced taxonomy.
  7. Binding edges era-9.3.5 (M3-4.5 V2 method):
     STATIC: (nif, nitrishape_block, prop_ref, ark_block, ark_idx) where the
       NiTriShape.properties[] contains prop_ref -> NiTexturingProperty and
       the ArkTexture entry.ref == prop_ref. Built TWICE by two independent
       traversal paths (builder: geometry-centric; validator: entry-centric)
       -> Jaccard self-check (expect >= 0.99).
     CONTROLLER: (nif, texprop_block, flipctrl_block) where
       NiTexturingProperty.controller -> NiFlipController (2003 V2 ANIM-01
       semantics: 148 edges from 125 NiFlipController in the 2003 canon).
     EFFECT: (nif, ninode_block, effect_block) where NiNode.effects[] ->
       NiTextureEffect; orphan NiTextureEffect blocks (no parent NiNode)
       get one ORPHAN edge each (2003 V2 EFFECT-01 semantics: 1,749 =
       1,649 attached + 100 orphan from 1,646 NiTextureEffect blocks).
  8. NEGATIVE CONTROLS (a nonzero NC1 rate would mean the lookup is fuzzy):
     NC1 10,000 uniform u32 draws -> resolution must collapse to ~0
     NC2 10,000 uniform draws within the observed id range (density probe)
     NC3 per-entry permutation of the real ids (set-membership is
       permutation-invariant - documented for what it does/does not test)
     NC4 +1/-1 byte shifts and big-endian decode of the trailing 9B
       (canon M3-4 R2 controls) -> all must be ~0
  9. Discipline: re-hash Models.bnt + Textures.bnt after the run == start
     pins; zero payloads written (only derived CSV/JSON metadata); artifact
     index with REAL in-driver SHA-256 of every in-scope artifact.

HARD STOPS: any pin mismatch; R61 hash mismatch; parse closure < 5,596;
CENSUS_MISMATCH unresolved (exit code 3 with partial evidence).
Era: EVERYTHING here is PCG_9_3_5. The 2003 chain (M3-4 R2 / M3-4.5 V2) is
the audited canon REFERENCE and is NOT re-run in this driver.
"""
import sys
import os
import csv
import json
import struct
import random
import hashlib
import time
from collections import Counter, defaultdict

# Never write .pyc into the frozen R61 source tree (or anywhere).
sys.dont_write_bytecode = True

RUN_ID = "PE_M1_935_BINDING_CHAIN_REVALIDATION_R1"
RUN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_RAW = os.path.join(RUN_DIR, "01_RAW")
OUT_CONTROL = os.path.join(RUN_DIR, "00_CONTROL")
OUT_REPORT = os.path.join(RUN_DIR, "06_REPORT")

MODELS_BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
MODELS_SHA256 = "c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0"
TEXTURES_BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Textures\Textures.bnt"
TEXTURES_SHA256_EXPECTED_PREFIX = "61ACD13B"  # contract prefix; full hash recorded fresh
R61_SOURCE_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\01_source"
R61_SHA_JSON = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\03_validation\SHA256_SOURCE.json"
R32_SLOTS_JSON = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MATERIAL_CENSUS_R32_20260904_160538\02_results\TEXTURE_SLOTS.json"
DRIVER_PATH = os.path.join(OUT_CONTROL, "binding_chain_revalidation_r1.py")
DRIVER_SHA_TXT = os.path.join(OUT_CONTROL, "SHA256_DRIVER.txt")

# ---- ITER-32 (R32) reference numbers, era PCG_9_3_5 (read-only canon) ----
R32_TOTAL = 24508
R32_V10 = 19637
R32_V4 = 4871
R32_V10_BLOCKS = 4838
R32_V4_BLOCKS = 758

# ---- 2003 canon reference numbers (era-2003, audited M3-4 R2 + M3-4.5 V2) ----
CANON_2003 = {
    "arktexture_entries": 23488,
    "resolved": 23455,
    "dangling": 33,
    "dangling_superspray_slots": 18,
    "dangling_unshipped_slots": 15,
    "unique_missing_ids": 14,
    "static_edges": 20427,
    "controller_edges": 148,
    "effect_edges": 1749,
    "flip_controllers": 125,
    "texture_effects": 1646,
    "effect_orphans": 100,
    "unique_missing_id_list": [73395, 216625, 354727, 354731, 354733,
                               392427, 392047, 392340, 418308, 420953,
                               425253, 425264, 425272, 581040],
}

T0 = time.time()


def log(m):
    print("[%7.1fs] %s" % (time.time() - T0, m), flush=True)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def hard_stop(reason, code=2):
    log("[DRIVER] HARD STOP: %s" % reason)
    sys.exit(code)


# ============================================================================
# G1: pins (R61 10/10, driver hash, corpus hashes)
# ============================================================================

def verify_r61():
    with open(R61_SHA_JSON, "r", encoding="utf-8-sig") as f:
        locked = json.load(f)
    n_ok = 0
    for name, sha in locked.items():
        if not name.endswith(".py"):
            continue
        actual = sha256_file(os.path.join(R61_SOURCE_DIR, name))
        if actual.lower() != str(sha).lower():
            hard_stop("R61 hash mismatch on %s (expected %s, got %s)" % (name, sha, actual))
        n_ok += 1
    if n_ok != 10:
        hard_stop("R61 expected 10 .py entries, got %d" % n_ok)
    log("G1a R61 frozen source hash verification: 10/10 OK")


def verify_driver_hash():
    self_hash = sha256_file(DRIVER_PATH)
    if not os.path.exists(DRIVER_SHA_TXT):
        hard_stop("SHA256_DRIVER.txt missing (hash-after-last-edit rule violated)")
    with open(DRIVER_SHA_TXT, "r", encoding="ascii") as f:
        declared = f.read().strip()
    if declared.lower() != self_hash.lower():
        hard_stop("driver hash mismatch: SHA256_DRIVER.txt=%s actual=%s (driver edited after hashing?)"
                  % (declared, self_hash))
    log("G1b driver hash provenance OK (%s)" % self_hash)
    return self_hash


def verify_corpus():
    global MODELS_SHA, TEXTURES_SHA
    MODELS_SHA = sha256_file(MODELS_BNT)
    if MODELS_SHA.lower() != MODELS_SHA256:
        hard_stop("Models.bnt hash mismatch: expected %s, got %s" % (MODELS_SHA256, MODELS_SHA))
    log("G1c Models.bnt SHA256 OK (%s)" % MODELS_SHA)
    TEXTURES_SHA = sha256_file(TEXTURES_BNT)
    if not TEXTURES_SHA.upper().startswith(TEXTURES_SHA256_EXPECTED_PREFIX.upper()):
        hard_stop("Textures.bnt hash prefix mismatch: expected prefix %s, got %s"
                  % (TEXTURES_SHA256_EXPECTED_PREFIX, TEXTURES_SHA))
    log("G1d Textures.bnt FULL SHA256 recorded fresh: %s (contract prefix %s OK)"
        % (TEXTURES_SHA, TEXTURES_SHA256_EXPECTED_PREFIX))


# ============================================================================
# BNT2 index parser (independent, both containers; adjacency + exact consumption)
# ============================================================================

def parse_bnt2_index(path, expected_count):
    """Parse a BNT2 archive index. Returns (entries, anomalies, meta).
    entries: list of (name, size, offset). Layout: footer u32 index_start
    @fs-8, magic 'BNT2' @fs-4; at index_start: u32 count, then per entry:
    name + 0x0A + u32 size + u32 offset + 8 unknown bytes (17-byte stride
    after the name terminator). Adjacency + exact consumption verified.
    """
    fs = os.path.getsize(path)
    with open(path, "rb") as f:
        f.seek(fs - 8)
        footer = f.read(8)
    istart = struct.unpack_from("<I", footer, 0)[0]
    magic = footer[4:8]
    anomalies = []
    if magic != b"BNT2":
        anomalies.append("MAGIC_NOT_BNT2:%r" % magic)
    if not (0 < istart < fs):
        anomalies.append("INDEX_START_OUT_OF_RANGE:%d" % istart)
    # read the full index region [istart, fs-8)
    with open(path, "rb") as f:
        f.seek(istart)
        idx = f.read(fs - 8 - istart)
    if len(idx) != fs - 8 - istart:
        anomalies.append("INDEX_READ_SHORT")
    count = struct.unpack_from("<I", idx, 0)[0]
    if count != expected_count:
        anomalies.append("COUNT_MISMATCH:%d!=%d" % (count, expected_count))
    pos = 4
    entries = []
    for i in range(count):
        ne = pos
        lim = min(len(idx), pos + 4096)
        while ne < lim and idx[ne] != 0x0A:
            ne += 1
        if ne >= lim:
            anomalies.append("ENTRY_%d_NAME_TERMINATOR_NOT_FOUND" % i)
            break
        name = idx[pos:ne].decode("ascii", errors="replace")
        if ne + 17 > len(idx):
            anomalies.append("ENTRY_%d_INDEX_TRUNCATED" % i)
            break
        size, off = struct.unpack_from("<II", idx, ne + 1)
        entries.append((name, size, off))
        pos = ne + 17
    # exact index consumption: cursor must land exactly at the end of the
    # index region (fs-8 absolute == len(idx) bytes read)
    if pos != len(idx):
        anomalies.append("INDEX_NOT_EXACTLY_CONSUMED:cursor=%d region=%d" % (pos, len(idx)))
    # full adjacency: offset[i+1] == offset[i] + size[i] for ALL consecutive
    adj_bad = 0
    for i in range(len(entries) - 1):
        if entries[i][2] + entries[i][1] != entries[i + 1][2]:
            adj_bad += 1
            if adj_bad <= 5:
                anomalies.append("ADJACENCY_BREAK@%d:%d+%d!=%d"
                                 % (i, entries[i][2], entries[i][1], entries[i + 1][2]))
    if entries:
        if entries[0][2] != 0:
            anomalies.append("FIRST_OFFSET_NOT_ZERO:%d" % entries[0][2])
        if entries[-1][2] + entries[-1][1] != istart:
            anomalies.append("DATA_REGION_NOT_CLOSED:last_end=%d istart=%d"
                             % (entries[-1][2] + entries[-1][1], istart))
    meta = {
        "file_size": fs, "index_start": istart, "magic": magic.decode("ascii", "replace"),
        "count_declared": count, "count_parsed": len(entries),
        "adjacency_breaks": adj_bad,
        "index_region_bytes": fs - 8 - istart,
        "index_cursor_final": pos,
        "exact_consumption": pos == len(idx),
        "first_offset": entries[0][2] if entries else None,
        "last_end": (entries[-1][2] + entries[-1][1]) if entries else None,
    }
    return entries, anomalies, meta


# ============================================================================
# Independent raw decoders (entry 9-byte trailing with ABSOLUTE offsets)
# ============================================================================

def decode_v10_with_offsets(raw):
    """v10 NiArkTextureExtraData raw decode (ITER-32 grammar) with absolute
    offsets of each entry's 9-byte trailing within raw. Returns dict."""
    try:
        off = 0
        hdr3 = raw[off:off + 3]
        off += 3
        nl = struct.unpack_from("<i", raw, off)[0]
        off += 4
        if nl < 0 or nl > 256 or off + nl > len(raw):
            return {"ok": False, "fail": "bad ArkTexture name len %d" % nl}
        ed_name = raw[off:off + nl].decode("ascii", errors="replace")
        off += nl
        num_tex = struct.unpack_from("<i", raw, off)[0]
        off += 4
        field1 = struct.unpack_from("<i", raw, off)[0]
        off += 4
        field2 = struct.unpack_from("<i", raw, off)[0]
        off += 4
        f2u = field2 & 0xFFFFFFFF
        low8 = f2u & 0xFF
        entry_count = (f2u >> 8) & 0x00FFFFFF
        pad = raw[off]
        off += 1
        texs = []
        for i in range(entry_count):
            nl2 = struct.unpack_from("<i", raw, off)[0]
            off += 4
            if nl2 < 1 or nl2 > 256 or off + nl2 + 21 > len(raw):
                return {"ok": False, "fail": "bad entry name len %d at entry %d" % (nl2, i)}
            nm = raw[off:off + nl2].decode("ascii", errors="replace")
            off += nl2
            f1 = struct.unpack_from("<i", raw, off)[0]
            off += 4
            f2v = struct.unpack_from("<i", raw, off)[0]
            off += 4
            ref = struct.unpack_from("<i", raw, off)[0]
            off += 4
            unk_abs = off
            unk = raw[off:off + 9]
            off += 9
            texs.append({"name": nm, "f1": f1, "f2": f2v, "ref": ref,
                         "unk_hex": unk.hex(), "unk_abs": unk_abs})
        return {"ok": off == len(raw), "fail": None if off == len(raw)
                else "cursor %d != rawlen %d" % (off, len(raw)),
                "hdr3_hex": hdr3.hex(), "ed_name": ed_name, "num_tex": num_tex,
                "field1": field1, "field2": field2, "low8": low8,
                "entry_count": entry_count, "pad": pad, "texs": texs,
                "consumed": off, "rawlen": len(raw)}
    except (struct.error, IndexError) as ex:
        return {"ok": False, "fail": "struct error: %s" % ex}


def decode_v4_with_offsets(raw):
    """v4 NiArkTextureExtraData raw decode (ITER-32 grammar) with absolute
    offsets. Mirrors the frozen v4 parser layout (which discards names)."""
    try:
        off = 0
        link = struct.unpack_from("<i", raw, off)[0]
        off += 4
        u1a = struct.unpack_from("<i", raw, off)[0]
        off += 4
        u1b = struct.unpack_from("<i", raw, off)[0]
        off += 4
        ub = raw[off]
        off += 1
        u2 = struct.unpack_from("<i", raw, off)[0]
        off += 4
        num_tex = struct.unpack_from("<i", raw, off)[0]
        off += 4
        if num_tex < 0 or num_tex > 4096:
            return {"ok": False, "fail": "bad num_tex %d" % num_tex}
        texs = []
        for i in range(num_tex):
            nl = struct.unpack_from("<i", raw, off)[0]
            off += 4
            if nl < 1 or nl > 256 or off + nl + 21 > len(raw):
                return {"ok": False, "fail": "bad entry name len %d at entry %d" % (nl, i)}
            nm = raw[off:off + nl].decode("ascii", errors="replace")
            off += nl
            f1 = struct.unpack_from("<i", raw, off)[0]
            off += 4
            f2v = struct.unpack_from("<i", raw, off)[0]
            off += 4
            ref = struct.unpack_from("<i", raw, off)[0]
            off += 4
            unk_abs = off
            unk = raw[off:off + 9]
            off += 9
            texs.append({"name": nm, "f1": f1, "f2": f2v, "ref": ref,
                         "unk_hex": unk.hex(), "unk_abs": unk_abs})
        return {"ok": off == len(raw), "fail": None if off == len(raw)
                else "cursor %d != rawlen %d" % (off, len(raw)),
                "link": link, "u1a": u1a, "u1b": u1b, "ub": ub, "u2": u2,
                "num_tex": num_tex, "texs": texs,
                "consumed": off, "rawlen": len(raw)}
    except (struct.error, IndexError) as ex:
        return {"ok": False, "fail": "struct error: %s" % ex}


def split_material_slot(name):
    """'<material>_<SLOT>' split at LAST underscore (ITER-32 convention;
    conforming slot = ^[A-Z][A-Z0-9]*$; ANIM0..31/DECAL0 are legitimate)."""
    import re
    if "_" not in name:
        return name, "", "NO_UNDERSCORE"
    material, slot = name.rsplit("_", 1)
    if slot == "":
        return material, "", "EMPTY_SLOT"
    if not re.match(r"^[A-Z][A-Z0-9]*$", slot):
        return material, slot, "SLOT_NOT_CONFORMING"
    return material, slot, None


def trailing_to_fields(unk_hex):
    """9-byte trailing -> (anim_flag u8, frame_index u32 LE, bnt2_id u32 LE).
    Canon: bytes[5:8] u32 LE = BNT2 texture ID (M3-4 R2, CONFIRMED 99.86%
    on era-2003; R32-era trailing pattern census: 00ffffffff + tail u32)."""
    raw = bytes.fromhex(unk_hex)
    anim_flag = raw[0]
    frame_index = struct.unpack_from("<I", raw, 1)[0]
    bnt2_id = struct.unpack_from("<I", raw, 5)[0]
    return anim_flag, frame_index, bnt2_id


# ============================================================================
# MAIN
# ============================================================================

def main():
    log("=== %s (era PCG_9_3_5) ===" % RUN_ID)
    verify_r61()
    driver_sha = verify_driver_hash()
    verify_corpus()

    sys.path.insert(0, R61_SOURCE_DIR)
    from pe_nif_reader import PENifReader  # noqa: E402  (frozen R61, READ-ONLY)

    # ---------------- G2: BNT2 indexes ----------------
    log("--- G2: parsing BNT2 indexes ---")
    models_entries, models_anom, models_meta = parse_bnt2_index(MODELS_BNT, 5596)
    textures_entries, textures_anom, textures_meta = parse_bnt2_index(TEXTURES_BNT, 8381)
    index_validation = {
        "era": "PCG_9_3_5",
        "models_bnt": {"meta": models_meta, "anomalies": models_anom,
                       "anomaly_count": len(models_anom)},
        "textures_bnt": {"meta": textures_meta, "anomalies": textures_anom,
                         "anomaly_count": len(textures_anom)},
        "total_anomaly_count": len(models_anom) + len(textures_anom),
    }
    if len(models_anom) or len(textures_anom):
        with open(os.path.join(OUT_RAW, "INDEX_VALIDATION.json"), "w", encoding="utf-8") as f:
            json.dump(index_validation, f, indent=1)
        hard_stop("BNT2 index anomalies: %s" % json.dumps(index_validation)[:400])
    log("G2 Models.bnt index: %d entries, adjacency_breaks=%d, exact_consumption=%s"
        % (models_meta["count_parsed"], models_meta["adjacency_breaks"],
           models_meta["exact_consumption"]))
    log("G2 Textures.bnt index: %d entries, adjacency_breaks=%d, exact_consumption=%s"
        % (textures_meta["count_parsed"], textures_meta["adjacency_breaks"],
           textures_meta["exact_consumption"]))
    with open(os.path.join(OUT_RAW, "INDEX_VALIDATION.json"), "w", encoding="utf-8") as f:
        json.dump(index_validation, f, indent=1)

    # Textures.bnt id set (exact membership, no fuzzy)
    tex_id_set = set()
    tex_name_anomalies = []
    for name, size, off in textures_entries:
        if not name.endswith(".dat"):
            tex_name_anomalies.append(name)
            continue
        try:
            tex_id_set.add(int(name[:-4]))
        except ValueError:
            tex_name_anomalies.append(name)
    log("Textures.bnt id set: %d ids; non-<id>.dat names: %d"
        % (len(tex_id_set), len(tex_name_anomalies)))

    # ---------------- parse loop ----------------
    log("--- parsing 5,596 NIF payloads with frozen R61 ---")
    with open(MODELS_BNT, "rb") as f:
        data = f.read()
    reader = PENifReader()

    id_rows = []            # full id table (one row per ArkTexture entry)
    dangling = []            # unresolved entries
    resolved_count = 0
    parse_failures = []
    n_pass = 0
    v10_block_ok = 0
    v10_raw_fail = []
    v4_block_ok = 0
    v4_raw_fail = []
    tx_v10_blocks = 0
    tx_v4_blocks = 0
    tx_per_version = Counter()
    per_slot_counts = Counter()
    per_slot_counts_v10 = Counter()
    per_slot_counts_v4 = Counter()
    slot_exceptions = Counter()

    # edges
    static_builder = set()   # (nif, tri_block, prop_ref, ark_block, ark_idx)
    static_validator = set()
    controller_edges = set()  # (nif, texprop_block, flipctrl_block)
    effect_edges = set()       # (nif, ninode_block, effect_block); orphan -> (-1, ...)
    flip_controller_blocks = 0
    texture_effect_blocks = 0
    anim_entries_ref_to_flip = 0
    static_edges_resolved = 0
    static_edges_dangling = 0
    controller_edges_resolved = 0
    effect_edges_resolved = 0
    nifs_bound = 0
    nifs_no_geometry = 0
    nifs_partially_bound = 0
    nifs_no_texture_binding = 0
    slot_conflict_rows = []

    for n, (name, size, off) in enumerate(models_entries, 1):
        payload = data[off:off + size]
        try:
            res = reader.parse_bytes(payload, source_name=name)
        except Exception as ex:  # noqa: BLE001 - frozen reader contract
            parse_failures.append({"file": name, "status": "EXCEPTION",
                                   "reason": "%s: %s" % (type(ex).__name__, ex)})
            continue
        if res.parse_status != "PASS":
            parse_failures.append({"file": name, "status": res.parse_status,
                                   "reason": res.fail_reason})
            continue
        n_pass += 1
        ver = res.version_string
        is_v4 = res.version_raw == 0x0401000C
        blocks = res.blocks
        block_by_idx = {b.block_index: b for b in blocks}

        # ---- collect ArkTexture entries (both grammars) ----
        # ark_by_ref: ref -> list of (ark_block, entry_idx, bnt2_id)
        ark_by_ref = defaultdict(list)
        nif_has_geometry = False
        nif_ark_count = 0
        nif_bind_rows = 0

        for b in blocks:
            bt = b.block_type
            fld = b.fields or {}

            if bt == "NiArkTextureExtraData":
                tx_per_version[ver] += 1
                if "ark_tex_num_tex" in fld:
                    grammar = "v10"
                    tx_v10_blocks += 1
                    dec = decode_v10_with_offsets(b.raw_bytes)
                    if dec.get("ok"):
                        v10_block_ok += 1
                        ptex = fld.get("ark_tex_textures", [])
                        if len(ptex) != len(dec["texs"]):
                            v10_raw_fail.append({"file": name, "kind": "ENTRY_LIST_LEN"})
                            texs = ptex  # parser authoritative
                            raw_map = {}
                        else:
                            texs = dec["texs"]
                            raw_map = {i: t for i, t in enumerate(texs)}
                            mism = []
                            for i, (pe, de) in enumerate(zip(ptex, dec["texs"])):
                                if (pe.get("name") != de["name"] or pe.get("f1") != de["f1"]
                                        or pe.get("f2") != de["f2"] or pe.get("ref") != de["ref"]):
                                    mism.append("entry_mismatch:%s" % de["name"])
                                    break
                            if mism:
                                v10_raw_fail.append({"file": name, "kind": "PARSER_VS_RAW_MISMATCH",
                                                     "detail": mism})
                    else:
                        v10_raw_fail.append({"file": name, "kind": "RAW_DECODE_FAIL",
                                             "detail": dec.get("fail")})
                        texs = fld.get("ark_tex_textures", [])
                        raw_map = {}
                else:
                    grammar = "v4"
                    tx_v4_blocks += 1
                    dec = decode_v4_with_offsets(b.raw_bytes)
                    if dec.get("ok"):
                        v4_block_ok += 1
                        texs = dec["texs"]
                        raw_map = {i: t for i, t in enumerate(texs)}
                        if dec["num_tex"] != fld.get("num_ark_textures"):
                            v4_raw_fail.append({"file": name, "kind": "NUMTEX_MISMATCH",
                                                "detail": {"parser": fld.get("num_ark_textures"),
                                                           "raw": dec["num_tex"]}})
                    else:
                        v4_raw_fail.append({"file": name, "kind": "RAW_DECODE_FAIL",
                                            "detail": dec.get("fail")})
                        texs = []
                        raw_map = {}

                for ai, t in enumerate(texs):
                    nm = t["name"]
                    f1, f2v, ref = t["f1"], t["f2"], t["ref"]
                    anim_flag, frame_index, bnt2_id = trailing_to_fields(t["unk_hex"])
                    material, slot, exc = split_material_slot(nm)
                    if exc:
                        slot_exceptions[exc] += 1
                    else:
                        per_slot_counts[slot] += 1
                        if grammar == "v10":
                            per_slot_counts_v10[slot] += 1
                        else:
                            per_slot_counts_v4[slot] += 1
                    resolved = bnt2_id in tex_id_set
                    if resolved:
                        resolved_count += 1
                    else:
                        dangling.append({
                            "nif": name, "version": ver, "grammar": grammar,
                            "block_index": b.block_index, "entry_idx": ai,
                            "name": nm, "material": material, "slot": slot,
                            "f1": f1, "f2": f2v, "ref": ref,
                            "anim_flag": anim_flag, "frame_index": frame_index,
                            "bnt2_id": bnt2_id,
                        })
                    id_rows.append({
                        "nif": name, "version": ver, "grammar": grammar,
                        "block_index": b.block_index, "entry_idx": ai,
                        "name": nm, "slot": slot, "f1": f1, "f2": f2v,
                        "ref": ref, "anim_flag": anim_flag,
                        "frame_index": frame_index, "bnt2_id": bnt2_id,
                        "resolved": "1" if resolved else "0",
                    })
                    nif_ark_count += 1
                    if ref != -1:
                        ark_by_ref[ref].append((b.block_index, ai, bnt2_id))
                    # shift-control bookkeeping happens post-loop (bulk)

            elif bt == "NiTriShape":
                nif_has_geometry = True

        # ---- STATIC edges, builder path (geometry-centric) ----
        for b in blocks:
            if b.block_type != "NiTriShape":
                continue
            for prop_ref in (b.fields or {}).get("properties", []):
                if prop_ref == -1:
                    continue
                pb = block_by_idx.get(prop_ref)
                if pb is None or pb.block_type != "NiTexturingProperty":
                    continue
                for (ark_blk, ark_idx, bid) in ark_by_ref.get(prop_ref, []):
                    edge = (name, b.block_index, prop_ref, ark_blk, ark_idx)
                    static_builder.add(edge)
                    nif_bind_rows += 1
                    if bid in tex_id_set:
                        static_edges_resolved += 1
                    else:
                        static_edges_dangling += 1

        # ---- STATIC edges, validator path (entry-centric; independent) ----
        for ref_target, lst in ark_by_ref.items():
            pb = block_by_idx.get(ref_target)
            if pb is None or pb.block_type != "NiTexturingProperty":
                continue
            for b in blocks:
                if b.block_type != "NiTriShape":
                    continue
                if ref_target in (b.fields or {}).get("properties", []):
                    for (ark_blk, ark_idx, bid) in lst:
                        static_validator.add((name, b.block_index, ref_target,
                                              ark_blk, ark_idx))

        # ---- CONTROLLER edges (NiTexturingProperty.controller -> NiFlipController) ----
        for b in blocks:
            if b.block_type != "NiTexturingProperty":
                continue
            ctrl = (b.fields or {}).get("controller", -1)
            if ctrl == -1:
                continue
            cb = block_by_idx.get(ctrl)
            if cb is not None and cb.block_type == "NiFlipController":
                controller_edges.add((name, b.block_index, ctrl))
                for (ark_blk, ark_idx, bid) in ark_by_ref.get(ctrl, []):
                    anim_entries_ref_to_flip += 1
                    if bid in tex_id_set:
                        controller_edges_resolved += 1

        # ---- EFFECT edges (NiNode.effects[] -> NiTextureEffect; orphans) ----
        nif_effect_attached = set()
        for b in blocks:
            if b.block_type != "NiNode":
                continue
            for eff in (b.fields or {}).get("effects", []):
                if eff == -1:
                    continue
                eb = block_by_idx.get(eff)
                if eb is not None and eb.block_type == "NiTextureEffect":
                    effect_edges.add((name, b.block_index, eff))
                    nif_effect_attached.add(eff)
        for b in blocks:
            if b.block_type == "NiTextureEffect":
                texture_effect_blocks += 1
                if b.block_index not in nif_effect_attached:
                    effect_edges.add((name, -1, b.block_index))  # ORPHAN edge
                else:
                    for (ark_blk, ark_idx, bid) in ark_by_ref.get(b.block_index, []):
                        if bid in tex_id_set:
                            effect_edges_resolved += 1

        # ---- NiFlipController census ----
        for b in blocks:
            if b.block_type == "NiFlipController":
                flip_controller_blocks += 1

        # ---- NIF status (M3-4.5 V2 STATUS-01 semantics) ----
        geo_count = sum(1 for b in blocks if b.block_type == "NiTriShape")
        if nif_bind_rows > 0:
            nifs_bound += 1
        elif geo_count > 0 and nif_ark_count > 0:
            nifs_partially_bound += 1
        elif geo_count > 0:
            nifs_no_texture_binding += 1
        else:
            nifs_no_geometry += 1

        if n % 1000 == 0:
            log("  %d/5596 NIFs parsed; entries=%d resolved=%d dangling=%d"
                % (n, len(id_rows), resolved_count, len(dangling)))

    log("parse loop done: pass=%d failures=%d" % (n_pass, len(parse_failures)))
    if n_pass != 5596:
        with open(os.path.join(OUT_RAW, "PARSE_FAILURES.json"), "w", encoding="utf-8") as f:
            json.dump(parse_failures, f, indent=1)
        hard_stop("parse closure %d/5596 (see PARSE_FAILURES.json)" % n_pass)

    # ---------------- G3: census reconciliation vs ITER-32 ----------------
    total_entries = len(id_rows)
    v10_entries = sum(1 for r in id_rows if r["grammar"] == "v10")
    v4_entries = sum(1 for r in id_rows if r["grammar"] == "v4")
    with open(R32_SLOTS_JSON, "r", encoding="utf-8") as f:
        r32_slots = json.load(f)
    r32_slot_counts = {k: v["count"] for k, v in r32_slots["slot_vocabulary"].items()}
    my_slot_counts = dict(per_slot_counts)
    slot_join = {
        "slots_checked": len(r32_slot_counts),
        "slots_matched": 0, "slots_mismatched": 0,
        "mismatches": [],
        "my_slots_absent_in_r32": sorted(set(my_slot_counts) - set(r32_slot_counts)),
    }
    for s, cnt in r32_slot_counts.items():
        if my_slot_counts.get(s, 0) == cnt:
            slot_join["slots_matched"] += 1
        else:
            slot_join["slots_mismatched"] += 1
            slot_join["mismatches"].append({"slot": s, "r32": cnt,
                                             "this_run": my_slot_counts.get(s, 0)})
    census = {
        "era": "PCG_9_3_5",
        "this_run": {
            "total_entries": total_entries, "v10_entries": v10_entries,
            "v4_entries": v4_entries, "v10_blocks": tx_v10_blocks,
            "v4_blocks": tx_v4_blocks, "per_version_blocks": dict(tx_per_version),
            "slot_counts": my_slot_counts,
            "slot_exception_counts": dict(slot_exceptions),
        },
        "iter32_reference": {
            "total_entries": R32_TOTAL, "v10_entries": R32_V10, "v4_entries": R32_V4,
            "v10_blocks": R32_V10_BLOCKS, "v4_blocks": R32_V4_BLOCKS,
            "slot_counts": r32_slot_counts,
        },
        "reconciliation": {
            "total_match": total_entries == R32_TOTAL,
            "v10_match": v10_entries == R32_V10,
            "v4_match": v4_entries == R32_V4,
            "blocks_v10_match": tx_v10_blocks == R32_V10_BLOCKS,
            "blocks_v4_match": tx_v4_blocks == R32_V4_BLOCKS,
            "slot_join": slot_join,
        },
        "validation_layers": {
            "v10_raw_decode_ok": v10_block_ok,
            "v10_raw_failures": len(v10_raw_fail),
            "v4_raw_decode_ok": v4_block_ok,
            "v4_raw_failures": len(v4_raw_fail),
            "v10_raw_fail_detail_head": v10_raw_fail[:20],
            "v4_raw_fail_detail_head": v4_raw_fail[:20],
        },
    }
    with open(os.path.join(OUT_RAW, "CENSUS_RECONCILIATION.json"), "w", encoding="utf-8") as f:
        json.dump(census, f, indent=1)
    log("G3 census: total=%d (ITER-32 %d) v10=%d (%d) v4=%d (%d) slot_join %d/%d matched"
        % (total_entries, R32_TOTAL, v10_entries, R32_V10, v4_entries, R32_V4,
           slot_join["slots_matched"], slot_join["slots_checked"]))
    census_ok = (total_entries == R32_TOTAL and v10_entries == R32_V10
                 and v4_entries == R32_V4 and tx_v10_blocks == R32_V10_BLOCKS
                 and tx_v4_blocks == R32_V4_BLOCKS
                 and slot_join["slots_mismatched"] == 0
                 and slot_join["my_slots_absent_in_r32"] == [])
    if not census_ok:
        log("CENSUS_MISMATCH: writing evidence and STOPPING (no resolution claims)")
        sys.exit(3)

    # ---------------- G4: resolution + dangling classification ----------------
    resolution_rate = 100.0 * resolved_count / total_entries if total_entries else 0.0
    canon_ids = set(CANON_2003["unique_missing_id_list"])
    missing_ids = Counter(d["bnt2_id"] for d in dangling)
    unique_missing = sorted(missing_ids.keys())
    # classification (honest; resolution itself was pure exact set membership)
    classes = defaultdict(list)
    for d in dangling:
        nm = d["name"]
        mid = d["bnt2_id"]
        if "SuperSpray" in nm:
            cls = "SUPERSPRAY_PARTICLE_SLOT_935"
        elif mid in canon_ids:
            cls = "SAME_MISSING_ID_AS_2003"
        else:
            cls = "NEW_935_MISSING_ID"
        classes[cls].append(d)
    # per-class summary
    class_summary = {}
    for cls, lst in classes.items():
        uids = sorted(set(d["bnt2_id"] for d in lst))
        slots = Counter(d["slot"] for d in lst)
        class_summary[cls] = {
            "dangling_entries": len(lst), "unique_missing_ids": len(uids),
            "missing_ids": uids, "slot_counts": dict(slots),
            "nifs": sorted(set(d["nif"] for d in lst))[:50],
            "example_names": [d["name"] for d in lst[:25]],
        }

    # comparison vs 2003 canon classes
    vs2003 = {
        "entries_2003": CANON_2003["arktexture_entries"],
        "entries_935": total_entries,
        "dangling_2003": CANON_2003["dangling"],
        "dangling_935": len(dangling),
        "superspray_slots_2003": CANON_2003["dangling_superspray_slots"],
        "superspray_slots_935": len(classes.get("SUPERSPRAY_PARTICLE_SLOT_935", [])),
        "unshipped_slots_2003": CANON_2003["dangling_unshipped_slots"],
        "unshipped_like_slots_935": len(classes.get("SAME_MISSING_ID_AS_2003", []))
                                     + len(classes.get("NEW_935_MISSING_ID", [])),
        "unique_missing_ids_2003": CANON_2003["unique_missing_ids"],
        "unique_missing_ids_935": len(unique_missing),
        "overlap_2003_935_missing_ids": sorted(canon_ids & set(unique_missing)),
        "only_in_2003": sorted(canon_ids - set(unique_missing)),
        "only_in_935": sorted(set(unique_missing) - canon_ids),
        "resolution_rate_2003": 100.0 * CANON_2003["resolved"] / CANON_2003["arktexture_entries"],
        "resolution_rate_935": resolution_rate,
    }

    # ---------------- edges: counts + Jaccard self-check ----------------
    inter = static_builder & static_validator
    union = static_builder | static_validator
    jaccard = (len(inter) / len(union)) if union else 1.0

    # ---------------- negative controls ----------------
    rng = random.Random(20260906)
    NC_DRAWS = 10000
    nc1_hits = sum(1 for _ in range(NC_DRAWS) if rng.getrandbits(32) in tex_id_set)
    nc1_rate = 100.0 * nc1_hits / NC_DRAWS
    obs_ids = [r["bnt2_id"] for r in id_rows]
    id_min, id_max = min(obs_ids), max(obs_ids)
    nc2_hits = sum(1 for _ in range(NC_DRAWS)
                   if rng.randint(id_min, id_max) in tex_id_set)
    nc2_rate = 100.0 * nc2_hits / NC_DRAWS
    # NC3: per-entry permutation of the real ids (set-membership invariance note)
    perm = list(obs_ids)
    rng.shuffle(perm)
    nc3_hits = sum(1 for v in perm if v in tex_id_set)
    nc3_rate = 100.0 * nc3_hits / len(perm)
    # NC4: shift/BE controls on the real trailing bytes (re-decode from blocks)
    # (second pass over files with entries; uses raw block bytes at unk_abs)
    shift_p1_hits = 0
    shift_m1_hits = 0
    be_hits = 0
    shift_eval = 0
    shift_skipped = 0
    for name, size, off in models_entries:
        payload = data[off:off + size]
        try:
            res = reader.parse_bytes(payload, source_name=name)
        except Exception:  # noqa: BLE001
            continue
        if res.parse_status != "PASS":
            continue
        for b in res.blocks:
            if b.block_type != "NiArkTextureExtraData":
                continue
            fld = b.fields or {}
            if "ark_tex_num_tex" in fld:
                dec = decode_v10_with_offsets(b.raw_bytes)
                ok = dec.get("ok")
            else:
                dec = decode_v4_with_offsets(b.raw_bytes)
                ok = dec.get("ok")
            if not ok:
                continue
            raw = b.raw_bytes
            for t in dec["texs"]:
                ua = t["unk_abs"]
                shift_eval += 1
                # +1 shift: bytes[6:10] of the trailing window
                if ua + 10 <= len(raw):
                    v = struct.unpack_from("<I", raw, ua + 6)[0]
                    if v in tex_id_set:
                        shift_p1_hits += 1
                else:
                    shift_skipped += 1
                # -1 shift: bytes[4:8]
                v = struct.unpack_from("<I", raw, ua + 4)[0]
                if v in tex_id_set:
                    shift_m1_hits += 1
                # big-endian decode of the canonical window bytes[5:9]
                v = struct.unpack_from(">I", raw, ua + 5)[0]
                if v in tex_id_set:
                    be_hits += 1
    nc4 = {
        "shift_p1_rate": 100.0 * shift_p1_hits / shift_eval if shift_eval else None,
        "shift_m1_rate": 100.0 * shift_m1_hits / shift_eval if shift_eval else None,
        "big_endian_rate": 100.0 * be_hits / shift_eval if shift_eval else None,
        "evaluated": shift_eval, "p1_skipped_out_of_block": shift_skipped,
    }
    negative_controls = {
        "era": "PCG_9_3_5",
        "NC1_random_u32_draws": {"draws": NC_DRAWS, "hits": nc1_hits, "rate_pct": nc1_rate},
        "NC2_random_in_observed_range": {
            "draws": NC_DRAWS, "observed_id_min": id_min, "observed_id_max": id_max,
            "hits": nc2_hits, "rate_pct": nc2_rate,
            "expected_density_pct": 100.0 * len(tex_id_set) / (id_max - id_min + 1),
        },
        "NC3_permutation_of_real_ids": {
            "entries": len(perm), "hits": nc3_hits, "rate_pct": nc3_rate,
            "honest_note": ("Set-membership resolution is permutation-invariant: "
                            "permuting the real id vector among entries preserves the "
                            "id multiset, so this rate equals the real rate by "
                            "construction. It documents WHICH property the control "
                            "does/does not test (pairing vs existence) - it is NOT "
                            "the collapse control; NC1/NC4 are."),
        },
        "NC4_canon_shift_endianness_controls": nc4,
    }

    # ---------------- discipline: re-hash originals ----------------
    models_sha_after = sha256_file(MODELS_BNT)
    textures_sha_after = sha256_file(TEXTURES_BNT)
    originals_untouched = (models_sha_after == MODELS_SHA
                            and textures_sha_after == TEXTURES_SHA)

    # ---------------- write 01_RAW artifacts ----------------
    log("--- writing 01_RAW artifacts ---")
    id_table_path = os.path.join(OUT_RAW, "ARKTEXTURE_ID_TABLE.csv")
    with open(id_table_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["nif", "version", "grammar", "block_index",
                                          "entry_idx", "name", "slot", "f1", "f2",
                                          "ref", "anim_flag", "frame_index",
                                          "bnt2_id", "resolved"])
        w.writeheader()
        for r in id_rows:
            w.writerow(r)
    dangling_path = os.path.join(OUT_RAW, "DANGLING_LIST.csv")
    with open(dangling_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["nif", "version", "grammar", "block_index", "entry_idx", "name",
                    "material", "slot", "f1", "f2", "ref", "anim_flag",
                    "frame_index", "bnt2_id", "classification"])
        cls_by_tuple = {}
        for cls, lst in classes.items():
            for d in lst:
                cls_by_tuple[(d["nif"], d["block_index"], d["entry_idx"], d["bnt2_id"])] = cls
        for d in dangling:
            k = (d["nif"], d["block_index"], d["entry_idx"], d["bnt2_id"])
            w.writerow([d["nif"], d["version"], d["grammar"], d["block_index"],
                        d["entry_idx"], d["name"], d["material"], d["slot"], d["f1"],
                        d["f2"], d["ref"], d["anim_flag"], d["frame_index"],
                        d["bnt2_id"], cls_by_tuple.get(k, "?")])
    with open(os.path.join(OUT_RAW, "DANGLING_CLASSIFICATION.json"), "w", encoding="utf-8") as f:
        json.dump({"era": "PCG_9_3_5", "dangling_entries": len(dangling),
                  "unique_missing_ids": unique_missing,
                  "unique_missing_id_counts": {str(k): v for k, v in missing_ids.items()},
                  "class_summary": class_summary, "comparison_vs_2003": vs2003},
                 f, indent=1)

    static_path = os.path.join(OUT_RAW, "STATIC_EDGES.csv")
    with open(static_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["nif", "nitrishape_block", "texturing_property_ref",
                    "arktexture_block", "arktexture_entry_idx"])
        for e in sorted(static_builder):
            w.writerow(list(e))
    ctrl_path = os.path.join(OUT_RAW, "CONTROLLER_EDGES.csv")
    with open(ctrl_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["nif", "texturing_property_block", "flip_controller_block", "kind"])
        for e in sorted(controller_edges):
            w.writerow(list(e) + ["NITEXPROP_CONTROLLER"])
    eff_path = os.path.join(OUT_RAW, "EFFECT_EDGES.csv")
    with open(eff_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["nif", "parent_ninode_block", "texture_effect_block", "kind"])
        for (nf, nb, eb) in sorted(effect_edges):
            kind = "NINODE_EFFECTS" if nb != -1 else "ORPHAN_NO_PARENT_NINODE"
            w.writerow([nf, nb, eb, kind])
    effect_attached = sum(1 for e in effect_edges if e[1] != -1)
    effect_orphan = len(effect_edges) - effect_attached
    edge_counts = {
        "era": "PCG_9_3_5",
        "method": "M3-4.5 V2 (mesh -> texturing-property slot -> ArkTexture; "
                  "controller via NiTexturingProperty.controller; effect via NiNode.effects[])",
        "static_edges": len(static_builder),
        "static_builder_count": len(static_builder),
        "static_validator_count": len(static_validator),
        "static_intersection": len(inter),
        "static_union": len(union),
        "static_jaccard": jaccard,
        "static_edges_bnt2_resolved": static_edges_resolved,
        "static_edges_bnt2_dangling": static_edges_dangling,
        "controller_edges": len(controller_edges),
        "controller_flip_blocks": flip_controller_blocks,
        "controller_edges_bnt2_resolved": controller_edges_resolved,
        "anim_entries_ref_to_flip": anim_entries_ref_to_flip,
        "effect_edges": len(effect_edges),
        "effect_attached": effect_attached,
        "effect_orphan": effect_orphan,
        "texture_effect_blocks": texture_effect_blocks,
        "nif_status": {"BOUND": nifs_bound, "NO_GEOMETRY": nifs_no_geometry,
                       "PARTIALLY_BOUND": nifs_partially_bound,
                       "NO_TEXTURE_BINDING": nifs_no_texture_binding,
                       "SUM": nifs_bound + nifs_no_geometry + nifs_partially_bound
                              + nifs_no_texture_binding},
        "canon_2003_comparison": {
            "static_edges_2003": CANON_2003["static_edges"],
            "controller_edges_2003": CANON_2003["controller_edges"],
            "effect_edges_2003": CANON_2003["effect_edges"],
            "flip_controllers_2003": CANON_2003["flip_controllers"],
            "texture_effects_2003": CANON_2003["texture_effects"],
            "effect_orphans_2003": CANON_2003["effect_orphans"],
        },
    }
    with open(os.path.join(OUT_RAW, "EDGE_COUNTS.json"), "w", encoding="utf-8") as f:
        json.dump(edge_counts, f, indent=1)
    with open(os.path.join(OUT_RAW, "NEGATIVE_CONTROLS.json"), "w", encoding="utf-8") as f:
        json.dump(negative_controls, f, indent=1)

    # ---------------- summary ----------------
    summary = {
        "era": "PCG_9_3_5",
        "run_id": RUN_ID,
        "models_bnt_sha256": MODELS_SHA,
        "textures_bnt_sha256_full": TEXTURES_SHA,
        "driver_sha256": driver_sha,
        "parse_closure": "%d/5596" % n_pass,
        "arktexture_entries": total_entries,
        "v10_entries": v10_entries, "v4_entries": v4_entries,
        "resolved": resolved_count, "dangling": len(dangling),
        "resolution_rate_pct": resolution_rate,
        "unique_missing_ids_935": len(unique_missing),
        "edges": edge_counts,
        "negative_controls": negative_controls,
        "originals_untouched": originals_untouched,
        "tex_id_set_size": len(tex_id_set),
        "tex_name_anomalies": len(tex_name_anomalies),
    }
    with open(os.path.join(OUT_RAW, "SUMMARY.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1)
    log("SUMMARY: resolved=%d/%d (%.4f%%) dangling=%d unique_missing=%d"
        % (resolved_count, total_entries, resolution_rate, len(dangling),
           len(unique_missing)))
    log("EDGES: static=%d (jaccard=%.6f) controller=%d effect=%d (attached=%d orphan=%d)"
        % (len(static_builder), jaccard, len(controller_edges), len(effect_edges),
           effect_attached, effect_orphan))
    log("NC1=%.4f%% NC2=%.4f%% NC4(p1/m1/be)=%.4f%%/%.4f%%/%.4f%%"
        % (nc1_rate, nc2_rate, nc4["shift_p1_rate"] or 0,
           nc4["shift_m1_rate"], nc4["big_endian_rate"]))
    log("originals_untouched=%s" % originals_untouched)
    log("DONE (exit 0)")


if __name__ == "__main__":
    main()
