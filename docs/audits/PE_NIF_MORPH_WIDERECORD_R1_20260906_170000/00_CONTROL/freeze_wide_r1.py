#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FREEZE script - RUN C PE_NIF_MORPH_WIDERECORD_R1_20260906_170000.

Writes EVERY Section-3 freeze artifact to 00_CONTROL BEFORE any test
execution (and before any corpus parse): the verbatim W1/W2/W3 grammar
definitions, the 269-population (334 minus the 65 RUN-A-validated keys),
the subtraction lists, the split side lists, the NC procedures, the
a-priori gates, and the PREREG_MARKER. No grammar predicate is executed
here; every population input is a pinned READ-ONLY artifact.

Standing sentence: no semantic claims; the +65 H5a/H5c2 status =
RETROSPECTIVE_VALIDATED (RUN A); the H7 join-mechanism = UNVALIDATED
(RUN A) - this run makes NO H7-based claims; the residual-325 population
is OUT OF SCOPE (stays mechanism-unexplained; a diagnostic note only, no
new claims). Result classes: BYTE_MATCH / REPEATABILITY /
RETROSPECTIVE_VALIDATION / RUNTIME_SEMANTICS (= explicitly NOT_TESTED
here, out of scope).
"""
import hashlib
import json
import os
import random
import time

RUN = (r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_"
       r"WIDERECORD_R1_20260906_170000")
CTRL = os.path.join(RUN, "00_CONTROL")
A = r"D:\Eudoria_Reconstruction\99_Audits"
K2_RUN = os.path.join(A, "PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209")
RUNA_RUN = os.path.join(A, "PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500")

PINS = {
    "K2_driver": (os.path.join(K2_RUN, "00_CONTROL", "morph_residual_deepdive_r1.py"),
                  "b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a"),
    "K2_NOFIT334_SPANS": (os.path.join(K2_RUN, "01_RAW", "NOFIT334_SPANS.txt"),
                          "8bb6556b166df656631af168031e58518b3147fe962d5815ca4e19009e0f605d"),
    "K2_COVERAGE_STATE": (os.path.join(K2_RUN, "05_ANALYSIS", "COVERAGE_STATE.json"),
                          "86c12fa7f3df1149213fbfdef3097f022bb7c7ba38dc2cf4289de4aab1b12fa4"),
    "K2_HYPOTHESIS_RESULTS": (os.path.join(K2_RUN, "05_ANALYSIS", "HYPOTHESIS_RESULTS.json"),
                              "c08fb4738ece9d1f2c9cbcb43fe05b866f7560b1808597abc78e70e6e438e4a9"),
    "K2_BASELINE_REPRODUCTION": (os.path.join(K2_RUN, "05_ANALYSIS", "BASELINE_REPRODUCTION.json"),
                                 "2e4014c9652df8adf6854b87c17388f9a5288c2c32dc757b34946320db46f1ca"),
    "RUNA_driver": (os.path.join(RUNA_RUN, "00_CONTROL", "revalidate_driver_r1.py"),
                    "02ecb955bc3796128ed3f3b99cc302df61649f9ac2202e83ee5860ed5de9dbe0"),
}

STANDING = ("Standing sentence: no semantic claims; the +65 H5a/H5c2 status "
            "= RETROSPECTIVE_VALIDATED (RUN A); the H7 join-mechanism = "
            "UNVALIDATED (RUN A) - this run makes NO H7-based claims; the "
            "residual-325 population is OUT OF SCOPE (stays mechanism-"
            "unexplained; a diagnostic note only, no new claims). Result "
            "classes: BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION "
            "/ RUNTIME_SEMANTICS (= explicitly NOT_TESTED here, out of "
            "scope).")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        while True:
            b = fh.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def wr_json(path, obj):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=1, ensure_ascii=True)
        f.write("\n")


def wr_lines(path, lines):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(x if x.endswith("\n") else x + "\n" for x in lines))


def verify_pins():
    for k, (p, exp) in PINS.items():
        got = sha256_file(p)
        if got.lower() != exp.lower():
            raise SystemExit("PIN MISMATCH %s: %s" % (k, got))
        print("pin OK: %s %s" % (k, got[:12]))
    # RUN A RETRO_SPAN_OUTCOMES.jsonl: pin taken from RUN A's
    # artifact_index.csv ORDINARY row (the K2 artifact_index is DEFECTIVE;
    # RUN A's manifest is the pinned row source; physical re-hash below).
    mani = os.path.join(RUNA_RUN, "artifact_index.csv")
    exp_row = None
    with open(mani, "r", encoding="utf-8", newline="") as f:
        for ln in f:
            if ln.startswith("01_RAW/RETRO_SPAN_OUTCOMES.jsonl,"):
                exp_row = ln.strip()
                break
    if exp_row is None:
        raise SystemExit("RUN A manifest row for RETRO_SPAN_OUTCOMES missing")
    sha_exp = exp_row.split(",")[-1]
    p_retro = os.path.join(RUNA_RUN, "01_RAW", "RETRO_SPAN_OUTCOMES.jsonl")
    got = sha256_file(p_retro)
    if got.lower() != sha_exp.lower():
        raise SystemExit("RUN A RETRO_SPAN_OUTCOMES hash mismatch vs manifest row")
    print("pin OK: RUNA_RETRO_SPAN_OUTCOMES (manifest row) %s" % got[:12])
    return {"RUNA_RETRO_SPAN_OUTCOMES": got, "RUNA_manifest_row": exp_row,
            "RUNA_artifact_index_sha256": sha256_file(mani)}


def parse_dump_headers(path):
    ids = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("== "):
                head = line[3:].split()
                ids.append((head[0], int(head[1].split("=")[1]),
                            int(head[2].split("=")[1])))
    return ids


def main():
    pinx = verify_pins()
    # ---- the 334 (pinned K2 dump headers) ----
    nf334 = sorted(parse_dump_headers(PINS["K2_NOFIT334_SPANS"][0]))
    if len(nf334) != 334:
        raise SystemExit("NOFIT334 dump header count != 334: %d" % len(nf334))
    # ---- the 65 RUN A removals (pinned RUN A per-record outcomes) ----
    h5a_fit = set()
    h5c2_fit = set()
    with open(os.path.join(RUNA_RUN, "01_RAW", "RETRO_SPAN_OUTCOMES.jsonl"),
              "r", encoding="utf-8") as f:
        for ln in f:
            r = json.loads(ln)
            k = tuple(r["span"])
            if r["grammar"] == "H5a" and r["outcome"] == "FIT":
                h5a_fit.add(k)
            elif r["grammar"] == "H5c2" and r["outcome"] == "FIT":
                h5c2_fit.add(k)
    if len(h5a_fit) != 39 or len(h5c2_fit) != 26:
        raise SystemExit("RUN A FIT key count mismatch: H5a=%d H5c2=%d"
                         % (len(h5a_fit), len(h5c2_fit)))
    union65 = h5a_fit | h5c2_fit
    if len(union65) != 65:
        raise SystemExit("union of RUN A removals != 65: %d" % len(union65))
    if not union65 <= set(nf334):
        raise SystemExit("RUN A removals not a subset of the 334")
    # ---- the 269 ----
    pop269 = sorted(k for k in nf334 if k not in union65)
    if len(pop269) != 269 or len(nf334) - len(union65) != 269:
        raise SystemExit("334 - 65 != 269 EXACT check failed")
    print("population freeze: 334 - %d = %d" % (len(union65), len(pop269)))

    # ---- split: file-level 50/50, seeded, family integrity ----
    files269 = sorted(set(k[0] for k in pop269))
    rng = random.Random(20260906)
    shuffled = list(files269)
    rng.shuffle(shuffled)
    n = len(shuffled)
    sideA = shuffled[:n // 2]
    sideB = shuffled[n // 2:]
    side_of = {}
    for f in sideA:
        side_of[f] = "A"
    for f in sideB:
        side_of[f] = "B"

    # ---- WIDE_GRAMMARS.md (verbatim K2 blocks, byte-verified) ----
    with open(PINS["K2_driver"][0], "r", encoding="utf-8", newline="") as f:
        k2_src = f.read().split("\n")
    blocks = [("B1_constants", 79, 83), ("B2_H4_WIN", 86, 86),
              ("B3_clean", 100, 103), ("B4_parse_fixed", 251, 285),
              ("B5_parse_variable", 288, 320), ("B6_nc2", 871, 882)]
    md = [
        "# WIDE_GRAMMARS.md - VERBATIM grammar freeze "
        "(PE_NIF_MORPH_WIDERECORD_R1_20260906_170000)", "",
        "Source of every block below: the PINNED K2 driver "
        "`00_CONTROL/morph_residual_deepdive_r1.py` of "
        "PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209, SHA256 "
        "b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a "
        "(re-hashed at freeze time; the K2 artifact_index.csv is DEFECTIVE "
        "and was NOT used as a hash source - every K2 artifact was re-hashed "
        "directly from bytes).", "",
        "Line ranges are 1-based inclusive ranges into that exact file. The "
        "driver byte-verifies each block against the pinned source BEFORE "
        "any test execution and imports the pinned module for execution, "
        "so the executed grammars ARE these frozen definitions. NO post-hoc "
        "variants; any additional probe must be labeled POST-HOC "
        "NON-COVERAGE and excluded from all coverage numbers.", "",
        STANDING, "",
        "## The pre-registered wide-record grammars (CONTRACT.md Section 3, "
        "VERBATIM)", "",
        "- W1 = the fixed-m mscan unit [u16 idx][32 x f32] (m=32) with the "
        "head weight pair, consuming the span from the walk start.",
        "- W2 = the var-k grammar with the k-range extended to 9..24 (all "
        "other constraints identical to the canon var-k).",
        "- W3 = W1 with a Wm mis-estimate window (Wm-64..Wm+64, step 4).", "",
        "## Frozen invocation semantics (operationalization, fixed BEFORE "
        "any test execution)", "",
        "1. Walk start u = Wm - 2 (the K2/R34 census convention; dp = "
        "s[2:], Wm = the block's most-common span length). W1 executes "
        "K2.parse_fixed(dp, u, N, 32) VERBATIM (m = 32 = MSCAN_MAX; the "
        "head weight pair fl0+fl1~1.0 within WP_TOL is the parse_fixed "
        "head-pair semantics, counted as wp by the frozen unit; the fit "
        "predicate is the frozen unit's own: ok and recs > 0 - no "
        "additional constraint, no parameter change, no improvement).",
        "2. W2 executes K2.parse_variable(dp, u, N, kmax=24) VERBATIM - "
        "the canon var-k with the k-range extended from 1..8 to 1..24 "
        "(the extension content is k in 9..24; for k<=8 the choice behavior "
        "is identical to the canon, so W2 differs from canon only via "
        "k in 9..24); ndelta=9, tol=1e-4, idx_limit=None (idx < N) - all "
        "other constraints identical to the canon var-k. Fit = ok and "
        "recs > 0.",
        "3. W3 executes K2.parse_fixed(dp, u + d, N, 32) VERBATIM over the "
        "frozen Wm mis-estimate window d in {-64, -60, ..., 0, ..., +60, "
        "+64} (Wm' = Wm + d, start u' = Wm' - 2; step 4; 33 positions "
        "INCLUDING d=0, so W3 is a superset of W1; scan order ascending "
        "from d=-64; the FIRST hitting offset is recorded; no per-span free "
        "parameter outside the frozen window). Fit = any window position "
        "yields ok and recs > 0.",
        "4. Negative controls (NC_PROCEDURES.md): per-span wrong-start "
        "trials at u+2 and u-2 (2 trials per span, explicit denominators), "
        "the SAME grammar executed at the wrong start; rate-vs-rate "
        "comparisons only.",
        "5. The 269 population: the 334 no-fit span keys MINUS the union "
        "of RUN A's H5a (39) + H5c2 (26) FIT keys (POPULATION_269.json); "
        "334 - 65 = 269 asserted EXACTLY.",
        "",
    ]
    for label, lo, hi in blocks:
        seg = "\n".join(k2_src[lo - 1:hi])
        md += ["## %s (lines %d-%d)" % (label, lo, hi), "",
               "```python", seg, "```", ""]
    wr_lines(os.path.join(CTRL, "WIDE_GRAMMARS.md"), md)

    # ---- POPULATION_269.json ----
    pop = {
        "run": "PE_NIF_MORPH_WIDERECORD_R1_20260906_170000",
        "standing": STANDING,
        "result_class": "REPEATABILITY",
        "definition": ("the 269 remaining 9.3.5 no-fit morph spans = the "
                      "334 K2 no-fit keys MINUS the union of RUN A's H5a "
                      "(39) + H5c2 (26) FIT keys; 334 - 65 = 269 EXACT"),
        "sources": {
            "K2_NOFIT334_SPANS.txt": {
                "path": PINS["K2_NOFIT334_SPANS"][0],
                "sha256": sha256_file(PINS["K2_NOFIT334_SPANS"][0])},
            "RUNA_RETRO_SPAN_OUTCOMES.jsonl": {
                "path": os.path.join(RUNA_RUN, "01_RAW",
                                     "RETRO_SPAN_OUTCOMES.jsonl"),
                "sha256": pinx["RUNA_RETRO_SPAN_OUTCOMES"],
                "pin_provenance": "RUN A artifact_index.csv ordinary row "
                                  "(hash taken from that row; physical "
                                  "re-hash matches)"},
        },
        "subtraction_lists": {
            "P1_nofit334_keys": [list(k) for k in nf334],
            "RUNA_H5a_FIT_keys_39": [list(k) for k in sorted(h5a_fit)],
            "RUNA_H5c2_FIT_keys_26": [list(k) for k in sorted(h5c2_fit)],
            "union_65": [list(k) for k in sorted(union65)],
            "assertion": "334 - 65 = 269 EXACT (asserted in freeze and "
                         "re-asserted in-driver post-census)"},
        "pop269_keys": [list(k) for k in pop269],
        "n_files": len(files269),
    }
    wr_json(os.path.join(CTRL, "POPULATION_269.json"), pop)

    # ---- NC_PROCEDURES.md ----
    wr_lines(os.path.join(CTRL, "NC_PROCEDURES.md"), [
        "# NC_PROCEDURES.md - negative-control procedures "
        "(frozen BEFORE any test execution)", "",
        "Seed discipline: deterministic (no sampling randomness needed; "
        "the wrong starts are pinned). Written to disk before any W1/W2/W3 "
        "test execution.", "",
        "## NC-A (span level, full-269)", "",
        "- For EVERY span of the 269 population and EVERY grammar "
        "(W1, W2, W3): 2 trials at the pinned wrong starts u+2 and u-2 "
        "(u = the walk start Wm-2).",
        "- Trial hit = the SAME grammar executed at the wrong start: W1 -> "
        "K2.parse_fixed(dp, u2, N, 32) ok and recs>0; W2 -> "
        "K2.parse_variable(dp, u2, N, kmax=24) ok and recs>0; W3 -> the "
        "W3 window anchored at u2 (offsets u2+d, d in -64..+64 step 4) "
        "any-hit.",
        "- Explicit denominator: spans x 2 = 269 x 2 = 538 per grammar. "
        "A trial with u2 < 0 is recorded as a NON-hit trial "
        "(reason INVALID_START_NONHIT) and stays in the denominator.",
        "- Rate = hits / 538. Compared to the full-269 positive rate "
        "(1 trial per span at the true start) as rate-vs-rate ONLY; "
        "raw-count cross-population comparisons FORBIDDEN.", "",
        "## NC-B (held-out side, unit level)", "",
        "- Unit machinery (RUN A standard): unit = byte-identical dp "
        "payload (sha256), dedup within the 269 population; unit side = "
        "side of its FIRST member in sorted (file,bi,si) order; split "
        "families (a unit whose members land on both sides) are counted "
        "once, on the first-member side; held-out side = side B.",
        "- For EVERY held-out-side unit (representative = the unit's first "
        "member): 2 trials at u_rep+2 and u_rep-2 with the same grammar "
        "semantics as NC-A. Explicit denominator: held-out units x 2.",
        "- Rate = hits / (held-out units x 2), compared to the held-out "
        "unit positive rate (1 trial per unit) as rate-vs-rate ONLY.", "",
        "## Vacuity guard", "",
        "THE VACUOUS CASE 0 >= 5x0 CANNOT PASS: NC denominator 0 => "
        "NC_EMPTY_DENOMINATOR non-pass; zero positives => ZERO_FITS "
        "non-pass (checked BEFORE any separation comparison).", "",
        STANDING, "",
    ])

    # ---- SPLIT_SIDES_269.json ----
    split = {
        "run": "PE_NIF_MORPH_WIDERECORD_R1_20260906_170000",
        "standing": STANDING,
        "result_class": "REPEATABILITY",
        "procedure": ("file-level 50/50 of the 269-population's files; "
                      "random.Random(20260906) over the sorted file list; "
                      "rng.shuffle(copy); side_A = first n//2 files; "
                      "side_B = remaining files (held-out side); FAMILY "
                      "INTEGRITY: all spans of a file land on the side of "
                      "its file; byte-identical dp payloads (units) may "
                      "still cross sides and are handled by the unit "
                      "machinery (first-member side; split families counted "
                      "once)"),
        "seed": 20260906,
        "n_files": n,
        "side_A_files": sideA,
        "side_B_files": sideB,
        "pop269_side_A": [list(k) for k in pop269 if side_of[k[0]] == "A"],
        "pop269_side_B": [list(k) for k in pop269 if side_of[k[0]] == "B"],
        "written_before_testing": True,
    }
    if len(split["pop269_side_A"]) + len(split["pop269_side_B"]) != 269:
        raise SystemExit("split side assignment does not cover the 269")
    wr_json(os.path.join(CTRL, "SPLIT_SIDES_269.json"), split)

    # ---- GATES_PREREGISTERED.md ----
    wr_lines(os.path.join(CTRL, "GATES_PREREGISTERED.md"), [
        "# GATES_PREREGISTERED.md - a-priori gates (CONTRACT.md Section 4 "
        "VERBATIM; fixed BEFORE any test execution; NEVER adjusted after "
        "seeing results)", "",
        "## G-PINS", "",
        "Every input pin verified in-driver before any parse (R61 10/10; "
        "Models.bnt; the RUN A artifacts; the K2 artifacts re-hashed from "
        "bytes). Mismatch = HARD STOP.", "",
        "## G-CENSUS", "",
        "The baseline reproduces EXACTLY (rr 2,427 / var 2,093 / nofit 334 "
        "= 62 alt + 272 none; unknown-325 = 325) AND the RUN A removals "
        "reproduce (H5a 39 + H5c2 26 FIT keys from the pinned RUN A "
        "artifacts) AND 334 - 65 = 269 exact. Mismatch = HARD STOP.", "",
        "## G-WIDE (evaluated per grammar W1, W2, W3 separately; the PASS "
        "predicate is a conjunction - ALL components must hold)", "",
        "PASS iff (full-269 fits >= 10) AND (full-269 positive rate >= 5x "
        "the matched-NC rate) AND (NC denominator > 0) AND (held-out side "
        "units >= 30) AND (held-out fits >= 10) AND (held-out rate >= 5x "
        "the held-out-side matched-NC rate).",
        "THE VACUOUS CASE 0 >= 5x0 CANNOT PASS (NC denominator 0 => "
        "NC_EMPTY_DENOMINATOR). Report the exact binomial 95% CI for every "
        "rate (full and held-out, positive and NC).",
        "NON-PASS classes: EMPTY_GROUP / ZERO_FITS / INSUFFICIENT_TRIALS"
        "(held-out units < 30) / NC_EMPTY_DENOMINATOR / "
        "NC_INSUFFICIENT_SEPARATION(<5x) / HETEROGENEOUS_SPLIT (the "
        "full-269 passes its rate test but the held-out side fails - "
        "report BOTH numbers).",
        "A-PRIORI JUSTIFICATION (recorded, never adjusted): fits >= 10 so "
        "the rate is not a 1-2-span artifact; units >= 30 so the exact "
        "binomial CI is not degenerate; 5x = the K2/RUN A pre-registered "
        "separation standard; the held-out conjunction prevents "
        "full-population masking of file-level heterogeneity.", "",
        "## Frozen operationalization decisions (fixed here, BEFORE any "
        "test execution)", "",
        "d1. 'full-269' components are MEMBER-level (the 269 spans; 1 "
        "positive trial per span at the true start; NC denominator "
        "spans x 2 = 538). 'held-out side' components are UNIT-level "
        "(dp-sha units, RUN A machinery: dedup, first-member side, split "
        "families counted once; held-out = side B; NC denominator "
        "units x 2 on unit representatives). The contract text uses "
        "'units' only for the held-out side; the full-269 unit-level "
        "numbers are ALSO computed and reported as transparency in "
        "WIDE_RESULTS.json (they do not enter the gate).",
        "d2. '(NC denominator > 0)' is enforced for BOTH matched NC "
        "denominators (full-269 and held-out side); either being 0 => "
        "NC_EMPTY_DENOMINATOR (fail-closed).",
        "d3. Deterministic non-pass classification order (first match "
        "wins; every branch is fail-closed): CORRUPTED_RECORD -> "
        "DUPLICATE_ACROSS_SIDES -> EMPTY_GROUP -> DENOMINATOR_MISMATCH -> "
        "NC_EMPTY_DENOMINATOR -> INSUFFICIENT_TRIALS (held-out units < 30) "
        "-> ZERO_FITS (full-269 fits < 10) -> NC_INSUFFICIENT_SEPARATION "
        "(full-269 rate < 5x full-269 NC rate) -> HETEROGENEOUS_SPLIT "
        "(held-out fits < 10 OR held-out rate < 5x held-out NC rate, "
        "with BOTH numbers reported).",
        "d4. Every fit/NC count is a counter increment over an EXECUTED "
        "record (per-record validation only; deriving any validation "
        "count from a group size is FORBIDDEN).",
        "d5. COVERAGE_DELTA.json: this run's validated additions X = the "
        "UNION of spans consumed by grammars whose G-WIDE verdict is "
        "PASS (consumed spans of non-pass grammars are recorded but "
        "EXCLUDED from X and from every coverage number - the K2 "
        "OC-rejection precedent). remaining no-fit = 269 - X.",
        "d6. POST-HOC probes (if any) are labeled POST-HOC NON-COVERAGE "
        "and excluded from every number; this run executes NO post-hoc "
        "probe.",
        "d7. The 2003-era corpus, H7, and the residual-325 are OUT OF "
        "SCOPE (no execution, no claims).", "",
        "## G-EXEC", "",
        "Every validation number computed by executing the predicate on a "
        "SPECIFIC record; per-record outcomes recorded (span ID, side, "
        "grammar, outcome, rejection reason, bytes consumed); deriving "
        "any validation count from a group size is FORBIDDEN. The driver "
        "must (a) self-audit: grep its own gate code for size-derived "
        "assignments and record the audit; (b) unit-test the gate with "
        "the EIGHT synthetic fixtures (each must produce an explicit "
        "non-pass): (1) zero successes both sides; (2) empty population; "
        "(3) only-previously-selected successes; (4) a duplicate present "
        "in both groups; (5) unequal denominators; (6) a corrupted "
        "record; (7) a malformed manifest row; (8) a missing input "
        "file. All eight fail-closed => G-EXEC PASS.", "",
        "## G-SCOPE", "",
        "Read-only originals; zero payloads; run-local tooling only in "
        "00_CONTROL; this run's own artifact_index.csv written per "
        "MANIFEST_SCHEMA_SPEC.md and its self-validation gate PASSES "
        "(dogfooding).", "",
        STANDING, "",
    ])

    # ---- PREREG_MARKER.txt ----
    wr_lines(os.path.join(CTRL, "PREREG_MARKER.txt"), [
        "PRE-REGISTRATION / FREEZE COMPLETE %s"
        % time.strftime("%Y-%m-%d %H:%M:%S"),
        "RUN: PE_NIF_MORPH_WIDERECORD_R1_20260906_170000 (RUN_CLASS "
        "LOAD_BEARING; PE-MASTER loop bd17344b iteration 3).",
        "Grammars VERBATIM frozen (WIDE_GRAMMARS.md sha256 %s)"
        % sha256_file(os.path.join(CTRL, "WIDE_GRAMMARS.md")),
        "The 269 population frozen (POPULATION_269.json sha256 %s)"
        % sha256_file(os.path.join(CTRL, "POPULATION_269.json")),
        "Split sides frozen (SPLIT_SIDES_269.json sha256 %s)"
        % sha256_file(os.path.join(CTRL, "SPLIT_SIDES_269.json")),
        "NC procedures frozen (NC_PROCEDURES.md sha256 %s)"
        % sha256_file(os.path.join(CTRL, "NC_PROCEDURES.md")),
        "Gates a-priori frozen (GATES_PREREGISTERED.md sha256 %s)"
        % sha256_file(os.path.join(CTRL, "GATES_PREREGISTERED.md")),
        "Assertions at freeze: 334 - 65 = 269 EXACT; H5a 39 + H5c2 26 = 65 "
        "(disjoint union asserted); the 269-key list + subtraction lists "
        "on disk BEFORE any test execution.",
        "NO grammar test has been executed at freeze time; the corpus has "
        "not been parsed at freeze time (population derived ONLY from "
        "pinned READ-ONLY artifacts).",
        STANDING, "",
    ])
    print("FREEZE COMPLETE: WIDE_GRAMMARS.md, POPULATION_269.json, "
          "NC_PROCEDURES.md, SPLIT_SIDES_269.json, GATES_PREREGISTERED.md, "
          "PREREG_MARKER.txt")
    print("269 files: %d -> side A %d / side B %d"
          % (n, len(sideA), len(sideB)))
    print("side A spans %d / side B spans %d"
          % (len(split["pop269_side_A"]), len(split["pop269_side_B"])))


if __name__ == "__main__":
    main()
