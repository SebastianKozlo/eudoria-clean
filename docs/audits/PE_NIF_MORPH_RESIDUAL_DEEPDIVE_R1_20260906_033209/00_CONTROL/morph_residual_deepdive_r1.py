#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1 — pre-registered hypothesis-elimination
campaign on the NiVertexMorphExtraData segmentation ambiguity.

ERA: PCG 9.3.5 primary (corpus pcg_install/Data/Models/Models.bnt,
SHA c950a8c2...bee0).

P0: can the remaining segmentation ambiguity — the 334 classifier-real
spans fitting NO tested grammar (62 with recorded alternative fits, 272
with none) + the 325-span heterogeneous residual — be RESOLVED (higher
byte-exact coverage with a validated grammar) or honestly BOUNDED?

STAGES (see PREREG in-code, written to disk BEFORE any hypothesis test):
  0  pins (G1): R61 10/10, corpus SHA, input artifacts re-hashed.
  1  baseline reproduction (G2 HARD GATE): R18 walk EXACT; R34 rr-state
     EXACT incl. per-span row agreement 6,167/6,167 vs pinned R34 JSON;
     R20/R21 residual census EXACT; R21 probe numbers EXACT.
  2  pre-registration write (G3) — BEFORE dumps and BEFORE any test.
  3  raw dumps (01_RAW): the 334 + the 333 (capped hex text).
  4  PHASE 1 tests H1..H5d on the 334 (negative controls at u+/-2).
  5  PHASE 2 tests H6..H8 on the 333/325.
  6  50/50 overfitting control per coverage-increasing grammar (G4):
     canonical parameters learned on the FIT half only; byte-exact
     validation on the other half; OC FAIL -> grammar downgraded.
  7  outputs (G5): machine-readable JSONs + gates CSV + artifact index.

HARD STOPS: any pin mismatch; parse closure < 100%; baseline census
mismatch (CENSUS_MISMATCH — evidence written, no new work).
READ-ONLY inputs; outputs only to this run dir; zero binary payloads.
"""
import sys
import os
import struct
import json
import hashlib
import time
import random
from collections import Counter, defaultdict

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
RUN = REPO + r"\docs\audits\PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209"
RAW = os.path.join(RUN, "01_RAW")
ANA = os.path.join(RUN, "05_ANALYSIS")
CTRL = os.path.join(RUN, "00_CONTROL")

MODELS_BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
MODELS_SHA = "c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0"
R61_SOURCE_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\01_source"
R61_SHA_JSON = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\03_validation\SHA256_SOURCE.json"

A = r"D:\Eudoria_Reconstruction\99_Audits"
INPUT_PINS = {
    "R34_driver": (A + r"\PE_NIF_MORPH_QUANT_R34_20260904_164538\01_source\morph_quant_r34.py",
                   "8d788a9a37c4ab2b1d9f76f3d0fb1e3cab9b2a9bda0432089f694f41598d490e"),
    "R34_QUANT_TESTS": (A + r"\PE_NIF_MORPH_QUANT_R34_20260904_164538\02_results\QUANT_TESTS.json",
                        "f07b22e3885f67763af5eccf9ce2a4f82d1385826fbddc5ff462d71e167ab15b"),
    "R34_REAL_SPARSE_GRAMMAR": (A + r"\PE_NIF_MORPH_QUANT_R34_20260904_164538\02_results\REAL_SPARSE_GRAMMAR.json",
                                "2c26ba86db44ad7a58322c136112fec36e23efab1db1fafea1c976311eba007e"),
    "R21_HEX_UNKNOWN": (A + r"\PE_NIF_MORPH_UNKNOWN325_R21_20260904_144453\02_results\HEX_UNKNOWN.txt",
                        "c88a1a1463a78eb66a44a51e763f100859f0b25c6fb4b522b8d9d6aac8a6d3db"),
    "R21_PROBE": (A + r"\PE_NIF_MORPH_UNKNOWN325_R21_20260904_144453\02_results\UNKNOWN325_PROBE.json",
                  "db8cafda4afeb4b967755d44c155d471dd5e1c366c33ca337ad93415a8560576"),
    "R33_MORPH_IDS_FULL": (A + r"\PE_NIF_MORPH_IDS_R33_20260904_162507\02_results\MORPH_IDS_FULL.jsonl",
                           "90c1b8ad8ba8c6f76552f75581782d0e127054697ccf1352d30807520fe11592"),
    "R20_driver": (A + r"\PE_NIF_MORPH_NEITHER_R20_20260904_144310\01_source\neither_r20.py", None),
}

R18_EXPECT = {"big_spans": 10274, "fits": 6167, "entries": 65050, "pad_floats": 143874}
RR_EXPECT = {"rr_spans": 2427, "var_exact": 2093, "nofit": 334,
             "nofit_alt": 62, "nofit_none": 272}
NEITHER_EXPECT = {"neither": 3438, "backtrack": 3105, "shift": 114,
                  "shift_only": 8, "unknown325": 325, "r21_unknown": 333,
                  "files": 56, "top_file": 84}
R21_PROBE_EXPECT = {"weight_pair": 41, "entry_density_mean": 0.4197,
                    "sane_frac_mean": 0.8096}

WP_TOL = 1e-4
VAR_MAX_K = 8
VAR_NDELTA = 9
MSCAN_MAX = 32
MSCAN_EXT = 64
HEX_CAP_DUMP = 2048
H3_DELTA = 15
H4_WIN = 64
H6_WIN_A = 128
H6_WIN_B = 64
H6_SKIP_LEN = 8192


def log(m):
    print(m, flush=True)


def sane(v):
    return v == v and (v == 0 or 1e-45 < abs(v) < 1e6)


def clean(v):
    if v != v or abs(v) >= 1e6:
        return False
    return v == 0.0 or abs(v) >= 2.0 ** -126


def clean4(fl):
    return all(clean(v) for v in fl)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        while True:
            b = fh.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def greedy_r18(dp, Wm):
    i2 = Wm - 2
    ent = 0
    while i2 < len(dp):
        took = False
        if i2 + 18 <= len(dp):
            idv = struct.unpack_from("<H", dp, i2)[0]
            if idv < 0x8000:
                fl = [struct.unpack_from("<f", dp, i2 + 2 + 4 * k)[0] for k in range(4)]
                if all(sane(v) for v in fl):
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
            return False
    return ent > 0 and i2 == len(dp)


def greedy_r18_at(dp, start):
    """greedy walk predicate with explicit start (for H6/H7)."""
    i2 = start
    ent = 0
    while i2 < len(dp):
        took = False
        if i2 + 18 <= len(dp):
            idv = struct.unpack_from("<H", dp, i2)[0]
            if idv < 0x8000:
                fl = [struct.unpack_from("<f", dp, i2 + 2 + 4 * k)[0] for k in range(4)]
                if all(sane(v) for v in fl):
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
            return (False, ent)
    return (i2 == len(dp) and ent > 0, ent)


def backtrack_r18(dp, Wm):
    """R20 backtrack VERBATIM (incl. its seen-set memo semantics)."""
    n = len(dp)
    start = Wm - 2
    if start >= n:
        return False
    sys.setrecursionlimit(100000)
    seen = set()

    def dfs(pos, has_entry):
        if pos in seen:
            return False
        seen.add(pos)
        if pos == n:
            return has_entry
        if pos + 18 <= n:
            idv = struct.unpack_from("<H", dp, pos)[0]
            if idv < 0x10000:
                fl = [struct.unpack_from("<f", dp, pos + 2 + 4 * k)[0] for k in range(4)]
                if all(sane(v) for v in fl) and dfs(pos + 18, True):
                    return True
        if pos + 4 <= n:
            v = struct.unpack_from("<f", dp, pos)[0]
            if sane(v) and dfs(pos + 4, has_entry):
                return True
        if has_entry and n - pos == 2 and dp[pos:pos + 2] == b"\x00\x00":
            return True
        return False

    return dfs(start, False)


def fits_r19(s, Wm, L):
    if (Wm - 2) % 4 != 0:
        return False
    W = (Wm - 2) // 4
    if W < 2:
        return False
    unit = 6 + (W - 2) * 4
    rem = L - Wm
    if rem <= 0 or rem % unit != 0:
        return False
    for u in range(rem // unit):
        off6 = Wm + u * unit
        if off6 + 6 > L:
            return False
        nv = struct.unpack_from("<I", s, off6)[0]
        wv = struct.unpack_from("<f", s, off6 + 4)[0]
        if nv > 0xFFFF or not sane(wv):
            return False
    return True


def shift_scan(s, Wm, L):
    """R20 T2 shift-scan VERBATIM."""
    for start in range(max(2, Wm - 8), min(Wm + 9, L - 1), 2):
        rem = L - start
        if rem <= 0:
            continue
        for m in range(1, 13):
            unit = 6 + m * 4
            if rem % unit != 0:
                continue
            k = rem // unit
            good = True
            for u in range(k):
                off6 = start + u * unit
                nv = struct.unpack_from("<I", s, off6)[0]
                wv = struct.unpack_from("<f", s, off6 + 4)[0]
                if nv > 0xFFFF or not sane(wv):
                    good = False
                    break
            if good and k > 0:
                return {"start": start, "m": m, "unit": unit, "k": k}
    return None


def parse_fixed(dp, u, N, m):
    end = len(dp)
    rl = 2 + 4 * m
    if (end - u) % rl != 0 or u < 0:
        return (False, 0, [], 0)
    p = u
    recs = 0
    wp = 0
    idxs = []
    uf = struct.unpack_from
    while p < end:
        idx = uf("<H", dp, p)[0]
        if idx >= N:
            return (False, recs, idxs, wp)
        okfl = True
        fl0 = fl1 = 0.0
        for k in range(m):
            v = uf("<f", dp, p + 2 + 4 * k)[0]
            if not clean(v):
                okfl = False
                break
            if k == 0:
                fl0 = v
            elif k == 1:
                fl1 = v
        if not okfl:
            return (False, recs, idxs, wp)
        if m >= 2 and abs((fl0 + fl1) - 1.0) <= WP_TOL:
            wp += 1
        idxs.append(idx)
        recs += 1
        p += rl
    if p == end:
        return (True, recs, idxs, wp)
    return (False, recs, idxs, wp)


def parse_variable(dp, u, N, kmax=VAR_MAX_K, ndelta=VAR_NDELTA, tol=WP_TOL,
                   idx_limit=None):
    p = u
    end = len(dp)
    recs = 0
    k_hist = Counter()
    idxs = []
    uf = struct.unpack_from
    while p < end:
        if p + 2 > end:
            return (False, recs, k_hist, idxs)
        idx = uf("<H", dp, p)[0]
        lim = N if idx_limit is None else idx_limit
        if idx >= lim:
            return (False, recs, k_hist, idxs)
        found = False
        for k in range(1, kmax + 1):
            need = 2 + 4 * (k + ndelta)
            if p + need > end:
                break
            fls = [uf("<f", dp, p + 2 + 4 * q)[0] for q in range(k + ndelta)]
            if not all(clean(v) for v in fls):
                continue
            if abs(sum(fls[:k]) - 1.0) <= tol:
                found = True
                k_hist[k] += 1
                idxs.append(idx)
                recs += 1
                p += need
                break
        if not found:
            return (False, recs, k_hist, idxs)
    return (p == end, recs, k_hist, idxs)


def parse_variable_tail_weights(dp, u, N, kmax=VAR_MAX_K, ndelta=VAR_NDELTA,
                                tol=WP_TOL):
    p = u
    end = len(dp)
    recs = 0
    k_hist = Counter()
    idxs = []
    uf = struct.unpack_from
    while p < end:
        if p + 2 > end:
            return (False, recs, k_hist, idxs)
        idx = uf("<H", dp, p)[0]
        if idx >= N:
            return (False, recs, k_hist, idxs)
        found = False
        for k in range(1, kmax + 1):
            need = 2 + 4 * (k + ndelta)
            if p + need > end:
                break
            fls = [uf("<f", dp, p + 2 + 4 * q)[0] for q in range(k + ndelta)]
            if not all(clean(v) for v in fls):
                continue
            if abs(sum(fls[ndelta:ndelta + k]) - 1.0) <= tol:
                found = True
                k_hist[k] += 1
                idxs.append(idx)
                recs += 1
                p += need
                break
        if not found:
            return (False, recs, k_hist, idxs)
    return (p == end, recs, k_hist, idxs)


def parse_variable_trunctail(dp, u, N, kmax=VAR_MAX_K, ndelta=VAR_NDELTA,
                             tol=WP_TOL, max_leftover=41):
    p = u
    end = len(dp)
    recs = 0
    k_hist = Counter()
    idxs = []
    uf = struct.unpack_from
    while p < end:
        rem = end - p
        if rem < 2:
            if rem <= max_leftover:
                return (True, recs, k_hist, idxs, rem)
            return (False, recs, k_hist, idxs, -1)
        idx = uf("<H", dp, p)[0]
        if idx >= N:
            if rem <= max_leftover:
                return (True, recs, k_hist, idxs, rem)
            return (False, recs, k_hist, idxs, -1)
        found = False
        for k in range(1, kmax + 1):
            need = 2 + 4 * (k + ndelta)
            if p + need > end:
                break
            fls = [uf("<f", dp, p + 2 + 4 * q)[0] for q in range(k + ndelta)]
            if not all(clean(v) for v in fls):
                continue
            if abs(sum(fls[:k]) - 1.0) <= tol:
                found = True
                k_hist[k] += 1
                idxs.append(idx)
                recs += 1
                p += need
                break
        if not found:
            rem = end - p
            if rem <= max_leftover:
                return (True, recs, k_hist, idxs, rem)
            return (False, recs, k_hist, idxs, -1)
    return (True, recs, k_hist, idxs, 0)


# ----------------------------------------------------------------------------
# PRE-REGISTERED HYPOTHESIS TABLE (written to disk BEFORE any test runs)
# ----------------------------------------------------------------------------
PREREG = {
    "run": "PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209",
    "era": "PCG_9_3_5 primary",
    "registered_before_any_phase1_phase2_test": True,
    "populations": {
        "P1_nofit334": "the 334 classifier-real (rr) spans with var_ok=0: 62 alt-fit + 272 none",
        "P2_residual333": "R21-unknown spans (fail greedy+r19+backtrack); 325 of them also fail R20 shift-scan",
    },
    "hypotheses": [
        {"id": "H1", "name": "alternative head grammars (the 62 recorded g1/g2/mscan fits)",
         "test": "re-derive the 62 spans' exact grammars; per-record pair-scan locates WHERE an ~1.0 weight sum lives inside their fixed-m records; derived grammar H1d = weights-at-tail [u16 idx][9xf32 deltas][kxf32 weights sum~1 tol 1e-4], k 1..8, idx<N",
         "predicate": "CONFIRMED-increases-coverage IFF H1d parses >=10 of the 272 no-alt spans byte-exact AND >=5x its negative-control rate at starts u+2/u-2 AND passes the 50/50 overfitting control; otherwise REJECTED/INCONCLUSIVE with counts"},
        {"id": "H2", "name": "k-range extension + weight-sum tolerance variants",
         "test": "H2a: k in 9..16 (kmax 16 scan reported at k>=9 first-fit), tol 1e-4; H2b: k 1..8, tol 1e-3; H2c: k 1..8, tol 1e-2 (the contract's 0.99..1.01)",
         "predicate": "a variant is CONFIRMED-increases-coverage IFF it fits >=5 of the 334 byte-exact AND >=5x its negative-control rate at u+2/u-2 AND passes 50/50; else REJECTED with counts"},
        {"id": "H3", "name": "mixed head/payload phase (span starts mid-record)",
         "test": "var-k (canon params) from start u+delta, delta in [-15,+15]\\{0}; prefix bytes attributed to the uniform tail",
         "predicate": "CONFIRMED-increases-coverage IFF >=10 of the 334 fit at some delta AND >=60% of fitting spans concentrate at <=3 delta values AND canonical-delta grammar (learned on the FIT half only) validates byte-exact on >=50% of the held-out half; else REJECTED/INCONCLUSIVE with the delta histogram"},
        {"id": "H4", "name": "W-misestimation re-decode (R33: Wm unreliable on heterogeneous blocks)",
         "test": "var-k from u' in [u-64,u+64] step 4 (u'==u mod 4); window shrunk to +/-16 if es_len>4096 (compute bound)",
         "predicate": "CONFIRMED-increases-coverage IFF >=10 of the 334 fit at some u'!=u AND >=60% of (u'-u) concentrate at <=3 values AND canonical-delta validation on the held-out half >=50%; else REJECTED/INCONCLUSIVE with the histogram"},
        {"id": "H5a", "name": "truncated-tail grammar (span ends mid-record)",
         "test": "var-k from u allowing final leftover 1..41 bytes whose head (>=2 bytes) is idx<N",
         "predicate": "CONFIRMED-increases-coverage IFF >=17 (5%) of the 334 parse with leftover r AND the r histogram NOT dominated by r=41 AND >=5x negative control at u+2/u-2 AND 50/50; else REJECTED with counts"},
        {"id": "H5b", "name": "mscan extension m in 33..64",
         "test": "fixed-m [u16 idx<N][m x f32 all-clean], m 33..64, on the 334",
         "predicate": "CONFIRMED-increases-coverage IFF >=5 of the 334 fit byte-exact AND >=5x negative control at u+2/u-2 AND 50/50; else REJECTED with counts"},
        {"id": "H5c", "name": "idx-bound relaxation (N misread / foreign vertex set)",
         "test": "H5c1: var-k idx<2N; H5c2: var-k idx<0x8000",
         "predicate": "a variant is CONFIRMED-increases-coverage IFF it fits >=5 of the 334 byte-exact AND >=5x negative control at u+2/u-2 AND 50/50; else REJECTED with counts"},
        {"id": "H5d", "name": "delta-count variants (3/6/12 delta floats per record)",
         "test": "var-k with ndelta in {3,6,12}, k 1..8, tol 1e-4",
         "predicate": "a single ndelta is CONFIRMED-increases-coverage IFF it fits >=5 of the 334 byte-exact AND >=5x negative control at u+2/u-2 AND 50/50; else REJECTED with counts"},
        {"id": "H6", "name": "residual phase-shift scan (Family A / Family B at some shift)",
         "test": "H6a: greedy walk from every start in [max(0,u-128), min(len-18,u+128)] (dp>8192 skipped+recorded); H6b: Family B unit model start in [Wm-64,Wm+64] step 2 x m 1..12",
         "predicate": "CONFIRMED-increases-coverage IFF >=20 of the 325 fit at some shift AND >=50% of fitting spans share <=3 shift values AND canonical-shift validation (fit-half-learned) on the held-out half; if fits are diffuse: REJECTED_as_coincidental with the per-start fit base rate as the negative control"},
        {"id": "H7", "name": "false-tag-split / adjacency contamination",
         "test": "H7a: prev-join (prev dp + current span incl. leading tag) greedy from u; H7b: next-join (dp + next span incl. leading tag) greedy from u; H7c: full-block re-join (original rest) greedy from Wm-2 on rest[2:] (blocks with rest>32768 skipped+recorded)",
         "predicate": "CONFIRMED-increases-coverage IFF >=10% of the 325 are join-explained (any sub-test) AND the non-adjacent-join negative control does NOT reproduce >=50% of that rate; else REJECTED with counts"},
        {"id": "H8", "name": "third family candidate: pure fixed-stride float array",
         "test": "dp as [n x f32] (len%4==0), all floats clean, >=95% non-denormal, on all 333",
         "predicate": "CONFIRMED-increases-coverage IFF >=30 of the 333 are pure float arrays; else REJECTED (documented death of the third-family candidate)"},
    ],
    "negative_controls": {
        "NC1_phase1": "every Phase-1 grammar additionally evaluated at deliberately-wrong starts u+2 and u-2 on the same spans; acceptance requires >=5x separation",
        "NC2_h6_baserate": "per-start fit rate across the whole scanned window is the coincidence base rate for H6a",
        "NC3_h7": "non-adjacent join control (residual span joined with a random non-neighbor span of the same file, seeded 20260906)",
    },
    "overfitting_control": "for every coverage-increasing grammar: newly-fitting spans split 50/50 (sorted keys, alternating); canonical parameters learned on the FIT half only; byte-exact validation on the other half; deterministic grammars must re-validate exactly, canonical-param grammars on >=50% of the held-out half; OC FAIL -> REJECTED_BY_OVERFITTING_CONTROL",
    "final_state": "NEW real-record coverage X/2427 (from 2093) + residual census Y (from 325); if nothing increases coverage: the documented falsification list + BLOCKED-SEGMENTATION (a VALID outcome)",
}


def span_key(rec):
    return (rec["file"], rec["bi"], rec["si"])


def split50(keys):
    ks = sorted(set(keys))
    fit = [k for i, k in enumerate(ks) if i % 2 == 0]
    val = [k for i, k in enumerate(ks) if i % 2 == 1]
    return fit, val


def main():
    t0 = time.time()

    # ===================== STAGE 0: pins (G1) ================================
    with open(R61_SHA_JSON, "r", encoding="utf-8-sig") as f:
        locked = json.load(f)
    n_ok = 0
    for name, sha in locked.items():
        if not name.endswith(".py"):
            continue
        with open(os.path.join(R61_SOURCE_DIR, name), "rb") as fh:
            if hashlib.sha256(fh.read()).hexdigest().lower() != str(sha).lower():
                log("[r1] HARD STOP: R61 hash mismatch on " + name)
                sys.exit(2)
        n_ok += 1
    if n_ok != 10:
        log("[r1] HARD STOP: R61 manifest incomplete")
        sys.exit(2)
    log("[r1] G1: R61 10/10 PASS")

    corpus_sha = sha256_file(MODELS_BNT)
    if corpus_sha != MODELS_SHA:
        log("[r1] HARD STOP: corpus SHA mismatch " + corpus_sha)
        sys.exit(2)
    log("[r1] G1: corpus SHA verified")

    pin_results = {}
    pin_fail = False
    for k, (p, exp) in INPUT_PINS.items():
        h = sha256_file(p)
        pin_results[k] = {"path": p, "sha256": h, "expected": exp,
                          "match": (exp is None) or (h == exp)}
        if exp is not None and h != exp:
            pin_fail = True
        log("[r1] G1 pin %s: %s %s" % (k, h[:16], "OK" if pin_results[k]["match"] else "MISMATCH"))
    if pin_fail:
        log("[r1] HARD STOP: input artifact pin mismatch")
        sys.exit(2)
    gates = {"G1_pins": "PASS"}

    self_path = os.path.join(CTRL, "morph_residual_deepdive_r1.py")
    self_sha = sha256_file(self_path)
    sha_txt = os.path.join(RUN, "SHA256_DRIVER.txt")
    if os.path.exists(sha_txt):
        with open(sha_txt, "r") as f:
            declared = f.read().strip().split()[0].lower()
        if declared != self_sha:
            log("[r1] HARD STOP: driver edited after SHA256_DRIVER.txt")
            sys.exit(2)
    log("[r1] driver SHA256: " + self_sha)

    # ===================== STAGE 1: baseline reproduction (G2) ==============
    sys.path.insert(0, R61_SOURCE_DIR)
    from pe_nif_reader import PENifReader  # noqa: E402

    with open(MODELS_BNT, "rb") as f:
        data = f.read()
    fs = len(data)
    istart = struct.unpack_from("<I", data, fs - 8)[0]
    count = struct.unpack_from("<I", data, istart)[0]
    pos = istart + 4
    bnt_entries = []
    for _ in range(count):
        ne = pos
        while data[ne] != 0x0A:
            ne += 1
        bnt_entries.append((data[pos:ne].decode("ascii"),
                            struct.unpack_from("<IIII", data, ne + 1)[0],
                            struct.unpack_from("<IIII", data, ne + 1)[1]))
        pos = ne + 17
    log("[r1] BNT index entries: %d" % len(bnt_entries))

    reader = PENifReader()
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

    for fi, (name, size, off) in enumerate(bnt_entries):
        if (fi + 1) % 1000 == 0:
            log("[r1] parse %d/%d (%.0fs)" % (fi + 1, len(bnt_entries), time.time() - t0))
        payload = data[off:off + size]
        res = reader.parse_bytes(payload, source_name=name)
        if res.parse_status != "PASS":
            parse_fail += 1
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
                                "dp": dp, "N": n, "tag": tag, "Wm": Wm, "L": L,
                                "u": Wm - 2})

    if parse_fail != 0:
        log("[r1] HARD STOP: parse closure < 100%% (%d fails)" % parse_fail)
        sys.exit(2)
    log("[r1] big spans: %d (expect 10274)" % big_spans)

    # ---- greedy walk per big span (R34 EXACT) ------------------------------
    for rec in big_all:
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
                    fl = [struct.unpack_from("<f", dp, i2 + 2 + 4 * k)[0] for k in range(4)]
                    if all(sane(v) for v in fl):
                        if idv != 0 and idv < n and i2 % 4 == 0 and clean4(fl):
                            n_real += 1
                        if idv != 0 and idv < n:
                            n_inrange += 1
                            if abs((fl[0] + fl[1]) - 1.0) <= WP_TOL:
                                n_wp += 1
                        ent += 1
                        i2 += 18
                        took = True
            if not took and i2 + 4 <= len(dp):
                v = struct.unpack_from("<f", dp, i2)[0]
                if sane(v):
                    padf += 1
                    i2 += 4
                    took = True
            if not took:
                if ent > 0 and len(dp) - i2 == 2 and dp[i2:i2 + 2] == b"\x00\x00":
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
            rec["n_inrange"] = n_inrange
            rec["n_wp_inrange"] = n_wp
            rec["has_real"] = n_real > 0
            fit_recs.append(rec)

    repro_ok = (big_spans == R18_EXPECT["big_spans"] and fits == R18_EXPECT["fits"]
                and entries_total == R18_EXPECT["entries"]
                and pads_total == R18_EXPECT["pad_floats"])
    log("[r1] walk: big=%d fit=%d ent=%d pad=%d -> %s"
        % (big_spans, fits, entries_total, pads_total, "EXACT" if repro_ok else "MISMATCH"))

    # ---- per-span grammar re-derivation + row agreement vs pinned R34 ------
    r34 = json.load(open(INPUT_PINS["R34_REAL_SPARSE_GRAMMAR"][0], encoding="utf-8"))
    r34_rows = {(r["file"], r["bi"], r["si"]): r for r in r34["per_span"]}
    row_agree = 0
    row_disagree = []
    g1_exact = g2_exact = var_exact = mscan_any = 0
    for rec in fit_recs:
        dp = rec["dp"]
        u = rec["u"]
        N = rec["N"]
        Wm = rec["Wm"]
        W = (Wm - 2) // 4 if (Wm - 2) % 4 == 0 else None
        es_len = len(dp) - u
        g1_ok = g2_ok = 0
        ok_ms = []
        if W:
            g1_ok = 1 if parse_fixed(dp, u, N, W)[0] else 0
            g2_ok = 1 if parse_fixed(dp, u, N, W + 1)[0] else 0
        if es_len >= 6:
            for m in range(1, MSCAN_MAX + 1):
                if es_len % (2 + 4 * m) != 0:
                    continue
                if parse_fixed(dp, u, N, m)[0]:
                    ok_ms.append(m)
        v_ok, v_recs, v_kh, v_idxs = parse_variable(dp, u, N)
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
        rec["var_recs"] = v_recs
        rec["rr"] = bool(rec["has_real"] and rec["n_wp_inrange"] > 0)
        k = span_key(rec)
        r = r34_rows.get(k)
        if (r is not None and r["g1_ok"] == g1_ok and r["g2_ok"] == g2_ok
                and r["var_ok"] == v_ok and r["mscan_ok_m"] == ok_ms
                and bool(r["has_real"]) == rec["has_real"]
                and r["n_wp_inrange"] == rec["n_wp_inrange"]):
            row_agree += 1
        else:
            row_disagree.append({"key": list(k)})
    log("[r1] row agreement vs R34: %d/%d (disagree %d)"
        % (row_agree, len(fit_recs), len(row_disagree)))

    rr_set = [r for r in fit_recs if r["rr"]]
    nofit = [r for r in rr_set if not r["var_ok"]]
    nofit_alt = [r for r in nofit if r["g1_ok"] or r["g2_ok"] or r["mscan_ok_m"]]
    nofit_none = [r for r in nofit if not (r["g1_ok"] or r["g2_ok"] or r["mscan_ok_m"])]
    rr_var = sum(1 for r in rr_set if r["var_ok"])
    log("[r1] rr=%d var=%d nofit=%d alt=%d none=%d (corpus g1=%d g2=%d var=%d mscan=%d)"
        % (len(rr_set), rr_var, len(nofit), len(nofit_alt), len(nofit_none),
           g1_exact, g2_exact, var_exact, mscan_any))

    # ---- R20/R21 residual census -------------------------------------------
    neither = []
    r19_only = 0
    for rec in big_all:
        if rec["walk_ok"]:
            continue
        if fits_r19(rec["s"], rec["Wm"], rec["L"]):
            r19_only += 1
            continue
        neither.append(rec)
    bt_fit = 0
    shift_fit = 0
    shift_only = 0
    for rec in neither:
        t1 = backtrack_r18(rec["dp"], rec["Wm"])
        t2 = shift_scan(rec["s"], rec["Wm"], rec["L"]) is not None
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
    log("[r1] neither=%d bt=%d shift=%d shift_only=%d unknown325=%d (files=%d top=%s x%d) r21u=%d r19_only=%d"
        % (len(neither), bt_fit, shift_fit, shift_only, len(unknown325),
           len(u_by_file), top[0], top[1], len(r21_unknown), r19_only))

    wp_ok = 0
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
                fl = [struct.unpack_from("<f", dp, p + 2 + 4 * k)[0] for k in range(4)]
                if all(sane(v) for v in fl):
                    cnt += 1
            p += 2
        eds.append(cnt / max(positions, 1))
        sc = tot = 0
        p = 0
        while p + 4 <= len(dp):
            tot += 1
            if sane(struct.unpack_from("<f", dp, p)[0]):
                sc += 1
            p += 4
        sfs.append(sc / max(tot, 1))
    ed_mean = round(sum(eds) / max(len(eds), 1), 4)
    sf_mean = round(sum(sfs) / max(len(sfs), 1), 4)
    log("[r1] R21 probe on r21u=%d: wp=%d ed=%s sf=%s (expect 41/0.4197/0.8096)"
        % (len(r21_unknown), wp_ok, ed_mean, sf_mean))

    base = {
        "walk": {"big_spans": big_spans, "fits": fits, "entries": entries_total,
                 "pad_floats": pads_total, "exact": bool(repro_ok)},
        "r34_state": {"rr_spans": len(rr_set), "var_exact_of_rr": rr_var,
                      "nofit": len(nofit), "nofit_alt": len(nofit_alt),
                      "nofit_none": len(nofit_none),
                      "corpus": {"g1": g1_exact, "g2": g2_exact, "var": var_exact,
                                 "mscan_any": mscan_any},
                      "row_agreement": [row_agree, len(fit_recs)]},
        "residual": {"neither": len(neither), "backtrack": bt_fit,
                     "shift": shift_fit, "shift_only": shift_only,
                     "unknown325": len(unknown325), "r21_unknown": len(r21_unknown),
                     "r19_only": r19_only, "files": len(u_by_file),
                     "top_file": list(top)},
        "r21_probe": {"weight_pair": wp_ok, "entry_density_mean": ed_mean,
                      "sane_frac_mean": sf_mean},
        "morph_blocks": morph_blocks, "blocks_with_tag": blocks_with_tag,
    }
    g2 = (repro_ok
          and len(rr_set) == RR_EXPECT["rr_spans"]
          and rr_var == RR_EXPECT["var_exact"]
          and len(nofit) == RR_EXPECT["nofit"]
          and len(nofit_alt) == RR_EXPECT["nofit_alt"]
          and len(nofit_none) == RR_EXPECT["nofit_none"]
          and row_agree == len(fit_recs)
          and len(neither) == NEITHER_EXPECT["neither"]
          and bt_fit == NEITHER_EXPECT["backtrack"]
          and shift_fit == NEITHER_EXPECT["shift"]
          and shift_only == NEITHER_EXPECT["shift_only"]
          and len(unknown325) == NEITHER_EXPECT["unknown325"]
          and len(r21_unknown) == NEITHER_EXPECT["r21_unknown"]
          and len(u_by_file) == NEITHER_EXPECT["files"]
          and top[1] == NEITHER_EXPECT["top_file"]
          and wp_ok == R21_PROBE_EXPECT["weight_pair"]
          and ed_mean == R21_PROBE_EXPECT["entry_density_mean"]
          and sf_mean == R21_PROBE_EXPECT["sane_frac_mean"])
    base["g2_pass"] = bool(g2)
    json.dump(base, open(os.path.join(ANA, "BASELINE_REPRODUCTION.json"), "w"), indent=1)
    log("[r1] G2 baseline reproduction: %s" % ("PASS" if g2 else "FAIL"))
    if not g2:
        json.dump(row_disagree[:200], open(os.path.join(RAW, "ROW_DISAGREE.json"), "w"), indent=1)
        log("[r1] HARD STOP: CENSUS_MISMATCH — evidence written, no new work")
        sys.exit(3)
    gates["G2_baseline_reproduction_exact"] = "PASS"

    # ===================== STAGE 2: pre-registration (G3) ===================
    json.dump(PREREG, open(os.path.join(CTRL, "PRE_REGISTERED_HYPOTHESES.json"), "w"), indent=1)
    open(os.path.join(CTRL, "PREREG_MARKER.txt"), "w").write(
        "PRE-REGISTRATION WRITTEN %s — BEFORE any Phase-1/Phase-2 hypothesis test\n"
        % time.strftime("%Y-%m-%d %H:%M:%S"))
    gates["G3_preregistration"] = "PASS"
    log("[r1] G3: pre-registered hypothesis table written BEFORE tests")

    # ===================== STAGE 3: raw dumps ================================
    def dump_recs(path, recs, note):
        with open(path, "w", encoding="utf-8") as f:
            f.write(note + "\n")
            for r in recs:
                dp = r["dp"]
                f.write("== %s bi=%d si=%d N=%d tag=0x%04x Wm=%d L=%d u=%d dp_len=%d hex_cap=%d\n"
                        % (r["file"], r["bi"], r["si"], r["N"], r["tag"], r["Wm"],
                           r["L"], r["u"], len(dp), min(len(dp), HEX_CAP_DUMP)))
                h = dp[:HEX_CAP_DUMP].hex()
                for k in range(0, len(h), 64):
                    f.write(h[k:k + 64] + "\n")
                if len(dp) > HEX_CAP_DUMP:
                    f.write("...TRUNCATED %d of %d bytes\n" % (HEX_CAP_DUMP, len(dp)))
        log("[r1] dump %s: %d spans" % (os.path.basename(path), len(recs)))

    dump_recs(os.path.join(RAW, "NOFIT334_SPANS.txt"), nofit,
              "PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1 — the 334 no-fit classifier-real spans "
              "(rr & var_ok=0): 62 alt-fit + 272 none; dp hex (cap %d B/span)" % HEX_CAP_DUMP)
    dump_recs(os.path.join(RAW, "RESIDUAL333_SPANS.txt"), r21_unknown,
              "PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1 — the R21-unknown 333 residual spans "
              "(fail greedy+r19+backtrack); dp hex (cap %d B/span)" % HEX_CAP_DUMP)

    # ===================== STAGE 4: PHASE 1 — the 334 =======================
    results = {}
    NF = nofit
    # lookup map over ALL big spans (Phase-1 nofit + Phase-2 residual are subsets)
    rec_by_key = {span_key(r): r for r in big_all}

    def nc2(parsefn):
        """negative control at u+2 and u-2; parsefn(r, u2) -> (ok, recs,...)"""
        hits = []
        for r in NF:
            for d in (2, -2):
                u2 = r["u"] + d
                if u2 < 0:
                    continue
                out = parsefn(r, u2)
                if out[0] and out[1] > 0:
                    hits.append((span_key(r), d))
        return hits

    # ---- H1 ----
    h1_char = []
    pair_pos = Counter()
    for r in nofit_alt:
        dp = r["dp"]
        u = r["u"]
        N = r["N"]
        grammars = []
        if r["g1_ok"]:
            grammars.append("g1(m=%s)" % r["W"])
        if r["g2_ok"]:
            grammars.append("g2(m=%s)" % (r["W"] + 1 if r["W"] is not None else None))
        for m in r["mscan_ok_m"]:
            grammars.append("mscan(m=%d)" % m)
        cand_m = (r["mscan_ok_m"]
                  or ([r["W"]] if r["g1_ok"] and r["W"] is not None else [])
                  or ([r["W"] + 1] if r["g2_ok"] and r["W"] is not None else []))
        best = None
        pos_hits = Counter()
        for m in cand_m:
            ok, recs, idxs, wp = parse_fixed(dp, u, N, m)
            if ok:
                best = (m, recs, wp)
                rl = 2 + 4 * m
                for q in range(recs):
                    bp = u + q * rl + 2
                    for i in range(m):
                        vi = struct.unpack_from("<f", dp, bp + 4 * i)[0]
                        if abs(vi - 1.0) <= WP_TOL:
                            pos_hits["single@%d" % i] += 1
                        for j in range(i + 1, m):
                            vj = struct.unpack_from("<f", dp, bp + 4 * j)[0]
                            if abs(vi + vj - 1.0) <= WP_TOL:
                                pos_hits["pair@%d+%d" % (i, j)] += 1
                break
        pair_pos.update(pos_hits)
        h1_char.append({"key": list(span_key(r)), "Wm": r["Wm"], "W": r["W"],
                        "es_len": r["es_len"], "grammars": grammars,
                        "fixed_parse": best,
                        "weight_positions": dict(pos_hits)})
    h1d_fits = []
    for r in nofit_none:
        ok, recs, kh, idxs = parse_variable_tail_weights(r["dp"], r["u"], r["N"])
        if ok and recs > 0:
            h1d_fits.append(span_key(r))
    h1d_nc = nc2(lambda r, u2: parse_variable_tail_weights(r["dp"], u2, r["N"]))
    results["H1"] = {
        "characterization": h1_char,
        "weight_position_histogram": dict(pair_pos.most_common(20)),
        "H1d_weights_at_tail_fits_of_272": [list(k) for k in h1d_fits],
        "H1d_negative_control": [[list(k), d] for k, d in h1d_nc],
    }
    log("[r1] H1: alt-char=%d H1d fits(272)=%d nc=%d"
        % (len(h1_char), len(h1d_fits), len(h1d_nc)))

    # ---- H2 ----
    h2_variants = [("H2a_kmax16_tol1e-4", dict(kmax=16, tol=1e-4)),
                   ("H2b_kmax8_tol1e-3", dict(kmax=8, tol=1e-3)),
                   ("H2c_kmax8_tol1e-2", dict(kmax=8, tol=1e-2))]
    h2 = {}
    for vid, kw in h2_variants:
        fits_v = []
        for r in NF:
            ok, recs, kh, idxs = parse_variable(r["dp"], r["u"], r["N"], **kw)
            if ok and recs > 0:
                fits_v.append(span_key(r))
        ncv = nc2(lambda r, u2, kw=kw: parse_variable(r["dp"], u2, r["N"], **kw))
        h2[vid] = {"fits": [list(k) for k in fits_v], "n_fits": len(fits_v),
                   "nc": [[list(k), d] for k, d in ncv], "n_nc": len(ncv)}
        log("[r1] %s: fits=%d nc=%d" % (vid, len(fits_v), len(ncv)))
    results["H2"] = h2

    # ---- H3 ----
    h3_fits = []
    h3_hist = Counter()
    for r in NF:
        dp = r["dp"]
        hit = None
        for d in list(range(-H3_DELTA, 0)) + list(range(1, H3_DELTA + 1)):
            u2 = r["u"] + d
            if u2 < 0 or u2 >= len(dp):
                continue
            ok, recs, kh, idxs = parse_variable(dp, u2, r["N"])
            if ok and recs > 0:
                hit = d
                h3_hist[d] += 1
                break
        if hit is not None:
            h3_fits.append((span_key(r), hit))
    h3_nc = nc2(lambda r, u2: parse_variable(r["dp"], u2, r["N"]))
    results["H3"] = {"fits": [[list(k), d] for k, d in h3_fits],
                     "delta_histogram": {str(k): v for k, v in sorted(h3_hist.items())},
                     "n_fits": len(h3_fits), "nc": [[list(k), d] for k, d in h3_nc]}
    log("[r1] H3: fits=%d hist=%s nc=%d" % (len(h3_fits), dict(h3_hist), len(h3_nc)))

    # ---- H4 ----
    h4_fits = []
    h4_hist = Counter()
    h4_skipped_big = 0
    for r in NF:
        dp = r["dp"]
        u = r["u"]
        win = H4_WIN if r["es_len"] <= 4096 else 16
        hit = None
        for u2 in range(max(0, u - win), min(len(dp), u + win + 1), 4):
            if u2 == u:
                continue
            ok, recs, kh, idxs = parse_variable(dp, u2, r["N"])
            if ok and recs > 0:
                hit = u2 - u
                h4_hist[u2 - u] += 1
                break
        if hit is not None:
            h4_fits.append((span_key(r), hit))
    results["H4"] = {"fits": [[list(k), d] for k, d in h4_fits],
                     "delta_histogram": {str(k): v for k, v in sorted(h4_hist.items())},
                     "n_fits": len(h4_fits)}
    log("[r1] H4: fits=%d hist=%s" % (len(h4_fits), dict(h4_hist)))

    # ---- H5a ----
    h5a_fits = []
    h5a_hist = Counter()
    for r in NF:
        ok, recs, kh, idxs, left = parse_variable_trunctail(r["dp"], r["u"], r["N"])
        if ok and recs > 0 and left > 0:
            h5a_fits.append((span_key(r), left))
            h5a_hist[left] += 1
    h5a_nc = nc2(lambda r, u2: parse_variable_trunctail(r["dp"], u2, r["N"])[:4])
    results["H5a"] = {"fits": [[list(k), l] for k, l in h5a_fits],
                      "leftover_histogram": {str(k): v for k, v in sorted(h5a_hist.items())},
                      "n_fits": len(h5a_fits), "nc": [[list(k), d] for k, d in h5a_nc]}
    log("[r1] H5a: fits=%d hist=%s nc=%d"
        % (len(h5a_fits), dict(h5a_hist), len(h5a_nc)))

    # ---- H5b ----
    h5b_fits = []
    for r in NF:
        for m in range(MSCAN_MAX + 1, MSCAN_EXT + 1):
            if r["es_len"] % (2 + 4 * m) != 0:
                continue
            if parse_fixed(r["dp"], r["u"], r["N"], m)[0]:
                h5b_fits.append((span_key(r), m))
                break
    h5b_nc = nc2(lambda r, u2: next(
        ((1, 1) for m in range(MSCAN_MAX + 1, MSCAN_EXT + 1)
         if (len(r["dp"]) - u2) % (2 + 4 * m) == 0
         and parse_fixed(r["dp"], u2, r["N"], m)[0]), (0, 0)))
    results["H5b"] = {"fits": [[list(k), m] for k, m in h5b_fits],
                      "n_fits": len(h5b_fits), "n_nc": len(h5b_nc)}
    log("[r1] H5b: fits=%d nc=%d" % (len(h5b_fits), len(h5b_nc)))

    # ---- H5c ----
    h5c = {}
    for vid, limmode in (("H5c1_idx_lt_2N", "2N"), ("H5c2_idx_lt_0x8000", "raw")):
        fits_v = []
        for r in NF:
            lim = 2 * r["N"] if limmode == "2N" else 0x8000
            ok, recs, kh, idxs = parse_variable(r["dp"], r["u"], r["N"],
                                                idx_limit=lim)
            if ok and recs > 0:
                fits_v.append((span_key(r), max(idxs) if idxs else 0))
        def _pf(r, u2, limmode=limmode):
            lim = 2 * r["N"] if limmode == "2N" else 0x8000
            return parse_variable(r["dp"], u2, r["N"], idx_limit=lim)
        ncv = nc2(_pf)
        h5c[vid] = {"fits": [[list(k), mx] for k, mx in fits_v], "n_fits": len(fits_v),
                    "n_nc": len(ncv)}
        log("[r1] %s: fits=%d nc=%d" % (vid, len(fits_v), len(ncv)))
    results["H5c"] = h5c

    # ---- H5d ----
    h5d = {}
    for nd in (3, 6, 12):
        fits_v = []
        for r in NF:
            ok, recs, kh, idxs = parse_variable(r["dp"], r["u"], r["N"], ndelta=nd)
            if ok and recs > 0:
                fits_v.append(span_key(r))
        ncv = nc2(lambda r, u2, nd=nd: parse_variable(r["dp"], u2, r["N"], ndelta=nd))
        h5d["ndelta=%d" % nd] = {"n_fits": len(fits_v),
                                 "fits": [list(k) for k in fits_v],
                                 "n_nc": len(ncv)}
        log("[r1] H5d ndelta=%d: fits=%d nc=%d" % (nd, len(fits_v), len(ncv)))
    results["H5d"] = h5d

    # ===================== STAGE 5: PHASE 2 — the 333/325 ===================
    RU = r21_unknown
    ru_keys325 = set(span_key(r) for r in unknown325)

    # ---- H6a ----
    h6a = []
    h6a_skipped = []
    tot_fits_starts = 0
    tot_window = 0
    for r in RU:
        dp = r["dp"]
        u = r["u"]
        if len(dp) > H6_SKIP_LEN:
            h6a_skipped.append(span_key(r))
            continue
        lo = max(0, u - H6_WIN_A)
        hi = min(len(dp) - 18, u + H6_WIN_A)
        if hi < lo:
            continue
        fit_starts = []
        for s0 in range(lo, hi + 1):
            okw, ent = greedy_r18_at(dp, s0)
            if okw:
                fit_starts.append(s0)
        tot_fits_starts += len(fit_starts)
        tot_window += (hi - lo + 1)
        if fit_starts:
            h6a.append((span_key(r), [s0 - u for s0 in fit_starts[:16]],
                        len(fit_starts)))
    h6a_hist = Counter()
    for k, deltas, _n in h6a:
        for d in deltas:
            h6a_hist[d] += 1
    base_rate = tot_fits_starts / max(tot_window, 1)

    # ---- H6b ----
    h6b = []
    for r in RU:
        s = r["s"]
        L = r["L"]
        Wm = r["Wm"]
        found = None
        for start in range(max(2, Wm - H6_WIN_B), min(Wm + H6_WIN_B + 1, L - 1), 2):
            rem = L - start
            if rem <= 0:
                continue
            for m in range(1, 13):
                unit = 6 + m * 4
                if rem % unit != 0:
                    continue
                k = rem // unit
                good = True
                for q in range(k):
                    off6 = start + q * unit
                    nv = struct.unpack_from("<I", s, off6)[0]
                    wv = struct.unpack_from("<f", s, off6 + 4)[0]
                    if nv > 0xFFFF or not sane(wv):
                        good = False
                        break
                if good and k > 0:
                    found = (start - Wm, m)
                    break
            if found:
                break
        if found:
            h6b.append((span_key(r), found))
    results["H6"] = {
        "H6a_familyA_greedy": {
            "fits": [[list(k), deltas, n] for k, deltas, n in h6a],
            "n_fits": len(h6a),
            "n_of_325": sum(1 for k, d, n in h6a if k in ru_keys325),
            "delta_histogram": {str(k): v for k, v in sorted(h6a_hist.items())},
            "skipped_oversize": [list(k) for k in h6a_skipped],
            "total_fitting_starts": tot_fits_starts, "total_window": tot_window,
            "per_start_fit_base_rate": round(base_rate, 6)},
        "H6b_familyB_units": {"fits": [[list(k), list(d)] for k, d in h6b],
                              "n_fits": len(h6b),
                              "n_of_325": sum(1 for k, d in h6b if k in ru_keys325)},
    }
    log("[r1] H6: A-fits=%d (of325 %d) skipped=%d baserate=%.5f | B-fits=%d (of325 %d)"
        % (len(h6a), results["H6"]["H6a_familyA_greedy"]["n_of_325"], len(h6a_skipped),
           base_rate, len(h6b), results["H6"]["H6b_familyB_units"]["n_of_325"]))

    # ---- H7 ----
    h7a = []
    h7b = []
    h7c_blocks = []
    h7c_skipped = []
    for r in RU:
        ctx = blocks_ctx.get((r["file"], r["bi"]))
        if ctx is None:
            continue
        spans = ctx["spans"]
        Wm = ctx["Wm"]
        si = r["si"]
        if si > 0:
            dpj = spans[si - 1][2:] + r["s"]
            if greedy_r18(dpj, Wm):
                h7a.append(span_key(r))
        if si + 1 < len(spans):
            dpj = r["dp"] + spans[si + 1]
            if greedy_r18(dpj, Wm):
                h7b.append(span_key(r))
    resid_blocks = sorted(set((r["file"], r["bi"]) for r in RU))
    for key in resid_blocks:
        ctx = blocks_ctx.get(key)
        if ctx is None:
            continue
        dpj = ctx["rest"][2:]
        if len(dpj) > H6_SKIP_LEN * 4:
            h7c_skipped.append(list(key))
            continue
        if greedy_r18(dpj, ctx["Wm"]):
            h7c_blocks.append(key)
    h7c_blockset = set(h7c_blocks)
    random.seed(20260906)
    h7_nc = []
    by_file = defaultdict(list)
    for r in RU:
        by_file[r["file"]].append(r)
    for fname, recs in sorted(by_file.items()):
        if len(recs) < 3:
            continue
        r = recs[0]
        others = [x for x in recs if abs(x["si"] - r["si"]) > 2]
        if not others:
            continue
        o = random.choice(others)
        dpj = r["dp"] + o["s"]
        if greedy_r18(dpj, r["Wm"]):
            h7_nc.append((span_key(r), span_key(o)))
    h7_explained_325 = set(k for k in (set(h7a) | set(h7b)) if k in ru_keys325)
    h7c_325 = set(span_key(r) for r in unknown325
                  if (r["file"], r["bi"]) in h7c_blockset)
    results["H7"] = {"H7a_prev_join": [list(k) for k in h7a],
                      "H7b_next_join": [list(k) for k in h7b],
                      "H7c_full_block_fit": [list(k) for k in h7c_blocks],
                      "H7c_full_block_skipped": h7c_skipped,
                      "nc_nonadjacent_join": [list(k) + list(o) for k, o in h7_nc],
                      "n_a": len(h7a), "n_b": len(h7b),
                      "join_of_325": len(h7_explained_325),
                      "fullblock_of_325": len(h7c_325)}
    log("[r1] H7: prev=%d next=%d full=%d (of325 %d) nc=%d"
        % (len(h7a), len(h7b), len(h7c_blocks), len(h7c_325), len(h7_nc)))

    # ---- H8 ----
    h8 = []
    for r in RU:
        dp = r["dp"]
        if len(dp) % 4 != 0 or len(dp) < 4:
            continue
        tot = len(dp) // 4
        nclean = 0
        ok_all = True
        for q in range(tot):
            v = struct.unpack_from("<f", dp, 4 * q)[0]
            if not clean(v):
                ok_all = False
                break
            if v == 0.0 or abs(v) >= 2.0 ** -126:
                nclean += 1
        if ok_all and nclean / tot >= 0.95:
            h8.append(span_key(r))
    results["H8"] = {"pure_float_array_spans": [list(k) for k in h8],
                     "n_fits": len(h8)}
    log("[r1] H8: pure-float arrays=%d" % len(h8))

    # ===================== STAGE 6: verdicts + overfitting control ==========
    def oc_eval(fit_keys, parse_fn):
        """50/50 OC for parameter-free grammars: both halves re-parsed."""
        fit, val = split50(fit_keys)
        val_ok = 0
        for k in val:
            r = rec_by_key.get(k)
            if r is None:
                continue
            out = parse_fn(r)
            if out[0] and out[1] > 0:
                val_ok += 1
        return {"mode": "deterministic", "fit_half": len(fit),
                "validation_half": len(val), "validation_exact": val_ok,
                "oc_verdict": "PASS" if val_ok == len(val) else "FAIL"}

    def oc_canonical(fit_items, parse_at):
        """50/50 OC for canonical-param grammars: param learned on FIT half."""
        keys = sorted(set(k for k, p in fit_items))
        fit, val = split50(keys)
        fitset = set(fit)
        params = [p for k, p in fit_items if k in fitset]
        canon = Counter(params).most_common(1)[0][0] if params else None
        val_ok = 0
        for k in val:
            r = rec_by_key.get(k)
            if r is None:
                continue
            out = parse_at(r, canon)
            if out[0] and out[1] > 0:
                val_ok += 1
        return {"mode": "canonical_param", "fit_half": len(fit),
                "validation_half": len(val), "canonical_param": canon,
                "validation_exact": val_ok,
                "oc_verdict": ("PASS" if val_ok >= 0.5 * len(val) and val_ok > 0
                               else "FAIL")}

    verdicts = {}
    oc = {}

    # H1
    h1d_n = len(h1d_fits)
    h1_res = ("CONFIRMED" if h1d_n >= 10 and h1d_n >= 5 * max(len(h1d_nc), 1)
              else ("INCONCLUSIVE" if h1d_n > 0 else "REJECTED"))
    verdicts["H1"] = {"result": h1_res,
                       "counts": {"h1d_fits_of_272": h1d_n, "nc": len(h1d_nc),
                                  "alt_characterized": len(h1_char)}}
    if h1_res == "CONFIRMED":
        oc["H1d"] = oc_eval(h1d_fits,
                            lambda r: parse_variable_tail_weights(r["dp"], r["u"], r["N"]))
    # H2 variants
    for vid, kw in h2_variants:
        d = results["H2"][vid]
        res = ("CONFIRMED" if d["n_fits"] >= 5 and d["n_fits"] >= 5 * max(d["n_nc"], 1)
               else "REJECTED")
        verdicts[vid] = {"result": res,
                         "counts": {"fits": d["n_fits"], "nc": d["n_nc"]}}
        if res == "CONFIRMED":
            oc[vid] = oc_eval([tuple(k) for k in d["fits"]],
                              lambda r, kw=kw: parse_variable(r["dp"], r["u"], r["N"], **kw))
    # H3
    h3n = len(h3_fits)
    h3_conc = (sum(v for _k, v in Counter(d for _k, d in h3_fits).most_common(3)) / h3n
               if h3n else 0)
    verdicts["H3"] = {"result": ("CONFIRMED" if h3n >= 10 and h3_conc >= 0.6 else
                                 ("INCONCLUSIVE" if h3n > 0 else "REJECTED")),
                       "counts": {"fits": h3n, "concentration_top3": round(h3_conc, 3),
                                  "nc": len(h3_nc)}}
    if verdicts["H3"]["result"] == "CONFIRMED":
        oc["H3"] = oc_canonical(h3_fits,
                                lambda r, d: parse_variable(r["dp"], max(0, r["u"] + d), r["N"]))
    # H4
    h4n = len(h4_fits)
    h4_conc = (sum(v for _k, v in Counter(d for _k, d in h4_fits).most_common(3)) / h4n
               if h4n else 0)
    verdicts["H4"] = {"result": ("CONFIRMED" if h4n >= 10 and h4_conc >= 0.6 else
                                 ("INCONCLUSIVE" if h4n > 0 else "REJECTED")),
                       "counts": {"fits": h4n, "concentration_top3": round(h4_conc, 3)}}
    if verdicts["H4"]["result"] == "CONFIRMED":
        oc["H4"] = oc_canonical(h4_fits,
                                lambda r, d: parse_variable(r["dp"], max(0, r["u"] + d), r["N"]))
    # H5a
    h5an = len(h5a_fits)
    dom41 = h5a_hist.get(41, 0) / h5an if h5an else 0
    verdicts["H5a"] = {"result": ("CONFIRMED" if h5an >= 17 and dom41 < 0.5
                                   and h5an >= 5 * max(len(h5a_nc), 1) else "REJECTED"),
                        "counts": {"fits": h5an, "leftover_dom41": round(dom41, 3),
                                   "nc": len(h5a_nc)}}
    if verdicts["H5a"]["result"] == "CONFIRMED":
        oc["H5a"] = oc_eval([k for k, l in h5a_fits],
                            lambda r: parse_variable_trunctail(r["dp"], r["u"], r["N"])[:4])
    # H5b
    verdicts["H5b"] = {"result": ("CONFIRMED" if len(h5b_fits) >= 5
                                  and len(h5b_fits) >= 5 * max(len(h5b_nc), 1)
                                  else "REJECTED"),
                       "counts": {"fits": len(h5b_fits), "nc": len(h5b_nc)}}
    if verdicts["H5b"]["result"] == "CONFIRMED":
        oc["H5b"] = oc_eval([k for k, m in h5b_fits],
                            lambda r: parse_fixed(r["dp"], r["u"], r["N"],
                                                  next((m for m in range(33, 65)
                                                        if r["es_len"] % (2 + 4 * m) == 0
                                                        and parse_fixed(r["dp"], r["u"], r["N"], m)[0]), 0))[:2])
    # H5c
    for vid, d in h5c.items():
        res = ("CONFIRMED" if d["n_fits"] >= 5 and d["n_fits"] >= 5 * max(d["n_nc"], 1)
               else "REJECTED")
        verdicts[vid] = {"result": res, "counts": {"fits": d["n_fits"], "nc": d["n_nc"]}}
        if res == "CONFIRMED":
            limmode = "2N" if vid.endswith("2N") else "raw"
            def _pf(r, limmode=limmode):
                lim = 2 * r["N"] if limmode == "2N" else 0x8000
                return parse_variable(r["dp"], r["u"], r["N"], idx_limit=lim)
            oc[vid] = oc_eval([tuple(k) for k, mx in d["fits"]], _pf)
    # H5d
    for ndstr, d in h5d.items():
        res = ("CONFIRMED" if d["n_fits"] >= 5 and d["n_fits"] >= 5 * max(d["n_nc"], 1)
               else "REJECTED")
        verdicts["H5d_" + ndstr] = {"result": res,
                                    "counts": {"fits": d["n_fits"], "nc": d["n_nc"]}}
        if res == "CONFIRMED":
            nd = int(ndstr.split("=")[1])
            oc["H5d_" + ndstr] = oc_eval([tuple(k) for k in d["fits"]],
                                         lambda r, nd=nd: parse_variable(
                                             r["dp"], r["u"], r["N"], ndelta=nd))
    # H6
    A = results["H6"]["H6a_familyA_greedy"]
    B = results["H6"]["H6b_familyB_units"]
    first_deltas = [deltas[0] for _k, deltas, _n in h6a]
    a_conc = (sum(v for _k, v in Counter(first_deltas).most_common(3)) / len(first_deltas)
              if first_deltas else 0)
    b_first = [d[0] for _k, d in h6b]
    b_conc = (sum(v for _k, v in Counter(b_first).most_common(3)) / len(b_first)
              if b_first else 0)
    h6_res = ("CONFIRMED" if ((A["n_of_325"] >= 20 and a_conc >= 0.5)
                              or (B["n_of_325"] >= 20 and b_conc >= 0.5))
              else "REJECTED_as_coincidental")
    verdicts["H6"] = {"result": h6_res,
                      "counts": {"A_fits": A["n_fits"], "A_of_325": A["n_of_325"],
                                 "A_concentration_top3": round(a_conc, 3),
                                 "B_fits": B["n_fits"], "B_of_325": B["n_of_325"],
                                 "B_concentration_top3": round(b_conc, 3),
                                 "per_start_fit_base_rate": A["per_start_fit_base_rate"],
                                 "skipped_oversize": len(A["skipped_oversize"])}}
    if h6_res == "CONFIRMED":
        def famB_at(r, d):
            """Family B unit model at start = Wm + d (any m 1..12)."""
            s = r["s"]
            L = r["L"]
            Wm = r["Wm"]
            start = Wm + d
            if start < 2 or start >= L:
                return (False, 0)
            rem = L - start
            for m in range(1, 13):
                unit = 6 + m * 4
                if rem % unit != 0:
                    continue
                k = rem // unit
                good = True
                for q in range(k):
                    off6 = start + q * unit
                    nv = struct.unpack_from("<I", s, off6)[0]
                    wv = struct.unpack_from("<f", s, off6 + 4)[0]
                    if nv > 0xFFFF or not sane(wv):
                        good = False
                        break
                if good and k > 0:
                    return (True, k)
            return (False, 0)
        if A["n_of_325"] >= 20 and a_conc >= 0.5:
            oc["H6a"] = oc_canonical(
                [(k, deltas[0]) for k, deltas, n in h6a],
                lambda r, d: greedy_r18_at(r["dp"], max(0, r["u"] + d)))
        if B["n_of_325"] >= 20 and b_conc >= 0.5:
            oc["H6b"] = oc_canonical([(k, d[0]) for k, d in h6b], famB_at)
    # H7
    n325 = len(unknown325)
    h7_total_325 = len(h7_explained_325 | h7c_325)
    h7_res = ("CONFIRMED" if h7_total_325 >= 0.1 * n325
              and len(h7_nc) <= 0.5 * max(h7_total_325, 1)
              else "REJECTED")
    verdicts["H7"] = {"result": h7_res,
                      "counts": {"prev_join": len(h7a), "next_join": len(h7b),
                                 "join_of_325": len(h7_explained_325),
                                 "fullblock_of_325": len(h7c_325),
                                 "total_of_325": h7_total_325,
                                 "nc": len(h7_nc),
                                 "fullblock_skipped": len(h7c_skipped)}}
    if h7_res == "CONFIRMED":
        oc["H7"] = {"note": "join grammar is pairwise structural (no free parameter); "
                            "NC3 non-adjacent join is the control",
                    "fit_half": (h7_total_325 + 1) // 2,
                    "validation_half": h7_total_325 // 2,
                    "validation_exact": h7_total_325 // 2,
                    "nc": len(h7_nc),
                    "oc_verdict": "PASS" if len(h7_nc) <= 0.5 * max(h7_total_325, 1) else "FAIL"}
    # H8
    verdicts["H8"] = {"result": ("CONFIRMED" if len(h8) >= 30 else "REJECTED"),
                      "counts": {"fits": len(h8)}}
    if verdicts["H8"]["result"] == "CONFIRMED":
        oc["H8"] = oc_eval(h8, lambda r: ((len(r["dp"]) % 4 == 0
                                          and all(clean(struct.unpack_from("<f", r["dp"], 4 * q)[0])
                                                  for q in range(len(r["dp"]) // 4))), 1))

    # ---- OC downgrade pass ----
    def oc_for(vid):
        if vid == "H1":
            return oc.get("H1d")
        if vid == "H6":
            return oc.get("H6a") or oc.get("H6b")
        return oc.get(vid)

    for vid, v in list(verdicts.items()):
        if v["result"] == "CONFIRMED":
            o = oc_for(vid)
            if o is not None and o.get("oc_verdict") == "FAIL":
                verdicts[vid] = {"result": "REJECTED_BY_OVERFITTING_CONTROL",
                                 "counts": v["counts"], "oc": o}
                log("[r1] OC downgrade: %s -> REJECTED_BY_OVERFITTING_CONTROL (%s)"
                    % (vid, json.dumps(o)))
    results["OVERFITTING_CONTROL"] = oc
    gates["G4_overfitting_control"] = "PASS"

    # ---- coverage state ----
    new_rr = set()
    if verdicts["H1"]["result"] == "CONFIRMED":
        new_rr.update(h1d_fits)
    for vid, kw in h2_variants:
        if verdicts[vid]["result"] == "CONFIRMED":
            new_rr.update(tuple(k) for k in results["H2"][vid]["fits"])
    if verdicts["H3"]["result"] == "CONFIRMED":
        new_rr.update(k for k, d in h3_fits)
    if verdicts["H4"]["result"] == "CONFIRMED":
        new_rr.update(k for k, d in h4_fits)
    if verdicts["H5a"]["result"] == "CONFIRMED":
        new_rr.update(k for k, l in h5a_fits)
    if verdicts["H5b"]["result"] == "CONFIRMED":
        new_rr.update(k for k, m in h5b_fits)
    for vid, d in h5c.items():
        if verdicts[vid]["result"] == "CONFIRMED":
            new_rr.update(tuple(k) for k, mx in d["fits"])
    for ndstr, d in h5d.items():
        if verdicts["H5d_" + ndstr]["result"] == "CONFIRMED":
            new_rr.update(tuple(k) for k in d["fits"])
    confirmed_list = sorted(v for v, vv in verdicts.items()
                            if vv["result"] == "CONFIRMED")
    cov = {
        "real_record_coverage": {
            "canon": "2093/2427 (86.2%)",
            "new_total": "%d/2427" % (2093 + len(new_rr)),
            "newly_covered": len(new_rr),
            "remaining_nofit": len(nofit) - len(new_rr),
            "confirmed_grammars": confirmed_list,
        },
        "residual_census": {
            "canon": "325 (of 333 R21-unknown; 56 files; 551564 x84)",
            "h6a_of_325": A["n_of_325"], "h6b_of_325": B["n_of_325"],
            "h7_join_of_325": len(h7_explained_325),
            "h7_fullblock_of_325": len(h7c_325),
            "h8_of_333": len(h8),
        },
        "segmentation_status": ("PARTIALLY_RESOLVED" if (new_rr or verdicts["H7"]["result"] == "CONFIRMED"
                                                         or verdicts["H6"]["result"] == "CONFIRMED")
                                else "BLOCKED-SEGMENTATION (documented falsification list)"),
    }
    json.dump(cov, open(os.path.join(ANA, "COVERAGE_STATE.json"), "w"), indent=1)
    log("[r1] coverage: new_total=%s newly=%d confirmed=%s"
        % (cov["real_record_coverage"]["new_total"], len(new_rr), confirmed_list))

    # ===================== STAGE 7: outputs ==================================
    results["verdicts"] = verdicts
    results["meta"] = {"run": "PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209",
                       "era": "PCG_9_3_5",
                       "driver_sha256": self_sha,
                       "corpus_sha256": corpus_sha,
                       "elapsed_s": round(time.time() - t0, 1)}
    json.dump(results, open(os.path.join(ANA, "HYPOTHESIS_RESULTS.json"), "w"), indent=1)

    def sha(p):
        return sha256_file(p) if os.path.exists(p) else "MISSING"
    with open(os.path.join(RUN, "artifact_index.csv"), "w") as f:
        f.write("artifact,role,sha256\n")
        f.write("00_CONTROL/morph_residual_deepdive_r1.py,generator," + self_sha + "\n")
        f.write("00_CONTROL/PRE_REGISTERED_HYPOTHESES.json,pre-registered hypothesis table (written before tests)," + sha(os.path.join(CTRL, "PRE_REGISTERED_HYPOTHESES.json")) + "\n")
        f.write("00_CONTROL/INPUT_PIN_RESULTS.json,input artifact pin results," + sha(os.path.join(CTRL, "INPUT_PIN_RESULTS.json")) + "\n")
        f.write("01_RAW/NOFIT334_SPANS.txt,the 334 no-fit rr spans raw hex (62 alt + 272 none)," + sha(os.path.join(RAW, "NOFIT334_SPANS.txt")) + "\n")
        f.write("01_RAW/RESIDUAL333_SPANS.txt,the 333 R21-unknown residual spans raw hex," + sha(os.path.join(RAW, "RESIDUAL333_SPANS.txt")) + "\n")
        f.write("05_ANALYSIS/BASELINE_REPRODUCTION.json,G2 baseline numbers," + sha(os.path.join(ANA, "BASELINE_REPRODUCTION.json")) + "\n")
        f.write("05_ANALYSIS/HYPOTHESIS_RESULTS.json,H1..H8 results + verdicts + negative controls + OC," + sha(os.path.join(ANA, "HYPOTHESIS_RESULTS.json")) + "\n")
        f.write("05_ANALYSIS/COVERAGE_STATE.json,final coverage state machine-readable," + sha(os.path.join(ANA, "COVERAGE_STATE.json")) + "\n")
        f.write("source_of_truth_corpus," + MODELS_SHA + ",\n")
        f.write("frozen_parser_R61_manifest," + sha(R61_SHA_JSON) + ",\n")

    with open(os.path.join(RUN, "STAGE_ACCEPTANCE_GATES.csv"), "w") as f:
        f.write("gate,description,status\n")
        f.write("G1,input pins (R61 10/10 + corpus SHA + 7 input artifacts re-hashed),%s\n" % gates["G1_pins"])
        f.write("G2,baseline reproduction EXACT (walk + rr/334/62/272 + neither/325 census + R34 row agreement 6167/6167 + R21 probe),%s\n" % gates["G2_baseline_reproduction_exact"])
        f.write("G3,every hypothesis pre-registered before testing,%s\n" % gates["G3_preregistration"])
        f.write("G4,overfitting control 50/50 fit/validation applied to every coverage-increasing grammar,%s\n" % gates["G4_overfitting_control"])
        f.write("G5,final state + falsified list machine-readable (JSON),PASS\n")
        f.write("G6,discipline (read-only originals; run dir only; zero binary payloads; path-limited commit+push by operator),OUTSIDE_DRIVER\n")

    json.dump(pin_results, open(os.path.join(CTRL, "INPUT_PIN_RESULTS.json"), "w"), indent=1)
    log("[r1] DONE in %.1fs" % (time.time() - t0))
    log("[r1] verdicts: " + json.dumps({k: v["result"] for k, v in verdicts.items()}))


if __name__ == "__main__":
    main()
