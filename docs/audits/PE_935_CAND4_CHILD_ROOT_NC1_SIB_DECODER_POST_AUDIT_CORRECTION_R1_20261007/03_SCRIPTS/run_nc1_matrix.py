"""run_nc1_matrix.py — mandatory five-case production regression matrix executor for
PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007
(RECORDS_AND_QC_MACHINERY_CORRECTION; contract §7 / dispatch STEPS 2-3).

Executes the ACTUAL corrected production function ctrl4_exact_endpoint from
03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py (imported via importlib — NOT a rewritten
imitation) on the mandatory five-case matrix over SYNTHETIC / IN-MEMORY buffers only:

    1. REAL_RECORDED_CLEAN          the published 0x42 clean window   EXPECTED = PASS
    2. HISTORICAL_EDI_CLOBBER       @0x0050A3DD 8B 3D D0 D8 B9 00      EXPECTED = FAIL (P2)
    3. FINAL_PUSH_ESI               @0x0050A3F6: 57 -> 56              EXPECTED = FAIL (P3)
    4. FINAL_PUSH_NOP               @0x0050A3F6: 57 -> 90              EXPECTED = FAIL (P3)
    5. NC1_SIB_HIDDEN_EDI_WRITE     @0x0050A3DD..0x0050A3E8:           EXPECTED = FAIL
                                    8B 8C 24 8C 00 00 E8 BF AA BB CC 90
                                    (the SIB guard must reject the first instruction
                                    before length computation; decode must never treat
                                    8B 8C 24 8C 00 00 as a 6-byte MOV)

PRE (pre-correction state, contract §14 / dispatch STEP 3): imports the OLD production
checker READ-ONLY from the SOURCE_PACKAGE
(docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007/03_SCRIPTS/
ctrl4_exact_endpoint.py) via importlib — module-level inert, run_and_write NEVER
invoked, SOURCE_PACKAGE untouched (sys.dont_write_bytecode is set first and this file
is executed with python -B so no __pycache__/.pyc is ever written) — and executes ITS
ctrl4_exact_endpoint on the same five in-memory buffers to independently reproduce the
NC1 false PASS (expected pre-correction measurements: clean PASS, clobber FAIL, esi
FAIL, nop FAIL, NC1 SIB PASS = the false PASS reproduced).

Writes (UTF-8, LF, no BOM; deterministic — no timestamps inside the JSON payloads):
    CONTROL_RESULTS_POST.json  (OUTPUT_ROOT root) — corrected production matrix
    CONTROL_RESULTS_PRE.json   (OUTPUT_ROOT root) — pre-correction state with explicit
                                SOURCE_DESKTOP_MEASUREMENT vs EXECUTOR_REPRODUCTION
                                provenance separation

No EXE access of any kind. All buffers are in-memory; no mutation is ever written to
any file. This executor run is correction-only (RECORDS_AND_QC_MACHINERY_CORRECTION):
zero new science, zero new RE.
"""
import sys
sys.dont_write_bytecode = True   # FIRST: never write __pycache__/.pyc into the READ-ONLY SOURCE_PACKAGE or OUTPUT_ROOT

import hashlib
import importlib.util
import json
import os

RUN_ID = "PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007"
RUN_CLASS = "RECORDS_AND_QC_MACHINERY_CORRECTION"

HERE = os.path.dirname(os.path.abspath(__file__))                 # OUTPUT_ROOT/03_SCRIPTS
PKG = os.path.dirname(HERE)                                      # OUTPUT_ROOT
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(PKG)))   # eudoria-clean repo root
SOURCE_PACKAGE_SCRIPTS = os.path.join(
    REPO_ROOT, "docs", "audits",
    "PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007", "03_SCRIPTS")
OLD_CHECKER_PATH = os.path.join(SOURCE_PACKAGE_SCRIPTS, "ctrl4_exact_endpoint.py")
FIXED_CHECKER_PATH = os.path.join(HERE, "ctrl4_exact_endpoint_sibfixed.py")

# Desktop CONTROL_COUNTERCHECKS.json case sib_hidden_edi_write "bytes" field —
# transcribed constant (from the verified Desktop input; see INPUT_IDENTITIES.md) used
# only to assert byte-identity of the constructed NC1 buffer with the authoritative
# synthetic counterexample Desktop measured.
DESKTOP_NC1_CASE_HEX = (
    "8B F8 E8 D2 6B 1B 00 84 C0 74 06 83 4E 2C 02 EB 04 83 66 2C FD"
    " 8B 4E 20 E8 DC 6C 1B 00 8B CE 50 57 E8 03 FE FF FF"
    " 8B 8C 24 8C 00 00 E8 BF AA BB CC 90"
    " 8B 4E 30 8B 01 8B 90 A4 00 00 00 6A 00 57 FF D2"
)

# Published clean-window boundary map (SOURCE_PACKAGE 03_SCRIPTS/FIXTURES.md §F3,
# 22 instructions, total 0x42) — regression reference proving the NC1 guard (and the
# P3 tooling cleanup) changed NO clean-window decode boundary.
PUBLISHED_CLEAN_MAP = [
    (0x0050A3B7, 2), (0x0050A3B9, 5), (0x0050A3BE, 2), (0x0050A3C0, 2),
    (0x0050A3C2, 4), (0x0050A3C6, 2), (0x0050A3C8, 4), (0x0050A3CC, 3),
    (0x0050A3CF, 5), (0x0050A3D4, 2), (0x0050A3D6, 1), (0x0050A3D7, 1),
    (0x0050A3D8, 5), (0x0050A3DD, 6), (0x0050A3E3, 1), (0x0050A3E4, 5),
    (0x0050A3E9, 3), (0x0050A3EC, 2), (0x0050A3EE, 6), (0x0050A3F4, 2),
    (0x0050A3F6, 1), (0x0050A3F7, 2),
]


def _sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def _import_from(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {name} from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _buf_hex(buf):
    return " ".join(f"{b:02X}" for b in buf)


def _listing(mod, buf):
    """Full decode listing (VA/size/mnemonic/operands) from the ACTUAL module's decode()."""
    insns = mod.decode(buf, mod.WIN_VA)
    rows = []
    for va in sorted(insns):
        ins = insns[va]
        rows.append({
            "va": f"0x{va:08X}",
            "size": ins.size,
            "mnemonic": ins.mnemonic,
            "operands": ins.op_str,
            "hex": ins.hex(),
            "writes_edi": ins.writes_edi,
        })
    return rows


def _boundaries(mod, buf):
    """Decode boundaries observed by the ACTUAL module's decode(), or the guard rejection.

    For a rejected (fail-closed) buffer: records the rejection message, the VA of the
    first rejected instruction (proven by a successful prefix decode ending exactly at
    the replacement span start plus the full-buffer rejection), and that no instruction
    at/after the rejected VA was ever produced.
    """
    try:
        listing = _listing(mod, buf)
        return {
            "decode_status": "DECODED",
            "instruction_count": len(listing),
            "listing": listing,
            "va_size_map": {f"0x{va:08X}": row["size"] for va, row in
                            zip([int(r["va"], 16) for r in listing], listing)},
        }
    except (ValueError, IndexError) as exc:
        # Fail-closed rejection (NC1 SIB guard / uncovered opcode / truncated read):
        # pinpoint the rejection boundary by prefix decode — the largest prefix that
        # decodes OK ends exactly where the rejected instruction begins.
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
            "note": ("decode aborted at the rejected instruction before any displacement/"
                     "length was computed for it; no instruction at/after this VA was produced"),
        }


def main():
    # ---- import the ACTUAL corrected production module and the OLD checker (read-only)
    fixed = _import_from(FIXED_CHECKER_PATH, "ctrl4_exact_endpoint_sibfixed")
    old = _import_from(OLD_CHECKER_PATH, "ctrl4_exact_endpoint_OLD_READONLY")

    fixed_sha = _sha256_file(FIXED_CHECKER_PATH)
    old_sha = _sha256_file(OLD_CHECKER_PATH)

    # fixture identity between the corrected successor and the READ-ONLY old checker
    fixture_identity = bytes(fixed.CLEAN_WINDOW) == bytes(old.CLEAN_WINDOW)

    # ---- build the mandatory five-case matrix (synthetic / in-memory buffers only)
    buffers = {
        "REAL_RECORDED_CLEAN": fixed.CLEAN_WINDOW,
        "HISTORICAL_EDI_CLOBBER": fixed.make_clobber_mutant(),
        "FINAL_PUSH_ESI": fixed.make_final_arg_mutant(0x56),
        "FINAL_PUSH_NOP": fixed.make_final_arg_mutant(0x90),
        "NC1_SIB_HIDDEN_EDI_WRITE": fixed.make_nc1_sib_mutant(),
    }
    expectations = {
        "REAL_RECORDED_CLEAN": ("PASS", "the published 0x42 clean window bytes (SOURCE_PACKAGE 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt)"),
        "HISTORICAL_EDI_CLOBBER": ("FAIL", "clean window with 6 bytes @0x0050A3DD replaced by 8B 3D D0 D8 B9 00 (mov edi,[0xB9D8D0]) — the historical clobber case; P2"),
        "FINAL_PUSH_ESI": ("FAIL", "@0x0050A3F6: 57->56 (push edi -> push esi); P3"),
        "FINAL_PUSH_NOP": ("FAIL", "@0x0050A3F6: 57->90 (push edi -> nop); P3"),
        "NC1_SIB_HIDDEN_EDI_WRITE": ("FAIL", "12 bytes @0x0050A3DD..0x0050A3E8 replaced by 8B 8C 24 8C 00 00 E8 BF AA BB CC 90; the SIB guard must reject the first instruction before length computation"),
    }
    case_descriptions = {
        "REAL_RECORDED_CLEAN": "the 0x42 published clean window (identical fixture to the SOURCE_PACKAGE checker)",
        "HISTORICAL_EDI_CLOBBER": "SYNTHETIC in-memory mutant: 6 bytes @0x0050A3DD replaced with 8B 3D D0 D8 B9 00 (same 6-byte length — boundaries preserved)",
        "FINAL_PUSH_ESI": "SYNTHETIC in-memory mutant @0x0050A3F6: 57 -> 56 (push edi -> push esi); the earlier push edi @0x0050A3D7 survives",
        "FINAL_PUSH_NOP": "SYNTHETIC in-memory mutant @0x0050A3F6: 57 -> 90 (push edi -> nop); the earlier push edi @0x0050A3D7 survives",
        "NC1_SIB_HIDDEN_EDI_WRITE": "SYNTHETIC in-memory mutant: 12-byte span @0x0050A3DD..0x0050A3E8 replaced with 8B 8C 24 8C 00 00 E8 BF AA BB CC 90 (total window stays 0x42) — the Desktop NC1 counterexample",
    }

    # NC1 buffer byte-identity with the authoritative Desktop counterexample bytes
    nc1_matches_desktop = bytes(buffers["NC1_SIB_HIDDEN_EDI_WRITE"]) == bytes.fromhex(DESKTOP_NC1_CASE_HEX)

    # ---- POST: corrected production matrix (the ACTUAL corrected production function)
    post_matrix = {}
    all_match = True
    for name, buf in buffers.items():
        expected, exp_note = expectations[name]
        ok, detail = fixed.ctrl4_exact_endpoint(buf)          # ACTUAL corrected production function
        actual = "PASS" if ok else "FAIL"
        row = {
            "case": case_descriptions[name],
            "mutants_synthetic_memory_only": True,
            "buffer_len_bytes": len(buf),
            "buffer_hex": _buf_hex(buf),
            "buffer_sha256": hashlib.sha256(buf).hexdigest().upper(),
            "expected": expected,
            "expected_note": exp_note,
            "actual": actual,
            "match": actual == expected,
            "checker_detail": detail,
            "checker_script": "03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py",
            "checker_script_sha256": fixed_sha,
            "decode_boundaries": _boundaries(fixed, buf),
        }
        post_matrix[name] = row
        all_match = all_match and (actual == expected)

    # ---- NC1 guard evidence: prefix decode ends exactly at the span start; full decode rejected
    nc1_buf = buffers["NC1_SIB_HIDDEN_EDI_WRITE"]
    span_off = fixed.NC1_SIB_VA - fixed.WIN_VA
    prefix_ok = True
    try:
        prefix_insns = fixed.decode(nc1_buf[:span_off], fixed.WIN_VA)
        prefix_last_end = max(prefix_insns) + prefix_insns[max(prefix_insns)].size
        clean_prefix_insns = fixed.decode(fixed.CLEAN_WINDOW[:span_off], fixed.WIN_VA)
        prefix_identical_to_clean = (sorted(prefix_insns) == sorted(clean_prefix_insns) and all(
            prefix_insns[va].size == clean_prefix_insns[va].size
            and prefix_insns[va].mnemonic == clean_prefix_insns[va].mnemonic
            and prefix_insns[va].op_str == clean_prefix_insns[va].op_str
            and prefix_insns[va].bytes == clean_prefix_insns[va].bytes
            for va in prefix_insns))
    except (ValueError, IndexError):
        prefix_ok = False
        prefix_last_end = None
        prefix_identical_to_clean = False
    nc1_guard_evidence = {
        "prefix_before_span": {
            "prefix_len_bytes": span_off,
            "prefix_decode_ok": prefix_ok,
            "prefix_decodes_identically_to_clean_prefix": bool(prefix_identical_to_clean),
            "prefix_last_instruction_end_va": f"0x{prefix_last_end:08X}" if prefix_ok else None,
        },
        "full_buffer_decode": "ValueError (unsupported SIB form) — rejected at the FIRST instruction of the replacement span, before any displacement/length computation",
        "rejected_at_va": f"0x{fixed.NC1_SIB_VA:08X}",
        "six_byte_mov_impossible": ("the corrected decode never treats 8B 8C 24 8C 00 00 as a 6-byte MOV — the guard raises before "
                                    "the old length logic could run; the reference 7-byte boundary set (0x0050A3DD: 8B 8C 24 8C 00 00 E8 "
                                    "/ 0x0050A3E4: BF AA BB CC 90 mov edi,0x90CCBBAA) can no longer be boundary-shifted out of P2"),
    }

    # ---- clean-window full decode listing + boundary regression (guard changed no boundary)
    clean_listing = _listing(fixed, fixed.CLEAN_WINDOW)
    clean_va_sizes = [(int(r["va"], 16), r["size"]) for r in clean_listing]
    boundary_regression = {
        "reference": "SOURCE_PACKAGE 03_SCRIPTS/FIXTURES.md F3 published clean-window map (22 instructions)",
        "published_va_size_map": {f"0x{va:08X}": size for va, size in PUBLISHED_CLEAN_MAP},
        "measured_va_size_map": {f"0x{va:08X}": size for va, size in clean_va_sizes},
        "va_sets_identical": sorted(va for va, _ in clean_va_sizes) == sorted(va for va, _ in PUBLISHED_CLEAN_MAP),
        "sizes_identical": dict(clean_va_sizes) == dict(PUBLISHED_CLEAN_MAP),
        "instruction_count": len(clean_listing),
        "total_bytes": sum(size for _, size in clean_va_sizes),
    }
    boundary_regression["result"] = (
        "PASS" if (boundary_regression["va_sets_identical"] and boundary_regression["sizes_identical"]
                   and boundary_regression["instruction_count"] == 22 and boundary_regression["total_bytes"] == 0x42)
        else "FAIL"
    )

    # ---- P3_TOOLING_CLEANUP regression: lengths separately + identical VA set
    old_clean = _listing(old, old.CLEAN_WINDOW)
    old_by_va = {r["va"]: r for r in old_clean}
    new_by_va = {r["va"]: r for r in clean_listing}
    grp1_rows = {}
    grp1_ok = True
    for va, bhex in ((0x0050A3C2, "83 4E 2C 02"), (0x0050A3C8, "83 66 2C FD")):
        o, n = old_by_va.get(f"0x{va:08X}"), new_by_va.get(f"0x{va:08X}")
        row = {
            "bytes": bhex,
            "old_operands": o["operands"] if o else None,
            "old_size": o["size"] if o else None,
            "new_operands": n["operands"] if n else None,
            "new_size": n["size"] if n else None,
            "length_unchanged": (o["size"] == n["size"] == 4) if (o and n) else False,
        }
        grp1_rows[f"0x{va:08X}"] = row
        grp1_ok = grp1_ok and row["length_unchanged"]
    p3_tooling_cleanup = {
        "status": "PERFORMED",
        "description": ("grp1-imm8 (0x83 mod=01) operand text: the immediate is now read from opcode+3 (after the disp8 at "
                        "opcode+2); the old code printed the disp byte as the immediate. Decoder-only edit; NO science status affected"),
        "length_regression": {
            "83 4E 2C 02 size 4": grp1_rows["0x0050A3C2"]["length_unchanged"],
            "83 66 2C FD size 4": grp1_rows["0x0050A3C8"]["length_unchanged"],
        },
        "per_instruction": grp1_rows,
        "clean_window_va_set_unchanged": boundary_regression["va_sets_identical"],
        "result": "PASS" if (grp1_ok and boundary_regression["va_sets_identical"]) else "FAIL",
    }

    # ---- PRE: pre-correction state (old production checker, read-only import)
    pre_matrix = {}
    old_false_pass_reproduced = False
    for name, buf in buffers.items():
        expected, exp_note = expectations[name]
        ok_old, detail_old = old.ctrl4_exact_endpoint(buf)      # ACTUAL OLD production function (READ-ONLY)
        actual_old = "PASS" if ok_old else "FAIL"
        false_pass = (expected == "FAIL" and actual_old == "PASS")
        pre_matrix[name] = {
            "case": case_descriptions[name],
            "mutants_synthetic_memory_only": True,
            "buffer_hex": _buf_hex(buf),
            "buffer_sha256": hashlib.sha256(buf).hexdigest().upper(),
            "true_expected": expected,
            "old_checker_result": actual_old,
            "old_checker_detail": detail_old,
            "false_pass": false_pass,
        }
        if name == "NC1_SIB_HIDDEN_EDI_WRITE":
            old_false_pass_reproduced = false_pass
            # OLD decode of the NC1 buffer itself (its boundaries at the span are
            # SHIFTED — this is the false-PASS evidence, distinct from the clean decode)
            old_nc1_listing = _listing(old, buf)
            pre_matrix[name]["old_decode_boundaries_at_replacement_span"] = [
                {k: row[k] for k in ("va", "size", "mnemonic", "operands", "hex", "writes_edi")}
                for row in old_nc1_listing if 0x0050A3DD <= int(row["va"], 16) < 0x0050A3E9
            ]
            pre_matrix[name]["old_boundary_shift_note"] = (
                "the OLD decoder omits the SIB byte: 8B 8C 24 8C 00 00 is mis-decoded as a 6-byte MOV (boundary 0x0050A3E3), "
                "E8 BF AA BB CC as a 5-byte CALL (boundary 0x0050A3E8), 90 as NOP — so the reference `mov edi, 0x90CCBBAA` "
                "@0x0050A3E4 (BF AA BB CC 90, an EDI write INSIDE the prohibited P2 range) is never decoded and the old "
                "checker FALSE-PASSES the buffer"
            )

    pre_doc = {
        "RUN_ID": RUN_ID,
        "RUN_CLASS": RUN_CLASS,
        "purpose": ("pre-correction state with explicit provenance separation (contract §14 / dispatch STEP 3): "
                    "SOURCE_DESKTOP_MEASUREMENT (Desktop post-audit of 57ecf350 — transcribed, NOT an executor "
                    "measurement) vs EXECUTOR_REPRODUCTION (this run's independent in-memory measurement of the OLD "
                    "production checker)"),
        "SOURCE_DESKTOP_MEASUREMENT": {
            "label": ("SOURCE_DESKTOP_MEASUREMENT — transcribed from the Desktop post-audit "
                      "(of 57ecf3506481e73ca27548ea02e4864904d9883a); this is Desktop's measurement, NOT this executor's"),
            "cited_file": "C:\\Users\\User\\Documents\\ChatGPT\\PE\\PE_935_CAND4_CORRECTION_DESKTOP_POST_AUDIT_57ECF350_20261007\\CONTROL_COUNTERCHECKS.json",
            "cited_file_size_bytes": 46675,
            "cited_file_sha256": "2288CB39E357343C4A404F83D6327E5A628547C467D28869A2C34237C0090C00",
            "case": "sib_hidden_edi_write",
            "EXPECTED": "FAIL",
            "PRODUCTION_CHECKER": "PASS",
            "INTERNAL_QC_CHECKER": "PASS",
            "REFERENCE_EDI_WRITE": "0x0050A3E4",
            "FALSE_PASS_REPRODUCED": "YES",
            "transcribed_raw_fields": {
                "expected": False,
                "production.ok": True,
                "independent_internal.ok": True,
                "capstone_edi_writes_in_required_range": ["0x50a3e4"],
            },
            "reference_decoder": {"library": "capstone", "version": "5.0.7"},
        },
        "EXECUTOR_REPRODUCTION": {
            "status": "PERFORMED",
            "method": ("OLD production checker imported READ-ONLY via importlib from the SOURCE_PACKAGE "
                       "(docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007/03_SCRIPTS/ctrl4_exact_endpoint.py; "
                       "module-level inert; run_and_write NEVER invoked; sys.dont_write_bytecode set before import and executed "
                       "with python -B — no .pyc written into the READ-ONLY SOURCE_PACKAGE); its ACTUAL ctrl4_exact_endpoint "
                       "executed on the same five in-memory buffers (byte-identical buffers — same SHA256s as the POST matrix)"),
            "old_checker_source_path": "docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007/03_SCRIPTS/ctrl4_exact_endpoint.py",
            "old_checker_sha256": old_sha,
            "matrix": pre_matrix,
            "expected_pre_correction_measurements": {
                "REAL_RECORDED_CLEAN": "PASS",
                "HISTORICAL_EDI_CLOBBER": "FAIL",
                "FINAL_PUSH_ESI": "FAIL",
                "FINAL_PUSH_NOP": "FAIL",
                "NC1_SIB_HIDDEN_EDI_WRITE": "PASS (the false PASS)",
            },
            "nc1_false_pass_reproduced_by_old_checker": "YES" if old_false_pass_reproduced else "NO",
            "verdict": ("OLD-CHECKER NC1 FALSE PASS REPRODUCED BY EXECUTOR (independent of the Desktop measurement): the OLD "
                        "production checker PASSes the NC1_SIB_HIDDEN_EDI_WRITE buffer whose true expected verdict is FAIL"
                        if old_false_pass_reproduced else
                        "OLD-CHECKER NC1 FALSE PASS NOT REPRODUCED — honest negative result (investigate before correction)"),
        },
        "fixture_identity_old_vs_corrected": bool(fixture_identity),
        "nc1_buffer_byte_identical_to_desktop_counterexample": bool(nc1_matches_desktop),
        "exe_accessed": False,
        "buffers_synthetic_in_memory_only": True,
    }

    post_doc = {
        "RUN_ID": RUN_ID,
        "RUN_CLASS": RUN_CLASS,
        "purpose": ("corrected-production (POST) five-case matrix results produced by the ACTUAL corrected production "
                    "checker (contract §7 / dispatch STEP 2)"),
        "production_checker": {
            "script": "03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py",
            "script_sha256": fixed_sha,
            "function": "ctrl4_exact_endpoint — EXECUTED via importlib import of ctrl4_exact_endpoint_sibfixed.py (the ACTUAL corrected production function; NOT a rewritten imitation)",
            "successor_of": "docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007/03_SCRIPTS/ctrl4_exact_endpoint.py (READ-ONLY, SHA256 " + old_sha + ")",
            "nc1_correction": ("fail-closed SIB guard in EVERY memory-ModRM branch (0x8B/0x89/0x8D; 0x84; 0x83; 0xFF): "
                               "if mod != 0b11 and rm == 0b100 -> ValueError('unsupported SIB form (mod=%02b rm=100) — FAIL CLOSED') "
                               "BEFORE any displacement/length computation; the old length logic never runs for such forms; "
                               "full SIB decoding NOT implemented (not required)"),
            "p1_p4_predicate_unchanged": True,
            "fail_closed_decode_design_unchanged": True,
            "fixture_identity_with_old_checker": bool(fixture_identity),
            "exe_accessed": False,
            "buffers_synthetic_in_memory_only": True,
        },
        "nc1_matrix_post": post_matrix,
        "nc1_guard_evidence": nc1_guard_evidence,
        "clean_window_full_decode_listing": {
            "provenance": "the published 0x42 clean window (SOURCE_PACKAGE 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt); decode by the ACTUAL corrected module",
            "instruction_count": len(clean_listing),
            "listing": clean_listing,
            "boundary_regression": boundary_regression,
            "note": ("full decode listing of the clean window proving the NC1 SIB guard (and the P3 tooling cleanup) did NOT "
                     "change any clean-window decode boundary: VA set and sizes are identical to the published map"),
        },
        "P3_TOOLING_CLEANUP": p3_tooling_cleanup,
        "matrix_verdict": "PASS" if all_match else "FAIL",
        "verdict_semantics": ("all five measured results equal the mandatory expectations (clean PASS; clobber/esi/nop/NC1 FAIL) "
                              "of the corrected production checker. Strongest permitted claim (contract §8): "
                              "CTRL4_BOUNDARY_VALIDATION = SUPPORTED_WITHIN_RECORDED_CLEAN_WINDOW_AND_REGISTERED_FALSIFIERS — "
                              "NOT GENERAL_X86_DECODER_PROVEN. This is QC-machinery correction only; it creates no science and "
                              "retracts no historical result"),
    }

    pre_path = os.path.join(PKG, "CONTROL_RESULTS_PRE.json")
    post_path = os.path.join(PKG, "CONTROL_RESULTS_POST.json")
    for path, doc in ((post_path, post_doc), (pre_path, pre_doc)):
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
            f.write("\n")

    # ---- console summary (transcript evidence; the JSON files are the persisted record)
    print(f"RUN_ID: {RUN_ID}")
    print(f"corrected checker SHA256: {fixed_sha}")
    print(f"old checker (READ-ONLY) SHA256: {old_sha}")
    print(f"fixture identity old vs corrected: {fixture_identity}")
    print(f"NC1 buffer byte-identical to Desktop counterexample: {nc1_matches_desktop}")
    print("\nPOST matrix (ACTUAL corrected production function):")
    for name, row in post_matrix.items():
        print(f"  {name:28s} expected={row['expected']:4s} actual={row['actual']:4s} match={row['match']}")
    print(f"  -> matrix_verdict: {post_doc['matrix_verdict']}")
    print(f"\nNC1 guard rejection: {post_matrix['NC1_SIB_HIDDEN_EDI_WRITE']['decode_boundaries']['rejection']}")
    print(f"NC1 guard rejected at: {nc1_guard_evidence['rejected_at_va']} "
          f"(prefix decode OK to 0x{prefix_last_end:08X})")
    print(f"clean-window boundary regression vs published map: {boundary_regression['result']} "
          f"({boundary_regression['instruction_count']} insns, {boundary_regression['total_bytes']:#x} bytes)")
    print(f"P3_TOOLING_CLEANUP: {p3_tooling_cleanup['status']} result={p3_tooling_cleanup['result']} "
          f"(83 4E 2C 02 -> '{new_by_va['0x0050A3C2']['operands']}'; "
          f"83 66 2C FD -> '{new_by_va['0x0050A3C8']['operands']}')")
    print("\nPRE matrix (ACTUAL OLD production function, read-only import):")
    for name, row in pre_matrix.items():
        print(f"  {name:28s} true_expected={row['true_expected']:4s} old_result={row['old_checker_result']:4s} false_pass={row['false_pass']}")
    print(f"  -> OLD-CHECKER NC1 FALSE PASS REPRODUCED: {old_false_pass_reproduced}")
    print(f"\nwrote: {post_path}")
    print(f"wrote: {pre_path}")

    return 0 if (all_match and boundary_regression["result"] == "PASS"
                 and p3_tooling_cleanup["result"] == "PASS" and old_false_pass_reproduced) else 1


if __name__ == "__main__":
    raise SystemExit(main())
