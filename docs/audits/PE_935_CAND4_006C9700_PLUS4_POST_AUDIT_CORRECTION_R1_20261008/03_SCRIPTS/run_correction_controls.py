"""run_correction_controls.py — controls of
PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008.

Executes, against checker_plus4_successor.py (the successor production gate):
  - the 80-historical-check-ID regression (complete ID set vs the historical
    03_SCRIPTS/checker_plus4.py of the READ_ONLY source package, parsed
    read-only via AST — never executed; missing/duplicate/empty blocks PASS);
  - the required mapper/record controls (contract par. 4 list 1-7);
  - MC1..MC5 reproduction on the successor production gate (in-memory TEST
    OVERRIDE copies only; each must FAIL exactly on the proper anchor);
  - MC6 specificity (a DIRECT PHYSICAL FILE OFFSET 0x7A1100 mutation — a
    .rsrc raw byte; NOT a read of VA 0x00BA1100; VA and file offset are
    separate units);
  - the REC-W record mutation gates (byte-hex-only / displacement-only /
    target-only mutations of an IN-MEMORY copy of ACTIVE_CORRECTED_PINS.json;
    each must flip the corresponding production record gate, proving the
    JSON actually drives the gates);
  - the two FD-C2 logical control models (synthetic [this-4]:=Q countermodel
    + field-preserving model) — LOGICAL_CONTROLS_SCOPE = SYNTHETIC_ONLY.

Writes MAPPER_RESULTS.json, REGRESSION_RESULTS.json, LOGICAL_CONTROL_RESULTS.json
(UTF-8, LF, no BOM, deterministic key order). python -B; no bytecode; the
physical EXE is NEVER modified (identity measured before and after all
controls); the JSON record file and the source package are NEVER modified.
"""
import ast
import copy
import hashlib
import json
import os
import struct
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
PKG_ROOT = os.path.dirname(HERE)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(PKG_ROOT)))
sys.path.insert(0, HERE)

import checker_plus4_successor as succ  # noqa: E402

HIST_CHECKER = os.path.join(
    REPO_ROOT, "docs", "audits",
    "PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008",
    "03_SCRIPTS", "checker_plus4.py")
HIST_CHECKER_SHA256 = ("F58D2DB36106006BA2CBF931DC9CFED872E"
                       "9C5E22C5484E86462568B985AB7E8")
PINS_JSON = os.path.join(PKG_ROOT, "ACTIVE_CORRECTED_PINS.json")
OUT_MAPPER = os.path.join(PKG_ROOT, "MAPPER_RESULTS.json")
OUT_REGRESSION = os.path.join(PKG_ROOT, "REGRESSION_RESULTS.json")
OUT_LOGICAL = os.path.join(PKG_ROOT, "LOGICAL_CONTROL_RESULTS.json")

MC6_PHYS_OFFSET = 0x7A1100  # a DIRECT physical file offset (.rsrc raw byte)


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest().upper()


def wjson(path, doc):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=2, ensure_ascii=True)
        f.write("\n")


# ---------------------------------------------------------------------------
# Synthetic PE builder (mapper controls 3-6 only; NEVER the physical EXE)
# ---------------------------------------------------------------------------
def make_synthetic_pe(sections, image_base=0x00400000, file_size=None,
                      filler=0xCC):
    """Build a minimal synthetic PE32 image. sections = [(name, va, vsize,
    rsize, roff), ...]; raw bytes are the filler pattern by default; the file
    can be made deliberately SHORTER than a declared raw range (control 4)."""
    nsec = len(sections)
    e_lfanew = 0x80
    coff = e_lfanew + 4
    size_opt = 0xE0
    sec0 = coff + 20 + size_opt
    need = sec0 + 40 * nsec
    for (_n, _va, _vs, rsize, roff) in sections:
        need = max(need, roff + rsize)
    if file_size is None:
        file_size = need
    buf = bytearray(filler for _ in range(file_size))
    buf[0:2] = b"MZ"
    struct.pack_into("<I", buf, 0x3C, e_lfanew)
    buf[e_lfanew:e_lfanew + 4] = b"PE\x00\x00"
    struct.pack_into("<HH", buf, coff, 0x014C, nsec)
    struct.pack_into("<H", buf, coff + 16, size_opt)
    struct.pack_into("<H", buf, coff + 20, 0x010B)  # PE32
    struct.pack_into("<I", buf, coff + 20 + 28, image_base)
    for i, (name, va, vsize, rsize, roff) in enumerate(sections):
        off = sec0 + 40 * i
        buf[off:off + 8] = name.encode()[:8].ljust(8, b"\x00")
        struct.pack_into("<IIII", buf, off + 8, vsize, va, rsize, roff)
    return bytes(buf), image_base


def put(buf, va, image_base, sva, roff, data):
    off = roff + (va - image_base - sva)
    buf[off:off + len(data)] = data


# ---------------------------------------------------------------------------
# 1. Regression — the COMPLETE set of the historical 80 check IDs
# ---------------------------------------------------------------------------
def parse_historical_tables():
    """Read-only AST extraction of the historical checker's pin tables. The
    historical file is NEVER executed (its module top level is inert, but the
    discipline is: read-only, no run)."""
    src = open(HIST_CHECKER, "r", encoding="utf-8").read()
    tree = ast.parse(src)
    tables = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in ("BYTE_PINS", "REL32_PINS",
                                           "RTTI_PINS", "STRING_PINS"):
            tables[node.targets[0].id] = ast.literal_eval(node.value)
    return tables


def regression(physical_data, exe_identity):
    hist_sha = sha256_file(HIST_CHECKER)
    tables = parse_historical_tables()
    byte_pins = tables["BYTE_PINS"]
    rel32_pins = tables["REL32_PINS"]
    rtti_pins = tables["RTTI_PINS"]
    string_pins = tables["STRING_PINS"]
    required_ids = (["EXE_IDENTITY"]
                    + [f"PIN:{t[0]}" for t in byte_pins]
                    + [f"REL32:{t[0]}" for t in rel32_pins]
                    + [f"RTTI:{t[0]}" for t in rtti_pins]
                    + [f"STR:{t[0]}" for t in string_pins])
    required_ids_sorted = sorted(required_ids)
    dup_required = len(required_ids_sorted) != len(set(required_ids_sorted))
    table_identity = {
        "BYTE_PINS": byte_pins == succ.BYTE_PINS,
        "REL32_PINS": rel32_pins == succ.REL32_PINS,
        "RTTI_PINS": rtti_pins == succ.RTTI_PINS,
        "STRING_PINS": string_pins == succ.STRING_PINS,
    }
    results = succ.run_checks()  # clean physical baseline
    ok, fails = succ.gate(results)
    measured = [r[0] for r in results]
    hist_measured = [r for r in results if not r[0].startswith("RECW:")]
    hist_ids = sorted(r[0] for r in hist_measured)
    missing = sorted(set(required_ids_sorted) - set(hist_ids))
    extra = sorted(set(hist_ids) - set(required_ids_sorted))
    duplicates = len(hist_ids) != len(set(hist_ids))
    hist_pass = sum(1 for r in hist_measured if r[1] == "PASS")
    hist_total = len(hist_measured)
    all_hist_pass = all(r[1] == "PASS" for r in hist_measured)
    recw_measured = [r for r in results if r[0].startswith("RECW:")]
    recw_pass = sum(1 for r in recw_measured if r[1] == "PASS")
    verdict_pass = (
        not dup_required and len(required_ids_sorted) == 80
        and len(missing) == 0 and len(extra) == 0 and not duplicates
        and hist_total > 0 and all_hist_pass and hist_total == 80
        and all(table_identity.values()) and ok)
    return {
        "required_id_source": {
            "path": "docs/audits/PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008/03_SCRIPTS/checker_plus4.py",
            "access": "READ-ONLY AST parse (never executed)",
            "sha256_measured": hist_sha,
            "sha256_expected_from_source_manifest": HIST_CHECKER_SHA256,
            "sha256_match": hist_sha == HIST_CHECKER_SHA256,
        },
        "required_check_id_count": len(required_ids_sorted),
        "required_check_ids": required_ids_sorted,
        "duplicate_required_ids": dup_required,
        "successor_table_identity_vs_historical": table_identity,
        "clean_baseline": {
            "suite_total": len(results),
            "historical_ids_measured": hist_total,
            "historical_pass_count": hist_pass,
            "historical_all_pass": all_hist_pass,
            "missing_ids": missing,
            "extra_ids": extra,
            "duplicate_ids": duplicates,
            "empty_suite": hist_total == 0,
            "gate": "PASS" if ok else "FAIL",
            "fail_ids": [f[0] for f in fails],
        },
        "new_record_controls_counted_separately": {
            "denominator": len(recw_measured),
            "pass_count": recw_pass,
            "ids": [r[0] for r in recw_measured],
            "note": ("the RECW:* record gates (ACTIVE_CORRECTED_PINS.json-"
                     "driven) are counted separately from the historical 80"),
        },
        "regression_verdict": "PASS" if verdict_pass else "FAIL",
        "regression_verdict_basis": (
            "complete 80-ID set present (no missing/duplicate/empty), "
            "80/80 historical checks PASS on the clean physical baseline, "
            "successor tables element-identical to the historical tables"),
    }


# ---------------------------------------------------------------------------
# 2. Mapper / record controls (contract par. 4 list 1-7)
# ---------------------------------------------------------------------------
def mapper_controls(physical_data):
    out = {
        "policy": {
            "classification_values": ["RAW_BACKED", "VIRTUAL_BSS", "UNMAPPED",
                                      "REJECTED_INVALID_INPUT"],
            "raw_padding_policy": succ.RAW_PADDING_POLICY,
            "header_va_reads": ("VAs below the first section are UNMAPPED; "
                                "the suite requires no header-VA read"),
            "membership_rule": ("membership may use max(VirtualSize, "
                                 "SizeOfRawData) but that NEVER grants a "
                                 "physical read"),
            "no_fabricated_zeros": True,
            "short_slice_is_not_success": True,
        },
        "controls": [],
    }

    def add(cid, cases):
        out["controls"].append({"control_id": cid, **cases})

    pe_real = succ.RangeSafePE(physical_data)

    # --- control 1: known code pin @0x006E8FA5, len 3 -> RAW_BACKED, 89 46 04
    cls, detail = pe_real.classify(0x006E8FA5, 3)
    got = pe_real.read(0x006E8FA5, 3)
    add("MAP1_raw_backed_code_pin", {
        "input": "read(0x006E8FA5, 3) on the physical EXE",
        "expected": "RAW_BACKED + 89 46 04",
        "observed_classification": cls,
        "observed_bytes": got.hex(" ").upper(),
        "failure_gate": "classification != RAW_BACKED or bytes != 89 46 04",
        "denominator": 1,
        "pass": cls == succ.RAW_BACKED and got.hex(" ").upper() == "89 46 04",
    })

    # --- control 2: the two named BSS VAs -> VIRTUAL_BSS, physical read FAIL
    c2_cases = []
    for va in (0x00BA1100, 0x00BA73BC):
        cls, detail = pe_real.classify(va, 1)
        read_err = None
        try:
            pe_real.read(va, 1)
        except succ.ControlledReadError as e:
            read_err = f"{e.classification}: {e.reason}"
        c2_cases.append({
            "va": f"0x{va:08X}",
            "classification": cls,
            "classify_detail": detail,
            "physical_read": "CONTROLLED_FAIL" if read_err else "UNEXPECTED_SUCCESS",
            "read_error": read_err,
            "physical_bytes_fetched": False,
        })
    add("MAP2_bss_vas_classified_not_fetched", {
        "input": "classify+read(0x00BA1100,1) and (0x00BA73BC,1) from headers "
                 "(contract par. 2 item e); NO physical bytes fetched for them",
        "expected": "VIRTUAL_BSS + controlled read error for both",
        "observed_cases": c2_cases,
        "failure_gate": "classification != VIRTUAL_BSS or read succeeded",
        "denominator": 2,
        "pass": all(c["classification"] == succ.VIRTUAL_BSS
                    and c["physical_read"] == "CONTROLLED_FAIL"
                    for c in c2_cases),
    })

    # --- control 3: synthetic raw->BSS crossing despite plausible further bytes
    sva = 0x1000
    svsize, srsize, sroff = 0x100, 0x80, 0x400
    base = 0x00400000
    # the file extends PAST the section's raw end: the further offsets
    # contain plausible-looking bytes (of the kind another section would
    # occupy) so a boundary-blind mapper would return them as if raw
    img, ib = make_synthetic_pe([(".text", sva, svsize, srsize, sroff)],
                                file_size=sroff + srsize + 0x80)
    buf = bytearray(img)
    # plausible-looking bytes of 'another section' PAST the raw end in the file
    for i in range(0x40):
        buf[sroff + srsize + i] = 0xE8 if (i % 5 == 0) else (0x33 + (i % 8))
    pe_syn = succ.RangeSafePE(bytes(buf))
    first_va = base + sva                      # first raw byte
    last_va = base + sva + srsize - 1          # last raw byte
    c3_cases = []
    cls, _ = pe_syn.classify(first_va, 1)
    b = pe_syn.read(first_va, 1)
    c3_cases.append({"read": f"read({first_va:#010x}, 1) first raw byte",
                     "classification": cls, "returned_n": len(b), "pass": cls == succ.RAW_BACKED})
    cls, _ = pe_syn.classify(last_va, 1)
    b = pe_syn.read(last_va, 1)
    c3_cases.append({"read": f"read({last_va:#010x}, 1) last raw byte",
                     "classification": cls, "returned_n": len(b), "pass": cls == succ.RAW_BACKED})
    err = None
    cls, detail = pe_syn.classify(last_va, 2)
    try:
        pe_syn.read(last_va, 2)
    except succ.ControlledReadError as e:
        err = f"{e.classification}: {e.reason}"
    c3_cases.append({
        "read": f"read({last_va:#010x}, 2) from the LAST raw byte, crossing raw->BSS",
        "classification": cls,
        "physical_read": "CONTROLLED_FAIL" if err else "UNEXPECTED_SUCCESS",
        "read_error": err,
        "plausible_further_file_bytes_present": True,
        "note": ("the byte at the next file offset looks like plausible code "
                 "of another mapping; the mapper still FAILs at the "
                 "raw->BSS boundary of THIS section"),
        "pass": cls == succ.VIRTUAL_BSS and err is not None,
    })
    add("MAP3_synthetic_raw_to_bss_crossing", {
        "input": "synthetic PE (.text vsize 0x100, rsize 0x80) with "
                 "plausible-looking bytes in the file past the raw end",
        "expected": "first/last raw byte reads PASS; the crossing read has a "
                    "controlled FAIL",
        "observed_cases": c3_cases,
        "failure_gate": "any of the three cases deviates",
        "denominator": 3,
        "pass": all(c["pass"] for c in c3_cases),
    })

    # --- control 4: declared raw range past the physical EOF -> no short read
    img4, ib4 = make_synthetic_pe([(".text", 0x1000, 0x100, 0x200, 0x400)],
                                  file_size=0x500)  # raw would need 0x600
    pe_syn4 = succ.RangeSafePE(img4)
    va_in = base + 0x1000 + 0x100  # delta 0x100; delta+0x10 <= rsize 0x200
    cls, detail = pe_syn4.classify(va_in, 0x10)
    err = None
    try:
        pe_syn4.read(va_in, 0x10)
    except succ.ControlledReadError as e:
        err = f"{e.classification}: {e.reason}"
    add("MAP4_synthetic_declared_raw_past_eof", {
        "input": ("synthetic PE declaring rsize 0x200 at roff 0x400 while the "
                  f"physical file ends at 0x500; read({va_in:#010x}, 0x10)"),
        "expected": "controlled FAIL (declared raw past EOF); no silent short read",
        "observed_classification": cls,
        "physical_read": "CONTROLLED_FAIL" if err else "UNEXPECTED_SUCCESS",
        "read_error": err,
        "bytes_returned": 0 if err else "NONEMPTY_UNEXPECTED",
        "failure_gate": "read succeeded or returned partial data",
        "denominator": 1,
        "pass": err is not None and cls == succ.REJECTED_INVALID_INPUT,
    })

    # --- control 5: UNMAPPED / invalid length / underflow / overflow / ambiguous
    c5_cases = []
    cls, _ = pe_syn.classify(base + 0x5000, 4)  # no section contains it
    err = None
    try:
        pe_syn.read(base + 0x5000, 4)
    except succ.ControlledReadError as e:
        err = f"{e.classification}"
    c5_cases.append({"case": "UNMAPPED VA beyond every section",
                     "classification": cls, "read": "CONTROLLED_FAIL" if err else "UNEXPECTED_SUCCESS",
                     "pass": cls == succ.UNMAPPED and err is not None})
    for n, label in ((0, "n=0"), (-3, "negative n")):
        cls, _ = pe_syn.classify(base + 0x1000, n)
        err = None
        try:
            pe_syn.read(base + 0x1000, n)
        except succ.ControlledReadError as e:
            err = e.classification
        c5_cases.append({"case": f"invalid length {label}",
                         "classification": cls, "read": "CONTROLLED_FAIL" if err else "UNEXPECTED_SUCCESS",
                         "pass": cls == succ.REJECTED_INVALID_INPUT and err is not None})
    cls, _ = pe_syn.classify(base - 1, 4)
    err = None
    try:
        pe_syn.read(base - 1, 4)
    except succ.ControlledReadError as e:
        err = e.classification
    c5_cases.append({"case": "VA underflow (va < ImageBase)",
                     "classification": cls, "read": "CONTROLLED_FAIL" if err else "UNEXPECTED_SUCCESS",
                     "pass": cls == succ.REJECTED_INVALID_INPUT and err is not None})
    cls, _ = pe_syn.classify(base + 0x7FFFFFFF, 4)
    err = None
    try:
        pe_syn.read(base + 0x7FFFFFFF, 4)
    except succ.ControlledReadError as e:
        err = e.classification
    c5_cases.append({"case": "VA range overflow beyond the image (controlled rejection)",
                     "classification": cls, "read": "CONTROLLED_FAIL" if err else "UNEXPECTED_SUCCESS",
                     "pass": cls == succ.UNMAPPED and err is not None})
    img5, ib5 = make_synthetic_pe([
        (".secA", 0x1000, 0x100, 0x100, 0x400),
        (".secB", 0x1080, 0x100, 0x100, 0x500),  # overlaps .secA membership
    ])
    pe_amb = succ.RangeSafePE(img5)
    amb_va = base + 0x1090  # inside both memberships
    cls, _ = pe_amb.classify(amb_va, 4)
    err = None
    try:
        pe_amb.read(amb_va, 4)
    except succ.ControlledReadError as e:
        err = e.classification
    c5_cases.append({"case": "ambiguous overlapping section mapping (no arbitrary first-section choice)",
                     "classification": cls, "read": "CONTROLLED_FAIL" if err else "UNEXPECTED_SUCCESS",
                     "pass": cls == succ.REJECTED_INVALID_INPUT and err is not None})
    add("MAP5_synthetic_rejections", {
        "input": "synthetic PE cases: unmapped, n=0, n=-3, VA underflow, "
                 "range overflow beyond the image, ambiguous overlapping sections",
        "expected": "every case is a controlled rejection (no read success)",
        "observed_cases": c5_cases,
        "failure_gate": "any case reads successfully or is unclassified",
        "denominator": len(c5_cases),
        "pass": all(c["pass"] for c in c5_cases),
    })

    # --- control 6: structured COL/name reads cannot bypass the API
    # synthetic .rdata: raw-backed 0x80 bytes, then BSS tail; a synthetic
    # vtable[-1] (raw-backed) points at a COL whose 20-byte read crosses the
    # raw boundary; a TypeDescriptor name read likewise.
    img6, ib6 = make_synthetic_pe([(".rdata", 0x1000, 0x100, 0x80, 0x400)])
    b6 = bytearray(img6)
    vt_va = base + 0x1040            # synthetic vtable base (raw-backed)
    col_va = base + 0x1000 + 0x78    # 20 B read at delta 0x78 crosses 0x80
    td_name_va = base + 0x1000 + 0x7C  # name read crossing too
    put(b6, vt_va - 4, ib6, 0x1000, 0x400, struct.pack("<I", col_va))
    pe6 = succ.RangeSafePE(bytes(b6))
    c6_cases = []
    col_ptr = pe6.u32(vt_va - 4)  # raw-backed: this read itself must PASS
    c6_cases.append({"step": "u32(vtable-4) raw-backed",
                     "observed": f"0x{col_ptr:08X}", "pass": col_ptr == col_va})
    err = None
    try:
        pe6.read(col_ptr, 20)  # the COL 20-byte read (as the RTTI gate does)
    except succ.ControlledReadError as e:
        err = f"{e.classification}: {e.reason}"
    c6_cases.append({"step": "read(COL, 20) crossing raw->BSS",
                     "physical_read": "CONTROLLED_FAIL" if err else "UNEXPECTED_SUCCESS",
                     "read_error": err,
                     "pass": err is not None})
    err = None
    try:
        pe6.read(td_name_va, 5)  # TypeDescriptor-style name read crossing
    except succ.ControlledReadError as e:
        err = f"{e.classification}: {e.reason}"
    c6_cases.append({"step": "read(TD+8 name) crossing raw->BSS",
                     "physical_read": "CONTROLLED_FAIL" if err else "UNEXPECTED_SUCCESS",
                     "read_error": err,
                     "pass": err is not None})
    add("MAP6_structured_col_name_range_crossing", {
        "input": ("synthetic PE with a synthetic vtable[-1] -> COL structure "
                  "whose 20-byte COL read and TypeDescriptor name read CROSS "
                  "the raw->BSS boundary"),
        "expected": ("the structured reads go through the SAME range-safe API "
                     "and are controlled FAILs (no garbage, no short slice)"),
        "observed_cases": c6_cases,
        "failure_gate": "any structured crossing read succeeds",
        "denominator": len(c6_cases),
        "pass": all(c["pass"] for c in c6_cases),
    })

    # --- control 7: MC6 specificity — DIRECT physical file offset 0x7A1100
    mut = bytearray(physical_data)
    before = mut[MC6_PHYS_OFFSET]
    mut[MC6_PHYS_OFFSET] = 0xAA
    results = succ.run_checks(data_override=bytes(mut))
    ok, fails = succ.gate(results)
    n_fail = len(fails)
    add("MAP7_MC6_physical_offset_specificity", {
        "input": ("in-memory TEST-OVERRIDE copy of the physical EXE with the "
                  "byte at the DIRECT PHYSICAL FILE OFFSET "
                  f"0x{MC6_PHYS_OFFSET:X} changed {before:#04X} -> 0xAA"),
        "description": ("a PHYSICAL-OFFSET mutation of a .rsrc raw byte "
                        "(file offsets and VAs are separate units); this is "
                        "NOT a read of VA 0x00BA1100, and the mutated buffer "
                        "is NOT the SHA-identical physical EXE"),
        "expected": "every existing-anchor gate (the historical 80 + the "
                    "RECW record gates) stays PASS",
        "observed_gate": "PASS" if ok else "FAIL",
        "failed_ids": [f[0] for f in fails],
        "failure_gate": "any anchor gate FAILs",
        "denominator": len(results),
        "pass_count": len(results) - n_fail,
        "pass": ok,
    })

    out["controls_all_pass"] = all(c["pass"] for c in out["controls"])
    out["controls_denominator"] = sum(c["denominator"] for c in out["controls"])
    out["controls_pass_count"] = sum(c["denominator"] if c["pass"] else 0
                                    for c in out["controls"])
    return out


# ---------------------------------------------------------------------------
# 3. MC1..MC5 on the successor production gate (in-memory TEST-OVERRIDES)
# ---------------------------------------------------------------------------
def mc_controls(physical_data):
    pe = succ.RangeSafePE(physical_data)
    mcs = []
    specs = [
        ("MC1_plus4_writer_anchor", 0x006E8FA5, "89 46 04", "8B 46 04",
         "PIN:CTOR_R4_STORE_P"),
        ("MC2_ctor_return_this_anchor", 0x006E9014, "8B C6", "8B C7",
         "PIN:CTOR_RETURN_THIS"),
        ("MC3_pump_return_R_anchor", 0x006C9808, "8B C6", "90 90",
         "PIN:PUMP_RETURN_R"),
    ]
    for mc_id, va, old, new, expected_fail in specs:
        off = pe.raw_offset(va, len(bytes.fromhex(old.replace(" ", ""))))
        mut = bytearray(physical_data)
        nb = bytes.fromhex(new.replace(" ", ""))
        mut[off:off + len(nb)] = nb
        results = succ.run_checks(data_override=bytes(mut))
        ok, fails = succ.gate(results)
        fail_ids = [f[0] for f in fails]
        mcs.append({
            "mc_id": mc_id,
            "corruption": f"@VA {va:#010x} (physical offset {off:#x}) "
                          f"{old} -> {new} (in-memory TEST-OVERRIDE copy)",
            "expected_fail_id": expected_fail,
            "observed_gate": "PASS" if ok else "FAIL",
            "observed_fail_ids": fail_ids,
            "fails_exactly_on_proper_anchor": fail_ids == [expected_fail],
            "anchor_detected": expected_fail in fail_ids,
            "note": ("the whole-file SHA gate is NOT the corruption detector; "
                     "the specific anchor check must FAIL"),
        })
    # MC4: rel32 operand byte bit-flip at the ctor call @0x006C97D8
    va = 0x006C97D8
    off = pe.raw_offset(va, 5)
    mut = bytearray(physical_data)
    mut[off + 1] ^= 0x01  # 93 -> 92: target ceases to be 0x006E8F70
    results = succ.run_checks(data_override=bytes(mut))
    ok, fails = succ.gate(results)
    fail_ids = [f[0] for f in fails]
    mcs.append({
        "mc_id": "MC4_ctor_call_rel32_anchor",
        "corruption": f"@VA {va:#010x} (physical offset {off:#x}) rel32 "
                      "operand byte bit-flip (93 -> 92; target ceases to be "
                      "0x006E8F70) — in-memory TEST-OVERRIDE copy",
        "expected_fail_id": "REL32:REL_PUMP_CTOR_R",
        "observed_gate": "PASS" if ok else "FAIL",
        "observed_fail_ids": fail_ids,
        "fails_exactly_on_proper_anchor": fail_ids == ["REL32:REL_PUMP_CTOR_R"],
        "anchor_detected": "REL32:REL_PUMP_CTOR_R" in fail_ids,
        "note": "own rel32 arithmetic detects the wrong target",
    })
    # MC5: TypeDescriptor name byte of the W RTTI chain
    td_name_va = 0x00B8CAC4 + 8
    off = pe.raw_offset(td_name_va, 1)
    mut = bytearray(physical_data)
    assert mut[off] == ord(".")
    mut[off] = ord("X")
    results = succ.run_checks(data_override=bytes(mut))
    ok, fails = succ.gate(results)
    fail_ids = [f[0] for f in fails]
    mcs.append({
        "mc_id": "MC5_w_rtti_chain_anchor",
        "corruption": f"@TypeDescriptor 0x00B8CAC4+8 (VA {td_name_va:#010x}, "
                      f"physical offset {off:#x}) first name byte '.' -> 'X' "
                      "(in-memory TEST-OVERRIDE copy)",
        "expected_fail_id": "RTTI:RTTI_W_ARKMODELRESOURCEINSTANCEREF",
        "observed_gate": "PASS" if ok else "FAIL",
        "observed_fail_ids": fail_ids,
        "fails_exactly_on_proper_anchor":
            fail_ids == ["RTTI:RTTI_W_ARKMODELRESOURCEINSTANCEREF"],
        "anchor_detected": "RTTI:RTTI_W_ARKMODELRESOURCEINSTANCEREF" in fail_ids,
        "note": "the COL 20 B + name reads go through the same range-safe API",
    })
    return mcs


# ---------------------------------------------------------------------------
# 4. REC-W record mutation gates (the JSON drives the record gates)
# ---------------------------------------------------------------------------
def w_record_mutation_gates():
    pins_sha_before = sha256_file(PINS_JSON)
    with open(PINS_JSON, "r", encoding="utf-8") as f:
        doc = json.load(f)
    gates = []

    def run_with(mut_rec, note):
        results = succ.run_checks(pins_override={"active_records": [mut_rec]})
        d = {r[0]: r for r in results}
        ok, fails = succ.gate(results)
        return d, ok, [f[0] for f in fails], note

    # MUT-BYTES: byte-hex-only change to the WRONG E8 35 transcription
    rec = copy.deepcopy(doc["active_records"][0])
    rec["BYTES"] = "E8 35 F0 02 00"
    d, ok, fails, note = run_with(rec,
        "JSON BYTES-only mutation to the erroneous E8 35 F0 02 00; the "
        "physical EXE is untouched; the JSON file is untouched")
    gates.append({
        "gate_id": "W_MUT_BYTES_ONLY",
        "mutation": "BYTES: 'E8 75 F0 02 00' -> 'E8 35 F0 02 00' (byte-hex only)",
        "note": note,
        "corresponding_gate": "RECW:W_RECORD_BYTES",
        "bytes_gate": d.get("RECW:W_RECORD_BYTES", ("RECW:W_RECORD_BYTES", "ABSENT", ""))[1],
        "rel32_gate": d.get("RECW:W_RECORD_REL32", ("", "ABSENT", ""))[1],
        "target_gate": d.get("RECW:W_RECORD_TARGET", ("", "ABSENT", ""))[1],
        "internal_consistency_gate": d.get("RECW:W_RECORD_INTERNAL_CONSISTENCY", ("", "ABSENT", ""))[1],
        "historical_80_all_pass": all(r[1] == "PASS" for r in d.values()
                                      if not r[0].startswith("RECW:")),
        "observed_fail_ids": fails,
        "pass": (d["RECW:W_RECORD_BYTES"][1] == "FAIL"
                 and d["RECW:W_RECORD_REL32"][1] == "PASS"
                 and d["RECW:W_RECORD_TARGET"][1] == "PASS"),
    })

    # MUT-REL32: displacement-only change to the erroneous +0x2F035
    rec = copy.deepcopy(doc["active_records"][0])
    rec["SIGNED_REL32"] = "+0x2F035"
    d, ok, fails, note = run_with(rec,
        "JSON SIGNED_REL32-only mutation to the erroneous +0x2F035; the "
        "physical EXE is untouched; the JSON file is untouched")
    gates.append({
        "gate_id": "W_MUT_REL32_ONLY",
        "mutation": "SIGNED_REL32: '+0x2F075' -> '+0x2F035' (displacement only)",
        "note": note,
        "corresponding_gate": "RECW:W_RECORD_REL32",
        "bytes_gate": d.get("RECW:W_RECORD_BYTES", ("", "ABSENT", ""))[1],
        "rel32_gate": d.get("RECW:W_RECORD_REL32", ("", "ABSENT", ""))[1],
        "target_gate": d.get("RECW:W_RECORD_TARGET", ("", "ABSENT", ""))[1],
        "internal_consistency_gate": d.get("RECW:W_RECORD_INTERNAL_CONSISTENCY", ("", "ABSENT", ""))[1],
        "historical_80_all_pass": all(r[1] == "PASS" for r in d.values()
                                      if not r[0].startswith("RECW:")),
        "observed_fail_ids": fails,
        "pass": (d["RECW:W_RECORD_REL32"][1] == "FAIL"
                 and d["RECW:W_RECORD_BYTES"][1] == "PASS"
                 and d["RECW:W_RECORD_TARGET"][1] == "PASS"),
    })

    # MUT-TARGET: target-only change to a wrong value
    rec = copy.deepcopy(doc["active_records"][0])
    rec["TARGET_VA"] = "0x006FA870"
    d, ok, fails, note = run_with(rec,
        "JSON TARGET_VA-only mutation to the wrong 0x006FA870 (the target the "
        "erroneous E8 35/+0x2F035 reading would produce); the physical EXE "
        "is untouched; the JSON file is untouched")
    gates.append({
        "gate_id": "W_MUT_TARGET_ONLY",
        "mutation": "TARGET_VA: '0x006FA8B0' -> '0x006FA870' (target only)",
        "note": note,
        "corresponding_gate": "RECW:W_RECORD_TARGET",
        "bytes_gate": d.get("RECW:W_RECORD_BYTES", ("", "ABSENT", ""))[1],
        "rel32_gate": d.get("RECW:W_RECORD_REL32", ("", "ABSENT", ""))[1],
        "target_gate": d.get("RECW:W_RECORD_TARGET", ("", "ABSENT", ""))[1],
        "internal_consistency_gate": d.get("RECW:W_RECORD_INTERNAL_CONSISTENCY", ("", "ABSENT", ""))[1],
        "historical_80_all_pass": all(r[1] == "PASS" for r in d.values()
                                      if not r[0].startswith("RECW:")),
        "observed_fail_ids": fails,
        "pass": (d["RECW:W_RECORD_TARGET"][1] == "FAIL"
                 and d["RECW:W_RECORD_BYTES"][1] == "PASS"
                 and d["RECW:W_RECORD_REL32"][1] == "PASS"),
    })

    pins_sha_after = sha256_file(PINS_JSON)
    return {
        "pins_json_sha256_before": pins_sha_before,
        "pins_json_sha256_after": pins_sha_after,
        "pins_json_file_unchanged": pins_sha_before == pins_sha_after,
        "mutation_scope": ("in-memory copies of the parsed JSON document only; "
                           "the JSON FILE and the physical EXE are never modified"),
        "hardcode_note": ("a correct constant hardcoded in the checker while "
                          "ignoring the JSON would NOT flip these gates; the "
                          "mutations prove the JSON actually drives them "
                          "(physical EXE and the historical 80 stay PASS)"),
        "gates": gates,
        "all_gates_pass": all(g["pass"] for g in gates),
    }


# ---------------------------------------------------------------------------
# 5. FD-C2 logical control models (SYNTHETIC_ONLY)
# ---------------------------------------------------------------------------
def logical_controls():
    # Countermodel: synthetic helper [this-4] := Q — a PROOF-SUFFICIENCY
    # demonstration. NOT a new physical PCG writer; NOT a claim that the real
    # FUN_006B2310 does this; NOT confirmation of actual corruption.
    mem = {}
    R, P, Q = 0x1000, 0x2000, 0x3000
    mem[R + 4] = P                        # PW-1 first-init store replayed
    first_writer_store = (mem[R + 4] == P)
    this = R + 8                          # the recorded receiver &R+8
    mem[this - 4] = Q                      # SYNTHETIC helper body [this-4]:=Q
    returned_r = R                         # ctor returns the same base, no adjustment
    T = mem[R + 4]                         # the installer's later field read
    countermodel = {
        "model": "SYNTHETIC_COUNTERMODEL_FIRST_INIT_P__OPAQUE_HELPER__T_EQUALS_Q",
        "r_base": hex(R), "initial_p": hex(P), "q": hex(Q),
        "helper_receiver_this": hex(this),
        "helper_store_expression": "[this-4] := Q (i.e. [R+4] := Q)",
        "premises_kept_true": {
            "first_init_store_R_plus_4_is_P": first_writer_store,
            "ctor_returns_same_base_R_no_adjustment": returned_r == R,
            "installer_reads_the_same_field_R_plus_4": True,
        },
        "installer_read_t": hex(T),
        "t_equals_first_initial_p": T == P,
        "demonstrates": ("first-init + no-adjustment return + same-field read "
                         "are INSUFFICIENT to prove T==P at use; the missing "
                         "condition is write-effects/frame preservation "
                         "through the unopened helper"),
        "actual_helper_mutation_observed": False,
        "actual_helper_body_opened": False,
        "is_physical_pcg_writer": False,
    }
    # Field-preserving model: the helper does not write [R+4]
    mem2 = {}
    mem2[R + 4] = P
    this2 = R + 8
    mem2[this2 + 0x100] = Q               # helper writes SOMEWHERE ELSE only
    returned_r2 = R
    T2 = mem2[R + 4]
    preserving = {
        "model": "SYNTHETIC_FIELD_PRESERVING_MODEL",
        "r_base": hex(R), "initial_p": hex(P), "q": hex(Q),
        "helper_receiver_this": hex(this2),
        "helper_store_expression": "[this+0x100] := Q (NOT [this-4])",
        "premises_kept_true": {
            "first_init_store_R_plus_4_is_P": mem2[R + 4] == P,
            "ctor_returns_same_base_R_no_adjustment": returned_r2 == R,
            "installer_reads_the_same_field_R_plus_4": True,
        },
        "installer_read_t": hex(T2),
        "t_equals_first_initial_p": T2 == P,
        "demonstrates": ("the same premises are equally consistent with T==P; "
                         "the models are symmetric — the evidence does not "
                         "decide between them"),
        "actual_helper_mutation_observed": False,
        "actual_helper_body_opened": False,
        "is_physical_pcg_writer": False,
    }
    return {
        "run_id": "PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008",
        "logical_controls_scope": "SYNTHETIC_ONLY",
        "scope_note": ("both models are LOGICAL controls (proof-sufficiency "
                       "demonstrations on synthetic state); neither is a new "
                       "physical PCG writer, neither confirms actual "
                       "corruption, and NEITHER resolves how the real "
                       "FUN_006B2310 works — its body was NOT opened and no "
                       "claim is made that it overwrites or preserves [R+4]"),
        "real_fun_006b2310_body_opened": False,
        "countermodel_helper_writes_r_plus_4": countermodel,
        "field_preserving_model": preserving,
        "both_models_execute_premises_true": (
            countermodel["premises_kept_true"]
            == preserving["premises_kept_true"] is not None),
        "verdict": ("T_EQUALS_FIRST_INITIAL_P = NOT_ESTABLISHED_WITHIN_BOUND; "
                    "ACTUAL_LATER_OVERWRITE_OBSERVED = NO; the write-effects/"
                    "frame gap through the conditional &R+8 branch stands"),
        "models_agree_on_all_measured_premises": True,
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    exe_identity_before = {
        "size": os.path.getsize(succ.EXE_PATH),
        "sha256": sha256_file(succ.EXE_PATH),
        "pinned_sha256": succ.EXE_SHA256,
        "match": sha256_file(succ.EXE_PATH) == succ.EXE_SHA256,
    }
    if not exe_identity_before["match"]:
        raise SystemExit("BLOCKED: physical EXE identity mismatch")
    physical_data = succ.load_pinned()

    reg = regression(physical_data, exe_identity_before)
    mapper = mapper_controls(physical_data)
    mcs = mc_controls(physical_data)
    exe_identity_after_controls = {
        "sha256": sha256_file(succ.EXE_PATH),
        "unchanged": sha256_file(succ.EXE_PATH) == succ.EXE_SHA256,
    }
    wmut = w_record_mutation_gates()
    logical = logical_controls()

    impl_identity = {
        "successor_script": {
            "path": "docs/audits/PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008/03_SCRIPTS/checker_plus4_successor.py",
            "sha256": sha256_file(os.path.join(HERE, "checker_plus4_successor.py")),
        },
        "controls_script": {
            "path": "docs/audits/PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008/03_SCRIPTS/run_correction_controls.py",
            "sha256": sha256_file(os.path.abspath(__file__)),
        },
        "exe_identity_before_all_controls": exe_identity_before,
        "exe_identity_after_all_controls": exe_identity_after_controls,
        "physical_exe_never_modified": exe_identity_after_controls["unchanged"],
        "mutants_are_in_memory_test_overrides": True,
    }
    mapper["implementation_identity"] = impl_identity
    mapper["mc1_to_mc5"] = mcs
    mapper["mc1_to_mc5_all_pass"] = all(
        m["anchor_detected"] and m["observed_gate"] == "FAIL" for m in mcs)
    mapper["mc1_to_mc5_fail_exactly_on_proper_anchor_all"] = all(
        m["fails_exactly_on_proper_anchor"] for m in mcs)
    mapper["w_record_mutation_gates"] = wmut

    reg["implementation_identity"] = impl_identity
    reg["mc1_to_mc6"] = {
        "mc1_to_mc5": {m["mc_id"]: {
            "gate": m["observed_gate"],
            "expected_fail_id": m["expected_fail_id"],
            "fails_exactly_on_proper_anchor": m["fails_exactly_on_proper_anchor"],
        } for m in mcs},
        "mc6": mapper["controls"][-1],
    }

    wjson(OUT_MAPPER, mapper)
    wjson(OUT_REGRESSION, reg)
    wjson(OUT_LOGICAL, logical)

    print("mapper controls all pass:", mapper["controls_all_pass"])
    print("MC1..MC5 all detected at proper anchors:", mapper["mc1_to_mc5_all_pass"])
    print("W-record mutation gates all pass:", wmut["all_gates_pass"])
    print("regression verdict:", reg["regression_verdict"])
    print("physical EXE unchanged after controls:", impl_identity["physical_exe_never_modified"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
