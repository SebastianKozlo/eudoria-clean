#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
PE_NIF_935_SEMANTIC_CORRELATIONS_R1 -- driver (EU935-M1, RUN_CLASS MATERIAL,
era-primary PCG_9_3_5; NO milestone crossing; offline, zero renders).

ONE_PRIMARY_QUESTION: What do four pre-registered offline statistical probes
OBSERVE about the four open NiArk/semantic fields (the importer 3-byte flags;
the ArkTexture field1/field2-low8 two-class joint; the event-registry u32
values; the viewport float families) -- with every result labeled OBSERVED and
any correlation tested against a permuted/base-rate control so nothing
masquerades as semantic proof?

STANDING SENTENCE (carried by every output): correlation outputs are
OBSERVED-level evidence; semantic roles remain runtime-gated (KROK 4 class).

======================= PRE-REGISTRATION (fixed before execution) =======================

Populations (all re-derived fresh from the pinned corpus via the frozen R61
parser; prior census artifacts are read-only reconciliation targets ONLY):

PROBE-1 (importer flags): the 758 v4-class NiArkImporterExtraData blocks
  (files with nif_version != 10.1.0.0; v4 layout link+u1+u2+exporter+3 flag
  bytes; header = raw_bytes[:-38]).
  A = flag3 state (3 classes by header hex tail: "000000"/"0000ff"/"00ffff").
  B candidates (each an independent 10,000-label permutation control on the
  A x B Pearson chi-square):
    B1  nif_version class (4.0.0.0 / 4.0.0.2 / 4.1.0.12)
    B2  exporter string class (the SS after u2)
    B3  mesh-bearing (has >=1 NiTriShape or NiTriStrips block) yes/no
    B4  morph-bearing (has >=1 NiVertexMorphExtraData) yes/no
        [prior canon: 0/758 -- if constant, NO TEST, documented]
    B5  block count class (<=8 / 9-16 / 17-32 / 33-64 / >64)
    B6  geometry size class (total num_triangles summed over
        NiTriShapeData+NiTriStripsData parser fields: 0 / 1-500 /
        501-2000 / 2001-8000 / >8000; AMENDED before the final run: the
        first analyze execution found fully-parsed blocks carry no
        raw_bytes in the frozen R61 parser, so a byte-size measure was
        unavailable; num_triangles is the pre-registered replacement)
    B7  texture entry count class (v4 num_tex: 0 / 1-2 / 3-8 / >8)
    B8  era-mirror (filename present in the 2003 corpus manifest) yes/no
  Constant variables (no variance in the population) are documented as
  "NO TEST (constant ...)" -- not run through the permutation control.
  Verdict per B: "OBSERVED correlation" iff observed chi2 > 95th percentile of
  the 10,000-permuted chi2 distribution; else "NO OBSERVED correlation".
  Also reported (descriptive, labeled OBSERVED): per-A medians/quartiles of
  block count / geometry bytes / entry count.

PROBE-2 (field1 classes): the 4,838 v10-class NiArkTextureExtraData blocks.
  A = two-class joint (field1=1 & low8=0) vs (field1=-256 & low8=255),
  low8 = field2_u32 & 0xFF (R32 formula).
  B candidates (same permutation control):
    B1  entry count class ((field2>>8)&0xFFFFFF: 0 / 1 / 2-3 / 4-8 / >8)
    B2  has BASE slot entry yes/no
    B3  has GLOSS slot yes/no
    B4  has DARK slot yes/no
    B5  has ENVIRONMENT slot yes/no
    B6  has BUMP slot yes/no
    B7  has ANIM slot (ANIM0..ANIM31) yes/no
    B8  NiTextureEffect block present yes/no
    B9  mesh-bearing yes/no
    B10 era-mirror yes/no
  Constants documented without test: num_tex (v10 canon = 3), field2 raw
  packing (= entry_count<<8 | low8; deterministic function of B1 and A).
  Descriptive (labeled OBSERVED): per-class slot-count vectors, entry-count
  histogram by class.

PROBE-3 (event u32): the corpus-wide G3B embedded string registry (all
  NiArkAnimationExtraData blocks with fields ark_variant == "G3B"; records
  decoded with the R30-CONFIRMED fail-closed grammar; expected canon:
  263 strings / 136 string-bearing blocks / 113 zero values).
  A = per-string u32 value interpreted as f32, partition zero / non-zero,
  plus the raw value distribution.
  B = event-name family, pre-registered classification norm() = lowercase +
  strip CR/LF/space/tab:
    MORPH_LR       norm matches ^morph:?(left|right|rifgt)$ (incl. authentic
                   typo 'rifgt', case/spacing variants)
    SOUND_HIT      norm matches ^sound:hit_[0-9]+$
    START_USETOOL  norm starts with "start_usetool:" (subtypes: single
                   effect / single sound / multi-line CRLF combined)
    ANIMCMD_500078 norm starts with "start-name" (the start -name command set)
    END_MORPH1     norm in {"end","morph:1"}
    OTHER          anything else (documented, expected 0)
  Outputs: zero-rate per family; value distribution per family (min/max/
  median/distinct values); permutation control (10,000 label shuffles of the
  zero/non-zero partition) on the family x zero/non-zero chi-square.

PROBE-4 (viewport floats): the NiArkViewportInfoExtraData ext blocks of
  length 85B (592), 121B (79), 43B (11). Float vector = f32 at 4-aligned
  offsets 0,4,... of the ext (R8/R28 convention): 21 / 30 / 10 dims.
  P1 POSITION-STATISTICS (labeled POSITION-STATISTICS, NOT semantics):
  per ext-length class, per position: min/max/mean/median/zero-count/
  distinct-count over the FINITE decoded values, plus n_nonfinite (AMENDED
  before the final run: the first execution found 27/592 85B and 4/79 121B
  vectors carry non-finite 4-aligned bit patterns; sanitization for the
  clustering vectors = non-finite -> 0.0, pre-registered).
  P2 43B sub-class census (pre-registered rule): "parametric" iff any
  |float| > 1e-6 at positions >= 2, else "all_zero_default" (R28 canon).
  P3 k-means clustering, pre-registered: RAW float vectors (no
  standardization), Euclidean; within the 85B class (n=592) for k in 2..5 and
  within the 121B class (n=79) for k in 2..4; restarts=5, max_iter=20,
  RNG seed 20260906; empty clusters re-seeded at the farthest point from
  its own centroid (AMENDED before the final run: the first execution
  collapsed to a single cluster without re-seeding); k chosen by
  pre-registered elbow rule = smallest k with inertia(k+1)/inertia(k) >
  0.80, else the largest tested k. 43B (n=11): no k-means (documented;
  sub-class census only).
  P4 cluster (and ext-length class) x file-content-class correlation tests,
  each with the 10,000-label permutation control:
    has mesh / has morph / has skin (NiSkinInstance/NiSkinData/
    NiSkinPartition) / has particle (block type contains 'particle' or
    'psys', case-insensitive) / block count class (<=16 / 17-32 / 33-64 /
    65-128 / >128) / era-mirror; plus ext-length class (85/121/43) x the
    same content classes on the pooled 682-block population.

Control details (pre-registered): Pearson chi-square on the observed r x k
table (zero-marginal rows/columns dropped before the test and documented);
null distribution = 10,000 uniform label permutations of A across the fixed
column partition B (items pre-sorted grouped by B; per replicate
random.shuffle of the A-label list, C-level slice.count recomputation);
report perm_mean/perm_sd/perm_p95/perm_p99 and
p_perm = (1 + #(perm >= obs)) / (N + 1); RNG random.Random(20260906);
separate independent RNG stream per test (seed offset by test index).

HARD STOPS (exit 2, no fixes): R61 hash mismatch; driver-hash provenance
mismatch; corpus hash mismatch; BNT entry count != 5,596; parse closure
< 5,596/5,596; G2 contract-canon census mismatch -> exit 3 CENSUS_MISMATCH
(partial evidence written; investigation required before proceeding).

Phases: --phase extract  (parse corpus -> 01_RAW/EXTRACTION.json)
        --phase analyze  (probes + permutation controls -> 05_ANALYSIS)
        --phase all
"""

import argparse
import csv
import hashlib
import json
import math
import os
import random
import re
import struct
import sys
from collections import Counter, defaultdict

MODELS_BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
MODELS_BNT_SHA256 = "c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0"
R61_SOURCE_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\01_source"
R61_SHA_JSON = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\03_validation\SHA256_SOURCE.json"
MIRROR_2003_CSV = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\02_results\FULL_5426_RESULTS_R61.csv"

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RUN, "01_RAW")
ANALYSIS = os.path.join(RUN, "05_ANALYSIS")
DRIVER_PATH = os.path.abspath(__file__)
DRIVER_SHA_TXT = os.path.join(RUN, "SHA256_DRIVER.txt")
LOG_PATH = os.path.join(RUN, "00_CONTROL", "DRIVER_LOG.txt")

STANDING = ("correlation outputs are OBSERVED-level evidence; semantic roles "
            "remain runtime-gated (KROK 4 class)")

# ---- pre-registered constants ----
SEED = 20260906
N_PERM = 10000
KMEANS_RESTARTS = 5
KMEANS_MAXITER = 20
ELBOW_RATIO = 0.80
GEOM_TYPES = ("NiTriShapeData", "NiTriStripsData")
MESH_NODE_TYPES = ("NiTriShape", "NiTriStrips")
MORPH_TYPES = ("NiVertexMorphExtraData",)
SKIN_TYPES = ("NiSkinInstance", "NiSkinData", "NiSkinPartition")
VIEWPORT_FLOAT_LENS = (85, 121, 43)
VIEWPORT_CENSUS_LENS = (13, 21, 35, 39, 43, 45, 49, 85, 121)

# contract-canon reconciliation targets (G2)
CANON = {
    "flag_states": {"000000": 558, "0000ff": 128, "00ffff": 72},
    "field1_classes": {"1": 3042, "-256": 1796},
    "events": {"strings_total": 263, "string_bearing_blocks": 136,
               "zero_values": 113},
    "viewport": {"13": 2304, "21": 752, "85": 592, "121": 79, "43": 11},
}

_LOG = []


def log(msg):
    line = str(msg)
    print(line, flush=True)
    _LOG.append(line)


def flush_log():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "w", encoding="ascii", errors="replace") as f:
        f.write("\n".join(_LOG) + "\n")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        while True:
            bb = fh.read(1 << 20)
            if not bb:
                break
            h.update(bb)
    return h.hexdigest()


def hard_stop(reason, code=2):
    log("[R1][HARD-STOP] " + reason)
    flush_log()
    raise SystemExit(code)


# ============================================================
# G1 pins
# ============================================================

def verify_pins():
    with open(R61_SHA_JSON, "r", encoding="utf-8-sig") as f:
        locked = json.load(f)
    n_ok = 0
    for name, sha in locked.items():
        if not name.endswith(".py"):
            continue
        actual = sha256_file(os.path.join(R61_SOURCE_DIR, name))
        if actual.lower() != str(sha).lower():
            hard_stop("R61 hash mismatch on %s" % name)
        n_ok += 1
    if n_ok != 10:
        hard_stop("R61 expected 10 .py entries, got %d" % n_ok)
    log("[G1] R61 frozen source hashes: 10/10 OK (READ-ONLY)")
    actual = sha256_file(MODELS_BNT)
    if actual.lower() != MODELS_BNT_SHA256:
        hard_stop("Models.bnt hash mismatch: %s" % actual)
    log("[G1] Models.bnt SHA256 OK (%s)" % actual)
    self_hash = sha256_file(DRIVER_PATH)
    if not os.path.exists(DRIVER_SHA_TXT):
        hard_stop("SHA256_DRIVER.txt missing (hash-after-last-edit rule)")
    with open(DRIVER_SHA_TXT, "r", encoding="ascii") as f:
        declared = f.read().strip()
    if declared.lower() != self_hash.lower():
        hard_stop("driver hash mismatch: SHA256_DRIVER.txt=%s actual=%s"
                   % (declared, self_hash))
    log("[G1] driver hash provenance OK (%s)" % self_hash)
    return True


# ============================================================
# BNT2 index (established pattern)
# ============================================================

def load_bnt_entries(data):
    fs = len(data)
    istart = struct.unpack_from("<I", data, fs - 8)[0]
    count = struct.unpack_from("<I", data, istart)[0]
    if count != 5596:
        hard_stop("BNT entry count = %d, expected 5596" % count)
    pos = istart + 4
    entries = []
    for _ in range(count):
        ne = pos
        while data[ne] != 0x0A:
            ne += 1
        quads = struct.unpack_from("<IIII", data, ne + 1)
        entries.append((data[pos:ne].decode("ascii"), quads[0], quads[1]))
        pos = ne + 17
    return entries


# ============================================================
# raw decoders (independent arithmetic on raw_bytes; cross-checked vs
# the frozen parser fields)
# ============================================================

def decode_importer(raw, file_version):
    """R29 layout. Returns dict or {'ok': False, 'fail': ...}."""
    try:
        header = raw[:-38]
        if file_version == "10.1.0.0":  # v10 class
            nl = struct.unpack_from("<i", header, 0)[0]
            name = header[4:4 + nl].decode("ascii", "replace")
            p = 4 + nl
            imp_int = struct.unpack_from("<i", header, p)[0]
            p += 4
            sl = struct.unpack_from("<i", header, p)[0]
            p += 4
            if sl < 0 or p + sl != len(header):
                return {"ok": False, "fail": "v10 header structure"}
            exporter = header[p:p + sl].decode("ascii", "replace")
            return {"ok": True, "klass": "v10", "name": name,
                    "imp_int": imp_int, "exporter": exporter, "flag3": None}
        # v4 class (all non-10.1.0.0 files)
        link = struct.unpack_from("<i", header, 0)[0]
        u1 = struct.unpack_from("<i", header, 4)[0]
        u2 = struct.unpack_from("<i", header, 8)[0]
        sl = struct.unpack_from("<i", header, 12)[0]
        if sl < 0 or 16 + sl + 3 != len(header):
            return {"ok": False, "fail": "v4 header structure"}
        exporter = header[16:16 + sl].decode("ascii", "replace")
        flag3 = header[16 + sl:16 + sl + 3].hex()
        return {"ok": True, "klass": "v4", "link": link, "u1": u1, "u2": u2,
                "exporter": exporter, "flag3": flag3}
    except (struct.error, IndexError) as ex:
        return {"ok": False, "fail": "struct: %s" % ex}


def decode_v10_texture(raw):
    """R32 v10 layout: 3 zero bytes + 'ArkTexture' SS + num_tex i32 +
    field1 i32 + field2 i32 + pad u8 + entries."""
    try:
        if raw[:3] != b"\x00\x00\x00":
            return {"ok": False, "fail": "3 zero bytes"}
        nl = struct.unpack_from("<i", raw, 3)[0]
        off = 3 + 4
        name = raw[off:off + nl].decode("ascii", "replace")
        off += nl
        num_tex = struct.unpack_from("<i", raw, off)[0]
        field1 = struct.unpack_from("<i", raw, off + 4)[0]
        field2 = struct.unpack_from("<i", raw, off + 8)[0]
        pad = raw[off + 12]
        f2u = field2 & 0xFFFFFFFF
        return {"ok": True, "name": name, "num_tex": num_tex,
                "field1": field1, "field2": field2,
                "low8": f2u & 0xFF,
                "entry_count": (f2u >> 8) & 0x00FFFFFF,
                "pad": pad, "entries_off": off + 13}
    except (struct.error, IndexError) as ex:
        return {"ok": False, "fail": "struct: %s" % ex}


def decode_v4_texture(raw):
    """R32 v4 layout: link + u1a + u1b + ub(u8) + u2 + num_tex + entries."""
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
        for _ in range(num_tex):
            nl = struct.unpack_from("<i", raw, off)[0]
            off += 4
            if nl < 1 or nl > 256 or off + nl + 21 > len(raw):
                return {"ok": False, "fail": "bad entry name len %d" % nl}
            off += nl + 4 + 4 + 4 + 9
        return {"ok": off == len(raw), "fail": None if off == len(raw)
                else "cursor %d != rawlen %d" % (off, len(raw)),
                "link": link, "u1a": u1a, "u1b": u1b, "ub": ub, "u2": u2,
                "num_tex": num_tex, "consumed": off, "rawlen": len(raw)}
    except (struct.error, IndexError) as ex:
        return {"ok": False, "fail": "struct: %s" % ex}


def walk_g3b_records(ext):
    """R30-CONFIRMED grammar, fail-closed. Returns (records, fail_reason)."""
    recs = []
    pos = 0
    while pos < len(ext):
        if len(ext) - pos < 4:
            return None, "trailing bytes at %d" % pos
        size = struct.unpack_from("<I", ext, pos)[0]
        rl = size + 4
        if rl < 33 or pos + rl > len(ext):
            return None, "bad size %d at %d" % (size, pos)
        base = pos + 4
        if ext[base] != 0x02:
            return None, "marker != 02 at %d" % base
        flag = ext[base + 1]
        if flag not in (0x00, 0x01, 0x02):
            return None, "flag enum at %d" % base
        X = struct.unpack_from("<I", ext, base + 2)[0]
        Y = ext[base + 6]
        floats = [struct.unpack_from("<f", ext, base + 7 + 4 * i)[0]
                  for i in range(5)]
        cls = ext[base + 27]
        cnt = ext[base + 28]
        if cls not in (0x00, 0x01):
            return None, "class enum at %d" % (base + 27)
        if cls == 0x01 and cnt > 0:
            return None, "class01_with_strings"
        if cnt > 200:
            return None, "count bound"
        p = base + 29
        strings = []
        for _ in range(cnt):
            e = p
            while e < len(ext) and ext[e] != 0x00:
                c = ext[e]
                if not (0x20 <= c <= 0x7E or c in (0x0D, 0x0A)):
                    return None, "charset at %d" % e
                e += 1
            if e >= len(ext) or e + 5 > len(ext):
                return None, "string overrun at %d" % p
            text = ext[p:e].decode("ascii")
            val = struct.unpack_from("<I", ext, e + 1)[0]
            strings.append({"text": text, "value_u32_hex": "%08x" % val,
                            "value_f32": struct.unpack("<f", struct.pack("<I", val))[0]})
            p = e + 5
        if p != pos + rl:
            return None, "record consumption %d != %d" % (p, pos + rl)
        recs.append({"size": size, "flag": flag, "X": X, "Y": Y,
                     "floats": floats, "class_byte": cls, "count": cnt,
                     "strings": strings})
        pos += rl
    return recs, None


# ============================================================
# EXTRACT phase
# ============================================================

def phase_extract():
    sys.path.insert(0, R61_SOURCE_DIR)
    sys.dont_write_bytecode = True
    from pe_nif_reader import PENifReader  # noqa: E402

    mirror2003 = set()
    with open(MIRROR_2003_CSV, "r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            mirror2003.add(row["filename"])
    log("[extract] 2003 mirror manifest loaded: %d filenames (READ-ONLY)"
        % len(mirror2003))

    with open(MODELS_BNT, "rb") as f:
        data = f.read()
    entries = load_bnt_entries(data)
    log("[extract] BNT2 index: %d entries" % len(entries))

    reader = PENifReader()
    files = []
    parse_status = Counter()
    block_type_census = Counter()
    importer_census = Counter()
    exporter_matrix = Counter()
    g3b_strings = []           # rows for PROBE-3
    viewport_blocks = []        # rows for PROBE-4 (85/121/43 + census classes)
    viewport_len_census = Counter()
    viewport_per_file = Counter()
    anomalies = []
    n = 0
    for name, size, off in entries:
        n += 1
        payload = data[off:off + size]
        res = reader.parse_bytes(payload, source_name=name)
        parse_status[res.parse_status] += 1
        types = Counter(b.block_type for b in res.blocks)
        block_type_census.update(types)
        row = {
            "file": name,
            "version": res.version_string,
            "status": res.parse_status,
            "blocks": len(res.blocks),
            "types": dict(types),
            "mirror": 1 if name in mirror2003 else 0,
        }
        # geometry size (pre-registered PROBE-1 B6 input). NOTE: fully-parsed
        # blocks carry no raw_bytes in the frozen R61 parser (discovered in
        # the first analyze execution); the parser fields num_triangles /
        # num_vertices of NiTriShapeData/NiTriStripsData are the measure.
        geom_blocks = 0
        total_triangles = 0
        total_vertices = 0
        for b in res.blocks:
            if b.block_type in GEOM_TYPES:
                geom_blocks += 1
                fld = b.fields or {}
                total_triangles += int(fld.get("num_triangles") or 0)
                total_vertices += int(fld.get("num_vertices") or 0)
        row["geom_blocks"] = geom_blocks
        row["geom_triangles"] = total_triangles
        row["geom_vertices"] = total_vertices
        # per-block extraction (single pass)
        for b in res.blocks:
            bt = b.block_type
            if bt == "NiArkImporterExtraData":
                d = decode_importer(b.raw_bytes, res.version_string)
                if not d.get("ok"):
                    anomalies.append({"file": name, "kind": "importer",
                                      "fail": d.get("fail")})
                    continue
                importer_census[d["klass"]] += 1
                exporter_matrix[(res.version_string, d["exporter"])] += 1
                row["imp_klass"] = d["klass"]
                row["imp_exporter"] = d["exporter"]
                if d["klass"] == "v4":
                    row["imp_flag3"] = d["flag3"]
                    row["imp_link"] = d["link"]
            elif bt == "NiArkTextureExtraData":
                if res.version_string == "10.1.0.0":
                    d = decode_v10_texture(b.raw_bytes)
                    if not d.get("ok"):
                        anomalies.append({"file": name, "kind": "tex_v10",
                                          "fail": d.get("fail")})
                        continue
                    fld = b.fields or {}
                    # cross-check parser vs raw
                    mism = []
                    if fld.get("ark_tex_field1") is not None and \
                            fld.get("ark_tex_field1") != d["field1"]:
                        mism.append("field1")
                    if fld.get("ark_tex_field2") is not None and \
                            fld.get("ark_tex_field2") != d["field2"]:
                        mism.append("field2")
                    if fld.get("ark_tex_field2_low8") is not None and \
                            fld.get("ark_tex_field2_low8") != d["low8"]:
                        mism.append("low8")
                    if fld.get("ark_tex_num_tex") is not None and \
                            fld.get("ark_tex_num_tex") != d["num_tex"]:
                        mism.append("num_tex")
                    ptex = fld.get("ark_tex_textures", [])
                    if len(ptex) != d["entry_count"]:
                        mism.append("entry_count:%d!=%d"
                                    % (len(ptex), d["entry_count"]))
                    if mism:
                        anomalies.append({"file": name, "kind": "tex_v10_x",
                                          "fail": ";".join(mism)})
                    row["tex_field1"] = d["field1"]
                    row["tex_field2"] = d["field2"]
                    row["tex_low8"] = d["low8"]
                    row["tex_entry_count"] = d["entry_count"]
                    row["tex_num_tex"] = d["num_tex"]
                    slots = Counter()
                    for pe in ptex:
                        nm = pe.get("name", "")
                        if "_" in nm:
                            slots[nm.rsplit("_", 1)[1]] += 1
                    row["tex_slots"] = dict(slots)
                else:
                    d = decode_v4_texture(b.raw_bytes)
                    if not d.get("ok"):
                        anomalies.append({"file": name, "kind": "tex_v4",
                                          "fail": d.get("fail")})
                        continue
                    row["tex_v4_num_tex"] = d["num_tex"]
                    row["tex_v4_consumed_ok"] = 1
            elif bt == "NiArkAnimationExtraData":
                fld = b.fields or {}
                if fld.get("ark_variant") == "G3B":
                    raw = b.raw_bytes or b""
                    nl = struct.unpack_from("<i", raw, 0)[0]
                    ext = raw[4 + nl + 16:]
                    stored = fld.get("ark_anim_ext_raw") or b""
                    if stored != ext:
                        anomalies.append({"file": name, "kind": "g3b_ext",
                                          "fail": "ext_vs_stored"})
                    recs, why = walk_g3b_records(ext)
                    if recs is None:
                        anomalies.append({"file": name, "kind": "g3b_walk",
                                          "fail": why, "ext_len": len(ext)})
                        continue
                    tstr = sum(r["count"] for r in recs)
                    if tstr > 0:
                        for r in recs:
                            for s in r["strings"]:
                                g3b_strings.append({
                                    "file": name, "text": s["text"],
                                    "value_u32_hex": s["value_u32_hex"],
                                    "value_f32": s["value_f32"],
                                    "record_X": r["X"], "record_Y": r["Y"],
                                    "record_flag": r["flag"],
                                    "record_class": r["class_byte"],
                                    "ext_len": len(ext)})
            elif bt == "NiArkViewportInfoExtraData":
                raw = b.raw_bytes or b""
                nl = struct.unpack_from("<i", raw, 0)[0]
                ext = raw[4 + nl:]
                el = len(ext)
                viewport_len_census[el] += 1
                viewport_per_file[name] += 1
                vrow = {"file": name, "ext_len": el}
                if el in VIEWPORT_FLOAT_LENS:
                    vrow["ext_hex"] = ext.hex()
                    vrow["floats"] = [
                        struct.unpack_from("<f", ext, o)[0]
                        for o in range(0, el - 3, 4)]
                else:
                    if viewport_len_census[el] == 1:
                        vrow["ext_hex"] = ext.hex()
                viewport_blocks.append(vrow)
        files.append(row)
        if n % 500 == 0:
            log("[extract] progress %d/5596 (PASS=%d)"
                % (n, parse_status.get("PASS", 0)))

    n_pass = parse_status.get("PASS", 0)
    log("[extract] parse closure: PASS=%d/%d dist=%s"
        % (n_pass, len(entries), dict(parse_status)))
    if n_pass != len(entries):
        hard_stop("parse closure %d/%d (<100%%)" % (n_pass, len(entries)))

    # derived per-file flags
    for row in files:
        types = row["types"]
        row["has_mesh_node"] = 1 if any(t in MESH_NODE_TYPES for t in types) else 0
        row["has_morph"] = 1 if any(t in MORPH_TYPES for t in types) else 0
        row["has_skin"] = 1 if any(t in SKIN_TYPES for t in types) else 0
        row["has_particle"] = 1 if any(
            ("particle" in t.lower() or "psys" in t.lower()) for t in types) else 0
        row["has_tex_effect"] = 1 if "NiTextureEffect" in types else 0

    out = {
        "run": "PE_NIF_935_SEMANTIC_CORRELATIONS_R1",
        "phase": "extract",
        "standing_sentence": STANDING,
        "pins": {
            "models_bnt_sha256": MODELS_BNT_SHA256,
            "r61_hashes_ok": 10,
            "bnt_entries": len(entries),
            "parse_closure": {"pass": n_pass, "total": len(entries)},
        },
        "block_type_census": dict(block_type_census),
        "importer_class_census": dict(importer_census),
        "exporter_version_matrix": {"%s|%s" % k: v
                                     for k, v in exporter_matrix.items()},
        "viewport_len_census": {str(k): v
                                for k, v in viewport_len_census.items()},
        "viewport_per_file_histogram": dict(Counter(
            viewport_per_file.values())),
        "g3b_string_rows": g3b_strings,
        "viewport_blocks": viewport_blocks,
        "anomalies": anomalies,
        "files": files,
    }
    os.makedirs(RAW, exist_ok=True)
    with open(os.path.join(RAW, "EXTRACTION.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    log("[extract] anomalies: %d" % len(anomalies))
    log("[extract] G3B string rows: %d" % len(g3b_strings))
    log("[extract] viewport len census: %s" % dict(viewport_len_census))
    log("[extract] wrote 01_RAW/EXTRACTION.json")
    flush_log()


# ============================================================
# statistics helpers
# ============================================================

def chi2_stat(table):
    """Pearson chi-square. table = list of rows (list of ints)."""
    rows = len(table)
    cols = len(table[0])
    row_tot = [sum(r) for r in table]
    col_tot = [sum(table[r][c] for r in range(rows)) for c in range(cols)]
    n = sum(row_tot)
    chi2 = 0.0
    for r in range(rows):
        for c in range(cols):
            e = row_tot[r] * col_tot[c] / float(n)
            if e <= 0:
                continue
            chi2 += (table[r][c] - e) ** 2 / e
    return chi2


def drop_zero_marginals(table, row_labels, col_labels):
    """Drop zero-marginal rows/cols; return (table, row_labels, col_labels,
    dropped_rows, dropped_cols)."""
    kept_r = [i for i in range(len(table)) if sum(table[i]) > 0]
    kept_c = [j for j in range(len(table[0]))
              if sum(table[i][j] for i in range(len(table))) > 0]
    t2 = [[table[i][j] for j in kept_c] for i in kept_r]
    return (t2, [row_labels[i] for i in kept_r],
            [col_labels[j] for j in kept_c],
            [row_labels[i] for i in range(len(table)) if i not in kept_r],
            [col_labels[j] for j in range(len(table[0]))
             if j not in kept_c])


def permutation_test(a_labels, col_of, col_labels, seed_offset,
                     n_perm=N_PERM):
    """A (int labels per item) x B (column index per item) chi-square
    permutation test. Items are pre-grouped by column (col_of gives the
    ordered column index per position in the packed arrays)."""
    n = len(a_labels)
    k = len(col_labels)
    ka = 1 + (max(a_labels) if a_labels else -1)
    # pack: items ordered grouped by column
    order = sorted(range(n), key=lambda i: col_of[i])
    packed_a = [a_labels[i] for i in order]
    packed_c = [col_of[i] for i in order]
    # compute column slices
    slices = []
    pos = 0
    for j in range(k):
        cnt = packed_c.count(j)
        slices.append((pos, pos + cnt))
        pos += cnt
    col_marg = [e - s for (s, e) in slices]

    def build_table(labs):
        t = [[0] * k for _ in range(ka)]
        for j, (s, e) in enumerate(slices):
            seg = labs[s:e]
            for r in range(ka):
                t[r][j] = seg.count(r)
        return t

    obs_table = build_table(packed_a)
    t2, rl, cl, dr, dc = drop_zero_marginals(
        obs_table, list(range(ka)), list(range(k)))
    obs = chi2_stat(t2) if (len(t2) > 1 and len(t2[0]) > 1) else 0.0
    rng = random.Random(SEED + seed_offset)
    labels = list(packed_a)
    ge = 0
    perm_vals = []
    for _ in range(n_perm):
        rng.shuffle(labels)
        pt = build_table(labels)
        pt2, _, _, _, _ = drop_zero_marginals(
            pt, list(range(ka)), list(range(k)))
        if len(pt2) > 1 and len(pt2[0]) > 1:
            v = chi2_stat(pt2)
        else:
            v = 0.0
        perm_vals.append(v)
        if v >= obs:
            ge += 1
    perm_vals.sort()
    p95 = perm_vals[int(0.95 * n_perm)]
    p99 = perm_vals[int(0.99 * n_perm)]
    mean = sum(perm_vals) / float(n_perm)
    sd = math.sqrt(sum((v - mean) ** 2 for v in perm_vals) / float(n_perm))
    return {
        "obs_chi2": obs,
        "perm_mean": mean, "perm_sd": sd,
        "perm_p95": p95, "perm_p99": p99,
        "p_perm": (1.0 + ge) / float(n_perm + 1),
        "obs_table": obs_table, "row_labels": rl, "col_labels": cl,
        "dropped_rows": dr, "dropped_cols": dc,
        "obs_exceeds_p95": bool(obs > p95),
        "n_perm": n_perm,
    }


def verdict_of(res):
    if res["obs_exceeds_p95"]:
        return "OBSERVED correlation (obs > perm p95; control numbers in " \
               "this record; OBSERVED-level evidence only)"
    return "NO OBSERVED correlation (obs <= perm p95; control numbers in " \
           "this record)"


def quantiles(vals):
    if not vals:
        return None
    s = sorted(vals)
    n = len(s)
    def q(p):
        i = min(int(p * (n - 1)), n - 1)
        return s[i]
    return {"min": s[0], "q25": q(0.25), "median": q(0.5), "q75": q(0.75),
            "max": s[-1], "mean": sum(s) / float(n), "n": n}


def binned(v, bins):
    """bins = list of upper bounds in ascending order; returns bin index."""
    for i, b in enumerate(bins):
        if v <= b:
            return i
    return len(bins)


# ============================================================
# k-means (pure python, pre-registered)
# ============================================================

def _dist2(a, b):
    s = 0.0
    for i in range(len(a)):
        d = a[i] - b[i]
        s += d * d
    return s


def kmeans_once(vecs, k, rng):
    cents = rng.sample(vecs, k)
    assign = [0] * len(vecs)
    for _ in range(KMEANS_MAXITER):
        moved = False
        for i, v in enumerate(vecs):
            best, bd = 0, _dist2(v, cents[0])
            for c in range(1, k):
                d = _dist2(v, cents[c])
                if d < bd:
                    bd, best = d, c
            if assign[i] != best:
                assign[i] = best
                moved = True
        # recompute
        sums = [[0.0] * len(vecs[0]) for _ in range(k)]
        cnts = [0] * k
        for i, v in enumerate(vecs):
            c = assign[i]
            cnts[c] += 1
            sv = sums[c]
            for j, x in enumerate(v):
                sv[j] += x
        for c in range(k):
            if cnts[c] > 0:
                cents[c] = [s / cnts[c] for s in sums[c]]
            else:
                # empty-cluster re-seeding (pre-registered): place the empty
                # centroid at the vector currently FARTHEST from its own
                # centroid (deterministic tie-break by index) -- prevents the
                # single-cluster collapse observed in the first execution
                far_i, far_d = -1, -1.0
                for i, v in enumerate(vecs):
                    d2c = _dist2(v, cents[assign[i]])
                    if d2c > far_d:
                        far_d, far_i = d2c, i
                if far_i >= 0 and far_d > 0:
                    cents[c] = list(vecs[far_i])
                    assign[far_i] = c
                    moved = True
        if not moved:
            break
    inertia = sum(_dist2(vecs[i], cents[assign[i]]) for i in range(len(vecs)))
    return inertia, assign, cents


def kmeans_best(vecs, k, seed_offset):
    rng = random.Random(SEED * 1000 + seed_offset * 10 + k)
    best = None
    for _ in range(KMEANS_RESTARTS):
        inertia, assign, cents = kmeans_once(vecs, k, rng)
        if best is None or inertia < best[0]:
            best = (inertia, assign, cents)
    return best


# ============================================================
# PROBE-3 family classification (pre-registered)
# ============================================================

RE_MORPH_LR = re.compile(r"^morph:?(left|right|rifgt)$")
RE_SOUND = re.compile(r"^sound:hit_[0-9]+$")


def classify_event(text):
    """Returns (family, subtype). Pre-registered rules; see docstring."""
    n = text.lower().replace("\r", "").replace("\n", "")
    n = n.replace(" ", "").replace("\t", "")
    if RE_MORPH_LR.match(n):
        return "MORPH_LR", ""
    if RE_SOUND.match(n):
        return "SOUND_HIT", ""
    if n.startswith("start_usetool:"):
        if "\r" in text or "\n" in text:
            sub = "multi_combined"
        elif "effect" in n:
            sub = "single_effect"
        else:
            sub = "single_sound"
        return "START_USETOOL", sub
    if n.startswith("start-name"):
        return "ANIMCMD_500078", ""
    if n in ("end", "morph:1"):
        return "END_MORPH1", ""
    return "OTHER", ""


# ============================================================
# ANALYZE phase
# ============================================================

def phase_analyze():
    with open(os.path.join(RAW, "EXTRACTION.json"), "r", encoding="utf-8") as f:
        ex = json.load(f)
    files = ex["files"]
    g3b_strings = ex["g3b_string_rows"]
    vp_blocks = ex["viewport_blocks"]
    os.makedirs(ANALYSIS, exist_ok=True)

    # ---------------- G2 reconciliation ----------------
    v4_files = [r for r in files if r.get("imp_klass") == "v4"]
    v10_tex = [r for r in files if "tex_field1" in r]
    flag_ct = Counter(r["imp_flag3"] for r in v4_files)
    f1_ct = Counter((str(r["tex_field1"]), r["tex_low8"]) for r in v10_tex)
    # field1/low8 joint canon: keys are (str(field1), low8) in f1_ct
    F1_CANON = [(("1", 0), 3042), (("-256", 255), 1796)]
    ev_blocks = len(set(s["file"] for s in g3b_strings))
    ev_total = len(g3b_strings)
    ev_zero = sum(1 for s in g3b_strings if s["value_f32"] == 0.0)
    vp_census = ex["viewport_len_census"]

    recon = {
        "canon_targets": CANON,
        "observed": {
            "flag_states": {k: flag_ct.get(k, 0)
                            for k in CANON["flag_states"]},
            "flag_states_extra": {k: v for k, v in flag_ct.items()
                                  if k not in CANON["flag_states"]},
            "field1_classes": {"%s|%d" % k: f1_ct.get(k, 0)
                               for k, _ in F1_CANON},
            "field1_classes_extra": {"%s|%d" % k: v for k, v in f1_ct.items()
                                      if k not in [ck for ck, _ in F1_CANON]},
            "events": {"strings_total": ev_total,
                       "string_bearing_blocks": ev_blocks,
                       "zero_values": ev_zero},
            "viewport": {k: vp_census.get(k, 0)
                         for k in CANON["viewport"]},
            "viewport_extra": {k: v for k, v in vp_census.items()
                               if k not in CANON["viewport"]},
            "importer_v10": ex["importer_class_census"].get("v10", 0),
            "importer_v4": ex["importer_class_census"].get("v4", 0),
        },
    }
    mism = []
    for k, v in CANON["flag_states"].items():
        if flag_ct.get(k, 0) != v:
            mism.append("flag_states[%s]: canon %d, observed %d"
                        % (k, v, flag_ct.get(k, 0)))
    for key, cnt in F1_CANON:
        if f1_ct.get(key, 0) != cnt:
            mism.append("field1_classes[%s|%d]: canon %d, observed %d"
                        % (key[0], key[1], cnt, f1_ct.get(key, 0)))
    if ev_total != CANON["events"]["strings_total"]:
        mism.append("events.strings_total: canon 263, observed %d" % ev_total)
    if ev_blocks != CANON["events"]["string_bearing_blocks"]:
        mism.append("events.string_bearing_blocks: canon 136, observed %d"
                    % ev_blocks)
    if ev_zero != CANON["events"]["zero_values"]:
        mism.append("events.zero_values: canon 113, observed %d" % ev_zero)
    for k, v in CANON["viewport"].items():
        if vp_census.get(k, 0) != v:
            mism.append("viewport[%s]: canon %d, observed %d"
                        % (k, v, vp_census.get(k, 0)))
    if ex["importer_class_census"].get("v4", 0) != 758:
        mism.append("importer v4: canon 758, observed %d"
                    % ex["importer_class_census"].get("v4", 0))
    if ex["importer_class_census"].get("v10", 0) != 4838:
        mism.append("importer v10: canon 4838, observed %d"
                    % ex["importer_class_census"].get("v10", 0))
    recon["mismatches"] = mism
    with open(os.path.join(ANALYSIS, "RECONCILIATION.json"), "w",
              encoding="utf-8") as f:
        json.dump(recon, f, indent=1)
    log("[G2] reconciliation mismatches: %d %s" % (len(mism), mism))
    if mism:
        with open(os.path.join(RUN, "STAGE_ACCEPTANCE_GATES.csv"), "w",
                  newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["gate", "description", "result", "detail"])
            w.writerow(["G1", "pins", "PASS",
                        "R61 10/10; corpus c950a8c2; driver hash provenance"])
            w.writerow(["G2", "canon reconciliation",
                        "MISMATCH", "; ".join(mism)])
        flush_log()
        hard_stop("CENSUS_MISMATCH: " + "; ".join(mism[:5]), code=3)

    # per-probe raw CSVs (G5 machine-readable)
    # PROBE-1 rows
    p1_rows = []
    for r in v4_files:
        p1_rows.append({
            "file": r["file"], "flag_state": r["imp_flag3"],
            "nif_version": r["version"],
            "exporter": r.get("imp_exporter", ""),
            "mesh": r["has_mesh_node"], "morph": r["has_morph"],
            "skin": r["has_skin"],
            "blocks": r["blocks"],
            "geom_triangles": r.get("geom_triangles", 0),
            "entry_count": r.get("tex_v4_num_tex", -1),
            "mirror": r["mirror"],
        })
    with open(os.path.join(RAW, "PROBE1_RAW.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(p1_rows[0].keys()))
        w.writeheader()
        w.writerows(p1_rows)

    # PROBE-2 rows
    p2_rows = []
    slot_names = ["BASE", "DARK", "DETAIL", "GLOSS", "GLOW", "BUMP",
                  "DECAL0", "ENVIRONMENT"]
    for r in v10_tex:
        slots = r.get("tex_slots", {})
        has_anim = any(k.startswith("ANIM") for k in slots)
        p2_rows.append({
            "file": r["file"], "klass": "%d|%d" % (r["tex_field1"],
                                                  r["tex_low8"]),
            "entry_count": r["tex_entry_count"], "num_tex": r["tex_num_tex"],
            "field2_raw": r["tex_field2"],
            "has_anim": 1 if has_anim else 0,
            "anim_count": sum(v for k, v in slots.items()
                              if k.startswith("ANIM")),
            **{"has_" + s.lower(): (1 if s in slots else 0)
               for s in slot_names},
            "tex_effect": r["has_tex_effect"], "mesh": r["has_mesh_node"],
            "blocks": r["blocks"], "mirror": r["mirror"],
        })
    with open(os.path.join(RAW, "PROBE2_RAW.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(p2_rows[0].keys()))
        w.writeheader()
        w.writerows(p2_rows)

    # PROBE-3 rows
    p3_rows = []
    for s in g3b_strings:
        fam, sub = classify_event(s["text"])
        p3_rows.append({
            "file": s["file"], "text": s["text"],
            "value_u32_hex": s["value_u32_hex"], "value_f32": s["value_f32"],
            "zero": 1 if s["value_f32"] == 0.0 else 0,
            "family": fam, "subtype": sub,
            "ext_len": s["ext_len"],
        })
    with open(os.path.join(RAW, "PROBE3_RAW.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(p3_rows[0].keys()))
        w.writeheader()
        w.writerows(p3_rows)

    # PROBE-4 rows (85/121/43)
    fidx = {r["file"]: r for r in files}
    p4_rows = []
    for vb in vp_blocks:
        if vb["ext_len"] not in VIEWPORT_FLOAT_LENS:
            continue
        fr = fidx.get(vb["file"], {})
        vec = vb.get("floats")
        sub43 = ""
        if vb["ext_len"] == 43 and vec is not None:
            sub43 = ("parametric" if any(abs(x) > 1e-6 for x in vec[2:])
                     else "all_zero_default")
        p4_rows.append({
            "file": vb["file"], "ext_len": vb["ext_len"],
            "subclass43": sub43, "ext_hex": vb["ext_hex"],
            "mesh": fr.get("has_mesh_node", 0), "morph": fr.get("has_morph", 0),
            "skin": fr.get("has_skin", 0), "particle": fr.get("has_particle", 0),
            "blocks": fr.get("blocks", 0), "mirror": fr.get("mirror", 0),
        })
    with open(os.path.join(RAW, "PROBE4_RAW.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(p4_rows[0].keys()))
        w.writeheader()
        w.writerows(p4_rows)

    # ---------------- PROBE-1 analysis ----------------
    so = 0
    p1_tests = {}
    a_labels = [ {"000000": 0, "0000ff": 1, "00ffff": 2}[r["imp_flag3"]]
                 for r in v4_files ]
    # B1 version
    def run_test(a, bvals, blabels, name, desc):
        nonlocal so
        so += 1
        res = permutation_test(a, bvals, blabels, so)
        res["variable"] = name
        res["description"] = desc
        res["verdict"] = verdict_of(res)
        log("[P1] %s: %s (obs=%.3f p95=%.3f p_perm=%.4f)"
            % (name, res["verdict"], res["obs_chi2"], res["perm_p95"],
               res["p_perm"]))
        return res

    ver_map = {"4.0.0.0": 0, "4.0.0.2": 1, "4.1.0.12": 2}
    def run_test(a, bvals, blabels, name, desc):
        nonlocal so
        if len(set(bvals)) < 2:
            res = {"variable": name, "description": desc,
                   "verdict": "NO TEST (constant in population: %s=%s in "
                              "all %d items -- documented per "
                              "pre-registration)"
                              % (name, blabels[bvals[0]], len(bvals)),
                   "constant": bvals[0]}
            log("[P1] %s: constant (%s) -- NO TEST" % (name, blabels[bvals[0]]))
            return res
        so += 1
        res = permutation_test(a, bvals, blabels, so)
        res["variable"] = name
        res["description"] = desc
        res["verdict"] = verdict_of(res)
        log("[P1] %s: %s (obs=%.3f p95=%.3f p_perm=%.4f)"
            % (name, res["verdict"], res["obs_chi2"], res["perm_p95"],
               res["p_perm"]))
        return res

    p1_tests["B1_nif_version"] = run_test(
        a_labels, [ver_map.get(r["version"], 3) for r in v4_files],
        list(ver_map.keys()) + ["other"], "B1_nif_version",
        "flag state x nif version class")
    exp_map = {"4.0.0.0": 0, "4.0.0.2": 1, "4.1.0.12": 2}
    p1_tests["B2_exporter"] = run_test(
        a_labels, [exp_map.get(r.get("imp_exporter"), 3) for r in v4_files],
        list(exp_map.keys()) + ["other"], "B2_exporter",
        "flag state x exporter string class")
    p1_tests["B3_mesh"] = run_test(
        a_labels, [r["has_mesh_node"] for r in v4_files], ["no", "yes"],
        "B3_mesh", "flag state x mesh-bearing")
    p1_tests["B4_morph"] = run_test(
        a_labels, [r["has_morph"] for r in v4_files], ["no", "yes"],
        "B4_morph", "flag state x morph-bearing")
    bc_bins = [8, 16, 32, 64]
    p1_tests["B5_blocks"] = run_test(
        a_labels, [binned(r["blocks"], bc_bins) for r in v4_files],
        ["<=8", "9-16", "17-32", "33-64", ">64"], "B5_blocks",
        "flag state x block count class")
    tri_bins = [0, 500, 2000, 8000]
    p1_tests["B6_geom"] = run_test(
        a_labels, [binned(r.get("geom_triangles", 0), tri_bins)
                   for r in v4_files],
        ["0", "1-500", "501-2000", "2001-8000", ">8000"], "B6_geom",
        "flag state x geometry size class (total num_triangles over "
        "NiTriShapeData/NiTriStripsData)")
    ec_bins = [0, 2, 8]
    p1_tests["B7_entries"] = run_test(
        a_labels, [binned(r.get("tex_v4_num_tex", 0), ec_bins)
                   for r in v4_files],
        ["0", "1-2", "3-8", ">8"], "B7_entries",
        "flag state x texture entry count class")
    p1_tests["B8_mirror"] = run_test(
        a_labels, [r["mirror"] for r in v4_files], ["no", "yes"],
        "B8_mirror", "flag state x era-mirror")
    # descriptives
    p1_desc = {}
    for st in ("000000", "0000ff", "00ffff"):
        grp = [r for r in v4_files if r["imp_flag3"] == st]
        p1_desc[st] = {
            "n": len(grp),
            "blocks": quantiles([r["blocks"] for r in grp]),
            "geom_triangles": quantiles([r.get("geom_triangles", 0)
                                         for r in grp]),
            "entry_count": quantiles([r.get("tex_v4_num_tex", 0)
                                      for r in grp]),
            "version_dist": dict(Counter(r["version"] for r in grp)),
            "exporter_dist": dict(Counter(r.get("imp_exporter")
                                          for r in grp)),
        }
    with open(os.path.join(ANALYSIS, "PROBE1_CONTINGENCY.json"), "w",
              encoding="utf-8") as f:
        json.dump({"tests": p1_tests, "descriptives": p1_desc,
                   "standing_sentence": STANDING}, f, indent=1)

    # ---------------- PROBE-2 analysis ----------------
    p2_tests = {}
    a2 = [0 if r["tex_field1"] == 1 else 1 for r in v10_tex]
    so2 = 100
    def run_test2(a, bvals, blabels, name, desc):
        nonlocal so2
        if len(set(bvals)) < 2 or len(set(a)) < 2:
            which = "A" if len(set(a)) < 2 else "B"
            res = {"variable": name, "description": desc,
                   "verdict": "NO TEST (constant in population: side %s "
                              "has <2 classes -- documented per "
                              "pre-registration)" % which}
            log("[P2] %s: constant side %s -- NO TEST" % (name, which))
            return res
        so2 += 1
        res = permutation_test(a, bvals, blabels, so2)
        res["variable"] = name
        res["description"] = desc
        res["verdict"] = verdict_of(res)
        log("[P2] %s: %s (obs=%.3f p95=%.3f p_perm=%.4f)"
            % (name, res["verdict"], res["obs_chi2"], res["perm_p95"],
               res["p_perm"]))
        return res

    ec_bins2 = [0, 1, 3, 8]
    p2_tests["B1_entry_count"] = run_test2(
        a2, [binned(r["tex_entry_count"], ec_bins2) for r in v10_tex],
        ["0", "1", "2-3", "4-8", ">8"], "B1_entry_count",
        "field1 class x entry count class")
    for slot in slot_names:
        key = "has_" + slot.lower()
        p2_tests["B_" + slot] = run_test2(
            a2, [1 if slot in r.get("tex_slots", {}) else 0
                 for r in v10_tex],
            ["no", "yes"], "B_" + slot,
            "field1 class x has %s slot" % slot)
    p2_tests["B7_anim"] = run_test2(
        a2, [1 if any(k.startswith("ANIM") for k in r.get("tex_slots", {}))
             else 0 for r in v10_tex],
        ["no", "yes"], "B7_anim", "field1 class x has ANIM slot")
    p2_tests["B8_tex_effect"] = run_test2(
        a2, [r["has_tex_effect"] for r in v10_tex], ["no", "yes"],
        "B8_tex_effect", "field1 class x NiTextureEffect present")
    p2_tests["B9_mesh"] = run_test2(
        a2, [r["has_mesh_node"] for r in v10_tex], ["no", "yes"],
        "B9_mesh", "field1 class x mesh-bearing")
    p2_tests["B10_mirror"] = run_test2(
        a2, [r["mirror"] for r in v10_tex], ["no", "yes"], "B10_mirror",
        "field1 class x era-mirror")
    # constants
    nt = Counter(r["tex_num_tex"] for r in v10_tex)
    p2_desc = {
        "num_tex_census": dict(nt),
        "num_tex_verdict": ("CONSTANT (=3 in 4838/4838) -- NO TEST"
                            if nt == {3: 4838} else "NON-CONSTANT -- see census"),
        "field2_packing_note": ("field2 raw = entry_count<<8 | low8 "
                                "(deterministic function of B1_entry_count "
                                "and A; tested via B1_entry_count, not "
                                "separately)"),
        "entry_count_hist_by_class": {},
        "slot_mean_counts_by_class": {},
    }
    for cls in (0, 1):
        grp = [r for r in v10_tex
               if (0 if r["tex_field1"] == 1 else 1) == cls]
        lab = "C1(field1=1,low8=0)" if cls == 0 else "C2(field1=-256,low8=255)"
        p2_desc["entry_count_hist_by_class"][lab] = dict(
            Counter(r["tex_entry_count"] for r in grp).most_common(12))
        slotsm = defaultdict(list)
        for r in grp:
            for k, v in r.get("tex_slots", {}).items():
                slotsm[k].append(v)
        p2_desc["slot_mean_counts_by_class"][lab] = {
            k: round(sum(v) / float(len(grp)), 4) for k, v in slotsm.items()}
    with open(os.path.join(ANALYSIS, "PROBE2_CONTINGENCY.json"), "w",
              encoding="utf-8") as f:
        json.dump({"tests": p2_tests, "descriptives": p2_desc,
                   "standing_sentence": STANDING}, f, indent=1)

    # ---------------- PROBE-3 analysis ----------------
    fam_ct = Counter(r["family"] for r in p3_rows)
    fam_zero = defaultdict(int)
    fam_vals = defaultdict(list)
    fam_distinct = defaultdict(Counter)
    for r in p3_rows:
        fam_zero[r["family"]] += r["zero"]
        if r["zero"] == 0:
            fam_vals[r["family"]].append(r["value_f32"])
            fam_distinct[r["family"]][r["value_f32"]] += 1
    p3_fam = {}
    for fam in fam_ct:
        p3_fam[fam] = {
            "n": fam_ct[fam],
            "zero_rate": round(fam_zero[fam] / float(fam_ct[fam]), 4),
            "nonzero_values_quantiles": quantiles(fam_vals[fam]),
            "nonzero_distinct_top": fam_distinct[fam].most_common(12),
        }
    # permutation control on zero/nonzero x family
    so3 = 200
    fam_order = sorted(fam_ct.keys())
    fam_idx = {f: i for i, f in enumerate(fam_order)}
    a3 = [r["zero"] for r in p3_rows]
    b3 = [fam_idx[r["family"]] for r in p3_rows]
    res3 = permutation_test(a3, b3, fam_order, so3)
    res3["variable"] = "zero_nonzero_x_family"
    res3["description"] = "per-string u32 zero/non-zero partition x " \
                          "event-name family"
    res3["verdict"] = verdict_of(res3)
    log("[P3] zero x family: %s (obs=%.3f p95=%.3f p_perm=%.4f)"
        % (res3["verdict"], res3["obs_chi2"], res3["perm_p95"], res3["p_perm"]))
    with open(os.path.join(ANALYSIS, "PROBE3_FAMILIES.json"), "w",
              encoding="utf-8") as f:
        json.dump({"families": p3_fam, "family_order": fam_order,
                   "permutation": res3, "standing_sentence": STANDING},
                  f, indent=1)

    # ---------------- PROBE-4 analysis ----------------
    vec_by_len = defaultdict(list)
    for vb in vp_blocks:
        if "floats" in vb:
            vec_by_len[vb["ext_len"]].append(vb)
    p4_pos = {}
    for el, vlist in sorted(vec_by_len.items()):
        dims = len(vlist[0]["floats"])
        pos_stats = []
        for p in range(dims):
            col = [v["floats"][p] for v in vlist]
            fin = [x for x in col if math.isfinite(x)]
            n_nonfinite = len(col) - len(fin)
            distinct = Counter(fin)
            pos_stats.append({
                "pos": p,
                "min": min(fin) if fin else None,
                "max": max(fin) if fin else None,
                "mean": (sum(fin) / float(len(fin))) if fin else None,
                "median": quantiles(fin)["median"] if fin else None,
                "n_zero_exact": sum(1 for x in fin if x == 0.0),
                "n_near_zero_lt_1e-6": sum(1 for x in fin if abs(x) < 1e-6),
                "n_nonfinite": n_nonfinite,
                "n_distinct": len(distinct),
                "top3": [[repr(k), c] for k, c in distinct.most_common(3)],
            })
        p4_pos[str(el)] = {"n_blocks": len(vlist), "dims": dims,
                           "label": "POSITION-STATISTICS (not semantics; "
                                    "non-finite decoded values counted "
                                    "separately, excluded from min/max)",
                           "positions": pos_stats}
    with open(os.path.join(ANALYSIS, "PROBE4_POSITION_STATS.json"), "w",
              encoding="utf-8") as f:
        json.dump(p4_pos, f, indent=1)

    # 43B sub-class census: parametric iff any FINITE |float| > 1e-6 at
    # positions >= 2 (pre-registered; non-finite counts as not-parametric)
    sub43 = Counter()
    for vb in vec_by_len.get(43, []):
        vec = vb["floats"]
        sub43["parametric" if any(
            math.isfinite(x) and abs(x) > 1e-6 for x in vec[2:])
            else "all_zero_default"] += 1
    log("[P4] 43B subclasses: %s" % dict(sub43))

    # k-means 85B and 121B
    p4_clusters = {}
    for el, ks in ((85, [2, 3, 4, 5]), (121, [2, 3, 4])):
        vlist = vec_by_len.get(el, [])
        if not vlist:
            continue
        # pre-registered sanitization: non-finite decoded values are not
        # camera parameters; replaced by 0.0 for clustering (census above)
        vecs = [[x if math.isfinite(x) else 0.0 for x in v["floats"]]
                for v in vlist]
        curve = {}
        results = {}
        for k in ks:
            inertia, assign, cents = kmeans_best(vecs, k, el % 7)
            results[k] = (inertia, assign, cents)
            curve[k] = {"inertia": round(inertia, 6),
                        "sizes": dict(Counter(assign))}
        chosen = ks[0]
        for i in range(len(ks) - 1):
            k, k2 = ks[i], ks[i + 1]
            r = curve[k2]["inertia"] / curve[k]["inertia"] \
                if curve[k]["inertia"] > 0 else 1.0
            if r > ELBOW_RATIO:
                chosen = k
                break
        else:
            chosen = ks[-1]
        inertia, assign, cents = results[chosen]
        p4_clusters[str(el)] = {
            "n": len(vecs), "dims": len(vecs[0]), "ks_tested": ks,
            "inertia_curve": curve, "elbow_rule": ELBOW_RATIO,
            "chosen_k": chosen,
            "chosen_sizes": dict(Counter(assign)),
            "chosen_centroids": [[round(x, 6) for x in c] for c in cents],
        }
        log("[P4] %dB kmeans: chosen k=%d sizes=%s"
            % (el, chosen, p4_clusters[str(el)]["chosen_sizes"]))
        # cluster x file-class tests
        tests = {}
        so4 = 300 + el
        def run_test4(a, bvals, blabels, name, desc):
            nonlocal so4
            if len(set(bvals)) < 2 or len(set(a)) < 2:
                which = "A" if len(set(a)) < 2 else "B"
                res = {"variable": name, "description": desc,
                       "verdict": "NO TEST (constant in population: side %s "
                                  "has <2 classes -- documented per "
                                  "pre-registration)" % which}
                log("[P4/%dB] %s: constant side %s -- NO TEST"
                    % (el, name, which))
                return res
            so4 += 1
            res = permutation_test(a, bvals, blabels, so4)
            res["variable"] = name
            res["description"] = desc
            res["verdict"] = verdict_of(res)
            log("[P4/%dB] %s: %s (obs=%.3f p95=%.3f p_perm=%.4f)"
                % (el, name, res["verdict"], res["obs_chi2"],
                   res["perm_p95"], res["p_perm"]))
            return res
        fprops = [fidx[v["file"]] for v in vlist]
        tests["cluster_x_mesh"] = run_test4(
            assign, [p["has_mesh_node"] for p in fprops], ["no", "yes"],
            "cluster_x_mesh", "cluster x mesh-bearing")
        tests["cluster_x_morph"] = run_test4(
            assign, [p["has_morph"] for p in fprops], ["no", "yes"],
            "cluster_x_morph", "cluster x morph-bearing")
        tests["cluster_x_skin"] = run_test4(
            assign, [p["has_skin"] for p in fprops], ["no", "yes"],
            "cluster_x_skin", "cluster x skinned")
        tests["cluster_x_particle"] = run_test4(
            assign, [p["has_particle"] for p in fprops], ["no", "yes"],
            "cluster_x_particle", "cluster x particle-bearing")
        bc_bins2 = [16, 32, 64, 128]
        tests["cluster_x_blocks"] = run_test4(
            assign, [binned(p["blocks"], bc_bins2) for p in fprops],
            ["<=16", "17-32", "33-64", "65-128", ">128"],
            "cluster_x_blocks", "cluster x block count class")
        tests["cluster_x_mirror"] = run_test4(
            assign, [p["mirror"] for p in fprops], ["no", "yes"],
            "cluster_x_mirror", "cluster x era-mirror")
        p4_clusters[str(el)]["tests"] = tests

    # pooled ext-length class x content classes (682 blocks)
    pool = [r for r in p4_rows]
    a_len = {"85": 0, "121": 1, "43": 2}
    a_pool = [a_len[str(r["ext_len"])] for r in pool]
    pool_tests = {}
    so5 = 400
    def run_test5(a, bvals, blabels, name, desc):
        nonlocal so5
        if len(set(bvals)) < 2 or len(set(a)) < 2:
            which = "A" if len(set(a)) < 2 else "B"
            res = {"variable": name, "description": desc,
                   "verdict": "NO TEST (constant in population: side %s "
                              "has <2 classes -- documented per "
                              "pre-registration)" % which}
            log("[P4/pooled] %s: constant side %s -- NO TEST"
                % (name, which))
            return res
        so5 += 1
        res = permutation_test(a, bvals, blabels, so5)
        res["variable"] = name
        res["description"] = desc
        res["verdict"] = verdict_of(res)
        log("[P4/pooled] %s: %s (obs=%.3f p95=%.3f p_perm=%.4f)"
            % (name, res["verdict"], res["obs_chi2"], res["perm_p95"],
               res["p_perm"]))
        return res
    pool_tests["extlen_x_mesh"] = run_test5(
        a_pool, [r["mesh"] for r in pool], ["no", "yes"],
        "extlen_x_mesh", "ext-length class x mesh-bearing")
    pool_tests["extlen_x_morph"] = run_test5(
        a_pool, [r["morph"] for r in pool], ["no", "yes"],
        "extlen_x_morph", "ext-length class x morph-bearing")
    pool_tests["extlen_x_skin"] = run_test5(
        a_pool, [r["skin"] for r in pool], ["no", "yes"],
        "extlen_x_skin", "ext-length class x skinned")
    pool_tests["extlen_x_particle"] = run_test5(
        a_pool, [r["particle"] for r in pool], ["no", "yes"],
        "extlen_x_particle", "ext-length class x particle-bearing")
    pool_tests["extlen_x_blocks"] = run_test5(
        a_pool, [binned(r["blocks"], [16, 32, 64, 128]) for r in pool],
        ["<=16", "17-32", "33-64", "65-128", ">128"],
        "extlen_x_blocks", "ext-length class x block count class")
    pool_tests["extlen_x_mirror"] = run_test5(
        a_pool, [r["mirror"] for r in pool], ["no", "yes"],
        "extlen_x_mirror", "ext-length class x era-mirror")

    # 43B subclass x content classes (n=11; permutation control executed)
    sub43_tests = {}
    rows43 = [r for r in pool if r["ext_len"] == 43]
    a43 = [0 if r["subclass43"] == "parametric" else 1 for r in rows43]
    so6 = 500
    def run_test6(a, bvals, blabels, name, desc):
        nonlocal so6
        if len(set(bvals)) < 2 or len(set(a)) < 2:
            which = "A" if len(set(a)) < 2 else "B"
            res = {"variable": name, "description": desc,
                   "verdict": "NO TEST (constant in population: side %s "
                              "has <2 classes -- documented per "
                              "pre-registration)" % which}
            log("[P4/43B-sub] %s: constant side %s -- NO TEST"
                % (name, which))
            return res
        so6 += 1
        res = permutation_test(a, bvals, blabels, so6)
        res["variable"] = name
        res["description"] = desc
        res["verdict"] = verdict_of(res)
        log("[P4/43B-sub] %s: %s (obs=%.3f p95=%.3f p_perm=%.4f)"
            % (name, res["verdict"], res["obs_chi2"], res["perm_p95"],
               res["p_perm"]))
        return res
    sub43_tests["subclass_x_mesh"] = run_test6(
        a43, [r["mesh"] for r in rows43], ["no", "yes"],
        "subclass_x_mesh", "43B subclass x mesh-bearing")
    sub43_tests["subclass_x_blocks"] = run_test6(
        a43, [binned(r["blocks"], [16, 32, 64, 128]) for r in rows43],
        ["<=16", "17-32", "33-64", "65-128", ">128"],
        "subclass_x_blocks", "43B subclass x block count class")

    with open(os.path.join(ANALYSIS, "PROBE4_CLUSTERS.json"), "w",
              encoding="utf-8") as f:
        json.dump({
            "position_stats_file": "PROBE4_POSITION_STATS.json",
            "subclass43_census": dict(sub43),
            "clusters": p4_clusters,
            "pooled_extlen_tests": pool_tests,
            "subclass43_tests": sub43_tests,
            "pre_registration": {
                "vector": "f32 at 4-aligned offsets of ext (R8/R28 convention)",
                "clustering": "k-means raw vectors, Euclidean, restarts=%d, "
                              "max_iter=%d, seed=%d, elbow_ratio=%.2f"
                              % (KMEANS_RESTARTS, KMEANS_MAXITER, SEED,
                                 ELBOW_RATIO),
                "note_43B": "n=11 below k-means threshold; subclass census "
                            "only (pre-registered)"},
            "standing_sentence": STANDING,
        }, f, indent=1)

    # ---------------- gates CSV (driver-evaluated) ----------------
    all_test_objs = []
    for t in p1_tests.values():
        all_test_objs.append(t)
    for t in p2_tests.values():
        all_test_objs.append(t)
    all_test_objs.append(res3)
    for cl in p4_clusters.values():
        for t in cl.get("tests", {}).values():
            all_test_objs.append(t)
    for t in pool_tests.values():
        all_test_objs.append(t)
    for t in sub43_tests.values():
        all_test_objs.append(t)
    n_rows = len(all_test_objs)
    n_const = sum(1 for t in all_test_objs
                  if str(t.get("verdict", "")).startswith("NO TEST"))
    n_executed = n_rows - n_const
    with open(os.path.join(RUN, "STAGE_ACCEPTANCE_GATES.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["gate", "description", "result", "detail"])
        w.writerow(["G1", "pins (R61 10/10; corpus SHA; driver hash)",
                    "PASS",
                    "R61 10/10 READ-ONLY; Models.bnt c950a8c2... verified; "
                    "SHA256_DRIVER.txt == self-hash"])
        w.writerow(["G2", "canon reconciliation vs contract baseline",
                    "PASS" if not mism else "MISMATCH",
                    "flag 558/128/72; field1 3042/1796; events 263/136/113; "
                    "viewport 2304/752/592/79/11 -- all re-derived from "
                    "pinned bytes; RECONCILIATION.json"])
        w.writerow(["G3", "every probe has permutation control executed",
                    "PASS",
                    "%d test rows: %d executed each with %d label-shuffle "
                    "permutations (Pearson chi-square null; RNG seed %d); "
                    "%d constant variables documented NO TEST without "
                    "permutation" % (n_rows, n_executed, N_PERM, SEED,
                                     n_const)])
        w.writerow(["G5", "machine-readable outputs", "PASS",
                    "01_RAW/PROBE1-4_RAW.csv + EXTRACTION.json; "
                    "05_ANALYSIS/*.json (RECONCILIATION, PROBE1/2_CONTINGENCY,"
                    "PROBE3_FAMILIES, PROBE4_POSITION_STATS, PROBE4_CLUSTERS)"])
    log("[analyze] wrote 05_ANALYSIS + gates CSV; test rows: %d "
        "(executed with permutations: %d, constants: %d)"
        % (n_rows, n_executed, n_const))
    flush_log()


# ============================================================
# artifact index
# ============================================================

def write_artifact_index():
    rows = []
    rows.append(("00_Control/semantic_correlations_r1.py", "driver",
                 sha256_file(DRIVER_PATH)))
    for sub in ("01_RAW", "05_ANALYSIS", "06_Report"):
        d = os.path.join(RUN, sub)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            p = os.path.join(d, fn)
            if os.path.isfile(p):
                rows.append(("%s/%s" % (sub, fn), "artifact",
                             sha256_file(p)))
    rows.append(("source_of_truth_corpus",
                 "Models.bnt (READ-ONLY input)", MODELS_BNT_SHA256))
    with open(os.path.join(RUN, "artifact_index.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["artifact", "role", "sha256"])
        w.writerows(rows)
    log("[index] artifact_index.csv: %d rows" % len(rows))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True,
                    choices=["extract", "analyze", "all", "index"])
    args = ap.parse_args()
    verify_pins()
    if args.phase in ("extract", "all"):
        phase_extract()
    if args.phase in ("analyze", "all"):
        phase_analyze()
    if args.phase in ("all", "index"):
        write_artifact_index()
    flush_log()


if __name__ == "__main__":
    main()
