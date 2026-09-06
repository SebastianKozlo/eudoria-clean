#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PE_NIF_MORPH_WIDERECORD_R1_20260906_170000 - RUN C driver
(widerecord_driver_r1.py). RUN_CLASS: LOAD_BEARING. Executor:
pe-reconstruction. Parent: PE-MASTER loop bd17344b (iteration 3).
Milestone EU935-M1 (NO crossing). ERA: PCG_9_3_5 primary.

ONE_PRIMARY_QUESTION (contract 00_CONTROL/CONTRACT.md): do the
pre-registered wide-record grammars - W1: the fixed-m mscan unit
[u16 idx][32 x f32] (m=32, head weights - the K2 post-hoc probe's
candidate); W2: var-k with the k-range extended to 9..24 (the 'k~23'
candidate); W3: W1 with a Wm mis-estimate window (Wm +/- 64, step 4) -
consume the 269 remaining 9.3.5 no-fit morph spans (334 minus the 65
RUN-A-validated H5a/H5c2 fits) byte-exactly, at rates separated >= 5x
from denominator-matched wrong-start negative controls, with
per-record validation and file-grouped retrospective homogeneity?

STAGES: S0 pins -> S1 census (G-CENSUS incl. the RUN A removal
reproduction + the 269 derivation + freeze cross-checks) -> S3 the
W1/W2/W3 per-record executions + NCs on the 269 -> S4 G-WIDE +
WIDE_RESULTS + COVERAGE_DELTA -> S5 G-EXEC (self-audit + 8 negative
fixtures) -> S6 outputs (gates CSV, reports, manifest + validation).

DISCIPLINE: read-only originals; outputs ONLY to this run dir (write
guards); zero payloads; run-local tooling only in 00_CONTROL; no git;
no wiki; no milestone action; the residual-325 is OUT OF SCOPE; NO
H7-based claims; POST-HOC probes = NON-COVERAGE (none executed).

Standing sentence (every artifact): no semantic claims; the +65
H5a/H5c2 status = RETROSPECTIVE_VALIDATED (RUN A); the H7
join-mechanism = UNVALIDATED (RUN A) - this run makes NO H7-based
claims; the residual-325 population is OUT OF SCOPE (stays
mechanism-unexplained; a diagnostic note only, no new claims). Result
classes: BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION /
RUNTIME_SEMANTICS (= explicitly NOT_TESTED here, out of scope).
"""
import sys
import os
import csv
import json
import time
import struct
import hashlib
import math
from collections import Counter, defaultdict

sys.dont_write_bytecode = True  # protect READ-ONLY source trees

RUN = (r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_"
       r"WIDERECORD_R1_20260906_170000")
CTRL = os.path.join(RUN, "00_CONTROL")
RAW = os.path.join(RUN, "01_RAW")
ANA = os.path.join(RUN, "05_ANALYSIS")
REPT = os.path.join(RUN, "06_REPORT")
for d in (CTRL, RAW, ANA, REPT):
    if not os.path.isdir(d):
        os.makedirs(d)

T0 = time.time()
DRIVER_PATH = os.path.join(CTRL, "widerecord_driver_r1.py")

STANDING = ("Standing sentence: no semantic claims; the +65 H5a/H5c2 "
            "status = RETROSPECTIVE_VALIDATED (RUN A); the H7 "
            "join-mechanism = UNVALIDATED (RUN A) - this run makes NO "
            "H7-based claims; the residual-325 population is OUT OF "
            "SCOPE (stays mechanism-unexplained; a diagnostic note only, "
            "no new claims). Result classes: BYTE_MATCH / REPEATABILITY "
            "/ RETROSPECTIVE_VALIDATION / RUNTIME_SEMANTICS (= "
            "explicitly NOT_TESTED here, out of scope).")

# ------------------------------------------------------------------ inputs ---
A = r"D:\Eudoria_Reconstruction\99_Audits"
K2_RUN = os.path.join(A, "PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209")
K2_CTRL = os.path.join(K2_RUN, "00_CONTROL")
K2_DRIVER = os.path.join(K2_CTRL, "morph_residual_deepdive_r1.py")
K2_RAWD = os.path.join(K2_RUN, "01_RAW")
K2_ANA = os.path.join(K2_RUN, "05_ANALYSIS")
RUNA_RUN = os.path.join(A, "PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500")
RUNA_RETRO = os.path.join(RUNA_RUN, "01_RAW", "RETRO_SPAN_OUTCOMES.jsonl")
RUNA_MANIFEST = os.path.join(RUNA_RUN, "artifact_index.csv")
R61_SOURCE_DIR = os.path.join(
    A, r"PE_R61_FROZEN_BASELINE_20260828\01_source")
R61_SHA_JSON = os.path.join(
    A, r"PE_R61_FROZEN_BASELINE_20260828\03_validation\SHA256_SOURCE.json")
MANIFEST_SPEC = os.path.join(
    A, r"PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500\00_CONTROL"
    r"\MANIFEST_SCHEMA_SPEC.md")
R34_RSG = os.path.join(
    A, r"PE_NIF_MORPH_QUANT_R34_20260904_164538\02_results"
    r"\REAL_SPARSE_GRAMMAR.json")
R34_RSG_SHA = "2c26ba86db44ad7a58322c136112fec36e23efab1db1fafea1c976311eba007e"

MODELS_935 = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
MODELS_935_SHA = ("c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face"
                  "7e969be0b3d3bee0")
MODELS_935_ENTRIES = 5596

K2_PINS = {
    "K2_driver": (K2_DRIVER,
                  "b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a"),
    "K2_NOFIT334_SPANS": (
        os.path.join(K2_RAWD, "NOFIT334_SPANS.txt"),
        "8bb6556b166df656631af168031e58518b3147fe962d5815ca4e19009e0f605d"),
    "K2_COVERAGE_STATE": (
        os.path.join(K2_ANA, "COVERAGE_STATE.json"),
        "86c12fa7f3df1149213fbfdef3097f022bb7c7ba38dc2cf4289de4aab1b12fa4"),
    "K2_HYPOTHESIS_RESULTS": (
        os.path.join(K2_ANA, "HYPOTHESIS_RESULTS.json"),
        "c08fb4738ece9d1f2c9cbcb43fe05b866f7560b1808597abc78e70e6e438e4a9"),
    "K2_BASELINE_REPRODUCTION": (
        os.path.join(K2_ANA, "BASELINE_REPRODUCTION.json"),
        "2e4014c9652df8adf6854b87c17388f9a5288c2c32dc757b34946320db46f1ca"),
    "RUNA_driver": (
        os.path.join(RUNA_RUN, "00_CONTROL", "revalidate_driver_r1.py"),
        "02ecb955bc3796128ed3f3b99cc302df61649f9ac2202e83ee5860ed5de9dbe0"),
    "R34_REAL_SPARSE_GRAMMAR": (R34_RSG, R34_RSG_SHA),
}
CONTRACT_SHA_EXPECT = ("404f73687913a5ee934ce123b6bd9588bc2427dfd7b73"
                       "b2f217f1b21f6ff5f3e")

# K2 census anchors (the pinned K2 BASELINE_REPRODUCTION.json; the
# G-CENSUS hard gate asserts these EXACTLY).
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

WIDE_GRAMMARS = {
    "W1": ("the fixed-m mscan unit [u16 idx][32 x f32] (m=32) with the "
           "head weight pair, consuming the span from the walk start; "
           "executed VERBATIM as K2.parse_fixed(dp, u, N, 32), fit = ok "
           "and recs > 0"),
    "W2": ("the var-k grammar with the k-range extended to 9..24 (all "
           "other constraints identical to the canon var-k); executed "
           "VERBATIM as K2.parse_variable(dp, u, N, kmax=24), fit = ok "
           "and recs > 0"),
    "W3": ("W1 with a Wm mis-estimate window (Wm-64..Wm+64, step 4); "
           "executed VERBATIM as K2.parse_fixed(dp, u+d, N, 32) over d "
           "in -64..+64 step 4 (33 positions incl. 0; ascending scan; "
           "first hit recorded), fit = any window position ok and "
           "recs > 0"),
}
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
        f.write("".join(x if x.endswith("\n") else x + "\n"
                        for x in lines))


def append_jsonl(path, obj):
    _guard(path)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(obj, ensure_ascii=True) + "\n")


def hard_stop_now(reason, evidence):
    """HARD STOP: write evidence + handoff, exit 3 (fail-closed)."""
    ev = {"run": "PE_NIF_MORPH_WIDERECORD_R1_20260906_170000",
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
    log("[rc] HARD STOP: " + reason)
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
    Direction convention (RUN A precedent): P(X<=k-1) is DECREASING in p,
    so the lower-bound bisection moves 'a' UP while the CDF is still
    above 0.975; the upper bound solves P(X<=k) = 0.025 the same way."""
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


def parse_dump_headers(path):
    ids = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("== "):
                head = line[3:].split()
                ids.append((head[0], int(head[1].split("=")[1]),
                            int(head[2].split("=")[1])))
    return ids


# --------------------------------------------- S0: pins (G-PINS) ------------
def stage0_pins():
    log("[rc] S0: pins (G-PINS)")
    pr = {}
    csha = sha256_file(os.path.join(CTRL, "CONTRACT.md"))
    if csha.lower() != CONTRACT_SHA_EXPECT:
        hard_stop_now("contract SHA mismatch", {"got": csha})
    pr["contract_sha256"] = csha
    pr["contract_match"] = True

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
    log("[rc] R61 10/10 PASS")

    s935 = sha256_file(MODELS_935)
    if s935 != MODELS_935_SHA:
        hard_stop_now("9.3.5 corpus SHA mismatch",
                      {"expected": MODELS_935_SHA, "got": s935})
    pr["corpus_935"] = {"path": MODELS_935, "sha256": s935}
    log("[rc] corpus 9.3.5 SHA verified (re-hashed from bytes)")

    with open(MODELS_935, "rb") as f:
        data935 = f.read()
    ent935 = read_bnt_index(data935)
    if len(ent935) != MODELS_935_ENTRIES or \
            len(set(nm for nm, _, _ in ent935)) != MODELS_935_ENTRIES:
        hard_stop_now("9.3.5 corpus entry count mismatch",
                      {"expected": MODELS_935_ENTRIES, "got": len(ent935)})
    pr["corpus_935"]["entries"] = len(ent935)
    log("[rc] corpus 9.3.5: %d entries" % len(ent935))

    for k, (p, exp) in K2_PINS.items():
        got = sha256_file(p)
        ok = got.lower() == exp.lower()
        pr[k] = {"path": p, "sha256": got, "expected": exp, "match": ok}
        if not ok:
            hard_stop_now("pin mismatch: " + k,
                          {"path": p, "expected": exp, "got": got})
        log("[rc] pin %s: %s OK" % (k, got[:12]))

    # RUN A RETRO_SPAN_OUTCOMES.jsonl: pin = the ordinary row of RUN A's
    # own artifact_index.csv (the K2 artifact_index is DEFECTIVE and is
    # NEVER used as a hash source; RUN A's manifest is the row source).
    exp_row = None
    with open(RUNA_MANIFEST, "r", encoding="utf-8", newline="") as f:
        for ln in f:
            if ln.startswith("01_RAW/RETRO_SPAN_OUTCOMES.jsonl,"):
                exp_row = ln.strip()
                break
    if exp_row is None:
        hard_stop_now("RUN A manifest row for RETRO_SPAN_OUTCOMES missing",
                      {})
    sha_exp = exp_row.split(",")[-1]
    got = sha256_file(RUNA_RETRO)
    if got.lower() != sha_exp.lower():
        hard_stop_now("RUN A RETRO_SPAN_OUTCOMES hash mismatch vs row",
                      {"row": exp_row, "got": got})
    pr["RUNA_RETRO_SPAN_OUTCOMES"] = {
        "path": RUNA_RETRO, "sha256": got,
        "pin_provenance": "RUN A artifact_index.csv ordinary row",
        "match": True}
    pr["RUNA_artifact_index_sha256"] = sha256_file(RUNA_MANIFEST)
    log("[rc] pin RUNA_RETRO_SPAN_OUTCOMES: %s OK (manifest-row pin)"
        % got[:12])

    if not os.path.isfile(MANIFEST_SPEC):
        hard_stop_now("MANIFEST_SCHEMA_SPEC.md missing", {})
    pr["MANIFEST_SCHEMA_SPEC"] = {"path": MANIFEST_SPEC,
                                  "sha256": sha256_file(MANIFEST_SPEC)}

    # freeze artifacts on disk: hashes recorded; PREREG_MARKER re-verified
    freeze_files = ["WIDE_GRAMMARS.md", "POPULATION_269.json",
                    "NC_PROCEDURES.md", "SPLIT_SIDES_269.json",
                    "GATES_PREREGISTERED.md", "PREREG_MARKER.txt",
                    "freeze_wide_r1.py"]
    marker = open(os.path.join(CTRL, "PREREG_MARKER.txt"),
                  encoding="utf-8").read()
    for fn in freeze_files:
        p = os.path.join(CTRL, fn)
        if not os.path.isfile(p):
            hard_stop_now("freeze artifact missing: " + fn, {})
        h = sha256_file(p)
        pr["freeze_" + fn] = h
        if fn not in ("PREREG_MARKER.txt", "freeze_wide_r1.py"):
            if h not in marker:
                hard_stop_now("freeze hash not recorded in PREREG_MARKER: "
                              + fn, {"sha256": h})
    # byte-verify the frozen grammar blocks vs the pinned K2 source
    with open(K2_DRIVER, "r", encoding="utf-8", newline="") as f:
        k2_src = f.read().split("\n")
    with open(os.path.join(CTRL, "WIDE_GRAMMARS.md"), encoding="utf-8") as f:
        frozen = f.read()
    blocks_ok = 0
    for label, lo, hi in K2_FROZEN_BLOCK_RANGES:
        seg = "\n".join(k2_src[lo - 1:hi])
        if ("```python\n" + seg + "\n```") in frozen:
            blocks_ok += 1
        else:
            hard_stop_now("WIDE_GRAMMARS.md block mismatch: " + label,
                          {"range": [lo, hi]})
    pr["frozen_grammars_verified_blocks"] = (
        "%d/%d VERBATIM byte-exact vs pinned K2 source"
        % (blocks_ok, len(K2_FROZEN_BLOCK_RANGES)))
    log("[rc] WIDE_GRAMMARS.md: %d/%d blocks byte-exact vs pinned K2 "
        "driver" % (blocks_ok, len(K2_FROZEN_BLOCK_RANGES)))

    pr["driver_sha256"] = sha256_file(DRIVER_PATH)
    pr["standing"] = STANDING
    wr_json(os.path.join(CTRL, "PIN_RESULTS.json"), pr)
    return {"data935": data935, "ent935": ent935}


# ----------------------------- census (K2 stage-1 replica; RUN A verbatim) ---
def run_census(reader, entries, data, expect, era_label, r34_rows=None):
    """Replicates the K2 census pipeline EXACTLY (K2 driver stage 1; the
    RUN A revalidation replica): R61 parse -> morph blocks with tag ->
    tag-split spans -> big spans -> R18 walk -> R34 grammar re-derivation
    (+ row agreement) -> rr/nofit census -> R20/R21 residual census ->
    R21 probe."""
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
            log("[rc] %s parse %d/%d (%.0fs)"
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
        hard_stop_now("%s parse closure < 100%% (%d fails)"
                      % (era_label, parse_fail), {"parse_fail": parse_fail})
    log("[rc] %s big spans: %d" % (era_label, big_spans))

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


# --------------------------- grammar executors (VERBATIM K2 verdicts) -------
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
            if not K2.clean(v):
                return ("UNCLEAN_FLOAT_AT_%d" % p, p, recs)
        recs += 1
        p += rl
    return ("COMPLETE", p, recs)


def diag_parse_variable_kmax(dp, u, N, kmax):
    """Mirror of the frozen W2 parser (K2.parse_variable with the frozen
    kmax extension) for failure classification ONLY. The FIT verdict
    ALWAYS comes from K2.parse_variable."""
    p = u
    end = len(dp)
    recs = 0
    while p < end:
        if p + 2 > end:
            return ("OVERRUN_AT_%d" % p, p, recs)
        idx = struct.unpack_from("<H", dp, p)[0]
        if idx >= N:
            return ("IDX_GE_N_AT_%d" % p, p, recs)
        found = False
        for k in range(1, kmax + 1):
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


def w3_window():
    return list(range(-W3_WIN, W3_WIN + 1, W3_STEP))


def exec_w1(rec):
    dp, u, N = rec["dp"], rec["u"], rec["N"]
    ok, recs, idxs, wp = K2.parse_fixed(dp, u, N, 32)
    fit = bool(ok and recs > 0)
    reason, p, drecs = diag_parse_fixed(dp, u, N, 32)
    agree = (drecs == recs) and ((reason == "COMPLETE") == bool(ok))
    consumed = (len(dp) - u) if fit else max(p - u, 0)
    return fit, reason, consumed, {"records": recs, "wp_pairs": wp,
                                  "diag_agree": agree}


def exec_w2(rec):
    dp, u, N = rec["dp"], rec["u"], rec["N"]
    ok, recs, kh, idxs = K2.parse_variable(dp, u, N, kmax=24)
    fit = bool(ok and recs > 0)
    reason, p, drecs = diag_parse_variable_kmax(dp, u, N, 24)
    agree = (drecs == recs) and ((reason == "COMPLETE") == bool(ok))
    consumed = (len(dp) - u) if fit else max(p - u, 0)
    return fit, reason, consumed, {"records": recs, "k_hist": dict(kh),
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
        ok, recs, idxs, wp = K2.parse_fixed(dp, u2, N, 32)
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
    if g == "W2":
        return exec_w2(rec)
    return exec_w3(rec)


def nc_exec(g, rec, u2):
    """NC trial: the SAME grammar executed at the pinned wrong start u2
    (u+2 / u-2 per NC_PROCEDURES.md). Returns (hit, reason, consumed)."""
    dp, N = rec["dp"], rec["N"]
    if u2 < 0:
        return False, "INVALID_START_NONHIT", 0
    if g == "W1":
        ok, recs, idxs, wp = K2.parse_fixed(dp, u2, N, 32)
        hit = bool(ok and recs > 0)
        reason, p, _dr = diag_parse_fixed(dp, u2, N, 32)
        consumed = (len(dp) - u2) if hit else max(p - u2, 0)
        return hit, reason, consumed
    if g == "W2":
        ok, recs, kh, idxs = K2.parse_variable(dp, u2, N, kmax=24)
        hit = bool(ok and recs > 0)
        reason, p, _dr = diag_parse_variable_kmax(dp, u2, N, 24)
        consumed = (len(dp) - u2) if hit else max(p - u2, 0)
        return hit, reason, consumed
    # W3: the frozen window anchored at u2 (the whole window shifted)
    d_hit = None
    for d in w3_window():
        u3 = u2 + d
        if u3 < 0:
            continue
        ok, recs, idxs, wp = K2.parse_fixed(dp, u3, N, 32)
        if ok and recs > 0:
            d_hit = d
            break
    if d_hit is None:
        return False, "NO_WINDOW_HIT", 0
    return True, ("WINDOW_HIT_%+d" % d_hit), len(dp) - (u2 + d_hit)


# --------------------------------------------- unit machinery (RUN A std) ---
def build_units(pop_recs, side_of):
    """Unit = byte-identical dp payload (sha256), dedup within the
    population; unit side = side of its FIRST member in sorted
    (file,bi,si) order; a unit whose members land on both sides is a
    split family (counted once, on the first-member side)."""
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


# ------------------------------------------------------------- G-WIDE gate ---
def evaluate_gwide(grammar_id, members_all, members_A, members_B,
                   nc_full_trials, nc_B_trials):
    """A-priori G-WIDE gate (GATES_PREREGISTERED.md; frozen operational
    decisions d1-d4). All fit/NC counts are counter increments over
    EXECUTED records (never len()); len() is used only for denominators
    and population transparency. Fail-closed; the deterministic class
    order is frozen in GATES_PREREGISTERED.md d3."""
    v = {"grammar": grammar_id, "gate": "G-WIDE", "non_pass_class": None,
         "result": "NON_PASS"}
    for m in list(members_all) + list(members_A) + list(members_B):
        if (not isinstance(m, dict) or not m.get("wellformed")
                or "key" not in m or "side" not in m or "unit" not in m
                or "fit" not in m or not isinstance(m.get("fit"), bool)):
            v["non_pass_class"] = "CORRUPTED_RECORD"
            v["detail"] = str(m)[:160]
            return v
    for t in list(nc_full_trials) + list(nc_B_trials):
        if not isinstance(t, dict) or not isinstance(t.get("hit"), bool):
            v["non_pass_class"] = "CORRUPTED_RECORD"
            v["detail"] = {"bad_nc_trial": str(t)[:160]}
            return v
    keysA = [tuple(m["key"]) if isinstance(m["key"], list) else m["key"]
             for m in members_A]
    keysB = [tuple(m["key"]) if isinstance(m["key"], list) else m["key"]
             for m in members_B]
    keys_all = [tuple(m["key"]) if isinstance(m["key"], list)
                else m["key"] for m in members_all]
    dup = sorted(set(keysA) & set(keysB))[:5]
    if dup:
        v["non_pass_class"] = "DUPLICATE_ACROSS_SIDES"
        v["detail"] = [list(d) if isinstance(d, tuple) else d
                       for d in dup]
        return v
    if len(keys_all) == 0:
        v["non_pass_class"] = "EMPTY_GROUP"
        v["detail"] = "population empty"
        return v
    if len(keysB) == 0:
        v["non_pass_class"] = "EMPTY_GROUP"
        v["detail"] = "held-out side empty"
        return v
    units_B = {}
    for m in members_B:
        u = m["unit"]
        if u not in units_B:
            units_B[u] = False
        if m["fit"]:
            units_B[u] = True
    n_units_B = 0
    for _u in units_B:
        n_units_B += 1
    nc_hits_full = 0
    for t in nc_full_trials:
        if t["hit"]:
            nc_hits_full += 1
    nc_den_full = len(nc_full_trials)
    nc_hits_B = 0
    for t in nc_B_trials:
        if t["hit"]:
            nc_hits_B += 1
    nc_den_B = len(nc_B_trials)
    if nc_den_full != 2 * len(members_all):
        v["non_pass_class"] = "DENOMINATOR_MISMATCH"
        v["detail"] = {"nc_full_trials": nc_den_full,
                       "members_x_2": 2 * len(members_all)}
        return v
    if nc_den_B != 2 * n_units_B:
        v["non_pass_class"] = "DENOMINATOR_MISMATCH"
        v["detail"] = {"nc_B_trials": nc_den_B,
                       "units_x_2": 2 * n_units_B}
        return v
    if nc_den_full == 0 or nc_den_B == 0:
        v["non_pass_class"] = "NC_EMPTY_DENOMINATOR"
        v["detail"] = {"nc_full": nc_den_full, "nc_B": nc_den_B}
        return v
    if n_units_B < 30:
        v["non_pass_class"] = "INSUFFICIENT_TRIALS"
        v["detail"] = {"held_out_units": n_units_B}
        return v
    full_fits = 0
    for m in members_all:
        if m["fit"]:
            full_fits += 1
    if full_fits < 10:
        v["non_pass_class"] = "ZERO_FITS"
        v["detail"] = {"full_269_fits": full_fits}
        return v
    n_full = len(members_all)
    full_rate = full_fits / n_full
    nc_full_rate = nc_hits_full / nc_den_full
    if not (full_rate >= 5 * nc_full_rate):
        v["non_pass_class"] = "NC_INSUFFICIENT_SEPARATION"
        v["detail"] = {"positive_rate_full": round(full_rate, 6),
                       "nc_rate_full": round(nc_full_rate, 6)}
        return v
    unit_fits_B = 0
    for _u, f in units_B.items():
        if f:
            unit_fits_B += 1
    member_fits_B = 0
    for m in members_B:
        if m["fit"]:
            member_fits_B += 1
    rate_B = unit_fits_B / n_units_B
    nc_B_rate = nc_hits_B / nc_den_B
    if unit_fits_B < 10 or not (rate_B >= 5 * nc_B_rate):
        v["non_pass_class"] = "HETEROGENEOUS_SPLIT"
        v["detail"] = {"held_out_unit_fits": unit_fits_B,
                       "held_out_units": n_units_B,
                       "held_out_rate": round(rate_B, 6),
                       "held_out_nc_rate": round(nc_B_rate, 6),
                       "full_fits": full_fits,
                       "full_rate": round(full_rate, 6),
                       "full_nc_rate": round(nc_full_rate, 6),
                       "note": "the full-269 passes its rate test but the "
                               "held-out side fails - BOTH numbers "
                               "reported"}
        return v
    v["result"] = "PASS"
    v["full_269"] = {
        "members": n_full, "fits": full_fits,
        "rate": round(full_rate, 6),
        "rate_ci95_exact_binomial": clopper_pearson_95(full_fits, n_full)}
    v["full_nc"] = {
        "hits": nc_hits_full, "denominator": nc_den_full,
        "rate": round(nc_full_rate, 6),
        "rate_ci95_exact_binomial": clopper_pearson_95(
            nc_hits_full, nc_den_full)}
    v["separation_full"] = (round(full_rate / nc_full_rate, 2)
                            if nc_full_rate > 0 else None)
    v["held_out_side_B"] = {
        "units": n_units_B, "unit_fits": unit_fits_B,
        "rate": round(rate_B, 6),
        "rate_ci95_exact_binomial": clopper_pearson_95(
            unit_fits_B, n_units_B),
        "member_fits": member_fits_B, "members": len(members_B)}
    v["held_out_nc"] = {
        "hits": nc_hits_B, "denominator": nc_den_B,
        "rate": round(nc_B_rate, 6),
        "rate_ci95_exact_binomial": clopper_pearson_95(
            nc_hits_B, nc_den_B)}
    v["separation_held_out"] = (round(rate_B / nc_B_rate, 2)
                                if nc_B_rate > 0 else None)
    return v


# --------------------------------------- manifest gate (RUN B spec) ---------
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


# ------------------- S1: census (G-CENSUS) + the 269 derivation + freeze ----
def s1_census(ent935, data935):
    log("[rc] S1: 9.3.5 baseline census reproduction (G-CENSUS)")
    with open(R34_RSG, encoding="utf-8") as f:
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
        hard_stop_now("G-CENSUS mismatch (9.3.5 baseline != K2)",
                      {"checks": census935["census_checks"],
                       "row_agreement": census935["row_agreement"]})
    log("[rc] G-CENSUS baseline: PASS (row agreement %d/%d)"
        % (census935["row_agreement"][0], census935["row_agreement"][1]))

    # the pinned K2 nofit dump == the census-derived 334 (EXACT)
    pinned334 = set(parse_dump_headers(K2_PINS["K2_NOFIT334_SPANS"][0]))
    census334 = set((r["file"], r["bi"], r["si"]) for r in nofit)
    if len(pinned334) != 334 or pinned334 != census334:
        hard_stop_now("G-CENSUS: nofit 334 mismatch vs pinned "
                      "NOFIT334_SPANS",
                      {"pinned": len(pinned334), "census": len(census334)})

    # ---- the RUN A removals reproduce: pinned keys vs re-execution -----
    h5a_pinned = set()
    h5c2_pinned = set()
    with open(RUNA_RETRO, "r", encoding="utf-8") as f:
        for ln in f:
            r = json.loads(ln)
            k = tuple(r["span"])
            if r["grammar"] == "H5a" and r["outcome"] == "FIT":
                h5a_pinned.add(k)
            elif r["grammar"] == "H5c2" and r["outcome"] == "FIT":
                h5c2_pinned.add(k)
    if len(h5a_pinned) != 39 or len(h5c2_pinned) != 26:
        hard_stop_now("G-CENSUS: pinned RUN A FIT key counts != 39/26",
                      {"H5a": len(h5a_pinned),
                       "H5c2": len(h5c2_pinned)})
    h5a_reexec = set()
    h5c2_reexec = set()
    for rec in nofit:
        ok, recs, kh, idxs, left = K2.parse_variable_trunctail(
            rec["dp"], rec["u"], rec["N"])
        if ok and recs > 0 and left > 0:
            h5a_reexec.add((rec["file"], rec["bi"], rec["si"]))
        ok, recs, kh, idxs = K2.parse_variable(
            rec["dp"], rec["u"], rec["N"], idx_limit=0x8000)
        if ok and recs > 0:
            h5c2_reexec.add((rec["file"], rec["bi"], rec["si"]))
    if h5a_reexec != h5a_pinned or h5c2_reexec != h5c2_pinned:
        hard_stop_now("G-CENSUS: RUN A removals do not reproduce under "
                      "re-execution",
                      {"H5a_reexec": len(h5a_reexec),
                       "H5a_pinned": len(h5a_pinned),
                       "H5c2_reexec": len(h5c2_reexec),
                       "H5c2_pinned": len(h5c2_pinned)})
    # K2 pinned cross-check (REPEATABILITY; transitive with RUN A)
    with open(K2_PINS["K2_HYPOTHESIS_RESULTS"][0], encoding="utf-8") as f:
        k2_results = json.load(f)
    k2_h5a = set(tuple(k) for k, _l in k2_results["H5a"]["fits"])
    k2_h5c2 = set(tuple(k) for k, _mx in
                  k2_results["H5c"]["H5c2_idx_lt_0x8000"]["fits"])
    if k2_h5a != h5a_pinned or k2_h5c2 != h5c2_pinned:
        hard_stop_now("G-CENSUS: K2 fit lists != RUN A pinned FIT keys", {})
    union65 = h5a_pinned | h5c2_pinned
    if len(union65) != 65:
        hard_stop_now("G-CENSUS: union of RUN A removals != 65",
                      {"union": len(union65)})
    if not union65 <= census334:
        hard_stop_now("G-CENSUS: RUN A removals not subset of the 334", {})
    if len(census334) - len(union65) != 269:
        hard_stop_now("G-CENSUS: 334 - 65 != 269 EXACT", {})
    pop269 = [r for r in nofit
              if (r["file"], r["bi"], r["si"]) not in union65]
    pop269_keys = sorted((r["file"], r["bi"], r["si"]) for r in pop269)
    if len(pop269) != 269:
        hard_stop_now("G-CENSUS: the derived 269 population != 269",
                      {"got": len(pop269)})
    log("[rc] G-CENSUS: RUN A removals reproduce (39 + 26 = 65; "
        "334 - 65 = 269 EXACT)")

    # ---- freeze cross-checks (the frozen lists == the census-derived) --
    with open(os.path.join(CTRL, "POPULATION_269.json"),
              encoding="utf-8") as f:
        frz = json.load(f)
    frozen269 = sorted(tuple(k) for k in frz["pop269_keys"])
    if frozen269 != pop269_keys:
        hard_stop_now("freeze population 269 != census-derived 269",
                      {"frozen": len(frozen269),
                       "census": len(pop269_keys)})
    with open(os.path.join(CTRL, "SPLIT_SIDES_269.json"),
              encoding="utf-8") as f:
        split = json.load(f)
    side_of = {}
    for f_ in split["side_A_files"]:
        side_of[f_] = "A"
    for f_ in split["side_B_files"]:
        side_of[f_] = "B"
    cover = len(split["pop269_side_A"]) + len(split["pop269_side_B"])
    if cover != 269:
        hard_stop_now("freeze split does not cover the 269",
                      {"cover": cover})
    for k in pop269_keys:
        if k[0] not in side_of:
            hard_stop_now("split side missing for file", {"file": k[0]})

    census935["era"] = "PCG_9_3_5"
    census935["result_class"] = "REPEATABILITY"
    census935["standing"] = STANDING
    census935["gate"] = ("G-CENSUS PASS: baseline reproduces K2 EXACTLY; "
                         "pinned 334 == census 334; RUN A removals "
                         "reproduce under re-execution (39 + 26 = 65); "
                         "334 - 65 = 269 EXACT; frozen 269 == census 269")
    census935["runA_removal_reproduction"] = {
        "result_class": "REPEATABILITY",
        "H5a_pinned_FIT_keys": len(h5a_pinned),
        "H5a_reexecuted_FIT_keys": len(h5a_reexec),
        "H5c2_pinned_FIT_keys": len(h5c2_pinned),
        "H5c2_reexecuted_FIT_keys": len(h5c2_reexec),
        "union_65": len(union65),
        "pop269": len(pop269_keys)}
    wr_json(os.path.join(ANA, "BASELINE_CENSUS_REPRODUCTION.json"),
            census935)
    return pop269, side_of, split


# --------------- S3: the W1/W2/W3 executions + NCs on the 269 ---------------
def s3_tests(pop269, side_of):
    log("[rc] S3: W1/W2/W3 per-record executions + NCs on the 269 "
        "(RETROSPECTIVE_VALIDATION)")
    out_jsonl = os.path.join(RAW, "WIDE_SPAN_OUTCOMES.jsonl")
    nc_jsonl = os.path.join(RAW, "WIDE_NC_TRIALS.jsonl")
    for p in (out_jsonl, nc_jsonl):
        if os.path.exists(p):
            os.remove(p)

    unit_side, unit_members, unit_split = build_units(pop269, side_of)
    members = {g: {"A": [], "B": []} for g in ("W1", "W2", "W3")}
    nc_full = {g: [] for g in ("W1", "W2", "W3")}
    nc_unit = {g: [] for g in ("W1", "W2", "W3")}
    consumed = {g: [] for g in ("W1", "W2", "W3")}
    n_outcome_lines = 0
    n_nc_lines = 0

    recs_sorted = sorted(pop269, key=lambda r: (r["file"], r["bi"],
                                                r["si"]))
    for rec in recs_sorted:
        key = [rec["file"], rec["bi"], rec["si"]]
        side = side_of.get(rec["file"], "?")
        unit = sha256_bytes(rec["dp"])
        is_split = unit in unit_split
        for g in ("W1", "W2", "W3"):
            fit, reason, consumed_b, extra = exec_grammar(g, rec)
            append_jsonl(out_jsonl, {
                "span": key, "side": side, "grammar": g,
                "outcome": "FIT" if fit else "NOFIT", "reason": reason,
                "bytes_consumed": consumed_b, "unit": unit,
                "split_family": is_split, "extra": extra,
                "result_class": "RETROSPECTIVE_VALIDATION"})
            n_outcome_lines += 1
            members[g][side].append({"key": key, "side": side,
                                     "unit": unit, "file": rec["file"],
                                     "fit": fit, "wellformed": True})
            if fit:
                consumed[g].append(tuple(key))
        # NC-A: per-span wrong-start trials u+2 / u-2 (2 per span)
        for g in ("W1", "W2", "W3"):
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

    # NC-B: held-out-side units (representatives), 2 trials per unit
    for g in ("W1", "W2", "W3"):
        for u in sorted(unit_members):
            if unit_side.get(u) != "B":
                continue
            rep = unit_members[u][0]
            key = [rep["file"], rep["bi"], rep["si"]]
            for d in (2, -2):
                u2 = rep["u"] + d
                tname = "u_plus_2" if d > 0 else "u_minus_2"
                hit, reason, cb = nc_exec(g, rep, u2)
                append_jsonl(nc_jsonl, {
                    "level": "unit_heldout", "unit": u, "span": key,
                    "side": "B", "grammar": g, "trial": tname, "u2": u2,
                    "hit": hit, "reason": reason, "bytes_consumed": cb,
                    "denominator": "units_x_2"})
                n_nc_lines += 1
                nc_unit[g].append({"hit": hit})

    log("[rc] S3: outcome lines %d; NC trial lines %d"
        % (n_outcome_lines, n_nc_lines))
    return (members, nc_full, nc_unit, consumed, unit_side, unit_members,
            unit_split)


# ------------- S4: G-WIDE evaluation + WIDE_RESULTS + COVERAGE_DELTA --------
def s4_results(members, nc_full, nc_unit, consumed, unit_side,
               unit_members, unit_split, split):
    log("[rc] S4: G-WIDE evaluation (a-priori conjunction, per grammar)")
    results = {
        "run": "PE_NIF_MORPH_WIDERECORD_R1_20260906_170000",
        "standing": STANDING,
        "result_class": "RETROSPECTIVE_VALIDATION",
        "leg": ("9.3.5 file-grouped 50/50 split of the 269 population "
                "(RETROSPECTIVE by construction - W1/W2/W3 were formulated "
                "from the K2 post-hoc probe of the SAME population's "
                "family; explicitly NOT unseen data)"),
        "gate": ("G-WIDE (GATES_PREREGISTERED.md; a-priori; never "
                 "adjusted after seeing results)"),
        "grammars": {},
    }
    verdicts = {}
    for g in ("W1", "W2", "W3"):
        mA = [m for m in members[g]["A"] if unit_side.get(m["unit"]) == "A"]
        mB = [m for m in members[g]["B"] if unit_side.get(m["unit"]) == "B"]
        mall_all = members[g]["A"] + members[g]["B"]
        v = evaluate_gwide(g, mall_all, mA, mB, nc_full[g], nc_unit[g])
        verdicts[g] = v
        # transparency numbers (never gate inputs)
        units_A = {}
        for m in mA:
            units_A.setdefault(m["unit"], False)
            if m["fit"]:
                units_A[m["unit"]] = True
        fits_A = 0
        for _u, f in units_A.items():
            if f:
                fits_A += 1
        units_all = {}
        for m in mall_all:
            units_all.setdefault(m["unit"], False)
            if m["fit"]:
                units_all[m["unit"]] = True
        ufits_all = 0
        for _u, f in units_all.items():
            if f:
                ufits_all += 1
        full_fits = 0
        for m in mall_all:
            if m["fit"]:
                full_fits += 1
        nc_hits_full = 0
        for t in nc_full[g]:
            if t["hit"]:
                nc_hits_full += 1
        member_fits_B = 0
        for m in mB:
            if m["fit"]:
                member_fits_B += 1
        units_B_t = {}
        for m in mB:
            units_B_t.setdefault(m["unit"], False)
            if m["fit"]:
                units_B_t[m["unit"]] = True
        unit_fits_B_t = 0
        for _u, f in units_B_t.items():
            if f:
                unit_fits_B_t += 1
        n_split_excl_B = 0
        for m in members[g]["B"]:
            if unit_side.get(m["unit"]) != "B":
                n_split_excl_B += 1
        side_B_files = sorted(set(m["file"] for m in mB))
        results["grammars"][g] = {
            "definition": WIDE_GRAMMARS[g],
            "gate_verdict": v,
            "full_269": {
                "members": len(mall_all), "fits": full_fits,
                "rate": (round(full_fits / len(mall_all), 6)
                         if mall_all else None),
                "rate_ci95_exact_binomial": clopper_pearson_95(
                    full_fits, len(mall_all)),
                "units_transparency": {
                    "units": len(units_all), "unit_fits": ufits_all,
                    "unit_rate": (round(ufits_all / len(units_all), 6)
                                  if units_all else None),
                    "note": "transparency only (d1); NOT a gate input"}},
            "full_nc": {
                "hits": nc_hits_full, "denominator": len(nc_full[g]),
                "rate": (round(nc_hits_full / len(nc_full[g]), 6)
                         if nc_full[g] else None),
                "rate_ci95_exact_binomial": clopper_pearson_95(
                    nc_hits_full, len(nc_full[g]))},
            "separation_full_transparency": (
                round((full_fits / len(mall_all))
                      / (nc_hits_full / len(nc_full[g])), 2)
                if nc_full[g] and nc_hits_full > 0 and mall_all else None),
            "held_out_side_B": {
                "members": len(mB), "member_fits": member_fits_B,
                "units": len(units_B_t), "unit_fits": unit_fits_B_t,
                "unit_rate": (round(unit_fits_B_t / len(units_B_t), 6)
                              if units_B_t else None),
                "unit_rate_ci95_exact_binomial": clopper_pearson_95(
                    unit_fits_B_t, len(units_B_t)),
                "files": side_B_files,
                "split_family_members_excluded": n_split_excl_B},
            "held_out_nc": {
                "hits": sum(1 for t in nc_unit[g] if t["hit"]),
                "denominator": len(nc_unit[g]),
                "rate": (round(
                    sum(1 for t in nc_unit[g] if t["hit"])
                    / len(nc_unit[g]), 6) if nc_unit[g] else None),
                "rate_ci95_exact_binomial": clopper_pearson_95(
                    sum(1 for t in nc_unit[g] if t["hit"]),
                    len(nc_unit[g]))},
            "side_A_transparency": {
                "members": len(mA), "units": len(units_A),
                "unit_fits": fits_A,
                "unit_rate": (round(fits_A / len(units_A), 6)
                              if units_A else None),
                "unit_rate_ci95_exact_binomial": clopper_pearson_95(
                    fits_A, len(units_A))},
            "consumed_keys": [list(k) for k in sorted(consumed[g])],
            "split_units_in_population": len(unit_split),
        }
        log("[rc] G-WIDE %s: %s %s (full %d/%d; NC %d/%d)"
            % (g, v["result"], v.get("non_pass_class") or "", full_fits,
               len(mall_all), nc_hits_full, len(nc_full[g])))

    sets = {g: set(consumed[g]) for g in ("W1", "W2", "W3")}
    results["grammar_overlaps"] = {
        "W1_and_W2": len(sets["W1"] & sets["W2"]),
        "W1_and_W3": len(sets["W1"] & sets["W3"]),
        "W2_and_W3": len(sets["W2"] & sets["W3"]),
        "W1_and_W2_and_W3": len(sets["W1"] & sets["W2"] & sets["W3"]),
        "union_all_grammars": len(sets["W1"] | sets["W2"] | sets["W3"]),
    }
    wr_json(os.path.join(ANA, "WIDE_RESULTS.json"), results)

    # ---- COVERAGE_DELTA.json (machine-readable coverage state) ----
    x_keys = set()
    per_grammar_cov = {}
    for g in ("W1", "W2", "W3"):
        verdict = verdicts[g]["result"]
        per_grammar_cov[g] = {
            "gate_verdict": verdict,
            "non_pass_class": verdicts[g].get("non_pass_class"),
            "consumed_spans": len(sets[g]),
            "counts_toward_coverage": bool(verdict == "PASS"),
            "status": ("RETROSPECTIVE_VALIDATED (RUN C; explicitly "
                       "retrospective, NOT unseen)" if verdict == "PASS"
                       else "EXCLUDED from coverage (gate NON_PASS; the "
                            "K2 OC-rejection precedent - fits recorded, "
                            "no coverage claim)")}
        if verdict == "PASS":
            x_keys |= sets[g]
    x = len(x_keys)
    total = 2093 + 65 + x
    cov = {
        "run": "PE_NIF_MORPH_WIDERECORD_R1_20260906_170000",
        "standing": STANDING,
        "result_class": "RETROSPECTIVE_VALIDATION",
        "real_record_coverage": {
            "denominator_rr_spans": 2427,
            "canon_var_k": {"spans": 2093,
                            "status": "BYTE_MATCH (canon var-k; K2/R34)"},
            "run_A_additions": {
                "spans": 65,
                "status": ("RETROSPECTIVE_VALIDATED (RUN A: H5a 39 + "
                           "H5c2 26; MASTER_ACCEPTED advisory)")},
            "this_run_additions": {
                "X_spans": x,
                "X_keys": [list(k) for k in sorted(x_keys)],
                "per_grammar": per_grammar_cov,
                "status": ("RETROSPECTIVE_VALIDATED (RUN C; explicitly "
                           "retrospective, NOT unseen)")},
            "new_total": total,
            "new_total_str": "%d/2427 (%.2f%%)"
                             % (total, 100.0 * total / 2427),
            "remaining_nofit": 269 - x,
            "remaining_nofit_note": "269 - X = %d" % (269 - x)},
        "out_of_scope": {
            "residual_325": ("OUT OF SCOPE this run - unchanged (RUN A: "
                             "74 join-explained, H7 mechanism UNVALIDATED; "
                             "251 unexplained; a diagnostic note only, "
                             "NO new claims)"),
            "H7": "this run makes NO H7-based claims",
            "era_2003": "out of scope this run (narrow 9.3.5 run)",
            "post_hoc_probes": ("NONE executed (any would be "
                                "NON-COVERAGE)")},
        "coverage_honesty": ("the +65 RUN A additions use grammars weaker "
                             "than canon (recorded in RUN A/K2); this "
                             "run's X is byte-exact SHAPE coverage with "
                             "per-record validation; RUNTIME_SEMANTICS "
                             "explicitly NOT_TESTED (out of scope)"),
    }
    wr_json(os.path.join(ANA, "COVERAGE_DELTA.json"), cov)
    log("[rc] COVERAGE_DELTA: X=%d -> new total %d/2427; remaining "
        "no-fit %d" % (x, total, 269 - x))
    return results, verdicts, cov


# --------------- S5: G-EXEC (self-audit + 8 negative fixtures) --------------
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
    log("[rc] S5: G-EXEC (self-audit + 8 negative fixtures)")
    fixtures = {"standing": STANDING, "result_class": "G-EXEC",
                "fixtures": []}

    def exec_fit(dp):
        ok, recs, idxs, wp = K2.parse_fixed(dp, 0, 4, 32)
        return bool(ok and recs > 0)

    def member(i, side, valid):
        dp = synthetic_payload(valid, i)
        return {"key": ["synthetic_%s_%03d.nif" % (side, i), 0, i],
                "side": side, "unit": sha256_bytes(dp),
                "file": "synthetic_%s_%03d.nif" % (side, i),
                "fit": exec_fit(dp), "wellformed": True}

    def nc(members, hit=False):
        out = []
        for m in members:
            for _tname in ("u_plus_2", "u_minus_2"):
                out.append({"span": m["key"], "hit": hit,
                            "reason": "synthetic"})
        return out

    # F1: zero successes both sides (32 units/side, all fail)
    f1_A = [member(i, "A", False) for i in range(32)]
    f1_B = [member(i, "B", False) for i in range(32)]
    v1 = evaluate_gwide("FIXTURE1", f1_A + f1_B, f1_A, f1_B,
                        nc(f1_A + f1_B), nc(f1_B))
    fixtures["fixtures"].append(
        {"id": 1, "name": "zero successes both sides",
         "expected": "explicit non-pass", "verdict": v1})
    # F2: empty population
    v2 = evaluate_gwide("FIXTURE2", [], [], [], [], [])
    fixtures["fixtures"].append(
        {"id": 2, "name": "empty population", "expected": "EMPTY_GROUP",
         "verdict": v2})
    # F3: only-previously-selected successes (side A fits, side B none)
    f3_A = [member(i, "A", True) for i in range(32)]
    f3_B = [member(i, "B", False) for i in range(32)]
    v3 = evaluate_gwide("FIXTURE3", f3_A + f3_B, f3_A, f3_B,
                        nc(f3_A + f3_B), nc(f3_B))
    fixtures["fixtures"].append(
        {"id": 3, "name": "only-previously-selected successes",
         "expected": ("explicit non-pass (full population passes; the "
                      "held-out side fails - BOTH numbers reported)"),
         "verdict": v3})
    # F4: a duplicate present in both groups
    dupm = member(0, "A", False)
    f4_B = [dupm] + [member(i, "B", False) for i in range(1, 32)]
    v4 = evaluate_gwide("FIXTURE4", [dupm] + f4_B, [dupm], f4_B,
                        nc([dupm] + f4_B), nc(f4_B))
    fixtures["fixtures"].append(
        {"id": 4, "name": "a duplicate present in both groups",
         "expected": "DUPLICATE_ACROSS_SIDES", "verdict": v4})
    # F5: unequal denominators (63 NC trials for 32 held-out units)
    f5_B = [member(i, "B", False) for i in range(32)]
    tr5 = nc(f5_B)[:63]
    v5 = evaluate_gwide("FIXTURE5", f5_B, [], f5_B, nc(f5_B), tr5)
    fixtures["fixtures"].append(
        {"id": 5, "name": "unequal denominators",
         "expected": "DENOMINATOR_MISMATCH", "verdict": v5})
    # F6: a corrupted record
    corrupt = {"key": ["x.nif", 0, 0], "side": "B", "unit": "u"}
    f6_B = [corrupt] + [member(i, "B", False) for i in range(1, 32)]
    v6 = evaluate_gwide("FIXTURE6", f6_B, [], f6_B, nc(f6_B), nc(f6_B))
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
    v8 = resolve_input_file(os.path.join(RUN,
                                         "NONEXISTENT_INPUT_FILE.json"))
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
    log("[rc] G-EXEC fixtures: %s (%d/8 fail-closed)"
        % (fixtures["gexec_verdict"], n_fix_ok))

    # (a) driver self-audit: size-derived assignments in gate code.
    # String literals are stripped to STR before the pattern scan so the
    # scanner cannot match its own detection code (RUN A precedent).
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


# ---------------------- S6: outputs (gates CSV, reports, manifest) ----------
def s6_outputs(results, verdicts, cov, gexec_pass, fixtures, audit,
               split, pin_results):
    log("[rc] S6: outputs (gates CSV, reports, manifest + validation)")
    gates = {}

    def add(name, desc, status):
        gates[name] = {"gate": name, "description": desc, "status": status}

    add("G-PINS", "every input pin verified in-driver before any parse "
        "(R61 10/10; Models.bnt re-hashed from bytes; the RUN A "
        "artifacts: driver + RETRO_SPAN_OUTCOMES via its manifest "
        "ordinary row; the K2 artifacts re-hashed from bytes - the K2 "
        "artifact_index.csv is DEFECTIVE and was never used as a hash "
        "source; the frozen grammar blocks byte-verified 6/6 vs the "
        "pinned K2 source; freeze hashes re-verified vs PREREG_MARKER)",
        "PASS")
    add("G-CENSUS", "9.3.5 baseline reproduces K2 EXACTLY (rr 2,427 / "
        "var 2,093 / nofit 334 = 62+272; unknown-325 = 325 / 56 files / "
        "551564 x84; walk 10,274/6,167/65,050/143,874; row agreement "
        "6,167/6,167) AND the RUN A removals reproduce under "
        "re-execution (H5a 39 + H5c2 26 = 65; K2 lists identical) AND "
        "334 - 65 = 269 EXACT AND the frozen 269 == the census-derived "
        "269", "PASS")
    for g in ("W1", "W2", "W3"):
        v = verdicts[g]
        add("G-WIDE_" + g,
            "a-priori conjunction (frozen, never adjusted): full-269 "
            "fits >= 10 AND full-269 rate >= 5x matched-NC rate AND NC "
            "denominator > 0 AND held-out units >= 30 AND held-out fits "
            ">= 10 AND held-out rate >= 5x held-out-side matched-NC "
            "rate; exact binomial 95% CIs in WIDE_RESULTS.json",
            v["result"] + (" (" + v["non_pass_class"] + ")"
                           if v["non_pass_class"] else ""))
    n_fix = len(fixtures["fixtures"])
    n_fix_ok = sum(1 for f in fixtures["fixtures"]
                   if f["verdict"].get("result") == "NON_PASS"
                   and f["verdict"].get("non_pass_class"))
    add("G-EXEC", "per-record validation discipline (zero size-derived "
        "validation counts; self-audit in 01_RAW/SELF_AUDIT.txt) + "
        "%d/%d negative fixtures fail-closed" % (n_fix_ok, n_fix),
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
    ok_x, out_x = validate_manifest_rows(_buf0.getvalue().splitlines(),
                                         RUN)
    log("[rc] manifest pre-validation (in memory, %d rows): %s"
        % (out_x["ordinary_rows"], "PASS" if ok_x else "FAIL"))
    external = []
    for sid, path, era in (
            ("corpus_935", MODELS_935, "PCG_9_3_5"),
            ("K2_driver", K2_DRIVER, "PCG_9_3_5"),
            ("K2_NOFIT334_SPANS", K2_PINS["K2_NOFIT334_SPANS"][0],
             "PCG_9_3_5"),
            ("K2_HYPOTHESIS_RESULTS", K2_PINS["K2_HYPOTHESIS_RESULTS"][0],
             "PCG_9_3_5"),
            ("K2_BASELINE_REPRODUCTION",
             K2_PINS["K2_BASELINE_REPRODUCTION"][0], "PCG_9_3_5"),
            ("K2_COVERAGE_STATE", K2_PINS["K2_COVERAGE_STATE"][0],
             "PCG_9_3_5"),
            ("RUNA_driver", K2_PINS["RUNA_driver"][0], "PCG_9_3_5"),
            ("RUNA_RETRO_SPAN_OUTCOMES", RUNA_RETRO, "PCG_9_3_5"),
            ("RUNA_artifact_index", RUNA_MANIFEST, "PCG_9_3_5"),
            ("R34_REAL_SPARSE_GRAMMAR", R34_RSG, "PCG_9_3_5"),
            ("R61_SHA_MANIFEST", R61_SHA_JSON, "PCG_9_3_5"),
            ("MANIFEST_SCHEMA_SPEC", MANIFEST_SPEC, "PCG_9_3_5")):
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
        log("[rc] G-SCOPE pre-validation findings: "
            + json.dumps(out_x["findings"][:6]))
    wr_lines(os.path.join(RUN, "STAGE_ACCEPTANCE_GATES.csv"),
             ["# " + STANDING, "gate,description,status"] +
             ['"%s","%s","%s"' % (gates[k]["gate"],
                                  gates[k]["description"].replace(
                                      '"', "'"),
                                  gates[k]["status"])
              for k in ("G-PINS", "G-CENSUS", "G-WIDE_W1", "G-WIDE_W2",
                        "G-WIDE_W3", "G-EXEC", "G-SCOPE")])

    # ---- 06_REPORT: 00_FINAL_REPORT.md (the s15 20-point contract) ----
    p0_ans = []
    for g in ("W1", "W2", "W3"):
        v = verdicts[g]
        p0_ans.append("%s=%s%s" % (g, v["result"],
                                   (" " + v["non_pass_class"])
                                   if v["non_pass_class"] else ""))
    x = cov["real_record_coverage"]["this_run_additions"]["X_spans"]
    handoff = [
        "AUDIT_OUTPUT_ROOT = " + RUN,
        "FINAL_REPORT_PATH = " + os.path.join(REPT, "00_FINAL_REPORT.md"),
        "PRIMARY_EVIDENCE_PATHS = " + "; ".join([
            os.path.join(ANA, "WIDE_RESULTS.json"),
            os.path.join(ANA, "COVERAGE_DELTA.json"),
            os.path.join(ANA, "BASELINE_CENSUS_REPRODUCTION.json"),
            os.path.join(CTRL, "PIN_RESULTS.json"),
            os.path.join(CTRL, "POPULATION_269.json"),
            os.path.join(CTRL, "SPLIT_SIDES_269.json"),
            os.path.join(RAW, "WIDE_SPAN_OUTCOMES.jsonl"),
            os.path.join(RAW, "WIDE_NC_TRIALS.jsonl"),
            os.path.join(RAW, "NEGATIVE_FIXTURES_GEXEC.json")]),
        "RUN_STATUS = COMPLETED",
        "HARD_STOP_REASON = NONE",
    ]
    L = []
    L.append("# FINAL REPORT - PE_NIF_MORPH_WIDERECORD_R1_20260906_170000 "
             "(RUN C)")
    L.append("")
    L.append("## 1. HUMAN-FIRST (what needs the human NOW)")
    L.append("")
    L.append("Nothing is required from the human inside this run. "
             "PE-MASTER owns the post-run 5-layer audit and the "
             "publication decision (NO commit was made by the executor). "
             "The residual-325 stays OUT OF SCOPE / mechanism-unexplained; "
             "no H7-based claims are made anywhere in this package.")
    L.append("")
    L.append("## 2. IDENTITY")
    L.append("")
    L.append("RUN_ID: PE_NIF_MORPH_WIDERECORD_R1_20260906_170000 | "
             "RUN_CLASS: LOAD_BEARING | milestone: EU935-M1 (NO crossing) "
             "| date: %s | executor: pe-reconstruction | parent: PE-MASTER "
             "loop bd17344b iteration 3 | era: PCG_9_3_5 primary | "
             "BASE_SHA 461098f534497113f85157b946cdae5f0331bfdc (no repo "
             "writes by the executor)" % time.strftime("%Y-%m-%d"))
    L.append("")
    L.append("## 3. STATE DELTA (before -> after)")
    L.append("")
    L.append("BEFORE: 269 of the 334 no-fit rr spans remained unconsumed "
             "after RUN A (the +65 H5a/H5c2 RETROSPECTIVE_VALIDATED "
             "removals); W1/W2/W3 existed only as the K2 post-hoc probe's "
             "NON-COVERAGE candidates. AFTER: the three grammars executed "
             "per-record on the frozen 269 population with "
             "denominator-matched wrong-start NCs and a seeded "
             "file-grouped 50/50 split, under the a-priori G-WIDE "
             "conjunction. Gate results: " + "; ".join(p0_ans)
             + ". Coverage delta: X=%d -> real-record coverage %s; "
             "remaining no-fit %d."
             % (x, cov["real_record_coverage"]["new_total_str"],
                cov["real_record_coverage"]["remaining_nofit"]))
    L.append("")
    L.append("## 4/12. EXACT VERDICT + ONE P0")
    L.append("")
    L.append("RUN verdict: COMPLETED (all contract outputs produced; no "
             "HARD STOP). ONE P0: 'Do the pre-registered wide-record "
             "grammars W1/W2/W3 consume the 269 remaining 9.3.5 no-fit "
             "morph spans byte-exactly, at rates separated >= 5x from "
             "denominator-matched wrong-start negative controls, with "
             "per-record validation and file-grouped retrospective "
             "homogeneity?' ANSWER (per grammar, a-priori G-WIDE "
             "conjunction): " + "; ".join(p0_ans) + ".")
    for g in ("W1", "W2", "W3"):
        v = verdicts[g]
        r = results["grammars"][g]
        hb = r["held_out_side_B"]
        L.append("")
        L.append("- G-WIDE %s: %s%s | full-269 fits=%s/%s rate=%s CI95=%s | "
                 "full NC %s/%s rate=%s CI95=%s | held-out units=%s "
                 "unit-fits=%s unit-rate=%s CI95=%s | held-out NC %s/%s "
                 "rate=%s CI95=%s | detail=%s"
                 % (g, v["result"],
                    (" " + v["non_pass_class"]) if v["non_pass_class"]
                    else "",
                    r["full_269"]["fits"], r["full_269"]["members"],
                    r["full_269"]["rate"],
                    r["full_269"]["rate_ci95_exact_binomial"],
                    r["full_nc"]["hits"], r["full_nc"]["denominator"],
                    r["full_nc"]["rate"],
                    r["full_nc"]["rate_ci95_exact_binomial"],
                    hb["units"], hb["unit_fits"], hb["unit_rate"],
                    hb["unit_rate_ci95_exact_binomial"],
                    r["held_out_nc"]["hits"],
                    r["held_out_nc"]["denominator"],
                    r["held_out_nc"]["rate"],
                    r["held_out_nc"]["rate_ci95_exact_binomial"],
                    json.dumps(v.get("detail", {}))))
    L.append("")
    L.append("## 5/6. CLAIM -> EVIDENCE + DENOMINATORS")
    L.append("")
    L.append("Every rate carries numerator/denominator and an exact "
             "binomial (Clopper-Pearson) 95% CI. Machine evidence: "
             "05_ANALYSIS/WIDE_RESULTS.json (per-grammar gates, CIs, "
             "overlaps, consumed keys), 05_ANALYSIS/COVERAGE_DELTA.json "
             "(the machine-readable coverage state), 01_RAW/"
             "WIDE_SPAN_OUTCOMES.jsonl (per-record outcomes: span ID, "
             "side, grammar, outcome, rejection reason, bytes consumed; "
             "the full 269, both sides), 01_RAW/WIDE_NC_TRIALS.jsonl "
             "(every NC trial with its explicit denominator: spans_x_2 = "
             "269x2 = 538 per grammar; units_x_2 for the held-out side), "
             "BASELINE_CENSUS_REPRODUCTION.json, NEGATIVE_FIXTURES_"
             "GEXEC.json, MANIFEST_NEGATIVE_TESTS.json. All fit/NC counts "
             "are counter increments over executed records (G-EXEC "
             "discipline; self-audit in 01_RAW/SELF_AUDIT.txt with the "
             "full len() census).")
    L.append("")
    L.append("## 7/8. OPEN ITEMS + COVERAGE HONESTY (NOT checked)")
    L.append("")
    L.append("- RUNTIME_SEMANTICS is explicitly NOT_TESTED here (out of "
             "scope). No semantic claims; no H7-based claims; the "
             "residual-325 population is OUT OF SCOPE (stays "
             "mechanism-unexplained; a diagnostic note only).")
    L.append("- The 269 leg is RETROSPECTIVE by construction (W1/W2/W3 "
             "were formulated from the K2 post-hoc probe of the same "
             "population family); explicitly NOT 'unseen' evidence.")
    L.append("- NOT checked: H5a/H5c1/H5c2/H7 re-testing (RUN A owns "
             "them), the 2003-era corpus, g1/g2/mscan m != 32, k-ranges "
             "beyond 24, Wm windows beyond +/-64/step 4, any POST-HOC "
             "probe (none executed; any would be NON-COVERAGE).")
    L.append("- Coverage honesty: X counts ONLY spans consumed by "
             "grammars whose G-WIDE verdict is PASS (frozen decision d5; "
             "the K2 OC-rejection precedent); consumed spans of non-pass "
             "grammars are recorded in WIDE_RESULTS.json but EXCLUDED "
             "from every coverage number.")
    L.append("")
    L.append("## 9/10. RETRACTIONS + CHAIN OF CUSTODY")
    L.append("")
    L.append("No retraction from this run. The +65 status = "
             "RETROSPECTIVE_VALIDATED (RUN A); the K2 post-hoc probe "
             "findings (m=32 wide records; k~23) were NON-COVERAGE lesson "
             "candidates - this run is their pre-registered test. "
             "Originals (corpus, R61, K2, RUN A, R34) READ-ONLY, verified "
             "by pins; the K2 artifact_index.csv is DEFECTIVE and was "
             "never used as a hash source (every K2 artifact re-hashed "
             "from bytes).")
    L.append("")
    L.append("## 11. PUSH DISCIPLINE")
    L.append("")
    L.append("No commit, no push (per contract). BASE_SHA 461098f... "
             "unchanged by this run (no repo writes).")
    L.append("")
    L.append("## 13. NEGATIVE CONTROLS")
    L.append("")
    L.append("- NC-A: per-span wrong-start trials u+2/u-2 (2 per span; "
             "denominator spans x 2 = 538 per grammar), the SAME grammar "
             "at the wrong start (W3's NC shifts the whole frozen "
             "window). NC-B: held-out-side unit representatives x 2 "
             "(denominator units x 2). Rate-vs-rate comparisons only. "
             "The vacuous case 0 >= 5x0 cannot pass (NC_EMPTY_DENOMINATOR "
             "/ ZERO_FITS fail-closed ordering).")
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
             "pin mismatch / census mismatch / write-outside / population "
             "mismatch.)")
    L.append("")
    L.append("## 15. NEXT STEP + GATES (PE-MASTER decision)")
    L.append("")
    L.append("Proposed next: PE-MASTER post-run audit of this package "
             "(verdict persistence + publication decision). Gate needs: "
             "nothing from the human; no human-gated action inside this "
             "run.")
    L.append("")
    L.append("## 16. UNKNOWN STAYS UNKNOWN")
    L.append("")
    L.append("No semantic claims anywhere in this package; the class "
             "-256/field1 semantics remain unknown; RUNTIME_SEMANTICS "
             "not tested; the counts recorded above are the only "
             "quantitative claims.")
    L.append("")
    L.append("## 17. PAYLOAD DISCIPLINE")
    L.append("")
    L.append("Zero proprietary payloads in this package: outputs carry "
             "identifiers, outcomes, rejection reasons and byte COUNTS "
             "only (no payload bytes, no hex dumps). Originals appear as "
             "identity metadata (SHA-256 + paths) in artifact_index.csv "
             "external-sources section.")
    L.append("")
    L.append("## 18. DERIVED-NUMBER PROVENANCE")
    L.append("")
    L.append("Generator: 00_CONTROL/widerecord_driver_r1.py sha256 %s "
             "(this file). Grammar execution = IMPORT of the pinned K2 "
             "module (sha256 %s); WIDE_GRAMMARS.md blocks byte-verified "
             "against the pinned source (6/6). Census = the K2 stage-1 "
             "replica (G-CENSUS PASS, row agreement 6,167/6,167)."
             % (pin_results.get("driver_sha256"),
                K2_PINS["K2_driver"][1]))
    L.append("")
    L.append("## 19. HANDOFF BLOCK (copyable)")
    L.append("")
    L.extend(handoff)
    L.append("")
    L.append("## 20. SELF-CONTAINED NOTES")
    L.append("")
    L.append("Population: the 269 = the 334 K2 no-fit keys minus the "
             "union of RUN A's H5a (39) + H5c2 (26) FIT keys; 334 - 65 = "
             "269 EXACT (frozen in 00_CONTROL/POPULATION_269.json BEFORE "
             "any test; re-derived in-driver from the census + "
             "re-executed RUN A removals). Split: seeded "
             "Random(20260906) file-level 50/50 over %d files (side A %d "
             "/ side B %d; spans %d/%d; family integrity; both side "
             "lists frozen BEFORE testing). Gates a-priori in "
             "00_CONTROL/GATES_PREREGISTERED.md (never adjusted). "
             "Consumed spans carry RETROSPECTIVE_VALIDATION (the RUN A "
             "standard - explicitly retrospective, NOT unseen)."
             % (split["n_files"], len(split["side_A_files"]),
                len(split["side_B_files"]), len(split["pop269_side_A"]),
                len(split["pop269_side_B"])))
    L.append("")
    L.append(STANDING)
    L.append("")
    wr_lines(os.path.join(REPT, "00_FINAL_REPORT.md"), L)
    wr_lines(os.path.join(REPT, "HANDOFF.md"),
             ["# HANDOFF - PE_NIF_MORPH_WIDERECORD_R1_20260906_170000",
              ""] + handoff + ["", STANDING])

    # ---- final manifest: written AFTER every other package file is final
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
            "05_ANALYSIS/MANIFEST_VALIDATION.json (circular: records the "
            "validation of this manifest; written last)"],
        "pre_validation_in_memory": {
            "gate_pass": bool(ok_x),
            "ordinary_rows": out_x["ordinary_rows"],
            "note": ("executed BEFORE the final gates CSV write; the "
                     "gates CSV row was added afterwards with the hash "
                     "of its final on-disk bytes")},
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
    log("[rc] manifest: %d ordinary + %d external rows; post-write "
        "validation PASS; MANIFEST_VALIDATION.json written last"
        % (man_out["ordinary_rows"], man_out["external_rows"]))
    log("[rc] DONE in %.1fs" % (time.time() - T0))
    log("[rc] gates: " + json.dumps(
        {k: v["status"] for k, v in gates.items()}))


def main():
    log("[rc] RUN C: PE_NIF_MORPH_WIDERECORD_R1_20260906_170000")
    corp = stage0_pins()
    data935, ent935 = corp["data935"], corp["ent935"]
    sys.path.insert(0, R61_SOURCE_DIR)
    from pe_nif_reader import PENifReader  # noqa: E402
    sys.path.insert(0, K2_CTRL)
    import morph_residual_deepdive_r1 as K2  # noqa: E402
    globals()["K2"] = K2
    globals()["PENifReader"] = PENifReader

    pop269, side_of, split = s1_census(ent935, data935)
    (members, nc_full, nc_unit, consumed, unit_side, unit_members,
     unit_split) = s3_tests(pop269, side_of)
    results, verdicts, cov = s4_results(
        members, nc_full, nc_unit, consumed, unit_side, unit_members,
        unit_split, split)
    gexec_pass, fixtures, audit = s5_gexec()
    with open(os.path.join(CTRL, "PIN_RESULTS.json"),
              encoding="utf-8") as f:
        pin_results = json.load(f)
    s6_outputs(results, verdicts, cov, gexec_pass, fixtures, audit,
               split, pin_results)
    log("[rc] RUN C COMPLETE. Log lines: %d" % len(LOG_LINES))


if __name__ == "__main__":
    main()
