#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
freeze_extraction.py — PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1 run-local tooling.

Extracts the FROZEN grammar definitions VERBATIM (byte-exact line ranges) from
the PINNED K2 driver (morph_residual_deepdive_r1.py, SHA256
b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a) and writes
00_CONTROL/FROZEN_GRAMMARS.md. No rewording, no parameter changes, no
improvements. The revalidation driver later byte-verifies every block in
FROZEN_GRAMMARS.md against the pinned K2 driver source before any test.
"""
import hashlib
import os
import sys

K2_DRIVER = (r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_RESIDUAL_DEEPDIVE_"
             r"R1_20260906_033209\00_CONTROL\morph_residual_deepdive_r1.py")
K2_SHA_EXPECT = "b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a"
RUN = (r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_GRAMMAR_"
       r"REVALIDATION_R1_20260906_140500")
OUT = os.path.join(RUN, "00_CONTROL", "FROZEN_GRAMMARS.md")

STANDING = ("Standing sentence (applies to this and every artifact of this run): "
            "no semantic claims; class -256/field1 MEANING remains unknown; the "
            "-256=>zero-entry association remains ONE-WAY. Result classes: "
            "BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION / "
            "ERA_TRANSFER_DIAGNOSTIC / RUNTIME_SEMANTICS (= explicitly NOT_TESTED "
            "here, out of scope).")

# (label, first_line_1based, last_line_1based, role) — line ranges of the PINNED
# K2 driver, read from the pinned file itself (never hand-copied).
BLOCKS = [
    ("B1_constants", 79, 82,
     "Grammar constants (verbatim; used by every parser below)."),
    ("B2_sane", 96, 97,
     "sane() — float sanity predicate used by greedy_r18 (H7 join walk)."),
    ("B3_clean", 100, 103,
     "clean() — float cleanliness predicate used by the variable-k parsers."),
    ("B4_greedy_r18", 121, 144,
     "greedy_r18(dp, Wm) — the frozen H7 adjacency-join walk predicate "
     "(R18 greedy walk, VERBATIM incl. the 2-byte 00 00 tail acceptance)."),
    ("B5_parse_variable", 288, 320,
     "parse_variable(dp, u, N, kmax, ndelta, tol, idx_limit) — the frozen "
     "variable-k grammar; H5c2 = this function with idx_limit=0x8000 (H5c "
     "idx-relaxed). VERBATIM, no parameter changes."),
    ("B6_parse_variable_trunctail", 357, 396,
     "parse_variable_trunctail(dp, u, N, kmax, ndelta, tol, max_leftover) — "
     "the frozen H5a truncated-tail grammar. VERBATIM, no parameter changes."),
    ("B7_H5a_invocation", 1003, 1016,
     "H5a test invocation in K2 (fit condition ok and recs>0 and left>0; "
     "negative control nc2 at u+2/u-2). VERBATIM."),
    ("B8_H5c_invocation", 1035, 1052,
     "H5c test invocation in K2 (H5c2 = idx_limit 0x8000; fit condition "
     "ok and recs>0; negative control nc2). VERBATIM."),
    ("B9_H7_invocation", 1152, 1171,
     "H7 prev/next adjacency-join procedure in K2 (H7a: prev dp + current "
     "span incl. leading tag; H7b: current dp + next span incl. leading "
     "tag; both tested with greedy_r18(dpj, Wm)). VERBATIM."),
    ("B10_nc2", 871, 882,
     "nc2() — K2 negative-control procedure at pinned wrong starts u+2 and "
     "u-2 (the H5a/H5c NC basis of this run). VERBATIM."),
]


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        while True:
            b = fh.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main():
    k2_sha = sha256_file(K2_DRIVER)
    if k2_sha.lower() != K2_SHA_EXPECT:
        print("[freeze] HARD ABORT: pinned K2 driver hash mismatch: " + k2_sha)
        sys.exit(2)
    print("[freeze] pinned K2 driver hash OK: " + k2_sha)
    with open(K2_DRIVER, "r", encoding="utf-8", newline="") as f:
        src_lines = f.read().split("\n")

    parts = []
    parts.append("# FROZEN_GRAMMARS.md — VERBATIM grammar freeze "
                 "(PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500)\n")
    parts.append("\nSource of every block below: the PINNED K2 driver "
                 "`00_CONTROL/morph_residual_deepdive_r1.py` of "
                 "PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209, SHA256 "
                 + k2_sha.lower() + " (re-hashed at extraction time).\n")
    parts.append("\nLine ranges are 1-based inclusive ranges into that exact "
                 "file. The revalidation driver byte-verifies each block "
                 "against the pinned source BEFORE any test execution and "
                 "imports the pinned module for execution, so the executed "
                 "grammars ARE these frozen definitions.\n")
    parts.append("\n" + STANDING + "\n")
    for label, lo, hi, role in BLOCKS:
        block = "\n".join(src_lines[lo - 1:hi])
        parts.append("\n## " + label + " (lines " + str(lo) + "-" + str(hi) + ")\n")
        parts.append("\n" + role + "\n")
        parts.append("\n```python\n" + block + "\n```\n")

    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(parts))
    print("[freeze] wrote " + OUT)
    print("[freeze] FROZEN_GRAMMARS.md sha256: " + sha256_file(OUT))


if __name__ == "__main__":
    main()
