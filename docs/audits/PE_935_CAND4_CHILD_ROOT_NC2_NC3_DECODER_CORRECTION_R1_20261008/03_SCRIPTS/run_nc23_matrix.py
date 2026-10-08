"""run_nc23_matrix.py — mandatory eight-case matrix executor for
PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008
(RECORDS_AND_QC_MACHINERY_CORRECTION; frozen human-authorized contract
OPENCODE_NC2_NC3_CORRECTION.md §4 / dispatch STEPS 2-4).

POST (dispatch STEP 2): executes the ACTUAL corrected production function
ctrl4_exact_endpoint from 03_SCRIPTS/ctrl4_exact_endpoint_nc23fixed.py (imported
via importlib — NOT a rewritten imitation) on the mandatory eight-case matrix
over SYNTHETIC / IN-MEMORY buffers only:

    1. REAL_RECORDED_CLEAN               the published 0x42 clean window  EXPECTED = PASS
    2. HISTORICAL_EDI_CLOBBER            @0x0050A3DD 8B 3D D0 D8 B9 00     EXPECTED = FAIL (P2)
    3. FINAL_PUSH_ESI                    @0x0050A3F6: 57 -> 56             EXPECTED = FAIL (P3)
    4. FINAL_PUSH_NOP                    @0x0050A3F6: 57 -> 90             EXPECTED = FAIL (P3)
    5. NC1_SIB_HIDDEN_EDI_WRITE          12 B @0x0050A3DD..0x0050A3E8:     EXPECTED = FAIL
                                         8B 8C 24 8C 00 00 E8 BF AA BB CC 90
    6. NC2_NON_SIB_TEST_HIDDEN_EDI       12 B @0x0050A3DD..0x0050A3E8:     EXPECTED = FAIL
                                         84 06 BF AA BB CC E8 90 90 90 90 90
    7. NC3_INVALID_FF_FAR_CALL_REGISTER  12 B @0x0050A3DD..0x0050A3E8:     EXPECTED = FAIL
                                         FF D8 90 90 90 90 90 90 90 90 90 90
    8. NC3_INVALID_LEA_REGISTER          12 B @0x0050A3DD..0x0050A3E8:     EXPECTED = FAIL
                                         8D C0 90 90 90 90 90 90 90 90 90 90

Cases 1-5 keep the buffer definitions IDENTICAL to the SOURCE_PACKAGE sibfixed
checker (they are the sibfixed builders themselves, AST-extracted and executed).
Cases 6-8 replace EXACTLY the 12 bytes @0x0050A3DD..0x0050A3E8 (window total
stays 0x42; P1/P3/P4 bytes preserved — asserted and recorded).

PRE (dispatch STEP 3): reproduces the pre-correction state on the REAL
HISTORICAL functions via SAFE AST EXTRACTION — the needed class/function/
constant definitions are extracted with Python `ast` from BOTH historical
scripts (SOURCE_PACKAGE 03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py — the
NC1-era production; SOURCE_PACKAGE 00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py
— the NC1-era QC checker + its decode function + its 9-form SIB battery),
statically call-censused, then compiled and executed in an isolated namespace.
The historical top level is NEVER executed (the historical QC script's top
level writes QC_RESULTS.json — executing it would corrupt the READ-ONLY package;
the historical production module's writer counterpart does not exist, and no
historical writer of any kind is invoked). Both extracted HISTORICAL checkers
are run on the SAME eight buffers; per-case results are recorded as measured
(NEVER forced) with per-case PRE_REPRODUCED flags. An unexpected exception
propagating out of a historical checker is captured by THIS harness as
{"result": "ERROR", ...} — never recorded as FAIL.

Desktop measurements are TRANSCRIBED SEPARATELY under SOURCE_DESKTOP_MEASUREMENT
(cited file path + size + SHA256) from Desktop CONTROL_COUNTERCHECKS.json
residual_tests — they are the Desktop's measurements, never relabeled as this
executor's. This executor's own measurements are labeled EXECUTOR_REPRODUCTION.

Regressions persisted in CONTROL_RESULTS_POST.json (dispatch STEP 4):
    A. clean-window full decode listing (22 instructions, total 0x42) + VA/size
       map identity vs the PUBLISHED record (my own regex parse of the
       PRIOR_SCIENCE_PACKAGE record) + exact P1/P3/P4 endpoints.
    B. the nine historical SIB negative cases (the 9-form battery, AST-extracted
       from the historical QC script as a constant) re-run against the NEW
       production decode: all rejected fail-closed.
    C. the Desktop 144-form sweep against the NEW production decode:
       6 opcode branches (8B/89/8D/84/83/FF) x 3 memory mod (00/01/10) x 8 reg,
       always rm=4 -> 144 synthetic SIB forms, every form tested AT THE DECODER
       LEVEL (decode called directly; rejection = decode raises; a decoder-level
       reject is NOT presented as a whole-checker P1 FAIL).
    D. the NC2/NC3 rejection mechanisms + the instruction-level diagnosis of each
       new case, CITING the Desktop reference decode (capstone 5.0.7 residual
       measurements — cited reference, not a new measurement; nothing installed).

Also verifies the register forms remain supported (0x8B/0x89 reg forms,
register TEST 84 C0, memory LEA 8D 06, FF D2 call edx) — with negative controls
(8D C0, 84 06, 84 44 24 00 all must raise).

Writes (UTF-8, LF, no BOM; deterministic — NO timestamps inside either JSON):
    CONTROL_RESULTS_POST.json  (OUTPUT_ROOT root)
    CONTROL_RESULTS_PRE.json   (OUTPUT_ROOT root)

No EXE access of any kind. All buffers are in-memory; no mutation is ever
written to any file. This executor run is correction-only
(RECORDS_AND_QC_MACHINERY_CORRECTION): zero new science, zero new RE.
"""
import sys
sys.dont_write_bytecode = True   # FIRST: never write __pycache__/.pyc into the READ-ONLY SOURCE_PACKAGE or OUTPUT_ROOT

import ast
import hashlib
import importlib.util
import json
import os
import re

RUN_ID = "PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008"
RUN_CLASS = "RECORDS_AND_QC_MACHINERY_CORRECTION"

HERE = os.path.dirname(os.path.abspath(__file__))                   # OUTPUT_ROOT/03_SCRIPTS
PKG = os.path.dirname(HERE)                                          # OUTPUT_ROOT
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(PKG)))   # eudoria-clean repo root

# ---- READ-ONLY historical inputs (SOURCE_PACKAGE = the NC1 package; PRIOR_SCIENCE_PACKAGE)
SOURCE_PACKAGE = os.path.join(REPO_ROOT, "docs", "audits",
                              "PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007")
HIST_PROD_PATH = os.path.join(SOURCE_PACKAGE, "03_SCRIPTS", "ctrl4_exact_endpoint_sibfixed.py")
HIST_QC_PATH = os.path.join(SOURCE_PACKAGE, "00_CONTROL_INTERNAL_QC", "qc_ind_ctrl_sib_own.py")
WIN_RECORD_PATH = os.path.join(REPO_ROOT, "docs", "audits",
                               "PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007", "01_RAW",
                               "JOIN_WINDOW_50A3B7_REPIN.txt")
DESKTOP_ROOT = r"C:\Users\User\Documents\ChatGPT\PE\PE_935_NC1_DESKTOP_POST_AUDIT_91598A98_20261007"
DESKTOP_CC_PATH = os.path.join(DESKTOP_ROOT, "CONTROL_COUNTERCHECKS.json")
DESKTOP_REPORT_PATH = os.path.join(DESKTOP_ROOT, "REPORT.md")
DESKTOP_AUDIT_CHECKS_PATH = os.path.join(DESKTOP_ROOT, "AUDIT_CHECKS.json")

# ---- the NEW corrected production module (THIS package)
NEW_PROD_PATH = os.path.join(HERE, "ctrl4_exact_endpoint_nc23fixed.py")

# ---- pinned input identities (contract §2 / dispatch STEP 0 — re-measured at run time)
PINNED_INPUTS = {
    "contract": {"path": r"C:\Users\User\Documents\ChatGPT\PE\PE_935_NC2_NC3_CORRECTION_PROMPT_20261008"
                         r"\OPENCODE_NC2_NC3_CORRECTION.md",
                 "size_bytes": 14069,
                 "sha256": "3E0BDB58A0CDC1488DE9477A855CEC04D712D492E147CC92CDB3C021B5143B8F"},
    "desktop_report": {"path": DESKTOP_REPORT_PATH, "size_bytes": 11570,
                       "sha256": "125C47CA195C5D2F782EA1DBCEA0BA1CA65B973CBABEBABDD4F78963C43E83B4"},
    "desktop_control_counterchecks": {"path": DESKTOP_CC_PATH, "size_bytes": 132471,
                                     "sha256": "AD8DC2052F714439497A277512944EF729F53BDC94B436CB20EE09FEE6BCC28D"},
    "desktop_audit_checks": {"path": DESKTOP_AUDIT_CHECKS_PATH, "size_bytes": 46417,
                             "sha256": "593B03C3AB87FD274BE8C02E7196D60A961975C95631278C97A8271E528862B7"},
    "historical_production_sibfixed": {"path": "docs/audits/PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_"
                                              "POST_AUDIT_CORRECTION_R1_20261007/03_SCRIPTS/"
                                              "ctrl4_exact_endpoint_sibfixed.py",
                                       "size_bytes": 17740,
                                       "sha256": "44155437F20FA6DA9D6847A236F708C7F2A40F26BABE71424B21C325B4FB4405"},
    "historical_internal_qc": {"path": "docs/audits/PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_"
                                      "CORRECTION_R1_20261007/00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py",
                               "size_bytes": 51943,
                               "sha256": "529B61DB312AEC338221425B12F2D94DE2BE351B5C62F68DDBA6BF915B007B25"},
    "published_window_record": {"path": "docs/audits/PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/"
                                        "01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt",
                                "size_bytes": 4043,
                                "sha256": "A0DEFAA16D6934FC307BD88210BCCA59B823C58FB57319A2C090F9ED59AD01E3"},
}
# absolute-path lookup for the repo-relative pins
_REPO_REL = {"historical_production_sibfixed": HIST_PROD_PATH,
             "historical_internal_qc": HIST_QC_PATH,
             "published_window_record": WIN_RECORD_PATH}

# ---- case geometry
WIN_VA = 0x0050A3B7
HEAD_VA = 0x0050A3B7
FINAL_PUSH_VA = 0x0050A3F6
JOIN_CALL_VA = 0x0050A3F7
NC23_SPAN_VA = 0x0050A3DD
NC23_SPAN_LEN = 12

CASE_ORDER = [
    "REAL_RECORDED_CLEAN",
    "HISTORICAL_EDI_CLOBBER",
    "FINAL_PUSH_ESI",
    "FINAL_PUSH_NOP",
    "NC1_SIB_HIDDEN_EDI_WRITE",
    "NC2_NON_SIB_TEST_HIDDEN_EDI",
    "NC3_INVALID_FF_FAR_CALL_REGISTER",
    "NC3_INVALID_LEA_REGISTER",
]

# dispatch STEP 2 required POST results: case1 PASS; cases 2-8 FAIL
POST_EXPECTED = {name: ("PASS" if name == "REAL_RECORDED_CLEAN" else "FAIL") for name in CASE_ORDER}

# dispatch STEP 3 expected PRE results (historical production / historical internal QC).
# Recorded as EXPECTATION only — actuals are measured, never forced; PRE_REPRODUCED
# is derived per case from the actuals.
PRE_EXPECTED = {
    "REAL_RECORDED_CLEAN": {"production": "PASS", "internal_qc": "PASS"},
    "HISTORICAL_EDI_CLOBBER": {"production": "FAIL", "internal_qc": "FAIL"},
    "FINAL_PUSH_ESI": {"production": "FAIL", "internal_qc": "FAIL"},
    "FINAL_PUSH_NOP": {"production": "FAIL", "internal_qc": "FAIL"},
    "NC1_SIB_HIDDEN_EDI_WRITE": {"production": "FAIL", "internal_qc": "FAIL"},
    "NC2_NON_SIB_TEST_HIDDEN_EDI": {"production": "PASS", "internal_qc": "FAIL"},
    "NC3_INVALID_FF_FAR_CALL_REGISTER": {"production": "FAIL", "internal_qc": "PASS"},
    "NC3_INVALID_LEA_REGISTER": {"production": "ERROR:TypeError", "internal_qc": "PASS"},
}

# per-case mutation spans (for the changed-span + outside-preservation records)
CASE_SPANS = {
    "REAL_RECORDED_CLEAN": None,
    "HISTORICAL_EDI_CLOBBER": (0x0050A3DD, 6, "8B 8E 8C 00 00 00", "8B 3D D0 D8 B9 00"),
    "FINAL_PUSH_ESI": (0x0050A3F6, 1, "57", "56"),
    "FINAL_PUSH_NOP": (0x0050A3F6, 1, "57", "90"),
    "NC1_SIB_HIDDEN_EDI_WRITE": (0x0050A3DD, 12, "8B 8E 8C 00 00 00 56 E8 F7 A2 01 00",
                                 "8B 8C 24 8C 00 00 E8 BF AA BB CC 90"),
    "NC2_NON_SIB_TEST_HIDDEN_EDI": (0x0050A3DD, 12, "8B 8E 8C 00 00 00 56 E8 F7 A2 01 00",
                                    "84 06 BF AA BB CC E8 90 90 90 90 90"),
    "NC3_INVALID_FF_FAR_CALL_REGISTER": (0x0050A3DD, 12, "8B 8E 8C 00 00 00 56 E8 F7 A2 01 00",
                                         "FF D8 90 90 90 90 90 90 90 90 90 90"),
    "NC3_INVALID_LEA_REGISTER": (0x0050A3DD, 12, "8B 8E 8C 00 00 00 56 E8 F7 A2 01 00",
                                 "8D C0 90 90 90 90 90 90 90 90 90 90"),
}


# ================================================================ helpers
def _sha256_bytes(b):
    return hashlib.sha256(b).hexdigest().upper()


def _sha256_file(path):
    with open(path, "rb") as f:
        return _sha256_bytes(f.read())


def _size_file(path):
    return os.path.getsize(path)


def _hexsp(b):
    return " ".join(f"{x:02X}" for x in b)


def _pin_paths():
    m = dict(PINNED_INPUTS)
    for k, p in _REPO_REL.items():
        m[k]["abs_path"] = p
    return m


def measure_pinned_inputs():
    """Re-measure every pinned input at run time (fail-closed). Returns
    (identities, all_match)."""
    ident = {}
    ok = True
    for key, pin in _pin_paths().items():
        path = pin.get("abs_path", pin["path"])
        size = _size_file(path)
        sha = _sha256_file(path)
        match = (size == pin["size_bytes"] and sha == pin["sha256"])
        ok = ok and match
        ident[key] = {
            "path": pin["path"],
            "size_bytes": size, "size_pin": pin["size_bytes"],
            "sha256": sha, "sha256_pin": pin["sha256"],
            "match": match,
        }
    return ident, ok


# ================================================================ SAFE AST EXTRACTION (PRE method)
# Static allowlists: every Call inside the extracted nodes must be either an
# allowed attribute method (pure byte/string helpers), an allowed builtin
# (pure computation + exception-class constructors used by the extracted raise
# statements — inherently non-I/O), or a name defined by the extraction
# whitelist itself. Any open()/write()/exec()/import()/etc. anywhere in the
# picked nodes fails the census -> extraction aborts.
ALLOWED_ATTR_CALLS = {"fromhex", "from_bytes", "join", "get", "hex"}
ALLOWED_BUILTIN_CALLS = {"sorted", "len", "range", "int", "bytes", "bytearray", "str", "isinstance", "enumerate",
                         "ValueError", "IndexError", "TypeError", "KeyError", "AssertionError", "RuntimeError"}


def ast_extract(source_path, whitelist):
    """SAFE AST EXTRACTION (dispatch STEP 3 METHOD): parse the historical source,
    pick ONLY the top-level nodes binding whitelisted names (FunctionDef / ClassDef /
    plain-Name Assign), statically census every Call inside the picked nodes against
    the allowlists, then compile and execute ONLY those nodes in a fresh namespace.
    The historical module top level is NEVER executed (no file I/O of the historical
    script — in particular the historical QC writer — can ever run)."""
    with open(source_path, encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)          # parse only — no execution
    picked = []
    bound = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in whitelist:
            picked.append(node)
            bound.append(node.name)
        elif (isinstance(node, ast.Assign) and len(node.targets) == 1
              and isinstance(node.targets[0], ast.Name) and node.targets[0].id in whitelist):
            picked.append(node)
            bound.append(node.targets[0].id)
    missing = sorted(set(whitelist) - set(bound))
    if missing:
        raise RuntimeError(f"AST extraction from {source_path}: missing symbols {missing}")
    census = {}
    for node in picked:
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call):
                if isinstance(sub.func, ast.Attribute):
                    key = "attr:" + sub.func.attr
                    if sub.func.attr not in ALLOWED_ATTR_CALLS:
                        raise RuntimeError(f"AST extraction from {source_path}: disallowed attribute "
                                           f"call '{sub.func.attr}' in extracted node")
                else:
                    key = "name:" + sub.func.id
                    if sub.func.id not in ALLOWED_BUILTIN_CALLS and sub.func.id not in whitelist:
                        raise RuntimeError(f"AST extraction from {source_path}: disallowed name "
                                           f"call '{sub.func.id}' in extracted node")
                census[key] = census.get(key, 0) + 1
    code = compile(ast.Module(body=picked, type_ignores=[]), filename=source_path, mode="exec")
    ns = {}
    exec(code, ns)     # execute ONLY the extracted defs/constants — never the historical top level
    return ns, bound, census


# whitelists of the symbols needed from each historical script
HIST_PROD_SYMBOLS = [
    "CLEAN_WINDOW_HEX", "WIN_VA", "HEAD_VA", "FINAL_PUSH_VA", "JOIN_CALL_VA", "CLEAN_WINDOW",
    "CLOBBER_VA", "CLOBBER_BYTES", "NC1_SIB_VA", "NC1_SIB_SPAN_LEN", "NC1_SIB_ORIGINAL",
    "NC1_SIB_BYTES", "REG", "GRP1", "Insn", "make_clobber_mutant", "make_final_arg_mutant",
    "make_nc1_sib_mutant", "_modrm", "_reject_sib", "decode", "ctrl4_exact_endpoint",
]
HIST_QC_SYMBOLS = [
    "WIN_VA", "HEAD_VA", "FINAL_PUSH_VA", "JOIN_CALL_VA", "CLOBBER_VA", "NC1_SPAN_VA",
    "NC1_SPAN_LEN", "REG", "GRP1", "Insn", "hexsp", "mrm_split", "mem_dlen", "my_decode",
    "my_ctrl4", "SIB_BATTERY",
]


def _import_from(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {name} from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)     # the NEW production module is inert at import (full-read verified)
    return mod


def run_checker(fn, buf):
    """Run ONE checker call and classify. A normal (ok, detail) return becomes
    PASS/FAIL. An exception PROPAGATING out of the checker (the historical
    production checker catches only (ValueError, IndexError) internally — its
    TypeError escapes) is captured HERE, at the harness boundary, and recorded
    as {"result": "ERROR", "exception": <type>} — NEVER as FAIL. (This harness
    catch is measurement classification, NOT a blanket catch inside any checker.)"""
    try:
        ok, detail = fn(buf)
    except Exception as exc:                      # harness classification only
        return {"result": "ERROR", "exception": type(exc).__name__,
                "detail": f"{type(exc).__name__}: {exc}"}
    return {"result": "PASS" if ok else "FAIL", "exception": None, "detail": detail}


def outside_preserved(buf, clean, span):
    """True iff buf equals clean at every byte OUTSIDE the mutation span."""
    if span is None:
        return bytes(buf) == bytes(clean)
    va, ln = span[0], span[1]
    off = va - WIN_VA
    return bytes(buf[:off]) == bytes(clean[:off]) and bytes(buf[off + ln:]) == bytes(clean[off + ln:])


def p1_p3_p4_preserved(buf):
    """True iff the P1 (8B F8 @0x0050A3B7), P3 (57 @0x0050A3F6) and P4 (FF D2
    @0x0050A3F7) bytes are present at their exact VAs (used for the three new
    NC2/NC3 cases, which must preserve them)."""
    return (bytes(buf[HEAD_VA - WIN_VA:HEAD_VA - WIN_VA + 2]) == b"\x8B\xF8"
            and buf[FINAL_PUSH_VA - WIN_VA] == 0x57
            and bytes(buf[JOIN_CALL_VA - WIN_VA:JOIN_CALL_VA - WIN_VA + 2]) == b"\xFF\xD2")


def decode_rejection(mod, buf):
    """Decoder-level rejection evidence for a buffer the NEW decode refuses:
    the exact exception, plus the rejection VA pinpointed by prefix decode (the
    largest decodable prefix ends exactly where the rejected instruction starts)."""
    try:
        insns = mod.decode(buf, mod.WIN_VA)
        return {"decode_status": "DECODED", "instruction_count": len(insns)}
    except (ValueError, IndexError) as exc:
        rejected_va = None
        for n in range(len(buf), 0, -1):
            try:
                mod.decode(buf[:n], mod.WIN_VA)
            except (ValueError, IndexError):
                continue
            rejected_va = mod.WIN_VA + n
            break
        return {
            "decode_status": "REJECTED_FAIL_CLOSED",
            "rejection": f"{type(exc).__name__}: {exc}",
            "rejected_at_va": f"0x{rejected_va:08X}" if rejected_va is not None else "UNKNOWN",
            "note": ("decode aborted at the rejected instruction BEFORE any displacement/length was "
                     "computed for it; no instruction at/after this VA was produced (fail-closed — "
                     "this is a DECODER-LEVEL reject, not an accidental whole-checker P1 FAIL)"),
        }


def full_listing(mod, buf):
    insns = mod.decode(buf, mod.WIN_VA)
    rows = []
    for va in sorted(insns):
        ins = insns[va]
        rows.append({"va": f"0x{va:08X}", "size": ins.size, "mnemonic": ins.mnemonic,
                     "operands": ins.op_str, "bytes": ins.hex(), "writes_edi": ins.writes_edi})
    return rows


# ================================================================ main
def main():
    # ---------- pinned inputs re-measured (fail-closed)
    input_identities, pins_ok = measure_pinned_inputs()
    if not pins_ok:
        print("FATAL: pinned input identity mismatch — refusing to proceed")
        return 2

    # ---------- SAFE AST EXTRACTION of BOTH historical checkers
    hist_prod_ns, prod_bound, prod_census = ast_extract(HIST_PROD_PATH, HIST_PROD_SYMBOLS)
    hist_qc_ns, qc_bound, qc_census = ast_extract(HIST_QC_PATH, HIST_QC_SYMBOLS)
    hist_prod_sha = _sha256_file(HIST_PROD_PATH)
    hist_qc_sha = _sha256_file(HIST_QC_PATH)

    # fixture sanity of the extracted historical production namespace
    clean_hist = hist_prod_ns["CLEAN_WINDOW"]
    assert len(clean_hist) == 0x42, "extracted historical clean window must be 0x42 bytes"
    assert hist_prod_ns["WIN_VA"] == WIN_VA and hist_qc_ns["WIN_VA"] == WIN_VA

    # ---------- the eight buffers (first five = the sibfixed builders themselves)
    buffers = {
        "REAL_RECORDED_CLEAN": clean_hist,
        "HISTORICAL_EDI_CLOBBER": hist_prod_ns["make_clobber_mutant"](),
        "FINAL_PUSH_ESI": hist_prod_ns["make_final_arg_mutant"](0x56),
        "FINAL_PUSH_NOP": hist_prod_ns["make_final_arg_mutant"](0x90),
        "NC1_SIB_HIDDEN_EDI_WRITE": hist_prod_ns["make_nc1_sib_mutant"](),
    }
    # the three new cases: replace EXACTLY the 12 bytes @0x0050A3DD..0x0050A3E8
    def build_nc23(repl_hex):
        repl = bytes.fromhex(repl_hex)
        assert len(repl) == NC23_SPAN_LEN
        buf = bytearray(clean_hist)
        off = NC23_SPAN_VA - WIN_VA
        assert bytes(buf[off:off + NC23_SPAN_LEN]) == bytes.fromhex(CASE_SPANS["NC2_NON_SIB_TEST_HIDDEN_EDI"][2])
        buf[off:off + NC23_SPAN_LEN] = repl
        return bytes(buf)

    buffers["NC2_NON_SIB_TEST_HIDDEN_EDI"] = build_nc23("84 06 BF AA BB CC E8 90 90 90 90 90")
    buffers["NC3_INVALID_FF_FAR_CALL_REGISTER"] = build_nc23("FF D8 90 90 90 90 90 90 90 90 90 90")
    buffers["NC3_INVALID_LEA_REGISTER"] = build_nc23("8D C0 90 90 90 90 90 90 90 90 90 90")

    # per-case buffer identity records
    buffer_records = {}
    for name in CASE_ORDER:
        buf = buffers[name]
        span = CASE_SPANS[name]
        rec = {
            "buffer_len_bytes": len(buf),
            "buffer_hex": _hexsp(buf),
            "buffer_sha256": _sha256_bytes(buf),
            "changed_span": ({"va_range": f"0x{span[0]:08X}..0x{span[0] + span[1] - 1:08X}",
                              "len": span[1], "original_bytes": span[2], "replacement_bytes": span[3]}
                             if span else {"va_range": None, "len": 0, "original_bytes": None,
                                           "replacement_bytes": None}),
            "bytes_outside_span_preserved_vs_clean": outside_preserved(buf, clean_hist, span),
            "p1_p3_p4_bytes_preserved": p1_p3_p4_preserved(buf),
        }
        assert len(buf) == 0x42
        assert rec["bytes_outside_span_preserved_vs_clean"]
        if name != "REAL_RECORDED_CLEAN":
            assert rec["p1_p3_p4_bytes_preserved"] or name in ("FINAL_PUSH_ESI", "FINAL_PUSH_NOP"), \
                f"P1/P3/P4 must survive in {name}"
        buffer_records[name] = rec

    # ---------- Desktop residual case byte-identity (cited cross-check, READ-ONLY)
    desktop_cc = json.load(open(DESKTOP_CC_PATH, encoding="utf-8"))
    desktop_residual = desktop_cc["residual_tests"]
    DESKTOP_CASE_FOR = {
        "NC2_NON_SIB_TEST_HIDDEN_EDI": "NON_SIB_TEST_HIDDEN_EDI",
        "NC3_INVALID_FF_FAR_CALL_REGISTER": "INVALID_FF_FAR_CALL_REGISTER",
        "NC3_INVALID_LEA_REGISTER": "INVALID_LEA_REGISTER",
    }
    desktop_buffer_identity = {}
    for case_name, desk_name in DESKTOP_CASE_FOR.items():
        desk_buf = bytes.fromhex(desktop_residual[desk_name]["buffer"])
        desktop_buffer_identity[case_name] = {
            "desktop_case": desk_name,
            "byte_identical_to_executor_buffer": bytes(buffers[case_name]) == desk_buf,
        }
        assert desktop_buffer_identity[case_name]["byte_identical_to_executor_buffer"], \
            f"{case_name}: executor buffer differs from the cited Desktop case bytes"

    # ---------- PRE: HISTORICAL production + HISTORICAL internal-QC checkers on the SAME buffers
    pre_matrix = {}
    for name in CASE_ORDER:
        buf = buffers[name]
        prod_row = run_checker(hist_prod_ns["ctrl4_exact_endpoint"], buf)
        qc_row = run_checker(hist_qc_ns["my_ctrl4"], buf)
        exp_prod = PRE_EXPECTED[name]["production"]
        exp_qc = PRE_EXPECTED[name]["internal_qc"]
        prod_actual = prod_row["result"] if prod_row["result"] != "ERROR" else f"ERROR:{prod_row['exception']}"
        qc_actual = qc_row["result"] if qc_row["result"] != "ERROR" else f"ERROR:{qc_row['exception']}"
        pre_matrix[name] = {
            "buffer_len_bytes": buffer_records[name]["buffer_len_bytes"],
            "buffer_hex": buffer_records[name]["buffer_hex"],
            "buffer_sha256": buffer_records[name]["buffer_sha256"],
            "expected": {"production": exp_prod, "internal_qc": exp_qc},
            "actual": {"production": prod_actual, "internal_qc": qc_actual},
            "production_detail": prod_row["detail"],
            "production_exception": prod_row["exception"],
            "internal_qc_detail": qc_row["detail"],
            "internal_qc_exception": qc_row["exception"],
            "production_reproduced": prod_actual == exp_prod,
            "internal_qc_reproduced": qc_actual == exp_qc,
        }
    pre_all = all(r["production_reproduced"] and r["internal_qc_reproduced"] for r in pre_matrix.values())

    pre_doc = {
        "RUN_ID": RUN_ID,
        "RUN_CLASS": RUN_CLASS,
        "purpose": ("PRE reproduction on the REAL HISTORICAL functions (dispatch STEP 3), separated from the "
                    "Desktop measurements: the NC1-era production checker (sibfixed) and the NC1-era internal-QC "
                    "checker (qc_ind_ctrl_sib_own) are AST-EXTRACTED (top level NEVER executed) and run on the "
                    "SAME eight synthetic in-memory buffers; per-case results are measured, NEVER forced, and "
                    "PRE_REPRODUCED flags are derived from the actuals"),
        "input_identities_remeasured_at_run_time": input_identities,
        "METHOD_SAFE_AST_EXTRACTION": {
            "description": ("SAFE AST EXTRACTION: Python ast parses each historical script; ONLY the top-level "
                             "nodes binding whitelisted names (FunctionDef / ClassDef / plain-Name Assign) are "
                             "picked; every Call inside the picked nodes is statically censused against allowlists "
                             "(allowed attribute methods: fromhex/from_bytes/join/get/hex; allowed builtins: "
                             "sorted/len/range/int/bytes/bytearray/str/isinstance/enumerate; allowed name calls: "
                             "whitelisted symbols themselves) — any open()/write()/exec()/import or other "
                             "disallowed call aborts the extraction; the picked nodes are then compiled and "
                             "executed in an isolated namespace. The historical top level is NEVER executed: the "
                             "historical QC script's top level writes QC_RESULTS.json (executing it would corrupt "
                             "the READ-ONLY package) and no historical writer of any kind is invoked."),
            "historical_production_source": {
                "path": PINNED_INPUTS["historical_production_sibfixed"]["path"],
                "size_bytes": _size_file(HIST_PROD_PATH), "sha256": hist_prod_sha,
                "extracted_symbols_in_source_order": prod_bound,
                "extracted_node_count": len(prod_bound),
                "static_call_census": prod_census,
                "top_level_executed": False,
                "historical_top_level_assert_skipped_note": ("the module-level 'assert len(CLEAN_WINDOW) == 0x42' "
                                                             "is NOT extracted; the harness asserts the 0x42 length "
                                                             "itself on the extracted constant"),
            },
            "historical_internal_qc_source": {
                "path": PINNED_INPUTS["historical_internal_qc"]["path"],
                "size_bytes": _size_file(HIST_QC_PATH), "sha256": hist_qc_sha,
                "extracted_symbols_in_source_order": qc_bound,
                "extracted_node_count": len(qc_bound),
                "static_call_census": qc_census,
                "top_level_executed": False,
            },
            "isolated_namespaces": {
                "historical_production": "fresh dict namespace; only the extracted defs/constants execute",
                "historical_internal_qc": "fresh dict namespace; only the extracted defs/constants execute",
                "historical_qc_writer_qc_results_json_invoked": False,
            },
        },
        "EXECUTOR_REPRODUCTION": {
            "label": ("EXECUTOR_REPRODUCTION — THIS run's own in-memory measurements of the REAL HISTORICAL "
                      "functions (AST-extracted), on buffers built by the sibfixed builders themselves (cases 1-5) "
                      "and by this harness's own 12-byte span builders (cases 6-8, byte-identical to the cited "
                      "Desktop residual case buffers). Never a relabel of the Desktop measurement."),
            "matrix_8_cases": pre_matrix,
            "PRE_REPRODUCED": {
                "per_case": {name: {"production": pre_matrix[name]["production_reproduced"],
                                    "internal_qc": pre_matrix[name]["internal_qc_reproduced"]}
                             for name in CASE_ORDER},
                "all_cases_production_and_internal_qc": pre_all,
                "note": ("PRE_REPRODUCED=YES requires every per-case actual to equal the contract-expected "
                         "historical behavior (incl. the historical NC2 production false-PASS, the historical NC3 "
                         "LEA production TypeError captured as ERROR:TypeError — never as FAIL — and the historical "
                         "QC /3-acceptance PASSes). Actuals differing from expectation are shown per case; the "
                         "flags are derived, never forced."),
            },
            "historical_defect_confirmation": {
                "NC2_memory_TEST_false_pass": ("historical production PASSes NC2_NON_SIB_TEST_HIDDEN_EDI (the "
                                                "false pass: 84 06 mis-lengthened to 6 bytes hides the true "
                                                "mov edi,0xE8CCBBAA @0x0050A3DF EDI write inside P2) while the "
                                                "historical QC correctly FAILs it (its 0x84 branch rejects every "
                                                "memory TEST form)"
                                                if (pre_matrix["NC2_NON_SIB_TEST_HIDDEN_EDI"]["actual"]["production"] == "PASS"
                                                    and pre_matrix["NC2_NON_SIB_TEST_HIDDEN_EDI"]["actual"]["internal_qc"] == "FAIL")
                                                else "NOT REPRODUCED AS EXPECTED — see per-case actuals"),
                "NC3_FF_D8_divergence": ("historical production FAILs FF D8 (FF branch accepts only /2 mod=11) "
                                          "while the historical QC PASSes it (its erroneous /3-acceptance branch "
                                          "decodes FF D8 as a harmless push — the NC3-A defect, corrected in the "
                                          "QC phase, not in this executor's scope)"
                                          if (pre_matrix["NC3_INVALID_FF_FAR_CALL_REGISTER"]["actual"]["production"] == "FAIL"
                                              and pre_matrix["NC3_INVALID_FF_FAR_CALL_REGISTER"]["actual"]["internal_qc"] == "PASS")
                                          else "NOT REPRODUCED AS EXPECTED — see per-case actuals"),
                "NC3_LEA_TypeError": ("historical production ERRORS with TypeError (NoneType operand formatting "
                                       "crash escapes the (ValueError, IndexError) catch) while the historical QC "
                                       "PASSes it (its mod=11 LEA formats 'eax, eax' as a harmless instruction)"
                                       if (pre_matrix["NC3_INVALID_LEA_REGISTER"]["actual"]["production"] == "ERROR:TypeError"
                                           and pre_matrix["NC3_INVALID_LEA_REGISTER"]["actual"]["internal_qc"] == "PASS")
                                       else "NOT REPRODUCED AS EXPECTED — see per-case actuals"),
            },
        },
        "SOURCE_DESKTOP_MEASUREMENT": {
            "label": ("SOURCE_DESKTOP_MEASUREMENT — transcribed VERBATIM from the Desktop post-audit of "
                      "91598a98 (CONTROL_COUNTERCHECKS.json residual_tests); this is the DESKTOP's "
                      "measurement, cited as reference, NEVER relabeled as this executor's own"),
            "cited_file": DESKTOP_CC_PATH,
            "cited_file_size_bytes": _size_file(DESKTOP_CC_PATH),
            "cited_file_sha256": _sha256_file(DESKTOP_CC_PATH),
            "residual_tests": {
                "NON_SIB_TEST_HIDDEN_EDI": desktop_residual["NON_SIB_TEST_HIDDEN_EDI"],
                "INVALID_FF_FAR_CALL_REGISTER": desktop_residual["INVALID_FF_FAR_CALL_REGISTER"],
                "INVALID_LEA_REGISTER": desktop_residual["INVALID_LEA_REGISTER"],
            },
            "executor_buffer_identity_vs_cited_desktop_cases": desktop_buffer_identity,
            "reference_decoder_cited": {"library": "capstone", "version": "5.0.7",
                                         "note": ("Desktop's independent reference decode; CITED, not re-measured "
                                                  "by this run (nothing installed; no new Capstone measurement)")},
        },
        "PROVENANCE_SEPARATION_NOTE": ("SOURCE_DESKTOP_MEASUREMENT (Desktop's measurements, transcribed with "
                                      "citation) and EXECUTOR_REPRODUCTION (this run's AST-extraction "
                                      "measurements) are recorded as SEPARATE labeled sections; no Desktop "
                                      "row is copied as a new executor measurement and vice versa."),
        "exe_accessed": False,
        "buffers_synthetic_in_memory_only": True,
        "determinism": "no timestamps; all rows machine-measured in this run",
    }

    # ---------- POST: the ACTUAL corrected production function (importlib — no imitation)
    NEW = _import_from(NEW_PROD_PATH, "ctrl4_exact_endpoint_nc23fixed")
    new_prod_sha = _sha256_file(NEW_PROD_PATH)
    fixture_identity = bytes(NEW.CLEAN_WINDOW) == bytes(clean_hist)

    # buffers rebuilt through the NEW module's own builders (byte-identity asserted vs the PRE set)
    new_buffers = {
        "REAL_RECORDED_CLEAN": NEW.CLEAN_WINDOW,
        "HISTORICAL_EDI_CLOBBER": NEW.make_clobber_mutant(),
        "FINAL_PUSH_ESI": NEW.make_final_arg_mutant(0x56),
        "FINAL_PUSH_NOP": NEW.make_final_arg_mutant(0x90),
        "NC1_SIB_HIDDEN_EDI_WRITE": NEW.make_nc1_sib_mutant(),
        "NC2_NON_SIB_TEST_HIDDEN_EDI": NEW.make_nc23_span_mutant(NEW.NC2_NON_SIB_TEST_BYTES),
        "NC3_INVALID_FF_FAR_CALL_REGISTER": NEW.make_nc23_span_mutant(NEW.NC3_INVALID_FF_BYTES),
        "NC3_INVALID_LEA_REGISTER": NEW.make_nc23_span_mutant(NEW.NC3_INVALID_LEA_BYTES),
    }
    buffers_byte_identical = all(bytes(new_buffers[n]) == bytes(buffers[n]) for n in CASE_ORDER)

    post_matrix = {}
    post_all = True
    for name in CASE_ORDER:
        buf = new_buffers[name]
        ok, detail = NEW.ctrl4_exact_endpoint(buf)          # the ACTUAL corrected production function
        actual = "PASS" if ok else "FAIL"
        expected = POST_EXPECTED[name]
        row = {
            "case": name,
            "buffer_len_bytes": len(buf),
            "buffer_hex": _hexsp(buf),
            "buffer_sha256": _sha256_bytes(buf),
            "changed_span": buffer_records[name]["changed_span"],
            "bytes_outside_span_preserved_vs_clean": outside_preserved(buf, NEW.CLEAN_WINDOW, CASE_SPANS[name]),
            "p1_p3_p4_bytes_preserved": p1_p3_p4_preserved(buf),
            "expected": expected,
            "actual": actual,
            "match": actual == expected,
            "checker_detail": detail,
            "decode_boundaries": decode_rejection(NEW, buf) if actual == "FAIL" else
                                 {"decode_status": "DECODED", "instruction_count": len(NEW.decode(buf, NEW.WIN_VA))},
        }
        post_matrix[name] = row
        post_all = post_all and row["match"]

    # decode rejection mechanisms for the three new cases (explicit, decoder-level)
    rejection_mechanisms = {
        "NC1_SIB_HIDDEN_EDI_WRITE": "NC1 SIB guard in the 0x8B branch: mod != 0b11 with rm == 0b100 -> "
                                     "ValueError('unsupported SIB form (mod=10 rm=100) — FAIL CLOSED') BEFORE any "
                                     "displacement/length computation (unchanged from sibfixed)",
        "NC2_NON_SIB_TEST_HIDDEN_EDI": "NC2 guard in the 0x84 branch: memory TEST form (mod=00) -> "
                                        "ValueError('unsupported memory TEST form (mod=00) — FAIL CLOSED') BEFORE "
                                        "any length computation (after the NC1 SIB guard); register TEST "
                                        "(84 C0, mod=11) remains supported",
        "NC3_INVALID_FF_FAR_CALL_REGISTER": "0xFF branch (UNCHANGED from sibfixed): only FF /2 (call r/m32) with "
                                            "mod=11 is accepted (the FF D2 endpoint); FF D8 = FF /3 with mod=11 is "
                                            "an invalid far-call register form -> ValueError('uncovered FF /3 "
                                            "mod=11'); no FF /6 or other forms added",
        "NC3_INVALID_LEA_REGISTER": "NC3-B guard in the 0x8B/0x89/0x8D branch: LEA with mod=11 is invalid -> "
                                     "ValueError('unsupported LEA register form (mod=11) — FAIL CLOSED') BEFORE "
                                     "operand formatting and before any verdict computation — the checker returns "
                                     "(False, diagnostic), never a TypeError",
    }

    # ---------- regression A: clean-window full decode listing + published-map identity
    clean_listing = full_listing(NEW, NEW.CLEAN_WINDOW)
    clean_va_sizes = [(int(r["va"], 16), r["size"]) for r in clean_listing]
    win_txt = open(WIN_RECORD_PATH, encoding="utf-8").read()
    pat = re.compile(r"^  0x([0-9a-f]{8})  ((?:[0-9A-F]{2} )*[0-9A-F]{2})", re.M)
    pieces = sorted((int(v, 16), bytes.fromhex(bx)) for v, bx in pat.findall(win_txt))
    pub_window = b"".join(bx for _, bx in pieces)
    pub_map = {va: len(bx) for va, bx in pieces}
    meas_map = dict(clean_va_sizes)
    boundary_regression = {
        "reference": ("PRIOR_SCIENCE_PACKAGE 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt — the published 22-instruction "
                      "record (pinned SHA256 " + PINNED_INPUTS["published_window_record"]["sha256"] + "); map "
                      "re-derived MY OWN way with a regex parser over the per-instruction byte column"),
        "published_record_window_identical_to_production_fixture": bytes(pub_window) == bytes(NEW.CLEAN_WINDOW),
        "published_va_size_map": {f"0x{va:08X}": sz for va, sz in sorted(pub_map.items())},
        "measured_va_size_map": {f"0x{va:08X}": sz for va, sz in clean_va_sizes},
        "va_sets_identical": sorted(meas_map) == sorted(pub_map),
        "sizes_identical": meas_map == pub_map,
        "instruction_count": len(clean_listing),
        "total_bytes": sum(sz for _, sz in clean_va_sizes),
        "p1_head_exact": (clean_listing[0]["va"] == "0x0050A3B7" and clean_listing[0]["bytes"] == "8B F8"
                          and clean_listing[0]["mnemonic"] == "mov" and clean_listing[0]["operands"] == "edi, eax"),
        "p3_final_push_exact": any(r["va"] == "0x0050A3F6" and r["bytes"] == "57" and r["mnemonic"] == "push"
                                   and r["operands"] == "edi" for r in clean_listing),
        "p4_join_call_exact": any(r["va"] == "0x0050A3F7" and r["bytes"] == "FF D2" and r["mnemonic"] == "call"
                                  and r["operands"] == "edx" for r in clean_listing),
    }
    boundary_regression["result"] = ("PASS" if (boundary_regression["va_sets_identical"]
                                                and boundary_regression["sizes_identical"]
                                                and boundary_regression["instruction_count"] == 22
                                                and boundary_regression["total_bytes"] == 0x42
                                                and boundary_regression["p1_head_exact"]
                                                and boundary_regression["p3_final_push_exact"]
                                                and boundary_regression["p4_join_call_exact"]
                                                and boundary_regression["published_record_window_identical_to_production_fixture"])
                                     else "FAIL")

    # ---------- regression B: the nine historical SIB negative cases vs the NEW production decode
    sib_battery = hist_qc_ns["SIB_BATTERY"]     # AST-extracted constant (9 forms; historical top level never run)
    regB_rows = []
    regB_ok = True
    for form_name, bhex, declared_mech in sib_battery:
        b = bytes.fromhex(bhex)
        try:
            NEW.decode(b, 0x00400000)
            raises, msg = False, "NO RAISE — DECODED (DEFECT)"
            regB_ok = False
        except (ValueError, IndexError) as exc:
            raises, msg = True, f"{type(exc).__name__}: {exc}"
        regB_rows.append({"form": form_name, "bytes": bhex,
                          "historical_declared_mechanism": declared_mech,
                          "new_production_raises": raises, "new_production_rejection": msg})
        if not raises:
            regB_ok = False

    # ---------- regression C: the Desktop 144-form sweep vs the NEW production decode (DECODER level)
    regC_rows = []
    regC_ok = True
    for opcode in (0x8B, 0x89, 0x8D, 0x84, 0x83, 0xFF):
        for mod in (0b00, 0b01, 0b10):
            for reg in range(8):
                modrm = (mod << 6) | (reg << 3) | 0b100          # always rm=4 (SIB)
                form = bytes([opcode, modrm, 0x24])               # SIB byte 0x24 (base=esp, index=none)
                if mod == 0b01:
                    form += b"\x00"                               # disp8
                elif mod == 0b10:
                    form += b"\x00\x00\x00\x00"                   # disp32
                if opcode == 0x83:
                    form += b"\x01"                               # imm8
                try:
                    NEW.decode(form, 0x00400000)
                    raises, msg = False, "NO RAISE — DECODED (DEFECT)"
                    regC_ok = False
                except (ValueError, IndexError) as exc:
                    raises, msg = True, f"{type(exc).__name__}: {exc}"
                regC_rows.append({"opcode": f"0x{opcode:02X}", "mod": mod, "reg": reg,
                                  "bytes": _hexsp(form), "rejected_at_decoder_level": raises,
                                  "rejection": msg})
    per_branch = {}
    for opcode in (0x8B, 0x89, 0x8D, 0x84, 0x83, 0xFF):
        rows = [r for r in regC_rows if r["opcode"] == f"0x{opcode:02X}"]
        per_branch[f"0x{opcode:02X}"] = {
            "forms": len(rows),
            "rejected": sum(1 for r in rows if r["rejected_at_decoder_level"]),
            "mechanism": (rows[0]["rejection"] if rows else None),
            "all_rejected": all(r["rejected_at_decoder_level"] for r in rows),
        }
    # form-set identity vs the cited Desktop sweep (production engine rows)
    desk_sweep_prod = [r for r in desktop_cc["sib_branch_sweep"] if r["engine"] == "production"]
    desk_forms = sorted(r["bytes"] for r in desk_sweep_prod)
    my_forms = sorted(r["bytes"].lower() for r in regC_rows)
    sweep_form_set_identical_to_desktop = my_forms == desk_forms

    # ---------- regression D: NC2/NC3 mechanisms + instruction-level diagnosis (cited Desktop reference)
    def _span_slice(case_key):
        ref = desktop_residual[DESKTOP_CASE_FOR[case_key]]["reference"]
        rows = [e for e in ref["listing"] if 0x0050A3DD <= int(e["va"], 16) <= 0x0050A3E8]
        return rows

    regression_D = {
        "NC2_NON_SIB_TEST_HIDDEN_EDI": {
            "new_production_rejection_mechanism": rejection_mechanisms["NC2_NON_SIB_TEST_HIDDEN_EDI"],
            "measured_rejection": post_matrix["NC2_NON_SIB_TEST_HIDDEN_EDI"]["decode_boundaries"]["rejection"],
            "cited_desktop_reference_decode_span": _span_slice("NC2_NON_SIB_TEST_HIDDEN_EDI"),
            "cited_desktop_edi_writes_in_required_interval":
                desktop_residual["NON_SIB_TEST_HIDDEN_EDI"]["reference"]["edi_writes_in_required_interval"],
            "instruction_level_diagnosis_cited": ("Desktop capstone 5.0.7 reference decode (CITED — not a new "
                                                   "measurement): 84 06 @0x0050A3DD is a 2-byte 'test byte ptr "
                                                   "[esi], al'; the following BF AA BB CC E8 @0x0050A3DF is a "
                                                   "5-byte 'mov edi, 0xe8ccbbaa' — an EDI WRITE INSIDE the "
                                                   "prohibited P2 interval (0x0050A3B7, 0x0050A3F6); tail 90 x5 "
                                                   "nops; true expected verdict FAIL. The sibfixed length logic "
                                                   "assigned 6 bytes to 84 06 and hid the EDI write (the "
                                                   "historical false pass); the corrected production now rejects "
                                                   "EVERY memory TEST form before any length computation."),
        },
        "NC3_INVALID_FF_FAR_CALL_REGISTER": {
            "new_production_rejection_mechanism": rejection_mechanisms["NC3_INVALID_FF_FAR_CALL_REGISTER"],
            "measured_rejection": post_matrix["NC3_INVALID_FF_FAR_CALL_REGISTER"]["decode_boundaries"]["rejection"],
            "cited_desktop_reference_meta": {
                "library": desktop_residual["INVALID_FF_FAR_CALL_REGISTER"]["reference"]["library"],
                "version": desktop_residual["INVALID_FF_FAR_CALL_REGISTER"]["reference"]["version"],
                "decoded_bytes": desktop_residual["INVALID_FF_FAR_CALL_REGISTER"]["reference"]["decoded_bytes"],
                "edi_writes_in_required_interval":
                    desktop_residual["INVALID_FF_FAR_CALL_REGISTER"]["reference"]["edi_writes_in_required_interval"],
                "note": "capstone decodes only the 38-byte prefix (stops at FF D8): FF /3 is CALLF m16:32 — a "
                        "memory-only form; FF D8 (mod=11) is an INVALID register encoding (undefined)",
            },
            "cited_desktop_historical_qc_internal_decode": ("the historical internal-QC decode accepted FF D8 via "
                                                            "its erroneous /3 branch as 'push eax' (2 bytes, no EDI "
                                                            "write) and PASSed the buffer — the NC3-A defect, "
                                                            "corrected on the QC side in the QC phase (NOT this "
                                                            "executor's scope); the historical production already "
                                                            "rejected it ('uncovered FF /3 mod=11') and this "
                                                            "successor keeps that behavior UNCHANGED"),
        },
        "NC3_INVALID_LEA_REGISTER": {
            "new_production_rejection_mechanism": rejection_mechanisms["NC3_INVALID_LEA_REGISTER"],
            "measured_rejection": post_matrix["NC3_INVALID_LEA_REGISTER"]["decode_boundaries"]["rejection"],
            "cited_desktop_reference_meta": {
                "library": desktop_residual["INVALID_LEA_REGISTER"]["reference"]["library"],
                "version": desktop_residual["INVALID_LEA_REGISTER"]["reference"]["version"],
                "decoded_bytes": desktop_residual["INVALID_LEA_REGISTER"]["reference"]["decoded_bytes"],
                "edi_writes_in_required_interval":
                    desktop_residual["INVALID_LEA_REGISTER"]["reference"]["edi_writes_in_required_interval"],
                "note": "capstone decodes only the 38-byte prefix (stops at 8D C0): LEA with mod=11 is an INVALID "
                        "x86 encoding",
            },
            "cited_desktop_historical_production_exception": ("sibfixed crashed inside LEA operand formatting with "
                                                               "'TypeError: unsupported format string passed to "
                                                               "NoneType.__format__' which escaped the checker — "
                                                               "reproduced in this run's PRE matrix as "
                                                               "ERROR:TypeError; the corrected successor returns "
                                                               "the controlled (False, diagnostic) verdict instead"),
            "cited_desktop_historical_qc_internal_decode": ("the historical internal-QC decode formatted 8D C0 as "
                                                             "a harmless 'lea eax, eax' (2 bytes, no EDI write) and "
                                                             "PASSed the buffer — the historical QC-side defect "
                                                             "(QC-phase scope, not this executor's)"),
        },
        "citation": {
            "file": DESKTOP_CC_PATH,
            "size_bytes": _size_file(DESKTOP_CC_PATH),
            "sha256": _sha256_file(DESKTOP_CC_PATH),
            "label": "SOURCE_DESKTOP_MEASUREMENT (Desktop post-audit of 91598a98) — cited reference decode, "
                     "NOT a new measurement by this run; nothing installed",
        },
    }

    # ---------- register-form support verification (NC3-B side condition) + negative controls
    reg_support = {}
    reg_support_ok = True
    for name, bhex, want_mn, want_ops in [
        ("mov_reg_8B_F8 (the P1 head form)", "8B F8", "mov", "edi, eax"),
        ("mov_reg_8B_C0", "8B C0", "mov", "eax, eax"),
        ("mov_reg_89_C8", "89 C8", "mov", "eax, ecx"),
        ("test_reg_84_C0 (register TEST stays supported)", "84 C0", "test", "al, al"),
        ("lea_mem_8D_06 (memory LEA stays supported)", "8D 06", "lea", "eax, dword ptr [esi + 0x0]"),
        ("call_reg_FF_D2 (the P4 endpoint form)", "FF D2", "call", "edx"),
    ]:
        b = bytes.fromhex(bhex)
        try:
            ins = NEW.decode(b, 0x00400000)
            got = ins[0x00400000]
            decoded, mn, ops = True, got.mnemonic, got.op_str
        except (ValueError, IndexError) as exc:
            decoded, mn, ops = False, None, f"{type(exc).__name__}: {exc}"
        ok = decoded and mn == want_mn and ops == want_ops
        reg_support[name] = {"bytes": bhex, "decoded": decoded, "mnemonic": mn, "operands": ops,
                             "expected": [want_mn, want_ops], "supported_as_before": ok}
        reg_support_ok = reg_support_ok and ok
    negative_controls = {}
    for name, bhex, want_mech in [
        ("NC3B lea_reg_8D_C0 must raise", "8D C0", "unsupported LEA register form"),
        ("NC2 test_mem_84_06 must raise", "84 06", "unsupported memory TEST form"),
        ("NC2 test_mem_84_44_24_00 must raise (SIB first)", "84 44 24 00", "unsupported SIB form"),
        ("NC3 ff_3_FF_D8 must raise", "FF D8", "uncovered FF /3"),
    ]:
        b = bytes.fromhex(bhex)
        try:
            NEW.decode(b, 0x00400000)
            raised, msg = False, "NO RAISE — DECODED (DEFECT)"
            reg_support_ok = False
        except (ValueError, IndexError) as exc:
            raised, msg = True, f"{type(exc).__name__}: {exc}"
        ok = raised and want_mech in msg
        negative_controls[name] = {"bytes": bhex, "raised": raised, "rejection": msg,
                                   "mechanism_as_expected": ok}
        reg_support_ok = reg_support_ok and ok

    # ---------- POST document
    post_doc = {
        "RUN_ID": RUN_ID,
        "RUN_CLASS": RUN_CLASS,
        "purpose": ("corrected-production (POST) eight-case matrix results produced by the ACTUAL corrected "
                    "production checker (dispatch STEP 2) + regressions A-D (dispatch STEP 4)"),
        "input_identities_remeasured_at_run_time": input_identities,
        "production_checker": {
            "script": "03_SCRIPTS/ctrl4_exact_endpoint_nc23fixed.py",
            "script_sha256": new_prod_sha,
            "function": "ctrl4_exact_endpoint — EXECUTED via importlib import of "
                        "ctrl4_exact_endpoint_nc23fixed.py (the ACTUAL corrected production function; NOT a "
                        "rewritten imitation; NOT hardcoded results)",
            "successor_of": ("SOURCE_PACKAGE docs/audits/PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_"
                             "CORRECTION_R1_20261007/03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py as published at "
                             "91598a9868037c4954e22e16c535d6a5a671771e, SHA256 " + hist_prod_sha),
            "corrections": {
                "NC2": "0x84 branch: ALL memory TEST forms (mod != 0b11) rejected fail-closed BEFORE any length "
                       "computation; register TEST (84 C0) stays supported; memory TEST decoding NOT added",
                "NC3_B": "0x8D branch: LEA with mod=11 rejected explicitly (ValueError) BEFORE operand formatting "
                         "and verdict computation — checker returns (False, diagnostic), never a TypeError",
                "NC3_FF_branch": "UNCHANGED from sibfixed: only FF /2 (call r/m32) with mod=11 accepted (FF D2 "
                                 "endpoint); everything else raises; FF /6 and other forms NOT added",
                "NC1_PRESERVED": "the fail-closed SIB guard (mod != 0b11 and rm == 0b100) stays in EVERY "
                                  "memory-ModRM branch (0x8B/0x89/0x8D, 0x84, 0x83, 0xFF) before any "
                                  "displacement/length computation",
                "P3_grp1_imm8_fix_kept": True,
                "p1_p4_predicate_unchanged": True,
                "checker_catch_unchanged": "only (ValueError, IndexError); unexpected exceptions propagate "
                                           "(no blanket catch)",
            },
            "fixture_identity_with_historical_sibfixed": fixture_identity,
            "buffers_byte_identical_between_hist_derived_and_new_module_builders": buffers_byte_identical,
            "exe_accessed": False,
            "buffers_synthetic_in_memory_only": True,
        },
        "nc23_matrix_post": post_matrix,
        "decode_rejection_mechanisms": rejection_mechanisms,
        "clean_window_full_decode_listing": {
            "provenance": ("the published 0x42 clean window (PRIOR_SCIENCE_PACKAGE 01_RAW/"
                           "JOIN_WINDOW_50A3B7_REPIN.txt, pinned SHA256 "
                           + PINNED_INPUTS["published_window_record"]["sha256"] + "); decode by the ACTUAL "
                           "corrected module — proving the NC2/NC3 changes altered NO clean boundary"),
            "instruction_count": len(clean_listing),
            "total_bytes": sum(r["size"] for r in clean_listing),
            "listing": clean_listing,
            "boundary_regression_A": boundary_regression,
        },
        "regression_B_sib_9_case_battery": {
            "source": ("the 9-form SIB battery AST-EXTRACTED as a constant from the historical "
                       "00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py (SIB_BATTERY; historical top level NEVER "
                       "run) — re-run against the NEW production decode at the DECODER level"),
            "rows": regB_rows,
            "all_nine_rejected_fail_closed": regB_ok,
        },
        "regression_C_144_form_sweep": {
            "description": ("Desktop sweep mirrored against the NEW production decode at the DECODER level: 6 "
                            "opcode branches (8B/89/8D/84/83/FF) x 3 memory mod (00/01/10) x 8 reg, always "
                            "rm=4 -> 144 synthetic SIB forms; every form must be REJECTED by decode itself "
                            "(decode raises) — recorded per form with the exact rejection; a decoder-level "
                            "reject is NOT presented as a whole-checker P1 FAIL"),
            "per_branch_counts": per_branch,
            "total_forms": len(regC_rows),
            "all_144_rejected_at_decoder_level": regC_ok,
            "form_set_identical_to_cited_desktop_sweep": sweep_form_set_identical_to_desktop,
            "raw_forms": regC_rows,
        },
        "regression_D_rejection_mechanisms_and_diagnosis": regression_D,
        "register_form_support_verification": {
            "description": ("0x8B/0x89 register forms, register TEST (84 C0), memory LEA (8D 06) and the FF D2 "
                            "endpoint remain supported EXACTLY as before; NC2/NC3-B negative controls must raise "
                            "with the expected mechanism"),
            "positive_controls": reg_support,
            "negative_controls": negative_controls,
            "result": "PASS" if reg_support_ok else "FAIL",
        },
        "matrix_verdict": "PASS" if post_all else "FAIL",
        "verdict_semantics": ("all eight measured results equal the mandatory expectations (clean PASS; clobber/"
                              "esi/nop/NC1 SIB/NC2 TEST/NC3 FF D8/NC3 LEA FAIL) of the corrected production "
                              "checker, with regressions A-D recorded. Strongest permitted claim for this "
                              "executor phase: the NC2/NC3 defects are corrected and revalidated WITHIN THE "
                              "TEST SCOPE of this matrix and battery (the fresh internal QC + final naming of "
                              "CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE belong to the QC phase, not this "
                              "executor). NEVER claimed: GENERAL_X86_DECODER_PROVEN — both engines cover only "
                              "the window's opcode universe and reject everything else fail-closed. This is "
                              "QC-machinery correction only; it creates no science and retracts no historical "
                              "result."),
        "determinism": "no timestamps; all rows machine-measured in this run",
    }

    # ---------- persist (UTF-8, LF, no BOM; deterministic)
    pre_path = os.path.join(PKG, "CONTROL_RESULTS_PRE.json")
    post_path = os.path.join(PKG, "CONTROL_RESULTS_POST.json")
    for path, doc in ((pre_path, pre_doc), (post_path, post_doc)):
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
            f.write("\n")

    # ---------- console summary (transcript evidence; the JSON files are the persisted record)
    print(f"RUN_ID: {RUN_ID}")
    print(f"input pins re-measured: {'ALL MATCH' if pins_ok else 'MISMATCH'}")
    print(f"corrected production (nc23fixed) SHA256: {new_prod_sha}")
    print(f"historical sibfixed (READ-ONLY) SHA256: {hist_prod_sha}")
    print(f"historical QC script (READ-ONLY) SHA256: {hist_qc_sha}")
    print(f"fixture identity (new vs historical sibfixed): {fixture_identity}")
    print(f"buffer sets byte-identical (hist-derived vs new-module builders): {buffers_byte_identical}")
    print("\nPOST matrix (ACTUAL corrected production function):")
    for name in CASE_ORDER:
        r = post_matrix[name]
        print(f"  {name:34s} expected={r['expected']:4s} actual={r['actual']:4s} match={r['match']}")
    print(f"  -> matrix_verdict: {post_doc['matrix_verdict']}")
    for name in ("NC2_NON_SIB_TEST_HIDDEN_EDI", "NC3_INVALID_FF_FAR_CALL_REGISTER", "NC3_INVALID_LEA_REGISTER"):
        print(f"  rejection {name}: {post_matrix[name]['decode_boundaries'].get('rejection')}")
    print(f"\nregression A (clean map vs published record): {boundary_regression['result']} "
          f"({boundary_regression['instruction_count']} insns, {boundary_regression['total_bytes']:#x} bytes)")
    print(f"regression B (9-form SIB battery vs new decode): "
          f"{'ALL REJECTED' if regB_ok else 'DEFECT — see rows'}")
    print(f"regression C (144-form sweep vs new decode): "
          f"{'ALL REJECTED' if regC_ok else 'DEFECT — see rows'}; form set == Desktop sweep: "
          f"{sweep_form_set_identical_to_desktop}")
    print(f"register-form support + negative controls: "
          f"{post_doc['register_form_support_verification']['result']}")
    print("\nPRE matrix (HISTORICAL production / HISTORICAL internal QC — AST-extracted, top level NEVER run):")
    for name in CASE_ORDER:
        r = pre_matrix[name]
        print(f"  {name:34s} exp prod={r['expected']['production']:14s} actual prod={r['actual']['production']:14s}"
              f" | exp qc={r['expected']['internal_qc']:4s} actual qc={r['actual']['internal_qc']:4s}"
              f" | reproduced={r['production_reproduced'] and r['internal_qc_reproduced']}")
    print(f"  -> PRE_REPRODUCED (all 8 cases, both historical checkers): {pre_all}")
    print(f"\nwrote: {post_path}")
    print(f"wrote: {pre_path}")

    gates = {
        "input_pins": pins_ok,
        "post_matrix_8_rows": post_all,
        "production_authenticity": fixture_identity and buffers_byte_identical,
        "regression_A_clean_map": boundary_regression["result"] == "PASS",
        "regression_B_sib9": regB_ok,
        "regression_C_sweep144": regC_ok,
        "nc23_explicit_rejections_no_error": all(
            post_matrix[n]["actual"] == "FAIL" and post_matrix[n]["decode_boundaries"]["decode_status"]
            == "REJECTED_FAIL_CLOSED" for n in ("NC1_SIB_HIDDEN_EDI_WRITE", "NC2_NON_SIB_TEST_HIDDEN_EDI",
                                                "NC3_INVALID_FF_FAR_CALL_REGISTER", "NC3_INVALID_LEA_REGISTER")),
        "register_form_support": reg_support_ok,
        "desktop_case_buffer_identity": all(v["byte_identical_to_executor_buffer"]
                                            for v in desktop_buffer_identity.values()),
    }
    print("\nGATES: " + json.dumps(gates))
    overall = all(gates.values())
    print(f"OVERALL: {'PASS' if overall else 'FAIL'}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
