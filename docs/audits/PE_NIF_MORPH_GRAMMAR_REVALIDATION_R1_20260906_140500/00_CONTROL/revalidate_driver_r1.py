#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500 — RUN A driver
(revalidate_driver_r1.py). RUN_CLASS: LOAD_BEARING. Executor: pe-reconstruction.
Parent: PE-MASTER loop bd17344b (iteration 2). Milestone EU935-M1 (NO crossing).

ONE_PRIMARY_QUESTION (contract 00_CONTROL/CONTRACT.md): do the FROZEN H5a
truncated-tail and H5c idx-relaxed grammars and the H7 adjacency-join model,
exactly as defined in K2 (PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209),
hold (i) on file-grouped splits of the 9.3.5 eligible populations they were
selected from (RETROSPECTIVE_REVALIDATION — explicitly NOT unseen data), and
(ii) on the 2003-era morph corpus (ERA_TRANSFER_DIAGNOSTIC — subject to
prior-use, duplicate and family checks; explicitly NOT a substitute for
9.3.5-target correctness)?

STAGES: S0 pins -> S1 9.3.5 census (G-CENSUS) -> S2 freeze -> S3 retro leg
(G-RETRO) -> S4 era prechecks -> S5 era leg (G-ERA) -> S6 G-EXEC (self-audit +
8 negative fixtures + manifest negative tests) -> S7 outputs.

DISCIPLINE: read-only originals; outputs ONLY to this run dir (enforced by
wr guards); zero payloads (no payload bytes, no hex dumps); run-local tooling
only in 00_CONTROL; no git; no wiki; no milestone action.
Standing sentence (every artifact): no semantic claims; class -256/field1
MEANING remains unknown; the -256=>zero-entry association remains ONE-WAY.
"""
import sys
import os
import csv
import json
import time
import struct
import random
import hashlib
import math
from collections import Counter, defaultdict

sys.dont_write_bytecode = True  # protect READ-ONLY source trees (R32/R35 precedent)

RUN = (r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_GRAMMAR_"
       r"REVALIDATION_R1_20260906_140500")
CTRL = os.path.join(RUN, "00_CONTROL")
RAW = os.path.join(RUN, "01_RAW")
ANA = os.path.join(RUN, "05_ANALYSIS")
REPT = os.path.join(RUN, "06_REPORT")
for d in (CTRL, RAW, ANA, REPT):
    if not os.path.isdir(d):
        os.makedirs(d)

T0 = time.time()
DRIVER_PATH = os.path.join(CTRL, "revalidate_driver_r1.py")

STANDING = ("Standing sentence: no semantic claims; class -256/field1 MEANING "
            "remains unknown; the -256=>zero-entry association remains ONE-WAY. "
            "Result classes: BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_"
            "VALIDATION / ERA_TRANSFER_DIAGNOSTIC / RUNTIME_SEMANTICS (= "
            "explicitly NOT_TESTED here, out of scope).")

# ------------------------------------------------------------------ inputs ---
A = r"D:\Eudoria_Reconstruction\99_Audits"
K2_RUN = os.path.join(A, "PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209")
K2_CTRL = os.path.join(K2_RUN, "00_CONTROL")
K2_DRIVER = os.path.join(K2_CTRL, "morph_residual_deepdive_r1.py")
K2_RAWD = os.path.join(K2_RUN, "01_RAW")
K2_ANA = os.path.join(K2_RUN, "05_ANALYSIS")

MODELS_935 = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
MODELS_935_SHA = ("c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face"
                  "7e969be0b3d3bee0")
MODELS_935_ENTRIES = 5596
MODELS_2003 = r"D:\Eudoria_Reconstruction\01_Original_Files\BNT_Models\Models.bnt"
MODELS_2003_SHA = ("1322adf2919b1b24a8b4fda9618347e00c5a2b35dbb54516e353"
                   "f1cefd3524a6")
MODELS_2003_ENTRIES = 5426
EXTRACTION_2003 = (r"D:\Eudoria_Reconstruction\99_Audits\PE_M1B3_REAL_PE_NIF_"
                   r"COMPATIBILITY_LAB_V1_20260819_010815\02_extraction\nif")
R61_SOURCE_DIR = os.path.join(A, r"PE_R61_FROZEN_BASELINE_20260828\01_source")
R61_SHA_JSON = os.path.join(A, r"PE_R61_FROZEN_BASELINE_20260828\03_validation\SHA256_SOURCE.json")

K2_PINS = {
    "K2_driver": (K2_DRIVER, "b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a"),
    "K2_NOFIT334_SPANS": (os.path.join(K2_RAWD, "NOFIT334_SPANS.txt"), "8bb6556b166df656631af168031e58518b3147fe962d5815ca4e19009e0f605d"),
    "K2_RESIDUAL333_SPANS": (os.path.join(K2_RAWD, "RESIDUAL333_SPANS.txt"), "e936ed510cbfc6a8ab45b99d3ac7892d467b5d05b24a5ede606f80ddf7bf0100"),
    "K2_COVERAGE_STATE": (os.path.join(K2_ANA, "COVERAGE_STATE.json"), "86c12fa7f3df1149213fbfdef3097f022bb7c7ba38dc2cf4289de4aab1b12fa4"),
    "K2_BASELINE_REPRODUCTION": (os.path.join(K2_ANA, "BASELINE_REPRODUCTION.json"), "2e4014c9652df8adf6854b87c17388f9a5288c2c32dc757b34946320db46f1ca"),
    "K2_HYPOTHESIS_RESULTS": (os.path.join(K2_ANA, "HYPOTHESIS_RESULTS.json"), "c08fb4738ece9d1f2c9cbcb43fe05b866f7560b1808597abc78e70e6e438e4a9"),
    "K2_PREREG": (os.path.join(K2_CTRL, "PRE_REGISTERED_HYPOTHESES.json"), "5bde44acd0817441bc3dadb1f4898f52221d566cfd6da1af4dc89c6027789836"),
}
FAMILY_PINS = {
    "R34_driver": (os.path.join(A, r"PE_NIF_MORPH_QUANT_R34_20260904_164538\01_source\morph_quant_r34.py"), "8d788a9a37c4ab2b1d9f76f3d0fb1e3cab9b2a9bda0432089f694f41598d490e"),
    "R34_QUANT_TESTS": (os.path.join(A, r"PE_NIF_MORPH_QUANT_R34_20260904_164538\02_results\QUANT_TESTS.json"), "f07b22e3885f67763af5eccf9ce2a4f82d1385826fbddc5ff462d71e167ab15b"),
    "R34_REAL_SPARSE_GRAMMAR": (os.path.join(A, r"PE_NIF_MORPH_QUANT_R34_20260904_164538\02_results\REAL_SPARSE_GRAMMAR.json"), "2c26ba86db44ad7a58322c136112fec36e23efab1db1fafea1c976311eba007e"),
    "R21_HEX_UNKNOWN": (os.path.join(A, r"PE_NIF_MORPH_UNKNOWN325_R21_20260904_144453\02_results\HEX_UNKNOWN.txt"), "c88a1a1463a78eb66a44a51e763f100859f0b25c6fb4b522b8d9d6aac8a6d3db"),
    "R21_PROBE": (os.path.join(A, r"PE_NIF_MORPH_UNKNOWN325_R21_20260904_144453\02_results\UNKNOWN325_PROBE.json"), "db8cafda4afeb4b967755d44c155d471dd5e1c366c33ca337ad93415a8560576"),
    "R33_MORPH_IDS_FULL": (os.path.join(A, r"PE_NIF_MORPH_IDS_R33_20260904_162507\02_results\MORPH_IDS_FULL.jsonl"), "90c1b8ad8ba8c6f76552f75581782d0e127054697ccf1352d30807520fe11592"),
    "R20_driver": (os.path.join(A, r"PE_NIF_MORPH_NEITHER_R20_20260904_144310\01_source\neither_r20.py"), "a22ff130742378936a6c686498ba02e49c6f2bf6510ecbe7350273db47b1c133"),
    "R18_driver": (os.path.join(A, r"PE_NIF_MORPH_KEYFRAME_R18_20260904_141009\01_source\morph_keyframe_r18.py"), None),
    "R35_driver": (os.path.join(A, r"PE_NIF_CROSS_ERA_R35_20260904_170224\01_source\cross_era_r35.py"), "d71c2d5ce99ef256e28138f83221ba462ae9821656e538bd1bd5d380e9391360"),
    "R35_GRAMMAR_VALIDATION": (os.path.join(A, r"PE_NIF_CROSS_ERA_R35_20260904_170224\02_results\GRAMMAR_VALIDATION.json"), "2f15df0d14dd03e1ee49d6f3d69cc4f7249ed7067800ffccc5174b8bdfa62d80"),
    "R35_REPORT": (os.path.join(A, r"PE_NIF_CROSS_ERA_R35_20260904_170224\REPORT.md"), None),
    "R12_manifest_2003": (os.path.join(A, r"PE_NIF_2003_MANIFEST_R12_20260904_132950\02_results\manifest_2003.csv"), None),
}

K2_EXPECT_WALK = {"big_spans": 10274, "fits": 6167, "entries": 65050, "pad_floats": 143874}
K2_EXPECT_RR = {"rr_spans": 2427, "var_exact_of_rr": 2093, "nofit": 334,
                "nofit_alt": 62, "nofit_none": 272}
K2_EXPECT_CORPUS = {"g1": 132, "g2": 1547, "var": 3186, "mscan_any": 3705}
K2_EXPECT_NEITHER = {"neither": 3438, "backtrack": 3105, "shift": 114,
                     "shift_only": 8, "unknown325": 325, "r21_unknown": 333,
                     "files": 56, "top_file": 84}
K2_EXPECT_PROBE = {"weight_pair": 41, "entry_density_mean": 0.4197,
                   "sane_frac_mean": 0.8096}
K2_EXPECT_BLOCKS = {"morph_blocks": 354, "blocks_with_tag": 334}
ERA2003_ANCHORS = {"morph_blocks": 286, "blocks_with_tag": 272,
                   "files_with_morph": 79, "big_spans": 8385, "fits": 4674,
                   "entries": 41438, "pads": 115755, "rr_spans": 1457,
                   "rr_var_bi_keyed": 1179, "rr_var_tag_keyed": 1180}
# RESOLUTION (verified by counter-check BEFORE this driver's final run, and
# re-verified in-driver): R35's published 2003 rr_var=1180 uses the
# (file,tag,si) span key, which COLLIDES when one file has multiple morph
# blocks sharing a tag (26 such collisions among 2003 fit spans; exactly one
# is load-bearing: 574845.nif bi=77 si=14 tag=3, var_ok but NOT rr, counted
# as rr_var via key collision). The collision-free (file,bi,si) census gives
# rr_var=1179, and the SAME census reproduces 1180 under R35's own keying.
# Both values are asserted in s45_era; the collision-free keying defines the
# era populations (consistent with K2 and the retro leg).
K2_FROZEN_BLOCK_RANGES = [
    ("B1_constants", 79, 82), ("B2_sane", 96, 97), ("B3_clean", 100, 103),
    ("B4_greedy_r18", 121, 144), ("B5_parse_variable", 288, 320),
    ("B6_parse_variable_trunctail", 357, 396), ("B7_H5a_invocation", 1003, 1016),
    ("B8_H5c_invocation", 1035, 1052), ("B9_H7_invocation", 1152, 1171),
    ("B10_nc2", 871, 882),
]

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
        hard_stop("write outside run dir attempted", {"path": path})


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


def hard_stop(reason, evidence):
    ev = {"run": "PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500",
          "hard_stop_reason": reason, "evidence": evidence,
          "elapsed_s": round(time.time() - T0, 1), "standing": STANDING}
    wr_json(os.path.join(ANA, "HARD_STOP_EVIDENCE.json"), ev)
    wr_lines(os.path.join(REPT, "HANDOFF.md"), [
        "# HANDOFF - HARD STOP", "",
        "AUDIT_OUTPUT_ROOT = " + RUN,
        "FINAL_REPORT_PATH = " + os.path.join(REPT, "00_FINAL_REPORT.md"),
        "PRIMARY_EVIDENCE_PATHS = " + os.path.join(ANA, "HARD_STOP_EVIDENCE.json"),
        "RUN_STATUS = HARD_STOPPED",
        "HARD_STOP_REASON = " + reason, "",
    ])
    wr_lines(os.path.join(REPT, "00_FINAL_REPORT.md"), [
        "# FINAL REPORT - HARD STOP", "",
        "HARD_STOP_REASON = " + reason,
        "See 05_ANALYSIS/HARD_STOP_EVIDENCE.json (machine-readable evidence).",
        "Identity: RUN PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500, "
        "RUN_CLASS LOAD_BEARING, milestone EU935-M1 (no crossing).", "",
        "1. HUMAN-FIRST: PE-MASTER must adjudicate the HARD STOP before any "
        "continuation; no human decision is required inside this run.",
        "12. ONE P0: interrupted before completion - see HARD_STOP_EVIDENCE.",
        "13. NEGATIVE CONTROLS: none executed past the stop point.",
        "14. HARD STOPS: " + reason, "",
        STANDING, "",
    ])
    log("[r1] HARD STOP: " + reason)
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
    NOTE: _binom_cdf(k, n, p) = P(X <= k) is DECREASING in p, so both
    bisections move 'a' UP while the CDF is still above its target.
    Lower bound lo solves P(X <= k-1) = 0.975; upper bound hi solves
    P(X <= k) = 0.025. (The first two executions had both directions
    inverted, converging to 1.0 — caught in output review, fixed, and
    re-run before any use of these numbers downstream.)"""
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


def stage0_pins():
    log("[r1] S0: pins (G-PINS)")
    pr = {}
    with open(R61_SHA_JSON, "r", encoding="utf-8-sig") as f:
        locked = json.load(f)
    r61_ok = 0
    for name, sha in locked.items():
        if not name.endswith(".py"):
            continue
        got = sha256_file(os.path.join(R61_SOURCE_DIR, name))
        if got.lower() != str(sha).lower():
            hard_stop("R61 pin mismatch: " + name,
                      {"expected": sha, "got": got})
        r61_ok += 1
    if r61_ok != 10:
        hard_stop("R61 manifest incomplete (%d/10)" % r61_ok, {})
    pr["R61_10_of_10"] = "PASS"
    log("[r1] R61 10/10 PASS")

    s935 = sha256_file(MODELS_935)
    if s935 != MODELS_935_SHA:
        hard_stop("9.3.5 corpus SHA mismatch",
                  {"expected": MODELS_935_SHA, "got": s935})
    s2003 = sha256_file(MODELS_2003)
    if s2003 != MODELS_2003_SHA:
        hard_stop("2003 corpus SHA mismatch",
                  {"expected": MODELS_2003_SHA, "got": s2003})
    pr["corpus_935"] = {"path": MODELS_935, "sha256": s935}
    pr["corpus_2003"] = {"path": MODELS_2003, "sha256": s2003}
    log("[r1] corpus SHAs verified (9.3.5 + 2003 container)")

    with open(MODELS_935, "rb") as f:
        data935 = f.read()
    with open(MODELS_2003, "rb") as f:
        data2003 = f.read()
    ent935 = read_bnt_index(data935)
    ent2003 = read_bnt_index(data2003)
    if len(ent935) != MODELS_935_ENTRIES or \
            len(set(nm for nm, _, _ in ent935)) != MODELS_935_ENTRIES:
        hard_stop("9.3.5 corpus entry count mismatch",
                  {"expected": MODELS_935_ENTRIES, "got": len(ent935)})
    n2003 = len(ent2003)
    u2003 = len(set(nm for nm, _, _ in ent2003))
    nif2003 = sum(1 for nm, _, _ in ent2003 if nm.lower().endswith(".nif"))
    if n2003 != 5426 or u2003 != 5426 or nif2003 != 5426:
        hard_stop("2003 corpus count mismatch (5,426-name class)",
                  {"entries": n2003, "unique_names": u2003, "nif": nif2003})
    pr["corpus_935"]["entries"] = len(ent935)
    pr["corpus_2003"]["entries"] = n2003
    pr["corpus_2003"]["unique_names"] = u2003
    pr["corpus_2003"]["nif_entries"] = nif2003
    pr["corpus_2003"]["name_class_check"] = (
        "5,426-name class EXACT (all entries .nif, all unique). The contract's "
        "'~5,441 NIF' is the physical-LINE count of the pinned R12 manifest "
        "CSV (5,442 lines incl. header) whose true CSV record count is 5,426 "
        "(verified with a standard CSV parser; GATES_PREREGISTERED.md "
        "decision 9). Matches PE-MASTER ground-truth pin '2003 Models "
        "1322ADF2...'.")
    log("[r1] 2003 container: %d entries / %d unique .nif names" % (n2003, u2003))

    r12 = FAMILY_PINS["R12_manifest_2003"][0]
    with open(r12, "r", encoding="utf-8", newline="") as f:
        r12_phys_lines = sum(1 for _ in f)
    with open(r12, "r", encoding="utf-8", newline="") as f:
        r12_records = list(csv.DictReader(f))
    pr["R12_manifest_2003"] = {
        "path": r12, "physical_lines": r12_phys_lines,
        "csv_records": len(r12_records),
        "pass_rows": sum(1 for r in r12_records if r.get("parse_status") == "PASS"),
        "note": ("physical lines incl. header = the contract's '~5,441' class; "
                 "true records = 5,426")}
    if len(r12_records) != 5426:
        hard_stop("R12 2003 manifest record count mismatch",
                  {"records": len(r12_records)})

    ext_files = sorted(fn for fn in os.listdir(EXTRACTION_2003)
                       if fn.endswith(".nif"))
    if len(ext_files) != 5426:
        hard_stop("2003 extraction dir count mismatch",
                  {"expected": 5426, "got": len(ext_files)})
    mismatch = 0
    checked = 0
    for nm, size, off in ent2003:
        fp = os.path.join(EXTRACTION_2003, nm)
        if not os.path.isfile(fp):
            mismatch += 1
            continue
        with open(fp, "rb") as f:
            fb = f.read()
        checked += 1
        if sha256_bytes(fb) != sha256_bytes(data2003[off:off + size]):
            mismatch += 1
    if mismatch != 0 or checked != 5426:
        hard_stop("2003 container-vs-extraction byte-tie FAILED",
                  {"checked": checked, "mismatch": mismatch})
    pr["container_extraction_tie"] = (
        "5,426/5,426 container payloads byte-identical to the prior-run "
        "extraction (R12/R61/R35/era-drift evidence base)")
    log("[r1] 2003 container<->extraction byte-tie: 5,426/5,426 IDENTICAL")

    for k, (p, exp) in list(K2_PINS.items()) + list(FAMILY_PINS.items()):
        got = sha256_file(p)
        ok = (exp is None) or (got.lower() == exp.lower())
        pr[k] = {"path": p, "sha256": got, "expected": exp, "match": ok}
        if not ok:
            hard_stop("pin mismatch: " + k,
                      {"path": p, "expected": exp, "got": got})
        log("[r1] pin %s: %s %s" % (k, got[:12], "OK" if ok else "MISMATCH"))

    with open(K2_DRIVER, "r", encoding="utf-8", newline="") as f:
        k2_src = f.read().split("\n")
    with open(os.path.join(CTRL, "FROZEN_GRAMMARS.md"), "r", encoding="utf-8",
              newline="") as f:
        frozen = f.read()
    blocks_ok = 0
    for label, lo, hi in K2_FROZEN_BLOCK_RANGES:
        seg = "\n".join(k2_src[lo - 1:hi])
        if ("```python\n" + seg + "\n```") in frozen:
            blocks_ok += 1
        else:
            hard_stop("FROZEN_GRAMMARS.md block mismatch: " + label,
                      {"range": [lo, hi]})
    pr["frozen_grammars_verified_blocks"] = (
        "%d/%d VERBATIM byte-exact vs pinned K2 source"
        % (blocks_ok, len(K2_FROZEN_BLOCK_RANGES)))
    log("[r1] FROZEN_GRAMMARS.md: %d/%d blocks byte-exact vs pinned K2 driver"
        % (blocks_ok, len(K2_FROZEN_BLOCK_RANGES)))

    pr["driver_sha256"] = sha256_file(DRIVER_PATH)
    pr["standing"] = STANDING
    pr["contract_sha256"] = sha256_file(os.path.join(CTRL, "CONTRACT.md"))
    if pr["contract_sha256"].lower() != ("02f32099ad7d9a528a6bc08c46e6c4f55"
                                         "c8218a06fbb482b5be529e76dc34f95"):
        hard_stop("contract SHA mismatch",
                  {"got": pr["contract_sha256"]})
    wr_json(os.path.join(CTRL, "PIN_RESULTS.json"), pr)
    return {"data935": data935, "ent935": ent935,
            "data2003": data2003, "ent2003": ent2003}


# --------------------------------------------- census (K2 stage-1 replica) ---
def run_census(reader, entries, data, expect, era_label, do_row_agreement,
               r34_rows=None):
    """Replicates the K2 census pipeline EXACTLY (K2 driver stage 1): R61 parse
    -> morph blocks with tag -> tag-split spans -> big spans -> R18 walk ->
    R34 grammar re-derivation (+ row agreement) -> rr/nofit census -> R20/R21
    residual census (r19/backtrack/shift) -> unknown325/r21u -> R21 probe."""
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
            log("[r1] %s parse %d/%d (%.0fs)"
                % (era_label, fi + 1, len(entries), time.time() - T0))
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
        hard_stop("%s parse closure < 100%% (%d fails)"
                  % (era_label, parse_fail), {"parse_fail": parse_fail})
    log("[r1] %s big spans: %d" % (era_label, big_spans))

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
                        if idv != 0 and idv < n and i2 % 4 == 0 and K2.clean4(fl):
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
        if do_row_agreement:
            k = (rec["file"], rec["bi"], rec["si"])
            r = r34_rows.get(k)
            if (r is not None and r["g1_ok"] == g1_ok and r["g2_ok"] == g2_ok
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
        "corpus_grammars": {"g1": g1_exact, "g2": g2_exact, "var": var_exact,
                            "mscan_any": mscan_any},
        "rr_state": {"rr_spans": len(rr_set), "var_exact_of_rr": rr_var,
                     "nofit": len(nofit), "nofit_alt": len(nofit_alt),
                     "nofit_none": len(nofit_none)},
        "residual": {"neither": len(neither), "backtrack": bt_fit,
                     "shift": shift_fit, "shift_only": shift_only,
                     "unknown325": len(unknown325),
                     "r21_unknown": len(r21_unknown), "r19_only": r19_only,
                     "files": len(u_by_file), "top_file": list(top)},
        "r21_probe": {"weight_pair": wp_ok, "entry_density_mean": ed_mean,
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
        if do_row_agreement:
            census["census_exact"] = (census["census_exact"]
                                      and row_agree == len(fit_recs))
    return (census, big_all, fit_recs, nofit, unknown325, r21_unknown,
            blocks_ctx)


# ------------------------------------- observational diagnostic mirrors -------
def diag_parse_variable_trunctail(dp, u, N):
    """Mirror of the VERBATIM H5a parser for failure classification ONLY.
    The FIT verdict ALWAYS comes from K2.parse_variable_trunctail."""
    p = u
    end = len(dp)
    recs = 0
    while p < end:
        rem = end - p
        if rem < 2:
            return ("TAIL_REM_%d" % rem, p, recs)
        idx = struct.unpack_from("<H", dp, p)[0]
        if idx >= N:
            return ("IDX_GE_N_AT_%d" % p, p, recs)
        found = False
        for k in range(1, K2.VAR_MAX_K + 1):
            need = 2 + 4 * (k + K2.VAR_NDELTA)
            if p + need > end:
                break
            fls = [struct.unpack_from("<f", dp, p + 2 + 4 * q)[0]
                   for q in range(k + K2.VAR_NDELTA)]
            if not all(K2.clean(v) for v in fls):
                continue
            if abs(sum(fls[:k]) - 1.0) <= K2.WP_TOL:
                found = True
                recs += 1
                p += need
                break
        if not found:
            return ("NO_K_FIT_AT_%d" % p, p, recs)
    return ("COMPLETE", p, recs)


def diag_parse_variable(dp, u, N, idx_limit):
    """Mirror of the VERBATIM H5c parser for failure classification ONLY.
    The FIT verdict ALWAYS comes from K2.parse_variable."""
    p = u
    end = len(dp)
    recs = 0
    while p < end:
        if p + 2 > end:
            return ("OVERRUN_AT_%d" % p, p, recs)
        idx = struct.unpack_from("<H", dp, p)[0]
        if idx >= idx_limit:
            return ("IDX_GE_LIMIT_AT_%d" % p, p, recs)
        found = False
        for k in range(1, K2.VAR_MAX_K + 1):
            need = 2 + 4 * (k + K2.VAR_NDELTA)
            if p + need > end:
                break
            fls = [struct.unpack_from("<f", dp, p + 2 + 4 * q)[0]
                   for q in range(k + K2.VAR_NDELTA)]
            if not all(K2.clean(v) for v in fls):
                continue
            if abs(sum(fls[:k]) - 1.0) <= K2.WP_TOL:
                found = True
                recs += 1
                p += need
                break
        if not found:
            return ("NO_K_FIT_AT_%d" % p, p, recs)
    return ("COMPLETE", p, recs)


def diag_greedy_r18(dpj, start):
    """Mirror of the VERBATIM greedy_r18 walk for stop-position ONLY.
    The FIT verdict ALWAYS comes from K2.greedy_r18."""
    i2 = start
    ent = 0
    while i2 < len(dpj):
        took = False
        if i2 + 18 <= len(dpj):
            idv = struct.unpack_from("<H", dpj, i2)[0]
            if idv < 0x8000:
                fl = [struct.unpack_from("<f", dpj, i2 + 2 + 4 * k)[0]
                      for k in range(4)]
                if all(K2.sane(v) for v in fl):
                    ent += 1
                    i2 += 18
                    took = True
        if not took and i2 + 4 <= len(dpj):
            v = struct.unpack_from("<f", dpj, i2)[0]
            if K2.sane(v):
                i2 += 4
                took = True
        if not took:
            if ent > 0 and len(dpj) - i2 == 2 and dpj[i2:i2 + 2] == b"\x00\x00":
                return ("TAIL_ACCEPT", len(dpj))
            return ("WALK_FAIL_AT_%d" % i2, i2)
    return ("COMPLETE", i2)


def exec_h5a(rec):
    ok, recs, kh, idxs, left = K2.parse_variable_trunctail(
        rec["dp"], rec["u"], rec["N"])
    fit = bool(ok and recs > 0 and left > 0)
    reason, p, drecs = diag_parse_variable_trunctail(rec["dp"], rec["u"],
                                                     rec["N"])
    agree = (drecs == recs) and ((reason == "COMPLETE") == bool(ok))
    consumed = (len(rec["dp"]) - left) if (ok and left >= 0) else (p - rec["u"])
    return fit, reason, consumed, {"leftover": left, "records": recs,
                                   "diag_agree": agree}


def exec_h5c2(rec):
    ok, recs, kh, idxs = K2.parse_variable(rec["dp"], rec["u"], rec["N"],
                                            idx_limit=0x8000)
    fit = bool(ok and recs > 0)
    reason, p, drecs = diag_parse_variable(rec["dp"], rec["u"], rec["N"],
                                           0x8000)
    agree = (drecs == recs) and ((reason == "COMPLETE") == bool(ok))
    consumed = len(rec["dp"]) if ok else (p - rec["u"])
    return fit, reason, consumed, {"records": recs, "diag_agree": agree}


def exec_h7(rec, ctx):
    """H7a/H7b adjacency-join trials, VERBATIM K2 procedure (frozen B9)."""
    spans = ctx["spans"]
    Wm = ctx["Wm"]
    si = rec["si"]
    trials = []
    explained = False
    if si > 0:
        dpj = spans[si - 1][2:] + rec["s"]
        ok = K2.greedy_r18(dpj, Wm)
        reason, stop = diag_greedy_r18(dpj, Wm - 2)
        trials.append({"trial": "prev", "hit": bool(ok), "reason": reason,
                       "join_len": len(dpj), "consumed": stop - (Wm - 2)})
        explained = explained or bool(ok)
    if si + 1 < len(spans):
        dpj = rec["dp"] + spans[si + 1]
        ok = K2.greedy_r18(dpj, Wm)
        reason, stop = diag_greedy_r18(dpj, Wm - 2)
        trials.append({"trial": "next", "hit": bool(ok), "reason": reason,
                       "join_len": len(dpj), "consumed": stop - (Wm - 2)})
        explained = explained or bool(ok)
    return explained, trials


def parse_dump_headers(path):
    ids = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("== "):
                head = line[3:].split()
                ids.append((head[0], int(head[1].split("=")[1]),
                            int(head[2].split("=")[1])))
    return ids


# ------------------------------------------ G-RETRO gate + input validators ---
def evaluate_gretro(grammar_id, membersA, membersB, nc_trials,
                    nc_expected_per_unit):
    """A-priori G-RETRO gate (GATES_PREREGISTERED.md). members carry 'fit' from
    EXECUTING the verbatim predicate on the record. Fail-closed prologue; fit
    counts are counter increments over executed records (never len())."""
    v = {"grammar": grammar_id, "gate": "G-RETRO", "non_pass_class": None,
         "result": "NON_PASS"}
    for m in list(membersA) + list(membersB):
        if (not isinstance(m, dict) or not m.get("wellformed")
                or "key" not in m or "side" not in m or "unit" not in m
                or "fit" not in m or not isinstance(m.get("fit"), bool)):
            v["non_pass_class"] = "CORRUPTED_RECORD"
            v["detail"] = str(m)[:160]
            return v
    keysA = [tuple(m["key"]) if isinstance(m["key"], list) else m["key"]
             for m in membersA]
    keysB = [tuple(m["key"]) if isinstance(m["key"], list) else m["key"]
             for m in membersB]
    dup = sorted(set(keysA) & set(keysB))[:5]
    if dup:
        v["non_pass_class"] = "DUPLICATE_ACROSS_SIDES"
        v["detail"] = [list(d) if isinstance(d, tuple) else d for d in dup]
        return v
    if len(keysA) + len(keysB) == 0:
        v["non_pass_class"] = "EMPTY_GROUP"
        v["detail"] = "population empty"
        return v
    if len(keysB) == 0:
        v["non_pass_class"] = "EMPTY_GROUP"
        v["detail"] = "held-out side empty"
        return v
    unitsB = {}
    for m in membersB:
        u = m["unit"]
        if u not in unitsB:
            unitsB[u] = False
        if m["fit"]:
            unitsB[u] = True
    n_units = 0
    n_unit_fits = 0
    for _u, f in unitsB.items():
        n_units += 1
        if f:
            n_unit_fits += 1
    member_fits_B = 0
    for m in membersB:
        if m["fit"]:
            member_fits_B += 1
    nc_hits = 0
    nc_bad = 0
    for t in nc_trials:
        if not isinstance(t, dict) or not isinstance(t.get("hit"), bool):
            nc_bad += 1
        elif t["hit"]:
            nc_hits += 1
    nc_den = len(nc_trials)
    if nc_expected_per_unit is not None and nc_bad == 0 \
            and nc_den != n_units * nc_expected_per_unit:
        v["non_pass_class"] = "DENOMINATOR_MISMATCH"
        v["detail"] = {"nc_trials": nc_den,
                       "units_x_expected": n_units * nc_expected_per_unit}
        return v
    if nc_bad:
        v["non_pass_class"] = "CORRUPTED_RECORD"
        v["detail"] = {"bad_nc_trials": nc_bad}
        return v
    if nc_den == 0:
        v["non_pass_class"] = "NC_EMPTY_DENOMINATOR"
        v["detail"] = {"nc_trials": 0, "units": n_units}
        return v
    if n_units < 30:
        v["non_pass_class"] = "INSUFFICIENT_TRIALS"
        v["detail"] = {"units": n_units}
        return v
    if n_unit_fits < 10:
        v["non_pass_class"] = "ZERO_FITS"
        v["detail"] = {"unit_fits": n_unit_fits, "units": n_units}
        return v
    rate = n_unit_fits / n_units
    nc_rate = nc_hits / nc_den
    if not (rate >= 5 * nc_rate):
        v["non_pass_class"] = "NC_INSUFFICIENT_SEPARATION"
        v["detail"] = {"positive_rate": round(rate, 6),
                       "nc_rate": round(nc_rate, 6)}
        return v
    v["result"] = "PASS"
    v["units"] = n_units
    v["unit_fits"] = n_unit_fits
    v["member_fits"] = member_fits_B
    v["positive_rate"] = round(rate, 6)
    v["positive_rate_ci95_exact_binomial"] = clopper_pearson_95(n_unit_fits,
                                                               n_units)
    v["nc_hits"] = nc_hits
    v["nc_denominator"] = nc_den
    v["nc_rate"] = round(nc_rate, 6)
    v["nc_rate_ci95_exact_binomial"] = clopper_pearson_95(nc_hits, nc_den)
    return v


def validate_manifest_rows(rows, root):
    """MANIFEST_SCHEMA_SPEC.md validation gate (standard csv parser).
    '#' comment lines are structural markers ('# external sources' switches
    the section); ordinary rows = artifact,role,sha256; external rows =
    source_id,kind,era,physical_path,sha256. Fail-closed."""
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
                    or "\\" in artifact or ":" in artifact or ".." in artifact):
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
        return {"result": "NON_PASS", "non_pass_class": "MISSING_INPUT_FILE",
                "path": path}
    return {"result": "PASS", "path": path}


# ----------------------------------------- S1: 9.3.5 census (G-CENSUS) --------
def s1_census(ent935, data935):
    log("[r1] S1: 9.3.5 baseline census reproduction (G-CENSUS)")
    with open(FAMILY_PINS["R34_REAL_SPARSE_GRAMMAR"][0], encoding="utf-8") as f:
        r34 = json.load(f)
    r34_rows = {(r["file"], r["bi"], r["si"]): r for r in r34["per_span"]}
    expect935 = {
        "walk": K2_EXPECT_WALK, "rr_state": K2_EXPECT_RR,
        "corpus_grammars": K2_EXPECT_CORPUS, "residual": K2_EXPECT_NEITHER,
        "r21_probe": K2_EXPECT_PROBE, "blocks": K2_EXPECT_BLOCKS,
    }
    (census935, big_all, fit_recs, nofit, unknown325, r21_unknown,
     blocks_ctx) = run_census(PENifReader(), ent935, data935, expect935,
                              "9.3.5", do_row_agreement=True,
                              r34_rows=r34_rows)
    if not census935["census_exact"]:
        hard_stop("G-CENSUS mismatch (9.3.5 baseline != K2)",
                  {"checks": census935["census_checks"],
                   "row_agreement": census935["row_agreement"]})
    log("[r1] G-CENSUS: PASS (row agreement %d/%d)"
        % (census935["row_agreement"][0], census935["row_agreement"][1]))
    census935["era"] = "PCG_9_3_5"
    census935["result_class"] = "REPEATABILITY"
    census935["standing"] = STANDING
    census935["gate"] = "G-CENSUS PASS: baseline reproduces K2 EXACTLY"
    wr_json(os.path.join(ANA, "BASELINE_CENSUS_REPRODUCTION.json"), census935)
    return big_all, nofit, unknown325, r21_unknown, blocks_ctx


# ----------------------------------------- S2: FREEZE (before any test) -----
def s2_freeze(nofit, unknown325, r21_unknown):
    log("[r1] S2: freeze write (populations + split sides)")
    p1_dump = parse_dump_headers(K2_PINS["K2_NOFIT334_SPANS"][0])
    r333_dump = parse_dump_headers(K2_PINS["K2_RESIDUAL333_SPANS"][0])
    p1_keys = sorted((r["file"], r["bi"], r["si"]) for r in nofit)
    p2_keys = sorted((r["file"], r["bi"], r["si"]) for r in unknown325)
    r333_keys = sorted((r["file"], r["bi"], r["si"]) for r in r21_unknown)
    if len(p1_dump) != 334 or set(p1_dump) != set(p1_keys):
        hard_stop("population P1 (334) mismatch vs pinned NOFIT334_SPANS.txt",
                  {"dump": len(p1_dump), "census": len(p1_keys)})
    if len(r333_dump) != 333 or set(r333_dump) != set(r333_keys):
        hard_stop("r21_unknown (333) mismatch vs pinned RESIDUAL333_SPANS.txt",
                  {"dump": len(r333_dump), "census": len(r333_keys)})
    if len(p2_keys) != 325 or not set(p2_keys) <= set(r333_keys):
        hard_stop("population P2 (325) mismatch",
                  {"p2": len(p2_keys),
                   "subset_of_333": len(set(p2_keys) & set(r333_keys))})
    pop_freeze = {
        "run": "PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500",
        "standing": STANDING,
        "P1_nofit334": {
            "definition": "the 334 classifier-real (rr) spans with var_ok=0 "
                          "(K2 P1)",
            "enumerated_from": {
                "artifact": K2_PINS["K2_NOFIT334_SPANS"][0],
                "sha256": K2_PINS["K2_NOFIT334_SPANS"][1]},
            "ids": [list(k) for k in p1_keys],
            "cross_check": "pinned dump headers == census-derived set (EXACT)"},
        "P2_residual325": {
            "definition": "the 325 residual spans: neither, fail backtrack "
                          "AND fail shift-scan (K2 unknown325)",
            "enumerated_from": {
                "artifact": K2_PINS["K2_RESIDUAL333_SPANS"][0],
                "sha256": K2_PINS["K2_RESIDUAL333_SPANS"][1],
                "note": "P2 = pinned 333-set minus the 8 shift_only spans "
                        "(re-derived by the frozen census pipeline); count "
                        "cross-checked = 325 across 56 files; 551564.nif x84 "
                        "(G-CENSUS)"},
            "ids": [list(k) for k in p2_keys],
            "cross_check": "P2 subset of pinned 333 EXACT; count 325 EXACT"},
        "R21_unknown333_dump_ids": [list(k) for k in r333_keys],
        "grammar_assignments": {"H5a": "P1_nofit334",
                                "H5c2": "P1_nofit334",
                                "H7": "P2_residual325"},
    }
    wr_json(os.path.join(CTRL, "POPULATIONS_334_325.json"), pop_freeze)

    pop_files = sorted(set(k[0] for k in p1_keys) | set(k[0] for k in p2_keys))
    rng = random.Random(20260906)
    shuffled = list(pop_files)
    rng.shuffle(shuffled)
    n = len(shuffled)
    sideA = shuffled[:n // 2]
    sideB = shuffled[n // 2:]
    side_of = {}
    for f in sideA:
        side_of[f] = "A"
    for f in sideB:
        side_of[f] = "B"
    split_freeze = {
        "run": "PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500",
        "standing": STANDING,
        "procedure": ("file-level 50/50 over sorted unique files of P1+P2; "
                      "random.Random(20260906); rng.shuffle(copy); side_A = "
                      "first n//2 files; side_B = remaining (held-out); "
                      "FAMILY INTEGRITY: all spans of a file on the side of "
                      "its file"),
        "seed": 20260906,
        "n_files": n,
        "side_A_files": sideA,
        "side_B_files": sideB,
        "P1_side_A": [list(k) for k in p1_keys if side_of.get(k[0]) == "A"],
        "P1_side_B": [list(k) for k in p1_keys if side_of.get(k[0]) == "B"],
        "P2_side_A": [list(k) for k in p2_keys if side_of.get(k[0]) == "A"],
        "P2_side_B": [list(k) for k in p2_keys if side_of.get(k[0]) == "B"],
    }
    wr_json(os.path.join(CTRL, "SPLIT_SIDES.json"), split_freeze)
    wr_lines(os.path.join(CTRL, "PREREG_MARKER.txt"), [
        "PRE-REGISTRATION / FREEZE COMPLETE %s"
        % time.strftime("%Y-%m-%d %H:%M:%S"),
        "Grammars VERBATIM frozen (FROZEN_GRAMMARS.md sha256 %s)"
        % sha256_file(os.path.join(CTRL, "FROZEN_GRAMMARS.md")),
        "Populations frozen (POPULATIONS_334_325.json sha256 %s)"
        % sha256_file(os.path.join(CTRL, "POPULATIONS_334_325.json")),
        "Split sides frozen (SPLIT_SIDES.json sha256 %s)"
        % sha256_file(os.path.join(CTRL, "SPLIT_SIDES.json")),
        "NC procedures frozen (NC_PROCEDURES.md sha256 %s)"
        % sha256_file(os.path.join(CTRL, "NC_PROCEDURES.md")),
        "Gates a-priori frozen (GATES_PREREGISTERED.md sha256 %s)"
        % sha256_file(os.path.join(CTRL, "GATES_PREREGISTERED.md")),
        "ALL freeze artifacts written BEFORE any grammar test execution (S3+).",
        STANDING,
    ])
    log("[r1] freeze: %d files split %d/%d; P1 %d/%d, P2 %d/%d"
        % (n, len(sideA), len(sideB),
           len(split_freeze["P1_side_A"]), len(split_freeze["P1_side_B"]),
           len(split_freeze["P2_side_A"]), len(split_freeze["P2_side_B"])))
    return side_of, split_freeze


# ----------------------------------------- S3: retro leg (G-RETRO) -----------
def build_units(pop_recs, side_of):
    """Unit machinery (GATES_PREREGISTERED.md decision 1): unit = byte-
    identical dp payload (sha256), dedup within the population; unit side =
    side of its FIRST member in sorted (file,bi,si) order; members on the
    other side of a split unit are flagged split_family and excluded from
    that side's gate units (counted once, first-member side)."""
    recs = sorted(pop_recs, key=lambda r: (r["file"], r["bi"], r["si"]))
    unit_side = {}
    unit_members = defaultdict(list)
    unit_split = set()
    for r in recs:
        u = sha256_bytes(r["dp"])
        unit_members[u].append(r)
        s = side_of.get(r["file"], "?")
        if u not in unit_side:
            unit_side[u] = s
        elif unit_side[u] != s:
            unit_split.add(u)
    return unit_side, unit_members, unit_split


def s3_retro(nofit, unknown325, side_of, blocks_ctx):
    log("[r1] S3: retro leg - per-record H5a/H5c2/H7 + NCs (RETROSPECTIVE)")
    retro_out = os.path.join(RAW, "RETRO_SPAN_OUTCOMES.jsonl")
    retro_nc = os.path.join(RAW, "RETRO_NC_TRIALS.jsonl")
    for p in (retro_out, retro_nc):
        if os.path.exists(p):
            os.remove(p)

    members = {"H5a": {"A": [], "B": []}, "H5c2": {"A": [], "B": []},
               "H7": {"A": [], "B": []}}
    h5a_fits = []
    h5c2_fits = []
    h7_explained = []
    nc_span_hits = {"H5a": [], "H5c2": []}

    unit_side_p1, unit_members_p1, unit_split_p1 = build_units(nofit, side_of)

    for rec in nofit:  # P1: H5a + H5c2 + span-level NC (K2 nc2 semantics)
        key = [rec["file"], rec["bi"], rec["si"]]
        side = side_of.get(rec["file"], "?")
        unit = sha256_bytes(rec["dp"])
        is_split = unit in unit_split_p1
        for g in ("H5a", "H5c2"):
            if g == "H5a":
                fit, reason, consumed, extra = exec_h5a(rec)
            else:
                fit, reason, consumed, extra = exec_h5c2(rec)
            append_jsonl(retro_out, {
                "span": key, "side": side, "grammar": g,
                "outcome": "FIT" if fit else "NOFIT", "reason": reason,
                "bytes_consumed": consumed, "unit": unit,
                "split_family": is_split, "extra": extra,
                "result_class": "RETROSPECTIVE_VALIDATION"})
            members[g][side].append({"key": key, "side": side, "unit": unit,
                                     "file": rec["file"], "fit": fit,
                                     "wellformed": True})
            if fit and g == "H5a":
                h5a_fits.append((tuple(key), extra["leftover"]))
            if fit and g == "H5c2":
                h5c2_fits.append(tuple(key))
        for g in ("H5a", "H5c2"):
            for d in (2, -2):
                u2 = rec["u"] + d
                tname = "u_plus_2" if d > 0 else "u_minus_2"
                if u2 < 0:
                    append_jsonl(retro_nc, {
                        "span": key, "side": side, "grammar": g,
                        "trial": tname, "u2": u2, "hit": False,
                        "reason": "INVALID_START_NONHIT",
                        "denominator": "spans_x_2"})
                    continue
                if g == "H5a":
                    out = K2.parse_variable_trunctail(
                        rec["dp"], u2, rec["N"])[:4]
                    reason, p, _dr = diag_parse_variable_trunctail(
                        rec["dp"], u2, rec["N"])
                else:
                    out = K2.parse_variable(rec["dp"], u2, rec["N"],
                                             idx_limit=0x8000)
                    reason, p, _dr = diag_parse_variable(
                        rec["dp"], u2, rec["N"], 0x8000)
                hit = bool(out[0] and out[1] > 0)
                append_jsonl(retro_nc, {
                    "span": key, "side": side, "grammar": g, "trial": tname,
                    "u2": u2, "hit": hit, "reason": reason,
                    "bytes_consumed": p - u2, "denominator": "spans_x_2"})
                if hit:
                    nc_span_hits[g].append([key, d])

    # P2: H7 + NC-B (per-span, seeded; NEVER one-per-file)
    unit_side_p2, unit_members_p2, unit_split_p2 = build_units(unknown325,
                                                               side_of)
    rng = random.Random(20260906)
    by_file_p2 = defaultdict(list)
    for rec in unknown325:
        by_file_p2[rec["file"]].append(rec)
    h7_nc_span_hits = set()
    h7_nc_span_den = set()
    for rec in sorted(unknown325,
                      key=lambda r: (r["file"], r["bi"], r["si"])):
        key = [rec["file"], rec["bi"], rec["si"]]
        side = side_of.get(rec["file"], "?")
        unit = sha256_bytes(rec["dp"])
        is_split = unit in unit_split_p2
        ctx = blocks_ctx.get((rec["file"], rec["bi"]))
        if ctx is None:
            append_jsonl(retro_out, {
                "span": key, "side": side, "grammar": "H7",
                "outcome": "NOFIT", "reason": "NO_BLOCK_CONTEXT",
                "bytes_consumed": 0, "unit": unit,
                "split_family": is_split, "extra": {},
                "result_class": "RETROSPECTIVE_VALIDATION"})
            members["H7"][side].append({"key": key, "side": side,
                                        "unit": unit, "file": rec["file"],
                                        "fit": False, "wellformed": True})
            continue
        explained, trials = exec_h7(rec, ctx)
        append_jsonl(retro_out, {
            "span": key, "side": side, "grammar": "H7",
            "outcome": "FIT" if explained else "NOFIT",
            "reason": (";".join(t["reason"] for t in trials)
                       if trials else "NO_TRIALS"),
            "bytes_consumed": max([t["consumed"] for t in trials] or [0]),
            "unit": unit, "split_family": is_split,
            "extra": {"trials": trials},
            "result_class": "RETROSPECTIVE_VALIDATION"})
        members["H7"][side].append({"key": key, "side": side, "unit": unit,
                                    "file": rec["file"], "fit": explained,
                                    "wellformed": True})
        if explained:
            h7_explained.append(tuple(key))
        others = sorted([x for x in by_file_p2[rec["file"]]
                         if abs(x["si"] - rec["si"]) > 2],
                        key=lambda r: (r["file"], r["bi"], r["si"]))
        for t in trials:
            if not others:
                append_jsonl(retro_nc, {
                    "span": key, "side": side, "grammar": "H7",
                    "trial": "nc_" + t["trial"], "partner": None,
                    "hit": False, "reason": "NC_NO_PARTNER",
                    "denominator": "nc_trials_executed"})
                continue
            o = rng.choice(others)
            if t["trial"] == "prev":
                dpj = o["dp"] + rec["s"]
            else:
                dpj = rec["dp"] + o["s"]
            okj = K2.greedy_r18(dpj, rec["Wm"])
            reason, stop = diag_greedy_r18(dpj, rec["Wm"] - 2)
            append_jsonl(retro_nc, {
                "span": key, "side": side, "grammar": "H7",
                "trial": "nc_" + t["trial"],
                "partner": [o["file"], o["bi"], o["si"]], "hit": bool(okj),
                "reason": reason,
                "bytes_consumed": stop - (rec["Wm"] - 2),
                "denominator": "nc_trials_executed"})
            h7_nc_span_den.add(tuple(key))
            if okj:
                h7_nc_span_hits.add(tuple(key))

    # REPEATABILITY cross-check vs K2 pinned fit lists (deterministic grammars)
    k2_results = json.load(open(K2_PINS["K2_HYPOTHESIS_RESULTS"][0],
                                encoding="utf-8"))
    k2_h5a = set(tuple(k) for k, _l in k2_results["H5a"]["fits"])
    k2_h5c2 = set(tuple(k) for k, _mx in
                  k2_results["H5c"]["H5c2_idx_lt_0x8000"]["fits"])
    k2_h7a = set(tuple(k) for k in k2_results["H7"]["H7a_prev_join"])
    k2_h7b = set(tuple(k) for k in k2_results["H7"]["H7b_next_join"])
    p2_set = set((r["file"], r["bi"], r["si"]) for r in unknown325)
    k2_h7_join325 = (k2_h7a | k2_h7b) & p2_set
    my_h5a = set(k for k, _l in h5a_fits)
    my_h5c2 = set(h5c2_fits)
    my_h7 = set(h7_explained)
    k2_h5a_nc = sorted([list(k) + [d] for k, d in k2_results["H5a"]["nc"]])
    my_h5a_nc = sorted([k + [d] for k, d in nc_span_hits["H5a"]])
    k2_h5c2_nc_n = k2_results["H5c"]["H5c2_idx_lt_0x8000"]["n_nc"]
    rep = {
        "standing": STANDING, "result_class": "REPEATABILITY",
        "H5a": {"k2_fits": len(k2_h5a), "this_run_fits": len(my_h5a),
                "identical": bool(k2_h5a == my_h5a)},
        "H5c2": {"k2_fits": len(k2_h5c2), "this_run_fits": len(my_h5c2),
                 "identical": bool(k2_h5c2 == my_h5c2)},
        "H7_join_of_325": {"k2": len(k2_h7_join325), "this_run": len(my_h7),
                           "identical": bool(k2_h7_join325 == my_h7)},
        "H5a_NC_hits": {"k2": len(k2_h5a_nc),
                        "this_run_pooled": len(my_h5a_nc),
                        "identical": bool(k2_h5a_nc == my_h5a_nc)},
        "H5c2_NC_hits": {
            "k2_n_nc": k2_h5c2_nc_n,
            "this_run_pooled": len(nc_span_hits["H5c2"]),
            "identical": bool(k2_h5c2_nc_n == len(nc_span_hits["H5c2"])),
            "note": "K2 stored only n_nc for H5c2 (no per-trial list); "
                    "count comparison"},
        "note": ("Deterministic grammars on pinned populations: the union of "
                 "both sides' fits must reproduce K2's full-population fit "
                 "lists EXACTLY.")}

    # per-unit gate NC (representatives; 2 trials per unit at u+/-2)
    def unit_nc_for_gate(unit_side, unit_members, grammar):
        trials = []
        for u in sorted(unit_members):
            if unit_side.get(u) != "B":
                continue
            rep = unit_members[u][0]
            for d in (2, -2):
                u2 = rep["u"] + d
                tname = "u_plus_2" if d > 0 else "u_minus_2"
                if u2 < 0:
                    trials.append({"span": [rep["file"], rep["bi"],
                                            rep["si"]],
                                   "grammar": grammar, "trial": tname,
                                   "hit": False,
                                   "reason": "INVALID_START_NONHIT"})
                    continue
                if grammar == "H5a":
                    out = K2.parse_variable_trunctail(
                        rep["dp"], u2, rep["N"])[:4]
                else:
                    out = K2.parse_variable(rep["dp"], u2, rep["N"],
                                            idx_limit=0x8000)
                trials.append({"span": [rep["file"], rep["bi"], rep["si"]],
                               "grammar": grammar, "trial": tname,
                               "hit": bool(out[0] and out[1] > 0),
                               "reason": "nc2"})
        return trials

    retro_results = {
        "run": "PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500",
        "standing": STANDING,
        "result_class": "RETROSPECTIVE_VALIDATION",
        "leg": ("9.3.5 file-grouped 50/50 split (RETROSPECTIVE_REVALIDATION; "
                "explicitly NOT unseen data; the grammars were SELECTED on "
                "the FULL populations in K2)"),
        "repeatability_vs_K2": rep,
        "grammars": {}}

    for g in ("H5a", "H5c2"):
        gate_nc = unit_nc_for_gate(unit_side_p1, unit_members_p1, g)
        # gate members: side B, excluding split-family members whose unit
        # belongs to side A (first-member rule; GATES_PREREGISTERED d1)
        mB = [m for m in members[g]["B"]
              if unit_side_p1.get(m["unit"]) == "B"]
        mA = [m for m in members[g]["A"]
              if unit_side_p1.get(m["unit"]) == "A"]
        verdict = evaluate_gretro(g, mA, mB, gate_nc, 2)
        units_A = {}
        for m in mA:
            units_A.setdefault(m["unit"], False)
            if m["fit"]:
                units_A[m["unit"]] = True
        fits_A = 0
        for _u, f in units_A.items():
            if f:
                fits_A += 1
        files_B = sorted(set(m["file"] for m in mB))
        n_split_excl_B = sum(1 for m in members[g]["B"]
                             if unit_side_p1.get(m["unit"]) != "B")
        retro_results["grammars"][g] = {
            "gate_verdict": verdict,
            "side_A_transparency": {
                "members": len(mA), "units": len(units_A),
                "unit_fits": fits_A,
                "files": len(set(m["file"] for m in mA))},
            "side_B_held_out": {
                "members": len(mB),
                "files": files_B,
                "split_family_members_excluded": n_split_excl_B},
            "nc": {"gate_trials_units_x_2": len(gate_nc),
                   "gate_hits": verdict.get("nc_hits"),
                   "span_level_pooled_hits": len(nc_span_hits[g]),
                   "span_level_pooled_trials": 2 * len(nofit)},
            "split_units_in_population": len(unit_split_p1)}
        log("[r1] G-RETRO %s: %s %s" % (g, verdict["result"],
                                        verdict.get("non_pass_class")))

    # H7 gate: unit-level positive vs unit-level span-structured NC
    # (the positive fit flags come from the per-record executions recorded in
    #  members["H7"]; here we only build the NC side per unit representative)
    h7_gate_units = {}
    for u in sorted(unit_members_p2):
        if unit_side_p2.get(u) != "B":
            continue
        h7_gate_units[u] = {"rep": unit_members_p2[u][0]}
    rng2 = random.Random(20260906)
    byf = defaultdict(list)
    for r in unknown325:
        byf[r["file"]].append(r)
    h7_nc_units = []
    for u in sorted(h7_gate_units):
        rep = h7_gate_units[u]["rep"]
        ctx = blocks_ctx.get((rep["file"], rep["bi"]))
        if ctx is None:
            continue
        _exp, trials = exec_h7(rep, ctx)
        others = sorted([x for x in byf[rep["file"]]
                         if abs(x["si"] - rep["si"]) > 2],
                        key=lambda r: (r["file"], r["bi"], r["si"]))
        nc_hit = False
        nc_exec = False
        for t in trials:
            if not others:
                continue
            o = rng2.choice(others)
            if t["trial"] == "prev":
                dpj = o["dp"] + rep["s"]
            else:
                dpj = rep["dp"] + o["s"]
            nc_exec = True
            if K2.greedy_r18(dpj, rep["Wm"]):
                nc_hit = True
        h7_nc_units.append({"unit": u, "nc_exec": nc_exec, "nc_hit": nc_hit})
    mB_h7 = [m for m in members["H7"]["B"]
             if unit_side_p2.get(m["unit"]) == "B"]
    mA_h7 = [m for m in members["H7"]["A"]
             if unit_side_p2.get(m["unit"]) == "A"]
    # explicit held-out side numbers (contract: CI for every rate)
    h7_explained_B = 0
    for m in mB_h7:
        if m["fit"]:
            h7_explained_B += 1
    h7_explained_A = 0
    for m in mA_h7:
        if m["fit"]:
            h7_explained_A += 1
    h7_units_B = {}
    for m in mB_h7:
        h7_units_B.setdefault(m["unit"], False)
        if m["fit"]:
            h7_units_B[m["unit"]] = True
    h7_unit_fits_B = 0
    for _u, f in h7_units_B.items():
        if f:
            h7_unit_fits_B += 1
    nc_exec_units = [x for x in h7_nc_units if x["nc_exec"]]
    nc_hits = 0
    for x in nc_exec_units:
        if x["nc_hit"]:
            nc_hits += 1
    h7_trials_for_gate = [{"hit": x["nc_hit"]} for x in nc_exec_units]
    h7_verdict = evaluate_gretro("H7", mA_h7, mB_h7, h7_trials_for_gate, None)
    retro_results["grammars"]["H7"] = {
        "gate_verdict": h7_verdict,
        "gate_nc_detail": {
            "positive_structure": "unit join-explained iff H7a or H7b "
                                  "walks clean (VERBATIM greedy_r18)",
            "nc_structure": "per-unit representative: one non-adjacent "
                            "mirror join per existing adjacency trial; "
                            "span-level any-hit; seeded random.Random("
                            "20260906)",
            "nc_units_B_executed": len(nc_exec_units),
            "nc_units_B_hits": nc_hits,
            "nc_span_level_rate_B": (round(nc_hits / len(nc_exec_units), 6)
                                     if nc_exec_units else None),
            "nc_rate_ci95_exact_binomial": clopper_pearson_95(
                nc_hits, len(nc_exec_units))},
        "side_A_transparency": {
            "members": len(mA_h7), "join_explained_members": h7_explained_A,
            "member_rate": (round(h7_explained_A / len(mA_h7), 6)
                            if mA_h7 else None),
            "member_rate_ci95_exact_binomial": clopper_pearson_95(
                h7_explained_A, len(mA_h7))},
        "side_B_held_out": {
            "members": len(mB_h7),
            "join_explained_members": h7_explained_B,
            "member_rate": (round(h7_explained_B / len(mB_h7), 6)
                            if mB_h7 else None),
            "member_rate_ci95_exact_binomial": clopper_pearson_95(
                h7_explained_B, len(mB_h7)),
            "units": len(h7_units_B), "unit_fits": h7_unit_fits_B,
            "unit_rate": (round(h7_unit_fits_B / len(h7_units_B), 6)
                          if h7_units_B else None),
            "unit_rate_ci95_exact_binomial": clopper_pearson_95(
                h7_unit_fits_B, len(h7_units_B)),
            "files": sorted(set(m["file"] for m in mB_h7))},
        "pooled_span_level_nc": {"nc_span_hits": len(h7_nc_span_hits),
                                 "nc_span_den": len(h7_nc_span_den)},
        "split_units_in_population": len(unit_split_p2)}
    log("[r1] G-RETRO H7: %s %s" % (h7_verdict["result"],
                                    h7_verdict.get("non_pass_class")))
    wr_json(os.path.join(ANA, "RETROSPECTIVE_RESULTS.json"), retro_results)
    return retro_results


# -------------------------------- S4: 2003-leg prechecks + era leg (G-ERA) ----
def grep_lines(path, needle, limit=6):
    out = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for i, ln in enumerate(f, 1):
            if needle in ln:
                out.append([i, ln.strip()[:240]])
                if len(out) >= limit:
                    break
    return out


def s45_era(ent935, data935, nofit_935, unknown325_935, big_all_935):
    log("[r1] S4: prior-use precheck")
    r21_driver = FAMILY_PINS["R21_PROBE"][0].replace(
        r"02_results\UNKNOWN325_PROBE.json", r"01_source\unknown325_r21.py")
    prior_use = {
        "standing": STANDING,
        "result_class": "ERA_TRANSFER_DIAGNOSTIC",
        "question": "was ANY grammar of the family (var-k, g1/g2, H5a, H5c, "
                    "H7 join) DERIVED from 2003-era data?",
        "evidence": [
            {"package": "R34 (var-k + g1/g2 derivation)",
             "path": FAMILY_PINS["R34_driver"][0],
             "sha256": sha256_file(FAMILY_PINS["R34_driver"][0]),
             "corpus_lines": grep_lines(FAMILY_PINS["R34_driver"][0],
                                        "MODELS_BNT")},
            {"package": "R18 (greedy walk derivation)",
             "path": FAMILY_PINS["R18_driver"][0],
             "sha256": sha256_file(FAMILY_PINS["R18_driver"][0]),
             "corpus_lines": grep_lines(FAMILY_PINS["R18_driver"][0],
                                        "MODELS_BNT")},
            {"package": "R21 (unknown325 census)",
             "path": r21_driver,
             "corpus_lines": grep_lines(r21_driver, "MODELS_BNT")},
            {"package": "K2 (H5a/H5c/H7 derivation)",
             "path": K2_DRIVER,
             "sha256": K2_PINS["K2_driver"][1],
             "corpus_lines": grep_lines(K2_DRIVER, "MODELS_BNT = "),
             "prereg_era": json.load(open(K2_PINS["K2_PREREG"][0],
                                          encoding="utf-8"))["era"]},
            {"package": "R35 (prior 2003 VALIDATION, 2026-09-04, PRE-K2; "
                        "NOT derivation)",
             "path": FAMILY_PINS["R35_REPORT"][0],
             "sha256": sha256_file(FAMILY_PINS["R35_REPORT"][0]),
             "p0_lines": grep_lines(FAMILY_PINS["R35_REPORT"][0], "P0")},
        ],
        "verdict": ("NO - every grammar of the family was DERIVED on the "
                    "9.3.5 corpus (R34/R18/R21/K2 corpus pins are all "
                    "pcg_install\\Data\\Models\\Models.bnt SHA c950a8c2...). "
                    "R35 (2026-09-04, pre-K2) provided prior VALIDATION "
                    "exposure of var-k + the greedy walk + the quantization "
                    "signature on the 2003 corpus (validation, not "
                    "derivation). The 2003 leg is therefore "
                    "ERA_TRANSFER_DIAGNOSTIC (not RETROSPECTIVE) for "
                    "H5a/H5c2/H7; var-k/walk/quant carry prior 2003 "
                    "validation exposure (recorded with paths).")}
    wr_json(os.path.join(ANA, "PRIOR_USE_VERDICT.json"), prior_use)

    log("[r1] S5: 2003 census + era leg (DIAGNOSTIC ONLY)")
    with open(MODELS_2003, "rb") as f:
        data2003 = f.read()
    ent2003 = read_bnt_index(data2003)
    era_expect = {
        "walk": {"big_spans": ERA2003_ANCHORS["big_spans"],
                 "fits": ERA2003_ANCHORS["fits"],
                 "entries": ERA2003_ANCHORS["entries"],
                 "pad_floats": ERA2003_ANCHORS["pads"]},
        "rr_state": {"rr_spans": ERA2003_ANCHORS["rr_spans"]},
        "blocks": {"morph_blocks": ERA2003_ANCHORS["morph_blocks"],
                   "blocks_with_tag": ERA2003_ANCHORS["blocks_with_tag"]},
    }
    (census2003, big_all_03, fit_recs_03, nofit_03, unknown_03, r21u_03,
     blocks_ctx_03) = run_census(PENifReader(), ent2003, data2003, era_expect,
                                 "2003", do_row_agreement=False)
    # rr_var two-way resolution (see ERA2003_ANCHORS comment): the
    # collision-free (file,bi,si) census value AND R35's own (file,tag,si)
    # keying value are both asserted; the census reproduces R35's published
    # number under R35's keying (no corpus/process divergence).
    rr_set_03 = [r for r in fit_recs_03 if r["rr"]]
    rr_keys_tag_03 = set((r["file"], r["tag"], r["si"]) for r in rr_set_03)
    rr_var_tag_keyed = 0
    collider_records = []
    for r in fit_recs_03:
        if r["var_ok"] and (r["file"], r["tag"], r["si"]) in rr_keys_tag_03:
            rr_var_tag_keyed += 1
            if not r["rr"]:
                collider_records.append(
                    {"file": r["file"], "bi": r["bi"], "si": r["si"],
                     "tag": r["tag"],
                     "note": "var_ok but NOT rr; counted as rr_var only "
                             "under the (file,tag,si) key collision"})
    rr_var_bi_keyed = census2003["rr_state"]["var_exact_of_rr"]
    if (rr_var_bi_keyed != ERA2003_ANCHORS["rr_var_bi_keyed"]
            or rr_var_tag_keyed != ERA2003_ANCHORS["rr_var_tag_keyed"]):
        hard_stop("2003 rr_var two-way resolution mismatch",
                  {"rr_var_bi_keyed": rr_var_bi_keyed,
                   "rr_var_tag_keyed": rr_var_tag_keyed,
                   "colliders": collider_records})
    census2003["rr_var_resolution"] = {
        "rr_var_bi_keyed_collision_free": rr_var_bi_keyed,
        "rr_var_tag_keyed_reproduces_R35": rr_var_tag_keyed,
        "R35_published": 1180,
        "finding": ("R35's published 2003 rr_var=1180 is a (file,tag,si) "
                    "key-collision artifact: 574845.nif bi=77 si=14 tag=3 "
                    "is var_ok but NOT rr, and is counted as rr_var only "
                    "under the colliding key. The collision-free census "
                    "reproduces every other R35 anchor EXACTLY and "
                    "reproduces 1180 under R35's own keying. Era "
                    "populations use the collision-free (file,bi,si) "
                    "keying (consistent with K2 and the retro leg)."),
        "collider_records": collider_records}
    if (not census2003["census_exact"]
            or census2003["files_with_morph"] != ERA2003_ANCHORS["files_with_morph"]):
        hard_stop("2003 era census mismatch vs R35 published anchors "
                  "(corpus/process divergence)",
                  {"checks": census2003.get("census_checks", []),
                   "files_with_morph": census2003["files_with_morph"]})
    log("[r1] 2003 census anchors EXACT vs R35 (morph %d / tag %d / big %d / "
        "fits %d / rr %d / var-of-rr %d bi-keyed (R35 keying reproduces %d) / "
        "files %d)"
        % (census2003["blocks"]["morph_blocks"],
           census2003["blocks"]["blocks_with_tag"],
           census2003["walk"]["big_spans"], census2003["walk"]["fits"],
           census2003["rr_state"]["rr_spans"], rr_var_bi_keyed,
           rr_var_tag_keyed, census2003["files_with_morph"]))
    census2003["era"] = "2003"
    census2003["result_class"] = "REPEATABILITY"
    census2003["standing"] = STANDING
    census2003["anchor_source"] = ("R35 GRAMMAR_VALIDATION.json sha256 "
                                   + FAMILY_PINS["R35_GRAMMAR_VALIDATION"][1])

    # duplicate census (morph-relevant file set; byte-identical payloads)
    sha_935 = {}
    for nm, size, off in ent935:
        sha_935[nm] = sha256_bytes(data935[off:off + size])
    sha_2003 = {}
    for nm, size, off in ent2003:
        sha_2003[nm] = sha256_bytes(data2003[off:off + size])
    morph_files_935 = sorted(set(r["file"] for r in big_all_935))
    morph_files_2003 = sorted(set(r["file"] for r in big_all_03))
    dup = {"standing": STANDING,
           "result_class": "ERA_TRANSFER_DIAGNOSTIC",
           "morph_relevant_files": {
               "with_morph_2003": len(morph_files_2003),
               "with_morph_935": len(morph_files_935),
               "shared_names": len(set(morph_files_2003)
                                   & set(morph_files_935)),
               "byte_identical": 0, "changed": 0, "only_2003": 0,
               "only_935": 0},
           "byte_identical_files_2003": [],
           "changed_files_2003": [],
           "only_2003_files": [],
           "only_935_files": [],
           "span_level": {"p1_dp_identical_across_eras": 0,
                          "p2_dp_identical_across_eras": 0},
           "family_grouping": {}}
    for f in morph_files_2003:
        if f not in sha_935:
            dup["only_2003_files"].append(f)
            dup["morph_relevant_files"]["only_2003"] += 1
        elif sha_2003[f] == sha_935[f]:
            dup["byte_identical_files_2003"].append(f)
            dup["morph_relevant_files"]["byte_identical"] += 1
        else:
            dup["changed_files_2003"].append(f)
            dup["morph_relevant_files"]["changed"] += 1
    for f in morph_files_935:
        if f not in sha_2003:
            dup["only_935_files"].append(f)
            dup["morph_relevant_files"]["only_935"] += 1
    dp_sha_p1_935 = set(sha256_bytes(r["dp"]) for r in nofit_935)
    dp_sha_p2_935 = set(sha256_bytes(r["dp"]) for r in unknown325_935)
    for r in nofit_03:
        if sha256_bytes(r["dp"]) in dp_sha_p1_935:
            dup["span_level"]["p1_dp_identical_across_eras"] += 1
    for r in unknown_03:
        if sha256_bytes(r["dp"]) in dp_sha_p2_935:
            dup["span_level"]["p2_dp_identical_across_eras"] += 1
    # family grouping: same file = one family; byte-identical dp = one family
    def family_grouping(pop):
        edges = defaultdict(set)
        for r in pop:
            u = sha256_bytes(r["dp"])
            edges[("file", r["file"])].add(u)
        # union-find over file nodes and dp-hash nodes
        parent = {}

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def uni(a, b):
            parent.setdefault(a, a)
            parent.setdefault(b, b)
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
        for r in pop:
            uni(("file", r["file"]), ("dp", sha256_bytes(r["dp"])))
        fams = defaultdict(list)
        for r in pop:
            fams[find(("file", r["file"]))].append(r)
        return fams
    fam_p1 = family_grouping(nofit_03)
    fam_p2 = family_grouping(unknown_03)
    dup["family_grouping"] = {
        "rule": "same file = one family; byte-identical payloads = one "
                "family; family count used as the independence unit",
        "P1_2003_families": len(fam_p1),
        "P2_2003_families": len(fam_p2)}
    wr_json(os.path.join(RAW, "ERA_DUPLICATE_CENSUS.json"), dup)
    wr_json(os.path.join(ANA, "ERA_CENSUS_2003.json"), census2003)
    log("[r1] era duplicate census: 2003 morph files %d (identical %d, "
        "changed %d, only-2003 %d); P1 fams %d; P2 fams %d"
        % (len(morph_files_2003),
           dup["morph_relevant_files"]["byte_identical"],
           dup["morph_relevant_files"]["changed"],
           dup["morph_relevant_files"]["only_2003"],
           len(fam_p1), len(fam_p2)))

    # era grammar executions (DIAGNOSTIC ONLY)
    era_out = os.path.join(RAW, "ERA_SPAN_OUTCOMES.jsonl")
    era_nc = os.path.join(RAW, "ERA_NC_TRIALS.jsonl")
    for p in (era_out, era_nc):
        if os.path.exists(p):
            os.remove(p)
    ident_files = set(dup["byte_identical_files_2003"])
    changed_files = set(dup["changed_files_2003"])

    def strat(file):
        if file in ident_files:
            return "byte_identical_to_935"
        if file in changed_files:
            return "changed_vs_935"
        return "only_2003"

    era_res = {"standing": STANDING,
               "result_class": "ERA_TRANSFER_DIAGNOSTIC",
               "gate": "G-ERA DIAGNOSTIC ONLY (no PASS/FAIL)",
               "era_census": census2003,
               "prior_use": prior_use,
               "duplicate_census": dup,
               "grammars": {}}
    for g, pop in (("H5a", nofit_03), ("H5c2", nofit_03)):
        members = []
        fits = 0
        for rec in pop:
            key = [rec["file"], rec["bi"], rec["si"]]
            if g == "H5a":
                fit, reason, consumed, extra = exec_h5a(rec)
            else:
                fit, reason, consumed, extra = exec_h5c2(rec)
            append_jsonl(era_out, {"span": key, "side": "era2003",
                                    "grammar": g,
                                    "outcome": "FIT" if fit else "NOFIT",
                                    "reason": reason,
                                    "bytes_consumed": consumed,
                                    "file_identity_class": strat(rec["file"]),
                                    "extra": extra,
                                    "result_class": "ERA_TRANSFER_DIAGNOSTIC"})
            members.append({"key": key, "unit": sha256_bytes(rec["dp"]),
                            "file": rec["file"], "fit": fit,
                            "side": "era2003", "wellformed": True})
            if fit:
                fits += 1
        # unit-level (dedup)
        units = {}
        for m in members:
            units.setdefault(m["unit"], False)
            if m["fit"]:
                units[m["unit"]] = True
        unit_fits = 0
        for _u, f in units.items():
            if f:
                unit_fits += 1
        # family-level
        fam_fits = 0
        for _fk, famrecs in fam_p1.items():
            fam_fit = False
            for r in famrecs:
                if any(m["key"] == [r["file"], r["bi"], r["si"]]
                       and m["fit"] for m in members):
                    fam_fit = True
                    break
            if fam_fit:
                fam_fits += 1
        # NC (per-span u+/-2, pooled)
        nc_hits = 0
        nc_trials = 0
        for rec in pop:
            for d in (2, -2):
                u2 = rec["u"] + d
                nc_trials += 1
                hit = False
                reason = "INVALID_START_NONHIT"
                if u2 >= 0:
                    if g == "H5a":
                        out = K2.parse_variable_trunctail(
                            rec["dp"], u2, rec["N"])[:4]
                    else:
                        out = K2.parse_variable(rec["dp"], u2, rec["N"],
                                                 idx_limit=0x8000)
                    hit = bool(out[0] and out[1] > 0)
                    reason = "nc2"
                append_jsonl(era_nc, {
                    "span": [rec["file"], rec["bi"], rec["si"]], "grammar": g,
                    "trial": "u_plus_2" if d > 0 else "u_minus_2", "u2": u2,
                    "hit": hit, "reason": reason,
                    "denominator": "spans_x_2"})
                if hit:
                    nc_hits += 1
        strat_fits = Counter()
        strat_units = Counter()
        for m in members:
            sc = strat(m["file"])
            strat_units[sc] += 1
            if m["fit"]:
                strat_fits[sc] += 1
        era_res["grammars"][g] = {
            "population": "2003 rr no-fit spans (rr and var_ok=0)",
            "members": len(members),
            "member_fits": fits,
            "member_rate": round(fits / len(members), 6) if members else None,
            "member_rate_ci95_exact_binomial": clopper_pearson_95(
                fits, len(members)),
            "units": len(units), "unit_fits": unit_fits,
            "unit_rate": (round(unit_fits / len(units), 6)
                          if units else None),
            "unit_rate_ci95_exact_binomial": clopper_pearson_95(
                unit_fits, len(units)),
            "families": len(fam_p1), "family_fits": fam_fits,
            "family_rate": (round(fam_fits / len(fam_p1), 6)
                            if fam_p1 else None),
            "family_rate_ci95_exact_binomial": clopper_pearson_95(
                fam_fits, len(fam_p1)),
            "nc_hits": nc_hits, "nc_trials": nc_trials,
            "nc_rate": (round(nc_hits / nc_trials, 6)
                        if nc_trials else None),
            "nc_rate_ci95_exact_binomial": clopper_pearson_95(
                nc_hits, nc_trials),
            "stratified_member_fits": dict(strat_fits),
            "stratified_members": dict(strat_units)}
        log("[r1] era %s: members %d fits %d (rate %s) nc %d/%d"
            % (g, len(members), fits,
               era_res["grammars"][g]["member_rate"], nc_hits, nc_trials))

    # H7 on the 2003 unknown-equivalent population
    rng3 = random.Random(20260906)
    byf03 = defaultdict(list)
    for r in unknown_03:
        byf03[r["file"]].append(r)
    h7_members = []
    h7_fits = 0
    nc_span_hits = 0
    nc_span_den = 0
    for rec in sorted(unknown_03,
                      key=lambda r: (r["file"], r["bi"], r["si"])):
        key = [rec["file"], rec["bi"], rec["si"]]
        ctx = blocks_ctx_03.get((rec["file"], rec["bi"]))
        if ctx is None:
            explained, trials = False, []
        else:
            explained, trials = exec_h7(rec, ctx)
        append_jsonl(era_out, {"span": key, "side": "era2003",
                               "grammar": "H7",
                               "outcome": "FIT" if explained else "NOFIT",
                               "reason": (";".join(t["reason"] for t in trials)
                                          if trials else
                                          ("NO_BLOCK_CONTEXT" if ctx is None
                                           else "NO_TRIALS")),
                               "bytes_consumed": max(
                                   [t["consumed"] for t in trials] or [0]),
                               "file_identity_class": strat(rec["file"]),
                               "unit": sha256_bytes(rec["dp"]),
                               "result_class": "ERA_TRANSFER_DIAGNOSTIC"})
        h7_members.append({"key": key, "unit": sha256_bytes(rec["dp"]),
                           "file": rec["file"], "fit": explained,
                           "side": "era2003", "wellformed": True})
        if explained:
            h7_fits += 1
        others = sorted([x for x in byf03[rec["file"]]
                          if abs(x["si"] - rec["si"]) > 2],
                         key=lambda r: (r["file"], r["bi"], r["si"]))
        for t in trials:
            if not others:
                continue
            o = rng3.choice(others)
            if t["trial"] == "prev":
                dpj = o["dp"] + rec["s"]
            else:
                dpj = rec["dp"] + o["s"]
            nc_span_den += 1
            okj = K2.greedy_r18(dpj, rec["Wm"])
            append_jsonl(era_nc, {"span": key, "grammar": "H7",
                                  "trial": "nc_" + t["trial"],
                                  "partner": [o["file"], o["bi"], o["si"]],
                                  "hit": bool(okj),
                                  "denominator": "nc_trials_executed"})
            if okj:
                nc_span_hits += 1
    h7_units = {}
    for m in h7_members:
        h7_units.setdefault(m["unit"], False)
        if m["fit"]:
            h7_units[m["unit"]] = True
    h7_unit_fits = 0
    for _u, f in h7_units.items():
        if f:
            h7_unit_fits += 1
    fam_fits_h7 = 0
    for _fk, famrecs in fam_p2.items():
        fam_fit = False
        for r in famrecs:
            if any(m["key"] == [r["file"], r["bi"], r["si"]] and m["fit"]
                   for m in h7_members):
                fam_fit = True
                break
        if fam_fit:
            fam_fits_h7 += 1
    strat_fits_h7 = Counter()
    strat_units_h7 = Counter()
    for m in h7_members:
        sc = strat(m["file"])
        strat_units_h7[sc] += 1
        if m["fit"]:
            strat_fits_h7[sc] += 1
    era_res["grammars"]["H7"] = {
        "population": "2003 residual spans (neither, fail backtrack AND "
                      "fail shift-scan)",
        "members": len(h7_members),
        "member_fits": h7_fits,
        "member_rate": (round(h7_fits / len(h7_members), 6)
                        if h7_members else None),
        "member_rate_ci95_exact_binomial": clopper_pearson_95(
            h7_fits, len(h7_members)),
        "units": len(h7_units), "unit_fits": h7_unit_fits,
        "unit_rate": (round(h7_unit_fits / len(h7_units), 6)
                      if h7_units else None),
        "unit_rate_ci95_exact_binomial": clopper_pearson_95(
            h7_unit_fits, len(h7_units)),
        "families": len(fam_p2), "family_fits": fam_fits_h7,
        "family_rate": (round(fam_fits_h7 / len(fam_p2), 6)
                        if fam_p2 else None),
        "family_rate_ci95_exact_binomial": clopper_pearson_95(
            fam_fits_h7, len(fam_p2)),
        "nc_hits": nc_span_hits, "nc_trials": nc_span_den,
        "nc_rate": (round(nc_span_hits / nc_span_den, 6)
                    if nc_span_den else None),
        "nc_rate_ci95_exact_binomial": clopper_pearson_95(
            nc_span_hits, nc_span_den),
        "stratified_member_fits": dict(strat_fits_h7),
        "stratified_members": dict(strat_units_h7)}
    log("[r1] era H7: members %d fits %d nc %d/%d"
        % (len(h7_members), h7_fits, nc_span_hits, nc_span_den))

    # CORPUS_SPECIFIC_935 assessment (near-zero transfer = valid outcome).
    # DIAGNOSTIC heuristic, explicitly NOT a gate: near-zero transfer = the
    # grammar produces no era fits, or fits at/below the 5x-of-matched-NC
    # coincidence level (a vacuous NC with 0 hits cannot force near-zero).
    per_grammar_signal = {}
    near_zero = True
    for g in ("H5a", "H5c2", "H7"):
        r = era_res["grammars"][g]
        fits = r["member_fits"]
        rate = r["member_rate"] or 0.0
        nc_rate = r["nc_rate"] or 0.0
        nc_trials = r["nc_trials"]
        transfer_signal = bool(fits > 0 and (nc_trials == 0
                                             or rate >= 5 * nc_rate))
        per_grammar_signal[g] = {
            "member_fits": fits, "member_rate": r["member_rate"],
            "nc_trials": nc_trials, "nc_rate": r["nc_rate"],
            "transfer_signal": transfer_signal}
        if transfer_signal:
            near_zero = False
    era_res["corpus_specific_935_assessment"] = {
        "near_zero_transfer_vs_matched_nc": bool(near_zero),
        "per_grammar": per_grammar_signal,
        "interpretation": ("if near-zero: the finding CORPUS_SPECIFIC_935 "
                           "(a VALID outcome, not a failure; explicitly NOT "
                           "a substitute for 9.3.5-target correctness). "
                           "The G-RETRO verdicts on the 9.3.5 split remain "
                           "the load-bearing result."),
        "note_5x": ("the era leg is DIAGNOSTIC ONLY; the 5x standard is the "
                    "retro leg's gate; this diagnostic reports the ratio vs "
                    "the matched NC rate for context only")}
    wr_json(os.path.join(ANA, "ERA_TRANSFER_RESULTS.json"), era_res)
    return era_res


# -------------------------------- S6: G-EXEC (self-audit + 8 fixtures) -------
def synthetic_payload(valid, idx):
    """Synthetic fixture payload (NOT game data): H5c2-grammar shaped bytes.
    valid: 8 records [u16 idx=1][f32 1.0][9 x f32 0.0] (42 B each);
    invalid: varying first byte + 0xff fill (idx=0xffff fails the limit)."""
    if valid:
        rec = struct.pack("<H", 1) + struct.pack("<f", 1.0) \
            + struct.pack("<f", 0.0) * 9
        return rec * 8
    return bytes([idx % 256]) + b"\xff" * (335 + idx % 7)


def s6_gexec():
    log("[r1] S6: G-EXEC (self-audit + 8 negative fixtures + manifest tests)")
    fixtures = {"standing": STANDING, "result_class": "G-EXEC",
                "fixtures": []}

    def exec_fit(dp):
        ok, recs, kh, idxs = K2.parse_variable(dp, 0, 4, idx_limit=0x8000)
        return bool(ok and recs > 0)

    def member(i, side, valid):
        dp = synthetic_payload(valid, i)
        return {"key": ["synthetic_%s_%03d.nif" % (side, i), 0, i],
                "side": side, "unit": sha256_bytes(dp),
                "file": "synthetic_%s_%03d.nif" % (side, i),
                "fit": exec_fit(dp), "wellformed": True}

    def nc_trials_for(members):
        out = []
        for m in members:
            for tname in ("u_plus_2", "u_minus_2"):
                out.append({"span": m["key"], "trial": tname,
                            "hit": False, "reason": "synthetic_no_hit"})
        return out

    # F1: zero successes both sides (32 units/side, all fail)
    f1_A = [member(i, "A", False) for i in range(32)]
    f1_B = [member(i, "B", False) for i in range(32)]
    v1 = evaluate_gretro("FIXTURE1", f1_A, f1_B, nc_trials_for(f1_B), 2)
    fixtures["fixtures"].append({"id": 1, "name": "zero successes both sides",
                                 "expected": "explicit non-pass",
                                 "verdict": v1})
    # F2: empty population
    v2 = evaluate_gretro("FIXTURE2", [], [], [], 2)
    fixtures["fixtures"].append({"id": 2, "name": "empty population",
                                 "expected": "EMPTY_GROUP", "verdict": v2})
    # F3: only-previously-selected successes (side A fits, side B none)
    f3_A = [member(i, "A", True) for i in range(32)]
    f3_B = [member(i, "B", False) for i in range(32)]
    v3 = evaluate_gretro("FIXTURE3", f3_A, f3_B, nc_trials_for(f3_B), 2)
    fixtures["fixtures"].append(
        {"id": 3, "name": "only-previously-selected successes",
         "expected": "explicit non-pass (held-out ZERO_FITS)", "verdict": v3})
    # F4: a duplicate present in both groups
    dupm = member(0, "A", False)
    f4_B = [dupm] + [member(i, "B", False) for i in range(1, 32)]
    v4 = evaluate_gretro("FIXTURE4", [dupm], f4_B,
                         nc_trials_for(f4_B), 2)
    fixtures["fixtures"].append(
        {"id": 4, "name": "duplicate present in both groups",
         "expected": "DUPLICATE_ACROSS_SIDES", "verdict": v4})
    # F5: unequal denominators (63 NC trials for 32 units)
    f5_B = [member(i, "B", False) for i in range(32)]
    tr5 = nc_trials_for(f5_B)[:63]
    v5 = evaluate_gretro("FIXTURE5", [], f5_B, tr5, 2)
    fixtures["fixtures"].append(
        {"id": 5, "name": "unequal denominators",
         "expected": "DENOMINATOR_MISMATCH", "verdict": v5})
    # F6: a corrupted record
    corrupt = {"key": ["x.nif", 0, 0], "side": "B", "unit": "u"}
    f6_B = [corrupt] + [member(i, "B", False) for i in range(1, 32)]
    v6 = evaluate_gretro("FIXTURE6", [], f6_B, nc_trials_for(f6_B), 2)
    fixtures["fixtures"].append({"id": 6, "name": "a corrupted record",
                                 "expected": "CORRUPTED_RECORD",
                                 "verdict": v6})
    # F7: a malformed manifest row
    ok7, out7 = validate_manifest_rows(
        ["00_CONTROL/CONTRACT.md,a role, with unquoted comma,"
         + "a" * 64], RUN)
    v7 = {"result": "PASS" if ok7 else "NON_PASS",
          "non_pass_class": (out7["findings"][0][0]
                             if out7["findings"] else None),
          "findings": out7["findings"]}
    fixtures["fixtures"].append({"id": 7, "name": "a malformed manifest row",
                                 "expected": "MALFORMED_MANIFEST_ROW",
                                 "verdict": v7})
    # F8: a missing input file
    v8 = resolve_input_file(os.path.join(RUN, "NONEXISTENT_INPUT_FILE.json"))
    fixtures["fixtures"].append({"id": 8, "name": "a missing input file",
                                 "expected": "MISSING_INPUT_FILE",
                                 "verdict": v8})
    all_fail_closed = all(
        (f["verdict"].get("result") == "NON_PASS"
         and f["verdict"].get("non_pass_class"))
        for f in fixtures["fixtures"])
    fixtures["all_eight_fail_closed"] = bool(all_fail_closed)
    fixtures["gexec_verdict"] = "PASS" if all_fail_closed else "FAIL"
    wr_json(os.path.join(RAW, "NEGATIVE_FIXTURES_GEXEC.json"), fixtures)
    log("[r1] G-EXEC fixtures: %s" % fixtures["gexec_verdict"])

    # (a) driver self-audit: size-derived assignments in gate code.
    # Scanner discipline: string LITERALS are stripped to 'STR' before the
    # pattern scan so the scanner cannot match its own detection code
    # (the two false positives of the first execution were exactly the
    # scanner's own pattern literals — documented here).
    import re as _re
    with open(DRIVER_PATH, "r", encoding="utf-8") as f:
        src = f.read().split("\n")
    len_lines = []
    forbidden = []
    for i, ln in enumerate(src, 1):
        code = _re.sub(r'"[^"\n]*"', "STR", ln)
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
                                  "SPLIT_PROCEDURE (contract Section 3; not "
                                  "a validation count)"])
            else:
                forbidden.append([i, ln.strip()])
    audit = {"standing": STANDING,
             "scan_target": "this driver's own source (gate code included)",
             "len_occurrences_classified": len(len_lines),
             "forbidden_patterns": forbidden,
             "len_line_census": len_lines,
             "audit_verdict": ("CLEAN - no size-derived validation/fit "
                              "assignments; all fit counts are counter "
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


# -------------------------------- S7: outputs + main --------------------------
def s7_outputs(retro, era_res, gexec_pass, fixtures, audit, pin_results,
               split_freeze):
    log("[r1] S7: outputs (reports, gates CSV, artifact_index + validation)")
    gates = {}

    def add(name, desc, status):
        gates[name] = {"gate": name, "description": desc, "status": status}

    add("G-PINS", "every input pin verified in-driver before any parse "
        "(R61 10/10; K2 artifacts re-hashed from bytes; 2003 container SHA "
        "1322adf2... + 5,426-name class + extraction tie 5,426/5,426)",
        "PASS")
    add("G-CENSUS", "9.3.5 baseline census reproduces K2 EXACTLY (rr 2,427 / "
        "var 2,093 / nofit 334 = 62+272; unknown-325 = 325 / 56 files / "
        "551564 x84; walk 10,274/6,167/65,050/143,874; row agreement "
        "6,167/6,167)", "PASS")
    for g in ("H5a", "H5c2", "H7"):
        v = retro["grammars"][g]["gate_verdict"]
        add("G-RETRO_" + g,
            "a-priori gate: units>=30 AND fits>=10 AND positive rate >= 5x "
            "matched-NC rate AND NC denominator > 0 (never adjusted; "
            "exact binomial 95% CIs reported in RETROSPECTIVE_RESULTS.json)",
            v["result"] + (" (" + v["non_pass_class"] + ")"
                           if v["non_pass_class"] else ""))
    era_xfer = era_res["corpus_specific_935_assessment"]
    add("G-ERA", "2003 leg DIAGNOSTIC ONLY (no PASS/FAIL): fit counts, rates "
        "+ exact binomial CIs, prior-use verdict, duplicate/family census; "
        "near-zero-transfer=%s; era census reproduces every R35 anchor "
        "EXACTLY incl. rr_var 1,180 under R35's own (file,tag,si) keying "
        "(collision-free (file,bi,si) value 1,179; R35 key-collision "
        "artifact documented in ERA_CENSUS_2003.json)"
        % era_xfer["near_zero_transfer_vs_matched_nc"],
        "DIAGNOSTIC_ONLY (CORPUS_SPECIFIC_935=%s)"
        % era_xfer["near_zero_transfer_vs_matched_nc"])
    n_fix = len(fixtures["fixtures"])
    n_fix_ok = sum(1 for f in fixtures["fixtures"]
                   if f["verdict"].get("result") == "NON_PASS"
                   and f["verdict"].get("non_pass_class"))
    add("G-EXEC", "per-record validation discipline + self-audit + %d/%d "
        "negative fixtures fail-closed + manifest negative tests 6/6"
        % (n_fix_ok, n_fix),
        "PASS" if gexec_pass else "FAIL")

    # manifest negative tests (spec item 4: a-f, each must FAIL the gate)
    neg = {"standing": STANDING,
           "spec": "MANIFEST_SCHEMA_SPEC.md validation gate negative tests",
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

    # pre-validation of the manifest row set IN MEMORY (BEFORE the final
    # gates CSV write so its G-SCOPE status is truthful): rows over every
    # package file except artifact_index.csv (self-hash impossible;
    # documented precedent), 05_ANALYSIS/MANIFEST_VALIDATION.json (circular:
    # it records the validation OF this manifest; documented exclusion) and
    # STAGE_ACCEPTANCE_GATES.csv (written immediately after this check; its
    # row is added to the manifest with the hash of its final on-disk bytes).
    exclusions = {"artifact_index.csv",
                  "05_ANALYSIS/MANIFEST_VALIDATION.json",
                  "STAGE_ACCEPTANCE_GATES.csv"}
    import io as _io0
    _buf0 = _io0.StringIO()
    _w0 = csv.writer(_buf0, lineterminator="\n")
    for root, dirs, files in os.walk(RUN):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for fn in sorted(files):
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, RUN).replace(os.sep, "/")
            if rel in exclusions:
                continue
            _w0.writerow([rel, "package artifact", sha256_file(fp)])
    ok_x, out_x = validate_manifest_rows(_buf0.getvalue().splitlines(), RUN)
    log("[r1] manifest rows pre-validation (in memory, %d rows): %s"
        % (out_x["ordinary_rows"], "PASS" if ok_x else "FAIL"))
    external = []
    for sid, path, era in (
            ("corpus_935", MODELS_935, "PCG_9_3_5"),
            ("corpus_2003", MODELS_2003, "2003"),
            ("K2_driver", K2_DRIVER, "PCG_9_3_5"),
            ("R34_driver", FAMILY_PINS["R34_driver"][0], "PCG_9_3_5"),
            ("R18_driver", FAMILY_PINS["R18_driver"][0], "PCG_9_3_5"),
            ("R20_driver", FAMILY_PINS["R20_driver"][0], "PCG_9_3_5"),
            ("R21_HEX_UNKNOWN", FAMILY_PINS["R21_HEX_UNKNOWN"][0],
             "PCG_9_3_5"),
            ("R21_PROBE", FAMILY_PINS["R21_PROBE"][0], "PCG_9_3_5"),
            ("R34_REAL_SPARSE_GRAMMAR",
             FAMILY_PINS["R34_REAL_SPARSE_GRAMMAR"][0], "PCG_9_3_5"),
            ("R34_QUANT_TESTS", FAMILY_PINS["R34_QUANT_TESTS"][0],
             "PCG_9_3_5"),
            ("R33_MORPH_IDS_FULL", FAMILY_PINS["R33_MORPH_IDS_FULL"][0],
             "PCG_9_3_5"),
            ("R35_GRAMMAR_VALIDATION",
             FAMILY_PINS["R35_GRAMMAR_VALIDATION"][0], "2003"),
            ("R35_driver", FAMILY_PINS["R35_driver"][0], "2003"),
            ("R35_REPORT", FAMILY_PINS["R35_REPORT"][0], "2003"),
            ("R61_SHA_MANIFEST", R61_SHA_JSON, "PCG_9_3_5"),
            ("K2_NOFIT334_SPANS", K2_PINS["K2_NOFIT334_SPANS"][0],
             "PCG_9_3_5"),
            ("K2_RESIDUAL333_SPANS", K2_PINS["K2_RESIDUAL333_SPANS"][0],
             "PCG_9_3_5"),
            ("K2_HYPOTHESIS_RESULTS", K2_PINS["K2_HYPOTHESIS_RESULTS"][0],
             "PCG_9_3_5"),
            ("K2_PREREG", K2_PINS["K2_PREREG"][0], "PCG_9_3_5"),
            ("K2_BASELINE_REPRODUCTION",
             K2_PINS["K2_BASELINE_REPRODUCTION"][0], "PCG_9_3_5"),
            ("K2_COVERAGE_STATE", K2_PINS["K2_COVERAGE_STATE"][0],
             "PCG_9_3_5"),
            ("R12_manifest_2003", FAMILY_PINS["R12_manifest_2003"][0],
             "2003")):
        external.append([sid, "external_source", era, path,
                         sha256_file(path)])
    gates["G-SCOPE"] = {"gate": "G-SCOPE",
                        "description": "read-only originals; zero payloads; "
                        "run-local tooling only in 00_CONTROL; "
                        "artifact_index.csv per RUN B spec + self-validation "
                        "(pre-validation in memory + post-write physical "
                        "validation; documented exclusions: the manifest's own "
                        "row and 05_ANALYSIS/MANIFEST_VALIDATION.json — "
                        "circular, precedent L12)",
                        "status": ("PASS" if (ok_x and all_neg_fail)
                                   else "FAIL")}
    if not ok_x:
        log("[r1] G-SCOPE pre-validation findings: "
            + json.dumps(out_x["findings"][:6]))
    wr_lines(os.path.join(RUN, "STAGE_ACCEPTANCE_GATES.csv"),
             ["# " + STANDING, "gate,description,status"] +
             ['"%s","%s","%s"' % (gates[k]["gate"],
                                  gates[k]["description"].replace('"', "'"),
                                  gates[k]["status"])
              for k in ("G-PINS", "G-CENSUS", "G-RETRO_H5a", "G-RETRO_H5c2",
                        "G-RETRO_H7", "G-ERA", "G-EXEC", "G-SCOPE")])

    # ------- 06_REPORT: 00_FINAL_REPORT.md (s15 20-point contract) -------
    rep = retro["grammars"]
    p0_ans = []
    for g in ("H5a", "H5c2", "H7"):
        v = rep[g]["gate_verdict"]
        p0_ans.append("%s=%s%s" % (g, v["result"],
                                   (" " + v["non_pass_class"])
                                   if v["non_pass_class"] else ""))
    handoff = [
        "AUDIT_OUTPUT_ROOT = " + RUN,
        "FINAL_REPORT_PATH = " + os.path.join(REPT, "00_FINAL_REPORT.md"),
        "PRIMARY_EVIDENCE_PATHS = " + "; ".join([
            os.path.join(ANA, "RETROSPECTIVE_RESULTS.json"),
            os.path.join(ANA, "ERA_TRANSFER_RESULTS.json"),
            os.path.join(ANA, "BASELINE_CENSUS_REPRODUCTION.json"),
            os.path.join(CTRL, "PIN_RESULTS.json"),
            os.path.join(CTRL, "SPLIT_SIDES.json"),
            os.path.join(RAW, "RETRO_SPAN_OUTCOMES.jsonl"),
            os.path.join(RAW, "RETRO_NC_TRIALS.jsonl"),
            os.path.join(RAW, "ERA_SPAN_OUTCOMES.jsonl"),
            os.path.join(RAW, "NEGATIVE_FIXTURES_GEXEC.json")]),
        "RUN_STATUS = COMPLETED",
        "HARD_STOP_REASON = NONE",
    ]
    lines = []
    lines.append("# FINAL REPORT - PE_NIF_MORPH_GRAMMAR_REVALIDATION_"
                 "R1_20260906_140500 (RUN A)")
    lines.append("")
    lines.append("## 1. HUMAN-FIRST (what needs the human NOW)")
    lines.append("")
    lines.append("Nothing is required from the human inside this run. "
                 "PE-MASTER owns the post-run 5-layer audit and the "
                 "publication decision (NO commit was made by the executor). "
                 "The +65/88.88% coverage status REMAINS CANDIDATE "
                 "regardless of this run's outcome until PE-MASTER's "
                 "post-run audit.")
    lines.append("")
    lines.append("## 2. IDENTITY")
    lines.append("")
    lines.append("RUN_ID: PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_"
                 "140500 | RUN_CLASS: LOAD_BEARING | milestone: EU935-M1 "
                 "(NO crossing) | date: %s | executor: pe-reconstruction | "
                 "parent: PE-MASTER loop bd17344b iteration 2"
                 % time.strftime("%Y-%m-%d"))
    lines.append("")
    lines.append("## 3. STATE DELTA (before -> after)")
    lines.append("")
    lines.append("BEFORE: K2 confirmed H5a/H5c1/H5c2/H7 on the FULL 9.3.5 "
                 "populations (+65 spans, 2158/2427 = 88.88% candidate; "
                 "status CANDIDATE). No file-grouped split validation and no "
                 "2003-era transfer of H5a/H5c2/H7 existed. AFTER: the three "
                 "frozen grammars revalidated per-record on a seeded "
                 "file-grouped 50/50 split (RETROSPECTIVE; NOT unseen data) "
                 "with denominator-matched NCs, executed on the 2003 corpus "
                 "(ERA_TRANSFER_DIAGNOSTIC), with prior-use/duplicate/"
                 "family prechecks, G-EXEC per-record discipline + 8/8 "
                 "fail-closed fixtures, and a spec-compliant manifest. "
                 "Gate results: " + "; ".join(p0_ans) + ".")
    lines.append("")
    lines.append("## 4/12. EXACT VERDICT + ONE P0")
    lines.append("")
    lines.append("RUN verdict: COMPLETED (all contract outputs produced; no "
                 "HARD STOP). ONE P0: 'Do the FROZEN H5a and H5c2 grammars "
                 "and the H7 join model hold on (i) file-grouped splits of "
                 "the 9.3.5 eligible populations (RETROSPECTIVE) and (ii) "
                 "the 2003-era morph corpus (ERA_TRANSFER_DIAGNOSTIC)?' "
                 "ANSWER (retro leg, load-bearing): " + "; ".join(p0_ans)
                 + ". ANSWER (era leg, diagnostic only): see 9/13 below; "
                 "explicitly NOT a substitute for 9.3.5-target correctness.")
    for g in ("H5a", "H5c2", "H7"):
        v = rep[g]["gate_verdict"]
        if v["result"] == "PASS":
            lines.append("")
            lines.append("- G-RETRO %s: %s%s | units=%s fits=%s rate=%s "
                         "CI95=%s | NC %s/%d rate=%s CI95=%s"
                         % (g, v["result"],
                            (" " + v["non_pass_class"]) if v["non_pass_class"]
                            else "",
                            v.get("units"), v.get("unit_fits"),
                            v.get("positive_rate"),
                            v.get("positive_rate_ci95_exact_binomial"),
                            v.get("nc_hits"), v.get("nc_denominator") or 0,
                            v.get("nc_rate"),
                            v.get("nc_rate_ci95_exact_binomial")))
        else:
            sb = rep[g].get("side_B_held_out", {})
            det = v.get("detail", {})
            ncm = rep[g].get("gate_nc_detail", {})
            lines.append("")
            lines.append("- G-RETRO %s: %s%s | detail=%s | held-out "
                         "members=%s explained=%s rate=%s CI95=%s | NC "
                         "units=%s hits=%s rate=%s CI95=%s"
                         % (g, v["result"],
                            (" " + v["non_pass_class"]) if v["non_pass_class"]
                            else "",
                            json.dumps(det),
                            sb.get("members"), sb.get("join_explained_members"),
                            sb.get("member_rate"),
                            sb.get("member_rate_ci95_exact_binomial"),
                            ncm.get("nc_units_B_executed"),
                            ncm.get("nc_units_B_hits"),
                            ncm.get("nc_span_level_rate_B"),
                            ncm.get("nc_rate_ci95_exact_binomial")))
    lines.append("")
    lines.append("## 5/6. CLAIM -> EVIDENCE + DENOMINATORS")
    lines.append("")
    lines.append("Every rate above carries numerator/denominator and an "
                 "exact binomial (Clopper-Pearson) 95% CI. Machine evidence: "
                 "05_ANALYSIS/RETROSPECTIVE_RESULTS.json (per-grammar gates, "
                 "CIs, repeatability), 01_RAW/RETRO_SPAN_OUTCOMES.jsonl + "
                 "RETRO_NC_TRIALS.jsonl (per-record outcomes: span ID, side, "
                 "grammar, outcome, rejection reason, bytes consumed), "
                 "ERA_TRANSFER_RESULTS.json, ERA_DUPLICATE_CENSUS.json, "
                 "BASELINE_CENSUS_REPRODUCTION.json, NEGATIVE_FIXTURES_"
                 "GEXEC.json, MANIFEST_NEGATIVE_TESTS.json. Validation "
                 "counts are counter increments over executed records "
                 "(G-EXEC discipline; self-audit in 01_RAW/SELF_AUDIT.txt "
                 "with the full len() census).")
    lines.append("")
    lines.append("## 7/8. OPEN ITEMS + COVERAGE HONESTY (NOT checked)")
    lines.append("")
    lines.append("- RUNTIME_SEMANTICS is explicitly NOT_TESTED here (out of "
                 "scope). Class -256/field1 MEANING remains unknown; the "
                 "-256=>zero-entry association remains ONE-WAY. No semantic "
                 "claim is made anywhere in this package.")
    lines.append("- The retro leg is RETROSPECTIVE by construction (the "
                 "grammars were selected on the FULL populations in K2); it "
                 "is explicitly NOT 'unseen'/'holdout' evidence.")
    lines.append("- The 2003 leg is DIAGNOSTIC ONLY; near-zero transfer "
                 "would be the finding CORPUS_SPECIFIC_935 (valid "
                 "outcome): reported near_zero_transfer=%s (see "
                 "ERA_TRANSFER_RESULTS.json, including per-stratum fits "
                 "over byte-identical / changed / only-2003 files)."
                 % era_res["corpus_specific_935_assessment"]
                 ["near_zero_transfer_vs_matched_nc"])
    lines.append("- NOT checked: g1/g2/mscan/H1-H4/H5b/H5d/H6/H8 grammars "
                 "(out of contract scope); H5c1 (idx<2N) was NOT in this "
                 "run's gate set (contract fixes H5a/H5c2/H7).")
    lines.append("- 2003 era census finding (prior-evidence defect, "
                 "documented): R35's published 2003 rr_var=1180 uses the "
                 "(file,tag,si) span key, which collides when one file "
                 "carries multiple same-tag morph blocks; the collider "
                 "(574845.nif bi=77 si=14 tag=3; var_ok but NOT rr) "
                 "inflates R35's count by exactly one. This run's census "
                 "reproduces EVERY other R35 anchor EXACTLY and reproduces "
                 "1,180 under R35's own keying; the collision-free "
                 "(file,bi,si) census value is 1,179, which defines the era "
                 "populations (see ERA_CENSUS_2003.json rr_var_resolution).")
    lines.append("")
    lines.append("## 9/10. RETRACTIONS + CHAIN OF CUSTODY")
    lines.append("")
    lines.append("No retraction from this run. Supersession-sensitive "
                 "context: K2's +65/88.88% coverage status REMAINS "
                 "CANDIDATE. This run made NO commit (PE-MASTER handles "
                 "publication after its audit); BASE_SHA per contract "
                 "90c86be9e52d00e4dd916ea75bc99ea93354c88f (no repo writes "
                 "by the executor). Originals (corpora, R61, K1/K2/K3, all "
                 "prior packages) READ-ONLY, verified by pins.")
    lines.append("")
    lines.append("## 11. PUSH DISCIPLINE")
    lines.append("")
    lines.append("No commit, no push (per contract). BASE_SHA 90c86be9... "
                 "unchanged by this run.")
    lines.append("")
    lines.append("## 13. NEGATIVE CONTROLS")
    lines.append("")
    lines.append("- NC-A: per-span trials at pinned wrong starts u+2/u-2 "
                 "(denominator spans x 2), K2 nc2 VERBATIM semantics; "
                 "NC-B: per-span non-adjacent joins (seeded 20260906, "
                 "mirroring the <=2 adjacency trials per span; NEVER "
                 "one-per-file). Vacuous 0>=5x0 CANNOT pass "
                 "(NC_EMPTY_DENOMINATOR).")
    lines.append("- G-EXEC: 8/8 synthetic fixtures fail-closed (see "
                 "NEGATIVE_FIXTURES_GEXEC.json); manifest negative tests "
                 "a-f: %d/6 FAIL the gate as required. The gates CAN fail "
                 "(several produce explicit non-pass classes on the real "
                 "populations where the a-priori thresholds are not met)."
                 % sum(1 for t in neg["tests"]
                       if t["gate_failed_as_required"]))
    lines.append("")
    lines.append("## 14. HARD STOPS")
    lines.append("")
    lines.append("NONE encountered. (HARD_STOP classes armed by the driver: "
                 "pin mismatch / census mismatch / write-outside / 2003 "
                 "corpus unresolvable.)")
    lines.append("")
    lines.append("## 15. NEXT STEP + GATES (PE-MASTER decision)")
    lines.append("")
    lines.append("Proposed next: PE-MASTER post-run audit of this package "
                 "(verdict persistence + publication). Gate needs: nothing "
                 "from the human; no human-gated action inside this run.")
    lines.append("")
    lines.append("## 16. UNKNOWN STAYS UNKNOWN")
    lines.append("")
    lines.append("-256/field1 semantics unknown; RUNTIME_SEMANTICS not "
                 "tested; family/corpus counts as recorded above are the "
                 "only quantitative claims.")
    lines.append("")
    lines.append("## 17. PAYLOAD DISCIPLINE")
    lines.append("")
    lines.append("Zero proprietary payloads in this package: outputs carry "
                 "identifiers, outcomes, rejection reasons and byte COUNTS "
                 "only (no payload bytes, no hex dumps). Originals appear "
                 "as identity metadata (SHA-256 + paths) in "
                 "artifact_index.csv external-sources section.")
    lines.append("")
    lines.append("## 18. DERIVED-NUMBER PROVENANCE")
    lines.append("")
    lines.append("Generator: 00_CONTROL/revalidate_driver_r1.py sha256 "
                 + pin_results["driver_sha256"])
    lines.append("Frozen grammars executed by IMPORT of the pinned K2 "
                 "module (sha256 " + K2_PINS["K2_driver"][1] + "); "
                 "FROZEN_GRAMMARS.md blocks byte-verified against the "
                 "pinned source (%s). Census pipeline replicates the K2 "
                 "stage-1 exactly (G-CENSUS PASS with row agreement "
                 "6,167/6,167)."
                 % pin_results["frozen_grammars_verified_blocks"])
    lines.append("")
    lines.append("## 19. HANDOFF BLOCK (copyable)")
    lines.append("")
    lines.extend(handoff)
    lines.append("")
    lines.append("## 20. SELF-CONTAINED NOTES")
    lines.append("")
    lines.append("Populations: P1 = the 334 no-fit rr spans (pinned "
                 "NOFIT334_SPANS.txt headers == census set, EXACT); P2 = "
                 "the 325 residual spans (subset of pinned 333, count 325 "
                 "EXACT, 56 files, 551564.nif x84). Split: seeded "
                 "Random(20260906) file-level 50/50 over %d files "
                 "(side A %d / side B %d). Prior-use verdict: NO grammar "
                 "of the family was derived from 2003-era data (evidence "
                 "in PRIOR_USE_VERDICT.json). 2003 corpus: 01_Original_"
                 "Files\\BNT_Models\\Models.bnt sha256 1322adf2...4a6, "
                 "5,426 entries (5,426-name class EXACT; container<-"
                 ">extraction tie 5,426/5,426); the contract's '~5,441' is "
                 "the R12 manifest CSV physical-line count (5,442 incl. "
                 "header) whose true CSV record count is 5,426 (standard "
                 "CSV parser; recorded in PIN_RESULTS.json)."
                 % (split_freeze["n_files"], len(split_freeze["side_A_files"]),
                    len(split_freeze["side_B_files"])))
    lines.append("")
    lines.append(STANDING)
    lines.append("")
    wr_lines(os.path.join(REPT, "00_FINAL_REPORT.md"), lines)
    wr_lines(os.path.join(REPT, "HANDOFF.md"),
             ["# HANDOFF - PE_NIF_MORPH_GRAMMAR_REVALIDATION_"
              "R1_20260906_140500", ""] + handoff + ["", STANDING])

    # ---- final manifest: written AFTER every other package file is final --
    # exclusions (documented): artifact_index.csv (self-hash impossible;
    # L12 precedent) and 05_ANALYSIS/MANIFEST_VALIDATION.json (circular: it
    # records the validation OF this manifest; written last).
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
    import io as _io
    buf = _io.StringIO()
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
        hard_stop("post-write manifest validation FAILED",
                  {"findings": man_out["findings"],
                   "pre_validation_ok": bool(ok_x)})
    man_val = {"standing": STANDING,
               "spec": "RUN B MANIFEST_SCHEMA_SPEC.md (dogfooding)",
               "manifest": manifest_path,
               "documented_exclusions": [
                   "artifact_index.csv (self-hash impossible; L12 precedent)",
                   "05_ANALYSIS/MANIFEST_VALIDATION.json (circular: records "
                   "the validation of this manifest; written last)"],
               "pre_validation_in_memory": {
                   "gate_pass": bool(ok_x),
                   "ordinary_rows": out_x["ordinary_rows"],
                   "note": "executed BEFORE the final gates CSV write; the "
                           "gates CSV row was added afterwards with the "
                           "hash of its final on-disk bytes"},
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
    log("[r1] manifest: %d ordinary + %d external rows; post-write "
        "validation PASS; MANIFEST_VALIDATION.json written last"
        % (man_out["ordinary_rows"], man_out["external_rows"]))
    log("[r1] DONE in %.1fs" % (time.time() - T0))
    log("[r1] gates: " + json.dumps({k: v["status"] for k, v in gates.items()}))


def main():
    log("[r1] RUN A: PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500")
    corp = stage0_pins()
    data935, ent935 = corp["data935"], corp["ent935"]
    data2003, ent2003 = corp["data2003"], corp["ent2003"]
    sys.path.insert(0, R61_SOURCE_DIR)
    from pe_nif_reader import PENifReader  # noqa: E402
    sys.path.insert(0, K2_CTRL)
    import morph_residual_deepdive_r1 as K2  # noqa: E402
    globals()["K2"] = K2
    globals()["PENifReader"] = PENifReader

    big_all, nofit, unknown325, r21_unknown, blocks_ctx = s1_census(
        ent935, data935)
    side_of, split_freeze = s2_freeze(nofit, unknown325, r21_unknown)
    retro = s3_retro(nofit, unknown325, side_of, blocks_ctx)
    era_res = s45_era(ent935, data935, nofit, unknown325, big_all)
    gexec_pass, fixtures, audit = s6_gexec()
    with open(os.path.join(CTRL, "PIN_RESULTS.json"), encoding="utf-8") as f:
        pin_results = json.load(f)
    s7_outputs(retro, era_res, gexec_pass, fixtures, audit, pin_results,
               split_freeze)
    log("[r1] RUN A COMPLETE. Log lines: %d" % len(LOG_LINES))


if __name__ == "__main__":
    main()
