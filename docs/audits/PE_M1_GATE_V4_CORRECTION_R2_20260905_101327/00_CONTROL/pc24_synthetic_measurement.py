#!/usr/bin/env python3
# -*- coding: ascii -*-
# pc24_synthetic_measurement.py - WORK ITEM: the PC24 SYNTHETIC RE-MEASUREMENT
# (PE_M1_GATE_V4_CORRECTION_R2_20260905_101327, NEXT_PROMPT W10).
#
# WHY THIS EXISTS: the frozen domain_reproof.json (validator-coverage repair run)
# records lerp_scale_synthetic.lerp_pc24_mismatches = 0, but repair_02_domain.py
# ran the synthetic domain with measure_pc24=False - the field is a DEFAULT
# COUNTER, NOT a measurement (HYG-1; CORRECTION_NOTES.md). The PE-MASTER
# post-audit measured the actual value auditor-side: 103,073/1,245,184.
# THIS script re-measures it RUN-SIDE (the double measurement) and sets the
# disposition: 103,073 -> CONFIRMED; != -> RETRACT + replace (LOUD); input SHA
# mismatch -> infeasible -> HARD STOP. The frozen 0 in domain_reproof.json is
# NEVER touched (disposed as HYGIENE-1, supersession-typed records only).
#
# METHOD (verbatim from the pinned records; NOTHING re-derived):
#   - the 38 synthetic pairs are READ from the FROZEN domain_reproof.json
#     (SHA-locked E654D2EF...; mismatch -> exit 3 = HARD STOP, no output);
#   - the PC-mode method from oracle_battery.json pcrc_conditional_model:
#     PC=24 -> f32(x) directly; PC=53 -> f32(f64(x)) (lerp_js); the engine
#     model = the 80-bit x87 chain with per-step exactness ENFORCED;
#   - the lerp semantics + the PC24 model are EXACTLY repair_02_domain.py's
#     lerp_engine / lerp_pc24 / lerp_js (measure_pc24=True semantics), with the
#     IEEE rounders VERBATIM from repair_lib_ieee.py (SHA256
#     1BF5B1C8A94D4D96FF9065B477CEDB3E2A9C81AB42537AB35A60F95195782D28);
#   - an INT fast path replaces Fraction in the hot loop; its result-identity
#     vs the VERBATIM Fraction path is ASSERTED on 2000 samples (fail-loud),
#     the same equivalence-guard pattern the repair run itself used.
#
# CONTROLS (fail-closed):
#   (NC1) the REAL domain (7 pairs from the same frozen file) is re-measured:
#         lerp_pc24_mismatches MUST equal 14,104 (the frozen measured value
#         AND the PE-MASTER independent confirmation). != -> INSTRUMENT_INVALID
#         -> exit 4 = HARD STOP (the gate is not provably fail-closed).
#   (NC2) the rand01 (32768) + positions (65536) engine-vs-PC24 domains: MUST
#         equal 0 (frozen measured values).
#   (NC3) engine-vs-js (PC=53) on BOTH domains: MUST equal 0 (frozen measured).
#   (NC4) the two pairs shared by the real + synthetic sets ((0.5,1.0) and
#         (0.5,2.0)) MUST produce IDENTICAL per-pair counts in both runs
#         (same inputs + same method -> same count; a method divergence
#         between the two loops would betray itself here).
import hashlib
import json
import os
import sys
from fractions import Fraction

RUN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(RUN_ROOT, "01_RAW", "pc24_synthetic_measurement.json")

DOMAIN_REPROOF = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\01_RAW\domain_reproof.json"
DOMAIN_REPROOF_SHA = "E654D2EF34BFF061FACF18794BE2F6A036B8BEFD847ED9308C0990F1795DEC3E"
ORACLE_BATTERY = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\01_RAW\oracle_battery.json"
ORACLE_BATTERY_SHA = "B04A3175F9E32669795D115271525E344AB823A8071171498845459D267DBFCE"
IEEE_LIB_SOURCE = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\00_CONTROL\repair_lib_ieee.py"
IEEE_LIB_SHA = "1BF5B1C8A94D4D96FF9065B477CEDB3E2A9C81AB42537AB35A60F95195782D28"

EXPECTED_REAL_PC24 = 14104          # frozen domain_reproof lerp_scale_real.lerp_pc24_mismatches
EXPECTED_SYNTH_PE_MASTER = 103073   # PE-MASTER_REVIEW.md CODE_FINDING 1 (auditor-side)
N_R = 32768

F = Fraction


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


# ================================================================ VERBATIM IEEE rounders
# copied VERBATIM from repair_lib_ieee.py (read-only evidence of the repair
# run; SHA-locked above). The sign/subnormal/overflow semantics are preserved
# exactly; our domain (values in [0.2, 9] + quotients in [0,1]) never leaves
# the normal band, but the code is the proven library, not a rewrite.

def _canon(q, e):
    if q == 0:
        return (0, 0)
    while not (q & 1):
        q >>= 1
        e -= 1
    return (q, e)


def _round_half_even_div(n, d):
    q, r = divmod(n, d)
    r2 = r << 1
    if r2 > d or (r2 == d and (q & 1)):
        q += 1
    return q


def _round_ieee(num, den, mant_bits, min_exp, sub_scale):
    if den <= 0:
        raise ValueError("den must be > 0")
    if num == 0:
        return (0, 0)
    sign = -1 if num < 0 else 1
    if num < 0:
        num = -num
    if num * (1 << (-min_exp)) < den:
        m = _round_half_even_div(num << sub_scale, den)
        if m == 0 and sign < 0:
            raise ValueError("negative input rounds to zero - outside domain")
        return _canon(sign * m, sub_scale)
    e = den.bit_length() + (mant_bits - 1) - num.bit_length()
    while True:
        if e >= 0:
            N, D = num << e, den
        else:
            N, D = num, den << (-e)
        if N < (D << (mant_bits - 1)):
            e += 1
        elif N >= (D << mant_bits):
            e -= 1
        else:
            break
    q = _round_half_even_div(N, D)
    if q == (1 << mant_bits):
        q >>= 1
        e -= 1
    res_exp = (mant_bits - 1) - e
    if res_exp > (-min_exp + 1):
        raise ValueError("input outside the finite binary domain")
    return _canon(sign * q, e)


def to_f32_nd(num, den):
    return _round_ieee(num, den, 24, -126, 149)


def to_f64_nd(num, den):
    return _round_ieee(num, den, 53, -1022, 1074)


def to_f80_nd(num, den):
    return _round_ieee(num, den, 64, -16382, 16445)


def _canon_to_fraction(q, e):
    if e > 0:
        return Fraction(q, 1 << e)
    if e < 0:
        return Fraction(q << (-e), 1)
    return Fraction(q)


# ================================================================ the VERBATIM models (Fraction path)
# exactly repair_02_domain.py's lerp_engine / lerp_pc24 / lerp_js, kept as the
# equivalence reference for the int fast path below.

def lerp_engine_v(a, mn32, d):
    p = a * d
    s = p + mn32
    qe = to_f80_nd(s.numerator, s.denominator)
    exact80 = _canon_to_fraction(*qe) == s
    return _canon_to_fraction(*to_f32_nd(s.numerator, s.denominator)), exact80


def lerp_pc24_v(a, mn32, d):
    d24 = _canon_to_fraction(*to_f32_nd(d.numerator, d.denominator))
    p24 = _canon_to_fraction(*to_f32_nd((a * d24).numerator, (a * d24).denominator))
    return _canon_to_fraction(*to_f32_nd((p24 + mn32).numerator, (p24 + mn32).denominator))


def lerp_js_v(a, mn32, d):
    p64 = _canon_to_fraction(*to_f64_nd((a * d).numerator, (a * d).denominator))
    s64 = _canon_to_fraction(*to_f64_nd((p64 + mn32).numerator, (p64 + mn32).denominator))
    return _canon_to_fraction(*to_f32_nd(s64.numerator, s64.denominator))


# ================================================================ the INT fast path
# exact rational arithmetic on (num, exp) with value = num * 2^-exp; the
# rounders are the VERBATIM to_*_nd above. Result-identity vs the verbatim
# Fraction path is ASSERTED on 2000 samples before any counting.

def _mul(x, y):
    return (x[0] * y[0], x[1] + y[1])


def _add(x, y):
    e = x[1] if x[1] >= y[1] else y[1]
    return ((x[0] << (e - x[1])) + (y[0] << (e - y[1])), e)


def _sub(x, y):
    e = x[1] if x[1] >= y[1] else y[1]
    return ((x[0] << (e - x[1])) - (y[0] << (e - y[1])), e)


def _norm(num, exp):
    # value = num * 2^-exp; den = 2^exp (exp >= 0 in this domain)
    if exp < 0:
        return (num << (-exp), 0)
    return (num, exp)


def lerp_engine_i(a, mn32, d):
    p = _mul(a, d)
    s = _add(p, mn32)
    sn, se = _norm(s[0], s[1])
    if sn == 0:
        return (0, 0), True
    q = sn
    tz = (q & -q).bit_length() - 1
    q >>= tz
    exact80 = q.bit_length() <= 64          # f80-exact for normal-range values
    return to_f32_nd(sn, 1 << se), exact80


def lerp_pc24_i(a, mn32, d):
    dn, de = _norm(d[0], d[1])
    d24 = to_f32_nd(dn, 1 << de)
    pn = a[0] * d24[0]
    pe = a[1] + d24[1]
    if pe < 0:
        pn <<= (-pe)
        pe = 0
    p24 = to_f32_nd(pn, 1 << pe)
    s24 = _add((p24[0], p24[1]), mn32)
    sn, se = _norm(s24[0], s24[1])
    return to_f32_nd(sn, 1 << se)


def lerp_js_i(a, mn32, d):
    p = _mul(a, d)
    pn, pe = _norm(p[0], p[1])
    p64 = to_f64_nd(pn, 1 << pe)
    s = _add((p64[0], p64[1]), mn32)
    sn, se = _norm(s[0], s[1])
    return to_f32_nd(sn, 1 << se)


def frac_to_tuple(fr):
    q, e = to_f32_nd(fr.numerator, fr.denominator)
    return (q, e)


# ================================================================ main

def main():
    # ---- input verification (fail-closed; mismatch -> HARD STOP, no output)
    dr_sha = sha256_file(DOMAIN_REPROOF)
    ob_sha = sha256_file(ORACLE_BATTERY)
    lib_sha = sha256_file(IEEE_LIB_SOURCE)
    if dr_sha != DOMAIN_REPROOF_SHA or ob_sha != ORACLE_BATTERY_SHA:
        print("HARD STOP: input SHA mismatch (infeasible re-measurement).")
        print("  domain_reproof.json pinned=%s actual=%s" % (DOMAIN_REPROOF_SHA, dr_sha))
        print("  oracle_battery.json  pinned=%s actual=%s" % (ORACLE_BATTERY_SHA, ob_sha))
        return 3
    if lib_sha != IEEE_LIB_SHA:
        print("HARD STOP: repair_lib_ieee.py SHA mismatch (the verbatim source).")
        return 3
    with open(DOMAIN_REPROOF, "r", encoding="ascii") as f:
        dr = json.load(f)
    pairs_synth = [tuple(p) for p in dr["sets"]["synthetic_pairs_old_script"]]
    pairs_real = [tuple(p) for p in dr["sets"]["source_pairs_original_vcl"]]
    assert len(pairs_synth) == 38 and len(pairs_real) == 7, "frozen set sizes wrong"
    assert dr["domains"]["lerp_scale_synthetic"]["n_pairs"] == 38
    assert dr["domains"]["lerp_scale_real"]["lerp_checks"] == 229376

    # ---- rand01 / positions precompute (engine / js / pc24; tuple canonical)
    a_eng = [None] * N_R
    a_js = [None] * N_R
    a_pc24 = [None] * N_R
    rand_eng_vs_js = 0
    rand_eng_vs_pc24 = 0
    for r in range(N_R):
        if r == 0:
            a_eng[r] = a_js[r] = a_pc24[r] = (0, 0)
            continue
        q80 = to_f80_nd(r, 32767)
        a_eng[r] = to_f32_nd(q80[0], 1 << q80[1])
        q64 = to_f64_nd(r, 32767)
        a_js[r] = to_f32_nd(q64[0], 1 << q64[1])
        a_pc24[r] = to_f32_nd(r, 32767)
        if a_eng[r] != a_js[r]:
            rand_eng_vs_js += 1
        if a_eng[r] != a_pc24[r]:
            rand_eng_vs_pc24 += 1
    pos_eng_vs_js = 0
    pos_eng_vs_pc24 = 0
    for u in range(1, 65536):
        q80 = to_f80_nd(u, 65535)
        pe = to_f32_nd(q80[0], 1 << q80[1])
        q64 = to_f64_nd(u, 65535)
        pj = to_f32_nd(q64[0], 1 << q64[1])
        p24 = to_f32_nd(u, 65535)
        if pe != pj:
            pos_eng_vs_js += 1
        if pe != p24:
            pos_eng_vs_pc24 += 1

    # ---- equivalence assertion: int path == verbatim Fraction path (2000 samples)
    import random as _rnd
    _rnd.seed(20260905)
    checked = 0
    for mn_f, mx_f in [(0.25, 1.0), (0.5, 1.5), (0.2, 0.6), (0.8, 1.5), (0.5, 1.55), (3.0, 6.0)]:
        mn32v = _canon_to_fraction(*to_f32_nd(F(mn_f).numerator, F(mn_f).denominator))
        mx32v = _canon_to_fraction(*to_f32_nd(F(mx_f).numerator, F(mx_f).denominator))
        d_v = mx32v - mn32v
        mn_t = frac_to_tuple(mn32v)
        mx_t = frac_to_tuple(mx32v)
        d_t = _sub(mx_t, mn_t)
        for _ in range(333):
            r = _rnd.randint(0, 32767)
            ae_f = _canon_to_fraction(*a_eng[r])
            a24_f = _canon_to_fraction(*a_pc24[r])
            aj_f = _canon_to_fraction(*a_js[r])
            ve_f, ex80v = lerp_engine_v(ae_f, mn32v, d_v)
            ve_t, ex80t = lerp_engine_i(a_eng[r], mn_t, d_t)
            assert ve_t == frac_to_tuple(ve_f), "int-path engine diverges at r=%d" % r
            assert ex80t == ex80v, "int-path exact80 diverges at r=%d" % r
            v24_f = lerp_pc24_v(a24_f, mn32v, d_v)
            assert lerp_pc24_i(a_pc24[r], mn_t, d_t) == frac_to_tuple(v24_f), "int-path pc24 diverges"
            vjs_f = lerp_js_v(aj_f, mn32v, d_v)
            assert lerp_js_i(a_js[r], mn_t, d_t) == frac_to_tuple(vjs_f), "int-path js diverges"
            checked += 1
    print("int-path equivalence vs verbatim Fraction path: %d/%d samples OK" % (checked, checked))

    # ---- the domain runner (measure_pc24=True semantics; per-pair counts)
    def run_domain(pairs, tag):
        per_pair = []
        tot_pc24 = tot_js = tot_x80 = 0
        for (mn_f, mx_f) in pairs:
            mn_t = frac_to_tuple(_canon_to_fraction(*to_f32_nd(F(mn_f).numerator, F(mn_f).denominator)))
            mx_t = frac_to_tuple(_canon_to_fraction(*to_f32_nd(F(mx_f).numerator, F(mx_f).denominator)))
            d_t = _sub(mx_t, mn_t)
            c24 = cjs = cx80 = 0
            for r in range(N_R):
                a_e = a_eng[r]
                v_eng, ex80 = lerp_engine_i(a_e, mn_t, d_t)
                if not ex80:
                    cx80 += 1
                v24 = lerp_pc24_i(a_pc24[r], mn_t, d_t)
                if v_eng != v24:
                    c24 += 1
                v_js = lerp_js_i(a_js[r], mn_t, d_t)
                if v_eng != v_js:
                    cjs += 1
            per_pair.append({"pair": [mn_f, mx_f], "checks": N_R,
                             "pc24_mismatches": c24, "engine_vs_js_mismatches": cjs,
                             "engine_80bit_inexact": cx80})
            tot_pc24 += c24
            tot_js += cjs
            tot_x80 += cx80
            print("  %s pair (%s, %s): pc24=%d eng-vs-js=%d x80viol=%d"
                  % (tag, mn_f, mx_f, c24, cjs, cx80))
        return {"tag": tag, "n_pairs": len(pairs), "checks": len(pairs) * N_R,
                "lerp_pc24_mismatches": tot_pc24,
                "lerp_engine_vs_js_mismatches": tot_js,
                "lerp_80bit_inexact": tot_x80,
                "per_pair": per_pair}

    print("measuring the REAL domain (7 frozen pairs; the negative-control anchor)...")
    dom_real = run_domain(pairs_real, "REAL")
    print("measuring the SYNTHETIC domain (38 frozen pairs x 32768 = 1,245,184)...")
    dom_synth = run_domain(pairs_synth, "SYNTH")

    # ---- controls NC1..NC4 (fail-closed)
    controls = {
        "NC1_real_domain_pc24_equals_frozen_14104": {
            "measured": dom_real["lerp_pc24_mismatches"], "expected": EXPECTED_REAL_PC24,
            "pass": dom_real["lerp_pc24_mismatches"] == EXPECTED_REAL_PC24},
        "NC2_rand01_positions_pc24_zero": {
            "rand01_engine_vs_pc24": rand_eng_vs_pc24, "positions_engine_vs_pc24": pos_eng_vs_pc24,
            "expected": 0, "pass": rand_eng_vs_pc24 == 0 and pos_eng_vs_pc24 == 0},
        "NC3_engine_vs_js_zero_both_domains": {
            "rand01": rand_eng_vs_js, "positions": pos_eng_vs_js,
            "real": dom_real["lerp_engine_vs_js_mismatches"], "synthetic": dom_synth["lerp_engine_vs_js_mismatches"],
            "expected": 0,
            "pass": (rand_eng_vs_js == 0 and pos_eng_vs_js == 0
                     and dom_real["lerp_engine_vs_js_mismatches"] == 0
                     and dom_synth["lerp_engine_vs_js_mismatches"] == 0)},
        "NC4_shared_pairs_same_per_pair_count": {"shared": []},
        "NC5_80bit_exactness_zero_violations": {
            "real": dom_real["lerp_80bit_inexact"], "synthetic": dom_synth["lerp_80bit_inexact"],
            "expected": 0,
            "pass": dom_real["lerp_80bit_inexact"] == 0 and dom_synth["lerp_80bit_inexact"] == 0},
    }
    synth_by_pair = {(p["pair"][0], p["pair"][1]): p for p in dom_synth["per_pair"]}
    shared_ok = True
    for p in dom_real["per_pair"]:
        key = (p["pair"][0], p["pair"][1])
        if key in synth_by_pair:
            same = p["pc24_mismatches"] == synth_by_pair[key]["pc24_mismatches"]
            controls["NC4_shared_pairs_same_per_pair_count"]["shared"].append(
                {"pair": list(key), "real": p["pc24_mismatches"],
                 "synthetic": synth_by_pair[key]["pc24_mismatches"], "pass": same})
            if not same:
                shared_ok = False
    controls["NC4_shared_pairs_same_per_pair_count"]["pass"] = shared_ok
    all_controls_pass = all(v.get("pass") for v in controls.values())
    if not all_controls_pass:
        print("HARD STOP: a measurement control FAILED - the instrument is not")
        print("  provably fail-closed; no disposition is asserted. Controls:")
        print(json.dumps(controls, indent=1))
        return 4

    # ---- the disposition
    measured_total = dom_synth["lerp_pc24_mismatches"]
    if measured_total == EXPECTED_SYNTH_PE_MASTER:
        disposition = {
            "disposition": "CONFIRMED",
            "detail": ("the citation 103,073/1,245,184 is PROMOTED to CONFIRMED "
                       "(double measurement: PE-MASTER auditor-side + THIS run-side, "
                       "independent implementations, exact agreement)"),
        }
    else:
        disposition = {
            "disposition": "RETRACTED_AND_REPLACED",
            "detail": ("LOUD NOTE: the PE-MASTER auditor-side citation 103,073/1,245,184 "
                       "is RETRACTED in the V4 package and REPLACED by the run-side measured "
                       "value %d/%d (no silent substitution; the divergence is recorded, "
                       "the negative-control anchors all PASSED, so the instrument is "
                       "trusted and the auditor-side figure is not)" % (measured_total, 1245184)),
            "retracted_value": 103073,
            "measured_value": measured_total,
        }

    script_sha = sha256_file(os.path.abspath(__file__))
    result = {
        "run_id": "PE_M1_GATE_V4_CORRECTION_R2_20260905_101327",
        "work_item": "W10 - the PC24 SYNTHETIC RE-MEASUREMENT (a measurement without an artifact is not evidence)",
        "purpose": "run-side double measurement of the synthetic-domain lerp PC=24 sensitivity; the frozen lerp_pc24_mismatches=0 of domain_reproof.json is a DEFAULT COUNTER (measure_pc24=False, HYG-1) and is NEVER touched by this run",
        "method": {
            "pc_modes": "oracle_battery.json pcrc_conditional_model: PC=24 -> f32(x) directly; PC=53 -> f32(f64(x)); the engine model = the 80-bit x87 chain (per-step exactness ENFORCED); the lerp semantics = repair_02_domain.py lerp_engine/lerp_pc24/lerp_js verbatim (measure_pc24=True semantics)",
            "lerp_expression": "value = rand01 * (f32(max) - f32(min)) + f32(min); rand01 = f32(r / 32767.0) with r in [0, 32767]; rand01 engine = f32(f80(r/32767)), rand01 pc24 = f32(r/32767) (measured EQUAL on the full rand01 domain)",
            "lerp_pc24_model": "d24 = f32(max-min); p24 = f32(rand01*d24); result = f32(p24 + f32(min)) - repair_02_domain.py lerp_pc24 verbatim",
            "ieee_rounders_source": {
                "path": IEEE_LIB_SOURCE,
                "sha256": lib_sha,
                "note": "the rounders (_round_ieee/_canon/_round_half_even_div/to_f32_nd/to_f64_nd/to_f80_nd) are VERBATIM from the platform-validated repair library",
            },
            "int_fast_path_equivalence_assertion": {"samples": checked, "verdict": "OK (2000-assert style, fail-loud on any divergence)"},
            "comparison_definition": "lerp_pc24_mismatches = count(r, pair) where lerp_engine != lerp_pc24 (the engine-vs-PC24 sensitivity; engine==js measured 0 on all domains here, so PC53-vs-PC24 is the same count)",
        },
        "inputs": {
            "domain_reproof_json": {"path": DOMAIN_REPROOF, "sha256": dr_sha, "pinned": DOMAIN_REPROOF_SHA, "match": True},
            "oracle_battery_json": {"path": ORACLE_BATTERY, "sha256": ob_sha, "pinned": ORACLE_BATTERY_SHA, "match": True},
            "pairs_source": "READ from the FROZEN file (sets.synthetic_pairs_old_script = 38; sets.source_pairs_original_vcl = 7); never re-derived",
        },
        "script_sha256": script_sha,
        "domains": {
            "rand01_r_32767": {"checked": N_R, "engine_vs_pc24": rand_eng_vs_pc24, "engine_vs_js": rand_eng_vs_js},
            "positions_u16_65535": {"checked": 65536, "engine_vs_pc24": pos_eng_vs_pc24, "engine_vs_js": pos_eng_vs_js},
            "lerp_pc24_sensitivity_real": dom_real,
            "lerp_pc24_sensitivity_synthetic": dom_synth,
        },
        "total_synthetic_comparisons": dom_synth["checks"],
        "measured_synthetic_pc24_mismatches": measured_total,
        "auditor_side_citation": {"value": 103073, "source": "PE_MASTER_REVIEW.md CODE_FINDING 1 + CORRECTION_NOTES.md HYG-1"},
        "negative_controls": controls,
        "all_negative_controls_pass": all_controls_pass,
        "disposition": disposition,
        "hygiene_note": ("the frozen domain_reproof.json lerp_scale_synthetic.lerp_pc24_mismatches=0 stays UNTOUCHED "
                         "(HYGIENE-1: it is a default counter from measure_pc24=False, superseded as a READING by "
                         "CORRECTION_NOTES.md; THIS file is the run-side artifact the reading now points to)"),
        "failures": [],
        "verdict": "PASS",
    }
    with open(OUT_PATH, "w", encoding="ascii") as f:
        json.dump(result, f, indent=1)
        f.write("\n")
    print()
    print("PC24 SYNTHETIC RE-MEASUREMENT: measured %d / %d" % (measured_total, dom_synth["checks"]))
    print("  real-domain anchor: %d (expected %d) - PASS" % (dom_real["lerp_pc24_mismatches"], EXPECTED_REAL_PC24))
    print("  disposition: %s" % disposition["disposition"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
