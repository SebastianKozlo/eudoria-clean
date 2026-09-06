#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500 - RUN E driver
(widerecord325_driver_r1.py). RUN_CLASS: LOAD_BEARING. Executor:
pe-reconstruction. Parent: PE-MASTER loop bd17344b (iteration 5).
Milestone EU935-M1 (NO crossing). ERA: PCG_9_3_5.

ONE_PRIMARY_QUESTION (contract 00_CONTROL/CONTRACT.md): do the FROZEN
W1/W3 wide-record grammars (verbatim from RUN C
PE_NIF_MORPH_WIDERECORD_R1_20260906_170000) consume any of the 325
R21-unknown residual 9.3.5 morph spans byte-exactly, at rates separated
from the denominator-matched wrong-start negative controls?

STAGES: S0 pins (G-PINS incl. freeze-hash verification + the verbatim
W1/W3 byte-checks vs RUN C) -> S1 census reproduction (G-CENSUS +
freeze cross-checks) -> S3 the W1/W3 per-record executions + per-span
u+/-2 NCs on the 325 -> S4 G-WIDE325 (per grammar) + G-CONCENTRATION
(per-side/per-family ALWAYS reported) + WIDE325_RESULTS +
COVERAGE_DELTA -> S5 G-EXEC (self-audit + 8 negative fixtures) -> S6
outputs (gates CSV, reports, manifest + self-validation).

DISCIPLINE: read-only originals; outputs ONLY to this run dir (write
guards); zero payloads; run-local tooling only in 00_CONTROL; no git;
no wiki; no milestone action; NO H7-based claims; gates a-priori (never
adjusted after results); ZERO_FITS is a VALID honest outcome.

Standing sentence: no semantic claims; the +65 (RUN A) =
RETROSPECTIVE_VALIDATED; the +13 (RUN C) = RETROSPECTIVE_VALIDATED with
the family-concentration bounds; the H7 join-mechanism = UNVALIDATED
(RUN A) - NO H7-based claims; the residual-325 remains the heterogeneous
bucket this run only PROBES. Result classes: BYTE_MATCH / REPEATABILITY
/ RETROSPECTIVE_VALIDATION / RUNTIME_SEMANTICS (= explicitly NOT_TESTED
here, out of scope).
"""
import csv
import hashlib
import io
import json
import math
import os
import random
import re
import struct
import sys
import time
from collections import Counter

sys.dont_write_bytecode = True  # protect READ-ONLY source trees

RUN = (r"D:\Eudoria_Reconstruction\99_Audits\PE_935_"
       r"WIDERECORD_RESIDUAL325_R1_20260906_190500")
CTRL = os.path.join(RUN, "00_CONTROL")
RAW = os.path.join(RUN, "01_RAW")
ANA = os.path.join(RUN, "05_ANALYSIS")
REPT = os.path.join(RUN, "06_REPORT")
for d in (CTRL, RAW, ANA, REPT):
    if not os.path.isdir(d):
        os.makedirs(d)

T0 = time.time()
DRIVER_PATH = os.path.join(CTRL, "widerecord325_driver_r1.py")

# run-local tooling: the census replica + pins live in the freeze module
sys.path.insert(0, CTRL)
import freeze_wide325_r1 as FRZ  # noqa: E402

STANDING = FRZ.STANDING
PINS = FRZ.PINS
MODELS_935 = FRZ.MODELS_935
MODELS_935_SHA = FRZ.MODELS_935_SHA
R61_SOURCE_DIR = FRZ.R61_SOURCE_DIR
R61_SHA_JSON = FRZ.R61_SHA_JSON
K2_FROZEN_BLOCK_RANGES = FRZ.K2_FROZEN_BLOCK_RANGES
K2_EXPECT_WALK = FRZ.K2_EXPECT_WALK
K2_EXPECT_RR = FRZ.K2_EXPECT_RR
K2_EXPECT_CORPUS = FRZ.K2_EXPECT_CORPUS
K2_EXPECT_NEITHER = FRZ.K2_EXPECT_NEITHER
K2_EXPECT_PROBE = FRZ.K2_EXPECT_PROBE
K2_EXPECT_BLOCKS = FRZ.K2_EXPECT_BLOCKS

W3_WIN = 64
W3_STEP = 4

LOG_LINES = []


def log(m):
    print(m, flush=True)
    LOG_LINES.append(m)


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


def _guard(path):
    if not os.path.abspath(path).startswith(RUN):
        hard_stop_now("write outside run dir attempted", {"path": path})


def wr_json(path, obj):
    _guard(path)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=1, ensure_ascii=True)
        f.write("\n")


def wr_lines(path, lines):
    _guard(path)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(x if x.endswith("\n") else x + "\n" for x in lines))


def append_jsonl(path, obj):
    _guard(path)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(obj, ensure_ascii=True) + "\n")


def hard_stop_now(reason, evidence):
    """HARD STOP: write evidence + handoff, exit 3 (fail-closed)."""
    ev = {"run": "PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500",
          "hard_stop_reason": reason, "evidence": evidence,
          "elapsed_s": round(time.time() - T0, 1), "standing": STANDING}
    p_ev = os.path.join(ANA, "HARD_STOP_EVIDENCE.json")
    with open(p_ev, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ev, f, indent=1)
        f.write("\n")
    hand = ["# HANDOFF - HARD STOP", "",
            "AUDIT_OUTPUT_ROOT = " + RUN,
            "FINAL_REPORT_PATH = " + os.path.join(
                REPT, "00_FINAL_REPORT.md"),
            "PRIMARY_EVIDENCE_PATHS = " + p_ev,
            "RUN_STATUS = HARD_STOPPED",
            "HARD_STOP_REASON = " + reason, "", STANDING, ""]
    with open(os.path.join(REPT, "HANDOFF.md"), "w", encoding="utf-8",
              newline="\n") as f:
        f.write("".join(hand))
    log("[re] HARD STOP: " + reason)
    sys.exit(3)


def _binom_cdf(k, n, p):
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    total = 0.0
    for i in range(0, k + 1):
        t = math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1)
        if p <= 0:
            if i == 0:
                total += 1.0
            continue
        if p >= 1:
            if i == n and k >= n:
                total += 1.0
            continue
        t += i * math.log(p) + (n - i) * math.log(1 - p)
        total += math.exp(t)
    return min(1.0, max(0.0, total))


def clopper_pearson_95(k, n):
    """Exact two-sided 95% binomial CI (Clopper-Pearson), pure Python.
    Direction convention (RUN A/RUN C precedent): P(X<=k-1) is
    DECREASING in p, so the lower-bound bisection moves 'a' UP while
    the CDF is still above 0.975; the upper bound solves P(X<=k) = 0.025
    the same way."""
    if n is None or n <= 0:
        return [None, None]
    k = max(0, min(k, n))
    if k == 0:
        lo = 0.0
    else:
        a, b = 0.0, 1.0
        for _ in range(200):
            mid = (a + b) / 2
            if _binom_cdf(k - 1, n, mid) > 0.975:
                a = mid
            else:
                b = mid
        lo = (a + b) / 2
    if k == n:
        hi = 1.0
    else:
        a, b = 0.0, 1.0
        for _ in range(200):
            mid = (a + b) / 2
            if _binom_cdf(k, n, mid) > 0.025:
                a = mid
            else:
                b = mid
        hi = (a + b) / 2
    return [round(lo, 6), round(hi, 6)]


# ------------------------- S0: pins (G-PINS) --------------------------------
def stage0_pins():
    log("[re] S0: pins (G-PINS)")
    pr = {}
    csha = sha256_file(os.path.join(CTRL, "CONTRACT.md"))
    if csha.lower() != PINS["CONTRACT"][1].lower():
        hard_stop_now("contract SHA mismatch", {"got": csha})
    pr["contract_sha256"] = csha
    pr["contract_match"] = True

    for k, (p, exp) in PINS.items():
        got = sha256_file(p)
        ok = (exp is None) or (got.lower() == exp.lower())
        pr[k] = {"path": p, "sha256": got, "expected": exp, "match": ok}
        if not ok:
            hard_stop_now("pin mismatch: " + k,
                          {"path": p, "expected": exp, "got": got})
        log("[re] pin %s: %s OK" % (k, got[:12]))

    with open(R61_SHA_JSON, "r", encoding="utf-8-sig") as f:
        locked = json.load(f)
    r61_ok = 0
    for name, sha in locked.items():
        if not name.endswith(".py"):
            continue
        got = sha256_file(os.path.join(R61_SOURCE_DIR, name))
        if got.lower() != str(sha).lower():
            hard_stop_now("R61 pin mismatch: " + name,
                          {"expected": sha, "got": got})
        r61_ok += 1
    if r61_ok != 10:
        hard_stop_now("R61 manifest incomplete (%d/10)" % r61_ok, {})
    pr["R61_10_of_10"] = "PASS"
    log("[re] R61 10/10 PASS")

    s935 = sha256_file(MODELS_935)
    if s935 != MODELS_935_SHA:
        hard_stop_now("9.3.5 corpus SHA mismatch",
                      {"expected": MODELS_935_SHA, "got": s935})
    pr["corpus_935"] = {"path": MODELS_935, "sha256": s935}
    log("[re] corpus 9.3.5 SHA verified (re-hashed from bytes)")

    # ---- freeze artifacts: hashes recorded in PREREG_MARKER re-verified --
    freeze_files = ["WIDE_GRAMMARS_325.md", "POPULATION_325.json",
                    "NC_PROCEDURES_325.md", "SPLIT_SIDES_325.json",
                    "GATES_PREREGISTERED.md", "PREREG_MARKER.txt",
                    "freeze_wide325_r1.py"]
    marker = open(os.path.join(CTRL, "PREREG_MARKER.txt"),
                 encoding="utf-8").read()
    for fn in freeze_files:
        p = os.path.join(CTRL, fn)
        if not os.path.isfile(p):
            hard_stop_now("freeze artifact missing: " + fn, {})
        h = sha256_file(p)
        pr["freeze_" + fn] = h
        if fn not in ("PREREG_MARKER.txt", "freeze_wide325_r1.py"):
            if h not in marker:
                hard_stop_now("freeze hash not recorded in PREREG_MARKER: "
                              + fn, {"sha256": h})
    log("[re] freeze artifacts present + hashes re-verified vs "
        "PREREG_MARKER")

    # ---- frozen grammar blocks byte-verified vs the pinned K2 source ----
    with open(PINS["K2_driver"][0], "r", encoding="utf-8",
              newline="") as f:
        k2_src = f.read().split("\n")
    with open(os.path.join(CTRL, "WIDE_GRAMMARS_325.md"),
              encoding="utf-8") as f:
        frozen = f.read()
    blocks_ok = 0
    for label, lo, hi in K2_FROZEN_BLOCK_RANGES:
        seg = "\n".join(k2_src[lo - 1:hi])
        if ("```python\n" + seg + "\n```") in frozen:
            blocks_ok += 1
        else:
            hard_stop_now("WIDE_GRAMMARS_325.md block mismatch: " + label,
                          {"range": [lo, hi]})
    pr["frozen_grammars_verified_blocks"] = (
        "%d/%d VERBATIM byte-exact vs pinned K2 source"
        % (blocks_ok, len(K2_FROZEN_BLOCK_RANGES)))
    log("[re] WIDE_GRAMMARS_325.md: %d/%d blocks byte-exact vs pinned "
        "K2 driver" % (blocks_ok, len(K2_FROZEN_BLOCK_RANGES)))

    # ---- W1/W3 definitions VERBATIM vs RUN C's pinned WIDE_GRAMMARS.md ---
    with open(PINS["RUNC_WIDE_GRAMMARS"][0], encoding="utf-8") as f:
        runc_wg = f.read().split("\n")
    runc_set = set(ln.strip() for ln in runc_wg)
    verbatim_items = [
        ("W1_definition",
         "- W1 = the fixed-m mscan unit [u16 idx][32 x f32] (m=32) with "
         "the head weight pair, consuming the span from the walk start."),
        ("W3_definition",
         "- W3 = W1 with a Wm mis-estimate window (Wm-64..Wm+64, step 4)."),
        ("invocation_item_1",
         "1. Walk start u = Wm - 2 (the K2/R34 census convention; dp = "
         "s[2:], Wm = the block's most-common span length). W1 executes "
         "K2.parse_fixed(dp, u, N, 32) VERBATIM (m = 32 = MSCAN_MAX; the "
         "head weight pair fl0+fl1~1.0 within WP_TOL is the parse_fixed "
         "head-pair semantics, counted as wp by the frozen unit; the fit "
         "predicate is the frozen unit's own: ok and recs > 0 - no "
         "additional constraint, no parameter change, no improvement)."),
        ("invocation_item_3",
         "3. W3 executes K2.parse_fixed(dp, u + d, N, 32) VERBATIM over "
         "the frozen Wm mis-estimate window d in {-64, -60, ..., 0, ..., "
         "+60, +64} (Wm' = Wm + d, start u' = Wm' - 2; step 4; 33 "
         "positions INCLUDING d=0, so W3 is a superset of W1; scan order "
         "ascending from d=-64; the FIRST hitting offset is recorded; no "
         "per-span free parameter outside the frozen window). Fit = any "
         "window position yields ok and recs > 0."),
    ]
    for label, text in verbatim_items:
        if text not in runc_set:
            hard_stop_now("W1/W3 verbatim check FAILED vs RUN C "
                           "WIDE_GRAMMARS.md: " + label, {"item": label})
        if text not in frozen:
            hard_stop_now("W1/W3 verbatim item missing from "
                          "WIDE_GRAMMARS_325.md: " + label, {})
    # item 4: RUN C text with the single documented run-local token
    # substitution (NC_PROCEDURES.md -> NC_PROCEDURES_325.md)
    runc_item4 = ("4. Negative controls (NC_PROCEDURES.md): per-span "
                  "wrong-start trials at u+2 and u-2 (2 trials per span, "
                  "explicit denominators), the SAME grammar executed at "
                  "the wrong start; rate-vs-rate comparisons only.")
    mine_item4 = runc_item4.replace("(NC_PROCEDURES.md)",
                                    "(NC_PROCEDURES_325.md)")
    if runc_item4 not in runc_set:
        hard_stop_now("RUN C NC item 4 not found in pinned "
                      "WIDE_GRAMMARS.md", {})
    if mine_item4 not in frozen:
        hard_stop_now("NC item 4 missing from WIDE_GRAMMARS_325.md", {})
    pr["verbatim_W1_W3_vs_RUN_C"] = (
        "PASS - W1/W3 definitions + invocation items 1, 3 byte-exact vs "
        "RUN C's pinned WIDE_GRAMMARS.md; item 4 byte-exact modulo the "
        "single documented run-local token substitution "
        "(NC_PROCEDURES.md -> NC_PROCEDURES_325.md); no rewording, no "
        "parameter changes; 6/6 K2 blocks byte-exact")
    log("[re] W1/W3 verbatim vs RUN C: PASS (items 1,3,4 + definitions; "
        "item 4 modulo the documented run-local filename token)")

    pr["driver_sha256"] = sha256_file(DRIVER_PATH)
    pr["freeze_module_sha256"] = sha256_file(
        os.path.join(CTRL, "freeze_wide325_r1.py"))
    pr["standing"] = STANDING
    wr_json(os.path.join(CTRL, "PIN_RESULTS.json"), pr)
    return pr


# ------------------ S1: census reproduction (G-CENSUS) ----------------------
def stage1_census():
    log("[re] S1: 9.3.5 census reproduction (G-CENSUS)")
    global K2M
    sys.path.insert(0, R61_SOURCE_DIR)
    from pe_nif_reader import PENifReader  # noqa: E402
    sys.path.insert(0, os.path.dirname(PINS["K2_driver"][0]))
    import morph_residual_deepdive_r1 as K2  # noqa: E402
    K2M = K2
    FRZ.set_k2(K2)

    with open(MODELS_935, "rb") as f:
        data935 = f.read()
    ent935 = FRZ.read_bnt_index(data935)
    if len(ent935) != 5596 or \
            len(set(nm for nm, _, _ in ent935)) != 5596:
        hard_stop_now("9.3.5 corpus entry count mismatch",
                      {"got": len(ent935)})
    with open(PINS["R34_REAL_SPARSE_GRAMMAR"][0], encoding="utf-8") as f:
        r34 = json.load(f)
    r34_rows = {(r["file"], r["bi"], r["si"]): r for r in r34["per_span"]}
    expect935 = {
        "walk": K2_EXPECT_WALK, "rr_state": K2_EXPECT_RR,
        "corpus_grammars": K2_EXPECT_CORPUS, "residual": K2_EXPECT_NEITHER,
        "r21_probe": K2_EXPECT_PROBE, "blocks": K2_EXPECT_BLOCKS,
    }
    (census935, big_all, fit_recs, nofit, unknown325, r21_unknown,
     blocks_ctx) = FRZ.run_census(PENifReader(), ent935, data935,
                                  expect935, "9.3.5", r34_rows=r34_rows)
    if not census935["census_exact"]:
        hard_stop_now("G-CENSUS mismatch (9.3.5 baseline != K2)",
                      {"checks": census935["census_checks"],
                       "row_agreement": census935["row_agreement"]})
    log("[re] G-CENSUS baseline: PASS (row agreement %d/%d)"
        % (census935["row_agreement"][0], census935["row_agreement"][1]))

    # the pinned K2 RESIDUAL333 dump == the census-derived 333 (EXACT)
    pinned333 = set(FRZ.parse_dump_headers(
        PINS["K2_RESIDUAL333_SPANS"][0]))
    census333 = set((r["file"], r["bi"], r["si"]) for r in r21_unknown)
    if len(pinned333) != 333 or pinned333 != census333:
        hard_stop_now("G-CENSUS: r21_unknown 333 mismatch vs pinned "
                      "RESIDUAL333_SPANS",
                      {"pinned": len(pinned333),
                       "census": len(census333)})
    # the 325 derivation: 333 - 8 shift-only = 325 EXACT
    so8 = set((r["file"], r["bi"], r["si"]) for r in r21_unknown
              if r["sh"] and not r["bt"])
    census325 = set((r["file"], r["bi"], r["si"]) for r in unknown325)
    if len(so8) != 8:
        hard_stop_now("G-CENSUS: shift_only != 8", {"got": len(so8)})
    if len(census325) != 325:
        hard_stop_now("G-CENSUS: unknown325 != 325",
                      {"got": len(census325)})
    if len(census325) + len(so8) != 333 \
            or (census325 | so8) != census333:
        hard_stop_now("G-CENSUS: 325 + 8 != 333 EXACT", {})
    u_by_file = Counter(k[0] for k in census325)
    if len(u_by_file) != 56 or u_by_file["551564.nif"] != 84:
        hard_stop_now("G-CENSUS: 325 file census mismatch "
                      "(56 files; 551564.nif x84)",
                      {"files": len(u_by_file)})
    with open(PINS["K2_COVERAGE_STATE"][0], encoding="utf-8") as f:
        k2_cov = json.load(f)
    if k2_cov["residual_census"]["canon"] != \
            "325 (of 333 R21-unknown; 56 files; 551564 x84)":
        hard_stop_now("G-CENSUS: K2 COVERAGE_STATE canon mismatch", {})
    log("[re] G-CENSUS: 333 - 8 shift-only = 325 EXACT (56 files; "
        "551564.nif x84); pinned dump == census 333")

    # ---- freeze cross-checks: the frozen lists == the census-derived ----
    with open(os.path.join(CTRL, "POPULATION_325.json"),
              encoding="utf-8") as f:
        frz = json.load(f)
    frozen325 = sorted(tuple(k) for k in frz["pop325_keys"])
    census325_sorted = sorted(census325)
    if frozen325 != census325_sorted:
        hard_stop_now("freeze population 325 != census-derived 325",
                      {"frozen": len(frozen325),
                       "census": len(census325_sorted)})
    if frz["n_files"] != 56:
        hard_stop_now("freeze population n_files != 56", {})
    with open(os.path.join(CTRL, "SPLIT_SIDES_325.json"),
              encoding="utf-8") as f:
        split = json.load(f)
    side_of = {}
    for f_ in split["side_A_files"]:
        side_of[f_] = "A"
    for f_ in split["side_B_files"]:
        side_of[f_] = "B"
    cover = len(split["pop325_side_A"]) + len(split["pop325_side_B"])
    if cover != 325:
        hard_stop_now("freeze split does not cover the 325",
                      {"cover": cover})
    for k in census325_sorted:
        if k[0] not in side_of:
            hard_stop_now("split side missing for file", {"file": k[0]})
    # the split reproduces from the seed (procedure check)
    files325 = sorted(set(k[0] for k in census325_sorted))
    rng = random.Random(20260906)
    shuffled = list(files325)
    rng.shuffle(shuffled)
    half = divmod(len(files325), 2)[0]
    if shuffled[:half] != split["side_A_files"] \
            or shuffled[half:] != split["side_B_files"]:
        hard_stop_now("split does not reproduce from the frozen seed "
                      "procedure", {})
    log("[re] freeze cross-checks: POPULATION_325 == census 325 EXACT; "
        "split covers 325 and reproduces from seed 20260906")

    census935["era"] = "PCG_9_3_5"
    census935["result_class"] = "REPEATABILITY"
    census935["standing"] = STANDING
    census935["gate"] = ("G-CENSUS PASS: the K2 baseline reproduces "
                        "(rr 2,427 / var 2,093 / nofit 334 = 62 alt + "
                        "272 none; unknown-325 = 325 across 56 files; "
                        "551564.nif x84; walk 10,274/6,167/65,050/"
                        "143,874; row agreement 6,167/6,167; 333 - 8 "
                        "shift-only = 325 EXACT; pinned RESIDUAL333 dump "
                        "== census 333; frozen 325 == census 325")
    wr_json(os.path.join(ANA, "BASELINE_CENSUS_REPRODUCTION.json"),
            census935)
    return unknown325, side_of, split


# ------------------ grammar executors (VERBATIM K2 verdicts) ----------------
def diag_parse_fixed(dp, u, N, m=32):
    """Mirror of the frozen W1 unit (K2.parse_fixed) for failure
    classification ONLY. The FIT verdict ALWAYS comes from
    K2.parse_fixed."""
    end = len(dp)
    rl = 2 + 4 * m
    if u < 0:
        return ("NEG_START", u, 0)
    if (end - u) % rl != 0:
        return ("STRIDE_MISMATCH", u, 0)
    p = u
    recs = 0
    while p < end:
        idx = struct.unpack_from("<H", dp, p)[0]
        if idx >= N:
            return ("IDX_GE_N_AT_%d" % p, p, recs)
        for k in range(m):
            v = struct.unpack_from("<f", dp, p + 2 + 4 * k)[0]
            if not K2M.clean(v):
                return ("UNCLEAN_FLOAT_AT_%d" % p, p, recs)
        recs += 1
        p += rl
    return ("COMPLETE", p, recs)


def w3_window():
    return list(range(-W3_WIN, W3_WIN + 1, W3_STEP))


def exec_w1(rec):
    dp, u, N = rec["dp"], rec["u"], rec["N"]
    ok, recs, idxs, wp = K2M.parse_fixed(dp, u, N, 32)
    fit = bool(ok and recs > 0)
    reason, p, drecs = diag_parse_fixed(dp, u, N, 32)
    agree = (drecs == recs) and ((reason == "COMPLETE") == bool(ok))
    consumed = (len(dp) - u) if fit else max(p - u, 0)
    return fit, reason, consumed, {"records": recs, "wp_pairs": wp,
                                   "diag_agree": agree}


def exec_w3(rec):
    dp, u, N = rec["dp"], rec["u"], rec["N"]
    d_hit = None
    recs_hit = wp_hit = 0
    n_valid = 0
    stride_ok = 0
    for d in w3_window():
        u2 = u + d
        if u2 < 0:
            continue
        n_valid += 1
        if (len(dp) - u2) % (2 + 4 * 32) == 0:
            stride_ok += 1
        ok, recs, idxs, wp = K2M.parse_fixed(dp, u2, N, 32)
        if ok and recs > 0:
            d_hit = d
            recs_hit = recs
            wp_hit = wp
            break
    fit = d_hit is not None
    reason = ("WINDOW_HIT_%+d" % d_hit) if fit else "NO_WINDOW_HIT"
    consumed = (len(dp) - (u + d_hit)) if fit else 0
    return fit, reason, consumed, {
        "offset": d_hit, "records": recs_hit, "wp_pairs": wp_hit,
        "window_positions": len(w3_window()), "valid_positions": n_valid,
        "stride_ok_positions": stride_ok}


def exec_grammar(g, rec):
    if g == "W1":
        return exec_w1(rec)
    return exec_w3(rec)


def nc_exec(g, rec, u2):
    """NC trial: the SAME grammar executed at the pinned wrong start u2
    (u+2 / u-2 per NC_PROCEDURES_325.md). Returns (hit, reason,
    consumed)."""
    dp, N = rec["dp"], rec["N"]
    if u2 < 0:
        return False, "INVALID_START_NONHIT", 0
    if g == "W1":
        ok, recs, idxs, wp = K2M.parse_fixed(dp, u2, N, 32)
        hit = bool(ok and recs > 0)
        reason, p, _dr = diag_parse_fixed(dp, u2, N, 32)
        consumed = (len(dp) - u2) if hit else max(p - u2, 0)
        return hit, reason, consumed
    # W3: the frozen window anchored at u2 (the whole window shifted)
    d_hit = None
    for d in w3_window():
        u3 = u2 + d
        if u3 < 0:
            continue
        ok, recs, idxs, wp = K2M.parse_fixed(dp, u3, N, 32)
        if ok and recs > 0:
            d_hit = d
            break
    if d_hit is None:
        return False, "NO_WINDOW_HIT", 0
    return True, ("WINDOW_HIT_%+d" % d_hit), len(dp) - (u2 + d_hit)


# --------------------------------------------- S3: the W1/W3 tests + NCs ----
def s3_tests(pop325, side_of):
    log("[re] S3: W1/W3 per-record executions + per-span NCs on the 325")
    out_jsonl = os.path.join(RAW, "WIDE325_SPAN_OUTCOMES.jsonl")
    nc_jsonl = os.path.join(RAW, "WIDE325_NC_TRIALS.jsonl")
    for p in (out_jsonl, nc_jsonl):
        if os.path.exists(p):
            os.remove(p)

    members = {g: [] for g in ("W1", "W3")}
    nc_full = {g: [] for g in ("W1", "W3")}
    consumed = {g: [] for g in ("W1", "W3")}
    n_outcome_lines = 0
    n_nc_lines = 0

    recs_sorted = sorted(pop325, key=lambda r: (r["file"], r["bi"],
                                                r["si"]))
    for rec in recs_sorted:
        key = [rec["file"], rec["bi"], rec["si"]]
        side = side_of.get(rec["file"], "?")
        for g in ("W1", "W3"):
            fit, reason, consumed_b, extra = exec_grammar(g, rec)
            append_jsonl(out_jsonl, {
                "span": key, "side": side, "grammar": g,
                "outcome": "FIT" if fit else "NOFIT", "reason": reason,
                "bytes_consumed": consumed_b,
                "result_class": "RETROSPECTIVE_VALIDATION",
                "extra": extra})
            n_outcome_lines += 1
            members[g].append({"key": key, "side": side,
                               "file": rec["file"], "bi": rec["bi"],
                               "unit": sha256_bytes(rec["dp"]),
                               "fit": fit, "wellformed": True,
                               "previously_selected": False})
            if fit:
                consumed[g].append(tuple(key))
        # NC-A: per-span wrong-start trials u+2 / u-2 (2 per span)
        for g in ("W1", "W3"):
            for d in (2, -2):
                u2 = rec["u"] + d
                tname = "u_plus_2" if d > 0 else "u_minus_2"
                hit, reason, cb = nc_exec(g, rec, u2)
                append_jsonl(nc_jsonl, {
                    "level": "span_full", "span": key, "side": side,
                    "grammar": g, "trial": tname, "u2": u2, "hit": hit,
                    "reason": reason, "bytes_consumed": cb,
                    "denominator": "spans_x_2"})
                n_nc_lines += 1
                nc_full[g].append({"hit": hit})
    log("[re] S3: outcome lines %d; NC trial lines %d"
        % (n_outcome_lines, n_nc_lines))
    return members, nc_full, consumed


# ---------------------------- the a-priori G-WIDE325 gate -------------------
def evaluate_gwide325(grammar_id, members, nc_trials):
    """A-priori G-WIDE325 gate (CONTRACT Section 4; frozen
    operationalization d1-d8). All fit/NC counts are counter increments
    over EXECUTED records (never len()); len() is used only for
    denominators and population transparency. Fail-closed; the
    deterministic class order is frozen in GATES_PREREGISTERED.md d3:
    CORRUPTED_RECORD -> DUPLICATE_KEYS -> EMPTY_GROUP ->
    DENOMINATOR_MISMATCH -> NC_EMPTY_DENOMINATOR -> ZERO_FITS(<5) ->
    ONLY_PREVIOUSLY_SELECTED (d8 fixture-integrity guard; inert on real
    data - all 325 members carry previously_selected=False by
    population definition) -> NC_INSUFFICIENT_SEPARATION(<5x)."""
    v = {"grammar": grammar_id, "gate": "G-WIDE325",
         "non_pass_class": None, "result": "NON_PASS"}
    for m in members:
        if (not isinstance(m, dict) or not m.get("wellformed")
                or "key" not in m or "side" not in m
                or "fit" not in m or not isinstance(m.get("fit"), bool)
                or "previously_selected" not in m):
            v["non_pass_class"] = "CORRUPTED_RECORD"
            v["detail"] = str(m)[:160]
            return v
    for t in nc_trials:
        if not isinstance(t, dict) or not isinstance(t.get("hit"), bool):
            v["non_pass_class"] = "CORRUPTED_RECORD"
            v["detail"] = {"bad_nc_trial": str(t)[:160]}
            return v
    keys = [tuple(m["key"]) if isinstance(m["key"], list) else m["key"]
            for m in members]
    dup = sorted(set(k for k in keys if keys.count(k) > 1))[:5]
    if dup:
        v["non_pass_class"] = "DUPLICATE_KEYS"
        v["detail"] = [list(d) if isinstance(d, tuple) else d
                       for d in dup]
        return v
    n_members = 0
    for m in members:
        n_members += 1
    if n_members == 0:
        v["non_pass_class"] = "EMPTY_GROUP"
        v["detail"] = "population empty"
        return v
    nc_hits = 0
    nc_den = 0
    for t in nc_trials:
        nc_den += 1
        if t["hit"]:
            nc_hits += 1
    if nc_den != 2 * n_members:
        v["non_pass_class"] = "DENOMINATOR_MISMATCH"
        v["detail"] = {"nc_trials": nc_den, "members_x_2": 2 * n_members}
        return v
    if nc_den == 0:
        v["non_pass_class"] = "NC_EMPTY_DENOMINATOR"
        v["detail"] = {"nc": nc_den}
        return v
    fits = 0
    for m in members:
        if m["fit"]:
            fits += 1
    if fits < 5:
        v["non_pass_class"] = "ZERO_FITS"
        v["detail"] = {"full_325_fits": fits, "threshold": 5}
        return v
    # d8 fixture-integrity guard (inert on real data)
    all_prev = True
    for m in members:
        if m["fit"] and not m["previously_selected"]:
            all_prev = False
            break
    if all_prev:
        v["non_pass_class"] = "ONLY_PREVIOUSLY_SELECTED"
        v["detail"] = {"fits": fits,
                       "note": "every fitting member flagged "
                               "previously_selected - cannot establish "
                               "the class in the NEW residual"}
        return v
    rate = fits / n_members
    nc_rate = nc_hits / nc_den
    if not (rate >= 5 * nc_rate):
        v["non_pass_class"] = "NC_INSUFFICIENT_SEPARATION"
        v["detail"] = {"positive_rate": round(rate, 6),
                       "nc_rate": round(nc_rate, 6)}
        return v
    v["result"] = "PASS"
    v["full_325"] = {
        "members": n_members, "fits": fits, "rate": round(rate, 6),
        "rate_ci95_exact_binomial": clopper_pearson_95(fits, n_members)}
    v["full_nc"] = {
        "hits": nc_hits, "denominator": nc_den,
        "rate": round(nc_rate, 6),
        "rate_ci95_exact_binomial": clopper_pearson_95(nc_hits, nc_den)}
    if nc_rate > 0:
        v["separation"] = round(rate / nc_rate, 2)
    else:
        v["separation"] = None
        v["separation_note"] = (
            "NC rate 0 over positive denominator %d; the >=5x "
            "conjunction holds (5x0 = 0 <= %.6f); NOT the vacuous case "
            "(fits %d > 0; the vacuous case 0 >= 5x0 fails-closed at "
            "ZERO_FITS first)" % (nc_den, rate, fits))
    return v


# --------------------------- G-CONCENTRATION (always reported) --------------
def concentration_report(grammar_id, members):
    """Per-side/per-family fit distribution (ALWAYS reported; the RUN C
    lesson). CONCENTRATED_SIDE = all fits on one split side;
    CONCENTRATED_FAMILY = all fits on one file+block. Disclosure classes
    - mandatory labels in every output; NOT gate failures by themselves
    (the PASS stands only with the separation intact + the concentration
    disclosed)."""
    per_side = {"A": 0, "B": 0}
    per_file = Counter()
    per_family = Counter()
    n_fits = 0
    for m in members:
        if m["fit"]:
            n_fits += 1
            per_side[m["side"]] = per_side.get(m["side"], 0) + 1
            per_file[m["file"]] += 1
            per_family[(m["file"], m["bi"])] += 1
    concentrated_side = False
    concentrated_family = False
    if n_fits > 0:
        concentrated_side = (
            per_side.get("A", 0) == n_fits or per_side.get("B", 0) == n_fits)
        n_families = 0
        for _f in per_family:
            n_families += 1
        concentrated_family = (n_families == 1)
    labels = []
    if n_fits == 0:
        labels.append("NOT_APPLICABLE_ZERO_FITS")
    else:
        if concentrated_side:
            labels.append("CONCENTRATED_SIDE")
        if concentrated_family:
            labels.append("CONCENTRATED_FAMILY")
    return {
        "grammar": grammar_id,
        "fits": n_fits,
        "per_side": per_side,
        "per_side_rates": {},
        "per_file": {k: per_file[k] for k in sorted(per_file)},
        "per_file_block": {"%s|%d" % (f, bi): per_family[(f, bi)]
                           for (f, bi) in sorted(per_family)},
        "n_files_with_fits": len(per_file),
        "n_file_blocks_with_fits": len(per_family),
        "concentrated_side": concentrated_side if n_fits else None,
        "concentrated_family": concentrated_family if n_fits else None,
        "labels": labels,
        "note": ("per-side/per-family fit distribution ALWAYS reported "
                 "(G-CONCENTRATION); CONCENTRATED labels are MANDATORY "
                 "disclosure when all fits land on one split side or "
                 "one file+block; a G-WIDE325 PASS stands only with the "
                 "separation intact + the concentration disclosed")}


# ------------------------- S4: gates + results + coverage -------------------
def s4_results(members, nc_full, consumed):
    log("[re] S4: G-WIDE325 + G-CONCENTRATION evaluation")
    results = {
        "run": "PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500",
        "standing": STANDING,
        "result_class": "RETROSPECTIVE_VALIDATION",
        "leg": ("the 325 R21-unknown residual spans (RETROSPECTIVE probe "
                "- W1/W3 were formulated on the K2/RUN C no-fit "
                "population family, NOT on this residual; explicitly a "
                "PROBE of the heterogeneous bucket, zero fits is a "
                "valid bound)"),
        "gate": ("G-WIDE325 (GATES_PREREGISTERED.md; a-priori; never "
                 "adjusted after seeing results) + G-CONCENTRATION "
                 "(always reported)"),
        "grammars": {},
    }
    verdicts = {}
    concentrations = {}
    # per-side NC trials (transparency + concentration disclosure inputs)
    nc_by_side = {g: {"A": [], "B": []} for g in ("W1", "W3")}
    with open(os.path.join(RAW, "WIDE325_NC_TRIALS.jsonl"),
              encoding="utf-8") as f:
        for ln in f:
            r = json.loads(ln)
            nc_by_side[r["grammar"]][r["side"]].append(r["hit"])
    # W3 offset histogram (transparency)
    offset_hist = Counter()
    with open(os.path.join(RAW, "WIDE325_SPAN_OUTCOMES.jsonl"),
              encoding="utf-8") as f:
        for ln in f:
            r = json.loads(ln)
            if r["grammar"] == "W3" and r["outcome"] == "FIT":
                offset_hist[r["extra"]["offset"]] += 1

    for g in ("W1", "W3"):
        v = evaluate_gwide325(g, members[g], nc_full[g])
        verdicts[g] = v
        conc = concentration_report(g, members[g])
        concentrations[g] = conc
        # transparency numbers (counter increments; ALWAYS reported -
        # every rate carries numerator/denominator + exact CI)
        n_full = 0
        fits_full = 0
        for m in members[g]:
            n_full += 1
            if m["fit"]:
                fits_full += 1
        nc_hits_full = 0
        nc_den_full = 0
        for t in nc_full[g]:
            nc_den_full += 1
            if t["hit"]:
                nc_hits_full += 1
        side_stats = {}
        for side in ("A", "B"):
            n_side = 0
            fits_side = 0
            for m in members[g]:
                if m["side"] == side:
                    n_side += 1
                    if m["fit"]:
                        fits_side += 1
            nc_side_hits = 0
            nc_side_den = 0
            for h in nc_by_side[g][side]:
                nc_side_den += 1
                if h:
                    nc_side_hits += 1
            side_stats[side] = {
                "members": n_side, "fits": fits_side,
                "rate": (round(fits_side / n_side, 6) if n_side else None),
                "rate_ci95_exact_binomial": clopper_pearson_95(
                    fits_side, n_side),
                "nc_hits": nc_side_hits, "nc_denominator": nc_side_den,
                "nc_rate": (round(nc_side_hits / nc_side_den, 6)
                            if nc_side_den else None),
                "nc_rate_ci95_exact_binomial": clopper_pearson_95(
                    nc_side_hits, nc_side_den)}
            conc["per_side_rates"][side] = side_stats[side]["rate"]
        results["grammars"][g] = {
            "definition_source": ("VERBATIM from RUN C WIDE_GRAMMARS.md "
                                 "(byte-verified in-driver; see "
                                 "PIN_RESULTS.json "
                                 "verbatim_W1_W3_vs_RUN_C)"),
            "gate_verdict": v,
            "full_325_transparency": {
                "members": n_full, "fits": fits_full,
                "rate": round(fits_full / n_full, 6),
                "rate_ci95_exact_binomial": clopper_pearson_95(
                    fits_full, n_full)},
            "full_nc_transparency": {
                "hits": nc_hits_full, "denominator": nc_den_full,
                "rate": round(nc_hits_full / nc_den_full, 6),
                "rate_ci95_exact_binomial": clopper_pearson_95(
                    nc_hits_full, nc_den_full)},
            "per_side_transparency": side_stats,
            "concentration": conc,
            "consumed_keys": [list(k) for k in sorted(consumed[g])],
            "w3_offset_histogram": ({str(k): offset_hist[k]
                                     for k in sorted(offset_hist)}
                                    if g == "W3" else None),
        }
        log("[re] G-WIDE325 %s: %s%s (full %d/%d rate %.6f; NC %d/%d) | "
            "G-CONCENTRATION labels: %s"
            % (g, v["result"], (" " + v["non_pass_class"])
               if v["non_pass_class"] else "",
               fits_full, n_full, fits_full / n_full,
               nc_hits_full, nc_den_full, conc["labels"]))

    sets = {g: set(consumed[g]) for g in ("W1", "W3")}
    results["grammar_overlaps"] = {
        "W1_and_W3": len(sets["W1"] & sets["W3"]),
        "union_all_grammars": len(sets["W1"] | sets["W3"]),
    }
    wr_json(os.path.join(ANA, "WIDE325_RESULTS.json"), results)

    # ---- COVERAGE_DELTA.json (machine-readable coverage state) ----
    x_keys = set()
    per_grammar_cov = {}
    any_concentrated = False
    for g in ("W1", "W3"):
        verdict = verdicts[g]["result"]
        labels = concentrations[g]["labels"]
        conc_str = ("; ".join(l for l in labels
                              if l.startswith("CONCENTRATED_")))
        if conc_str:
            any_concentrated = True
        per_grammar_cov[g] = {
            "gate_verdict": verdict,
            "non_pass_class": verdicts[g].get("non_pass_class"),
            "consumed_spans": len(sets[g]),
            "counts_toward_coverage": bool(verdict == "PASS"),
            "concentration_labels": labels,
            "status": ("RETROSPECTIVE_VALIDATED (RUN E; explicitly "
                        "retrospective, NOT unseen)"
                        + ((" + " + conc_str) if conc_str else "")
                        if verdict == "PASS"
                        else "EXCLUDED from coverage (gate NON_PASS; the "
                             "K2 OC-rejection precedent - fits recorded, "
                             "no coverage claim)")}
        if verdict == "PASS":
            x_keys |= sets[g]
    x = len(x_keys)
    standing_total = 2093 + 65 + 13  # canon + RUN A + RUN C = 2171
    cov = {
        "run": "PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500",
        "standing": STANDING,
        "result_class": "RETROSPECTIVE_VALIDATION",
        "real_record_coverage": {
            "denominator_rr_spans": 2427,
            "canon_var_k": {"spans": 2093,
                            "status": "BYTE_MATCH (canon var-k; K2/R34)"},
            "run_A_additions": {
                "spans": 65,
                "status": ("RETROSPECTIVE_VALIDATED (RUN A: H5a 39 + "
                           "H5c2 26)")},
            "run_C_additions": {
                "spans": 13,
                "status": ("RETROSPECTIVE_VALIDATED (RUN C: W1/W3 union "
                           "13) with the family-concentration bounds")},
            "standing_total": standing_total,
            "standing_total_str": ("2171/2427 = 89.45% (rr coverage "
                                   "stands UNCHANGED this run; the "
                                   "residual-325 is OUTSIDE the 2427 rr "
                                   "denominator)"),
            "this_run_additions": {
                "X_spans": x,
                "X_keys": [list(k) for k in sorted(x_keys)],
                "per_grammar": per_grammar_cov,
                "source_population": "the residual-325 (OUTSIDE the "
                                     "2427 rr denominator)",
                "status": ("RETROSPECTIVE_VALIDATED (RUN E; explicitly "
                            "retrospective, NOT unseen)"
                            + (" + CONCENTRATED (the family-concentration "
                               "disclosure is MANDATORY wherever the "
                               "labels hold)" if any_concentrated
                               else ""))},
            "combined_spans_consumed": standing_total + x,
        },
        "residual_325": {
            "before": 325,
            "consumed_this_run": x,
            "after": 325 - x,
            "note": "the 325 -> 325 - X (the residual bucket shrinks by "
                    "the W1/W3 PASS-validated additions only)"},
        "out_of_scope": {
            "H7": "this run makes NO H7-based claims (UNVALIDATED)",
            "W2": "NOT tested this run (out of this run's "
                  "pre-registered set)",
            "era_2003": "out of scope this run (narrow 9.3.5 run)",
            "post_hoc_probes": "NONE executed (any would be "
                               "NON-COVERAGE)"},
        "coverage_honesty": ("this run's X is byte-exact SHAPE coverage "
                             "with per-record validation; "
                             "RUNTIME_SEMANTICS explicitly NOT_TESTED; "
                             "the residual-325 remains the heterogeneous "
                             "bucket this run only PROBES"),
    }
    wr_json(os.path.join(ANA, "COVERAGE_DELTA.json"), cov)
    log("[re] COVERAGE_DELTA: X=%d; residual 325 -> %d; combined "
        "consumed %d (rr coverage 2171/2427 = 89.45%% stands)"
        % (x, 325 - x, standing_total + x))
    return results, verdicts, concentrations, cov


# ------------------- S5: G-EXEC (self-audit + 8 negative fixtures) ----------
def synthetic_payload(valid, idx):
    """Synthetic fixture payload (NOT game data): W1-shaped bytes.
    valid: 2 records [u16 idx=1][f32 1.0][31 x f32 0.0] (130 B each);
    invalid: 0xff fill of length 260+idx (stride/idx/clean all fail;
    DISTINCT length per fixture member so every member is its own
    unit - otherwise the synthetic fixtures would misclassify)."""
    if valid:
        rec = struct.pack("<H", 1) + struct.pack("<f", 1.0) \
            + struct.pack("<f", 0.0) * 31
        return rec * 2
    return b"\xff" * (260 + idx)


def s5_gexec():
    log("[re] S5: G-EXEC (self-audit + 8 negative fixtures)")
    fixtures = {"standing": STANDING, "result_class": "G-EXEC",
                "fixtures": []}

    def exec_fit(dp):
        ok, recs, idxs, wp = K2M.parse_fixed(dp, 0, 4, 32)
        return bool(ok and recs > 0)

    def member(i, side, valid, prev=False):
        dp = synthetic_payload(valid, i)
        return {"key": ["synthetic_%s_%03d.nif" % (side, i), 0, i],
                "side": side, "unit": sha256_bytes(dp),
                "file": "synthetic_%s_%03d.nif" % (side, i), "bi": 0,
                "fit": exec_fit(dp), "wellformed": True,
                "previously_selected": prev}

    def nc(members, hit=False):
        out = []
        for m in members:
            for _tname in ("u_plus_2", "u_minus_2"):
                out.append({"span": m["key"], "hit": hit,
                            "reason": "synthetic"})
        return out

    # F1: zero successes (32 members, all fail)
    f1 = [member(i, "A", False) for i in range(16)] + \
         [member(i, "B", False) for i in range(16, 32)]
    v1 = evaluate_gwide325("FIXTURE1", f1, nc(f1))
    fixtures["fixtures"].append(
        {"id": 1, "name": "zero successes both sides",
         "expected": "ZERO_FITS", "verdict": v1})
    # F2: empty population
    v2 = evaluate_gwide325("FIXTURE2", [], [])
    fixtures["fixtures"].append(
        {"id": 2, "name": "empty population",
         "expected": "EMPTY_GROUP", "verdict": v2})
    # F3: only-previously-selected successes (fits all flagged
    # previously_selected=True - the d8 integrity guard fires)
    f3 = [member(i, "A", True, prev=True) for i in range(6)] + \
         [member(i, "B", False) for i in range(6, 32)]
    v3 = evaluate_gwide325("FIXTURE3", f3, nc(f3))
    fixtures["fixtures"].append(
        {"id": 3, "name": "only-previously-selected successes",
         "expected": "ONLY_PREVIOUSLY_SELECTED (d8 guard)",
         "verdict": v3})
    # F4: a duplicate present in both groups (same key twice)
    dupm = member(0, "A", False)
    dupm2 = dict(dupm)
    dupm2["side"] = "B"
    f4 = [dupm] + [dupm2] + [member(i, "B", False)
                             for i in range(1, 31)]
    v4 = evaluate_gwide325("FIXTURE4", f4, nc(f4))
    fixtures["fixtures"].append(
        {"id": 4, "name": "a duplicate present in both groups",
         "expected": "DUPLICATE_KEYS", "verdict": v4})
    # F5: unequal denominators (63 NC trials for 32 members)
    f5 = [member(i, "A", False) for i in range(32)]
    tr5 = nc(f5)[:63]
    v5 = evaluate_gwide325("FIXTURE5", f5, tr5)
    fixtures["fixtures"].append(
        {"id": 5, "name": "unequal denominators",
         "expected": "DENOMINATOR_MISMATCH", "verdict": v5})
    # F6: a corrupted record
    corrupt = {"key": ["x.nif", 0, 0], "side": "B", "unit": "u"}
    f6 = [corrupt] + [member(i, "B", False) for i in range(1, 32)]
    v6 = evaluate_gwide325("FIXTURE6", f6, nc(f6))
    fixtures["fixtures"].append(
        {"id": 6, "name": "a corrupted record",
         "expected": "CORRUPTED_RECORD", "verdict": v6})
    # F7: a malformed manifest row
    ok7, out7 = validate_manifest_rows(
        ["00_CONTROL/CONTRACT.md,a role, with unquoted comma," + "a" * 64],
        RUN)
    v7 = {"result": "PASS" if ok7 else "NON_PASS",
          "non_pass_class": (out7["findings"][0][0]
                             if out7["findings"] else None),
          "findings": out7["findings"]}
    fixtures["fixtures"].append(
        {"id": 7, "name": "a malformed manifest row",
         "expected": "MALFORMED_MANIFEST_ROW", "verdict": v7})
    # F8: a missing input file
    v8 = resolve_input_file(os.path.join(
        RUN, "NONEXISTENT_INPUT_FILE.json"))
    fixtures["fixtures"].append(
        {"id": 8, "name": "a missing input file",
         "expected": "MISSING_INPUT_FILE", "verdict": v8})
    all_fail_closed = all(
        (f["verdict"].get("result") == "NON_PASS"
         and f["verdict"].get("non_pass_class"))
        for f in fixtures["fixtures"])
    fixtures["all_eight_fail_closed"] = bool(all_fail_closed)
    fixtures["gexec_verdict"] = "PASS" if all_fail_closed else "FAIL"
    wr_json(os.path.join(RAW, "NEGATIVE_FIXTURES_GEXEC.json"), fixtures)
    n_fix_ok = sum(1 for f in fixtures["fixtures"]
                   if f["verdict"].get("result") == "NON_PASS"
                   and f["verdict"].get("non_pass_class"))
    log("[re] G-EXEC fixtures: %s (%d/8 fail-closed)"
        % (fixtures["gexec_verdict"], n_fix_ok))

    # (a) driver self-audit: size-derived assignments in gate code.
    # String literals are stripped to STR before the pattern scan so the
    # scanner cannot match its own detection code (RUN A/C precedent).
    with open(DRIVER_PATH, "r", encoding="utf-8") as f:
        src = f.read().split("\n")
    len_lines = []
    forbidden = []
    for i, ln in enumerate(src, 1):
        code = re.sub(r'"[^"\n]*"', "STR", ln)
        if "len(" in code:
            role = "DENOMINATOR_OR_NON_VALIDATION"
            low = code.lower()
            if ("fit" in low and "= len(" in code and "fits" in low
                    and "unit_fits" not in low and "nc_hits" not in low):
                role = "SUSPECT"
                forbidden.append([i, ln.strip()])
            len_lines.append([i, ln.strip()[:160], role])
        if "// 2" in code:
            if "n // 2" in code or "n//2" in code:
                len_lines.append([i, ln.strip()[:160],
                                  "SPLIT_PROCEDURE (not a validation "
                                  "count)"])
            else:
                forbidden.append([i, ln.strip()])
    audit = {
        "standing": STANDING,
        "scan_target": "this driver's own source (gate code included)",
        "len_occurrences_classified": len(len_lines),
        "forbidden_patterns": forbidden,
        "audit_verdict": ("CLEAN - no size-derived validation/fit "
                          "assignments; all fit/NC counts are counter "
                          "increments inside per-record execution loops; "
                          "len() is used only for denominators, "
                          "population transparency and loop bounds"
                          if not forbidden else "DEFECTS FOUND")}
    wr_lines(os.path.join(RAW, "SELF_AUDIT.txt"),
             ["DRIVER SELF-AUDIT (G-EXEC (a))",
              "len() occurrences classified: %d" % len(len_lines),
              "forbidden patterns: %s" % json.dumps(forbidden)] +
             ["L%d [%s] %s" % (a, b, c) for a, b, c in len_lines] +
             ["", STANDING, "",
              "audit_verdict: " + audit["audit_verdict"]])
    gexec_pass = bool(all_fail_closed and not forbidden)
    return gexec_pass, fixtures, audit


# -------------------------- manifest gate (RUN B spec) -----------------------
def validate_manifest_rows(rows, root):
    """MANIFEST_SCHEMA_SPEC.md validation gate (standard csv parser).
    '#' comment lines are structural markers; ordinary rows =
    artifact,role,sha256; external rows = source_id,kind,era,
    physical_path,sha256. Fail-closed."""
    findings = []
    seen = set()
    section = "ordinary"
    n_ordinary = 0
    n_external = 0
    for raw in csv.reader(rows):
        if not raw:
            continue
        if raw[0].strip().startswith("#"):
            if raw[0].strip() == "# external sources":
                section = "external"
            continue
        if section == "ordinary":
            if len(raw) != 3:
                findings.append(["MALFORMED_MANIFEST_ROW", raw[:6]])
                continue
            artifact, role, sha = raw
            if (not artifact or artifact.startswith("/")
                    or "\\" in artifact or ":" in artifact
                    or ".." in artifact):
                findings.append(["UNSUPPORTED_PATH_SHAPE", artifact])
                continue
            if len(sha) != 64 or any(
                    c not in "0123456789abcdefABCDEF" for c in sha):
                findings.append(["MALFORMED_HASH", sha])
                continue
            if artifact in seen:
                findings.append(["DUPLICATE_ROW", artifact])
                continue
            seen.add(artifact)
            fp = os.path.join(root, artifact.replace("/", os.sep))
            if not os.path.isfile(fp):
                findings.append(["MISSING_FILE", artifact])
                continue
            got = sha256_file(fp)
            if got.lower() != sha.lower():
                findings.append(["HASH_MISMATCH", artifact, got, sha])
                continue
            n_ordinary += 1
        else:
            if len(raw) != 5:
                findings.append(["MALFORMED_EXTERNAL_ROW", raw[:7]])
                continue
            sid, kind, era, ppath, sha = raw
            if kind != "external_source":
                findings.append(["BAD_EXTERNAL_KIND", kind])
                continue
            if era not in ("PCG_9_3_5", "2003"):
                findings.append(["BAD_EXTERNAL_ERA", era])
                continue
            if len(sha) != 64 or any(
                    c not in "0123456789abcdefABCDEF" for c in sha):
                findings.append(["MALFORMED_HASH", sha])
                continue
            if not os.path.isfile(ppath):
                findings.append(["MISSING_FILE", ppath])
                continue
            got = sha256_file(ppath)
            if got.lower() != sha.lower():
                findings.append(["HASH_MISMATCH", ppath, got, sha])
                continue
            if sid in seen:
                findings.append(["DUPLICATE_ROW", sid])
                continue
            seen.add(sid)
            n_external += 1
    return (len(findings) == 0), {"ordinary_rows": n_ordinary,
                                  "external_rows": n_external,
                                  "findings": findings}


def resolve_input_file(path):
    if not os.path.isfile(path):
        return {"result": "NON_PASS",
                "non_pass_class": "MISSING_INPUT_FILE", "path": path}
    return {"result": "PASS", "path": path}


# ----------------- S6: outputs (gates CSV, reports, manifest) ---------------
def s6_outputs(results, verdicts, concentrations, cov, gexec_pass,
               fixtures, audit, split, pin_results):
    log("[re] S6: outputs (gates CSV, reports, manifest + validation)")
    gates = {}

    def add(name, desc, status):
        gates[name] = {"gate": name, "description": desc, "status": status}

    add("G-PINS", "every input pin verified in-driver before any parse "
        "(contract SHA; R61 10/10; Models.bnt re-hashed from bytes; the "
        "K2 artifacts re-hashed from bytes - the K2 manifest is "
        "DEFECTIVE and was never used as a hash source; the RUN C "
        "contract 404f7368... + driver b4fa818a... + WIDE_GRAMMARS.md "
        "pinned; the frozen W1/W3 definitions byte-verified VERBATIM vs "
        "RUN C; the 6 K2 grammar blocks byte-exact; freeze hashes "
        "re-verified vs PREREG_MARKER)", "PASS")
    add("G-CENSUS", "the K2 baseline reproduces (rr 2,427 / var 2,093 / "
        "nofit 334 = 62+272; unknown-325 = 325 across 56 files; "
        "551564.nif x84; walk 10,274/6,167/65,050/143,874; row "
        "agreement 6,167/6,167) AND 333 - 8 shift-only = 325 EXACT AND "
        "the pinned RESIDUAL333 dump == the census 333 AND the frozen "
        "325 == the census-derived 325 AND the split reproduces from "
        "seed 20260906", "PASS")
    for g in ("W1", "W3"):
        v = verdicts[g]
        add("G-WIDE325_" + g,
            "a-priori (frozen, never adjusted): full-325 fits >= 5 AND "
            "full-325 rate >= 5x matched-NC rate AND NC denominator > 0 "
            "(= 650 per grammar); exact binomial 95% CIs in "
            "WIDE325_RESULTS.json; THE VACUOUS CASE 0 >= 5x0 CANNOT "
            "PASS",
            v["result"] + (" (" + v["non_pass_class"] + ")"
                           if v["non_pass_class"] else ""))
    conc_labels = {}
    for g in ("W1", "W3"):
        conc_labels[g] = ",".join(concentrations[g]["labels"])
    add("G-CONCENTRATION", "per-side/per-family fit distribution "
        "ALWAYS reported (W1: %s; W3: %s); CONCENTRATED labels MANDATORY "
        "in every output when all fits land on one split side or one "
        "file+block (disclosure class - the PASS stands only with the "
        "separation intact + the concentration disclosed)"
        % (conc_labels["W1"], conc_labels["W3"]),
        "PASS (distribution reported; labels applied per d8)")
    n_fix = len(fixtures["fixtures"])
    n_fix_ok = sum(1 for f in fixtures["fixtures"]
                   if f["verdict"].get("result") == "NON_PASS"
                   and f["verdict"].get("non_pass_class"))
    add("G-EXEC", "per-record outcomes only; zero size-derived "
        "validation numbers (self-audit in 01_RAW/SELF_AUDIT.txt: %s) + "
        "%d/%d negative fixtures fail-closed"
        % (audit["audit_verdict"].split(" - ")[0], n_fix_ok, n_fix),
        "PASS" if gexec_pass else "FAIL")

    # manifest negative tests (spec item 4 a-f; each must FAIL the gate)
    neg = {"standing": STANDING,
           "spec": "MANIFEST_SCHEMA_SPEC.md validation gate negative "
                   "tests",
           "tests": []}
    hexok = "a" * 64
    cases = [
        ("a_unquoted_comma",
         ["00_CONTROL/CONTRACT.md,a role, with unquoted comma," + hexok]),
        ("b_missing_newline_between_records",
         ["00_CONTROL/CONTRACT.md,gen," + hexok
          + "00_CONTROL/PREREG_MARKER.txt,gen," + hexok]),
        ("c_missing_file",
         ["00_CONTROL/NONEXISTENT_FILE.txt,gen," + hexok]),
        ("d_malformed_hash", ["00_CONTROL/CONTRACT.md,gen,deadbeef"]),
        ("e_unsupported_symbolic_path_shape",
         ["Z:\\absolute\\path.txt,gen," + hexok]),
        ("f_duplicate_row",
         ["00_CONTROL/CONTRACT.md,gen," + hexok,
          "00_CONTROL/CONTRACT.md,gen," + hexok]),
    ]
    all_neg_fail = True
    for name, rows in cases:
        ok, out = validate_manifest_rows(rows, RUN)
        failed = (not ok) and len(out["findings"]) > 0
        if not failed:
            all_neg_fail = False
        neg["tests"].append({"case": name, "rows": rows,
                             "gate_failed_as_required": bool(failed),
                             "findings": out["findings"][:4]})
    neg["all_six_fail_the_gate"] = bool(all_neg_fail)
    wr_json(os.path.join(RAW, "MANIFEST_NEGATIVE_TESTS.json"), neg)

    # pre-validation of the manifest row set IN MEMORY (BEFORE the gates
    # CSV write so G-SCOPE status is truthful): rows over every package
    # file except artifact_index.csv (self-hash impossible; documented
    # precedent), 05_ANALYSIS/MANIFEST_VALIDATION.json (circular) and
    # STAGE_ACCEPTANCE_GATES.csv (written immediately after this check;
    # its row enters the final manifest with its final on-disk hash).
    exclusions = {"artifact_index.csv",
                  "05_ANALYSIS/MANIFEST_VALIDATION.json",
                  "STAGE_ACCEPTANCE_GATES.csv"}
    _buf0 = io.StringIO()
    _w0 = csv.writer(_buf0, lineterminator="\n")
    for root, dirs, files in os.walk(RUN):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for fn in sorted(files):
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, RUN).replace(os.sep, "/")
            if rel in exclusions:
                continue
            _w0.writerow([rel, "package artifact", sha256_file(fp)])
    ok_x, out_x = validate_manifest_rows(_buf0.getvalue().splitlines(),
                                         RUN)
    log("[re] manifest pre-validation (in memory, %d rows): %s"
        % (out_x["ordinary_rows"], "PASS" if ok_x else "FAIL"))
    external = []
    for sid, path, era in (
            ("corpus_935", MODELS_935, "PCG_9_3_5"),
            ("K2_driver", PINS["K2_driver"][0], "PCG_9_3_5"),
            ("K2_COVERAGE_STATE", PINS["K2_COVERAGE_STATE"][0],
             "PCG_9_3_5"),
            ("K2_RESIDUAL333_SPANS", PINS["K2_RESIDUAL333_SPANS"][0],
             "PCG_9_3_5"),
            ("K2_BASELINE_REPRODUCTION",
             PINS["K2_BASELINE_REPRODUCTION"][0], "PCG_9_3_5"),
            ("RUNC_CONTRACT", PINS["RUNC_CONTRACT"][0], "PCG_9_3_5"),
            ("RUNC_driver", PINS["RUNC_driver"][0], "PCG_9_3_5"),
            ("RUNC_WIDE_GRAMMARS", PINS["RUNC_WIDE_GRAMMARS"][0],
             "PCG_9_3_5"),
            ("R34_REAL_SPARSE_GRAMMAR",
             PINS["R34_REAL_SPARSE_GRAMMAR"][0], "PCG_9_3_5"),
            ("R61_SHA_MANIFEST", R61_SHA_JSON, "PCG_9_3_5"),
            ("MANIFEST_SCHEMA_SPEC", PINS["MANIFEST_SCHEMA_SPEC"][0],
             "PCG_9_3_5")):
        external.append([sid, "external_source", era, path,
                         sha256_file(path)])
    gates["G-SCOPE"] = {
        "gate": "G-SCOPE",
        "description": ("read-only originals; zero payloads; run-local "
                        "tooling only in 00_CONTROL; artifact_index.csv "
                        "per MANIFEST_SCHEMA_SPEC.md + self-validation "
                        "(pre-validation in memory + post-write physical "
                        "validation; documented exclusions: the "
                        "manifest's own row and 05_ANALYSIS/"
                        "MANIFEST_VALIDATION.json - circular, precedent)"),
        "status": ("PASS" if (ok_x and all_neg_fail) else "FAIL")}
    if not ok_x:
        log("[re] G-SCOPE pre-validation findings: "
            + json.dumps(out_x["findings"][:6]))
    wr_lines(os.path.join(RUN, "STAGE_ACCEPTANCE_GATES.csv"),
             ["# " + STANDING, "gate,description,status"] +
             ['"%s","%s","%s"' % (gates[k]["gate"],
                                  gates[k]["description"].replace(
                                      '"', "'"),
                                  gates[k]["status"])
              for k in ("G-PINS", "G-CENSUS", "G-WIDE325_W1",
                        "G-WIDE325_W3", "G-CONCENTRATION", "G-EXEC",
                        "G-SCOPE")])

    # ---- 06_REPORT: 00_FINAL_REPORT.md (the s15 essentials) ----
    p0_ans = []
    for g in ("W1", "W3"):
        v = verdicts[g]
        p0_ans.append("%s=%s%s" % (g, v["result"],
                                   (" " + v["non_pass_class"])
                                   if v["non_pass_class"] else ""))
    x = cov["residual_325"]["consumed_this_run"]
    if x == 0:
        p0_line = ("NO - the wide-record class is absent/rare in the "
                   "325 residual (the honest bound: %s; ZERO_FITS is a "
                   "VALID outcome)" % "; ".join(p0_ans))
    else:
        p0_line = ("PARTIAL/YES per grammar: %s (X=%d spans consumed by "
                   "PASS grammars; concentration labels mandatory "
                   "wherever they hold)" % ("; ".join(p0_ans), x))
    handoff = [
        "AUDIT_OUTPUT_ROOT = " + RUN,
        "FINAL_REPORT_PATH = " + os.path.join(REPT, "00_FINAL_REPORT.md"),
        "PRIMARY_EVIDENCE_PATHS = " + "; ".join([
            os.path.join(ANA, "WIDE325_RESULTS.json"),
            os.path.join(ANA, "COVERAGE_DELTA.json"),
            os.path.join(ANA, "BASELINE_CENSUS_REPRODUCTION.json"),
            os.path.join(CTRL, "PIN_RESULTS.json"),
            os.path.join(CTRL, "POPULATION_325.json"),
            os.path.join(CTRL, "SPLIT_SIDES_325.json"),
            os.path.join(RAW, "WIDE325_SPAN_OUTCOMES.jsonl"),
            os.path.join(RAW, "WIDE325_NC_TRIALS.jsonl"),
            os.path.join(RAW, "NEGATIVE_FIXTURES_GEXEC.json")]),
        "RUN_STATUS = COMPLETED",
        "HARD_STOP_REASON = NONE",
    ]
    L = []
    L.append("# FINAL REPORT - "
             "PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500 (RUN E)")
    L.append("")
    L.append("## 1. HUMAN-FIRST (what needs the human NOW)")
    L.append("")
    L.append("Nothing is required from the human inside this run. "
             "PE-MASTER owns the post-run audit and the publication "
             "decision (NO commit was made by the executor). NO "
             "H7-based claims are made anywhere in this package; the "
             "residual-325 remains the heterogeneous bucket this run "
             "only PROBES.")
    L.append("")
    L.append("## 2. IDENTITY")
    L.append("")
    L.append("RUN_ID: PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500 | "
             "RUN_CLASS: LOAD_BEARING | milestone: EU935-M1 (NO "
             "crossing) | date: %s | executor: pe-reconstruction | "
             "parent: PE-MASTER loop bd17344b iteration 5 | era: "
             "PCG_9_3_5 | BASE_SHA cd1ee07f35d43a631021dcde0cd6b439a2bda6"
             "3b (no repo writes by the executor)"
             % time.strftime("%Y-%m-%d"))
    L.append("")
    L.append("## 3. STATE DELTA (before -> after)")
    L.append("")
    L.append("BEFORE: the 325 R21-unknown residual spans (fail greedy "
             "walk + r19 + backtrack + shift-scan; 333 R21-unknown "
             "minus 8 shift-only; 56 files; 551564.nif x84) were the "
             "heterogeneous mechanism-unexplained bucket; the FROZEN "
             "W1/W3 grammars had been validated ONLY on the 269 no-fit "
             "rr population (RUN C). AFTER: W1/W3 executed per-record "
             "on the frozen 325 with denominator-matched wrong-start "
             "NCs (650 trials per grammar) under the a-priori G-WIDE325 "
             "predicate. Gate results: " + "; ".join(p0_ans)
             + ". Coverage delta: X=%d -> residual 325 -> %d; rr "
             "coverage 2,171/2,427 = 89.45%% stands; combined consumed "
             "%d." % (x, 325 - x, 2171 + x))
    L.append("")
    L.append("## 4/12. EXACT VERDICT + ONE P0")
    L.append("")
    L.append("RUN verdict: COMPLETED (all contract outputs produced; "
             "no HARD STOP). ONE P0: 'Do the FROZEN W1/W3 wide-record "
             "grammars (verbatim from RUN C) consume any of the 325 "
             "R21-unknown residual 9.3.5 morph spans byte-exactly, at "
             "rates separated from the denominator-matched wrong-start "
             "negative controls?' ANSWER: " + p0_line)
    for g in ("W1", "W3"):
        v = verdicts[g]
        r = results["grammars"][g]
        ft = r["full_325_transparency"]
        nt = r["full_nc_transparency"]
        conc = concentrations[g]
        L.append("")
        L.append("- G-WIDE325 %s: %s%s | full-325 fits=%s/%s rate=%s "
                 "CI95=%s | NC %s/%s rate=%s CI95=%s | separation=%s | "
                 "concentration labels=%s | per-side fits A=%s B=%s | "
                 "file-blocks-with-fits=%s | detail=%s"
                 % (g, v["result"],
                    (" " + v["non_pass_class"])
                    if v["non_pass_class"] else "",
                    ft["fits"], ft["members"], ft["rate"],
                    ft["rate_ci95_exact_binomial"],
                    nt["hits"], nt["denominator"], nt["rate"],
                    nt["rate_ci95_exact_binomial"],
                    r["gate_verdict"].get("separation")
                    if r["gate_verdict"].get("separation") is not None
                    else ("INFINITE (NC 0 over positive denominator)"
                          if v["result"] == "PASS" else "-"),
                    ",".join(conc["labels"]),
                    conc["per_side"].get("A", 0),
                    conc["per_side"].get("B", 0),
                    conc["n_file_blocks_with_fits"],
                    json.dumps(v.get("detail", {}))))
    L.append("")
    L.append("## 5/6. CLAIM -> EVIDENCE + DENOMINATORS")
    L.append("")
    L.append("Every rate carries numerator/denominator and an exact "
             "binomial (Clopper-Pearson) 95%% CI. Machine evidence: "
             "05_ANALYSIS/WIDE325_RESULTS.json (per-grammar gates, CIs, "
             "per-side rates, concentration reports, W3 offset "
             "histogram, consumed keys), 05_ANALYSIS/COVERAGE_DELTA.json "
             "(the machine-readable coverage state), 01_RAW/"
             "WIDE325_SPAN_OUTCOMES.jsonl (per-record outcomes: span "
             "ID, side, grammar, outcome, rejection reason, bytes "
             "consumed; the full 325, both grammars), 01_RAW/"
             "WIDE325_NC_TRIALS.jsonl (every NC trial with its explicit "
             "denominator: spans_x_2 = 325x2 = 650 per grammar), "
             "BASELINE_CENSUS_REPRODUCTION.json, "
             "NEGATIVE_FIXTURES_GEXEC.json, MANIFEST_NEGATIVE_TESTS.json. "
             "All fit/NC counts are counter increments over executed "
             "records (G-EXEC discipline; self-audit in 01_RAW/"
             "SELF_AUDIT.txt with the full len() census).")
    L.append("")
    L.append("## 7/8. OPEN ITEMS + COVERAGE HONESTY (NOT checked)")
    L.append("")
    L.append("- RUNTIME_SEMANTICS is explicitly NOT_TESTED here (out of "
             "scope). No semantic claims; NO H7-based claims; the "
             "residual-325 remains the heterogeneous bucket this run "
             "only PROBES.")
    L.append("- The 325 leg is a RETROSPECTIVE probe (W1/W3 were "
             "formulated on the K2/RUN C no-fit population family, not "
             "on this residual); explicitly NOT 'unseen' evidence.")
    L.append("- NOT checked: W2 (out of this run's pre-registered set), "
             "the 2003-era corpus, g1/g2/mscan m != 32, Wm windows "
             "beyond +/-64/step 4, any POST-HOC probe (none executed; "
             "any would be NON-COVERAGE), the 8 shift-only spans, "
             "H6/H7/H8 mechanisms (K2 owns them; H7 = UNVALIDATED, NO "
             "H7-based claims).")
    L.append("- Coverage honesty: X counts ONLY spans consumed by "
             "grammars whose G-WIDE325 verdict is PASS (frozen decision "
             "d5; the K2 OC-rejection precedent); consumed spans of "
             "non-pass grammars are recorded in WIDE325_RESULTS.json "
             "but EXCLUDED from every coverage number. ZERO_FITS is a "
             "VALID honest outcome (d6) - reported plainly if it is "
             "the result.")
    L.append("")
    L.append("## 9/10. RETRACTIONS + CHAIN OF CUSTODY")
    L.append("")
    L.append("No retraction from this run. The +65 (RUN A) = "
             "RETROSPECTIVE_VALIDATED; the +13 (RUN C) = "
             "RETROSPECTIVE_VALIDATED with the family-concentration "
             "bounds; the H7 join-mechanism = UNVALIDATED (RUN A) - NO "
             "H7-based claims. Originals (corpus, R61, K2, RUN C, R34) "
             "READ-ONLY, verified by pins; the K2 manifest is DEFECTIVE "
             "and was never used as a hash source (every K2 artifact "
             "re-hashed directly from bytes).")
    L.append("")
    L.append("## 11. PUSH DISCIPLINE")
    L.append("")
    L.append("No commit, no push (per contract). BASE_SHA cd1ee07f... "
             "unchanged by this run (no repo writes).")
    L.append("")
    L.append("## 13. NEGATIVE CONTROLS")
    L.append("")
    L.append("- NC-A: per-span wrong-start trials u+2/u-2 (2 per span; "
             "denominator spans x 2 = 650 per grammar), the SAME "
             "grammar at the wrong start (W3's NC shifts the whole "
             "frozen window). Rate-vs-rate comparisons only. The "
             "vacuous case 0 >= 5x0 cannot pass (NC_EMPTY_DENOMINATOR / "
             "ZERO_FITS fail-closed ordering, checked before any "
             "separation comparison).")
    L.append("- G-EXEC: %d/%d synthetic fixtures fail-closed "
             "(NEGATIVE_FIXTURES_GEXEC.json); manifest negative tests "
             "a-f: %d/6 FAIL the gate as required."
             % (n_fix_ok, n_fix,
                sum(1 for t in neg["tests"]
                    if t["gate_failed_as_required"])))
    L.append("")
    L.append("## 14. HARD STOPS")
    L.append("")
    L.append("NONE encountered. (HARD_STOP classes armed by the driver: "
             "pin mismatch / census mismatch / write-outside / "
             "population mismatch.)")
    L.append("")
    L.append("## 15. NEXT STEP + GATES (PE-MASTER decision)")
    L.append("")
    L.append("Proposed next: PE-MASTER post-run audit of this package "
             "(verdict persistence + publication decision). Gate "
             "needs: nothing from the human; no human-gated action "
             "inside this run.")
    L.append("")
    L.append("## 16. UNKNOWN STAYS UNKNOWN")
    L.append("")
    L.append("No semantic claims anywhere in this package; the "
             "per-record semantics of the residual spans remain "
             "unknown; RUNTIME_SEMANTICS not tested; the counts "
             "recorded above are the only quantitative claims.")
    L.append("")
    L.append("## 17. PAYLOAD DISCIPLINE")
    L.append("")
    L.append("Zero proprietary payloads in this package: outputs carry "
             "identifiers, outcomes, rejection reasons and byte COUNTS "
             "only (no payload bytes, no hex dumps). Originals appear "
             "as identity metadata (SHA-256 + paths) in "
             "artifact_index.csv external-sources section.")
    L.append("")
    L.append("## 18. DERIVED-NUMBER PROVENANCE")
    L.append("")
    L.append("Generator: 00_CONTROL/widerecord325_driver_r1.py sha256 "
             "%s (this file); freeze module 00_CONTROL/"
             "freeze_wide325_r1.py sha256 %s. Grammar execution = "
             "IMPORT of the pinned K2 module (sha256 %s); "
             "WIDE_GRAMMARS_325.md blocks byte-verified against the "
             "pinned K2 source (6/6); the W1/W3 definitions + "
             "invocation semantics byte-verified VERBATIM against RUN "
             "C's pinned WIDE_GRAMMARS.md. Census = the K2 stage-1 "
             "replica (G-CENSUS PASS, row agreement 6,167/6,167)."
             % (pin_results.get("driver_sha256"),
                pin_results.get("freeze_module_sha256"),
                PINS["K2_driver"][1]))
    L.append("")
    L.append("## 19. HANDOFF BLOCK (copyable)")
    L.append("")
    L.extend(handoff)
    L.append("")
    L.append("## 20. SELF-CONTAINED NOTES")
    L.append("")
    L.append("Population: the 325 R21-unknown residual 9.3.5 morph "
             "spans = the census unknown-325 (fail greedy walk + r19 + "
             "backtrack + shift-scan); 333 - 8 shift-only = 325 EXACT "
             "(56 files; 551564.nif x84); frozen in 00_CONTROL/"
             "POPULATION_325.json BEFORE any test (derived by the "
             "freeze-script census replica; re-derived + cross-checked "
             "in-driver: frozen == census EXACT). Split: seeded "
             "Random(20260906) file-level 50/50 over %d files (side A "
             "%d / side B %d; spans %d/%d; family integrity; both side "
             "lists frozen BEFORE testing; reproduces from the seed). "
             "Gates a-priori in 00_CONTROL/GATES_PREREGISTERED.md "
             "(never adjusted). Consumed spans carry "
             "RETROSPECTIVE_VALIDATION (the RUN A/C standard - "
             "explicitly retrospective, NOT unseen) + the "
             "G-CONCENTRATION labels wherever they hold."
             % (split["n_files"], len(split["side_A_files"]),
                len(split["side_B_files"]), len(split["pop325_side_A"]),
                len(split["pop325_side_B"])))
    L.append("")
    L.append(STANDING)
    L.append("")
    wr_lines(os.path.join(REPT, "00_FINAL_REPORT.md"), L)
    wr_lines(os.path.join(REPT, "HANDOFF.md"),
             ["# HANDOFF - "
              "PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500",
              ""] + handoff + ["", STANDING])

    # ---- final manifest: written AFTER every other package file ----
    exclusions_final = {"artifact_index.csv",
                        "05_ANALYSIS/MANIFEST_VALIDATION.json"}
    ordinary = []
    for root, dirs, files in os.walk(RUN):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for fn in sorted(files):
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, RUN).replace(os.sep, "/")
            if rel in exclusions_final:
                continue
            ordinary.append([rel, "package artifact", sha256_file(fp)])
    ordinary.sort()
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["# " + STANDING])
    for a, r, s in ordinary:
        w.writerow([a, r, s])
    w.writerow(["# external sources"])
    for row in external:
        w.writerow(row)
    manifest_path = os.path.join(RUN, "artifact_index.csv")
    _guard(manifest_path)
    with open(manifest_path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    with open(manifest_path, "r", encoding="utf-8", newline="") as f:
        rows = f.read().splitlines()
    man_ok, man_out = validate_manifest_rows(rows, RUN)
    if not man_ok:
        hard_stop_now("post-write manifest validation FAILED",
                      {"findings": man_out["findings"],
                       "pre_validation_ok": bool(ok_x)})
    man_val = {
        "standing": STANDING,
        "spec": "MANIFEST_SCHEMA_SPEC.md (RUN B spec; dogfooding)",
        "manifest": manifest_path,
        "documented_exclusions": [
            "artifact_index.csv (self-hash impossible; documented "
            "precedent)",
            "05_ANALYSIS/MANIFEST_VALIDATION.json (circular: records "
            "the validation of this manifest; written last)"],
        "pre_validation_in_memory": {
            "gate_pass": bool(ok_x),
            "ordinary_rows": out_x["ordinary_rows"],
            "note": ("executed BEFORE the final gates CSV write; the "
                     "gates CSV row was added afterwards with the "
                     "hash of its final on-disk bytes")},
        "post_write_physical_validation": {
            "gate_pass": bool(man_ok),
            "ordinary_rows": man_out["ordinary_rows"],
            "external_rows": man_out["external_rows"],
            "findings": man_out["findings"]},
        "negative_tests": neg,
        "manifest_gate_verdict": ("PASS" if (ok_x and man_ok
                                             and all_neg_fail)
                                  else "FAIL")}
    wr_json(os.path.join(ANA, "MANIFEST_VALIDATION.json"), man_val)
    log("[re] manifest: %d ordinary + %d external rows; post-write "
        "validation PASS; MANIFEST_VALIDATION.json written last"
        % (man_out["ordinary_rows"], man_out["external_rows"]))
    log("[re] DONE in %.1fs" % (time.time() - T0))
    log("[re] gates: " + json.dumps(
        {k: v["status"] for k, v in gates.items()}))


def main():
    log("[re] RUN E: PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500")
    pin_results = stage0_pins()
    pop325, side_of, split = stage1_census()
    members, nc_full, consumed = s3_tests(pop325, side_of)
    results, verdicts, concentrations, cov = s4_results(
        members, nc_full, consumed)
    gexec_pass, fixtures, audit = s5_gexec()
    with open(os.path.join(CTRL, "PIN_RESULTS.json"),
              encoding="utf-8") as f:
        pin_results = json.load(f)
    s6_outputs(results, verdicts, concentrations, cov, gexec_pass,
               fixtures, audit, split, pin_results)
    log("[re] RUN E COMPLETE. Log lines: %d" % len(LOG_LINES))


if __name__ == "__main__":
    main()
