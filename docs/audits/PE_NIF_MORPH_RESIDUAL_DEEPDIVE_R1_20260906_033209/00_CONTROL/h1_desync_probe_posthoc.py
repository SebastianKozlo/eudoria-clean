#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""POST-HOC CHARACTERIZATION PROBE (NON-COVERAGE) — PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1.

Labeled POST-HOC: designed AFTER seeing H1 characterization results; adds
NO coverage (the pre-registered predicates are untouched); its purpose is
to mechanically identify WHY the 23 all-paired alt-fit spans fail var-k
(smallest-k selection desync vs record-width mismatch), completing H1's
"extract what those grammars are" mandate for the falsification list.

Read-only on the corpus; writes 01_RAW/H1_DESYNC_PROBE.json only.
"""
import sys
import os
import json
import struct
from collections import Counter

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
RUN = REPO + r"\docs\audits\PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209"
MODELS_BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
R61_SOURCE_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\01_source"
R61_SHA_JSON = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\03_validation\SHA256_SOURCE.json"
import hashlib

WP_TOL = 1e-4


def sane(v):
    return v == v and (v == 0 or 1e-45 < abs(v) < 1e6)


def clean(v):
    if v != v or abs(v) >= 1e6:
        return False
    return v == 0.0 or abs(v) >= 2.0 ** -126


def main():
    with open(R61_SHA_JSON, "r", encoding="utf-8-sig") as f:
        locked = json.load(f)
    for name, sha in locked.items():
        if not name.endswith(".py"):
            continue
        with open(os.path.join(R61_SOURCE_DIR, name), "rb") as fh:
            if hashlib.sha256(fh.read()).hexdigest().lower() != str(sha).lower():
                raise RuntimeError("R61 mismatch")
    sys.path.insert(0, R61_SOURCE_DIR)
    from pe_nif_reader import PENifReader

    with open(MODELS_BNT, "rb") as f:
        data = f.read()
    fs = len(data)
    istart = struct.unpack_from("<I", data, fs - 8)[0]
    count = struct.unpack_from("<I", data, istart)[0]
    pos = istart + 4
    bnt = []
    for _ in range(count):
        ne = pos
        while data[ne] != 0x0A:
            ne += 1
        bnt.append((data[pos:ne].decode("ascii"),
                    struct.unpack_from("<IIII", data, ne + 1)[0],
                    struct.unpack_from("<IIII", data, ne + 1)[1]))
        pos = ne + 17
    reader = PENifReader()
    nofit = []
    for name, size, off in bnt:
        payload = data[off:off + size]
        res = reader.parse_bytes(payload, source_name=name)
        for bi, b in enumerate(res.blocks):
            if b.block_type != "NiVertexMorphExtraData":
                continue
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
            for si, s in enumerate(spans):
                L = len(s)
                if L <= Wm or L < 52:
                    continue
                dp = s[2:]
                u = Wm - 2
                # reproduce walk fit + REAL/WP counters (R34 predicates)
                i2 = u
                ok = True
                ent = 0
                n_real = n_wp = 0
                while i2 < len(dp):
                    took = False
                    if i2 + 18 <= len(dp):
                        idv = struct.unpack_from("<H", dp, i2)[0]
                        if idv < 0x8000:
                            fl = [struct.unpack_from("<f", dp, i2 + 2 + 4 * k)[0] for k in range(4)]
                            if all(sane(v) for v in fl):
                                if idv != 0 and idv < n and i2 % 4 == 0 and all(clean(v) for v in fl):
                                    n_real += 1
                                if idv != 0 and idv < n and abs((fl[0] + fl[1]) - 1.0) <= WP_TOL:
                                    n_wp += 1
                                ent += 1
                                i2 += 18
                                took = True
                    if not took and i2 + 4 <= len(dp):
                        v = struct.unpack_from("<f", dp, i2)[0]
                        if sane(v):
                            i2 += 4
                            took = True
                    if not took:
                        if ent > 0 and len(dp) - i2 == 2 and dp[i2:i2 + 2] == b"\x00\x00":
                            i2 = len(dp)
                            break
                        ok = False
                        break
                if not (ok and ent > 0 and i2 == len(dp)):
                    continue
                if not (n_real > 0 and n_wp > 0):
                    continue
                # var-k canon (smallest k first)
                def vark(dp, u, N, order, kmax=8, ndelta=9, tol=WP_TOL):
                    p = u
                    end = len(dp)
                    recs = 0
                    kh = Counter()
                    while p < end:
                        if p + 2 > end:
                            return (False, recs, kh)
                        idx = struct.unpack_from("<H", dp, p)[0]
                        if idx >= N:
                            return (False, recs, kh)
                        found = False
                        for k in order:
                            need = 2 + 4 * (k + ndelta)
                            if p + need > end:
                                continue
                            fls = [struct.unpack_from("<f", dp, p + 2 + 4 * q)[0]
                                   for q in range(k + ndelta)]
                            if not all(clean(v) for v in fls):
                                continue
                            if abs(sum(fls[:k]) - 1.0) <= tol:
                                found = True
                                kh[k] += 1
                                recs += 1
                                p += need
                                break
                        if not found:
                            return (False, recs, kh)
                    return (p == end, recs, kh)
                okc, rc, khc = vark(dp, u, n, range(1, 9))
                if okc and rc > 0:
                    continue  # var-k fit span — not in the 334
                nofit.append({"file": name, "bi": bi, "si": si, "N": n,
                              "Wm": Wm, "dp": dp, "u": u})
    print("nofit spans reproduced: %d (expect 334)" % len(nofit))

    # For each nofit span: test k-preference variants
    out = []
    for r in nofit:
        dp = r["dp"]
        u = r["u"]
        N = r["N"]
        row = {"key": [r["file"], r["bi"], r["si"]], "Wm": r["Wm"], "N": N,
               "es_len": len(dp) - u}
        for label, order in (("largest_first", range(8, 0, -1)),
                             ("k2_first", [2, 1, 3, 4, 5, 6, 7, 8]),
                             ("k2_only", [2]),
                             ("k1_only", [1])):
            okv, rv, khv = vark(dp, u, N, order)
            row[label] = {"ok": bool(okv and rv > 0), "recs": rv,
                          "k_hist": dict(khv)}
        out.append(row)
    n = len(out)
    summ = {
        "label": "POST-HOC CHARACTERIZATION (NON-COVERAGE)",
        "n_spans": n,
        "largest_first_fits": sum(1 for x in out if x["largest_first"]["ok"]),
        "k2_first_fits": sum(1 for x in out if x["k2_first"]["ok"]),
        "k2_only_fits": sum(1 for x in out if x["k2_only"]["ok"]),
        "k1_only_fits": sum(1 for x in out if x["k1_only"]["ok"]),
        "rows": out,
    }
    json.dump(summ, open(os.path.join(RUN, "01_RAW", "H1_DESYNC_PROBE.json"), "w"),
              indent=1)
    print("largest_first:", summ["largest_first_fits"], "k2_first:",
          summ["k2_first_fits"], "k2_only:", summ["k2_only_fits"],
          "k1_only:", summ["k1_only_fits"])


if __name__ == "__main__":
    main()
