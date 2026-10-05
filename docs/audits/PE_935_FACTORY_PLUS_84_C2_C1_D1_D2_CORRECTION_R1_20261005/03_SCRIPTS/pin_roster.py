# pin_roster.py
# RUN: PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005
# D2: the EXPECTED pin universe - the separate expected roster of claim IDs,
# addresses and intended roles, extracted from the BASE-pinned
# 03_SCRIPTS/c1_pin_ledger.py::PINS specification.
#
# ANTI-CIRCULARITY CONTRACT (Desktop finding D2/P2):
#   * The expected universe is NEVER derived from the artifacts under test
#     (the current C1 JSON/CSV being checked) and the PINS specification is
#     NEVER edited to make a missing or relabelled record pass.
#   * The roster is re-extracted IN-RUN from the exact BASE Git blob
#     (git show BASE_SHA:<relpath>) by AST LITERAL EVALUATION of the PINS
#     assignment - NO historical code is executed (no module import, no
#     side effects); the blob identity is recorded with every extraction.
#   * The module caches ONE extraction per process (the identity of the
#     BASE blob is stable within a run; the cache is in-memory only).
# The specification defines what must be measured; it does not prove that its
# expected machine behaviour is true - the battery separately re-derives
# every load-bearing field from the pinned EXE with the corrected decoder
# and justified boundaries (gate Q2/Q3), and cross-checks the EXE-derived EA
# against the roster's pinned expect_ea spec. Unresolved evidence remains
# unresolved.

import ast
import hashlib
import subprocess
import sys

sys.dont_write_bytecode = True

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
BASE_SHA = "9d31a82b6589f46e9ca6c75c6e323b433c1ebf92"
PIN_LEDGER_REL = ("docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_"
                  "CORRECTION_R1_20261005/03_SCRIPTS/c1_pin_ledger.py")

_CACHE = {}


def _git(*args):
    return subprocess.check_output(["git", "-C", REPO] + list(args))


def _blob_bytes():
    return _git("show", "%s:%s" % (BASE_SHA, PIN_LEDGER_REL))


def _git_blob_sha():
    return _git("rev-parse", "%s:%s" % (BASE_SHA, PIN_LEDGER_REL)).decode().strip()


def expected_from_git():
    """dict claim_id -> {"claim_id", "va", "role", "expect_bytes",
    "expect_ea" (list|None), "expect_imm"}. Cached per process; the cache
    stores the roster identity alongside the roster."""
    if "roster" in _CACHE:
        return _CACHE["roster"]
    src = _blob_bytes()
    tree = ast.parse(src.decode("utf-8"))
    pins = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "PINS":
                    pins = ast.literal_eval(node.value)
    if pins is None:
        raise SystemExit("PINS assignment not found in the BASE blob")
    roster = {}
    for (cid, va, kind, expect_bytes, expect_ea, expect_imm, source, corr) in pins:
        if cid in roster:
            raise SystemExit("duplicate claim_id in BASE PINS: %s" % cid)
        roster[cid] = {
            "claim_id": cid,
            "va": va,
            "role": kind,
            "expect_bytes": expect_bytes,
            "expect_ea": list(expect_ea) if expect_ea is not None else None,
            "expect_imm": expect_imm,
        }
    _CACHE["roster"] = roster
    _CACHE["identity"] = {
        "source_rel": PIN_LEDGER_REL,
        "base_sha": BASE_SHA,
        "git_blob_sha": _git_blob_sha(),
        "source_file_sha256": hashlib.sha256(src).hexdigest().upper(),
        "extraction_method": ("AST literal evaluation of the PINS assignment "
                              "from the BASE Git blob (no historical code "
                              "executed; no module import)"),
        "expected_total": len(roster),
    }
    return roster


def roster_identity():
    """Identity of the last extraction (source blob, method, cardinality)."""
    if "identity" not in _CACHE:
        expected_from_git()
    return dict(_CACHE["identity"])


def role_tally():
    roster = expected_from_git()
    tally = {}
    for rec in roster.values():
        tally[rec["role"]] = tally.get(rec["role"], 0) + 1
    return tally
