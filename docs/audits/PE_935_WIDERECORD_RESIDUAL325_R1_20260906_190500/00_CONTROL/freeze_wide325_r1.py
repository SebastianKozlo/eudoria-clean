#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FREEZE script - RUN E PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500.

Writes EVERY Section-3 freeze artifact to 00_CONTROL BEFORE any W1/W3
test execution: the verbatim W1/W3 grammar definitions (copied VERBATIM
from RUN C PE_NIF_MORPH_WIDERECORD_R1_20260906_170000 - its contract
404f7368... and driver b4fa818a... pinned first), the 325-key list with
hashes (the census-derived unknown-325 population; NO pinned artifact
lists the 325 keys individually - R20's NEITHER_CLASSIFICATION.json rows
lack bi/si, and K2's RESIDUAL333_SPANS.txt holds the SUPERSET 333 - so
the list is derived here by the K2 stage-1 census replica and is
re-derived + cross-checked in-driver), the split side lists, the NC
procedures, the a-priori gates, and the PREREG_MARKER.

NO W1/W3 grammar execution on the 325 occurs in this script. The census
replica executed here is the K2 stage-1 BASELINE (walk / r19 / backtrack
/ shift-scan classifiers on the corpus) - it is population derivation,
not a grammar test of W1/W3 (same pre-test baseline K2 and RUN C ran).

Standing sentence: no semantic claims; the +65 (RUN A) =
RETROSPECTIVE_VALIDATED; the +13 (RUN C) = RETROSPECTIVE_VALIDATED with
the family-concentration bounds; the H7 join-mechanism = UNVALIDATED
(RUN A) - NO H7-based claims; the residual-325 remains the heterogeneous
bucket this run only PROBES. Result classes: BYTE_MATCH / REPEATABILITY
/ RETROSPECTIVE_VALIDATION / RUNTIME_SEMANTICS (= explicitly NOT_TESTED
here, out of scope).
"""
import hashlib
import json
import os
import random
import struct
import sys
import time
from collections import Counter

sys.dont_write_bytecode = True  # protect READ-ONLY source trees

RUN = (r"D:\Eudoria_Reconstruction\99_Audits\PE_935_"
       r"WIDERECORD_RESIDUAL325_R1_20260906_190500")
CTRL = os.path.join(RUN, "00_CONTROL")
A = r"D:\Eudoria_Reconstruction\99_Audits"
K2_RUN = os.path.join(A, "PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209")
K2_CTRL = os.path.join(K2_RUN, "00_CONTROL")
RUNC_RUN = os.path.join(A, "PE_NIF_MORPH_WIDERECORD_R1_20260906_170000")
R61_SOURCE_DIR = os.path.join(A, r"PE_R61_FROZEN_BASELINE_20260828\01_source")
R61_SHA_JSON = os.path.join(
    A, r"PE_R61_FROZEN_BASELINE_20260828\03_validation\SHA256_SOURCE.json")
MODELS_935 = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"

# ---- input pins (READ-ONLY; verified before any derivation) --------------
PINS = {
    "CONTRACT": (os.path.join(CTRL, "CONTRACT.md"),
                 "da2843436e02d0148de8546e7e26a1a07afdb43699a61136dcbe09d705fdd7fd"),
    "K2_driver": (os.path.join(K2_CTRL, "morph_residual_deepdive_r1.py"),
                  "b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a"),
    "K2_COVERAGE_STATE": (os.path.join(K2_RUN, "05_ANALYSIS",
                                       "COVERAGE_STATE.json"),
                          "86c12fa7f3df1149213fbfdef3097f022bb7c7ba38dc2cf4289de4aab1b12fa4"),
    "K2_RESIDUAL333_SPANS": (os.path.join(K2_RUN, "01_RAW",
                                          "RESIDUAL333_SPANS.txt"),
                             "e936ed510cbfc6a8ab45b99d3ac7892d467b5d05b24a5ede606f80ddf7bf0100"),
    "K2_BASELINE_REPRODUCTION": (os.path.join(K2_RUN, "05_ANALYSIS",
                                              "BASELINE_REPRODUCTION.json"),
                                 "2e4014c9652df8adf6854b87c17388f9a5288c2c32dc757b34946320db46f1ca"),
    "RUNC_CONTRACT": (os.path.join(RUNC_RUN, "00_CONTROL", "CONTRACT.md"),
                      "404f73687913a5ee934ce123b6bd9588bc2427dfd7b73b2f217f1b21f6ff5f3e"),
    "RUNC_driver": (os.path.join(RUNC_RUN, "00_CONTROL",
                                 "widerecord_driver_r1.py"),
                    "b4fa818a7f7b42de565eb73837b1c10e368f021c3ab54f54146eb84cb499a714"),
    "RUNC_WIDE_GRAMMARS": (os.path.join(RUNC_RUN, "00_CONTROL",
                                        "WIDE_GRAMMARS.md"),
                           "3079ecabee7b95721668e24e4ff3845c11d76835d651379d81ac7ad2c0b8557e"),
    "R34_REAL_SPARSE_GRAMMAR": (
        os.path.join(A, r"PE_NIF_MORPH_QUANT_R34_20260904_164538\02_results"
                    r"\REAL_SPARSE_GRAMMAR.json"),
        "2c26ba86db44ad7a58322c136112fec36e23efab1db1fafea1c976311eba007e"),
    "MANIFEST_SCHEMA_SPEC": (
        os.path.join(A, r"PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500"
                    r"\00_CONTROL\MANIFEST_SCHEMA_SPEC.md"),
        None),  # existence + hash recorded (no contract pin)
}
MODELS_935_SHA = ("c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face"
                 "7e969be0b3d3bee0")
MODELS_935_ENTRIES = 5596
CONTRACT_SHA_EXPECT = PINS["CONTRACT"][1]

# K2 census anchors (the pinned K2 BASELINE_REPRODUCTION.json; asserted
# EXACTLY here and re-asserted in-driver).
K2_EXPECT_WALK = {"big_spans": 10274, "fits": 6167, "entries": 65050,
                  "pad_floats": 143874}
K2_EXPECT_RR = {"rr_spans": 2427, "var_exact_of_rr": 2093, "nofit": 334,
                "nofit_alt": 62, "nofit_none": 272}
K2_EXPECT_CORPUS = {"g1": 132, "g2": 1547, "var": 3186, "mscan_any": 3705}
K2_EXPECT_NEITHER = {"neither": 3438, "backtrack": 3105, "shift": 114,
                     "shift_only": 8, "unknown325": 325, "r21_unknown": 333,
                     "files": 56, "top_file": 84}
K2_EXPECT_PROBE = {"weight_pair": 41, "entry_density_mean": 0.4197,
                   "sane_frac_mean": 0.8096}
K2_EXPECT_BLOCKS = {"morph_blocks": 354, "blocks_with_tag": 334}

K2_FROZEN_BLOCK_RANGES = [
    ("B1_constants", 79, 83), ("B2_H4_WIN", 86, 86),
    ("B3_clean", 100, 103), ("B4_parse_fixed", 251, 285),
    ("B5_parse_variable", 288, 320), ("B6_nc2", 871, 882),
]

STANDING = ("Standing sentence: no semantic claims; the +65 (RUN A) = "
            "RETROSPECTIVE_VALIDATED; the +13 (RUN C) = "
            "RETROSPECTIVE_VALIDATED with the family-concentration bounds; "
            "the H7 join-mechanism = UNVALIDATED (RUN A) - NO H7-based "
            "claims; the residual-325 remains the heterogeneous bucket "
            "this run only PROBES. Result classes: BYTE_MATCH / "
            "REPEATABILITY / RETROSPECTIVE_VALIDATION / RUNTIME_SEMANTICS "
            "(= explicitly NOT_TESTED here, out of scope).")

K2 = None  # set by set_k2() before run_census


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        while True:
            b = fh.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def wr_json(path, obj):
    if not os.path.abspath(path).startswith(RUN):
        raise SystemExit("WRITE OUTSIDE RUN DIR: " + path)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=1, ensure_ascii=True)
        f.write("\n")


def wr_lines(path, lines):
    if not os.path.abspath(path).startswith(RUN):
        raise SystemExit("WRITE OUTSIDE RUN DIR: " + path)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(x if x.endswith("\n") else x + "\n" for x in lines))


def parse_dump_headers(path):
    ids = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("== "):
                head = line[3:].split()
                ids.append((head[0], int(head[1].split("=")[1]),
                            int(head[2].split("=")[1])))
    return ids


def read_bnt_index(data):
    fs = len(data)
    istart = struct.unpack_from("<I", data, fs - 8)[0]
    count = struct.unpack_from("<I", data, istart)[0]
    pos = istart + 4
    entries = []
    for _ in range(count):
        ne = pos
        while data[ne] != 0x0A:
            ne += 1
        name = data[pos:ne].decode("ascii")
        hdr = struct.unpack_from("<IIII", data, ne + 1)
        entries.append((name, hdr[0], hdr[1]))
        pos = ne + 17
    return entries


def set_k2(k2_module):
    global K2
    K2 = k2_module


# --------------------- census replica (RUN C run_census VERBATIM) -----------
def run_census(reader, entries, data, expect, era_label, r34_rows=None):
    """Replicates the K2 census pipeline EXACTLY (K2 driver stage 1; the
    RUN A/RUN C revalidation replica): R61 parse -> morph blocks with tag
    -> tag-split spans -> big spans -> R18 walk -> R34 grammar
    re-derivation (+ row agreement) -> rr/nofit census -> R20/R21
    residual census -> R21 probe. Population derivation ONLY - no W1/W3
    execution on the 325 anywhere in here."""
    big_spans = 0
    fits = 0
    entries_total = 0
    pads_total = 0
    morph_blocks = 0
    blocks_with_tag = 0
    parse_fail = 0
    fit_recs = []
    big_all = []
    blocks_ctx = {}

    for fi, (name, size, off) in enumerate(entries):
        if (fi + 1) % 1000 == 0:
            print("[freeze] %s parse %d/%d" % (era_label, fi + 1,
                                               len(entries)), flush=True)
        payload = data[off:off + size]
        res = reader.parse_bytes(payload, source_name=name)
        if res.parse_status != "PASS":
            parse_fail += 1
            continue
        for bi, b in enumerate(res.blocks):
            if b.block_type != "NiVertexMorphExtraData":
                continue
            morph_blocks += 1
            raw = b.raw_bytes or b""
            if len(raw) < 20:
                continue
            nl = struct.unpack_from("<i", raw, 0)[0]
            body = raw[4 + nl:]
            if len(body) < 7 or body[0] != 1:
                continue
            n = struct.unpack_from("<I", body, 1)[0]
            tag = struct.unpack_from("<H", body, 5)[0]
            if tag == 0:
                continue
            blocks_with_tag += 1
            rest = body[7:]
            tagb = struct.pack("<H", tag)
            spans = []
            i = 0
            while i < len(rest):
                j = rest.find(tagb, i + 2)
                if j < 0:
                    spans.append(rest[i:])
                    break
                spans.append(rest[i:j])
                i = j
            lens = Counter(len(s) for s in spans)
            if not lens:
                continue
            Wm = lens.most_common(1)[0][0]
            blocks_ctx[(name, bi)] = {"N": n, "tag": tag, "Wm": Wm,
                                      "spans": spans, "rest": rest}
            for si, s in enumerate(spans):
                L = len(s)
                if L <= Wm or L < 52:
                    continue
                big_spans += 1
                dp = s[2:]
                big_all.append({"file": name, "bi": bi, "si": si, "s": s,
                                "dp": dp, "N": n, "tag": tag, "Wm": Wm,
                                "L": L, "u": Wm - 2})
    if parse_fail != 0:
        raise CensusError("%s parse closure < 100%% (%d fails)"
                          % (era_label, parse_fail))
    print("[freeze] %s big spans: %d" % (era_label, big_spans), flush=True)

    for rec in big_all:  # greedy walk per big span (K2 census walk replica)
        dp = rec["dp"]
        u = rec["u"]
        n = rec["N"]
        i2 = u
        ok = True
        ent = 0
        padf = 0
        n_real = n_inrange = n_wp = 0
        while i2 < len(dp):
            took = False
            if i2 + 18 <= len(dp):
                idv = struct.unpack_from("<H", dp, i2)[0]
                if idv < 0x8000:
                    fl = [struct.unpack_from("<f", dp, i2 + 2 + 4 * k)[0]
                          for k in range(4)]
                    if all(K2.sane(v) for v in fl):
                        if idv != 0 and idv < n and i2 % 4 == 0 \
                                and K2.clean4(fl):
                            n_real += 1
                        if idv != 0 and idv < n:
                            n_inrange += 1
                            if abs((fl[0] + fl[1]) - 1.0) <= K2.WP_TOL:
                                n_wp += 1
                        ent += 1
                        i2 += 18
                        took = True
            if not took and i2 + 4 <= len(dp):
                v = struct.unpack_from("<f", dp, i2)[0]
                if K2.sane(v):
                    padf += 1
                    i2 += 4
                    took = True
            if not took:
                if ent > 0 and len(dp) - i2 == 2 \
                        and dp[i2:i2 + 2] == b"\x00\x00":
                    padf += 1
                    i2 = len(dp)
                    break
                ok = False
                break
        rec["walk_ok"] = bool(ok and ent > 0 and i2 == len(dp))
        if rec["walk_ok"]:
            fits += 1
            entries_total += ent
            pads_total += padf
            rec["n_real"] = n_real
            rec["n_wp_inrange"] = n_wp
            rec["has_real"] = n_real > 0
            fit_recs.append(rec)

    row_agree = 0
    row_disagree = 0
    g1_exact = g2_exact = var_exact = mscan_any = 0
    for rec in fit_recs:  # R34 grammar re-derivation per fit span
        dp = rec["dp"]
        u = rec["u"]
        N = rec["N"]
        Wm = rec["Wm"]
        W = (Wm - 2) // 4 if (Wm - 2) % 4 == 0 else None
        es_len = len(dp) - u
        g1_ok = g2_ok = 0
        ok_ms = []
        if W:
            g1_ok = 1 if K2.parse_fixed(dp, u, N, W)[0] else 0
            g2_ok = 1 if K2.parse_fixed(dp, u, N, W + 1)[0] else 0
        if es_len >= 6:
            for m in range(1, K2.MSCAN_MAX + 1):
                if es_len % (2 + 4 * m) != 0:
                    continue
                if K2.parse_fixed(dp, u, N, m)[0]:
                    ok_ms.append(m)
        v_ok, v_recs, v_kh, v_idxs = K2.parse_variable(dp, u, N)
        v_ok = 1 if (v_ok and v_recs > 0) else 0
        g1_exact += g1_ok
        g2_exact += g2_ok
        var_exact += v_ok
        if ok_ms:
            mscan_any += 1
        rec["W"] = W
        rec["es_len"] = es_len
        rec["g1_ok"] = g1_ok
        rec["g2_ok"] = g2_ok
        rec["mscan_ok_m"] = ok_ms
        rec["var_ok"] = v_ok
        rec["rr"] = bool(rec["has_real"] and rec["n_wp_inrange"] > 0)
        if r34_rows is not None:
            k = (rec["file"], rec["bi"], rec["si"])
            r = r34_rows.get(k)
            if (r is not None and r["g1_ok"] == g1_ok
                    and r["g2_ok"] == g2_ok
                    and r["var_ok"] == v_ok and r["mscan_ok_m"] == ok_ms
                    and bool(r["has_real"]) == rec["has_real"]
                    and r["n_wp_inrange"] == rec["n_wp_inrange"]):
                row_agree += 1
            else:
                row_disagree += 1

    rr_set = [r for r in fit_recs if r["rr"]]
    nofit = [r for r in rr_set if not r["var_ok"]]
    nofit_alt = [r for r in nofit
                 if r["g1_ok"] or r["g2_ok"] or r["mscan_ok_m"]]
    nofit_none = [r for r in nofit
                  if not (r["g1_ok"] or r["g2_ok"] or r["mscan_ok_m"])]
    rr_var = 0
    for r in rr_set:
        if r["var_ok"]:
            rr_var += 1

    neither = []
    r19_only = 0
    for rec in big_all:  # R20/R21 residual census
        if rec["walk_ok"]:
            continue
        if K2.fits_r19(rec["s"], rec["Wm"], rec["L"]):
            r19_only += 1
            continue
        neither.append(rec)
    bt_fit = 0
    shift_fit = 0
    shift_only = 0
    for rec in neither:
        t1 = K2.backtrack_r18(rec["dp"], rec["Wm"])
        t2 = K2.shift_scan(rec["s"], rec["Wm"], rec["L"]) is not None
        rec["bt"] = t1
        rec["sh"] = t2
        if t1:
            bt_fit += 1
        if t2:
            shift_fit += 1
        if t2 and not t1:
            shift_only += 1
    unknown325 = [r for r in neither if not r["bt"] and not r["sh"]]
    r21_unknown = [r for r in neither if not r["bt"]]
    u_by_file = Counter(r["file"] for r in unknown325)
    top = u_by_file.most_common(1)[0] if u_by_file else ("-", 0)

    wp_ok = 0  # R21 probe on r21_unknown
    eds = []
    sfs = []
    for rec in r21_unknown:
        dp = rec["dp"]
        if len(dp) >= 8:
            w0 = struct.unpack_from("<f", dp, 0)[0]
            w1 = struct.unpack_from("<f", dp, 4)[0]
            if abs(w0 + w1 - 1.0) < 1e-4:
                wp_ok += 1
        st = rec["u"]
        cnt = 0
        positions = 0
        p = st
        while p + 18 <= len(dp):
            positions += 1
            idv = struct.unpack_from("<H", dp, p)[0]
            if idv < 0x10000:
                fl = [struct.unpack_from("<f", dp, p + 2 + 4 * k)[0]
                      for k in range(4)]
                if all(K2.sane(v) for v in fl):
                    cnt += 1
            p += 2
        eds.append(cnt / max(positions, 1))
        sc = tot = 0
        p = 0
        while p + 4 <= len(dp):
            tot += 1
            if K2.sane(struct.unpack_from("<f", dp, p)[0]):
                sc += 1
            p += 4
        sfs.append(sc / max(tot, 1))
    ed_mean = round(sum(eds) / max(len(eds), 1), 4)
    sf_mean = round(sum(sfs) / max(len(sfs), 1), 4)

    census = {
        "walk": {"big_spans": big_spans, "fits": fits,
                 "entries": entries_total, "pad_floats": pads_total},
        "corpus_grammars": {"g1": g1_exact, "g2": g2_exact,
                            "var": var_exact, "mscan_any": mscan_any},
        "rr_state": {"rr_spans": len(rr_set), "var_exact_of_rr": rr_var,
                     "nofit": len(nofit), "nofit_alt": len(nofit_alt),
                     "nofit_none": len(nofit_none)},
        "residual": {"neither": len(neither), "backtrack": bt_fit,
                     "shift": shift_fit, "shift_only": shift_only,
                     "unknown325": len(unknown325),
                     "r21_unknown": len(r21_unknown), "r19_only": r19_only,
                     "files": len(u_by_file), "top_file": list(top)},
        "r21_probe": {"weight_pair": wp_ok,
                      "entry_density_mean": ed_mean,
                      "sane_frac_mean": sf_mean},
        "blocks": {"morph_blocks": morph_blocks,
                   "blocks_with_tag": blocks_with_tag},
        "row_agreement": [row_agree, len(fit_recs), row_disagree],
        "files_with_morph": len(set(r["file"] for r in big_all)),
    }
    checks = []
    if expect:
        for section, expvals in expect.items():
            got = census[section]
            for kk, vv in expvals.items():
                if section == "residual" and kk == "top_file":
                    gv = got["top_file"][1]
                else:
                    gv = got[kk]
                checks.append([section + "." + str(kk), gv, vv, gv == vv])
        census["census_checks"] = checks
        census["census_exact"] = all(c[3] for c in checks)
        if r34_rows is not None:
            census["census_exact"] = (census["census_exact"]
                                       and row_agree == len(fit_recs))
    return (census, big_all, fit_recs, nofit, unknown325, r21_unknown,
            blocks_ctx)


class CensusError(Exception):
    pass


# ------------------------------- main --------------------------------------
def main():
    t0 = time.time()
    print("[freeze] RUN E freeze: pins -> census -> freeze files", flush=True)

    # ---- pins ----
    for k, (p, exp) in PINS.items():
        if not os.path.isfile(p):
            raise SystemExit("PIN MISSING %s: %s" % (k, p))
        got = sha256_file(p)
        if exp is not None and got.lower() != exp.lower():
            raise SystemExit("PIN MISMATCH %s: %s" % (k, got))
        print("pin OK: %s %s" % (k, got[:12]), flush=True)
    with open(R61_SHA_JSON, "r", encoding="utf-8-sig") as f:
        locked = json.load(f)
    r61_ok = 0
    for name, sha in locked.items():
        if not name.endswith(".py"):
            continue
        got = sha256_file(os.path.join(R61_SOURCE_DIR, name))
        if got.lower() != str(sha).lower():
            raise SystemExit("R61 pin mismatch: " + name)
        r61_ok += 1
    if r61_ok != 10:
        raise SystemExit("R61 manifest incomplete (%d/10)" % r61_ok)
    print("pin OK: R61 10/10", flush=True)
    s935 = sha256_file(MODELS_935)
    if s935 != MODELS_935_SHA:
        raise SystemExit("corpus SHA mismatch: " + s935)
    print("pin OK: Models.bnt 9.3.5", flush=True)

    # the pinned K2 BASELINE_REPRODUCTION.json values == the frozen anchors
    with open(PINS["K2_BASELINE_REPRODUCTION"][0], encoding="utf-8") as f:
        k2_base = json.load(f)
    assert k2_base["walk"]["big_spans"] == K2_EXPECT_WALK["big_spans"]
    assert k2_base["walk"]["fits"] == K2_EXPECT_WALK["fits"]
    assert k2_base["walk"]["entries"] == K2_EXPECT_WALK["entries"]
    assert k2_base["walk"]["pad_floats"] == K2_EXPECT_WALK["pad_floats"]
    assert k2_base["r34_state"]["rr_spans"] == K2_EXPECT_RR["rr_spans"]
    assert k2_base["r34_state"]["var_exact_of_rr"] == K2_EXPECT_RR["var_exact_of_rr"]
    assert k2_base["r34_state"]["nofit"] == K2_EXPECT_RR["nofit"]
    assert k2_base["r34_state"]["nofit_alt"] == K2_EXPECT_RR["nofit_alt"]
    assert k2_base["r34_state"]["nofit_none"] == K2_EXPECT_RR["nofit_none"]
    assert k2_base["residual"]["shift_only"] == K2_EXPECT_NEITHER["shift_only"]
    assert k2_base["residual"]["unknown325"] == K2_EXPECT_NEITHER["unknown325"]
    assert k2_base["residual"]["r21_unknown"] == K2_EXPECT_NEITHER["r21_unknown"]
    assert k2_base["residual"]["files"] == K2_EXPECT_NEITHER["files"]
    assert k2_base["residual"]["top_file"][1] == K2_EXPECT_NEITHER["top_file"]
    print("[freeze] K2 baseline JSON == frozen anchors", flush=True)

    # ---- census (population derivation ONLY; NO W1/W3 execution) ----
    sys.path.insert(0, R61_SOURCE_DIR)
    from pe_nif_reader import PENifReader  # noqa: E402
    sys.path.insert(0, K2_CTRL)
    import morph_residual_deepdive_r1 as K2M  # noqa: E402
    set_k2(K2M)
    with open(MODELS_935, "rb") as f:
        data935 = f.read()
    ent935 = read_bnt_index(data935)
    if len(ent935) != MODELS_935_ENTRIES or \
            len(set(nm for nm, _, _ in ent935)) != MODELS_935_ENTRIES:
        raise SystemExit("corpus entry count mismatch: %d" % len(ent935))
    with open(PINS["R34_REAL_SPARSE_GRAMMAR"][0], encoding="utf-8") as f:
        r34 = json.load(f)
    r34_rows = {(r["file"], r["bi"], r["si"]): r for r in r34["per_span"]}
    expect935 = {
        "walk": K2_EXPECT_WALK, "rr_state": K2_EXPECT_RR,
        "corpus_grammars": K2_EXPECT_CORPUS, "residual": K2_EXPECT_NEITHER,
        "r21_probe": K2_EXPECT_PROBE, "blocks": K2_EXPECT_BLOCKS,
    }
    (census935, big_all, fit_recs, nofit, unknown325, r21_unknown,
     blocks_ctx) = run_census(PENifReader(), ent935, data935, expect935,
                              "9.3.5", r34_rows=r34_rows)
    if not census935["census_exact"]:
        raise SystemExit("CENSUS MISMATCH: "
                         + json.dumps(census935["census_checks"]))
    print("[freeze] census EXACT (row agreement %d/%d)"
          % (census935["row_agreement"][0], census935["row_agreement"][1]),
          flush=True)

    # ---- population derivation + cross-checks ----
    ru333 = sorted((r["file"], r["bi"], r["si"]) for r in r21_unknown)
    so8 = sorted((r["file"], r["bi"], r["si"]) for r in r21_unknown
                 if r["sh"] and not r["bt"])
    pop325 = sorted((r["file"], r["bi"], r["si"]) for r in unknown325)
    pinned333 = sorted(parse_dump_headers(
        PINS["K2_RESIDUAL333_SPANS"][0]))
    if len(pinned333) != 333 or pinned333 != ru333:
        raise SystemExit("pinned RESIDUAL333 dump != census r21_unknown "
                         "(%d vs %d)" % (len(pinned333), len(ru333)))
    if len(so8) != 8:
        raise SystemExit("shift_only != 8: %d" % len(so8))
    if len(pop325) != 325:
        raise SystemExit("unknown325 != 325: %d" % len(pop325))
    if len(pop325) + len(so8) != len(ru333) or len(ru333) != 333:
        raise SystemExit("325 + 8 != 333 EXACT failed")
    if set(pop325) & set(so8):
        raise SystemExit("unknown325 intersects shift_only")
    if set(pop325) | set(so8) != set(ru333):
        raise SystemExit("325 | 8 != 333 EXACT failed")
    with open(PINS["K2_COVERAGE_STATE"][0], encoding="utf-8") as f:
        k2_cov = json.load(f)
    canon = k2_cov["residual_census"]["canon"]
    if canon != "325 (of 333 R21-unknown; 56 files; 551564 x84)":
        raise SystemExit("K2 COVERAGE_STATE canon string mismatch: " + canon)
    u_by_file = Counter(k[0] for k in pop325)
    if len(u_by_file) != 56 or u_by_file["551564.nif"] != 84:
        raise SystemExit("325 population file census mismatch: %d files"
                         % len(u_by_file))
    print("[freeze] population: 333 - 8 shift-only = 325 EXACT "
          "(56 files; 551564.nif x84)", flush=True)

    # per-key records with hashes
    rec_by_key = {(r["file"], r["bi"], r["si"]): r for r in unknown325}
    per_key = []
    for k in pop325:
        r = rec_by_key[k]
        per_key.append({
            "file": k[0], "bi": k[1], "si": k[2], "N": r["N"],
            "tag": r["tag"], "Wm": r["Wm"], "L": r["L"], "u": r["u"],
            "dp_len": len(r["dp"]), "dp_sha256": sha256_bytes(r["dp"]),
            "previously_selected": False})

    # ---- split: file-level 50/50, seeded, family integrity ----
    files325 = sorted(set(k[0] for k in pop325))
    rng = random.Random(20260906)
    shuffled = list(files325)
    rng.shuffle(shuffled)
    n = len(shuffled)
    sideA = shuffled[:n // 2]
    sideB = shuffled[n // 2:]
    side_of = {}
    for f_ in sideA:
        side_of[f_] = "A"
    for f_ in sideB:
        side_of[f_] = "B"

    # ---- WIDE_GRAMMARS_325.md (W1/W3 VERBATIM from RUN C + K2 blocks) ----
    with open(PINS["K2_driver"][0], "r", encoding="utf-8", newline="") as f:
        k2_src = f.read().split("\n")
    blocks = K2_FROZEN_BLOCK_RANGES
    md = [
        "# WIDE_GRAMMARS_325.md - VERBATIM W1/W3 grammar freeze "
        "(PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500)", "",
        "The W1/W3 definitions are copied VERBATIM from RUN C "
        "PE_NIF_MORPH_WIDERECORD_R1_20260906_170000 (its CONTRACT.md "
        "sha256 404f73687913a5ee934ce123b6bd9588bc2427dfd7b73b2f217f1b21f"
        "6ff5f3e and its driver widerecord_driver_r1.py sha256 b4fa818a"
        "7f7b42de565eb73837b1c10e368f021c3ab54f54146eb84cb499a714 pinned "
        "first; both verified in-driver). The frozen grammar blocks "
        "below are the PINNED K2 driver `00_CONTROL/"
        "morph_residual_deepdive_r1.py` of "
        "PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209, SHA256 "
        "b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a "
        "(re-hashed at freeze time; the K2 manifest is DEFECTIVE and was "
        "NOT used as a hash source - every K2 artifact was re-hashed "
        "directly from bytes).", "",
        "Line ranges are 1-based inclusive ranges into that exact file. "
        "The driver byte-verifies each block against the pinned source "
        "BEFORE any test execution and imports the pinned module for "
        "execution, so the executed grammars ARE these frozen "
        "definitions. The driver also byte-verifies the W1/W3 definition "
        "lines and invocation-semantics items against RUN C's pinned "
        "WIDE_GRAMMARS.md (sha256 3079ecabee7b95721668e24e4ff3845c11d768"
        "35d651379d81ac7ad2c0b8557e). NO post-hoc variants; any "
        "additional probe must be labeled POST-HOC NON-COVERAGE and "
        "excluded from all coverage numbers. W2 (RUN C) is NOT part of "
        "this run's pre-registered set (this contract tests W1/W3 "
        "only); no W2 execution, no W2 claims.", "",
        STANDING, "",
        "## The pre-registered wide-record grammars (RUN C CONTRACT.md "
        "Section 3, VERBATIM; W1 and W3 only this run)", "",
        "- W1 = the fixed-m mscan unit [u16 idx][32 x f32] (m=32) with "
        "the head weight pair, consuming the span from the walk start.",
        "- W3 = W1 with a Wm mis-estimate window (Wm-64..Wm+64, step 4).",
        "",
        "## Frozen invocation semantics (RUN C operationalization, "
        "VERBATIM; items 1, 3, 4; the 325-specific item 5 replaces RUN "
        "C's 269-specific item 5)", "",
        "1. Walk start u = Wm - 2 (the K2/R34 census convention; dp = "
        "s[2:], Wm = the block's most-common span length). W1 executes "
        "K2.parse_fixed(dp, u, N, 32) VERBATIM (m = 32 = MSCAN_MAX; the "
        "head weight pair fl0+fl1~1.0 within WP_TOL is the parse_fixed "
        "head-pair semantics, counted as wp by the frozen unit; the fit "
        "predicate is the frozen unit's own: ok and recs > 0 - no "
        "additional constraint, no parameter change, no improvement).",
        "3. W3 executes K2.parse_fixed(dp, u + d, N, 32) VERBATIM over "
        "the frozen Wm mis-estimate window d in {-64, -60, ..., 0, ..., "
        "+60, +64} (Wm' = Wm + d, start u' = Wm' - 2; step 4; 33 "
        "positions INCLUDING d=0, so W3 is a superset of W1; scan order "
        "ascending from d=-64; the FIRST hitting offset is recorded; no "
        "per-span free parameter outside the frozen window). Fit = any "
        "window position yields ok and recs > 0.",
        "4. Negative controls (NC_PROCEDURES_325.md): per-span "
        "wrong-start trials at u+2 and u-2 (2 trials per span, explicit "
        "denominators), the SAME grammar executed at the wrong start; "
        "rate-vs-rate comparisons only.",
        "5. The 325 population: the 325 R21-unknown residual 9.3.5 "
        "morph keys (the census-verified unknown-325 population: fail "
        "greedy walk + r19 + backtrack + shift-scan; 333 R21-unknown "
        "MINUS 8 shift-only = 325 EXACT; 56 files; 551564.nif x84) "
        "(POPULATION_325.json); 333 - 8 = 325 asserted EXACTLY.",
        "",
    ]
    for label, lo, hi in blocks:
        seg = "\n".join(k2_src[lo - 1:hi])
        md += ["## %s (lines %d-%d)" % (label, lo, hi), "",
               "```python", seg, "```", ""]
    wr_lines(os.path.join(CTRL, "WIDE_GRAMMARS_325.md"), md)

    # ---- POPULATION_325.json ----
    pop = {
        "run": "PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500",
        "standing": STANDING,
        "result_class": "REPEATABILITY",
        "definition": ("the 325 R21-unknown residual 9.3.5 morph spans "
                       "(the K2 census unknown-325 population: fail "
                       "greedy walk + r19 + backtrack + shift-scan); "
                       "333 R21-unknown MINUS 8 shift-only = 325 EXACT; "
                       "56 files; 551564.nif x84"),
        "derivation_note": ("NO pinned artifact lists the 325 keys "
                           "individually (R20 NEITHER_CLASSIFICATION.json "
                           "rows lack bi/si; K2 RESIDUAL333_SPANS.txt "
                           "holds the SUPERSET 333) - the list is "
                           "derived by the K2 stage-1 census replica at "
                           "freeze time and re-derived + cross-checked "
                           "in-driver (G-CENSUS)"),
        "sources": {
            "K2_RESIDUAL333_SPANS.txt": {
                "path": PINS["K2_RESIDUAL333_SPANS"][0],
                "sha256": sha256_file(PINS["K2_RESIDUAL333_SPANS"][0])},
            "K2_COVERAGE_STATE.json": {
                "path": PINS["K2_COVERAGE_STATE"][0],
                "sha256": sha256_file(PINS["K2_COVERAGE_STATE"][0])},
            "K2_BASELINE_REPRODUCTION.json": {
                "path": PINS["K2_BASELINE_REPRODUCTION"][0],
                "sha256": sha256_file(PINS["K2_BASELINE_REPRODUCTION"][0])},
            "Models_bnt_935": {"path": MODELS_935, "sha256": s935},
        },
        "subtraction_lists": {
            "r21_unknown_333_keys": [list(k) for k in ru333],
            "shift_only_8_keys": [list(k) for k in so8],
            "assertion": "333 - 8 shift-only = 325 EXACT (asserted at "
                         "freeze and re-asserted in-driver post-census)"},
        "pop325_keys": [list(k) for k in pop325],
        "per_key": per_key,
        "n_files": len(files325),
        "file_histogram": dict(sorted(u_by_file.items())),
    }
    wr_json(os.path.join(CTRL, "POPULATION_325.json"), pop)

    # ---- NC_PROCEDURES_325.md ----
    wr_lines(os.path.join(CTRL, "NC_PROCEDURES_325.md"), [
        "# NC_PROCEDURES_325.md - negative-control procedures "
        "(frozen BEFORE any test execution)", "",
        "Seed discipline: deterministic (no sampling randomness needed; "
        "the wrong starts are pinned). Written to disk before any W1/W3 "
        "test execution.", "",
        "## NC-A (span level, full-325)", "",
        "- For EVERY span of the 325 population and EVERY grammar "
        "(W1, W3): 2 trials at the pinned wrong starts u+2 and u-2 "
        "(u = the walk start Wm-2).",
        "- Trial hit = the SAME grammar executed at the wrong start: W1 "
        "-> K2.parse_fixed(dp, u2, N, 32) ok and recs>0; W3 -> the W3 "
        "window anchored at u2 (offsets u2+d, d in -64..+64 step 4) "
        "any-hit.",
        "- Explicit denominator: spans x 2 = 325 x 2 = 650 per grammar. "
        "A trial with u2 < 0 is recorded as a NON-hit trial (reason "
        "INVALID_START_NONHIT) and stays in the denominator.",
        "- Rate = hits / 650. Compared to the full-325 positive rate "
        "(1 trial per span at the true start) as rate-vs-rate ONLY; "
        "raw-count cross-population comparisons FORBIDDEN.",
        "- Per-side (A/B) NC rates are computed and reported as "
        "TRANSPARENCY + G-CONCENTRATION disclosure inputs only (never "
        "gate inputs).", "",
        "## Vacuity guard", "",
        "THE VACUOUS CASE 0 >= 5x0 CANNOT PASS: NC denominator 0 => "
        "NC_EMPTY_DENOMINATOR non-pass; fewer than 5 fits => "
        "ZERO_FITS(<5) non-pass (checked BEFORE any separation "
        "comparison).", "",
        STANDING, "",
    ])

    # ---- SPLIT_SIDES_325.json ----
    split = {
        "run": "PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500",
        "standing": STANDING,
        "result_class": "REPEATABILITY",
        "procedure": ("file-level 50/50 of the 325-population's files; "
                      "random.Random(20260906) over the sorted file "
                      "list; rng.shuffle(copy); side_A = first n//2 "
                      "files; side_B = remaining files; FAMILY "
                      "INTEGRITY: all spans of a file land on the side "
                      "of its file; the split feeds G-CONCENTRATION "
                      "(per-side fit distribution ALWAYS reported) - "
                      "it is NOT a G-WIDE325 gate component this run"),
        "seed": 20260906,
        "n_files": n,
        "side_A_files": sideA,
        "side_B_files": sideB,
        "pop325_side_A": [list(k) for k in pop325
                          if side_of[k[0]] == "A"],
        "pop325_side_B": [list(k) for k in pop325
                          if side_of[k[0]] == "B"],
        "written_before_testing": True,
    }
    if len(split["pop325_side_A"]) + len(split["pop325_side_B"]) != 325:
        raise SystemExit("split side assignment does not cover the 325")
    wr_json(os.path.join(CTRL, "SPLIT_SIDES_325.json"), split)

    # ---- GATES_PREREGISTERED.md ----
    wr_lines(os.path.join(CTRL, "GATES_PREREGISTERED.md"), [
        "# GATES_PREREGISTERED.md - a-priori gates (CONTRACT.md Section 4 "
        "VERBATIM; fixed BEFORE any test execution; NEVER adjusted after "
        "seeing results)", "",
        "## G-PINS", "",
        "All pins in-driver; mismatch = HARD STOP.", "",
        "## G-CENSUS", "",
        "The K2 baseline reproduces (rr 2,427 / var 2,093 / nofit 334; "
        "unknown-325 = 325 across 56 files; 551564.nif x84); mismatch = "
        "HARD STOP.", "",
        "## G-WIDE325 (per grammar W1, W3 separately)", "",
        "PASS iff (full-325 fits >= 5) AND (full-325 rate >= 5x the "
        "matched-NC rate) AND (NC denominator > 0). A-PRIORI "
        "JUSTIFICATION (recorded): fits >= 5 (not 10) because this is a "
        "LOW-PREVALECE probe of a heterogeneous fragment bucket - 5+ "
        "fits with >= 5x separation and exact CIs establish the class's "
        "existence; fewer than 5 = the class ABSENT/RARE (a valid "
        "bound, not a failure). Report the exact binomial CI for every "
        "rate. THE VACUOUS CASE 0 >= 5x0 CANNOT PASS.",
        "NON-PASS classes: EMPTY_GROUP / ZERO_FITS(<5) / "
        "NC_EMPTY_DENOMINATOR / NC_INSUFFICIENT_SEPARATION(<5x).", "",
        "## G-CONCENTRATION (the RUN C lesson)", "",
        "The per-side/per-family fit distribution is ALWAYS reported; "
        "if ALL fits land on one split side or one file+block, the "
        "label CONCENTRATED is MANDATORY in every output (a disclosure "
        "class, not a gate failure by itself; the PASS stands only with "
        "the separation intact + the concentration disclosed).", "",
        "## G-EXEC", "",
        "Per-record outcomes only; zero size-derived validation numbers "
        "(the driver self-audit); the EIGHT negative fixtures "
        "fail-closed (the standard list): (1) zero successes both "
        "sides; (2) empty population; (3) only-previously-selected "
        "successes; (4) a duplicate present in both groups; (5) unequal "
        "denominators; (6) a corrupted record; (7) a malformed manifest "
        "row; (8) a missing input file.", "",
        "## G-SCOPE", "",
        "Read-only originals; zero payloads; run-local tooling only; "
        "the artifact_index per the spec + self-validation PASS.", "",
        "## Frozen operationalization decisions (fixed here, BEFORE any "
        "test execution)", "",
        "d1. 'full-325' components are MEMBER-level (the 325 spans; 1 "
        "positive trial per span at the true start; NC denominator "
        "spans x 2 = 650 per grammar). Per-side (A/B) fit/NC rates and "
        "per-(file,bi) fit distributions are TRANSPARENCY + "
        "G-CONCENTRATION disclosure inputs, never G-WIDE325 gate "
        "inputs (this contract has NO held-out conjunction).",
        "d2. '(NC denominator > 0)' is enforced on the per-span "
        "matched-NC denominator (650); 0 => NC_EMPTY_DENOMINATOR "
        "(fail-closed). With fits >= 5 > 0 and NC hits 0 over a "
        "positive denominator, the >= 5x separation test is satisfied "
        "(5x0 = 0 <= rate); this is NOT the vacuous case (the vacuous "
        "case is fits 0 AND NC 0, which cannot pass - ZERO_FITS is "
        "checked first).",
        "d3. Deterministic non-pass classification order (first match "
        "wins; every branch fail-closed): CORRUPTED_RECORD -> "
        "DUPLICATE_KEYS -> EMPTY_GROUP -> DENOMINATOR_MISMATCH -> "
        "NC_EMPTY_DENOMINATOR -> ZERO_FITS(<5) -> "
        "NC_INSUFFICIENT_SEPARATION(<5x).",
        "d4. Every fit/NC count is a counter increment over an EXECUTED "
        "record (per-record validation only; deriving any validation "
        "count from a group size is FORBIDDEN).",
        "d5. COVERAGE_DELTA.json: the 2,171/2,427 = 89.45% state stands "
        "(canon 2,093 + RUN A +65 RETROSPECTIVE_VALIDATED + RUN C +13 "
        "RETROSPECTIVE_VALIDATED with the family-concentration bounds); "
        "this run's additions X = the UNION of 325-spans consumed by "
        "grammars whose G-WIDE325 verdict is PASS, each labeled "
        "RETROSPECTIVE_VALIDATED (+ CONCENTRATED when d8 applies); the "
        "325 -> 325 - X. Consumed spans of non-pass grammars are "
        "recorded but EXCLUDED from every coverage number (the K2 "
        "OC-rejection precedent).",
        "d6. POST-HOC probes (if any) are labeled POST-HOC "
        "NON-COVERAGE and excluded from every number; this run "
        "executes NO post-hoc probe. ZERO_FITS is a VALID honest "
        "outcome - if the wide-record class is absent/rare in the 325 "
        "residual, that bound is reported plainly.",
        "d7. W2 (RUN C), H7 mechanisms, the 2003-era corpus and the "
        "R61 parser internals are OUT OF SCOPE (no execution, no "
        "claims; H7 = UNVALIDATED, NO H7-based claims).",
        "d8. G-CONCENTRATION: the per-side and per-(file,bi) fit "
        "distributions are ALWAYS reported; CONCENTRATED_SIDE (all "
        "fits on one split side) and CONCENTRATED_FAMILY (all fits on "
        "one file+block) labels are MANDATORY in every output when "
        "they hold; they are disclosure classes - a G-WIDE325 PASS "
        "stands only with the separation intact AND the concentration "
        "disclosed. Fixture 3's ONLY_PREVIOUSLY_SELECTED integrity "
        "guard: if every fitting member is flagged "
        "previously_selected=True the gate fails-closed (the real 325 "
        "members all carry previously_selected=False by population "
        "definition, so the guard is inert on real data).", "",
        STANDING, "",
    ])

    # ---- PREREG_MARKER.txt ----
    wr_lines(os.path.join(CTRL, "PREREG_MARKER.txt"), [
        "PRE-REGISTRATION / FREEZE COMPLETE %s"
        % time.strftime("%Y-%m-%d %H:%M:%S"),
        "RUN: PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500 (RUN_CLASS "
        "LOAD_BEARING; PE-MASTER loop bd17344b iteration 5; milestone "
        "EU935-M1, NO crossing).",
        "Grammars VERBATIM frozen (WIDE_GRAMMARS_325.md sha256 %s)"
        % sha256_file(os.path.join(CTRL, "WIDE_GRAMMARS_325.md")),
        "The 325-key list frozen (POPULATION_325.json sha256 %s)"
        % sha256_file(os.path.join(CTRL, "POPULATION_325.json")),
        "Split sides frozen (SPLIT_SIDES_325.json sha256 %s)"
        % sha256_file(os.path.join(CTRL, "SPLIT_SIDES_325.json")),
        "NC procedures frozen (NC_PROCEDURES_325.md sha256 %s)"
        % sha256_file(os.path.join(CTRL, "NC_PROCEDURES_325.md")),
        "Gates a-priori frozen (GATES_PREREGISTERED.md sha256 %s)"
        % sha256_file(os.path.join(CTRL, "GATES_PREREGISTERED.md")),
        "Assertions at freeze: 333 R21-unknown - 8 shift-only = 325 "
        "EXACT; 56 files; 551564.nif x84; the pinned K2 RESIDUAL333 dump "
        "== the census r21_unknown (333 headers EXACT); K2 baseline "
        "anchors reproduced EXACTLY (walk 10274/6167/65050/143874; rr "
        "2427 / var 2093 / nofit 334 = 62+272; neither 3438 / backtrack "
        "3105 / shift 114 / shift_only 8 / unknown325 325; probe "
        "41/0.4197/0.8096; row agreement 6167/6167).",
        "NO W1/W3 grammar test has been executed at freeze time. The "
        "census replica executed here is the K2 stage-1 BASELINE "
        "(population DERIVATION ONLY; the same pre-test baseline K2 and "
        "RUN C ran); the W1/W3 tests + NCs execute only in the driver, "
        "after this marker.",
        STANDING, "",
    ])
    print("[freeze] FREEZE COMPLETE in %.1fs" % (time.time() - t0))
    print("[freeze] 325 files: %d -> side A %d / side B %d"
          % (n, len(sideA), len(sideB)))
    print("[freeze] side A spans %d / side B spans %d"
          % (len(split["pop325_side_A"]), len(split["pop325_side_B"])))


if __name__ == "__main__":
    main()
