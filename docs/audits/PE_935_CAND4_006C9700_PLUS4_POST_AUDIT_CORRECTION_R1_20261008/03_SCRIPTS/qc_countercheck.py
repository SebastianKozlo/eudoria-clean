# qc_countercheck.py — fresh-context INTERNAL QC counter-checks of
# PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008.
#
# AUTHOR/PROCESS: pe-master-auditor fresh-context internal QC (internal to
# PE-MASTER; NOT an independent Desktop audit; NOT self-review by the
# executor). QC_RUN_ID =
# PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008_INTERNAL_QC_R1.
#
# INDEPENDENCE ARCHITECTURE (contract par. 7):
#   - The QCPE mapper below is the QC's OWN separate range-check/arithmetic
#     implementation for the required mapper cases. It is NOT a re-export of
#     the production checker's RangeSafePE (different class, different code
#     path, different synthetic-PE builder; only the PE format itself is
#     shared). Every REQUIRED mapper case (contract par. 4 list 1-7) is
#     measured by QCPE independently.
#   - The production gate replay (checker_plus4_successor.py, loaded via
#     importlib) is clearly separated and labeled REPLAY_*: it re-runs the
#     SAME production gate for the mutant set (clean -> PASS; each mutant ->
#     its specific FAIL), proving the production machinery behaves as
#     required. Replay is never presented as independence.
#
# EXE ACCESS POLICY (contract par. 2) honored: full re-hash, PE headers,
# already-recorded pin/COL/TD/name ranges, the 5 W-ctor bytes @0x006CB836,
# BSS classification from headers. NO other regions; in-memory TEST-OVERRIDE
# copies only for the mechanical mutants; the physical file is never
# modified. python -B; no bytecode; no residue.
#
# Output: 00_CONTROL_INTERNAL_QC/QC_COUNTERCHECK_RAW.json (machine-readable
# raw results; the QC verdict lives in the package-root QC_RESULTS.json).
import ast
import copy
import hashlib
import importlib.util
import json
import os
import struct
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
PKG_ROOT = os.path.dirname(HERE)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(PKG_ROOT)))
QC_DIR = os.path.join(PKG_ROOT, "00_CONTROL_INTERNAL_QC")
OUT_RAW = os.path.join(QC_DIR, "QC_COUNTERCHECK_RAW.json")

SRC_PKG = os.path.join(REPO_ROOT, "docs", "audits",
                       "PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008")
HIST_CHECKER = os.path.join(SRC_PKG, "03_SCRIPTS", "checker_plus4.py")
HIST_CHECKER_SHA256 = ("F58D2DB36106006BA2CBF931DC9CFED872E9C5E2"
                       "2C5484E86462568B985AB7E8")
# (pre-execution self-corrections of THIS QC TOOL's own constants,
#  disclosed in-place — NOT defects of the audited package:
#  a) the pinned SHA constant had a transcription typo (63 chars); the true
#     pinned SHA of the historical checker_plus4.py is
#     F58D2DB36106006BA2CBF931DC9CFED872E9C5E22C5484E86462568B985AB7E8
#     (verified against the source-package manifest and INPUT_IDENTITIES);
#  b) the W-record SIGNED_REL32 field comparison was case-sensitive
#     ("+0x2f075" vs "+0x2F075"); now compared numerically.)
SUCC_PATH = os.path.join(HERE, "checker_plus4_successor.py")
PINS_JSON = os.path.join(PKG_ROOT, "ACTIVE_CORRECTED_PINS.json")

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_SIZE = 8015872
EXE_SHA256 = ("E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F75376"
              "5D5280F31")

# ---------------------------------------------------------------------------
# QCPE — the QC's own independent range-safe PE32 mapper (NOT a re-export)
# ---------------------------------------------------------------------------
QC_RAW = "QC_RAW_BACKED"
QC_BSS = "QC_VIRTUAL_BSS"
QC_UNMAPPED = "QC_UNMAPPED"
QC_REJECT = "QC_REJECTED_INVALID_INPUT"


class QCReadError(Exception):
    """Controlled read failure carrying the QC's own classification."""

    def __init__(self, cls, reason):
        self.cls = cls
        self.reason = reason
        super().__init__(f"[{cls}] {reason}")


class QCPE:
    """Independent whole-range PE32 physical-file mapper (QC's own code).

    Classification precedes any read; the WHOLE range is checked; membership
    may consider max(VirtualSize, SizeOfRawData) but NEVER grants a physical
    read; zeros are never fabricated; short slices are never success.
    """

    def __init__(self, data, expect_image_base=0x00400000):
        self.data = data if isinstance(data, (bytes, bytearray)) else None
        if self.data is None or len(data) < 0x40:
            raise QCReadError(QC_REJECT, "image too small")
        if bytes(data[0:2]) != b"MZ":
            raise QCReadError(QC_REJECT, "no MZ")
        self.e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
        if self.e_lfanew + 24 > len(data):
            raise QCReadError(QC_REJECT, "bad e_lfanew")
        if bytes(data[self.e_lfanew:self.e_lfanew + 4]) != b"PE\x00\x00":
            raise QCReadError(QC_REJECT, "no PE signature")
        coff = self.e_lfanew + 4
        machine, nsec = struct.unpack_from("<HH", data, coff)
        if machine != 0x014C:
            raise QCReadError(QC_REJECT, f"machine {machine:#x} != 0x14C")
        size_opt = struct.unpack_from("<H", data, coff + 16)[0]
        magic = struct.unpack_from("<H", data, coff + 20)[0]
        if magic != 0x010B:
            raise QCReadError(QC_REJECT, f"opt magic {magic:#x} != 0x10B")
        self.image_base = struct.unpack_from("<I", data, coff + 20 + 28)[0]
        if self.image_base != expect_image_base:
            raise QCReadError(QC_REJECT,
                              f"ImageBase {self.image_base:#x} != expected "
                              f"{expect_image_base:#x}")
        sec0 = coff + 20 + size_opt
        if sec0 + 40 * nsec > len(data):
            raise QCReadError(QC_REJECT, "incomplete section table")
        self.sections = []
        for i in range(nsec):
            o = sec0 + 40 * i
            nm = bytes(data[o:o + 8]).rstrip(b"\x00").decode("ascii", "replace")
            vsize, sva, rsize, roff = struct.unpack_from("<IIII", data, o + 8)
            self.sections.append((nm, sva, vsize, rsize, roff))

    def _sections_covering(self, rva, n):
        out = []
        for (nm, sva, vsize, rsize, roff) in self.sections:
            end = sva + max(vsize, rsize)
            if sva <= rva and (rva + n) <= end:
                out.append((nm, sva, vsize, rsize, roff))
        return out

    def classify(self, va, n):
        if not isinstance(va, int) or isinstance(va, bool) \
                or not isinstance(n, int) or isinstance(n, bool):
            return (QC_REJECT, "va/n must be integers")
        if va < 0:
            return (QC_REJECT, f"negative VA {va}")
        if n <= 0:
            return (QC_REJECT, f"invalid length n={n}")
        if va < self.image_base:
            return (QC_REJECT, f"VA underflow {va:#x} < ImageBase")
        rva = va - self.image_base
        cov = self._sections_covering(rva, n)
        if not cov:
            return (QC_UNMAPPED,
                    f"RVA {rva:#x}+{n} inside no section")
        if len(cov) > 1:
            return (QC_REJECT, "ambiguous section mapping: "
                    + "/".join(c[0] for c in cov))
        (nm, sva, vsize, rsize, roff) = cov[0]
        delta = rva - sva
        if delta + n <= rsize:
            if roff + delta + n <= len(self.data):
                return (QC_RAW, f"section {nm} delta {delta:#x} raw whole-range")
            return (QC_REJECT,
                    f"declared raw of {nm} past EOF: roff {roff:#x}+delta "
                    f"{delta:#x}+{n} > file {len(self.data):#x}")
        if delta < rsize:
            return (QC_BSS,
                    f"cross raw->BSS in {nm}: delta {delta:#x} < rsize "
                    f"{rsize:#x} but delta+n {delta + n:#x} > rsize")
        return (QC_BSS,
                f"RVA {rva:#x} in {nm} virtual tail: delta {delta:#x} >= "
                f"rsize {rsize:#x}")

    def read(self, va, n):
        cls, detail = self.classify(va, n)
        if cls != QC_RAW:
            raise QCReadError(cls, detail)
        rva = va - self.image_base
        (nm, sva, vsize, rsize, roff) = self._sections_covering(rva, n)[0]
        delta = rva - sva
        out = bytes(self.data[roff + delta:roff + delta + n])
        if len(out) != n:
            raise QCReadError(QC_REJECT, f"short slice {len(out)}/{n}")
        return out

    def file_offset(self, va, n):
        cls, _ = self.classify(va, n)
        if cls != QC_RAW:
            raise QCReadError(cls, "not raw-backed")
        rva = va - self.image_base
        (nm, sva, vsize, rsize, roff) = self._sections_covering(rva, n)[0]
        return roff + (rva - sva)

    def u32(self, va):
        return struct.unpack("<I", self.read(va, 4))[0]


def make_minipe(sections, image_base=0x00400000, file_size=None):
    """QC's OWN synthetic PE builder (independent of production code)."""
    nsec = len(sections)
    lfanew = 0x90
    coff = lfanew + 4
    opt_size = 0xE0
    sec0 = coff + 20 + opt_size
    need = sec0 + 40 * nsec
    for (_n, _va, _vs, rs, ro) in sections:
        need = max(need, ro + rs)
    if file_size is None:
        file_size = need
    b = bytearray(b"\xCC") * file_size
    b[0:2] = b"MZ"
    struct.pack_into("<I", b, 0x3C, lfanew)
    b[lfanew:lfanew + 4] = b"PE\x00\x00"
    struct.pack_into("<HH", b, coff, 0x014C, nsec)
    struct.pack_into("<H", b, coff + 16, opt_size)
    struct.pack_into("<H", b, coff + 20, 0x010B)
    struct.pack_into("<I", b, coff + 20 + 28, image_base)
    for i, (nm, va, vs, rs, ro) in enumerate(sections):
        o = sec0 + 40 * i
        b[o:o + 8] = nm.encode()[:8].ljust(8, b"\x00")
        struct.pack_into("<IIII", b, o + 8, vs, va, rs, ro)
    return bytes(b), image_base


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest().upper()


def sha256_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def parse_hex(s):
    return bytes.fromhex(s.replace(" ", ""))


# ===========================================================================
def main():
    results = {
        "qc_run_id": ("PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_"
                      "R1_20261008_INTERNAL_QC_R1"),
        "author_process": ("pe-master-auditor fresh-context internal QC "
                           "(internal to PE-MASTER; NOT a Desktop audit; "
                           "NOT executor self-review)"),
        "independence_architecture": {
            "own_mapper": "QCPE (this file) — independent implementation; "
                          "NOT a re-export of RangeSafePE",
            "own_synthetic_builder": "make_minipe (this file)",
            "production_replay": "checker_plus4_successor.py via importlib — "
                                  "clearly labeled REPLAY_*, never presented "
                                  "as independence",
        },
    }

    # -- EXE identity (full re-hash; fail-closed) ---------------------------
    with open(EXE_PATH, "rb") as f:
        exe = f.read()
    exe_sha = sha256_bytes(exe)
    results["exe_identity"] = {
        "size": len(exe),
        "sha256": exe_sha,
        "pinned_size": EXE_SIZE,
        "pinned_sha256": EXE_SHA256,
        "match": len(exe) == EXE_SIZE and exe_sha == EXE_SHA256,
    }
    if not results["exe_identity"]["match"]:
        raise SystemExit("BLOCKED: EXE identity mismatch")
    qcpe = QCPE(exe)
    results["pe_header_measured"] = {
        "image_base": f"0x{qcpe.image_base:08X}",
        "e_lfanew": f"0x{qcpe.e_lfanew:X}",
        "sections": [
            {"name": nm, "va": f"0x{sva:08X}", "vsize": f"0x{vsize:X}",
             "rsize": f"0x{rsize:X}", "roff": f"0x{roff:X}"}
            for (nm, sva, vsize, rsize, roff) in qcpe.sections
        ],
    }

    # =======================================================================
    # DUTY 2 — W record recheck (own read + own arithmetic)
    # =======================================================================
    W_VA = 0x006CB836
    off_w = qcpe.file_offset(W_VA, 5)
    w_bytes = qcpe.read(W_VA, 5)
    w_rel = struct.unpack("<i", w_bytes[1:5])[0]
    w_next = W_VA + 5
    w_target = W_VA + 5 + w_rel
    with open(PINS_JSON, "r", encoding="utf-8") as f:
        pins_doc = json.load(f)
    rec = pins_doc["active_records"][0]
    duty2 = {
        "implementation": "QCPE own read + own struct rel32 arithmetic",
        "physical_offset_measured": f"0x{off_w:X}",
        "physical_offset_json": rec["PHYSICAL_OFFSET"],
        "bytes_measured": w_bytes.hex(" ").upper(),
        "bytes_json": rec["BYTES"],
        "signed_rel32_measured": f"{w_rel:+#x}",
        "signed_rel32_json": rec["SIGNED_REL32"],
        "next_va_measured": f"0x{w_next:08X}",
        "next_va_json": rec["NEXT_VA"],
        "target_va_measured": f"0x{w_target:08X}",
        "target_va_json": rec["TARGET_VA"],
        "target_formula_json": rec["TARGET_FORMULA"],
        "callsite_va_json": rec["CALLSITE_VA"],
        "signed_rel32_numeric_match": int(rec["SIGNED_REL32"], 16) == w_rel,
        "fields_all_match": (
            rec["PHYSICAL_OFFSET"] == f"0x{off_w:X}"
            and rec["BYTES"] == w_bytes.hex(" ").upper()
            and int(rec["SIGNED_REL32"], 16) == w_rel
            and rec["NEXT_VA"] == f"0x{w_next:08X}"
            and rec["TARGET_VA"] == f"0x{w_target:08X}"
            and rec["CALLSITE_VA"] == f"0x{W_VA:08X}"
            and rec["TARGET_FORMULA"] == (
                "CALLSITE_VA + 5 + signed_little_endian_int32(BYTES[1:5])")),
        "expected_values_per_contract": {
            "BYTES": "E8 75 F0 02 00", "SIGNED_REL32": "+0x2F075",
            "NEXT_VA": "0x006CB83B", "TARGET_VA": "0x006FA8B0"},
        "contract_values_match": (
            w_bytes.hex(" ").upper() == "E8 75 F0 02 00"
            and f"{w_rel:+#x}" == "+0x2f075"
            and f"0x{w_next:08X}" == "0x006CB83B"
            and f"0x{w_target:08X}" == "0x006FA8B0"),
    }
    results["duty2_w_record_recheck"] = duty2

    # =======================================================================
    # DUTY 3 — OWN mapper controls 1..7 (independent implementation)
    # =======================================================================
    mapper = {"implementation": "QCPE own (independent); NOT production code"}

    # 1: known code pin RAW_BACKED
    b1 = qcpe.read(0x006E8FA5, 3)
    c1, _ = qcpe.classify(0x006E8FA5, 3)
    mapper["map1_raw_backed_pin"] = {
        "expected": "QC_RAW_BACKED + 89 46 04",
        "measured_class": c1, "measured_bytes": b1.hex(" ").upper(),
        "pass": c1 == QC_RAW and b1.hex(" ").upper() == "89 46 04"}

    # 2: the two BSS VAs — classify + controlled read FAIL, no bytes
    m2 = []
    for va in (0x00BA1100, 0x00BA73BC):
        cls, detail = qcpe.classify(va, 1)
        read_failed = None
        try:
            qcpe.read(va, 1)
        except QCReadError as e:
            read_failed = f"{e.cls}: {e.reason}"
        m2.append({
            "va": f"0x{va:08X}", "measured_class": cls, "detail": detail,
            "controlled_read_fail": read_failed is not None,
            "read_error": read_failed,
            "pass": cls == QC_BSS and read_failed is not None,
        })
    mapper["map2_bss_vas"] = {"cases": m2,
                              "pass": all(x["pass"] for x in m2)}

    # 3: synthetic raw->BSS crossing with plausible further bytes
    sva, sv, sr, sro = 0x1000, 0x100, 0x80, 0x400
    base = 0x00400000
    img, ib = make_minipe([(".text", sva, sv, sr, sro)],
                          file_size=sro + sr + 0x80)
    buf = bytearray(img)
    for i in range(0x40):
        buf[sro + sr + i] = 0xE8 if (i % 5 == 0) else (0x33 + (i % 8))
    syn = QCPE(bytes(buf), ib)
    first_va, last_va = base + sva, base + sva + sr - 1
    b_first = syn.read(first_va, 1)
    b_last = syn.read(last_va, 1)
    cross = None
    try:
        syn.read(last_va, 2)
    except QCReadError as e:
        cross = f"{e.cls}: {e.reason}"
    mapper["map3_raw_to_bss_crossing"] = {
        "first_raw_byte_class": syn.classify(first_va, 1)[0],
        "first_raw_byte_ok": b_first == bytes([buf[sro]]),
        "last_raw_byte_class": syn.classify(last_va, 1)[0],
        "last_raw_byte_ok": b_last == bytes([buf[sro + sr - 1]]),
        "crossing_class": syn.classify(last_va, 2)[0],
        "crossing_controlled_fail": cross is not None,
        "crossing_error": cross,
        "plausible_further_bytes_present": True,
        "pass": (syn.classify(first_va, 1)[0] == QC_RAW
                 and syn.classify(last_va, 1)[0] == QC_RAW
                 and syn.classify(last_va, 2)[0] == QC_BSS
                 and cross is not None)}

    # 4: declared raw past EOF (no silent short read)
    img4, ib4 = make_minipe([(".text", 0x1000, 0x100, 0x200, 0x400)],
                            file_size=0x500)
    syn4 = QCPE(img4, ib4)
    va4 = base + 0x1100
    err4 = None
    try:
        syn4.read(va4, 0x10)
    except QCReadError as e:
        err4 = f"{e.cls}: {e.reason}"
    mapper["map4_declared_raw_past_eof"] = {
        "measured_class": syn4.classify(va4, 0x10)[0],
        "controlled_read_fail": err4 is not None,
        "read_error": err4,
        "pass": (syn4.classify(va4, 0x10)[0] == QC_REJECT
                 and err4 is not None)}

    # 5: unmapped / n=0 / negative n / underflow / overflow / ambiguous
    m5 = []
    cls, _ = syn.classify(base + 0x5000, 4)
    rf = _try_read(syn, base + 0x5000, 4)
    m5.append({"case": "unmapped", "class": cls, "fail": rf is not None,
               "pass": cls == QC_UNMAPPED and rf is not None})
    cls, _ = syn.classify(base + 0x1000, 0)
    rf = _try_read(syn, base + 0x1000, 0)
    m5.append({"case": "n=0", "class": cls, "fail": rf is not None,
               "pass": cls == QC_REJECT and rf is not None})
    cls, _ = syn.classify(base + 0x1000, -3)
    rf = _try_read(syn, base + 0x1000, -3)
    m5.append({"case": "negative n", "class": cls, "fail": rf is not None,
               "pass": cls == QC_REJECT and rf is not None})
    cls, _ = syn.classify(base - 1, 4)
    rf = _try_read(syn, base - 1, 4)
    m5.append({"case": "va underflow", "class": cls, "fail": rf is not None,
               "pass": cls == QC_REJECT and rf is not None})
    cls, _ = syn.classify(base + 0x7FFFFFFF, 4)
    rf = _try_read(syn, base + 0x7FFFFFFF, 4)
    m5.append({"case": "range overflow beyond image", "class": cls,
               "fail": rf is not None,
               "pass": cls in (QC_UNMAPPED, QC_REJECT) and rf is not None})
    img5, ib5 = make_minipe([(".aaa", 0x1000, 0x100, 0x100, 0x400),
                             (".bbb", 0x1080, 0x100, 0x100, 0x500)])
    amb = QCPE(img5, ib5)
    cls, _ = amb.classify(base + 0x1090, 4)
    rf = _try_read(amb, base + 0x1090, 4)
    m5.append({"case": "ambiguous overlapping sections", "class": cls,
               "fail": rf is not None,
               "pass": cls == QC_REJECT and rf is not None})
    mapper["map5_rejections"] = {"cases": m5,
                                 "pass": all(x["pass"] for x in m5)}

    # 6: structured COL/name crossing through the SAME API
    img6, ib6 = make_minipe([(".rdata", 0x1000, 0x100, 0x80, 0x400)])
    b6 = bytearray(img6)
    vt_va = base + 0x1040
    col_va = base + 0x1078
    td_name_va = base + 0x107C
    d_off = 0x400 + (vt_va - base - 0x1000) - 4
    struct.pack_into("<I", b6, d_off, col_va)
    syn6 = QCPE(bytes(b6), ib6)
    got_ptr = syn6.u32(vt_va - 4)
    col_err = _try_read(syn6, col_va, 20)
    td_err = _try_read(syn6, td_name_va, 5)
    mapper["map6_structured_col_name_crossing"] = {
        "u32_vtable_minus_4": f"0x{got_ptr:08X}",
        "u32_matches_synth_col": got_ptr == col_va,
        "col20_controlled_fail": col_err is not None,
        "col_error": col_err,
        "td_name_controlled_fail": td_err is not None,
        "td_error": td_err,
        "pass": (got_ptr == col_va and col_err is not None
                 and td_err is not None)}

    # 7: MC6 specificity — DIRECT physical file offset 0x7A1100 (own version)
    # (a .rsrc raw byte; NOT a read of VA 0x00BA1100)
    mc6_off = 0x7A1100
    sec_owner = None
    for (nm, sva, vsize, rsize, roff) in qcpe.sections:
        if roff <= mc6_off < roff + rsize:
            sec_owner = nm
            break
    before_byte = exe[mc6_off]
    mut6 = bytearray(exe)
    mut6[mc6_off] = 0xAA
    qcpe6 = QCPE(bytes(mut6))
    # all pins still read identical through the QC's own mapper
    pins_same = all(qcpe.read(va, len(parse_hex(hx))) ==
                    qcpe6.read(va, len(parse_hex(hx)))
                    for (_id, va, hx) in SUCC_BYTE_PINS_FOR_MAP7)
    rel_same = all(qcpe.read(va, 5) == qcpe6.read(va, 5)
                   for (_id, va, _t) in SUCC_REL32_PINS_FOR_MAP7)
    mapper["map7_mc6_physical_offset_specificity"] = {
        "mutation": f"direct FILE offset 0x{mc6_off:X} byte "
                    f"{before_byte:#04X} -> 0xAA (in-memory copy)",
        "file_offset_owner_section": sec_owner,
        "is_rsrc_raw_byte": sec_owner == ".rsrc",
        "pin_reads_identical_after_mutation": pins_same,
        "rel32_reads_identical_after_mutation": rel_same,
        "pass": sec_owner == ".rsrc" and pins_same and rel_same}
    results["duty3_own_mapper_controls"] = mapper

    # =======================================================================
    # DUTY 4 — production gate REPLAY via importlib (clearly labeled)
    # =======================================================================
    spec = importlib.util.spec_from_file_location(
        "checker_plus4_successor_replay", SUCC_PATH)
    succ = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(succ)
    replay = {
        "implementation": "checker_plus4_successor.py via importlib (REPLAY)",
        "import_inertness": "verified by FULL READ of the file before this "
                            "run (no module-top-level side effects; "
                            "main() under __main__ guard only)",
    }
    res_clean = succ.run_checks()
    ok_clean, fails_clean = succ.gate(res_clean)
    replay["clean"] = {
        "checks_total": len(res_clean),
        "pass_count": sum(1 for r in res_clean if r[1] == "PASS"),
        "gate": "PASS" if ok_clean else "FAIL",
        "fail_ids": [f[0] for f in fails_clean],
    }

    # MC1..MC5 — own offsets via QCPE; own in-memory TEST-OVERRIDE copies
    mc_specs = [
        ("MC1", 0x006E8FA5, "89 46 04", "8B 46 04", "PIN:CTOR_R4_STORE_P"),
        ("MC2", 0x006E9014, "8B C6", "8B C7", "PIN:CTOR_RETURN_THIS"),
        ("MC3", 0x006C9808, "8B C6", "90 90", "PIN:PUMP_RETURN_R"),
    ]
    mcs = []
    for mc_id, va, old, new, exp_fail in mc_specs:
        nb_old = parse_hex(old)
        off = qcpe.file_offset(va, len(nb_old))
        assert bytes(exe[off:off + len(nb_old)]) == nb_old
        mut = bytearray(exe)
        nb_new = parse_hex(new)
        mut[off:off + len(nb_new)] = nb_new
        res = succ.run_checks(data_override=bytes(mut))
        ok, fails = succ.gate(res)
        fail_ids = [f[0] for f in fails]
        mcs.append({
            "mc_id": mc_id, "mutation": f"@{va:#010x} {old} -> {new}",
            "gate": "PASS" if ok else "FAIL",
            "expected_fail_id": exp_fail,
            "observed_fail_ids": fail_ids,
            "fails_exactly_on_proper_anchor": fail_ids == [exp_fail],
            "pass": (not ok) and fail_ids == [exp_fail]})
    # MC4: rel32 bit-flip on the ctor call @0x006C97D8
    va4 = 0x006C97D8
    off4 = qcpe.file_offset(va4, 5)
    assert exe[off4] == 0xE8
    mut = bytearray(exe)
    mut[off4 + 1] ^= 0x01  # 93 -> 92
    res = succ.run_checks(data_override=bytes(mut))
    ok, fails = succ.gate(res)
    fail_ids = [f[0] for f in fails]
    mcs.append({
        "mc_id": "MC4",
        "mutation": f"@{va4:#010x} rel32 operand byte bit-flip (93->92)",
        "gate": "PASS" if ok else "FAIL",
        "expected_fail_id": "REL32:REL_PUMP_CTOR_R",
        "observed_fail_ids": fail_ids,
        "fails_exactly_on_proper_anchor": fail_ids == ["REL32:REL_PUMP_CTOR_R"],
        "pass": (not ok) and fail_ids == ["REL32:REL_PUMP_CTOR_R"]})
    # MC5: W RTTI chain TypeDescriptor first name byte
    td_name_va = 0x00B8CAC4 + 8
    off5 = qcpe.file_offset(td_name_va, 1)
    assert exe[off5] == ord(".")
    mut = bytearray(exe)
    mut[off5] = ord("X")
    res = succ.run_checks(data_override=bytes(mut))
    ok, fails = succ.gate(res)
    fail_ids = [f[0] for f in fails]
    mcs.append({
        "mc_id": "MC5",
        "mutation": f"@TD 0x00B8CAC4+8 first name byte '.' -> 'X'",
        "gate": "PASS" if ok else "FAIL",
        "expected_fail_id": "RTTI:RTTI_W_ARKMODELRESOURCEINSTANCEREF",
        "observed_fail_ids": fail_ids,
        "fails_exactly_on_proper_anchor":
            fail_ids == ["RTTI:RTTI_W_ARKMODELRESOURCEINSTANCEREF"],
        "pass": (not ok)
        and fail_ids == ["RTTI:RTTI_W_ARKMODELRESOURCEINSTANCEREF"]})
    replay["mc1_to_mc5"] = mcs
    replay["mc1_to_mc5_all_pass"] = all(m["pass"] for m in mcs)

    # REC-W record mutation gates (JSON drives the gates) — own mutations
    w_gates = []
    with open(PINS_JSON, "r", encoding="utf-8") as f:
        base_rec = json.load(f)["active_records"][0]
    for gate_id, field, val, exp_gate in (
            ("W_MUT_BYTES_ONLY", "BYTES", "E8 35 F0 02 00",
             "RECW:W_RECORD_BYTES"),
            ("W_MUT_REL32_ONLY", "SIGNED_REL32", "+0x2F035",
             "RECW:W_RECORD_REL32"),
            ("W_MUT_TARGET_ONLY", "TARGET_VA", "0x006FA870",
             "RECW:W_RECORD_TARGET")):
        r2 = copy.deepcopy(base_rec)
        r2[field] = val
        res = succ.run_checks(pins_override={"active_records": [r2]})
        d = {r[0]: r[1] for r in res}
        ok, fails = succ.gate(res)
        fail_ids = [f[0] for f in fails]
        other_two = [k for k in ("RECW:W_RECORD_BYTES", "RECW:W_RECORD_REL32",
                                 "RECW:W_RECORD_TARGET") if k != exp_gate]
        hist_ok = all(v == "PASS" for (k, v) in d.items()
                      if not k.startswith("RECW:"))
        w_gates.append({
            "gate_id": gate_id, "mutated_field": field, "mutated_value": val,
            "expected_gate_fail": exp_gate,
            "expected_gate_measured": d.get(exp_gate),
            "other_two_gates": {k: d.get(k) for k in other_two},
            "internal_consistency_gate": d.get("RECW:W_RECORD_INTERNAL_CONSISTENCY"),
            "historical_80_all_pass": hist_ok,
            "observed_fail_ids": fail_ids,
            "pass": (d.get(exp_gate) == "FAIL"
                     and all(d.get(k) == "PASS" for k in other_two)
                     and hist_ok)})
    replay["w_record_mutation_gates"] = w_gates
    replay["w_record_mutation_gates_all_pass"] = all(g["pass"]
                                                     for g in w_gates)
    # JSON file and EXE unchanged by the replay phase
    replay["pins_json_sha256_after"] = sha256_file(PINS_JSON)
    replay["exe_sha256_after_replay"] = sha256_file(EXE_PATH)
    results["duty4_production_gate_replay"] = replay

    # =======================================================================
    # DUTY 7 — logical models (own implementation; SYNTHETIC_ONLY)
    # =======================================================================
    R, P, Q = 0x1000, 0x2000, 0x3000
    mem = {R + 4: P}
    p1 = mem[R + 4] == P
    this = R + 8
    mem[this - 4] = Q
    T = mem[R + 4]
    cm = {
        "model": "QC_COUNTERMODEL_FIRST_INIT_P_OPAQUE_HELPER_T_Q",
        "premises": {"first_init_store": p1,
                     "ctor_returns_same_base_no_adjustment": True,
                     "installer_reads_same_field": True},
        "t_measured": hex(T), "t_equals_first_initial_p": T == P,
        "demonstrates": ("first-init + no-adjustment return + same-field "
                        "read are INSUFFICIENT for T==P at use"),
    }
    mem2 = {R + 4: P}
    this2 = R + 8
    mem2[this2 + 0x100] = Q
    T2 = mem2[R + 4]
    fp = {
        "model": "QC_FIELD_PRESERVING_MODEL",
        "premises": {"first_init_store": mem2[R + 4] == P,
                     "ctor_returns_same_base_no_adjustment": True,
                     "installer_reads_same_field": True},
        "t_measured": hex(T2), "t_equals_first_initial_p": T2 == P,
        "demonstrates": ("the same premises are equally consistent with "
                        "T==P; symmetric — evidence does not decide"),
    }
    results["duty7_logical_models"] = {
        "scope": "SYNTHETIC_ONLY",
        "countermodel": cm, "field_preserving_model": fp,
        "both_execute_premises_true": (
            all(cm["premises"].values())
            and all(fp["premises"].values())),
        "countermodel_t_equals_p": cm["t_equals_first_initial_p"],
        "field_preserving_t_equals_p": fp["t_equals_first_initial_p"],
        "resolves_real_FUN_006B2310": False,
        "package_reports_say_neither_resolves": True,
        "pass": (cm["t_equals_first_initial_p"] is False
                 and fp["t_equals_first_initial_p"] is True
                 and cm["premises"]["first_init_store"] is True
                 and fp["premises"]["first_init_store"] is True),
    }

    # =======================================================================
    # DUTY 9 — 80-ID regression: own AST extraction + own 80-check run
    # =======================================================================
    hist_sha = sha256_file(HIST_CHECKER)
    with open(HIST_CHECKER, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    tables = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in ("BYTE_PINS", "REL32_PINS",
                                           "RTTI_PINS", "STRING_PINS"):
            tables[node.targets[0].id] = ast.literal_eval(node.value)
    bp, rp, rt, sp = (tables["BYTE_PINS"], tables["REL32_PINS"],
                      tables["RTTI_PINS"], tables["STRING_PINS"])
    required_ids = (["EXE_IDENTITY"]
                    + [f"PIN:{t[0]}" for t in bp]
                    + [f"REL32:{t[0]}" for t in rp]
                    + [f"RTTI:{t[0]}" for t in rt]
                    + [f"STR:{t[0]}" for t in sp])
    dup = len(required_ids) != len(set(required_ids))

    # OWN execution of the 80 checks via QCPE (independent re-execution)
    own = [("EXE_IDENTITY", "PASS")]  # measured above (size+SHA match)
    for pid, va, hx in bp:
        try:
            got = qcpe.read(va, len(parse_hex(hx)))
            own.append((f"PIN:{pid}",
                        "PASS" if got == parse_hex(hx) else "FAIL"))
        except QCReadError as e:
            own.append((f"PIN:{pid}", f"FAIL {e}"))
    for rid, va, tgt in rp:
        try:
            b = qcpe.read(va, 5)
            if b[0] != 0xE8:
                own.append((f"REL32:{rid}", "FAIL opcode"))
                continue
            rel = struct.unpack("<i", b[1:5])[0]
            own.append((f"REL32:{rid}",
                        "PASS" if va + 5 + rel == tgt else "FAIL"))
        except QCReadError as e:
            own.append((f"REL32:{rid}", f"FAIL {e}"))
    for tid, vt, nm in rt:
        try:
            colp = qcpe.u32(vt - 4)
            col = qcpe.read(colp, 20)
            sig, _o, _cd, ptd, _pcd = struct.unpack("<5I", col)
            g = qcpe.read(ptd + 8, len(nm) + 1)
            okk = sig == 0 and g[:-1] == nm and g[-1] == 0
            own.append((f"RTTI:{tid}", "PASS" if okk else "FAIL"))
        except QCReadError as e:
            own.append((f"RTTI:{tid}", f"FAIL {e}"))
    for sid, va, s in sp:
        try:
            g = qcpe.read(va, len(s) + 1)
            own.append((f"STR:{sid}", "PASS" if g[:-1] == s and g[-1] == 0
                        else "FAIL"))
        except QCReadError as e:
            own.append((f"STR:{sid}", f"FAIL {e}"))
    own_pass = sum(1 for (_i, v) in own if v == "PASS")
    own_fail = [(i, v) for (i, v) in own if v != "PASS"]

    # successor table identity (own comparison) vs historical tables
    succ_tables_identity = {
        "BYTE_PINS": [list(t) for t in bp] == [list(t) for t in succ.BYTE_PINS],
        "REL32_PINS": [list(t) for t in rp] == [list(t) for t in succ.REL32_PINS],
        "RTTI_PINS": [list(t) for t in rt] == [list(t) for t in succ.RTTI_PINS],
        "STRING_PINS": [list(t) for t in sp] == [list(t) for t in succ.STRING_PINS],
    }
    # replay clean-baseline historical count (from duty 4 clean run)
    hist_measured = [r[0] for r in res_clean if not r[0].startswith("RECW:")]
    results["duty9_80id_regression"] = {
        "hist_checker_sha256_measured": hist_sha,
        "hist_checker_sha256_expected": HIST_CHECKER_SHA256,
        "hist_checker_sha_match": hist_sha == HIST_CHECKER_SHA256,
        "required_id_count": len(required_ids),
        "required_ids": sorted(required_ids),
        "duplicate_required_ids": dup,
        "own_execution": {
            "implementation": "QCPE own reads + own arithmetic (NOT the "
                              "production checker)",
            "checks": len(own), "pass_count": own_pass,
            "all_pass": len(own_fail) == 0,
            "fail_list": [{"id": i, "detail": v} for (i, v) in own_fail][:20],
        },
        "successor_table_identity_vs_historical": succ_tables_identity,
        "replay_clean_historical_ids": len(hist_measured),
        "replay_clean_historical_all_pass": all(
            r[1] == "PASS" for r in res_clean if not r[0].startswith("RECW:")),
        "new_record_controls_denominator": 6,
        "regression_pass": (
            hist_sha == HIST_CHECKER_SHA256 and not dup
            and len(required_ids) == 80 and len(own_fail) == 0
            and len(own) == 80 and len(hist_measured) == 80
            and all(succ_tables_identity.values())),
    }

    # physical EXE identity after everything (fail-closed re-check)
    results["exe_identity_after_all"] = {
        "sha256": sha256_file(EXE_PATH),
        "unchanged": sha256_file(EXE_PATH) == EXE_SHA256,
    }

    results["overall_pass"] = (
        duty2["fields_all_match"] and duty2["contract_values_match"]
        and mapper["map1_raw_backed_pin"]["pass"]
        and mapper["map2_bss_vas"]["pass"]
        and mapper["map3_raw_to_bss_crossing"]["pass"]
        and mapper["map4_declared_raw_past_eof"]["pass"]
        and mapper["map5_rejections"]["pass"]
        and mapper["map6_structured_col_name_crossing"]["pass"]
        and mapper["map7_mc6_physical_offset_specificity"]["pass"]
        and replay["clean"]["gate"] == "PASS"
        and replay["mc1_to_mc5_all_pass"]
        and replay["w_record_mutation_gates_all_pass"]
        and results["duty7_logical_models"]["pass"]
        and results["duty9_80id_regression"]["regression_pass"]
        and results["exe_identity_after_all"]["unchanged"])

    os.makedirs(QC_DIR, exist_ok=True)
    with open(OUT_RAW, "w", encoding="utf-8", newline="\n") as f:
        json.dump(results, f, indent=2, ensure_ascii=True)
        f.write("\n")
    print("qc_countercheck overall_pass:", results["overall_pass"])
    for k in ("duty2_w_record_recheck",):
        print(k, "fields_all_match =", results[k]["fields_all_match"])
    print("duty3 mapper all pass:",
          all(results["duty3_own_mapper_controls"][k]["pass"]
              for k in results["duty3_own_mapper_controls"]
              if k.startswith("map")))
    print("duty4 replay clean gate:", replay["clean"]["gate"],
          "checks:", replay["clean"]["checks_total"])
    print("duty4 mc1..mc5 all pass:", replay["mc1_to_mc5_all_pass"])
    print("duty4 w-gates all pass:", replay["w_record_mutation_gates_all_pass"])
    print("duty7 pass:", results["duty7_logical_models"]["pass"])
    print("duty9 regression_pass:",
          results["duty9_80id_regression"]["regression_pass"],
          "own 80-check:", own_pass, "/", len(own))
    return 0


def _try_read(pe, va, n):
    try:
        pe.read(va, n)
        return None
    except QCReadError:
        return "CONTROLLED_FAIL"


# Byte/rel32 pin lists for MAP7's own specificity check (mirror of the
# successor tables, used ONLY to enumerate pin ranges for the QC's own
# before/after comparison; the expected values themselves come from the
# historical tables read in duty 9 — here as literal constants for the map).
SUCC_BYTE_PINS_FOR_MAP7 = [
    ("PUMP_SEH_HANDLER", 0x006C9702, "68 13 57 A0 00"),
    ("PUMP_ARG3_LOAD", 0x006C9725, "8B 7C 24 30"),
    ("PUMP_ARG2_LOAD", 0x006C9729, "8B 4C 24 2C"),
    ("PUMP_ARG1_LOAD", 0x006C972D, "8B 44 24 28"),
    ("PUMP_PAIR_TYPE_0x66", 0x006C973A, "C7 44 24 20 66 00 00 00"),
    ("PUMP_PAIR_ID_A", 0x006C9742, "89 44 24 24"),
    ("PUMP_S_NULL_TEST", 0x006C9754, "85 F6"),
    ("PUMP_S_NULL_JE", 0x006C9756, "74 4D"),
    ("PUMP_ARG4_LOAD", 0x006C9758, "8B 44 24 34"),
    ("PUMP_SLOT_LEA", 0x006C975D, "8D 4C 24 2C"),
    ("PUMP_SLOT_CMP", 0x006C9769, "83 7C 24 28 00"),
    ("PUMP_SLOT_JNE", 0x006C9776, "75 41"),
    ("PUMP_RELEASEA_DEC", 0x006C9790, "83 40 04 FF"),
    ("PUMP_RELEASEA_DESTROY", 0x006C979E, "8B 11 8B 42 04 FF D0"),
    ("PUMP_RETURN_NULL", 0x006C97A5, "33 C0"),
    ("PUMP_NEW_SIZE_0x10", 0x006C97B9, "6A 10"),
    ("PUMP_ALLOC_LOCAL_SAVE", 0x006C97C3, "89 44 24 0C"),
    ("PUMP_ALLOC_FAIL_JE", 0x006C97CE, "74 11"),
    ("PUMP_CTOR_PUSH_P", 0x006C97D4, "51"),
    ("PUMP_CTOR_PUSH_S", 0x006C97D5, "56"),
    ("PUMP_CTOR_RECEIVER", 0x006C97D6, "8B C8"),
    ("PUMP_CTOR_RESULT_SAVE", 0x006C97DD, "8B F0"),
    ("PUMP_RELEASEB_DEC", 0x006C97F3, "83 40 04 FF"),
    ("PUMP_RELEASEB_DESTROY", 0x006C9801, "8B 11 8B 42 04 FF D0"),
    ("PUMP_RETURN_R", 0x006C9808, "8B C6"),
    ("PUMP_TERMINAL_RET", 0x006C981B, "C3"),
    ("CTOR_THIS_SAVE", 0x006E8F93, "8B F1"),
    ("CTOR_R0_STORE_S", 0x006E8F9D, "89 06"),
    ("CTOR_R4_STORE_P", 0x006E8FA5, "89 46 04"),
    ("CTOR_P_ADDREF", 0x006E8FAF, "01 48 04"),
    ("CTOR_R8_ZERO", 0x006E8FBD, "C7 07 00 00 00 00"),
    ("CTOR_RC_ZERO", 0x006E8FC9, "C7 46 0C 00 00 00 00"),
    ("CTOR_GATE_CMP_0xB7DC", 0x006E8FD5, "81 78 04 DC B7 00 00"),
    ("CTOR_P_VT_SLOT17", 0x006E8FE3, "8B 42 44"),
    ("CTOR_P_NAME_ARG", 0x006E8FE6, "68 A4 5D A8 00"),
    ("CTOR_RETURN_THIS", 0x006E9014, "8B C6"),
    ("CTOR_TERMINAL_RET8", 0x006E9027, "C2 08 00"),
    ("SETTER_SLOT_CLEAR", 0x006C95A0, "C7 06 00 00 00 00"),
    ("SETTER_RECEIVER_S10", 0x006C95A6, "8B 49 10"),
    ("SETTER_FLAG_CMP", 0x006C95AE, "38 5C 24 28"),
    ("SETTER_FLAG_JNE", 0x006C95BE, "75 71"),
    ("SETTER_SLOT_STORE_P", 0x006C9651, "89 3E"),
    ("SETTER_P_ADDREF", 0x006C9657, "01 5F 04"),
    ("SETTER_TERMINAL_RET8_A", 0x006C962E, "C2 08 00"),
    ("SETTER_TERMINAL_RET8_B", 0x006C966C, "C2 08 00"),
    ("PGET_RECEIVER_SAVE", 0x007B79D4, "8B F9"),
    ("PGET_ALLOC_SIZE_4", 0x007B79D6, "6A 04"),
    ("PRODUCER_STORE_6C", 0x006C7008, "89 46 6C"),
    ("INSTALLER_LOAD_R", 0x006C67B3, "8B 46 6C"),
    ("INSTALLER_READ_R4", 0x006C67BE, "8B 78 04"),
    ("INSTALLER_EBX_1", 0x006C67C9, "BB 01 00 00 00"),
    ("INSTALLER_WRITE_68", 0x006C67E2, "89 7E 68"),
    ("INSTALLER_INCREF_T", 0x006C67E7, "01 5F 04"),
    ("INSTALLER_DECREF_OLD", 0x006C67D4, "01 69 04"),
    ("HIST_CALLER_PUMP_CALL", 0x006CB7CF, "E8 2C DF FF FF"),
    ("HIST_CALLER_NEW_0xC", 0x006CB819, "6A 0C"),
    ("HIST_CALLER_CTOR_CALL", 0x006CB836, "E8 75 F0 02 00"),
]
SUCC_REL32_PINS_FOR_MAP7 = [
    ("REL_PUMP_REQISSUE", 0x006C9746, 0x00415670),
    ("REL_PUMP_SGETTER", 0x006C974D, 0x00823C10),
    ("REL_PUMP_SLOTSETTER", 0x006C9764, 0x006C9570),
    ("REL_PUMP_SMETHOD_8268A0", 0x006C977B, 0x008268A0),
    ("REL_PUMP_ALLOC_NEW", 0x006C97BB, 0x0095D3C4),
    ("REL_PUMP_CTOR_R", 0x006C97D8, 0x006E8F70),
    ("REL_CTOR_GATE", 0x006E8FD0, 0x00728150),
    ("REL_SETTER_VARIANT", 0x006C95C5, 0x007B7660),
    ("REL_SETTER_PGETTER", 0x006C9631, 0x007B79B0),
    ("REL_PGET_ALLOC", 0x007B79D8, 0x0095D3C4),
    ("REL_PGET_INIT", 0x007B79F2, 0x007B7930),
    ("REL_CAND4_CALLER_PUMP", 0x006C6FFC, 0x006C9700),
    ("REL_PRODUCER_INSTALLER", 0x006C7049, 0x006C6780),
    ("REL_HIST_PUMP", 0x006CB7CF, 0x006C9700),
    ("REL_HIST_NEW", 0x006CB81B, 0x0095D3C4),
    ("REL_HIST_WCTOR", 0x006CB836, 0x006FA8B0),
]


if __name__ == "__main__":
    sys.exit(main())
