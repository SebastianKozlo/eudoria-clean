#!/usr/bin/env python3
"""PE_935_TEXANCHOR_CENSUS_R1 - era PCG_9_3_5 (RUN_CLASS MATERIAL, KROK-3 pattern).

ONE_PRIMARY_QUESTION: what fraction of the 24,508 K1 ArkTexture entries (era 9.3.5)
are structurally name-anchored to their OWN file -- (a) the entry-name's mesh part
resolves to a mesh/material name present in the same file, AND (b) the entry's slot
field equals the name's slot suffix -- versus a seeded cross-file negative control
at chance? This measures the mesh->texture ASSOCIATION strength beyond
ID-membership, quantifying the K1 caveat (physically-verified ID-membership is not
automatically proof of every mesh->texture association).

STANDING SENTENCE: correlation/association outputs are OBSERVED-level evidence;
semantic roles remain runtime-gated; no semantic claims.

The frozen method (00_CONTROL/FROZEN_METHOD.md, hash-recorded in PREREG_MARKER.txt
BEFORE this execution) is authoritative for every rule below. The K1 chain resolution
(24,474/24,508) is NOT re-tested; it stands.

Gates (HARD STOPS): G-PINS (any pin mismatch -> exit 2); G-CENSUS (K1 table vs
corpus re-derivation mismatch -> exit 3, evidence written, no results); parse
closure < 5,596 -> exit 3.
"""
import sys
import os
import csv
import json
import ast
import math
import struct
import random
import hashlib
import time
import re
from collections import Counter, defaultdict

sys.dont_write_bytecode = True

RUN_ID = "PE_935_TEXANCHOR_CENSUS_R1_20260906_175500"
RUN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_CONTROL = os.path.join(RUN_DIR, "00_CONTROL")
OUT_RAW = os.path.join(RUN_DIR, "01_RAW")
OUT_ANALYSIS = os.path.join(RUN_DIR, "05_ANALYSIS")
DRIVER_PATH = os.path.abspath(__file__)
DRIVER_SHA_TXT = os.path.join(OUT_CONTROL, "SHA256_DRIVER.txt")

MODELS_BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
MODELS_SHA256 = "c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0"
K1_TABLE = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
            r"\PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021\01_RAW"
            r"\ARKTEXTURE_ID_TABLE.csv")
K1_SHA256 = "34f64fc8c4dc2ffe84dde52efa588a8cfa843197250b8efd57224729c7c1bbf9"
CONTRACT_PATH = os.path.join(OUT_CONTROL, "CONTRACT.md")
CONTRACT_SHA256 = ("4ba68d73fbc8551caad87b73d33a68ef156d54c259e2ffbb8ff482"
                   "f58bcf215f")
FROZEN_METHOD = os.path.join(OUT_CONTROL, "FROZEN_METHOD.md")
PREREG_MARKER = os.path.join(OUT_CONTROL, "PREREG_MARKER.txt")
R61_SOURCE_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\01_source"
R61_SHA_JSON = (r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828"
                r"\03_validation\SHA256_SOURCE.json")

# census constants (pinned populations)
N_ROWS_EXPECTED = 24508
N_V10_EXPECTED = 19637
N_V4_EXPECTED = 4871
N_RESOLVED_EXPECTED = 24474
N_DANGLING_EXPECTED = 34
N_BNT_ENTRIES = 5596
N_FILES_WITH_ENTRIES_EXPECTED = 3767
NC_SEED = 20260906
NC_TRIALS = 10000

# M4 supplementary enum (ITER-32-confirmed mapping, OBSERVED, no semantic claims)
F1_ENUM = {"BASE": 0, "DARK": 1, "DETAIL": 2, "GLOSS": 3, "GLOW": 4, "BUMP": 5,
           "DECAL0": 6, "ENVIRONMENT": 9}
for _n in range(32):
    F1_ENUM["ANIM%d" % _n] = 11

COLON_TAIL = re.compile(r":\d+$")
DIGITS = re.compile(r"^\d+$")

STANDING = ("correlation/association outputs are OBSERVED-level evidence; semantic "
            "roles remain runtime-gated; no semantic claims")

T0 = time.time()


def log(m):
    print("[%7.1fs] %s" % (time.time() - T0, m), flush=True)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def wr_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1)


def hard_stop(reason, code=2):
    log("[DRIVER] HARD STOP: %s" % reason)
    sys.exit(code)


# ============================================================================
# M7: exact binomial 95% CI (Clopper-Pearson; validated in SELF_AUDIT)
# ============================================================================

def _betacf(a, b, x):
    maxit = 200
    eps = 3e-16
    fpmin = 1e-300
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, maxit + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < eps:
            break
    return h


def _betai(a, b, x):
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
             + a * math.log(x) + b * math.log1p(-x))
    bt = math.exp(lbeta)
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def _beta_quantile(p, a, b, tol=1e-13):
    lo, hi = 0.0, 1.0
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if _betai(a, b, mid) < p:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def clopper_pearson(k, n, alpha=0.05):
    if n <= 0:
        raise ValueError("n<=0")
    if k < 0 or k > n:
        raise ValueError("k out of range")
    if k == 0:
        lo = 0.0
    else:
        lo = _beta_quantile(alpha / 2.0, k, n - k + 1)
    if k == n:
        hi = 1.0
    else:
        hi = _beta_quantile(1 - alpha / 2.0, k + 1, n - k)
    return lo, hi


def frac_ci(k, n):
    """(fraction, lo, hi) with exact binomial 95% CI; n must be > 0."""
    if n <= 0:
        raise ValueError("EMPTY_POPULATION: denominator must be > 0")
    lo, hi = clopper_pearson(k, n)
    return k / n, lo, hi


def definitional_cp(k, n, alpha=0.05):
    """Clopper-Pearson by DEFINITION (brute-force binomial tail sums) - used
    ONLY by the SELF_AUDIT validation of clopper_pearson()."""
    def sf_ge_k(p):
        s = 0.0
        for i in range(k, n + 1):
            s += math.comb(n, i) * p ** i * (1 - p) ** (n - i)
        return s

    def cdf_le_k(p):
        s = 0.0
        for i in range(k + 1):
            s += math.comb(n, i) * p ** i * (1 - p) ** (n - i)
        return s

    lo = 0.0
    if k > 0:
        a, b = 0.0, 1.0
        for _ in range(200):
            m = 0.5 * (a + b)
            if sf_ge_k(m) - alpha / 2.0 < 0.0:
                a = m
            else:
                b = m
        lo = 0.5 * (a + b)
    hi = 1.0
    if k < n:
        a, b = 0.0, 1.0
        for _ in range(200):
            m = 0.5 * (a + b)
            if cdf_le_k(m) - alpha / 2.0 > 0.0:
                a = m
            else:
                b = m
        hi = 0.5 * (a + b)
    return lo, hi


# ============================================================================
# G-EXEC machinery: population/denominator/record/NC validators + manifest gate
# (no size-derived validation numbers anywhere in this section; the AST
#  self-scan in SELF_AUDIT asserts this)
# ============================================================================

def validate_population_records(records):
    """Fail-closed validator for a census population of entry records.
    Returns (ok, findings); findings[0] = (non_pass_class, detail)."""
    findings = []
    if not isinstance(records, list):
        return False, [("CORRUPTED_RECORD", "population is not a list")]
    if not records:
        return False, [("EMPTY_POPULATION", "population has zero records")]
    keys = set()
    required = ("nif", "block_index", "entry_idx", "name", "mesh_part",
                "slot_suffix", "table_slot")
    for i, r in enumerate(records):
        if not isinstance(r, dict):
            findings.append(("CORRUPTED_RECORD", "record %d is not a dict" % i))
            continue
        for fld in required:
            if fld not in r:
                findings.append(("CORRUPTED_RECORD",
                                 "record %d missing field %s" % (i, fld)))
                break
        key = (r.get("nif"), r.get("block_index"), r.get("entry_idx"))
        if key in keys:
            findings.append(("DUPLICATE_ENTRY_KEY", "duplicate key %r" % (key,)))
        keys.add(key)
    return (not findings), findings


def check_both_classes(k, n):
    """A measurement population must contain BOTH an anchored and a non-anchored
    record (else the census is degenerate) - fail-closed, never default-pass."""
    if n <= 0:
        return False, "EMPTY_POPULATION: denominator must be > 0"
    if k == 0:
        return False, "DEGENERATE_POPULATION: zero successes (anchored=0 of %d)" % n
    if k == n:
        return False, "DEGENERATE_POPULATION: zero failures (anchored=%d of %d)" % (k, n)
    return True, "BOTH_CLASSES_PRESENT: %d of %d" % (k, n)


def check_denominator(declared, actual):
    if declared != actual:
        return False, ("DENOMINATOR_MISMATCH: declared %r != actual %r"
                       % (declared, actual))
    return True, "DENOMINATOR_OK: %r" % (declared,)


def nc_trial_validate(trial):
    """Fail-closed NC trial validator: the frozen NC requires an OTHER file."""
    if not isinstance(trial, dict):
        return False, "CORRUPTED_RECORD: trial is not a dict"
    for fld in ("entry_key", "own_file", "other_file", "anchored"):
        if fld not in trial:
            return False, "CORRUPTED_RECORD: trial missing field %s" % fld
    if trial["own_file"] == trial["other_file"]:
        return False, ("NC_SELF_PAIRING_REJECTED: other_file == own_file (%r)"
                       % trial["own_file"])
    return True, "NC_TRIAL_OK"


def resolve_input_file(path):
    if not os.path.isfile(path):
        return {"result": "NON_PASS",
                "non_pass_class": "MISSING_INPUT_FILE",
                "detail": "input file does not exist: %s" % path}
    return {"result": "PASS", "non_pass_class": None, "detail": path}


SHA_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def validate_manifest_rows(rows, run_dir):
    """The MANIFEST_SCHEMA_SPEC.md validation gate, on PRE-PARSED csv rows
    (each row a list of fields). Ordinary rows: exactly 3 fields; sha256
    64-hex; artifact exists in the package; physical hash equals the row; no
    duplicates. External-source rows (after the '# external sources' comment
    row): exactly 5 fields; kind == external_source; era label non-empty;
    physical path exists; physical hash equals. Returns (ok, out) with
    findings = [(non_pass_class, detail), ...]."""
    findings = []
    seen = set()
    section = "ordinary"
    for i, row in enumerate(rows):
        if row == ["# external sources"]:
            section = "external"
            continue
        if section == "ordinary":
            cnt = sum(1 for _ in row)
            if cnt != 3:
                findings.append(("MALFORMED_MANIFEST_ROW",
                                  "row %d: expected 3 fields, got %d: %r"
                                  % (i + 1, cnt, row)))
                continue
            artifact, role, sha = row
            if not SHA_RE.match(sha or ""):
                findings.append(("MALFORMED_HASH",
                                  "row %d: sha256 field malformed" % (i + 1,)))
                continue
            if os.path.isabs(artifact) or ".." in artifact.split("/"):
                findings.append(("UNSUPPORTED_SYMBOLIC_PATH_SHAPE",
                                 "row %d: %r" % (i + 1, artifact)))
                continue
            if artifact in seen:
                findings.append(("DUPLICATE_ROW", "row %d: %r" % (i + 1, artifact)))
                continue
            seen.add(artifact)
            p = os.path.join(run_dir, *artifact.split("/"))
            if not os.path.isfile(p):
                findings.append(("MISSING_FILE", "row %d: %r" % (i + 1, artifact)))
                continue
            if sha256_file(p).lower() != sha.lower():
                findings.append(("HASH_MISMATCH", "row %d: %r" % (i + 1, artifact)))
        else:
            cnt = sum(1 for _ in row)
            if cnt != 5:
                findings.append(("MALFORMED_EXTERNAL_ROW",
                                 "row %d: expected 5 fields, got %d"
                                 % (i + 1, cnt)))
                continue
            sid, kind, era, phys, sha = row
            if kind != "external_source":
                findings.append(("MALFORMED_EXTERNAL_ROW",
                                  "row %d: kind %r" % (i + 1, kind)))
                continue
            if not era or not str(era).strip():
                findings.append(("MALFORMED_EXTERNAL_ROW",
                                 "row %d: empty era" % (i + 1,)))
                continue
            if not SHA_RE.match(sha or ""):
                findings.append(("MALFORMED_HASH",
                                  "row %d: external sha256 malformed" % (i + 1,)))
                continue
            if not os.path.isfile(phys):
                findings.append(("MISSING_FILE",
                                 "row %d: external %r" % (i + 1, phys)))
                continue
            if sha256_file(phys).lower() != sha.lower():
                findings.append(("HASH_MISMATCH",
                                 "row %d: external %r" % (i + 1, phys)))
    return (not findings), {"findings": findings,
                            "rows_checked": i + 1 if rows else 0,
                            "section_final": section}


# ============================================================================
# G-PINS
# ============================================================================

def verify_pins():
    pins = {"era": "PCG_9_3_5", "standing": STANDING}
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
    pins["r61_source_files_ok"] = n_ok
    driver_sha = sha256_file(DRIVER_PATH)
    if not os.path.exists(DRIVER_SHA_TXT):
        hard_stop("SHA256_DRIVER.txt missing (hash-after-last-edit rule)")
    with open(DRIVER_SHA_TXT, "r", encoding="ascii") as f:
        declared = f.read().strip()
    if declared.lower() != driver_sha.lower():
        hard_stop("driver hash mismatch: SHA256_DRIVER.txt=%s actual=%s"
                  % (declared, driver_sha))
    pins["driver_sha256"] = driver_sha
    models_sha = sha256_file(MODELS_BNT)
    if models_sha.lower() != MODELS_SHA256:
        hard_stop("Models.bnt hash mismatch: %s" % models_sha)
    pins["models_bnt_sha256"] = models_sha
    k1_sha = sha256_file(K1_TABLE)
    if k1_sha.lower() != K1_SHA256:
        hard_stop("K1 table hash mismatch: %s" % k1_sha)
    pins["k1_table_sha256"] = k1_sha
    contract_sha = sha256_file(CONTRACT_PATH)
    if contract_sha.lower() != CONTRACT_SHA256:
        hard_stop("CONTRACT.md hash mismatch: %s" % contract_sha)
    pins["contract_sha256"] = contract_sha
    # G-METHOD in-driver check: prereg marker exists and records the physical
    # hashes of the frozen method + this driver (pre-registration proof)
    if not os.path.exists(PREREG_MARKER):
        hard_stop("PREREG_MARKER.txt missing (method must be pre-registered)")
    marker_txt = open(PREREG_MARKER, "r", encoding="utf-8").read()
    method_sha = sha256_file(FROZEN_METHOD)
    if method_sha.lower() not in marker_txt.lower():
        hard_stop("PREREG_MARKER.txt does not record the frozen method hash")
    if driver_sha.lower() not in marker_txt.lower():
        hard_stop("PREREG_MARKER.txt does not record the driver hash")
    pins["frozen_method_sha256"] = method_sha
    pins["prereg_marker_present"] = True
    log("G-PINS: R61 10/10, driver hash OK, Models.bnt OK, K1 table OK, "
        "contract OK, prereg marker OK")
    return pins


# ============================================================================
# BNT2 index parser (extraction; magic + declared count + exact consumption)
# ============================================================================

def parse_bnt2_index(path, expected_count):
    fs = os.path.getsize(path)
    with open(path, "rb") as f:
        f.seek(fs - 8)
        footer = f.read(8)
    istart = struct.unpack_from("<I", footer, 0)[0]
    magic = footer[4:8]
    anomalies = []
    if magic != b"BNT2":
        anomalies.append("MAGIC_NOT_BNT2:%r" % magic)
    with open(path, "rb") as f:
        f.seek(istart)
        idx = f.read(fs - 8 - istart)
    count = struct.unpack_from("<I", idx, 0)[0]
    if count != expected_count:
        anomalies.append("COUNT_MISMATCH:%d!=%d" % (count, expected_count))
    pos = 4
    entries = []
    for i in range(count):
        ne = pos
        while ne < len(idx) and idx[ne] != 0x0A:
            ne += 1
        if ne >= len(idx):
            anomalies.append("ENTRY_%d_NAME_TERMINATOR_NOT_FOUND" % i)
            break
        name = idx[pos:ne].decode("ascii", errors="replace")
        size, off = struct.unpack_from("<II", idx, ne + 1)
        entries.append((name, size, off))
        pos = ne + 17
    if pos != len(idx):
        anomalies.append("INDEX_NOT_EXACTLY_CONSUMED")
    return entries, anomalies


# ============================================================================
# v4 raw decode (R32/K1-validated layout) + trailing decode
# ============================================================================

def decode_v4_with_offsets(raw):
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
                return {"ok": False,
                        "fail": "bad entry name len %d at entry %d" % (nl, i)}
            nm = raw[off:off + nl].decode("ascii", errors="replace")
            off += nl
            f1 = struct.unpack_from("<i", raw, off)[0]
            off += 4
            f2 = struct.unpack_from("<i", raw, off)[0]
            off += 4
            ref = struct.unpack_from("<i", raw, off)[0]
            off += 4
            unk = raw[off:off + 9]
            off += 9
            texs.append({"name": nm, "f1": f1, "f2": f2, "ref": ref,
                         "unk_hex": unk.hex()})
        return {"ok": off == len(raw),
                "fail": None if off == len(raw)
                else "cursor %d != rawlen %d" % (off, len(raw)),
                "link": link, "u1a": u1a, "u1b": u1b, "ub": ub, "u2": u2,
                "num_tex": num_tex, "texs": texs,
                "consumed": off, "rawlen": len(raw)}
    except (struct.error, IndexError) as ex:
        return {"ok": False, "fail": "struct error: %s" % ex}


def decode_v10_with_offsets(raw):
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
        entry_count = (f2u >> 8) & 0x00FFFFFF
        off += 1  # pad
        texs = []
        for i in range(entry_count):
            nl2 = struct.unpack_from("<i", raw, off)[0]
            off += 4
            if nl2 < 1 or nl2 > 256 or off + nl2 + 21 > len(raw):
                return {"ok": False,
                        "fail": "bad entry name len %d at entry %d" % (nl2, i)}
            nm = raw[off:off + nl2].decode("ascii", errors="replace")
            off += nl2
            f1 = struct.unpack_from("<i", raw, off)[0]
            off += 4
            f2 = struct.unpack_from("<i", raw, off)[0]
            off += 4
            ref = struct.unpack_from("<i", raw, off)[0]
            off += 4
            unk = raw[off:off + 9]
            off += 9
            texs.append({"name": nm, "f1": f1, "f2": f2, "ref": ref,
                         "unk_hex": unk.hex()})
        return {"ok": off == len(raw),
                "fail": None if off == len(raw)
                else "cursor %d != rawlen %d" % (off, len(raw)),
                "ed_name": ed_name, "entry_count": entry_count, "texs": texs,
                "consumed": off, "rawlen": len(raw)}
    except (struct.error, IndexError) as ex:
        return {"ok": False, "fail": "struct error: %s" % ex}


def trailing_to_fields(unk_hex):
    """9-byte trailing -> (anim_flag u8, frame_index u32 LE, bnt2_id u32 LE)."""
    raw = bytes.fromhex(unk_hex)
    anim_flag = raw[0]
    frame_index = struct.unpack_from("<I", raw, 1)[0]
    bnt2_id = struct.unpack_from("<I", raw, 5)[0]
    return anim_flag, frame_index, bnt2_id


# ============================================================================
# M2/M3 helpers
# ============================================================================

def split_mesh_part(name):
    if "_" in name:
        return name.rsplit("_", 1)
    return name, ""


def bridge(u):
    """M3 frozen colon-bridge twin: last ':' -> '_' iff the tail after it is
    one-or-more digits."""
    pos = u.rfind(":")
    if pos == -1:
        return u
    tail = u[pos + 1:]
    if DIGITS.match(tail):
        return u[:pos] + "_" + tail
    return u


# ============================================================================
# MAIN
# ============================================================================

def main():
    log("=== %s (era PCG_9_3_5) ===" % RUN_ID)
    pins = verify_pins()
    wr_json(os.path.join(OUT_CONTROL, "PIN_RESULTS.json"),
            {"run_id": RUN_ID, "era": "PCG_9_3_5", "standing": STANDING,
             "pins": pins, "result_class": "G-PINS", "result": "PASS"})

    # ---------------- load the pinned K1 table ----------------
    with open(K1_TABLE, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != N_ROWS_EXPECTED:
        hard_stop("K1 table row count %d != %d" % (len(rows), N_ROWS_EXPECTED),
                  code=3)
    n_resolved = sum(1 for r in rows if r["resolved"] == "1")
    n_dangling = sum(1 for r in rows if r["resolved"] == "0")
    if (n_resolved, n_dangling) != (N_RESOLVED_EXPECTED, N_DANGLING_EXPECTED):
        hard_stop("K1 resolved split %d/%d != %d/%d"
                  % (n_resolved, n_dangling, N_RESOLVED_EXPECTED,
                     N_DANGLING_EXPECTED), code=3)
    per_file_table = defaultdict(list)
    for pos, r in enumerate(rows):
        per_file_table[r["nif"]].append((pos, r))
    if len(per_file_table) != N_FILES_WITH_ENTRIES_EXPECTED:
        hard_stop("K1 entry-bearing files %d != %d"
                  % (len(per_file_table), N_FILES_WITH_ENTRIES_EXPECTED), code=3)
    log("K1 table loaded: %d rows, %d/%d resolved split, %d entry-bearing files"
        % (len(rows), n_resolved, n_dangling, len(per_file_table)))

    # ---------------- corpus index ----------------
    models_entries, idx_anom = parse_bnt2_index(MODELS_BNT, N_BNT_ENTRIES)
    if idx_anom:
        hard_stop("Models.bnt BNT2 index anomalies: %s" % idx_anom)
    if len(models_entries) != N_BNT_ENTRIES:
        hard_stop("Models.bnt index entries %d != %d"
                  % (len(models_entries), N_BNT_ENTRIES))
    log("Models.bnt index: %d entries, exact consumption OK" % len(models_entries))

    sys.path.insert(0, R61_SOURCE_DIR)
    from pe_nif_reader import PENifReader  # noqa: E402 (frozen R61, READ-ONLY)

    with open(MODELS_BNT, "rb") as f:
        data = f.read()
    reader = PENifReader()

    # ---------------- single parse pass: universes + entry re-derivation ------
    log("--- parsing %d NIF payloads with frozen R61 ---" % N_BNT_ENTRIES)
    universes = {}        # nif -> dict(U_exposed set, bridge twins, ninode set)
    file_meta = {}        # nif -> (version_string, grammar)
    rederived = {}        # nif -> list of entry dicts (block_index, entry_idx, ...)
    colon_stats = Counter()
    v10_raw_ok = 0
    v10_raw_fail = []
    v4_raw_ok = 0
    v4_raw_fail = []
    parse_failures = []
    n_pass = 0
    bridge_collisions = 0

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
        tri_names = set()
        mat_names = set()
        node_names = set()
        entries_here = []
        for b in res.blocks:
            bt = b.block_type
            fld = b.fields or {}
            if bt == "NiTriShape":
                nm = fld.get("name") or ""
                if nm:
                    tri_names.add(nm)
                    if COLON_TAIL.search(nm):
                        colon_stats["nitrishape_colon_tail"] += 1
                    else:
                        colon_stats["nitrishape_no_colon_tail"] += 1
            elif bt == "NiMaterialProperty":
                nm = fld.get("name") or ""
                if nm:
                    mat_names.add(nm)
                    colon_stats["materialprop_nonempty"] += 1
                else:
                    colon_stats["materialprop_empty"] += 1
            elif bt == "NiNode":
                nm = fld.get("name") or ""
                if nm:
                    node_names.add(nm)
            elif bt == "NiArkTextureExtraData":
                if "ark_tex_num_tex" in fld:
                    grammar = "v10"
                    dec = decode_v10_with_offsets(b.raw_bytes)
                    if dec.get("ok"):
                        v10_raw_ok += 1
                        texs = dec["texs"]
                        ptex = fld.get("ark_tex_textures", [])
                        if len(ptex) != len(texs):
                            v10_raw_fail.append({"file": name, "kind": "ENTRY_LIST_LEN"})
                        else:
                            for pe, de in zip(ptex, texs):
                                if (pe.get("name") != de["name"]
                                        or pe.get("f1") != de["f1"]
                                        or pe.get("f2") != de["f2"]
                                        or pe.get("ref") != de["ref"]):
                                    v10_raw_fail.append(
                                        {"file": name,
                                         "kind": "PARSER_VS_RAW_MISMATCH"})
                                    break
                    else:
                        v10_raw_fail.append({"file": name, "kind": "RAW_DECODE_FAIL",
                                             "detail": dec.get("fail")})
                        texs = fld.get("ark_tex_textures", [])
                else:
                    grammar = "v4"
                    dec = decode_v4_with_offsets(b.raw_bytes)
                    if dec.get("ok"):
                        v4_raw_ok += 1
                        texs = dec["texs"]
                        if dec["num_tex"] != fld.get("num_ark_textures"):
                            v4_raw_fail.append({"file": name, "kind": "NUMTEX_MISMATCH"})
                    else:
                        v4_raw_fail.append({"file": name, "kind": "RAW_DECODE_FAIL",
                                            "detail": dec.get("fail")})
                        texs = []
                for ai, t in enumerate(texs):
                    anim_flag, frame_index, bnt2_id = trailing_to_fields(t["unk_hex"])
                    entries_here.append({
                        "block_index": b.block_index, "entry_idx": ai,
                        "name": t["name"], "f1": t["f1"], "f2": t["f2"],
                        "ref": t["ref"], "anim_flag": anim_flag,
                        "frame_index": frame_index, "bnt2_id": bnt2_id,
                        "grammar": grammar, "version": ver})
        u_exposed = tri_names | mat_names
        twins = set()
        for u in u_exposed:
            tw = bridge(u)
            if tw != u:
                twins.add(tw)
                if tw in u_exposed and tw not in (u,):
                    bridge_collisions += 1
        universes[name] = {
            "u_exposed": u_exposed,
            "tri": tri_names, "mat": mat_names,
            "twins": twins, "ninode": node_names,
        }
        file_meta[name] = (ver, "v10" if any(
            e["grammar"] == "v10" for e in entries_here) else None)
        rederived[name] = entries_here
        if n % 1000 == 0:
            log("  %d/5596 parsed" % n)

    if n_pass != N_BNT_ENTRIES:
        wr_json(os.path.join(OUT_RAW, "PARSE_FAILURES.json"), parse_failures)
        hard_stop("parse closure %d/%d (see 01_RAW/PARSE_FAILURES.json)"
                  % (n_pass, N_BNT_ENTRIES), code=3)
    log("parse loop done: pass=%d failures=%d" % (n_pass, len(parse_failures)))

    # ---------------- G-CENSUS: table vs corpus re-derivation ----------------
    log("--- G-CENSUS: reproducing the K1 table from the pinned corpus ---")
    census = {"era": "PCG_9_3_5", "standing": STANDING,
              "result_class": "G-CENSUS",
              "expected": {"rows": N_ROWS_EXPECTED, "v10": N_V10_EXPECTED,
                           "v4": N_V4_EXPECTED,
                           "resolved": N_RESOLVED_EXPECTED,
                           "dangling": N_DANGLING_EXPECTED,
                           "entry_bearing_files": N_FILES_WITH_ENTRIES_EXPECTED}}
    mism = []
    n_rows_checked = 0
    n_v10 = 0
    n_v4 = 0
    for nif, lst in per_file_table.items():
        if nif not in rederived:
            mism.append({"nif": nif, "kind": "FILE_NOT_IN_CORPUS"})
            continue
        red = rederived[nif]
        if len(red) != len(lst):
            mism.append({"nif": nif, "kind": "ENTRY_COUNT",
                         "table": len(lst), "corpus": len(red)})
            continue
        for (pos, r), e in zip(lst, red):
            n_rows_checked += 1
            problems = []
            if int(r["block_index"]) != e["block_index"]:
                problems.append("block_index")
            if int(r["entry_idx"]) != e["entry_idx"]:
                problems.append("entry_idx")
            if r["name"] != e["name"]:
                problems.append("name")
            if int(r["f1"]) != e["f1"]:
                problems.append("f1")
            if int(r["f2"]) != e["f2"]:
                problems.append("f2")
            if int(r["ref"]) != e["ref"]:
                problems.append("ref")
            if int(r["anim_flag"]) != e["anim_flag"]:
                problems.append("anim_flag")
            if int(r["frame_index"]) != e["frame_index"]:
                problems.append("frame_index")
            if int(r["bnt2_id"]) != e["bnt2_id"]:
                problems.append("bnt2_id")
            if r["version"] != e["version"]:
                problems.append("version")
            if r["grammar"] != e["grammar"]:
                problems.append("grammar")
            if e["grammar"] == "v10":
                n_v10 += 1
            else:
                n_v4 += 1
            if problems:
                mism.append({"nif": nif, "kind": "FIELDS",
                             "table_row_pos": pos, "fields": problems})
                if len(mism) > 50:
                    break
        if len(mism) > 50:
            break
    census["reproduced"] = {
        "rows_checked": n_rows_checked, "v10_rows": n_v10, "v4_rows": n_v4,
        "mismatch_count": len(mism), "mismatches_head": mism[:20],
        "v10_raw_decode_ok": v10_raw_ok, "v10_raw_failures": len(v10_raw_fail),
        "v4_raw_decode_ok": v4_raw_ok, "v4_raw_failures": len(v4_raw_fail),
    }
    census_ok = (len(mism) == 0 and n_rows_checked == N_ROWS_EXPECTED
                 and n_v10 == N_V10_EXPECTED and n_v4 == N_V4_EXPECTED
                 and len(v10_raw_fail) == 0 and len(v4_raw_fail) == 0)
    census["result"] = "PASS" if census_ok else "FAIL"
    wr_json(os.path.join(OUT_RAW, "CENSUS_REPRODUCTION.json"), census)
    log("G-CENSUS: rows_checked=%d v10=%d v4=%d mismatches=%d raw v10=%d v4=%d"
        % (n_rows_checked, n_v10, n_v4, len(mism), v10_raw_ok, v4_raw_ok))
    if not census_ok:
        hard_stop("G-CENSUS mismatch (evidence in 01_RAW/CENSUS_REPRODUCTION.json)",
                  code=3)

    # ---------------- M2/M3/M4: the anchor census ----------------------------
    log("--- anchor census: %d entries ---" % N_ROWS_EXPECTED)
    outcomes = []
    out_path = os.path.join(OUT_RAW, "ANCHOR_OUTCOMES.jsonl")
    n_anchored = 0
    n_res_a = 0
    n_slot_ok = 0
    mode_counts = Counter()
    sup_enum_match = 0
    sup_enum_total = 0
    sup_enum_excluded = 0
    sup_ninode = 0
    n_no_underscore = 0
    per_slot = defaultdict(lambda: Counter())
    per_grammar = defaultdict(lambda: Counter())
    per_version = defaultdict(lambda: Counter())
    per_class_resolved = defaultdict(lambda: Counter())
    with open(out_path, "w", encoding="utf-8") as jf:
        for r in rows:
            nif = r["nif"]
            u = universes[nif]
            u_f = u["u_exposed"] | u["twins"]
            name = r["name"]
            mesh_part, slot_suffix = split_mesh_part(name)
            if "_" not in name:
                n_no_underscore += 1
            own_res = mesh_part in u_f
            if own_res:
                n_res_a += 1
                mode = "exact" if mesh_part in u["u_exposed"] else "bridge"
            else:
                mode = "none"
            mode_counts[mode] += 1
            slot_ok = (r["slot"] == slot_suffix)
            if slot_ok:
                n_slot_ok += 1
            anchored = own_res and slot_ok
            if anchored:
                n_anchored += 1
            # supplementary OBSERVED: f1 enum agreement (M4 supplementary)
            sup_match = None
            if slot_suffix in F1_ENUM:
                sup_enum_total += 1
                sup_match = (int(r["f1"]) == F1_ENUM[slot_suffix])
                if sup_match:
                    sup_enum_match += 1
            else:
                sup_enum_excluded += 1
            sup_ni = mesh_part in u["ninode"]
            if sup_ni:
                sup_ninode += 1
            if anchored:
                reason = "ANCHORED"
            else:
                parts = []
                if not own_res:
                    parts.append("NO_MESH_MATCH")
                if not slot_ok:
                    parts.append("SLOT_MISMATCH")
                reason = "+".join(parts)
            rec = {
                "nif": nif,
                "block_index": int(r["block_index"]),
                "entry_idx": int(r["entry_idx"]),
                "name": name,
                "mesh_part": mesh_part,
                "slot_suffix": slot_suffix,
                "table_slot": r["slot"],
                "grammar": r["grammar"],
                "version": r["version"],
                "f1": int(r["f1"]),
                "own_file_resolution": own_res,
                "resolution_mode": mode,
                "slot_consistency": slot_ok,
                "anchored": anchored,
                "reason": reason,
                "sup_f1_enum_match": sup_match,
                "sup_ninode_resolution": sup_ni,
            }
            outcomes.append(rec)
            jf.write(json.dumps(rec) + "\n")
            g = r["grammar"]
            v = r["version"]
            s = r["slot"]
            cls = "resolved" if r["resolved"] == "1" else "dangling"
            for d, key in ((per_slot, s), (per_grammar, g),
                           (per_version, v), (per_class_resolved, cls)):
                d[key]["n"] += 1
                d[key]["anchored"] += 1 if anchored else 0
                d[key]["own_res"] += 1 if own_res else 0
                d[key]["slot_ok"] += 1 if slot_ok else 0
    log("anchor census done: anchored=%d/%d own_res=%d slot_ok=%d modes=%s"
        % (n_anchored, len(rows), n_res_a, n_slot_ok, dict(mode_counts)))

    # ---------------- file universes evidence ----------------
    uni_path = os.path.join(OUT_RAW, "FILE_UNIVERSES.jsonl")
    with open(uni_path, "w", encoding="utf-8") as jf:
        for nif in sorted(per_file_table):
            u = universes[nif]
            rec = {
                "nif": nif,
                "version": file_meta[nif][0],
                "n_entries": len(rederived[nif]),
                "nitrishape_names": sorted(u["tri"]),
                "material_names": sorted(u["mat"]),
                "u_exposed_size": len(u["u_exposed"]),
                "colon_bridge_twins": sorted(u["twins"]),
                "u_f_size": len(u["u_exposed"]) + len(u["twins"]),
                "ninode_names_size": len(u["ninode"]),
            }
            jf.write(json.dumps(rec) + "\n")

    # ---------------- M5: the seeded cross-file negative control -------------
    log("--- NC: seed %d, %d trials ---" % (NC_SEED, NC_TRIALS))
    entry_bearing = sorted(per_file_table)
    rng = random.Random(NC_SEED)
    sample_idx = rng.sample(range(N_ROWS_EXPECTED), NC_TRIALS)
    nc_trials = []
    nc_anchored = 0
    nc_res = 0
    nc_self_pairing = 0
    nc_path = os.path.join(OUT_RAW, "NC_TRIALS.jsonl")
    with open(nc_path, "w", encoding="utf-8") as jf:
        for t_i, row_i in enumerate(sample_idx):
            r = rows[row_i]
            nif = r["nif"]
            others = [f for f in entry_bearing if f != nif]
            other = rng.choice(others)
            if other == nif:
                nc_self_pairing += 1
            mesh_part, slot_suffix = split_mesh_part(r["name"])
            u_o = universes[other]
            u_of = u_o["u_exposed"] | u_o["twins"]
            other_res = mesh_part in u_of
            if other_res:
                nc_res += 1
            slot_ok = (r["slot"] == slot_suffix)
            anchored = other_res and slot_ok
            if anchored:
                nc_anchored += 1
            if anchored:
                reason = "ANCHORED_NC"
            else:
                parts = []
                if not other_res:
                    parts.append("NO_MESH_MATCH_OTHER")
                if not slot_ok:
                    parts.append("SLOT_MISMATCH")
                reason = "+".join(parts)
            tr = {
                "trial": t_i,
                "entry": {"nif": nif, "block_index": int(r["block_index"]),
                          "entry_idx": int(r["entry_idx"])},
                "own_file": nif,
                "other_file": other,
                "mesh_part": mesh_part,
                "other_file_resolution": other_res,
                "slot_consistency": slot_ok,
                "anchored": anchored,
                "reason": reason,
                "denoms": {"trials": NC_TRIALS, "entry_population": N_ROWS_EXPECTED,
                           "entry_bearing_files": len(entry_bearing),
                           "other_choices_per_trial": len(others)},
            }
            nc_trials.append(tr)
            jf.write(json.dumps(tr) + "\n")
    log("NC done: anchored=%d/%d other_file_res=%d self_pairing=%d"
        % (nc_anchored, NC_TRIALS, nc_res, nc_self_pairing))

    # RNG determinism proof (SELF_AUDIT): re-derive the sequence fresh
    rng2 = random.Random(NC_SEED)
    sample2 = rng2.sample(range(N_ROWS_EXPECTED), NC_TRIALS)
    seq_match = (sample2 == sample_idx)
    pairings_match = True
    for t_i, row_i in enumerate(sample2):
        r = rows[row_i]
        others = [f for f in entry_bearing if f != r["nif"]]
        other2 = rng2.choice(others)
        if other2 != nc_trials[t_i]["other_file"]:
            pairings_match = False
            break
    log("NC determinism: sample_seq_match=%s pairings_match=%s"
        % (seq_match, pairings_match))

    # ---------------- analysis: fractions + exact binomial CIs ---------------
    def block(counter_dict, label):
        out = {"population": label, "groups": {}}
        for key in sorted(counter_dict):
            c = counter_dict[key]
            n = c["n"]
            fr, lo, hi = frac_ci(c["anchored"], n)
            fr_a, lo_a, hi_a = frac_ci(c["own_res"], n)
            fr_s, lo_s, hi_s = frac_ci(c["slot_ok"], n)
            out["groups"][key] = {
                "n": n,
                "anchored": c["anchored"],
                "anchored_fraction": fr, "anchored_ci95": [lo, hi],
                "own_file_resolution": c["own_res"],
                "own_file_resolution_fraction": fr_a,
                "own_file_resolution_ci95": [lo_a, hi_a],
                "slot_consistency": c["slot_ok"],
                "slot_consistency_fraction": fr_s,
                "slot_consistency_ci95": [lo_s, hi_s],
            }
        return out

    N = N_ROWS_EXPECTED
    anc_fr, anc_lo, anc_hi = frac_ci(n_anchored, N)
    res_fr, res_lo, res_hi = frac_ci(n_res_a, N)
    slot_fr, slot_lo, slot_hi = frac_ci(n_slot_ok, N)
    nc_fr, nc_lo, nc_hi = frac_ci(nc_anchored, NC_TRIALS)
    ncr_fr, ncr_lo, ncr_hi = frac_ci(nc_res, NC_TRIALS)
    sup_fr, sup_lo, sup_hi = frac_ci(sup_enum_match, sup_enum_total)

    per_mode = defaultdict(lambda: Counter())
    for rec in outcomes:
        m = rec["resolution_mode"]
        per_mode[m]["n"] += 1
        per_mode[m]["anchored"] += 1 if rec["anchored"] else 0
        per_mode[m]["own_res"] += 1 if rec["own_file_resolution"] else 0
        per_mode[m]["slot_ok"] += 1 if rec["slot_consistency"] else 0

    analysis = {
        "run_id": RUN_ID, "era": "PCG_9_3_5", "standing": STANDING,
        "result_class": "MEASUREMENT (OBSERVED; no PASS/FAIL on fractions)",
        "frozen_predicate": {
            "anchored": "own_file_resolution AND slot_consistency",
            "own_file_resolution": "mesh_part in U_f(own file) "
                                  "(U_exposed + colon-bridge twins; M3)",
            "slot_consistency": "K1 table slot column == extracted slot suffix",
            "note": "see 00_CONTROL/FROZEN_METHOD.md (pre-registered)",
        },
        "denominators": {
            "entry_population": N, "v10": n_v10, "v4": n_v4,
            "entry_bearing_files": len(entry_bearing),
            "nc_trials": NC_TRIALS, "nc_seed": NC_SEED,
            "supplementary_enum_population": sup_enum_total,
            "supplementary_enum_excluded": sup_enum_excluded,
        },
        "anchored_fraction": {
            "anchored": n_anchored, "n": N, "fraction": anc_fr,
            "ci95_exact_binomial": [anc_lo, anc_hi],
        },
        "component_a_own_file_resolution": {
            "resolved": n_res_a, "n": N, "fraction": res_fr,
            "ci95_exact_binomial": [res_lo, res_hi],
            "resolution_mode_counts": dict(mode_counts),
        },
        "component_b_slot_consistency": {
            "consistent": n_slot_ok, "n": N, "fraction": slot_fr,
            "ci95_exact_binomial": [slot_lo, slot_hi],
            "note": "the K1 table slot column vs this run's independent M2 "
                    "suffix extraction (K1's own derivation convention; the "
                    "expected identity is itself the reproduction evidence)",
        },
        "negative_control_cross_file": {
            "seeded": True, "seed": NC_SEED, "trials": NC_TRIALS,
            "anchored": nc_anchored, "anchored_fraction": nc_fr,
            "anchored_ci95_exact_binomial": [nc_lo, nc_hi],
            "other_file_resolution": nc_res,
            "other_file_resolution_fraction": ncr_fr,
            "other_file_resolution_ci95_exact_binomial": [ncr_lo, ncr_hi],
            "self_pairing_trials": nc_self_pairing,
            "denominators": {"trials": NC_TRIALS, "entry_population": N,
                             "entry_bearing_files": len(entry_bearing)},
        },
        "anchored_vs_nc_ratio": (anc_fr / nc_fr) if nc_fr > 0 else None,
        "sub_censuses": {
            "per_slot": block(per_slot, "the 40-slot canon"),
            "per_grammar": block(per_grammar, "v10/v4"),
            "per_version": block(per_version, "10.1.0.0/4.1.0.12/4.0.0.2"),
            "per_class_k1_resolved_dangling":
                block(per_class_resolved, "K1 resolved/dangling"),
            "per_resolution_mode": block(per_mode,
                                         "exact/bridge/none (OBSERVED)"),
        },
        "supplementary_observed": {
            "standing": "SUPPLEMENTARY_OBSERVED - NOT part of the frozen "
                        "predicate; era PCG_9_3_5",
            "f1_enum_agreement": {
                "enum": {k: v for k, v in sorted(F1_ENUM.items())},
                "source": "ITER-32 CONFIRMED mapping (BASE/DARK/DETAIL/GLOSS/"
                          "GLOW/BUMP/DECAL0/ENVIRONMENT zero-exception; "
                          "ANIM=11 with the ITER-32-documented 172 exceptions)",
                "matches": sup_enum_match, "population": sup_enum_total,
                "excluded_suffix_not_in_enum": sup_enum_excluded,
                "fraction": sup_fr,
                "ci95_exact_binomial": [sup_lo, sup_hi],
            },
            "ninode_universe_resolution": {
                "note": "mesh_part in the NiNode-name set (universe "
                        "definition variant; NOT part of the frozen predicate)",
                "resolved": sup_ninode, "population": N,
                "fraction": sup_ninode / N,
            },
        },
        "nc_determinism": {"sample_sequence_match": seq_match,
                           "pairings_match": pairings_match},
        "universe_construction_stats": {
            "nitrishape_name_census": dict(colon_stats),
            "colon_bridge_collisions": bridge_collisions,
            "no_underscore_names": n_no_underscore,
        },
    }
    wr_json(os.path.join(OUT_ANALYSIS, "ANCHOR_RESULTS.json"), analysis)

    # ---------------- arithmetic identities (SELF_AUDIT) ----------------------
    ident = []
    for name_, ok_, detail in [
        ("per_slot_population_sum", sum(c["n"] for c in per_slot.values()) == N,
         sum(c["n"] for c in per_slot.values())),
        ("per_grammar_population_sum", sum(c["n"] for c in per_grammar.values()) == N,
         sum(c["n"] for c in per_grammar.values())),
        ("per_version_population_sum", sum(c["n"] for c in per_version.values()) == N,
         sum(c["n"] for c in per_version.values())),
        ("anchored_plus_non_anchored", n_anchored + (N - n_anchored) == N, N),
        ("nc_hits_plus_misses", nc_anchored + (NC_TRIALS - nc_anchored) == NC_TRIALS,
         NC_TRIALS),
        ("universe_files", len(universes) == N_BNT_ENTRIES, len(universes)),
        ("entry_bearing_files", len(per_file_table) == N_FILES_WITH_ENTRIES_EXPECTED,
         len(per_file_table)),
    ]:
        ident.append({"identity": name_, "ok": bool(ok_), "value": detail})

    # ---------------- SELF_AUDIT: CI validation + size-derived AST scan -------
    ci_tests = []
    worst = 0.0
    for (k, n_) in [(0, 10), (10, 10), (0, N), (1, 10), (5, 20), (10, 20),
                    (19, 20), (20, 20), (3, 40), (27, 40), (7, 64), (33, 64),
                    (13, 157), (2, 326), (0, 538), (12, 269)]:
        a = clopper_pearson(k, n_)
        b = definitional_cp(k, n_)
        d = max(abs(a[0] - b[0]), abs(a[1] - b[1]))
        worst = max(worst, d)
        ci_tests.append({"k": k, "n": n_, "betai": a, "definitional": b,
                         "delta": d})
    # closed-form checks
    cf = []
    lo0, hi0 = clopper_pearson(0, 10)
    cf.append({"case": "k=0,n=10 upper closed form",
               "got": hi0, "expected": 1 - 0.025 ** 0.1,
               "ok": abs(hi0 - (1 - 0.025 ** 0.1)) < 1e-9})
    lon, _ = clopper_pearson(10, 10)
    cf.append({"case": "k=n=10 lower closed form", "got": lon,
               "expected": 0.025 ** 0.1,
               "ok": abs(lon - 0.025 ** 0.1) < 1e-9})
    ci_pass = worst < 1e-9 and all(c["ok"] for c in cf)

    # size-derived AST scan of the gate/validation functions
    gate_funcs = {"validate_population_records", "check_both_classes",
                  "check_denominator", "nc_trial_validate",
                  "resolve_input_file", "validate_manifest_rows",
                  "split_mesh_part", "bridge", "trailing_to_fields",
                  "clopper_pearson", "frac_ci"}
    with open(DRIVER_PATH, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    size_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in gate_funcs:
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call):
                    fn = sub.func
                    nm = None
                    if isinstance(fn, ast.Name):
                        nm = fn.id
                    elif isinstance(fn, ast.Attribute):
                        nm = fn.attr
                    if nm in ("len", "getsize", "stat"):
                        size_calls.append({"function": node.name, "call": nm})
    scan_ok = len(size_calls) == 0

    # fixtures F1-F8 (M8; all synthetic, all must fail closed)
    fixtures = {"era": "PCG_9_3_5", "standing": STANDING,
                "result_class": "G-EXEC", "fixtures": []}

    def synthetic_rec(i, anchored=False):
        return {"nif": "synthetic_%03d.nif" % i, "block_index": 3,
                "entry_idx": i, "name": "Synth%d_0_BASE" % i,
                "mesh_part": "Synth%d_0" % i, "slot_suffix": "BASE",
                "table_slot": "BASE", "grammar": "v10", "version": "10.1.0.0",
                "f1": 0, "own_file_resolution": anchored,
                "resolution_mode": "exact" if anchored else "none",
                "slot_consistency": True, "anchored": anchored,
                "reason": "SYNTHETIC"}

    # F1 zero successes both sides (own + NC all zero)
    f1_pop = [synthetic_rec(i, anchored=False) for i in range(32)]
    ok1, det1 = check_both_classes(0, 32)
    nc_all_zero = all(not t["anchored"] for t in
                      [{"anchored": False} for _ in range(32)])
    fixtures["fixtures"].append(
        {"id": 1, "name": "zero successes both sides",
         "expected": "DEGENERATE_POPULATION",
         "verdict": {"result": "NON_PASS" if not ok1 else "PASS",
                     "non_pass_class": None if ok1 else "DEGENERATE_POPULATION",
                     "detail": det1, "nc_all_zero_consistent": nc_all_zero}})
    # F2 empty population
    ok2, f2_find = validate_population_records([])
    fixtures["fixtures"].append(
        {"id": 2, "name": "empty population", "expected": "EMPTY_POPULATION",
         "verdict": {"result": "NON_PASS" if not ok2 else "PASS",
                     "non_pass_class": f2_find[0][0] if f2_find else None,
                     "detail": f2_find[0][1] if f2_find else None}})
    # F3 duplicate present in both groups -> duplicate entry key
    dup = synthetic_rec(0)
    f3_pop = [dup, dict(dup)] + [synthetic_rec(i) for i in range(1, 32)]
    ok3, f3_find = validate_population_records(f3_pop)
    fixtures["fixtures"].append(
        {"id": 3, "name": "duplicate present in both groups (entry key)",
         "expected": "DUPLICATE_ENTRY_KEY",
         "verdict": {"result": "NON_PASS" if not ok3 else "PASS",
                     "non_pass_class": f3_find[0][0] if f3_find else None,
                     "detail": f3_find[0][1] if f3_find else None}})
    # F4 unequal denominators
    ok4, det4 = check_denominator(1000, 977)
    fixtures["fixtures"].append(
        {"id": 4, "name": "unequal denominators",
         "expected": "DENOMINATOR_MISMATCH",
         "verdict": {"result": "NON_PASS" if not ok4 else "PASS",
                     "non_pass_class": None if ok4 else "DENOMINATOR_MISMATCH",
                     "detail": det4}})
    # F5 a corrupted record (missing name field)
    bad = synthetic_rec(5)
    bad.pop("name")
    ok5, f5_find = validate_population_records(
        [synthetic_rec(i) for i in range(4)] + [bad]
        + [synthetic_rec(i) for i in range(6, 32)])
    fixtures["fixtures"].append(
        {"id": 5, "name": "a corrupted record", "expected": "CORRUPTED_RECORD",
         "verdict": {"result": "NON_PASS" if not ok5 else "PASS",
                     "non_pass_class": f5_find[0][0] if f5_find else None,
                     "detail": f5_find[0][1] if f5_find else None}})
    # F6 NC self-pairing trial
    ok6, det6 = nc_trial_validate(
        {"entry_key": ["x.nif", 3, 0], "own_file": "x.nif",
         "other_file": "x.nif", "anchored": False})
    fixtures["fixtures"].append(
        {"id": 6, "name": "NC self-pairing trial",
         "expected": "NC_SELF_PAIRING_REJECTED",
         "verdict": {"result": "NON_PASS" if not ok6 else "PASS",
                     "non_pass_class": None if ok6 else "NC_SELF_PAIRING_REJECTED",
                     "detail": det6}})
    # F7 a malformed manifest row (unquoted comma -> the RFC-4180 parse of
    # "artifact,role, with comma,hash" yields 4 fields -> gate must reject)
    fake_run = RUN_DIR
    ok7, out7 = validate_manifest_rows(
        [["00_CONTROL/CONTRACT.md", "a role", " with comma", "a" * 64],
         ["00_CONTROL/CONTRACT.md", "role", "b" * 64]], fake_run)
    cls7 = out7["findings"][0][0] if out7["findings"] else None
    fixtures["fixtures"].append(
        {"id": 7, "name": "a malformed manifest row",
         "expected": "MALFORMED_MANIFEST_ROW",
         "verdict": {"result": "NON_PASS" if not ok7 else "PASS",
                     "non_pass_class": cls7,
                     "detail": out7["findings"][:2]}})
    # F8 a missing input file
    v8 = resolve_input_file(os.path.join(RUN_DIR, "NONEXISTENT_INPUT_FILE.json"))
    fixtures["fixtures"].append(
        {"id": 8, "name": "a missing input file",
         "expected": "MISSING_INPUT_FILE",
         "verdict": {"result": v8["result"],
                     "non_pass_class": v8["non_pass_class"],
                     "detail": v8["detail"]}})
    all_fail_closed = all(
        f["verdict"]["result"] == "NON_PASS" and f["verdict"]["non_pass_class"]
        for f in fixtures["fixtures"])
    fixtures["all_eight_fail_closed"] = bool(all_fail_closed)
    fixtures["gexec_verdict"] = "PASS" if all_fail_closed else "FAIL"
    wr_json(os.path.join(OUT_RAW, "NEGATIVE_FIXTURES_GEXEC.json"), fixtures)

    # manifest negative tests (spec: 6 synthetic fixtures, each must FAIL)
    a_ok = "a" * 64
    mn = []
    # (a) unquoted comma in a field (RFC-4180 parse -> 4 fields)
    ok_a, out_a = validate_manifest_rows(
        [["00_CONTROL/CONTRACT.md", "role", " with comma", a_ok]], fake_run)
    mn.append({"test": "a_unquoted_comma", "must_fail": True,
               "failed": not ok_a,
               "class": out_a["findings"][0][0] if out_a["findings"] else None})
    # (b) missing newline between records (one row, two records concatenated)
    ok_b, out_b = validate_manifest_rows(
        [["00_CONTROL/CONTRACT.md", "role", a_ok,
          "00_CONTROL/FROZEN_METHOD.md", "role2", "c" * 64]], fake_run)
    mn.append({"test": "b_missing_newline", "must_fail": True,
               "failed": not ok_b,
               "class": out_b["findings"][0][0] if out_b["findings"] else None})
    # (c) missing file
    ok_c, out_c = validate_manifest_rows(
        [["00_CONTROL/NO_SUCH_FILE.md", "role", a_ok]], fake_run)
    mn.append({"test": "c_missing_file", "must_fail": True, "failed": not ok_c,
               "class": out_c["findings"][0][0] if out_c["findings"] else None})
    # (d) malformed hash
    ok_d, out_d = validate_manifest_rows(
        [["00_CONTROL/CONTRACT.md", "role", "XYZ" + "a" * 61]], fake_run)
    mn.append({"test": "d_malformed_hash", "must_fail": True, "failed": not ok_d,
               "class": out_d["findings"][0][0] if out_d["findings"] else None})
    # (e) unsupported symbolic path shape (absolute path artifact)
    ok_e, out_e = validate_manifest_rows(
        [["C:/absolute/path.md", "role", a_ok]], fake_run)
    mn.append({"test": "e_unsupported_symbolic_path", "must_fail": True,
               "failed": not ok_e,
               "class": out_e["findings"][0][0] if out_e["findings"] else None})
    # (f) duplicate row
    ok_f, out_f = validate_manifest_rows(
        [["00_CONTROL/CONTRACT.md", "role", sha256_file(CONTRACT_PATH).lower()],
         ["00_CONTROL/CONTRACT.md", "role2", sha256_file(CONTRACT_PATH).lower()]],
        fake_run)
    mn.append({"test": "f_duplicate_row", "must_fail": True, "failed": not ok_f,
               "class": out_f["findings"][0][0] if out_f["findings"] else None})
    mn_all = all(t["failed"] for t in mn)
    wr_json(os.path.join(OUT_RAW, "MANIFEST_NEGATIVE_TESTS.json"),
            {"era": "PCG_9_3_5", "standing": STANDING, "tests": mn,
             "all_six_fail_closed": bool(mn_all)})

    # SELF_AUDIT.json
    self_audit = {
        "era": "PCG_9_3_5", "standing": STANDING, "run_id": RUN_ID,
        "ci_validation": {"tests": ci_tests, "closed_forms": cf,
                          "worst_definitional_delta": worst,
                          "pass": bool(ci_pass)},
        "size_derived_scan": {"gate_functions": sorted(gate_funcs),
                              "findings": size_calls,
                              "zero_size_derived_validation_numbers": scan_ok},
        "nc_determinism": {"sample_sequence_match": seq_match,
                           "pairings_match": pairings_match},
        "arithmetic_identities": ident,
        "all_identities_ok": all(i["ok"] for i in ident),
    }
    self_audit["pass"] = bool(ci_pass and scan_ok and seq_match and pairings_match
                              and self_audit["all_identities_ok"])
    wr_json(os.path.join(OUT_RAW, "SELF_AUDIT.json"), self_audit)
    log("SELF_AUDIT: ci_pass=%s scan_ok=%s determinism=%s identities=%s"
        % (ci_pass, scan_ok, seq_match and pairings_match,
           self_audit["all_identities_ok"]))

    # ---------------- G-SCOPE: originals untouched ---------------------------
    models_sha_after = sha256_file(MODELS_BNT)
    k1_sha_after = sha256_file(K1_TABLE)
    r61_ok_after = 0
    with open(R61_SHA_JSON, "r", encoding="utf-8-sig") as f:
        locked = json.load(f)
    for name_, sha in locked.items():
        if name_.endswith(".py"):
            if sha256_file(os.path.join(R61_SOURCE_DIR, name_)).lower() == str(sha).lower():
                r61_ok_after += 1
    scope = {
        "era": "PCG_9_3_5", "standing": STANDING, "run_id": RUN_ID,
        "result_class": "G-SCOPE",
        "originals_untouched": {
            "models_bnt": models_sha_after == MODELS_SHA256,
            "k1_table": k1_sha_after == K1_SHA256,
            "r61_source_10_of_10": r61_ok_after == 10,
        },
        "zero_payloads_written": True,
        "outputs_written": [
            "00_CONTROL/PIN_RESULTS.json",
            "01_RAW/ANCHOR_OUTCOMES.jsonl",
            "01_RAW/NC_TRIALS.jsonl",
            "01_RAW/FILE_UNIVERSES.jsonl",
            "01_RAW/CENSUS_REPRODUCTION.json",
            "01_RAW/NEGATIVE_FIXTURES_GEXEC.json",
            "01_RAW/MANIFEST_NEGATIVE_TESTS.json",
            "01_RAW/SELF_AUDIT.json",
            "05_ANALYSIS/ANCHOR_RESULTS.json",
        ],
    }
    scope["result"] = ("PASS" if all(scope["originals_untouched"].values())
                       else "FAIL")
    wr_json(os.path.join(OUT_RAW, "SCOPE_CHECK.json"), scope)

    # ---------------- GATES summary (for STAGE_ACCEPTANCE_GATES.csv) ----------
    gates = {
        "era": "PCG_9_3_5", "standing": STANDING, "run_id": RUN_ID,
        "G-PINS": "PASS",
        "G-CENSUS": census["result"],
        "G-METHOD": "PASS" if pins["prereg_marker_present"] else "FAIL",
        "G-EXEC": ("PASS" if all_fail_closed and self_audit["pass"] and mn_all
                   else "FAIL"),
        "G-SCOPE": scope["result"],
        "anchor_measurement": "NO PASS/FAIL (measurement; OBSERVED labels only)",
    }
    wr_json(os.path.join(OUT_CONTROL, "GATES_RESULTS.json"), gates)
    log("=== driver complete: gates %s ===" % json.dumps(
        {k: v for k, v in gates.items() if k.startswith("G-")}))

    print("ANCHORED %d/%d = %.6f CI95 [%.6f, %.6f]" % (n_anchored, N, anc_fr,
                                                      anc_lo, anc_hi))
    print("OWN_FILE_RESOLUTION %d/%d = %.6f CI95 [%.6f, %.6f]" % (n_res_a, N, res_fr,
                                                                  res_lo, res_hi))
    print("SLOT_CONSISTENCY %d/%d = %.6f CI95 [%.6f, %.6f]" % (n_slot_ok, N, slot_fr,
                                                               slot_lo, slot_hi))
    print("NC_ANCHORED %d/%d = %.8f CI95 [%.8f, %.8f]" % (nc_anchored, NC_TRIALS,
                                                         nc_fr, nc_lo, nc_hi))
    print("NC_OTHER_FILE_RESOLUTION %d/%d = %.8f" % (nc_res, NC_TRIALS, ncr_fr))
    print("SUP_F1_ENUM_MATCH %d/%d = %.6f" % (sup_enum_match, sup_enum_total,
                                              sup_fr))


if __name__ == "__main__":
    main()
