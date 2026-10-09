#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""run_pre_counterexamples.py — PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009

PRE phase (contract section 5) — reproduce the CMO-C1 false PASS using the EXACT
historical implementations, BEFORE any correction.

Method (fail-closed, immutable-evidence):
  * The historical scripts are NEVER executed at top level and NEVER imported as
    modules (repin_write_provenance.py's module level mutates sys.path and imports
    an external module; both mains() write into the historical package). Instead
    the required definitions are AST-EXTRACTED by name from the parsed sources and
    exec'd in isolated namespaces. The free-name sets of the extracted functions
    are verified against the injected namespace (completeness check).
  * The historical executor ECX-clobber scan (an inline comprehension in main(),
    source lines 444-446) is lifted VERBATIM from the source text and executed
    byte-for-byte (the executed code IS the historical code, minus the results[]
    assignment on line 447).
  * The historical QC ECX scan helper `writers_between` (nested def in main(),
    source lines 497-499) is AST-extracted, and its historical call expression
    (source line 509) is lifted VERBATIM and eval'd byte-for-byte.
  * Mutants are IN-MEMORY ONLY (window copy for the executor decoder; full-image
    copy for the QC decoder, whose linear_decode path requires a PE image). The
    physical EXE is never modified and the mutant is never hashed or presented as
    the original.
  * Supplementary (clearly labeled non-historical) EBP-interval scan documents
    the false EBP attribution inside the reaching-definition interval.
  * Historical 8x8 alias-matrix census (64 cases x 2 historical decoders = 128
    historical decode outcomes) documents the blast radius of the alias-index
    defect (expected-wrong values for high aliases; low-alias correctness is
    COINCIDENCE, not correctness of the mapping).

Outputs (written ONLY under this package's OUTPUT_ROOT):
  00_PRE/PRE_COUNTEREXAMPLES.json
  00_PRE/PRE_SHA256_INDEX.csv

python -B; stdlib only; no residue.
"""
import ast
import builtins
import csv
import hashlib
import json
import os
import struct
import sys

RUN_ID = "PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009"
HERE = os.path.dirname(os.path.abspath(__file__))            # OUTPUT_ROOT/03_SCRIPTS
PKG = os.path.dirname(HERE)                                   # OUTPUT_ROOT
REPO = os.path.dirname(os.path.dirname(os.path.dirname(PKG)))  # repo root
SOURCE_PKG = os.path.join(
    REPO, "docs", "audits",
    "PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009")
EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
CONTRACT_PATH = (r"C:\Users\User\Documents\ChatGPT\PE"
                 r"\PE_CMO_C1_HIGH_BYTE_CORRECTION_PROMPT_20261008"
                 r"\OPENCODE_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009.md")

# ---- fail-closed identities (contract section 2) ----------------------------
EXPECTED = {
    "exe": (8015872,
            "E7785430E81DFFE648CE8F5312414B17"
            "BC9FCE61389689A22F753765D5280F31"),
    "repin_write_provenance.py": (34043, "45120C91AD6A94A79C56E9B06F1C035481FB99"
                                   "D3017688E7F589732BEC6EE931"),
    "qc_remeasure.py": (31970, "4E5426AEAB8FBD9A9364A5FE445ED2EA7C5D9F4B"
                        "3E2F2E71B3EB5B3F3F8DDE1A"),
    "CONTROL_RESULTS.json": (18509, "9545D0D78881C29BC805EA3A05C8AA936D364256"
                             "671D31A1AE907677A63DE2F8"),
    "QC_RESULTS.json": (31350, "DE7DF210FAFA465E27D7A7C4410C9D9C44C9BAE1"
                        "492B9FEDE2B3101F01BF0545"),
    "contract": (16623, "61AAA55854942A22085F3767A7D64512248EDFAE3A7B9BB54A5CB"
                "E36F36D3981"),
}

W1_VA = 0x0085B1A8
W1_LEN = 232
FN_START = 0x0085B1B0
FN_END = 0x0085B290
MUT_VA = 0x0085B24D
MUT_ORIG = b"\xD9\xE8"      # fld1
MUT_CH = b"\x88\xDD"        # mov ch, bl  (ModRM DD: mod=3 reg=3(BL) rm=5(CH))
MUT_CL = b"\x88\xD9"        # mov cl, bl  (ModRM D9: mod=3 reg=3(BL) rm=1(CL))

# independent reference (for the historical blast-radius census; NOT the
# production mapping helper — this is PRE, describing expected-wrong history)
REF_ALIAS = [
    ("al", "eax", [0, 8]), ("cl", "ecx", [0, 8]),
    ("dl", "edx", [0, 8]), ("bl", "ebx", [0, 8]),
    ("ah", "eax", [8, 16]), ("ch", "ecx", [8, 16]),
    ("dh", "edx", [8, 16]), ("bh", "ebx", [8, 16]),
]
BUILTINS = set(dir(builtins))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def hx(b):
    return " ".join("%02X" % c for c in b)


def die(msg):
    sys.stderr.write("FAIL-CLOSED: %s\n" % msg)
    sys.exit(2)


# ---------------------------------------------------------------------------
# AST extraction
# ---------------------------------------------------------------------------
def extract_top(tree, consts, classes, funcs):
    got_c, got_k, got_f = {}, {}, {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)):
            if node.targets[0].id in consts:
                got_c[node.targets[0].id] = node
        elif isinstance(node, ast.ClassDef) and node.name in classes:
            got_k[node.name] = node
        elif isinstance(node, ast.FunctionDef) and node.name in funcs:
            got_f[node.name] = node
    return got_c, got_k, got_f


def extract_nested(main_node, names):
    out = {}
    for node in ast.walk(main_node):
        if isinstance(node, ast.FunctionDef) and node.name in names:
            out[node.name] = node
    return out


def func_free_names(func_node):
    """Names a function loads but neither stores nor takes as parameters."""
    loads, stores, params = set(), set(), set()
    for node in ast.walk(func_node):
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Load):
                loads.add(node.id)
            else:
                stores.add(node.id)
        elif isinstance(node, ast.arguments):
            for a in (list(node.args) + list(node.posonlyargs)
                      + list(node.kwonlyargs)
                      + ([node.vararg] if node.vararg else [])
                      + ([node.kwarg] if node.kwarg else [])):
                params.add(a.arg)
        elif isinstance(node, ast.Lambda):
            for a in (list(node.args.args) + list(node.args.posonlyargs)
                      + list(node.args.kwonlyargs)
                      + ([node.args.vararg] if node.args.vararg else [])
                      + ([node.args.kwarg] if node.args.kwarg else [])):
                params.add(a.arg)
    return sorted(loads - stores - params - BUILTINS)


def exec_nodes(nodes, namespace, srcname):
    mod = ast.Module(body=list(nodes), type_ignores=[])
    ast.fix_missing_locations(mod)
    code = compile(mod, srcname, "exec")
    exec(code, namespace)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    R = {"run_id": RUN_ID, "phase": "PRE_COUNTEREXAMPLES",
         "generator": "03_SCRIPTS/run_pre_counterexamples.py (python -B)",
         "python": sys.version.split()[0]}

    # ---- 0. fail-closed input identities ----------------------------------
    ids = {}
    src_scripts = {}
    for fn in ("repin_write_provenance.py", "qc_remeasure.py"):
        p = os.path.join(SOURCE_PKG, "03_SCRIPTS", fn)
        size, sha = os.path.getsize(p), sha256_file(p)
        exp = EXPECTED[fn]
        if (size, sha) != exp:
            die("source script identity mismatch: %s (%s, %s) != (%s, %s)"
                % (fn, size, sha, exp[0], exp[1]))
        ids[fn] = {"size": size, "sha256": sha, "match": True,
                   "path": os.path.relpath(p, REPO).replace("\\", "/")}
        src_scripts[fn] = p
    for fn in ("CONTROL_RESULTS.json", "QC_RESULTS.json"):
        p = os.path.join(SOURCE_PKG, fn)
        size, sha = os.path.getsize(p), sha256_file(p)
        exp = EXPECTED[fn]
        if (size, sha) != exp:
            die("source artifact identity mismatch: %s" % fn)
        ids[fn] = {"size": size, "sha256": sha, "match": True,
                   "path": os.path.relpath(p, REPO).replace("\\", "/")}
    csize, csha = os.path.getsize(CONTRACT_PATH), sha256_file(CONTRACT_PATH)
    if (csize, csha) != EXPECTED["contract"]:
        die("contract identity mismatch")
    ids["contract"] = {"size": csize, "sha256": csha, "match": True,
                       "path": CONTRACT_PATH}
    R["input_identities"] = ids

    exe_size, exe_sha = os.path.getsize(EXE_PATH), sha256_file(EXE_PATH)
    if (exe_size, exe_sha) != EXPECTED["exe"]:
        die("EXE identity mismatch: %s / %s" % (exe_size, exe_sha))
    R["exe_identity"] = {"size": exe_size, "sha256": exe_sha,
                         "policy": "read-only; mutants are in-memory copies; "
                                   "the physical file is never modified and "
                                   "never rehashed as the original"}

    # ---- 1. AST extraction of the historical implementations -------------
    with open(src_scripts["repin_write_provenance.py"], "r",
              encoding="utf-8") as f:
        ex_src = f.read()
    with open(src_scripts["qc_remeasure.py"], "r", encoding="utf-8") as f:
        qc_src = f.read()
    ex_tree = ast.parse(ex_src)
    qc_tree = ast.parse(qc_src)

    ex_c, ex_k, ex_f = extract_top(
        ex_tree, consts=["REGS", "R8", "R16"], classes=["DecodeError"],
        funcs=["_modrm", "_fmt_mem", "decode_instruction",
               "linear_decode_window", "hexs"])
    ex_names = (set(ex_c) | set(ex_k) | set(ex_f))
    if ex_names != {"REGS", "R8", "R16", "DecodeError", "_modrm", "_fmt_mem",
                    "decode_instruction", "linear_decode_window", "hexs"}:
        die("executor AST extraction incomplete: %s" % sorted(ex_names))
    ex_ns = {"struct": struct, "__builtins__": builtins}
    exec_nodes([ex_c["REGS"], ex_c["R8"], ex_c["R16"],
                ex_k["DecodeError"],
                ex_f["_modrm"], ex_f["_fmt_mem"], ex_f["decode_instruction"],
                ex_f["linear_decode_window"], ex_f["hexs"]],
               ex_ns, "<repin_write_provenance_extracted>")

    qc_c, qc_k, qc_f = extract_top(
        qc_tree, consts=["GPR", "GPR8", "GPR16"],
        classes=["QcDecodeError", "MyPE"],
        funcs=["my_modrm", "_mem_str", "my_decode", "linear_decode", "hx"])
    qc_main = next(n for n in qc_tree.body
                   if isinstance(n, ast.FunctionDef) and n.name == "main")
    qc_nested = extract_nested(qc_main, ["writers_between", "calls_between"])
    if set(qc_nested) != {"writers_between", "calls_between"}:
        die("QC nested scan helpers not found")
    qc_names = set(qc_c) | set(qc_k) | set(qc_f) | set(qc_nested)
    if qc_names != {"GPR", "GPR8", "GPR16", "QcDecodeError", "MyPE",
                    "my_modrm", "_mem_str", "my_decode", "linear_decode",
                    "hx", "writers_between", "calls_between"}:
        die("QC AST extraction incomplete: %s" % sorted(qc_names))
    qc_ns = {"struct": struct, "__builtins__": builtins}
    exec_nodes([qc_c["GPR"], qc_c["GPR8"], qc_c["GPR16"],
                qc_k["QcDecodeError"], qc_k["MyPE"],
                qc_f["my_modrm"], qc_f["_mem_str"], qc_f["my_decode"],
                qc_f["linear_decode"], qc_f["hx"],
                qc_nested["writers_between"], qc_nested["calls_between"]],
               qc_ns, "<qc_remeasure_extracted>")

    # free-name completeness verification (documented evidence)
    free_report = {"executor": {}, "qc": {}}
    for name in ("_modrm", "_fmt_mem", "decode_instruction",
                 "linear_decode_window", "hexs"):
        fn_free = func_free_names(ex_f[name])
        unresolved = [n for n in fn_free
                     if n not in ex_names and n not in ex_ns]
        free_report["executor"][name] = {"free_names": fn_free,
                                         "unresolved": unresolved}
        if unresolved:
            die("executor extraction incomplete for %s: %s"
                % (name, unresolved))
    for name in ("my_modrm", "_mem_str", "my_decode", "linear_decode", "hx"):
        fn_free = func_free_names(qc_f[name])
        unresolved = [n for n in fn_free
                     if n not in qc_names and n not in qc_ns]
        free_report["qc"][name] = {"free_names": fn_free,
                                   "unresolved": unresolved}
        if unresolved:
            die("QC extraction incomplete for %s: %s" % (name, unresolved))
    wb_free = func_free_names(qc_nested["writers_between"])
    free_report["qc"]["writers_between"] = {
        "free_names": wb_free,
        "note": "ins_list is resolved at call time from this namespace "
                "(the historical closure over main()'s local ins_list is "
                "reproduced by binding ins_list in the namespace before the "
                "verbatim call)"}
    if wb_free != ["ins_list"]:
        die("unexpected writers_between free-name set: %s" % wb_free)
    R["ast_extraction"] = {
        "policy": "the historical scripts were NEVER executed at top level "
                  "and NEVER imported as modules; definitions were "
                  "AST-extracted by name and exec'd in isolated namespaces "
                  "(struct injected as the only external dependency, matching "
                  "the historical module imports used by these definitions)",
        "executor_script": {
            "path": ids["repin_write_provenance.py"]["path"],
            "extracted": ["REGS", "R8", "R16", "DecodeError", "_modrm",
                         "_fmt_mem", "decode_instruction",
                         "linear_decode_window", "hexs"],
            "not_extracted_not_executed": ["main", "build_selected_txt",
                                           "module-level imports (sys.path "
                                           "insertion + checker_plus4_"
                                           "successor_v2 import)", "RUN_ID",
                                           "OUT_RAW and all package-file "
                                           "writes"],
            "top_level_effects_avoided": "the executor script's module level "
                                         "inserts SOURCE_B_DIR into sys.path "
                                         "and imports checker_plus4_"
                                         "successor_v2; its main() writes "
                                         "01_RAW/SELECTED_WRITE_BYTES.txt "
                                         "and CONTROL_RESULTS.json into the "
                                         "HISTORICAL package - none of this "
                                         "ran",
            "free_name_verification": free_report["executor"]},
        "qc_script": {
            "path": ids["qc_remeasure.py"]["path"],
            "extracted": ["GPR", "GPR8", "GPR16", "QcDecodeError", "MyPE",
                          "my_modrm", "_mem_str", "my_decode",
                          "linear_decode", "hx",
                          "writers_between (nested def inside main, AST-"
                          "extracted)", "calls_between (nested, extracted for "
                          "completeness of the historical scan helper set)"],
            "not_extracted_not_executed": ["main", "module-level constants "
                                           "(EXE paths, pins dict, regexes)",
                                           "the package-wide token/epistemology "
                                           "file scans"],
            "top_level_effects_avoided": "the QC script's main() loads the "
                                         "EXE and walks the ENTIRE historical "
                                         "package scanning files - none of "
                                         "this ran",
            "free_name_verification": free_report["qc"]}}

    # ---- 2. verbatim historical scan extraction ----------------------------
    ex_lines = ex_src.splitlines()
    scan_text = "\n".join(l[4:] for l in ex_lines[443:446])  # source lines 444-446
    scan_expected = ('ecx_writers = [i["va"] for i in ins_list\n'
                     '               if 0x0085B24B < i["va"] < 0x0085B27A\n'
                     '               and "ecx" in i["writes"]]')
    qc_lines = qc_src.splitlines()
    call_line = qc_lines[508].strip()          # source line 509
    if call_line.endswith(","):
        call_text = call_line[:-1]
    else:
        die("QC scan call line does not end with a comma")
    call_expected = 'writers_between(0x0085B24B, 0x0085B27A - 1, "ecx")'
    verbatim_ok = (scan_text == scan_expected and call_text == call_expected)
    if not verbatim_ok:
        die("verbatim scan transcription mismatch (executor=%s, qc=%s)"
            % (scan_text == scan_expected, call_text == call_expected))
    R["scan_verbatim"] = {
        "executor_scan": {
            "source": "repin_write_provenance.py main(), source lines 444-446",
            "verbatim_text": scan_text,
            "byte_for_byte_verified": True,
            "execution": "the VERBATIM extracted text itself is exec'd with "
                         "ins_list bound to the decoded window (line 447's "
                         "results[] assignment is the only omitted context)"},
        "qc_scan": {
            "helper_source": "qc_remeasure.py main(), nested def "
                             "writers_between, source lines 497-499 "
                             "(AST-extracted)",
            "call_source": "qc_remeasure.py main(), source line 509",
            "verbatim_call_text": call_text,
            "byte_for_byte_verified": True,
            "execution": "the VERBATIM extracted call is eval'd in the QC "
                         "namespace with ins_list bound to the decoded window"}}

    def run_ex_ecx_scan(ins_list):
        ns = {"ins_list": ins_list, "__builtins__": builtins}
        exec(compile(scan_text, "<historical_executor_scan_verbatim>", "exec"),
             ns)
        return list(ns["ecx_writers"])

    def run_qc_ecx_scan(ins_list):
        qc_ns["ins_list"] = ins_list
        return list(eval(compile(call_text,
                                 "<historical_qc_scan_call_verbatim>",
                                 "eval"), qc_ns))

    def supp_ebp_scan(ins_list):
        # SUPPLEMENTARY (NOT historical): documents the false EBP attribution
        # landing inside the same reaching-definition interval.
        return [i["va"] for i in ins_list
                if 0x0085B24B < i["va"] < 0x0085B27A
                and "ebp" in i["writes"]]

    # ---- 3. physical window identity --------------------------------------
    with open(EXE_PATH, "rb") as f:
        exe_bytes = f.read()
    if hashlib.sha256(exe_bytes).hexdigest().upper() != EXPECTED["exe"][1]:
        die("EXE bytes changed during load")
    pe_clean = qc_ns["MyPE"](exe_bytes)
    w1 = pe_clean.read(W1_VA, W1_LEN)
    with open(os.path.join(SOURCE_PKG, "CONTROL_RESULTS.json"), "r",
              encoding="utf-8") as f:
        committed = json.load(f)
    w1_committed_hex = committed["windows"]["W1"]["hex"]
    w1_own_hex = hx(w1)
    if w1_own_hex != w1_committed_hex:
        die("W1 byte identity vs committed CONTROL_RESULTS failed")
    win_off = MUT_VA - FN_START
    win = bytes(w1[FN_START - W1_VA: FN_END - W1_VA])
    if len(win) != 224 or win[win_off:win_off + 2] != MUT_ORIG:
        die("window slice invalid (len=%s, bytes at mutation site=%s)"
            % (len(win), hx(win[win_off:win_off + 2])))
    mut_file_off = pe_clean.off(MUT_VA, 2)
    # cross-check base: 4567464 is the COMMITTED raw offset of W1_VA=0x0085B1A8
    # (source CONTROL_RESULTS.json windows.W1.raw_offset); the mutation-site
    # offset must be that base plus (MUT_VA - W1_VA) = 165.
    mut_off_expected = 4567464 + (MUT_VA - W1_VA)
    R["window_identity"] = {
        "w1_own_hex": w1_own_hex,
        "w1_committed_hex_match": True,
        "window": "[0x0085B1B0, 0x0085B290) 224 bytes",
        "mutation_site": {"va": "0x%08X" % MUT_VA, "window_offset": win_off,
                          "file_offset": mut_file_off,
                          "original_bytes": hx(MUT_ORIG),
                          "expected_file_offset": mut_off_expected,
                          "expected_offset_formula":
                              "committed W1 raw_offset 4567464 (VA 0x0085B1A8) "
                              "+ (MUT_VA - W1_VA = 165)",
                          "file_offset_consistent":
                              mut_file_off == mut_off_expected},
        "exe_hash_after_load_recheck": hashlib.sha256(
            pe_clean.data).hexdigest().upper()}
    if mut_file_off != mut_off_expected:
        die("mutation-site file offset %s != expected %s"
            % (mut_file_off, mut_off_expected))

    # ---- 4. decode + scan helpers per case --------------------------------
    def ser_ins(i, impl):
        d = {"va": "0x%08X" % i["va"], "va_int": i["va"],
             "length": i["length"], "bytes": hx(i["bytes"]),
             "mnemonic": i.get("mnemonic"),
             "text": i.get("text"), "dst": i.get("dst"),
             "src": i.get("src"), "width": i.get("width"),
             "writes": sorted(i["writes"]), "reads": sorted(i["reads"]),
             "mem_dst": i.get("mem_dst"), "prefix66": i.get("prefix66"),
             "impl": impl}
        for k in ("call_target",):
            if i.get(k) is not None:
                d[k] = "0x%08X" % i[k]
        return d

    def dec_executor(window_bytes):
        ins = ex_ns["linear_decode_window"](window_bytes, FN_START,
                                            FN_START, FN_END)
        return ins

    def dec_qc(full_image_bytes):
        pe = qc_ns["MyPE"](full_image_bytes)
        ins = qc_ns["linear_decode"](pe, FN_START, FN_END)
        return ins

    def summary(ins):
        last = ins[-1]
        return {"instruction_count": len(ins),
                "total_bytes": sum(i["length"] for i in ins),
                "end_va": "0x%08X" % (last["va"] + last["length"]),
                "end_exact_0x0085B290":
                    last["va"] + last["length"] == FN_END}

    def at(ins, va):
        for i in ins:
            if i["va"] == va:
                return i
        return None

    def make_window_mutant(newbytes):
        w = bytearray(win)
        w[win_off] = newbytes[0]
        w[win_off + 1] = newbytes[1]
        return bytes(w)

    def make_full_mutant(newbytes):
        m = bytearray(exe_bytes)
        m[mut_file_off] = newbytes[0]
        m[mut_file_off + 1] = newbytes[1]
        return bytes(m)

    def build_case(name, mut_bytes, impl):
        rec = {"case_id": name, "implementation": impl}
        try:
            if impl == "executor":
                ins = dec_executor(make_window_mutant(mut_bytes)
                                   if mut_bytes else win)
            else:
                ins = dec_qc(make_full_mutant(mut_bytes)
                             if mut_bytes else exe_bytes)
            rec["decode"] = summary(ins)
            site = at(ins, MUT_VA)
            if site is None:
                raise RuntimeError("no instruction at mutation site")
            rec["mutation_site_instruction"] = ser_ins(site, impl)
            if impl == "executor":
                rec["scans"] = {
                    "historical_executor_ecx_scan_(0x0085B24B,0x0085B27A)":
                        ["0x%08X" % v for v in run_ex_ecx_scan(ins)],
                    "supplementary_nonhistorical_ebp_scan":
                        ["0x%08X" % v for v in supp_ebp_scan(ins)]}
            else:
                rec["scans"] = {
                    "historical_qc_ecx_scan_(0x0085B24B,0x0085B27A)":
                        ["0x%08X" % v for v in run_qc_ecx_scan(ins)]}
            rec["status"] = "OK"
        except Exception as e:  # preserve evidence of any failure
            rec["status"] = "DECODE_EXCEPTION"
            rec["exception"] = "%s: %s" % (type(e).__name__, e)
        return rec

    cases = {}
    cases["PRE-EX-CLEAN"] = build_case("PRE-EX-CLEAN", None, "executor")
    cases["PRE-QC-CLEAN"] = build_case("PRE-QC-CLEAN", None, "qc")
    cases["PRE-EX-CH"] = build_case("PRE-EX-CH", MUT_CH, "executor")
    cases["PRE-QC-CH"] = build_case("PRE-QC-CH", MUT_CH, "qc")
    cases["PRE-EX-CL"] = build_case("PRE-EX-CL", MUT_CL, "executor")
    cases["PRE-QC-CL"] = build_case("PRE-QC-CL", MUT_CL, "qc")
    for cid, c in cases.items():
        if c["status"] != "OK":
            die("case %s failed: %s" % (cid, c.get("exception")))
        if not c["decode"]["end_exact_0x0085B290"] \
                or c["decode"]["instruction_count"] != 64:
            die("case %s decode boundary/count unexpected: %s"
                % (cid, c["decode"]))

    # expected-value adjudication (PRE falsifiers F-PRE-1..7)
    def ex_scan(c):
        return c["scans"][
            "historical_executor_ecx_scan_(0x0085B24B,0x0085B27A)"]

    def qc_scan(c):
        return c["scans"][
            "historical_qc_ecx_scan_(0x0085B24B,0x0085B27A)"]

    ch_ex = cases["PRE-EX-CH"]["mutation_site_instruction"]
    ch_qc = cases["PRE-QC-CH"]["mutation_site_instruction"]
    clean_ex = cases["PRE-EX-CLEAN"]["mutation_site_instruction"]
    clean_qc = cases["PRE-QC-CLEAN"]["mutation_site_instruction"]
    cl_ex = cases["PRE-EX-CL"]["mutation_site_instruction"]
    cl_qc = cases["PRE-QC-CL"]["mutation_site_instruction"]

    adj = {
        "F-PRE-1_executor_ch_writes_is_ebp_NOT_ecx": {
            "measured_writes": ch_ex["writes"],
            "expected_wrong_value": ["ebp"],
            "reproduced": ch_ex["writes"] == ["ebp"],
            "dst_string_correct_anyway": ch_ex["dst"] == "ch",
            "reads_measured": ch_ex["reads"],
            "reads_note": "reads=['ebx'] is BL's parent - correct only by "
                          "LOW-ALIAS COINCIDENCE (REGS[3]==ebx==parent(BL))"},
        "F-PRE-2_executor_ch_ecx_scan_false_empty": {
            "measured_scan": ex_scan(cases["PRE-EX-CH"]),
            "expected_false_value": [],
            "reproduced": ex_scan(cases["PRE-EX-CH"]) == [],
            "false_pass_derivation":
                "the scan guarding the ECX reaching definition returned [] "
                "on a mutant that physically writes CH (ECX bits [8,16)); "
                "any historical provenance conclusion built on this scan "
                "would PASS on the mutant - the component-level false PASS "
                "of CMO-C1",
            "supplementary_ebp_scan":
                cases["PRE-EX-CH"]["scans"][
                    "supplementary_nonhistorical_ebp_scan"],
            "supplementary_note": "the false EBP attribution lands INSIDE "
                                  "the same interval - the clobber exists, "
                                  "it is merely misfiled under EBP"},
        "F-PRE-3_qc_ch_writes_is_ebp_NOT_ecx": {
            "measured_writes": ch_qc["writes"],
            "expected_wrong_value": ["ebp"],
            "reproduced": ch_qc["writes"] == ["ebp"],
            "dst_string_correct_anyway": ch_qc["dst"] == "ch",
            "reads_measured": ch_qc["reads"],
            "reads_note": "reads=[] - the register-direct byte SOURCE parent "
                          "was never recorded by the historical QC decoder "
                          "(missing, not merely wrong)"},
        "F-PRE-4_qc_ch_ecx_scan_false_empty": {
            "measured_scan": qc_scan(cases["PRE-QC-CH"]),
            "expected_false_value": [],
            "reproduced": qc_scan(cases["PRE-QC-CH"]) == []},
        "F-PRE-5_clean_no_ecx_clobber_both_impls": {
            "executor_scan": ex_scan(cases["PRE-EX-CLEAN"]),
            "qc_scan": qc_scan(cases["PRE-QC-CLEAN"]),
            "executor_site_bytes": clean_ex["bytes"],
            "executor_site_mnemonic": clean_ex["mnemonic"],
            "qc_site_bytes": clean_qc["bytes"],
            "reproduced": (ex_scan(cases["PRE-EX-CLEAN"]) == []
                           and qc_scan(cases["PRE-QC-CLEAN"]) == []
                           and clean_ex["bytes"] == "D9 E8"
                           and clean_ex["mnemonic"] == "fld1"
                           and clean_ex["writes"] == [])},
        "F-PRE-6_cl_detected_by_coincidence_both_impls": {
            "executor_scan": ex_scan(cases["PRE-EX-CL"]),
            "qc_scan": qc_scan(cases["PRE-QC-CL"]),
            "executor_writes": cl_ex["writes"],
            "qc_writes": cl_qc["writes"],
            "reproduced": (ex_scan(cases["PRE-EX-CL"]) == ["0x%08X" % MUT_VA]
                           and qc_scan(cases["PRE-QC-CL"])
                           == ["0x%08X" % MUT_VA]
                           and cl_ex["writes"] == ["ecx"]
                           and cl_qc["writes"] == ["ecx"]),
            "note": "CL is a LOW alias (R8[1]); REGS[1]==ecx==parent(CL) - "
                    "the low-alias path was correct by COINCIDENCE"},
        "F-PRE-7_length_preservation_all_mutants": {
            "counts": {cid: cases[cid]["decode"]["instruction_count"]
                       for cid in cases},
            "ends_exact": {cid:
                           cases[cid]["decode"]["end_exact_0x0085B290"]
                           for cid in cases},
            "reproduced": all(
                cases[cid]["decode"]["instruction_count"] == 64
                and cases[cid]["decode"]["end_exact_0x0085B290"]
                for cid in cases)},
    }
    for k, v in adj.items():
        if not v.get("reproduced", True):
            die("PRE falsifier %s NOT reproduced - honest stop" % k)
    R["falsifier_adjudication"] = adj
    R["cases"] = cases

    R["pre_summary"] = {
        "PRE_EXECUTOR_FALSE_PASS_REPRODUCED":
            adj["F-PRE-1_executor_ch_writes_is_ebp_NOT_ecx"]["reproduced"]
            and adj["F-PRE-2_executor_ch_ecx_scan_false_empty"]["reproduced"],
        "PRE_QC_FALSE_PASS_REPRODUCED":
            adj["F-PRE-3_qc_ch_writes_is_ebp_NOT_ecx"]["reproduced"]
            and adj["F-PRE-4_qc_ch_ecx_scan_false_empty"]["reproduced"],
        "WRONG_WRITES_SET_OBSERVED": {
            "executor_ch_mutant": ch_ex["writes"],
            "qc_ch_mutant": ch_qc["writes"]},
        "CLEAN_NO_ECX_CLOBBER": adj["F-PRE-5_clean_no_ecx_clobber_both_impls"
                                    ""]["reproduced"],
        "CL_DETECTED_BY_HISTORICAL":
            adj["F-PRE-6_cl_detected_by_coincidence_both_impls"]["reproduced"],
        "HISTORICAL_WOULD_BE_PROVENANCE_VERDICT_ON_CH_MUTANT":
            "PASS (FALSE) - the historical ECX-clobber scan returned [] on "
            "the CH mutant, so the historical reaching-definition guard "
            "cannot see the clobber; this is the reproduced false PASS"}

    # ---- 5. historical 8x8 alias-matrix census (blast radius) -------------
    matrix = []
    ex_w_ok = ex_r_ok = qc_w_ok = 0
    both_ok_ex = 0
    qc_reads_absent = 0
    for dst_i in range(8):
        for src_i in range(8):
            modrm = 0xC0 | (src_i << 3) | dst_i
            buf = bytes([0x88, modrm])
            e = ex_ns["decode_instruction"](buf, 0, MUT_VA)
            q = qc_ns["my_decode"](buf, 0, MUT_VA)
            ref_d = REF_ALIAS[dst_i]
            ref_s = REF_ALIAS[src_i]
            e_w_ok = (e["writes"] == {ref_d[1]})
            e_r_ok = (e["reads"] == {ref_s[1]})
            q_w_ok = (q["writes"] == {ref_d[1]})
            q_r_absent = (len(q["reads"]) == 0)
            ex_w_ok += e_w_ok
            ex_r_ok += e_r_ok
            qc_w_ok += q_w_ok
            qc_reads_absent += q_r_absent
            both_ok_ex += (e_w_ok and e_r_ok)
            matrix.append({
                "case_id": "H-%02d%02d" % (dst_i, src_i),
                "bytes": hx(buf), "modrm": "0x%02X" % modrm,
                "x86_32_meaning": "mov %s, %s (reg=%s source, rm=%s dest)"
                                 % (ref_d[0], ref_s[0], ref_s[0], ref_d[0]),
                "reference": {"dst_name": ref_d[0], "dst_parent": ref_d[1],
                              "dst_bits": ref_d[2],
                              "src_name": ref_s[0], "src_parent": ref_s[1],
                              "src_bits": ref_s[2]},
                "historical_executor": {
                    "dst": e["dst"], "src": e["src"], "width": e["width"],
                    "length": e["length"],
                    "writes": sorted(e["writes"]),
                    "reads": sorted(e["reads"]),
                    "writes_parent_correct": e_w_ok,
                    "reads_parent_correct": e_r_ok,
                    "expected_wrong_writes_when_incorrect":
                        None if e_w_ok else sorted(e["writes"])},
                "historical_qc": {
                    "dst": q["dst"], "src": q["src"], "width": q["width"],
                    "length": q["length"],
                    "writes": sorted(q["writes"]),
                    "reads": sorted(q["reads"]),
                    "writes_parent_correct": q_w_ok,
                    "source_parent_recorded": not q_r_absent},
                "verdict_note":
                    ("dst<=3 and src<=3: LOW-ALIAS COINCIDENCE - correct "
                     "parents despite the alias-index defect"
                     if (dst_i < 4 and src_i < 4)
                     else "at least one high alias (index>=4): historical "
                          "writes/reads parent WRONG or missing by design "
                          "of the defect")})
    R["historical_alias_matrix_census"] = {
        "purpose": "blast-radius census of the historical alias-index defect "
                   "across the complete 8x8 register-direct 0x88 matrix; "
                   "expected-WRONG values for high aliases are the point "
                   "(this is a historical census, NOT a pass/fail control; "
                   "low-alias correctness is coincidence: R8[i]==parent "
                   "only for i<4 because the R8 table is not parallel to "
                   "REGS)",
        "cases": 64, "decoders": 2, "historical_outcomes": 128,
        "executor": {
            "writes_parent_correct": ex_w_ok, "writes_parent_wrong": 64 - ex_w_ok,
            "writes_wrong_detail": "dest 4-7 (AH,CH,DH,BH) map to "
                                   "esp,ebp,esi,edi instead of "
                                   "eax,ecx,edx,ebx",
            "reads_parent_correct": ex_r_ok, "reads_parent_wrong": 64 - ex_r_ok,
            "reads_wrong_detail": "source 4-7 (AH,CH,DH,BH) map to "
                                  "esp,ebp,esi,edi instead of "
                                  "eax,ecx,edx,ebx",
            "both_writes_and_reads_correct": both_ok_ex,
            "both_correct_detail": "exactly the 16 cases with dst<=3 AND "
                                   "src<=3 (coincidence, not correctness "
                                   "of the mapping)"},
        "qc": {
            "writes_parent_correct": qc_w_ok,
            "writes_parent_wrong": 64 - qc_w_ok,
            "register_form_source_parent_recorded": 64 - qc_reads_absent,
            "source_parent_absent": qc_reads_absent,
            "reads_detail": "the register-direct byte SOURCE parent was "
                            "never recorded in any of the 64 cases "
                            "(missing, not merely wrong)"},
        "rows": matrix}

    # ---- 6. write immutable PRE evidence ---------------------------------
    pre_dir = os.path.join(PKG, "00_PRE")
    os.makedirs(pre_dir, exist_ok=True)
    pre_json = os.path.join(pre_dir, "PRE_COUNTEREXAMPLES.json")
    with open(pre_json, "w", encoding="utf-8", newline="\n") as f:
        json.dump(R, f, indent=1, sort_keys=False)

    # ---- 7. PRE SHA256 index ----------------------------------------------
    idx_rows = []
    for p in (pre_json,
              os.path.abspath(__file__),
              src_scripts["repin_write_provenance.py"],
              src_scripts["qc_remeasure.py"],
              os.path.join(SOURCE_PKG, "CONTROL_RESULTS.json"),
              os.path.join(SOURCE_PKG, "QC_RESULTS.json")):
        if os.path.isabs(p) and p.startswith(REPO):
            rel = os.path.relpath(p, REPO).replace("\\", "/")
        else:
            rel = p
        idx_rows.append((rel, os.path.getsize(p), sha256_file(p)))
    idx_rows.append((EXE_PATH, os.path.getsize(EXE_PATH),
                     sha256_file(EXE_PATH)))
    idx_rows.append((CONTRACT_PATH, csize, csha))
    idx_csv = os.path.join(pre_dir, "PRE_SHA256_INDEX.csv")
    with open(idx_csv, "w", encoding="utf-8", newline="\n") as f:
        f.write("# PRE_SHA256_INDEX.csv - %s\n" % RUN_ID)
        f.write("# PRE evidence + executed-input provenance index, generated "
                "by 03_SCRIPTS/run_pre_counterexamples.py immediately after\n")
        f.write("# 00_PRE/PRE_COUNTEREXAMPLES.json was written. Repo-relative "
                "paths for repository files; absolute paths for the two\n")
        f.write("# inputs external to the repository (EXE, contract). "
                "ROW_COUNT = %d\n" % len(idx_rows))
        f.write("path,size_bytes,sha256\n")
        for rel, size, sha in idx_rows:
            f.write("%s,%d,%s\n" % (rel, size, sha.lower()))

    print("PRE COMPLETE")
    print("executor CH mutant: writes=%s dst=%r src=%r ecx_scan=%s"
          % (ch_ex["writes"], ch_ex["dst"], ch_ex["src"],
             ex_scan(cases["PRE-EX-CH"])))
    print("qc        CH mutant: writes=%s dst=%r src=%r ecx_scan=%s"
          % (ch_qc["writes"], ch_qc["dst"], ch_qc["src"],
             qc_scan(cases["PRE-QC-CH"])))
    print("clean: ex_scan=%s qc_scan=%s site=%s %s"
          % (ex_scan(cases["PRE-EX-CLEAN"]),
             qc_scan(cases["PRE-QC-CLEAN"]),
             clean_ex["bytes"], clean_ex["mnemonic"]))
    print("CL control: ex_scan=%s qc_scan=%s"
          % (ex_scan(cases["PRE-EX-CL"]), qc_scan(cases["PRE-QC-CL"])))
    print("historical matrix: executor writes ok %d/64, reads ok %d/64, "
          "both ok %d/64; qc writes ok %d/64, source-parent recorded %d/64"
          % (ex_w_ok, ex_r_ok, both_ok_ex, qc_w_ok, 64 - qc_reads_absent))
    print("PRE_EXECUTOR_FALSE_PASS_REPRODUCED=%s"
          % R["pre_summary"]["PRE_EXECUTOR_FALSE_PASS_REPRODUCED"])
    print("PRE_QC_FALSE_PASS_REPRODUCED=%s"
          % R["pre_summary"]["PRE_QC_FALSE_PASS_REPRODUCED"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
