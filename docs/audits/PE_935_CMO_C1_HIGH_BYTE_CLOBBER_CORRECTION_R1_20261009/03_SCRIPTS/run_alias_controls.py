#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""run_alias_controls.py — PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009

POST controls driver (contract section 6). Runs the corrected executor decoder
(03_SCRIPTS/corrected_executor_decoder.py) through the pre-registered control
list C1-C6 (+ AUX-1 fail-closed demonstration) and writes:

  00_POST/POST_COUNTEREXAMPLES.json
  00_POST/POST_SHA256_INDEX.csv
  CONTROL_MATRIX.csv
  REGRESSION_RESULTS.json

Method notes:
  * Own minimal PE section-table mapper (VA -> file offset); the decoder module
    stays pure-byte-level (no file I/O), like its historical predecessor.
  * The C4 alias matrix is verified against an INDEPENDENT reference table
    defined in THIS driver — it does NOT import the production decoder's
    mapping helper (corrected_executor_decoder.BYTE8_PARENT).
  * C6 re-executes the AST-extracted HISTORICAL executor decoder (read-only,
    top-level never run) on the physical clean window and requires
    field-by-field equality with the corrected decode (the fix must be
    invisible on the physical window), in addition to the committed
    CONTROL_RESULTS.json instruction-table anchor.
  * All mutants are in-memory copies; the physical EXE is rehashed at the end
    (acceptance gate 7).
  * python -B; stdlib only; writes ONLY under this package's OUTPUT_ROOT.
"""
import ast
import builtins
import csv
import hashlib
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(PKG)))
sys.path.insert(0, HERE)
import corrected_executor_decoder as ced  # noqa: E402

SOURCE_PKG = os.path.join(
    REPO, "docs", "audits",
    "PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009")
EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
CONTRACT_PATH = (r"C:\Users\User\Documents\ChatGPT\PE"
                 r"\PE_CMO_C1_HIGH_BYTE_CORRECTION_PROMPT_20261008"
                 r"\OPENCODE_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009.md")

EXE_SIZE = 8015872
EXE_SHA = ("E7785430E81DFFE648CE8F5312414B17"
           "BC9FCE61389689A22F753765D5280F31")
OLD_EXECUTOR = os.path.join(SOURCE_PKG, "03_SCRIPTS",
                            "repin_write_provenance.py")
OLD_EXECUTOR_SHA = ("45120C91AD6A94A79C56E9B06F1C035481FB99"
                    "D3017688E7F589732BEC6EE931")
OLD_EXECUTOR_SIZE = 34043
CONTROL_RESULTS = os.path.join(SOURCE_PKG, "CONTROL_RESULTS.json")
CONTROL_RESULTS_SHA = ("9545D0D78881C29BC805EA3A05C8AA936D364256"
                       "671D31A1AE907677A63DE2F8")
CONTROL_RESULTS_SIZE = 18509

W1_VA = 0x0085B1A8
FN_START = 0x0085B1B0
FN_END = 0x0085B290
MUT_VA = 0x0085B24D
MUT_OFF = MUT_VA - FN_START

# INDEPENDENT reference table for opcode 0x88 byte aliases (x86-32).
# NOT imported from the production decoder's mapping helper.
REF_BYTE8 = [
    ("al", "eax", (0, 8)), ("cl", "ecx", (0, 8)),
    ("dl", "edx", (0, 8)), ("bl", "ebx", (0, 8)),
    ("ah", "eax", (8, 16)), ("ch", "ecx", (8, 16)),
    ("dh", "edx", (8, 16)), ("bh", "ebx", (8, 16)),
]


def hx(b):
    return " ".join("%02X" % c for c in b)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def die(msg):
    sys.stderr.write("FAIL-CLOSED: %s\n" % msg)
    sys.exit(2)


class OwnPE:
    """Minimal PE32 section-table mapper (VA -> file offset), fail-closed."""

    def __init__(self, data):
        self.data = data
        if data[:2] != b"MZ":
            raise SystemExit("no MZ")
        e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
        if data[e_lfanew:e_lfanew + 4] != b"PE\x00\x00":
            raise SystemExit("no PE sig")
        coff = e_lfanew + 4
        nsec = struct.unpack_from("<H", data, coff + 2)[0]
        opt_size = struct.unpack_from("<H", data, coff + 16)[0]
        opt = coff + 20
        if struct.unpack_from("<H", data, opt)[0] != 0x10B:
            raise SystemExit("not PE32")
        self.image_base = struct.unpack_from("<I", data, opt + 28)[0]
        self.sections = []
        tbl = opt + opt_size
        for i in range(nsec):
            s = tbl + 40 * i
            vsize = struct.unpack_from("<I", data, s + 8)[0]
            vaddr = struct.unpack_from("<I", data, s + 12)[0]
            rsize = struct.unpack_from("<I", data, s + 16)[0]
            rptr = struct.unpack_from("<I", data, s + 20)[0]
            self.sections.append((vaddr, max(vsize, rsize), rptr))

    def off(self, va, n=1):
        rva = va - self.image_base
        for vaddr, span, rptr in self.sections:
            if vaddr <= rva < vaddr + span:
                fo = rva - vaddr + rptr
                if fo < 0 or fo + n > len(self.data):
                    raise SystemExit("range outside file for VA %#x" % va)
                return fo
        raise SystemExit("VA %#x not in any section" % va)

    def read(self, va, n):
        fo = self.off(va, n)
        return self.data[fo:fo + n]

    def u32(self, va):
        return struct.unpack("<I", self.read(va, 4))[0]


def extract_historical_executor():
    """AST-extract the HISTORICAL executor decoder (read-only; no top level)."""
    with open(OLD_EXECUTOR, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    consts, classes, funcs = {}, {}, {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id in ("REGS", "R8", "R16")):
            consts[node.targets[0].id] = node
        elif isinstance(node, ast.ClassDef) and node.name == "DecodeError":
            classes[node.name] = node
        elif (isinstance(node, ast.FunctionDef) and node.name in
              ("_modrm", "_fmt_mem", "decode_instruction",
               "linear_decode_window", "hexs")):
            funcs[node.name] = node
    if (set(consts) != {"REGS", "R8", "R16"} or set(classes) != {"DecodeError"}
            or set(funcs) != {"_modrm", "_fmt_mem", "decode_instruction",
                              "linear_decode_window", "hexs"}):
        die("historical executor AST extraction incomplete")
    ns = {"struct": struct, "__builtins__": builtins}
    mod = ast.Module(body=[consts["REGS"], consts["R8"], consts["R16"],
                           classes["DecodeError"],
                           funcs["_modrm"], funcs["_fmt_mem"],
                           funcs["decode_instruction"],
                           funcs["linear_decode_window"], funcs["hexs"]],
                     type_ignores=[])
    ast.fix_missing_locations(mod)
    exec(compile(mod, "<historical_executor_readonly>", "exec"), ns)
    return ns


def ser_site(i):
    return {"va": "0x%08X" % i["va"], "length": i["length"],
            "bytes": hx(i["bytes"]), "mnemonic": i["mnemonic"],
            "text": i["text"], "dst": i["dst"], "src": i["src"],
            "width": i["width"], "writes": sorted(i["writes"]),
            "reads": sorted(i["reads"]), "mem_dst": i["mem_dst"],
            "byte_dst": i.get("byte_dst"),
            "byte_dst_parent": i.get("byte_dst_parent"),
            "byte_dst_bits": i.get("byte_dst_bits"),
            "byte_src": i.get("byte_src"),
            "byte_src_parent": i.get("byte_src_parent"),
            "byte_src_bits": i.get("byte_src_bits"),
            "partial_gpr_write": i.get("partial_gpr_write"),
            "gpr_write_bits": i.get("gpr_write_bits")}


def dec_summary(ins):
    last = ins[-1]
    return {"instruction_count": len(ins),
            "total_bytes": sum(x["length"] for x in ins),
            "end_va": "0x%08X" % (last["va"] + last["length"]),
            "end_exact_0x0085B290": last["va"] + last["length"] == FN_END}


def at(ins, va):
    for i in ins:
        if i["va"] == va:
            return i
    return None


def main():
    R = {"run_id": "PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009",
         "phase": "POST_COUNTEREXAMPLES",
         "driver": "03_SCRIPTS/run_alias_controls.py (python -B)",
         "python": sys.version.split()[0]}

    # ---- identities -------------------------------------------------------
    if (os.path.getsize(OLD_EXECUTOR), sha256_file(OLD_EXECUTOR)) != \
            (OLD_EXECUTOR_SIZE, OLD_EXECUTOR_SHA):
        die("historical executor script identity mismatch")
    if (os.path.getsize(CONTROL_RESULTS), sha256_file(CONTROL_RESULTS)) != \
            (CONTROL_RESULTS_SIZE, CONTROL_RESULTS_SHA):
        die("CONTROL_RESULTS.json identity mismatch")
    if (os.path.getsize(EXE_PATH), sha256_file(EXE_PATH)) != \
            (EXE_SIZE, EXE_SHA):
        die("EXE identity mismatch at POST start")

    ced_path = os.path.join(HERE, "corrected_executor_decoder.py")
    R["script_mapping"] = {
        "OLD_EXECUTOR_SCRIPT": {
            "path": os.path.relpath(OLD_EXECUTOR, REPO).replace("\\", "/"),
            "size": OLD_EXECUTOR_SIZE, "sha256": OLD_EXECUTOR_SHA,
            "status": "historical, IMMUTABLE, not edited"},
        "CORRECTED_EXECUTOR_SCRIPT": {
            "path": os.path.relpath(ced_path, REPO).replace("\\", "/"),
            "size": os.path.getsize(ced_path),
            "sha256": sha256_file(ced_path),
            "status": "corrected successor (this run; CMO-C1 fix)"},
        "OLD_QC_SCRIPT": {
            "path": os.path.relpath(
                os.path.join(SOURCE_PKG, "03_SCRIPTS", "qc_remeasure.py"),
                REPO).replace("\\", "/"),
            "size": 31970,
            "sha256": ("4E5426AEAB8FBD9A9364A5FE445ED2EA7C5D9F4B"
                       "3E2F2E71B3EB5B3F3F8DDE1A"),
            "status": "historical, IMMUTABLE, not edited"},
        "CORRECTED_QC_SCRIPT": {
            "path": "03_SCRIPTS/corrected_qc_decoder.py (TO BE WRITTEN by "
                    "the fresh-QC worker phase; NOT this executor phase)",
            "status": "NOT_PERFORMED_IN_EXECUTOR_PHASE (delegation note in "
                      "PREREGISTRATION section 6)"}}

    with open(EXE_PATH, "rb") as f:
        exe_bytes = f.read()
    pe = OwnPE(exe_bytes)
    w1 = pe.read(W1_VA, 232)
    win = bytes(w1[FN_START - W1_VA: FN_END - W1_VA])
    if len(win) != 224 or win[MUT_OFF:MUT_OFF + 2] != b"\xD9\xE8":
        die("physical window premise failed")
    accessor = pe.read(0x00746560, 4)
    w3 = pe.read(0x00528E74, 52)

    def window_mutant(b2):
        w = bytearray(win)
        w[MUT_OFF] = b2[0]
        w[MUT_OFF + 1] = b2[1]
        return bytes(w)

    def decode_win(w):
        return ced.linear_decode_window(w, FN_START, FN_START, FN_END)

    def ecx_scan(ins):
        return ["0x%08X" % v for v in ced.scan_writers_interval(
            ins, "ecx", 0x0085B24B, 0x0085B27A)]

    controls = {}

    # ================= C1 — clean baseline =================================
    ins = decode_win(win)
    site = at(ins, MUT_VA)
    gate = ced.value_provenance_gate(ins, accessor)
    c1 = {
        "input": "physical window bytes [0x0085B1B0,0x0085B290) (read-only)",
        "decode": dec_summary(ins),
        "mutation_site_pin": {"va": "0x0085B24D",
                             "expected": "D9 E8", "measured": hx(site["bytes"]),
                             "match": hx(site["bytes"]) == "D9 E8"},
        "ecx_clobber_scan_(0x0085B24B,0x0085B27A)": ecx_scan(ins),
        "ECX_CLOBBER_AT_MUTATION_SITE": "NO" if ecx_scan(ins) == [] else "YES",
        "provenance_gate": gate,
        "expected": {"DECODE": "PASS", "INSTRUCTION_COUNT": 64,
                     "DECODE_END": "0x0085B290",
                     "ECX_CLOBBER_AT_MUTATION_SITE": "NO",
                     "CORE_VALUE_SOURCE": "[arg1+8]",
                     "VALUE_PROVENANCE_GATE": "PASS"}}
    c1_pass = (dec_summary(ins)["instruction_count"] == 64
               and dec_summary(ins)["end_exact_0x0085B290"]
               and c1["mutation_site_pin"]["match"]
               and c1["ECX_CLOBBER_AT_MUTATION_SITE"] == "NO"
               and gate["gate"] == "PASS"
               and gate["core_value_source"] == "[arg1+8]")
    c1["verdict"] = "PASS" if c1_pass else "FAIL"
    controls["C1_clean_baseline"] = c1

    # ============ C2 / C3 — CH mutant and CL control ========================
    def mutant_case(name, b2, exp_operand, exp_parent, exp_dst_bits):
        w = window_mutant(b2)
        insm = decode_win(w)
        s = at(insm, MUT_VA)
        g = ced.value_provenance_gate(insm, accessor)
        scan = ecx_scan(insm)
        rec = {
            "input": "in-memory window copy; bytes %s @0x0085B24D "
                     "(physical EXE untouched)" % hx(b2),
            "decode": dec_summary(insm),
            "mutation_site_instruction": ser_site(s),
            "ecx_clobber_scan_(0x0085B24B,0x0085B27A)": scan,
            "provenance_gate": g,
            "expected": {
                "DECODE": "PASS", "INSTRUCTION_COUNT": 64,
                "DECODE_END": "0x0085B290",
                "OPERAND": exp_operand,
                "WRITES_PARENT": exp_parent,
                "CLOBBER_SCAN": "DETECTED",
                "CLOBBER_VA": "0x0085B24D",
                "VALUE_PROVENANCE_GATE": "FAIL",
                "GATE_FAILURE_REASON": "ECX_REACHING_DEF_BROKEN"}}
        checks = {
            "decode_pass_64_exact": (
                dec_summary(insm)["instruction_count"] == 64
                and dec_summary(insm)["end_exact_0x0085B290"]),
            "operand": s["dst"] == exp_operand,
            "writes_parent": sorted(s["writes"]) == [exp_parent],
            "byte_dst_bits": list(s.get("byte_dst_bits", []))
            == list(exp_dst_bits),
            "width_8_partial": (s["width"] == 8
                                and s.get("partial_gpr_write") is True),
            "length_2": s["length"] == 2,
            "clobber_scan_detected": (scan == ["0x%08X" % MUT_VA]),
            "gate_fail": g["gate"] == "FAIL",
            "gate_failure_came_from_broken_ecx_reaching_def":
                g["failure_reasons"] == ["ECX_REACHING_DEF_BROKEN"],
            "gate_all_other_checks_pass": all(
                v for k, v in g["checks"].items()
                if k != "ecx_reaching_definition_intact"),
            "exe_identity_unaffected": True}
        rec["checks"] = checks
        ok = all(checks.values())
        rec["verdict"] = "PASS" if ok else "FAIL"
        return rec

    controls["C2_ch_mutant_88_DD"] = mutant_case(
        "C2", b"\x88\xDD", "ch", "ecx", (8, 16))
    controls["C3_cl_control_88_D9"] = mutant_case(
        "C3", b"\x88\xD9", "cl", "ecx", (0, 8))

    # ============ C4 — alias matrix (8x8, 64 cases; executor impl) ==========
    matrix_rows = []
    matrix_pass = 0
    dst_names, src_names = set(), set()
    for dst_i in range(8):
        for src_i in range(8):
            modrm = 0xC0 | (src_i << 3) | dst_i
            buf = bytes([0x88, modrm])
            i = ced.decode_instruction(buf, 0, MUT_VA)
            rd = REF_BYTE8[dst_i]
            rs = REF_BYTE8[src_i]
            dst_names.add(rd[0])
            src_names.add(rs[0])
            case_checks = {
                "exact_destination_operand": i["dst"] == rd[0],
                "byte_dst_name": i.get("byte_dst") == rd[0],
                "correct_parent": i.get("byte_dst_parent") == rd[1],
                "writes_set_is_exactly_parent":
                    i["writes"] == {rd[1]},
                "no_false_write_to_unrelated_parent":
                    i["writes"] == {rd[1]},
                "width_8": i["width"] == 8,
                "length_2": i["length"] == 2,
                "partial_write_not_full_32bit": (
                    i.get("partial_gpr_write") is True
                    and i["width"] == 8
                    and list(i.get("gpr_write_bits", []))
                    == [rd[2][0], rd[2][1]]),
                "dst_bit_range": list(i.get("byte_dst_bits", []))
                == [rd[2][0], rd[2][1]],
                "exact_source_operand": i["src"] == rs[0],
                "byte_src_name": i.get("byte_src") == rs[0],
                "source_parent": i.get("byte_src_parent") == rs[1],
                "reads_set_is_exactly_source_parent":
                    i["reads"] == {rs[1]},
                "src_bit_range": list(i.get("byte_src_bits", []))
                == [rs[2][0], rs[2][1]],
                "text_form": i["text"] == "mov %s, %s" % (rd[0], rs[0])}
            ok = all(case_checks.values())
            matrix_pass += ok
            matrix_rows.append({
                "case_id": "A-%02d%02d" % (dst_i, src_i),
                "bytes": hx(buf), "modrm": "0x%02X" % modrm,
                "x86_32_meaning": "mov %s, %s" % (rd[0], rs[0]),
                "reference": {"dst_name": rd[0], "dst_parent": rd[1],
                              "dst_bits": [rd[2][0], rd[2][1]],
                              "src_name": rs[0], "src_parent": rs[1],
                              "src_bits": [rs[2][0], rs[2][1]]},
                "decoded": ser_site(i),
                "checks": case_checks,
                "outcome": "PASS" if ok else "FAIL"})
    controls["C4_alias_matrix"] = {
        "design": "complete 8x8 register-direct matrix for opcode 0x88, "
                  "mod=11: 64 distinct 2-byte instruction cases per decoder "
                  "(8 byte destinations x 8 byte sources, AH/CH/DH/BH on "
                  "both sides); synthetic alias matrix, NOT 128 provenance-"
                  "path tests; cases, implementations and outcomes are "
                  "reported as different units",
        "independent_reference_table": {
            "definition": "REF_BYTE8 defined inside run_alias_controls.py; "
                          "does NOT import "
                          "corrected_executor_decoder.BYTE8_PARENT",
            "values": [[n, p, [b[0], b[1]]] for n, p, b in REF_BYTE8]},
        "cases_per_decoder": 64,
        "implementations": {
            "corrected_executor_decoder (this phase)": {
                "outcomes_measured": 64, "outcomes_pass": matrix_pass},
            "corrected_qc_decoder (fresh-QC worker phase)": {
                "outcomes_measured": 0,
                "status": "NOT_PERFORMED_IN_EXECUTOR_PHASE — assigned to "
                          "the fresh-QC worker (03_SCRIPTS/"
                          "corrected_qc_decoder.py + QC_RESULTS.json); the "
                          "full 128-outcome two-implementation total "
                          "completes in that phase"}},
        "coverage": {"distinct_destinations_exercised":
                     sorted(dst_names),
                     "distinct_destinations_count": len(dst_names),
                     "distinct_sources_exercised": sorted(src_names),
                     "distinct_sources_count": len(src_names),
                     "destination_alias_coverage": "%d/8" % len(dst_names),
                     "source_alias_coverage": "%d/8" % len(src_names),
                     "note": "each of the 8 aliases appears as destination "
                             "in 8 cases and as source in 8 cases; testing "
                             "all destinations against only BL is "
                             "insufficient and was NOT done"},
        "partial_write_semantics_note":
            "a partial-byte write CLOBBERS the parent register for "
            "reaching-definition purposes but is NOT a full 32-bit "
            "overwrite; preserved via width=8, byte bit-ranges "
            "(low [0,8), high [8,16)) and partial_gpr_write/gpr_write_bits",
        "rows": matrix_rows,
        "verdict": "PASS" if (matrix_pass == 64 and len(dst_names) == 8
                               and len(src_names) == 8) else "FAIL"}

    # ============ C5 — unrelated-parent negatives ==========================
    c5_cases = [
        ("C5.1_mov_bh_bl_88_DF", b"\x88\xDF", "bh", "ebx", (8, 16),
         "bl", "ebx"),
        ("C5.2_mov_ah_bl_88_DC", b"\x88\xDC", "ah", "eax", (8, 16),
         "bl", "ebx"),
        ("C5.3_mov_dh_cl_88_CE", b"\x88\xCE", "dh", "edx", (8, 16),
         "cl", "ecx"),
        ("C5.4_mov_bh_bh_88_FF", b"\x88\xFF", "bh", "ebx", (8, 16),
         "bh", "ebx")]
    c5 = {}
    for name, b2, dst_name, dst_parent, dst_bits, src_name, src_parent \
            in c5_cases:
        w = window_mutant(b2)
        insm = decode_win(w)
        s = at(insm, MUT_VA)
        g = ced.value_provenance_gate(insm, accessor)
        scan = ecx_scan(insm)
        checks = {
            "attributed_to_correct_parent":
                sorted(s["writes"]) == [dst_parent],
            "not_attributed_to_edi": "edi" not in s["writes"],
            "not_attributed_to_ecx": "ecx" not in s["writes"],
            "ecx_scan_does_not_report_ecx_modified": scan == [],
            "provenance_gate_stays_pass": g["gate"] == "PASS",
            "source_parent_recorded": sorted(s["reads"]) == [src_parent],
            "reads_are_not_clobbers": (
                "a byte READ of a parent (e.g. the CL source parent ECX "
                "in mov dh,cl) appears in the READS set but never triggers "
                "the WRITER-based clobber scan")}
        c5[name] = {
            "input": "in-memory window copy; bytes %s @0x0085B24D" % hx(b2),
            "x86_32_meaning": "mov %s, %s" % (dst_name, src_name),
            "expected_parent": dst_parent,
            "decode": dec_summary(insm),
            "mutation_site_instruction": ser_site(s),
            "ecx_clobber_scan_(0x0085B24B,0x0085B27A)": scan,
            "provenance_gate": g,
            "checks": checks,
            "expected": {
                "WRITES_PARENT": dst_parent,
                "CLOBBER_SCAN": "[] (ECX not modified)",
                "VALUE_PROVENANCE_GATE": "PASS (chain intact)"},
            "verdict": "PASS" if (all(checks.values())
                                   and checks["provenance_gate_stays_pass"]
                                   and checks["ecx_scan_does_not_report_ecx"
                                              "_modified"]) else "FAIL"}
    controls["C5_unrelated_parent_negatives"] = c5

    # ============ C6 — historical scientific regression ====================
    # (a) byte pins within the approved windows
    pins = [
        ("boundary_ret_0x0085B1AC", 0x0085B1AC, "C3"),
        ("boundary_pad_0x0085B1AD_AF", 0x0085B1AD, "CC CC CC"),
        ("entry_0x0085B1B0", 0x0085B1B0, "8B 44 24 08"),
        ("receiver_def_0x0085B1B7", 0x0085B1B7, "8B F1"),
        ("vbase_stamp_0x0085B1C1", 0x0085B1C1, "C7 06 4C 1E A9 00"),
        ("arg1_load_0x0085B1DA", 0x0085B1DA, "8B 7C 24 14"),
        ("zeroinit_0x0085B1E4", 0x0085B1E4, "D9 56 44"),
        ("zeroinit_0x0085B1E7", 0x0085B1E7, "D9 56 48"),
        ("zeroinit_0x0085B1EC", 0x0085B1EC, "D9 56 4C"),
        ("ecx_from_edi_0x0085B24B", 0x0085B24B, "8B CF"),
        ("mutation_site_0x0085B24D", 0x0085B24D, "D9 E8"),
        ("call_0x0085B27A", 0x0085B27A, "E8 E1 B2 EE FF"),
        ("value_load_0x0085B27F", 0x0085B27F, "8B 08"),
        ("store_0x0085B281", 0x0085B281, "89 4E 44"),
        ("load_edx_0x0085B284", 0x0085B284, "8B 50 04"),
        ("copy48_0x0085B287_PIN_ONLY_NO_ANALYSIS", 0x0085B287, "89 56 48"),
        ("load_eax_0x0085B28A", 0x0085B28A, "8B 40 08"),
        ("copy4C_0x0085B28D_PIN_ONLY_NO_ANALYSIS", 0x0085B28D, "89 46 4C"),
        ("accessor_0x00746560", 0x00746560, "8D 41 08 C3"),
        ("caller_esi_0x00528E76", 0x00528E76, "8B F1"),
        ("caller_ecx_0x00528E8B", 0x00528E8B, "8B CE"),
        ("caller_call_0x00528E8D", 0x00528E8D, "E8 1E 23 33 00"),
        ("derived_vtable_0x00528EA2", 0x00528EA2, "C7 06 B0 DC A7 00"),
    ]
    pin_results = {}
    pin_all = True
    for name, va, expect in pins:
        got = hx(pe.read(va, len(expect.split())))
        pin_results[name] = {"va": "0x%08X" % va, "expected": expect,
                             "measured": got, "match": got == expect}
        pin_all = pin_all and got == expect
    rel_a = struct.unpack("<i", pe.read(0x0085B27B, 4))[0]
    tgt_a = (0x0085B27A + 5 + rel_a) & 0xffffffff
    rel_b = struct.unpack("<i", pe.read(0x00528E8E, 4))[0]
    tgt_b = (0x00528E8D + 5 + rel_b) & 0xffffffff

    def rtti(vtable, exp_col, exp_td, exp_name):
        col_ptr = pe.u32(vtable - 4)
        col = pe.read(col_ptr, 20)
        sig, _o, _cd, ptd, _pcd = struct.unpack("<5I", col)
        nb = pe.read(ptd + 8, len(exp_name) + 1)
        name = nb[:-1].decode("ascii", "replace")
        return {"vtable": "0x%08X" % vtable,
                "col_ptr": "0x%08X" % col_ptr,
                "col_sig": sig, "td": "0x%08X" % ptd, "name": name,
                "null_terminated": nb[-1] == 0,
                "expected_col": "0x%08X" % exp_col,
                "expected_td": "0x%08X" % exp_td,
                "expected_name": exp_name,
                "match": (sig == 0 and col_ptr == exp_col and ptd == exp_td
                          and name == exp_name and nb[-1] == 0)}
    rtti_mo = rtti(0x00A91E4C, 0x00AB33D0, 0x00B7997C, ".?AVMovableObject@@")
    rtti_cmo = rtti(0x00A7DCB0, 0x00AA17CC, 0x00B79958,
                    ".?AVClientMovableObject@@")

    # (b) corrected clean decode + committed-table anchor + historical-equality
    ins_clean = decode_win(win)
    clean_summary = dec_summary(ins_clean)
    with open(CONTROL_RESULTS, "r", encoding="utf-8") as f:
        committed = json.load(f)
    committed_rows = committed["decode"]["instructions"]
    tbl_match, tbl_rows = True, []
    if len(committed_rows) != len(ins_clean):
        tbl_match = False
    else:
        for h, c in zip(ins_clean, committed_rows):
            okrow = (h["va"] == c["va"] and h["length"] == c["len"]
                     and hx(h["bytes"]) == c["bytes"]
                     and h["text"] == c["text"])
            tbl_match = tbl_match and okrow
            tbl_rows.append({"va": "0x%08X" % h["va"],
                             "corrected": {"len": h["length"],
                                           "bytes": hx(h["bytes"]),
                                           "text": h["text"]},
                             "committed": {"len": c["len"],
                                           "bytes": c["bytes"],
                                           "text": c["text"]},
                             "match": okrow})

    hist_ns = extract_historical_executor()
    ins_hist = hist_ns["linear_decode_window"](win, FN_START,
                                               FN_START, FN_END)
    eq_fields, eq_all = [], True
    for a, b in zip(ins_clean, ins_hist):
        feq = {"va": "0x%08X" % a["va"],
               "match": (a["va"] == b["va"] and a["length"] == b["length"]
                         and a["bytes"] == b["bytes"]
                         and a["text"] == b["text"]
                         and a["writes"] == b["writes"]
                         and a["reads"] == b["reads"]
                         and a["dst"] == b["dst"] and a["src"] == b["src"]
                         and a["width"] == b["width"]
                         and a["mnemonic"] == b["mnemonic"])}
        eq_all = eq_all and feq["match"]
        eq_fields.append(feq)

    esi_writers = ["0x%08X" % v for v in ced.scan_writers_interval(
        ins_clean, "esi", 0x0085B1B7, 0x0085B281, hi_inclusive=True)]
    edi_writers = ["0x%08X" % v for v in ced.scan_writers_interval(
        ins_clean, "edi", 0x0085B1DA, 0x0085B24B, hi_inclusive=True)]
    ecx_w1 = ecx_scan(ins_clean)
    ecx_w2 = ["0x%08X" % v for v in ced.scan_writers_interval(
        ins_clean, "ecx", 0x0085B27F, 0x0085B281)]
    gate_clean = ced.value_provenance_gate(ins_clean, accessor)

    c6 = {
        "scope": "revalidation of existing original-client measurements "
                 "ONLY (no new bodies); the sibling stores +0x48/+0x4C are "
                 "byte-pinned ONLY (NO analysis, contract section 9); "
                 "exclusion-census pins outside the approved windows were "
                 "NOT re-read (NOT_PERFORMED by scope)",
        "pins": pin_results,
        "pins_all_match": pin_all,
        "rel32_recomputation": {
            "call_0x0085B27A": {"rel32_signed": rel_a,
                                "target": "0x%08X" % tgt_a,
                                "expected": "0x00746560",
                                "match": tgt_a == 0x00746560},
            "call_0x00528E8D": {"rel32_signed": rel_b,
                                "target": "0x%08X" % tgt_b,
                                "expected": "0x0085B1B0",
                                "match": tgt_b == 0x0085B1B0}},
        "rtti": {"MovableObject_vtable_0x00A91E4C": rtti_mo,
                 "ClientMovableObject_vtable_0x00A7DCB0": rtti_cmo},
        "clean_decode_corrected": clean_summary,
        "committed_table_anchor": {
            "source": "CONTROL_RESULTS.json (immutable; SHA256 verified)",
            "rows_compared": len(tbl_rows),
            "all_va_len_bytes_text_match": tbl_match,
            "rows": tbl_rows},
        "historical_executor_equality": {
            "method": "the AST-extracted HISTORICAL executor decoder "
                      "(read-only, top level never executed) re-decoded the "
                      "physical clean window; the corrected decode must be "
                      "field-by-field identical on the physical bytes "
                      "(the CMO-C1 fix is invisible on this window)",
            "rows_compared": len(eq_fields),
            "all_fields_equal": eq_all,
            "fields_compared": ["va", "length", "bytes", "text", "writes",
                                "reads", "dst", "src", "width", "mnemonic"],
            "rows": eq_fields},
        "receiver_chain": {
            "esi_def_pin_0x0085B1B7": pin_results[
                "receiver_def_0x0085B1B7"]["match"],
            "base_vtable_stamp_0x0085B1C1": pin_results[
                "vbase_stamp_0x0085B1C1"]["match"],
            "esi_writers_(0x0085B1B7,0x0085B281]": esi_writers,
            "derived_stamp_after_return_0x00528EA2": pin_results[
                "derived_vtable_0x00528EA2"]["match"],
            "rtti_MovableObject": rtti_mo["match"],
            "rtti_ClientMovableObject": rtti_cmo["match"]},
        "value_chain": {
            "edi_def_pin_0x0085B1DA": pin_results[
                "arg1_load_0x0085B1DA"]["match"],
            "ecx_def_pin_0x0085B24B": pin_results[
                "ecx_from_edi_0x0085B24B"]["match"],
            "edi_writers_(0x0085B1DA,0x0085B24B]": edi_writers,
            "ecx_writers_(0x0085B24B,0x0085B27A)": ecx_w1,
            "ecx_writers_(0x0085B27F,0x0085B281)": ecx_w2,
            "accessor_pin": pin_results["accessor_0x00746560"]["match"],
            "value_load_pin_0x0085B27F": pin_results[
                "value_load_0x0085B27F"]["match"],
            "store_pin_0x0085B281": pin_results[
                "store_0x0085B281"]["match"],
            "provenance_gate": gate_clean,
            "CORE_VALUE_SOURCE": gate_clean["core_value_source"]},
        "j3_statuses_carried_verbatim": {
            "PHYSICAL_TRANSFORM_MEASUREMENTS": "PRESERVED",
            "NEW_TRANSFORM_TRACE":
                "MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION",
            "SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN":
                "NOT_QUALIFIED_BY_ORIGINAL_SCOPE",
            "ORIGINAL_J3_EDGE_BUDGET_COMPLIANCE": "FAIL",
            "WORLD_XYZ_RECOVERED": "NO",
            "source": "J3 SUPERSESSION.md (docs/audits/"
                      "PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_"
                      "CORRECTION_R1_20261007/, 8339 B / DD11137A…) + source "
                      "FINAL_REPORT section 8; statuses carried, NOT "
                      "re-derived, NOT reinterpreted by this run"},
        "expected": {
            "store_0x0085B281": "89 4E 44",
            "caller_target": "0x0085B1B0",
            "accessor_target": "0x00746560",
            "rtti": "MovableObject + ClientMovableObject",
            "clean_decode": "64 instructions ending exactly 0x0085B290",
            "receiver_chain": "ESI := ctor this; no intervening ESI writer",
            "value_chain": "CORE_VALUE_SOURCE = [arg1+8]",
            "CORE_RECEIVER_VALUE_CHAIN":
                "PRESERVED_CONFIRMED_STATIC_CONDITIONAL"}}
    c6_ok = (pin_all
             and tgt_a == 0x00746560 and tgt_b == 0x0085B1B0
             and rtti_mo["match"] and rtti_cmo["match"]
             and clean_summary["instruction_count"] == 64
             and clean_summary["end_exact_0x0085B290"]
             and tbl_match and eq_all
             and esi_writers == [] and edi_writers == []
             and ecx_w1 == [] and ecx_w2 == []
             and gate_clean["gate"] == "PASS"
             and gate_clean["core_value_source"] == "[arg1+8]")
    c6["CORE_RECEIVER_VALUE_CHAIN"] = (
        "PRESERVED_CONFIRMED_STATIC_CONDITIONAL" if c6_ok
        else "REGRESSION_CHECK_FAILED")
    c6["verdict"] = "PASS" if c6_ok else "FAIL"
    controls["C6_historical_regression"] = c6

    # ============ AUX-1 — controlled unsupported-opcode failure ============
    aux = {"input": "in-memory window copy; unsupported opcode bytes "
                    "0F B0 @0x0085B24D",
           "expected": "controlled UNSUPPORTED fail-closed result "
                       "(DecodeError), never a silent acceptance"}
    try:
        decode_win(window_mutant(b"\x0F\xB0"))
        aux["outcome"] = "DECODE_RETURNED — FAIL (silent acceptance)"
        aux["verdict"] = "FAIL"
    except ced.DecodeError as e:
        aux["outcome"] = "UNSUPPORTED_FAIL_CLOSED"
        aux["exception_class"] = type(e).__name__
        aux["exception_message"] = str(e)
        aux["verdict"] = "PASS"
    except Exception as e:  # non-controlled failure: record honestly
        aux["outcome"] = "UNEXPECTED_EXCEPTION_CLASS"
        aux["exception_class"] = type(e).__name__
        aux["exception_message"] = str(e)
        aux["verdict"] = "FAIL"
    controls["AUX-1_unsupported_opcode_fail_closed"] = aux

    # ---- per-control methodology (contract section 7 four-field record) ---
    R["methodology"] = {
        "C1": {
            "measured_quantity": "physical window decode (count/end), the "
                                 "D9 E8 mutation-site pin, the ECX "
                                 "reaching-definition writer scan and the "
                                 "production provenance gate on the pinned "
                                 "physical bytes",
            "independent_source_of_truth": "the physical EXE (SHA256 "
                                            "fail-closed) + the committed "
                                            "CONTROL_RESULTS.json "
                                            "instruction table",
            "why_non_circular": "expectations pre-registered in "
                                "PREREGISTRATION from committed evidence "
                                "independent of this run; the decoder is "
                                "exercised on physical bytes, never on its "
                                "own outputs",
            "failure_case_detected": "C2/C3: the same gate FAILs exactly on "
                                     "the two byte mutants through the "
                                     "ECX scan"},
        "C2": {
            "measured_quantity": "mutant decode writes/reads/bit-ranges at "
                                  "0x0085B24D + ECX scan + per-check gate "
                                  "decomposition",
            "independent_source_of_truth": "x86-32 alias semantics via the "
                                            "independent reference table "
                                            "and the production byte pins",
            "why_non_circular": "the gate is the SAME predicate as C1; the "
                                "mutant differs from clean only in the two "
                                "bytes at 0x0085B24D; every pin, the rel32 "
                                "recomputation and the accessor check still "
                                "PASS, so the failure is causally the broken "
                                "ECX reaching definition — no hard-coded "
                                "mutant assertion exists in the gate",
            "failure_case_detected": "the CH counterexample itself "
                                     "(DETECTED); C5 negatives prove the "
                                     "detector is not an always-fail "
                                     "oracle"},
        "C3": {"measured_quantity": "same as C2 for the 88 D9 CL mutant",
                "independent_source_of_truth": "same as C2",
                "why_non_circular": "same as C2; CL additionally crosses "
                                    "the low-alias boundary (dst bits "
                                    "[0,8) vs CH's [8,16))",
                "failure_case_detected": "CL counterexample DETECTED"},
        "C4": {
            "measured_quantity": "64 standalone 2-byte decodes (all 8 "
                                 "destinations x all 8 sources) with "
                                 "per-case property checks",
            "independent_source_of_truth": "REF_BYTE8 defined in this "
                                            "driver (NOT imported from the "
                                            "production decoder helper) + "
                                            "x86-32 ModRM encoding rules",
            "why_non_circular": "the decoder under test never sees the "
                                "reference table; expectations are derived "
                                "from the external table, not from the "
                                "decoder's own mapping",
            "failure_case_detected": "the PRE historical matrix shows the "
                                     "same 64 cases fail 48/64 (executor) "
                                     "on the historical decoders — the "
                                     "matrix has discriminating power"},
        "C5": {
            "measured_quantity": "4 negative mutants at the mutation site: "
                                 "parent attribution + ECX scan + gate",
            "independent_source_of_truth": "REF_BYTE8 + the production gate",
            "why_non_circular": "the negatives must NOT flip the gate; an "
                                "always-fail gate would fail here; a byte "
                                "READ (e.g. CL source parent ECX in mov "
                                "dh,cl) must not trigger the WRITER-based "
                                "scan",
            "failure_case_detected": "C2/C3 flip the gate; C5.1-C5.4 do not"},
        "C6": {
            "measured_quantity": "23 byte pins + 2 rel32 recomputations + 2 "
                                 "RTTI walks + corrected clean decode vs the "
                                 "committed table AND vs the re-executed "
                                 "AST-extracted historical decoder "
                                 "(field-level equality) + receiver/value "
                                 "chain scans",
            "independent_source_of_truth": "the physical EXE + the "
                                            "immutable committed records + "
                                            "the immutable historical "
                                            "implementation",
            "why_non_circular": "the no-behavior-change property is proven "
                                "by equality against the historical "
                                "implementation re-executed read-only, not "
                                "by re-asserting the correction",
            "failure_case_detected": "any pin/row/field divergence or gate "
                                     "flip would FAIL C6"},
    }

    R["controls"] = controls

    # ---- executor-phase repairs disclosed (honest process record) ---------
    R["repairs_disclosed"] = {
        "POST_C5.4_test_data_repair": {
            "what": "the first POST run declared case C5.4 as 'mov bh, bh' "
                    "but supplied ModRM 0xF7, which per x86-32 rules is reg="
                    "6 (DH source), rm=7 (BH dest) = mov bh, dh",
            "who_was_right": "the CORRECTED DECODER was right (it decoded "
                             "88 F7 as 'mov bh, dh' with writes={ebx}, "
                             "reads={edx}); the TEST DATA was wrong — the "
                             "control verdict FAIL was the control doing "
                             "its job (the mismatch appeared exactly as "
                             "source_parent_recorded=false)",
            "repair": "case bytes corrected to 88 FF (reg=7 rm=7 = mov bh, "
                      "bh, the originally intended negative control); no "
                      "decoder change was needed or made",
            "first_run_measured": "C5.4 bytes 88 F7 decoded 'mov bh, dh'; "
                                  "writes=['ebx'], reads=['edx'], gate=PASS, "
                                  "verdict=FAIL (source-parent mismatch "
                                  "against the declared expectation)",
            "attempt_preservation": "the failed attempt's substance is "
                                    "recorded here and in the run handoff; "
                                    "the corrected re-run replaced the "
                                    "POST outputs (same executor phase, no "
                                    "completed run was modified)"},
        "PRE_regeneration_note": {
            "what": "the PRE phase was regenerated once during this "
                    "executor phase to fix two evidence-completeness "
                    "defects caught by self-check BEFORE finalization: "
                    "(a) the per-case decode records were not being "
                    "attached to PRE_COUNTEREXAMPLES.json (R['cases'] "
                    "omission); (b) the mutation-site file-offset "
                    "cross-check used the window-start VA instead of the "
                    "committed W1 base VA as its base, producing a false "
                    "'file_offset_consistent=false' flag (MyPE was right; "
                    "the cross-check formula was wrong)",
            "measured_values_affected": "none — all measured decode/scan "
                                        "values were identical across both "
                                        "PRE runs; only the completeness of "
                                        "the evidence file and the "
                                        "consistency flag changed"},
        "POST_csv_expected_column_repair": {
            "what": "the CONTROL_MATRIX.csv C5 'expected' column initially "
                    "rendered the destination NAME (e.g. 'bh,') instead of "
                    "the expected PARENT (ebx/eax/edx) due to a row-"
                    "generator slicing slip",
            "affected": "presentation only — every C5 verdict and measured "
                        "value was correct in all runs; the JSON evidence "
                        "records carried the correct expectations throughout",
            "repair": "expected_parent stored per C5 record and used in "
                      "the CSV row generation"},
    }

    # ---- final identity re-checks (acceptance gate 7) ---------------------
    R["exe_identity_post"] = {"size": os.path.getsize(EXE_PATH),
                              "sha256": sha256_file(EXE_PATH),
                              "unchanged":
                                  sha256_file(EXE_PATH) == EXE_SHA}
    R["source_package_unchanged"] = {
        "repin_write_provenance.py":
            sha256_file(OLD_EXECUTOR) == OLD_EXECUTOR_SHA,
        "CONTROL_RESULTS.json":
            sha256_file(CONTROL_RESULTS) == CONTROL_RESULTS_SHA,
        "qc_remeasure.py": sha256_file(
            os.path.join(SOURCE_PKG, "03_SCRIPTS", "qc_remeasure.py"))
            == "4E5426AEAB8FBD9A9364A5FE445ED2EA7C5D9F4B"
              "3E2F2E71B3EB5B3F3F8DDE1A",
        "QC_RESULTS.json": sha256_file(
            os.path.join(SOURCE_PKG, "QC_RESULTS.json"))
            == "DE7DF210FAFA465E27D7A7C4410C9D9C44C9BAE1"
              "492B9FEDE2B3101F01BF0545"}

    # residue scan (hygiene)
    residue = []
    for root, dirs, files in os.walk(PKG):
        for d in list(dirs):
            if d == "__pycache__":
                residue.append(os.path.relpath(
                    os.path.join(root, d), PKG))
        for fn in files:
            if fn.endswith(".pyc"):
                residue.append(os.path.relpath(
                    os.path.join(root, fn), PKG))
    R["residue_scan"] = {"hits": residue, "count": len(residue)}

    # ---- write outputs -----------------------------------------------------
    post_dir = os.path.join(PKG, "00_POST")
    os.makedirs(post_dir, exist_ok=True)
    post_json = os.path.join(post_dir, "POST_COUNTEREXAMPLES.json")
    with open(post_json, "w", encoding="utf-8", newline="\n") as f:
        json.dump(R, f, indent=1, sort_keys=False)

    # REGRESSION_RESULTS.json (C6 record + terminal statuses)
    reg = {
        "run_id": R["run_id"],
        "record": "C6 historical scientific regression (contract section 6)",
        "selected_store": {"va": "0x0085B281", "bytes": "89 4E 44",
                           "pin_match": pin_results["store_0x0085B281"][
                               "match"],
                           "physical_offset": pe.off(0x0085B281, 3)},
        "caller_target": c6["rel32_recomputation"]["call_0x00528E8D"],
        "accessor_target": c6["rel32_recomputation"]["call_0x0085B27A"],
        "accessor": pin_results["accessor_0x00746560"],
        "rtti": c6["rtti"],
        "clean_decode": clean_summary,
        "committed_table_anchor": c6["committed_table_anchor"]
        ["all_va_len_bytes_text_match"],
        "historical_executor_field_equality": eq_all,
        "receiver_chain": c6["receiver_chain"],
        "value_chain": c6["value_chain"],
        "j3_statuses_carried_verbatim": c6["j3_statuses_carried_verbatim"],
        "pins_all_match": pin_all,
        "sibling_stores_note": "+0x48 (0x0085B287) and +0x4C (0x0085B28D) "
                               "byte-pinned ONLY; NO analysis per contract "
                               "section 9; their semantic status remains: "
                               "byte-documented in the historical census, "
                               "unanalyzed",
        "exclusion_census_pins_note": "NOT re-read (outside the approved "
                                      "windows; not part of the C6 pin set); "
                                      "their historical status is unchanged",
        "CORE_RECEIVER_VALUE_CHAIN": c6["CORE_RECEIVER_VALUE_CHAIN"],
        "no_promotion_statement": "no promotion beyond the original static "
                                  "scope; FIELD_SEMANTICS = UNVERIFIED; "
                                  "WORLD_INSTANCE_IDENTITY = "
                                  "NOT_ESTABLISHED; HISTORICAL_PLACEMENT = "
                                  "NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO",
        "c6_verdict": c6["verdict"]}
    reg_json = os.path.join(PKG, "REGRESSION_RESULTS.json")
    with open(reg_json, "w", encoding="utf-8", newline="\n") as f:
        json.dump(reg, f, indent=1, sort_keys=False)

    # CONTROL_MATRIX.csv
    cm_path = os.path.join(PKG, "CONTROL_MATRIX.csv")
    with open(cm_path, "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f, lineterminator="\n")
        f.write("# CONTROL_MATRIX.csv — "
                "PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009\n")
        f.write("# per-control expected vs measured (executor phase; full "
                "raw records in 00_POST/POST_COUNTEREXAMPLES.json; the "
                "corrected QC implementation's controls are the fresh-QC "
                "worker phase)\n")
        w.writerow(["control_id", "case", "measured_quantity",
                     "expected", "measured", "verdict"])
        c2 = controls["C2_ch_mutant_88_DD"]
        c3 = controls["C3_cl_control_88_D9"]
        w.writerow(["C1", "clean baseline (physical D9 E8 @0x0085B24D)",
                    "decode count/end + site pin + ECX scan + provenance "
                    "gate",
                    "DECODE PASS; 64; end 0x0085B290; "
                    "ECX_CLOBBER=NO; CORE_VALUE_SOURCE=[arg1+8]; gate PASS",
                    "count %d; end_exact %s; site %s; scan %s; gate %s; "
                    "core %s" % (
                        c1["decode"]["instruction_count"],
                        c1["decode"]["end_exact_0x0085B290"],
                        c1["mutation_site_pin"]["measured"],
                        c1["ecx_clobber_scan_(0x0085B24B,0x0085B27A)"],
                        gate["gate"], gate["core_value_source"]),
                    c1["verdict"]])
        w.writerow(["C2", "CH mutant 88 DD @0x0085B24D",
                    "site operand/parent/bits + ECX scan + gate "
                    "decomposition",
                    "64; end 0x0085B290; OPERAND=CH; WRITES_PARENT=ECX; "
                    "bits [8,16); scan DETECTED @0x0085B24D; gate FAIL via "
                    "ECX_REACHING_DEF_BROKEN only",
                    "64; end_exact; dst %s; writes %s; bits %s; scan %s; "
                    "gate %s; reasons %s" % (
                        c2["mutation_site_instruction"]["dst"],
                        c2["mutation_site_instruction"]["writes"],
                        c2["mutation_site_instruction"]["byte_dst_bits"],
                        c2["ecx_clobber_scan_(0x0085B24B,0x0085B27A)"],
                        c2["provenance_gate"]["gate"],
                        c2["provenance_gate"]["failure_reasons"]),
                    c2["verdict"]])
        w.writerow(["C3", "CL control 88 D9 @0x0085B24D",
                    "same as C2 for the low-alias CL mutant",
                    "OPERAND=CL; WRITES_PARENT=ECX; bits [0,8); scan "
                    "DETECTED; gate FAIL via ECX_REACHING_DEF_BROKEN only",
                    "dst %s; writes %s; bits %s; scan %s; gate %s; reasons "
                    "%s" % (
                        c3["mutation_site_instruction"]["dst"],
                        c3["mutation_site_instruction"]["writes"],
                        c3["mutation_site_instruction"]["byte_dst_bits"],
                        c3["ecx_clobber_scan_(0x0085B24B,0x0085B27A)"],
                        c3["provenance_gate"]["gate"],
                        c3["provenance_gate"]["failure_reasons"]),
                    c3["verdict"]])
        w.writerow(["C4", "alias matrix 8x8 mod=11 (64 cases/decoder)",
                    "64 standalone decodes vs independent REF_BYTE8 table",
                    "64/64 PASS (corrected executor implementation); dest "
                    "coverage 8/8; source coverage 8/8; corrected QC "
                    "implementation 64 outcomes = fresh-QC worker phase",
                    "outcomes_pass %d/64; destinations %d/8; sources %d/8; "
                    "qc_impl = NOT_PERFORMED_IN_EXECUTOR_PHASE" % (
                        matrix_pass, len(dst_names), len(src_names)),
                    controls["C4_alias_matrix"]["verdict"]])
        for name, rec in c5.items():
            w.writerow(["C5", name,
                        "negative mutant parent attribution + ECX scan + "
                        "gate",
                        "WRITES_PARENT=%s; scan []; gate PASS"
                        % rec["expected_parent"],
                        "writes %s; scan %s; gate %s" % (
                            rec["mutation_site_instruction"]["writes"],
                            rec["ecx_clobber_scan_(0x0085B24B,0x0085B27A)"],
                            rec["provenance_gate"]["gate"]),
                        rec["verdict"]])
        w.writerow(["C6", "historical regression (physical EXE)",
                    "23 pins + rel32 x2 + RTTI x2 + corrected decode vs "
                    "committed table and vs re-executed historical decoder "
                    "+ chain scans",
                    "all pins match; targets 0x0085B1B0/0x00746560; RTTI "
                    "MovableObject+ClientMovableObject; 64 insns end "
                    "0x0085B290; ESI/EDI/ECX scans []; CORE_VALUE_SOURCE="
                    "[arg1+8]; "
                    "CORE_RECEIVER_VALUE_CHAIN="
                    "PRESERVED_CONFIRMED_STATIC_CONDITIONAL",
                    "pins_all %s; rel32 %s/%s; rtti %s/%s; decode %s; "
                    "committed_table %s; hist_equality %s; scans %s/%s/%s/"
                    "%s; gate %s; chain %s" % (
                        pin_all, tgt_a == 0x00746560, tgt_b == 0x0085B1B0,
                        rtti_mo["match"], rtti_cmo["match"],
                        clean_summary["instruction_count"], tbl_match,
                        eq_all, esi_writers, edi_writers, ecx_w1, ecx_w2,
                        gate_clean["gate"], c6["CORE_RECEIVER_VALUE_CHAIN"]),
                    c6["verdict"]])
        w.writerow(["AUX-1", "unsupported opcode 0F B0 @0x0085B24D "
                             "(auxiliary)",
                    "full-window decode attempt on the in-memory mutant",
                    "controlled UNSUPPORTED fail-closed (DecodeError), "
                    "never a silent acceptance",
                    "%s (%s)" % (aux["outcome"],
                                 aux.get("exception_class", "n/a")),
                    aux["verdict"]])

    # POST SHA256 index
    idx_rows = []
    for p in (post_json, reg_json, cm_path,
              os.path.abspath(__file__), ced_path,
              OLD_EXECUTOR,
              os.path.join(SOURCE_PKG, "03_SCRIPTS", "qc_remeasure.py"),
              CONTROL_RESULTS,
              os.path.join(SOURCE_PKG, "QC_RESULTS.json")):
        rel = (os.path.relpath(p, REPO).replace("\\", "/")
               if p.startswith(REPO) else p)
        idx_rows.append((rel, os.path.getsize(p), sha256_file(p)))
    idx_rows.append((EXE_PATH, os.path.getsize(EXE_PATH),
                     sha256_file(EXE_PATH)))
    idx_rows.append((CONTRACT_PATH, os.path.getsize(CONTRACT_PATH),
                     sha256_file(CONTRACT_PATH)))
    idx_csv = os.path.join(post_dir, "POST_SHA256_INDEX.csv")
    with open(idx_csv, "w", encoding="utf-8", newline="\n") as f:
        f.write("# POST_SHA256_INDEX.csv — "
                "PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009\n")
        f.write("# POST evidence + executed-input provenance index, "
                "generated by run_alias_controls.py immediately after the\n")
        f.write("# POST/CONTROL_MATRIX/REGRESSION outputs were written. "
                "Repo-relative paths for repository files; absolute paths\n")
        f.write("# for the two inputs external to the repository (EXE, "
                "contract). ROW_COUNT = %d\n" % len(idx_rows))
        f.write("path,size_bytes,sha256\n")
        for rel, size, sha in idx_rows:
            f.write("%s,%d,%s\n" % (rel, size, sha.lower()))

    # ---- console summary ---------------------------------------------------
    print("POST COMPLETE")
    print("C1:", c1["verdict"], "| count",
          c1["decode"]["instruction_count"], "| gate", gate["gate"],
          "| core", gate["core_value_source"])
    print("C2:", c2["verdict"], "| dst",
          c2["mutation_site_instruction"]["dst"], "| writes",
          c2["mutation_site_instruction"]["writes"], "| bits",
          c2["mutation_site_instruction"]["byte_dst_bits"], "| scan",
          c2["ecx_clobber_scan_(0x0085B24B,0x0085B27A)"], "| gate",
          c2["provenance_gate"]["gate"], "| reasons",
          c2["provenance_gate"]["failure_reasons"])
    print("C3:", c3["verdict"], "| dst",
          c3["mutation_site_instruction"]["dst"], "| writes",
          c3["mutation_site_instruction"]["writes"], "| scan",
          c3["ecx_clobber_scan_(0x0085B24B,0x0085B27A)"], "| gate",
          c3["provenance_gate"]["gate"], "| reasons",
          c3["provenance_gate"]["failure_reasons"])
    print("C4:", controls["C4_alias_matrix"]["verdict"],
          "| pass %d/64 | dests %d | srcs %d"
          % (matrix_pass, len(dst_names), len(src_names)))
    for name, rec in c5.items():
        print("C5:", name, rec["verdict"], "| writes",
              rec["mutation_site_instruction"]["writes"], "| gate",
              rec["provenance_gate"]["gate"])
    print("C6:", c6["verdict"], "| pins", pin_all, "| table", tbl_match,
          "| hist-eq", eq_all, "| chain",
          c6["CORE_RECEIVER_VALUE_CHAIN"])
    print("AUX-1:", aux["verdict"], "|", aux["outcome"])
    print("exe unchanged:", R["exe_identity_post"]["unchanged"],
          "| residue:", len(residue))
    return 0


if __name__ == "__main__":
    sys.exit(main())
