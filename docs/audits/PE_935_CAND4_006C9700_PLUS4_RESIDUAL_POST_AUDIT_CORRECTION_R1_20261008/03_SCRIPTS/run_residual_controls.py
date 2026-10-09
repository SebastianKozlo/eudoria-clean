"""run_residual_controls.py — residual controls of
PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008.

RUN_CLASS = RECORDS_AND_QC_MACHINERY_CORRECTION (correction-only; EXACTLY the
three Desktop P2 findings + one REC-W P3 of the residual contract).

Phases (contract par. 6 evidence discipline):
  --phase PRE  (run BEFORE checker_plus4_successor_v2.py exists): executes the
      EXACT SOURCE scripts of the READ_ONLY SOURCE_RUN package
      (03_SCRIPTS/checker_plus4_successor.py imported via importlib — its
      module top level was read IN FULL and is inert (definitions only; main()
      under a __main__ guard); 03_SCRIPTS/qc_countercheck.py is NEVER imported
      and NEVER executed at module level — the QCPE class and its helper
      functions are AST-EXTRACTED (only the listed definition nodes are
      compiled and executed in a fresh namespace; main() and every other
      top-level statement are never executed)) on the pinned physical EXE and
      on synthetic fixtures replicating the Desktop ADVERSARIAL_COUNTERCHECKS
      geometry. Every PRE raw output is written run-stamped under 00_PRE/ and
      never overwritten afterwards.
  --phase POST (run AFTER checker_plus4_successor_v2.py exists): re-executes
      every case against the corrected PRODUCTION v2 (and, for continuity, the
      historical v1 QCPE — the fixed independent QC of the QC phase is a
      SEPARATE parent phase and is NOT performed here; the post_qc columns say
      so honestly), plus the MC1..MC6 replay, the W-record mutation gates, the
      80-ID historical regression and the new RECW:W_RECORD_IDENTITY gate.
      Writes 00_POST/ raws plus MAPPER_BOUNDARY_RESULTS.json and
      REGRESSION_RESULTS.json.

Every essential PASS names MEASURED_QUANTITY, INDEPENDENT_SOURCE_OF_TRUTH,
WHY_NON_CIRCULAR and FAILURE_CASE_DETECTED. Expected classifications are
computed by THIS runner's own interval arithmetic (oracle_expectation), which
is a separate implementation of the contract rule — never a replay of the
mapper under test. Replay of production is never presented as independence.

python -B; stdlib only; no bytecode; the physical EXE is NEVER modified
(mechanical-control corruptions are in-memory TEST-OVERRIDE copies supplied by
the caller); the SOURCE_RUN package and its ACTIVE_CORRECTED_PINS.json are
NEVER modified (mutant records live in isolated scratch fixture JSON files
under 00_PRE/scratch/ and 00_POST/scratch/).
"""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import os
import struct
import sys
from datetime import datetime, timezone

sys.dont_write_bytecode = True

RUN_ID = "PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008"
SOURCE_RUN = "PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008"

HERE = os.path.dirname(os.path.abspath(__file__))
PKG_ROOT = os.path.dirname(HERE)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(PKG_ROOT)))
SOURCE_PKG = os.path.join(REPO_ROOT, "docs", "audits", SOURCE_RUN)
SRC_CHECKER = os.path.join(SOURCE_PKG, "03_SCRIPTS", "checker_plus4_successor.py")
SRC_CHECKER_SHA256 = ("F50DDC40F4780FB4431C8B08808F3A5E74DBE"
                      "CD91398A1AC0977556744FBAF45")
SRC_QC = os.path.join(SOURCE_PKG, "03_SCRIPTS", "qc_countercheck.py")
SRC_QC_SHA256 = ("11957F40F7D067E4E422D86E630599142AFBB073F8"
                 "43CEBDB92216E382CB0870")
SRC_PINS = os.path.join(SOURCE_PKG, "ACTIVE_CORRECTED_PINS.json")
SRC_PINS_SHA256 = ("64C64DA9D59CEEC25C72D1890C89E38935BB21530D8"
                   "E3ED8B90537B98705001F")
SRC_PINS_SIZE = 4835
HIST_PKG = os.path.join(REPO_ROOT, "docs", "audits",
                        "PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008")
HIST_CHECKER = os.path.join(HIST_PKG, "03_SCRIPTS", "checker_plus4.py")
HIST_CHECKER_SHA256 = ("F58D2DB36106006BA2CBF931DC9CFED872E9C5E"
                       "22C5484E86462568B985AB7E8")
DESKTOP_JSON = (r"C:\Users\User\Documents\ChatGPT\PE"
                r"\PE_PLUS4_CORRECTION_DESKTOP_POST_AUDIT_0B94C48_20261008"
                r"\ADVERSARIAL_COUNTERCHECKS.json")
DESKTOP_JSON_SHA256 = ("62646637C323E0BAEAD371A0AE979D1F92DD2752B"
                       "60C9D402E70A5A8FA38837B")
DESKTOP_JSON_SIZE = 16079
V2_CHECKER = os.path.join(HERE, "checker_plus4_successor_v2.py")

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_SIZE = 8015872
EXE_SHA256 = ("E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F"
              "753765D5280F31")

W_CANONICAL_VA = 0x006CB836           # the pinned historical W callsite
W_TELEPORT_VA = 0x006C97D8            # REL32:REL_PUMP_CTOR_R callsite (Desktop mutant)
W_GENERALITY_VA = 0x006CB7CF          # REL32:REL_HIST_PUMP callsite (generality mutant)


def sha256_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest().upper()


def wjson(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=2, ensure_ascii=True)
        f.write("\n")


def verify_pin(path, size, sha, label):
    got_size = os.path.getsize(path)
    got_sha = sha256_file(path)
    ok = got_size == size and got_sha == sha
    if not ok:
        raise SystemExit(f"BLOCKED: {label} identity mismatch: "
                         f"size {got_size} (expected {size}), "
                         f"sha {got_sha} (expected {sha})")
    return {"path": path, "size": got_size, "sha256": got_sha, "match": True}


def import_source_checker():
    """Import the EXACT SOURCE production checker via importlib (READ_ONLY).
    Import inertness: the file was read IN FULL before this run — module top
    level contains definitions and constants only; main() is under the
    __main__ guard; no file I/O happens at import."""
    verify_pin(SRC_CHECKER, 30167, SRC_CHECKER_SHA256, "SOURCE checker")
    spec = importlib.util.spec_from_file_location("checker_plus4_successor_src",
                                                  SRC_CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def import_v2_checker():
    if not os.path.isfile(V2_CHECKER):
        raise SystemExit("BLOCKED: POST phase requires "
                         "03_SCRIPTS/checker_plus4_successor_v2.py")
    spec = importlib.util.spec_from_file_location("checker_plus4_successor_v2",
                                                  V2_CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


QC_AST_NAMES_CLASSES = ("QCReadError", "QCPE")
QC_AST_NAMES_FUNCS = ("make_minipe", "sha256_bytes", "sha256_file",
                      "parse_hex", "_try_read")
QC_AST_CONSTS = ("QC_RAW", "QC_BSS", "QC_UNMAPPED", "QC_REJECT")


def ast_extract_qcpe():
    """AST-extract the QC's own QCPE implementation from the SOURCE
    qc_countercheck.py WITHOUT executing the module top level. Only the
    definition nodes listed below are compiled and executed in a fresh
    namespace; main() and every other top-level statement are never executed.
    Returns (namespace, executed_definition_names)."""
    verify_pin(SRC_QC, 40309, SRC_QC_SHA256, "SOURCE qc_countercheck")
    with open(SRC_QC, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    nodes = []
    executed = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name in QC_AST_NAMES_CLASSES:
            nodes.append(node)
            executed.append(node.name)
        elif isinstance(node, ast.FunctionDef) and node.name in QC_AST_NAMES_FUNCS:
            nodes.append(node)
            executed.append(node.name)
        elif isinstance(node, ast.Assign) and all(
                isinstance(t, ast.Name) and t.id in QC_AST_CONSTS
                for t in node.targets):
            nodes.append(node)
            executed.extend(t.id for t in node.targets
                            if isinstance(t, ast.Name))
    ns = {"struct": struct, "hashlib": hashlib}
    for node in nodes:
        mod = ast.Module(body=[node], type_ignores=[])
        code = compile(mod, SRC_QC, "exec")
        exec(code, ns)
    return ns, executed


def load_desktop_json():
    verify_pin(DESKTOP_JSON, DESKTOP_JSON_SIZE, DESKTOP_JSON_SHA256,
               "Desktop ADVERSARIAL_COUNTERCHECKS.json")
    with open(DESKTOP_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Synthetic PE builder (Desktop fixture layout, contract par. 3:
# e_lfanew=0x80, COFF at 0x84, Magic at 0x98, ImageBase at 0xB4)
# ---------------------------------------------------------------------------
def build_synthetic_pe(sections, image_base=0x00400000, file_size=None,
                       filler=0x41, section_fills=None):
    """sections = [(name, rva, vsize, rsize, roff), ...]; section_fills =
    {name: bytes} written at the section's raw offset (before truncation)."""
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
    buf = bytearray([filler]) * file_size
    buf[0:2] = b"MZ"
    struct.pack_into("<I", buf, 0x3C, e_lfanew)
    buf[e_lfanew:e_lfanew + 4] = b"PE\x00\x00"
    struct.pack_into("<HH", buf, coff, 0x014C, nsec)
    struct.pack_into("<H", buf, coff + 16, size_opt)
    struct.pack_into("<H", buf, coff + 20, 0x010B)          # Magic @0x98
    struct.pack_into("<I", buf, coff + 20 + 28, image_base)  # ImageBase @0xB4
    for i, (name, va, vsize, rsize, roff) in enumerate(sections):
        off = sec0 + 40 * i
        buf[off:off + 8] = name.encode()[:8].ljust(8, b"\x00")
        struct.pack_into("<IIII", buf, off + 8, vsize, va, rsize, roff)
        if section_fills and name in section_fills:
            fb = section_fills[name]
            buf[roff:roff + len(fb)] = fb
    return bytes(buf)


def fmt_va(va):
    if isinstance(va, int) and not isinstance(va, bool):
        return f"0x{va:010X}"
    return repr(va)


def serialize_sections(impl_label, pe):
    """v1/v2 RangeSafePE store (name, va, vsize, roff, rsize);
    the historical QCPE stores (name, va, vsize, rsize, roff)."""
    out = []
    for t in pe.sections:
        if impl_label == "qc":
            nm, sva, vsize, rsize, roff = t
        else:
            nm, sva, vsize, roff, rsize = t
        out.append({"name": nm, "rva": f"0x{sva:08X}", "vsize": f"0x{vsize:X}",
                    "raw_offset": f"0x{roff:X}", "raw_size": f"0x{rsize:X}",
                    "member_end": f"0x{sva + max(vsize, rsize):X}"})
    return out


def observe_construct(impl_label, cls, data, expected_image_base=0x00400000):
    try:
        pe = cls(data, expected_image_base)
        return {"outcome": "CONSTRUCTED",
                "image_base": f"0x{pe.image_base:08X}",
                "sections": serialize_sections(impl_label, pe)}
    except Exception as e:  # noqa: BLE001 — raw observation, never a PASS
        return {"outcome": "EXCEPTION", "exception_type": type(e).__name__,
                "exception_message": str(e),
                "controlled": type(e).__name__ in
                ("ControlledReadError", "QCReadError")}


def observe_read(pe, va, n):
    """Raw classify+read observation — no interpretation."""
    obs = {"request": {"va": fmt_va(va), "n": n}}
    try:
        cls, detail = pe.classify(va, n)
        obs["classify"] = {"classification": cls, "detail": detail}
    except Exception as e:  # noqa: BLE001
        obs["classify"] = {"exception_type": type(e).__name__,
                           "exception_message": str(e)}
    try:
        b = pe.read(va, n)
        obs["read"] = {"outcome": "RETURNED", "length": len(b),
                       "bytes_hex": b.hex(" ").upper()}
    except Exception as e:  # noqa: BLE001
        obs["read"] = {"outcome": "EXCEPTION", "exception_type": type(e).__name__,
                       "exception_message": str(e)}
    return obs


def interval_hits(sections, rva0, rva1):
    """Independent ANY-INTERSECTION arithmetic (half-open intervals)."""
    hits = []
    for i, (nm, sva, vsize, rsize, roff) in enumerate(sections):
        mend = sva + max(vsize, rsize)
        if sva < rva1 and rva0 < mend:
            hits.append({"index": i, "name": nm, "start": sva, "member_end": mend})
    return hits


def oracle_expectation(sections, image_base, file_size, va, n):
    """THIS runner's own implementation of the contract rule (independent of
    the mapper under test): half-open [VA, VA+n) validation BEFORE section
    matching; any-intersection section matching; whole-request coverage."""
    if not isinstance(va, int) or isinstance(va, bool) \
            or not isinstance(n, int) or isinstance(n, bool):
        return "REJECTED_INVALID_INPUT", "type validation (va/n not integers)"
    if va < 0:
        return "REJECTED_INVALID_INPUT", "negative VA"
    if n <= 0:
        return "REJECTED_INVALID_INPUT", "n <= 0"
    if va >= 2 ** 32:
        return "REJECTED_INVALID_INPUT", "VA >= 2**32"
    if va + n > 2 ** 32:
        return "REJECTED_INVALID_INPUT", "VA+n > 2**32"
    if va < image_base:
        return "REJECTED_INVALID_INPUT", "VA underflow (< ImageBase)"
    rva0 = va - image_base
    rva1 = rva0 + n
    hits = interval_hits(sections, rva0, rva1)
    if not hits:
        return "UNMAPPED", "intersects no section"
    if len(hits) > 1:
        names = "/".join(h["name"] for h in hits)
        return "REJECTED_INVALID_INPUT", f"{len(hits)} sections intersect ({names})"
    h = hits[0]
    if not (h["start"] <= rva0 and rva1 <= h["member_end"]):
        return ("REJECTED_INVALID_INPUT",
                "partially covered by the single intersecting section")
    (nm, sva, vsize, rsize, roff) = sections[h["index"]]
    delta = rva0 - sva
    if delta + n <= rsize:
        if roff + delta + n <= file_size:
            return "RAW_BACKED", "whole range inside one section's raw range and the file"
        return "REJECTED_INVALID_INPUT", "declared raw runs past physical EOF"
    if delta < rsize:
        return "VIRTUAL_BSS", "crosses raw->BSS boundary"
    return "VIRTUAL_BSS", "inside the virtual tail (past the raw range)"


def oracle_constructor_expectation(file_size, nsec=1):
    """Independent staged-header oracle for the P2-B probes: the first
    physical-availability stage that a file of this size cannot satisfy."""
    e_lfanew = 0x80
    coff = e_lfanew + 4
    stages = [
        ("e_lfanew + PE signature", e_lfanew + 4),
        ("COFF machine/nsections", coff + 4),
        ("COFF SizeOfOptionalHeader", coff + 18),
        ("optional-header Magic @0x98", coff + 22),
        ("optional-header ImageBase @0xB4", coff + 52),
        ("section table (0x178 + 40*nsec)", coff + 20 + 0xE0 + 40 * nsec),
    ]
    for stage, need in stages:
        if file_size < need:
            return {"outcome": "EXCEPTION",
                    "failing_stage": stage,
                    "bytes_needed": need}
    return {"outcome": "CONSTRUCTED",
            "failing_stage": None,
            "note": "all header stages physically available; only raw reads "
                    "remain (a short raw region is rejected per-read)"}


# ---------------------------------------------------------------------------
# Fixture geometry (Desktop ADVERSARIAL_COUNTERCHECKS replicas)
# ---------------------------------------------------------------------------
OVERLAP_SECTIONS = [("A", 0x1000, 0x100, 0x100, 0x400),
                    ("B", 0x1050, 0x20, 0x20, 0x600)]
SEC4GB_C3 = [("A", 0xFFBFFFF0, 0x80, 0x80, 0x400)]
SEC4GB_C4 = [("A", 0xFFC00000, 0x80, 0x80, 0x400)]
TOUCH_SECTIONS = [(".s1", 0x1000, 0x100, 0x100, 0x400),
                 (".s2", 0x1100, 0x100, 0x100, 0x600)]
AMBIG_SECTIONS = [(".secA", 0x1000, 0x100, 0x100, 0x400),
                  (".secB", 0x1080, 0x100, 0x100, 0x500)]
CROSS_SECTIONS = [(".text", 0x1000, 0x100, 0x80, 0x400)]
TRUNC_SECTIONS = [(".text", 0x1000, 0x100, 0x100, 0x400)]


def p2a_cases():
    """(case_id, desktop_name_or_None, fixture_bytes, geometry_desc, sections,
    image_base, file_size, va, n, contract_expected, contract_basis)"""
    f_overlap = build_synthetic_pe(OVERLAP_SECTIONS, file_size=0x900, filler=0x41)
    f_distinct = build_synthetic_pe(OVERLAP_SECTIONS, file_size=0x900,
                                    filler=0x41,
                                    section_fills={"B": bytes([0x42]) * 0x20})
    f_c3 = build_synthetic_pe(SEC4GB_C3, file_size=0x900, filler=0x41)
    f_c4 = build_synthetic_pe(SEC4GB_C4, file_size=0x900, filler=0x41)
    f_touch = build_synthetic_pe(TOUCH_SECTIONS, file_size=0x900, filler=0xCC)
    f_amb = build_synthetic_pe(AMBIG_SECTIONS, file_size=0x900, filler=0xCC)
    f_cross = build_synthetic_pe(CROSS_SECTIONS, file_size=0x500, filler=0xCC,
                                 section_fills={
                                     ".text": bytes(range(0x80))})
    cases = [
        ("P2A-DESKTOP-1",
         "PARTIAL_OVERLAP_SECOND_SECTION_STARTS_INSIDE_READ",
         f_overlap, OVERLAP_SECTIONS, 0x00400000, 0x900,
         0x0040104F, 4, "REJECTED_INVALID_INPUT",
         "two sections intersect the half-open range; VA=0xFFFFFFFF-family not involved"),
        ("P2A-DESKTOP-2",
         "PARTIAL_OVERLAP_SECOND_SECTION_ENDS_INSIDE_READ",
         f_overlap, OVERLAP_SECTIONS, 0x00400000, 0x900,
         0x0040106F, 4, "REJECTED_INVALID_INPUT",
         "two sections intersect (B-intersection is exactly ONE byte 0x106F)"),
        ("P2A-DISTINCT-1", None, f_distinct, OVERLAP_SECTIONS, 0x00400000,
         0x900, 0x0040104F, 4, "REJECTED_INVALID_INPUT",
         "same geometry; section B raw bytes are 0x42 — a false-pass read "
         "would provably return the WRONG section's bytes (A=0x41) for a "
         "range that covers B's region"),
        ("P2A-DISTINCT-2", None, f_distinct, OVERLAP_SECTIONS, 0x00400000,
         0x900, 0x0040106F, 4, "REJECTED_INVALID_INPUT",
         "same geometry; the last byte 0x106F of the request lies in B's "
         "raw region (0x42 content) — a false-pass read returns A's 0x41"),
        ("P2A-DESKTOP-3", "PE32_ABSOLUTE_VA_END_CROSSES_4GB",
         f_c3, SEC4GB_C3, 0x00400000, 0x900,
         0xFFFFFFFE, 4, "REJECTED_INVALID_INPUT",
         "VA+n = 0x100000002 > 2**32 — invalid by address arithmetic "
         "BEFORE section matching"),
        ("P2A-DESKTOP-4", "PE32_ABSOLUTE_VA_START_ABOVE_4GB",
         f_c4, SEC4GB_C4, 0x00400000, 0x900,
         0x100000000, 4, "REJECTED_INVALID_INPUT",
         "VA = 2**32 — outside the PE32 32-bit address space"),
        ("P2A-BOUNDARY-VALID-1", None, f_c3, SEC4GB_C3, 0x00400000, 0x900,
         0xFFFFFFFF, 1, "RAW_BACKED",
         "VA=0xFFFFFFFF,n=1: the exclusive endpoint equals 2**32 — VALID "
         "half-open interval; the fixture section genuinely covers RVA "
         "0xFFBFFFFF (raw-backed); must NOT be rejected"),
        ("P2A-BOUNDARY-VALID-2", None, f_c3, SEC4GB_C3, 0x00400000, 0x900,
         0xFFFFFFFE, 2, "RAW_BACKED",
         "VA=0xFFFFFFFE,n=2: exclusive endpoint exactly 2**32 — VALID; "
         "raw-backed; must NOT be rejected"),
        ("P2A-TOUCH-INSIDE-S1", None, f_touch, TOUCH_SECTIONS, 0x00400000,
         0x900, 0x004010F8, 8, "RAW_BACKED",
         "non-overlapping sections touching at an endpoint: the request "
         "[0x10F8,0x1100) ends exactly at .s2's start — NO intersection with "
         ".s2; single-section read is legitimate"),
        ("P2A-TOUCH-LAST-BYTE-S1", None, f_touch, TOUCH_SECTIONS,
         0x00400000, 0x900, 0x004010FF, 1, "RAW_BACKED",
         "the last byte of .s1; endpoint touching .s2 is not overlap"),
        ("P2A-TOUCH-FIRST-BYTE-S2", None, f_touch, TOUCH_SECTIONS,
         0x00400000, 0x900, 0x00401100, 1, "RAW_BACKED",
         "the first byte of .s2 (start of the second section)"),
        ("P2A-TOUCH-CROSSING", None, f_touch, TOUCH_SECTIONS, 0x00400000,
         0x900, 0x004010FE, 4, "REJECTED_INVALID_INPUT",
         "the request [0x10FE,0x1102) crosses .s1->.s2: BOTH sections "
         "intersect — a cross-section interval never yields bytes"),
        ("P2A-HIST-AMBIGUOUS", None, f_amb, AMBIG_SECTIONS, 0x00400000,
         0x900, 0x00401090, 4, "REJECTED_INVALID_INPUT",
         "historical control: BOTH sections fully contain the read — "
         "full-section-overlap rejection preserved"),
        ("P2A-PARTIAL-START", None, f_overlap, OVERLAP_SECTIONS, 0x00400000,
         0x900, 0x00400FF0, 0x18, "REJECTED_INVALID_INPUT",
         "the request [0x0FF0,0x1008) starts below section A and intersects "
         "it — partially unmapped interval, no bytes"),
        ("P2A-PARTIAL-END", None, f_cross, CROSS_SECTIONS, 0x00400000,
         0x500, 0x004011F8, 0x10, "UNMAPPED",
         "runner case-design correction (disclosed): the request "
         "[0x11F8,0x1208) lies ENTIRELY past the single section's "
         "membership end 0x1100 — no section intersects, so UNMAPPED is "
         "the correct expectation (v1 agreed); the true partial-end "
         "demonstration is the separate case P2A-PARTIAL-END-2; the "
         "immutable PRE raw carries the earlier wrong expected label for "
         "this case_id (the REQUEST never changed)"),
        ("P2A-PARTIAL-END-2", None, f_cross, CROSS_SECTIONS, 0x00400000,
         0x500, 0x004010F8, 0x10, "REJECTED_INVALID_INPUT",
         "the request [0x10F8,0x1108) STARTS inside the section membership "
         "[0x1000,0x1100) and extends past its end — partially unmapped "
         "interval, no bytes (POST-run case added after the runner "
         "case-design correction; disclosed as NOT_IN_PRE)"),
        ("P2A-RELABLED-UNMAPPED", None, f_cross, CROSS_SECTIONS, 0x00400000,
         0x500, 0x803FFFFF, 4, "UNMAPPED",
         "RELABELLED: ImageBase+0x7FFFFFFF is a VALID 32-bit range that "
         "intersects no section — UNMAPPED far beyond the image; it is NOT "
         "a PE32 address-space overflow test (the real boundary tests are "
         "P2A-DESKTOP-3/4 and P2A-BOUNDARY-VALID-1/2)"),
        ("P2A-RAW-CROSSING-FIRST", None, f_cross, CROSS_SECTIONS, 0x00400000,
         0x500, 0x00401000, 1, "RAW_BACKED",
         "first raw byte of a section whose raw range (0x80) is shorter "
         "than its virtual size (0x100)"),
        ("P2A-RAW-CROSSING-LAST", None, f_cross, CROSS_SECTIONS, 0x00400000,
         0x500, 0x0040107F, 1, "RAW_BACKED",
         "last raw byte of the same section"),
        ("P2A-RAW-CROSSING-CROSS", None, f_cross, CROSS_SECTIONS,
         0x00400000, 0x500, 0x0040107F, 2, "VIRTUAL_BSS",
         "read from the LAST raw byte crossing raw->BSS — controlled FAIL, "
         "no fabricated bytes, even though plausible bytes exist further "
         "in the file"),
    ]
    return cases


def p2a_exe_cases(exe_data):
    return [
        ("P2A-REAL-PIN-6E8FA5", None, exe_data, None, 0x00400000,
         len(exe_data), 0x006E8FA5, 3, "RAW_BACKED",
         "contract par. 2 item 4: the ordinary pinned byte-pin read must "
         "return 89 46 04 on the pinned physical EXE"),
        ("P2A-REAL-BSS-BA1100", None, exe_data, None, 0x00400000,
         len(exe_data), 0x00BA1100, 1, "VIRTUAL_BSS",
         "contract par. 2 item 4: the .data zero-init tail VA must classify "
         "VIRTUAL_BSS and never return fabricated file bytes"),
        ("P2A-REAL-BSS-BA73BC", None, exe_data, None, 0x00400000,
         len(exe_data), 0x00BA73BC, 1, "VIRTUAL_BSS",
         "same for the second named BSS VA"),
    ]


def p2a_input_type_cases():
    return [
        ("P2A-INPUT-BOOL-VA", True, 1),
        ("P2A-INPUT-BOOL-N", 0x00401000, True),
        ("P2A-INPUT-STR-VA", "0x00401000", 4),
        ("P2A-INPUT-FLOAT-N", 0x00401000, 4.0),
        ("P2A-INPUT-N-ZERO", 0x00401000, 0),
        ("P2A-INPUT-N-NEGATIVE", 0x00401000, -3),
        ("P2A-INPUT-VA-NEGATIVE", -1, 4),
        ("P2A-INPUT-VA-UNDERFLOW", 0x003FFFFF, 4),
    ]


# ---------------------------------------------------------------------------
# P2-B header truncation fixtures (contract par. 3 layout)
# ---------------------------------------------------------------------------
def p2b_fixtures():
    full = build_synthetic_pe(TRUNC_SECTIONS, file_size=0x500, filler=0xCC)
    truncs = {}
    for size in (0x98, 0x99, 0x9A, 0xB4, 0xB7, 0xB8, 0x190, 0x1C0):
        truncs[size] = full[:size]
    return full, truncs


def header_field_expectations():
    return {
        "e_lfanew": "0x80",
        "pe_signature": "PE\\x00\\x00",
        "machine": "0x14C",
        "number_of_sections": 1,
        "size_of_optional_header": "0xE0",
        "optional_header_magic": "0x10B (PE32)",
        "image_base": "0x00400000",
        "coff_file_offset": "0x84",
        "magic_file_offset": "0x98",
        "image_base_file_offset": "0xB4",
        "section_table_file_offset": "0x178",
        "sections": [{"name": ".text", "rva": "0x00001000",
                      "vsize": "0x100", "raw_offset": "0x400",
                      "raw_size": "0x100", "member_end": "0x1100"}],
        "note": ("runner self-correction disclosed: an earlier version of "
                 "this helper stated section_table_file_offset 0x1A0 — the "
                 "correct value is 0x178 (= 0x84 + 20 + 0xE0); the wrong "
                 "value was copied into the immutable PRE raw as a "
                 "descriptive-only defect (no gate consumed it); corrected "
                 "before the POST phase"),
    }


# ---------------------------------------------------------------------------
# P3 — wrong-callsite mutant scratch fixtures
# ---------------------------------------------------------------------------
def build_mutant_pins_doc(base_doc, record_overrides, note):
    doc = copy.deepcopy(base_doc)
    rec = copy.deepcopy(doc["active_records"][0])
    rec.update(record_overrides)
    rec["MEASUREMENT_BASIS"] = (
        "SCRATCH MUTANT FIXTURE of the residual correction run "
        f"({RUN_ID}) — {note}; NOT a physical measurement record; the SOURCE "
        "ACTIVE_CORRECTED_PINS.json is untouched")
    doc["active_records"][0] = rec
    doc["residual_run_mutation_note"] = note
    return doc


def write_scratch_fixture(path, doc):
    wjson(path, doc)
    return {"path": os.path.relpath(path, REPO_ROOT).replace("\\", "/"),
            "size": os.path.getsize(path), "sha256": sha256_file(path)}


def make_mutant_fixtures(stamp, scratch_dir, src_checker_mod):
    with open(SRC_PINS, "r", encoding="utf-8") as f:
        base_doc = json.load(f)
    verify_pin(SRC_PINS, SRC_PINS_SIZE, SRC_PINS_SHA256, "SOURCE pins JSON")
    pe = src_checker_mod.RangeSafePE(src_checker_mod.load_pinned())
    off_teleport = pe.raw_offset(W_TELEPORT_VA, 5)
    off_generality = pe.raw_offset(W_GENERALITY_VA, 5)
    rec = base_doc["active_records"][0]
    fixtures = {}
    # W1: the Desktop wrong-callsite mutant (RECORD_ID kept, callsite replaced)
    w1 = build_mutant_pins_doc(
        base_doc,
        {"CALLSITE_VA": "0x006C97D8", "BYTES": "E8 93 F7 01 00",
         "SIGNED_REL32": "+0x1F793", "NEXT_VA": "0x006C97DD",
         "TARGET_VA": "0x006E8F70",
         "PHYSICAL_OFFSET": f"0x{off_teleport:X}"},
        "W1 wrong-callsite teleport to the independently pinned REL_PUMP_"
        "CTOR_R callsite 0x006C97D8 (Desktop ADVERSARIAL_COUNTERCHECKS "
        "W_RECORD_TELEPORTED_TO_OTHER_ALREADY_PINNED_CALLSITE)")
    fixtures["W1"] = (w1, write_scratch_fixture(
        os.path.join(scratch_dir, f"W1_wrong_callsite_{stamp}.json"), w1))
    # W2: RECORD_ID-only wrong identity (callsite kept canonical)
    w2 = build_mutant_pins_doc(
        base_doc, {"RECORD_ID": "W_CTOR_CALL_AT_006C97D8"},
        "W2 RECORD_ID-only wrong identity: RECORD_ID changed, CALLSITE_VA "
        "kept at the canonical 0x006CB836 with the original correct values")
    fixtures["W2"] = (w2, write_scratch_fixture(
        os.path.join(scratch_dir, f"W2_wrong_record_id_{stamp}.json"), w2))
    # W3: generality teleport to a different pinned historical callsite
    w3 = build_mutant_pins_doc(
        base_doc,
        {"CALLSITE_VA": "0x006CB7CF", "BYTES": "E8 2C DF FF FF",
         "SIGNED_REL32": "-0x20D4", "NEXT_VA": "0x006CB7D4",
         "TARGET_VA": "0x006C9700",
         "PHYSICAL_OFFSET": f"0x{off_generality:X}"},
        "W3 generality mutant: teleport to the independently pinned "
        "REL_HIST_PUMP callsite 0x006CB7CF (E8 2C DF FF FF, -0x20D4 -> "
        "0x006C9700)")
    fixtures["W3"] = (w3, write_scratch_fixture(
        os.path.join(scratch_dir, f"W3_generality_callsite_{stamp}.json"), w3))
    # W4: clean copy (byte-identical content to the source record)
    clean_doc = copy.deepcopy(base_doc)
    fixtures["CLEAN"] = (clean_doc, write_scratch_fixture(
        os.path.join(scratch_dir, f"CLEAN_copy_{stamp}.json"), clean_doc))
    return fixtures, rec


def replay_record_through_gate(checker_mod, fixture_path, label):
    """Replay a scratch fixture record through the checker's NORMAL
    ACTIVE_CORRECTED_PINS.json loader path (physical file -> json parse ->
    schema validation) and the SAME overall production gate — NOT an
    alternate predicate and NOT a prevalidated-dict bypass (the record passed
    onward is the loader's own output)."""
    loaded = checker_mod.load_active_corrected_pins(fixture_path)
    results = checker_mod.run_checks(pins_override=loaded)
    ok, fails = checker_mod.gate(results)
    d = {r[0]: r[1] for r in results}
    return {
        "replay_label": label,
        "loader_path": ("load_active_corrected_pins(<scratch fixture path>) — "
                        "physical-file parse + schema validation executed; "
                        "then run_checks() + gate() (the SAME overall "
                        "production gate)"),
        "fixture_path": os.path.relpath(fixture_path, REPO_ROOT).replace("\\", "/"),
        "checks_total": len(results),
        "pass_count": sum(1 for r in results if r[1] == "PASS"),
        "gate": "PASS" if ok else "FAIL",
        "fail_ids": [f[0] for f in fails],
        "recw_verdicts": {k: v for k, v in d.items() if k.startswith("RECW:")},
        "historical_80_all_pass": all(v == "PASS" for (k, v) in d.items()
                                      if not k.startswith("RECW:")),
        "results_raw": [list(r) for r in results],
    }


def fixed_address_qc_comparison(qcpe_cls, fixture_doc):
    """The historical QC's duty-2 style FIXED-ADDRESS comparison (the QC reads
    the CANONICAL W callsite 0x006CB836 and compares the record's declared
    callsite/bytes/rel32/next/target against it). This is the separate
    fixed-address QC oracle that catches the wrong-callsite teleport."""
    rec = fixture_doc["active_records"][0]
    w_bytes = qcpe_cls_read(qcpe_cls, W_CANONICAL_VA, 5)
    w_rel = struct.unpack("<i", w_bytes[1:5])[0]
    declared_callsite = int(rec["CALLSITE_VA"], 16)
    return {
        "implementation": "historical QC duty-2 style fixed-address comparison "
                          "(QCPE own read at the CANONICAL 0x006CB836)",
        "canonical_bytes_measured": w_bytes.hex(" ").upper(),
        "canonical_rel32_recomputed": f"{w_rel:+#x}",
        "canonical_next_va": f"0x{W_CANONICAL_VA + 5:08X}",
        "canonical_target_recomputed": f"0x{W_CANONICAL_VA + 5 + w_rel:08X}",
        "declared_callsite_va": rec["CALLSITE_VA"],
        "callsite_mismatch_detected": declared_callsite != W_CANONICAL_VA,
        "declared_bytes": rec["BYTES"],
        "bytes_mismatch_detected": (rec["BYTES"].upper()
                                   != w_bytes.hex(" ").upper()),
        "verdict": ("MISMATCH_DETECTED" if declared_callsite != W_CANONICAL_VA
                    or rec["BYTES"].upper() != w_bytes.hex(" ").upper()
                    else "MATCH_NO_MISMATCH"),
    }


def qcpe_cls_read(qcpe_cls, va, n):
    """QCPE read of the pinned EXE (headers + the 5 canonical W bytes — the
    contract-allowed read classes)."""
    if not hasattr(qcpe_cls_read, "_pe"):
        with open(EXE_PATH, "rb") as f:
            data = f.read()
        qcpe_cls_read._pe = qcpe_cls(data)
    return qcpe_cls_read._pe.read(va, n)


# ---------------------------------------------------------------------------
# Historical-table AST extraction (80-ID regression)
# ---------------------------------------------------------------------------
def ast_pin_tables(path, expected_sha, names=("BYTE_PINS", "REL32_PINS",
                                              "RTTI_PINS", "STRING_PINS")):
    verify_pin(path, os.path.getsize(path), expected_sha, f"AST tables {path}")
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    tables = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in names:
            tables[node.targets[0].id] = ast.literal_eval(node.value)
    return tables


def required_80_ids(tables):
    ids = (["EXE_IDENTITY"]
           + [f"PIN:{t[0]}" for t in tables["BYTE_PINS"]]
           + [f"REL32:{t[0]}" for t in tables["REL32_PINS"]]
           + [f"RTTI:{t[0]}" for t in tables["RTTI_PINS"]]
           + [f"STR:{t[0]}" for t in tables["STRING_PINS"]])
    return ids


# ---------------------------------------------------------------------------
# MC controls (in-memory TEST-OVERRIDE copies only)
# ---------------------------------------------------------------------------
def mc_specs():
    return [
        ("MC1_plus4_writer_anchor", 0x006E8FA5, "89 46 04", "8B 46 04",
         "PIN:CTOR_R4_STORE_P"),
        ("MC2_ctor_return_this_anchor", 0x006E9014, "8B C6", "8B C7",
         "PIN:CTOR_RETURN_THIS"),
        ("MC3_pump_return_R_anchor", 0x006C9808, "8B C6", "90 90",
         "PIN:PUMP_RETURN_R"),
    ]


def run_mc_controls(checker_mod, exe_data):
    pe = checker_mod.RangeSafePE(exe_data)
    mcs = []
    for mc_id, va, old, new, exp_fail in mc_specs():
        off = pe.raw_offset(va, len(bytes.fromhex(old.replace(" ", ""))))
        mut = bytearray(exe_data)
        nb = bytes.fromhex(new.replace(" ", ""))
        mut[off:off + len(nb)] = nb
        results = checker_mod.run_checks(data_override=bytes(mut))
        ok, fails = checker_mod.gate(results)
        fail_ids = [f[0] for f in fails]
        mcs.append({"mc_id": mc_id,
                    "corruption": f"@VA {va:#010x} (physical offset {off:#x}) "
                                  f"{old} -> {new} (in-memory TEST-OVERRIDE copy)",
                    "expected_fail_id": exp_fail,
                    "observed_gate": "PASS" if ok else "FAIL",
                    "observed_fail_ids": fail_ids,
                    "fails_exactly_on_proper_anchor": fail_ids == [exp_fail]})
    # MC4: rel32 operand bit-flip at the ctor call @0x006C97D8
    va = 0x006C97D8
    off = pe.raw_offset(va, 5)
    mut = bytearray(exe_data)
    mut[off + 1] ^= 0x01
    results = checker_mod.run_checks(data_override=bytes(mut))
    ok, fails = checker_mod.gate(results)
    fail_ids = [f[0] for f in fails]
    mcs.append({"mc_id": "MC4_ctor_call_rel32_anchor",
                "corruption": f"@VA {va:#010x} (physical offset {off:#x}) rel32 "
                              "operand byte bit-flip (93 -> 92) — in-memory "
                              "TEST-OVERRIDE copy",
                "expected_fail_id": "REL32:REL_PUMP_CTOR_R",
                "observed_gate": "PASS" if ok else "FAIL",
                "observed_fail_ids": fail_ids,
                "fails_exactly_on_proper_anchor":
                    fail_ids == ["REL32:REL_PUMP_CTOR_R"]})
    # MC5: W RTTI chain TypeDescriptor first name byte
    td_name_va = 0x00B8CAC4 + 8
    off = pe.raw_offset(td_name_va, 1)
    mut = bytearray(exe_data)
    mut[off] = ord("X")
    results = checker_mod.run_checks(data_override=bytes(mut))
    ok, fails = checker_mod.gate(results)
    fail_ids = [f[0] for f in fails]
    mcs.append({"mc_id": "MC5_w_rtti_chain_anchor",
                "corruption": f"@TypeDescriptor 0x00B8CAC4+8 (VA {td_name_va:#010x}, "
                              f"physical offset {off:#x}) first name byte "
                              "'.X' mutation — in-memory TEST-OVERRIDE copy",
                "expected_fail_id": "RTTI:RTTI_W_ARKMODELRESOURCEINSTANCEREF",
                "observed_gate": "PASS" if ok else "FAIL",
                "observed_fail_ids": fail_ids,
                "fails_exactly_on_proper_anchor":
                    fail_ids == ["RTTI:RTTI_W_ARKMODELRESOURCEINSTANCEREF"]})
    # MC6: DIRECT physical file offset 0x7A1100 mutation (.rsrc raw byte — a
    # physical-offset unit, NOT a read of VA 0x00BA1100)
    off6 = 0x7A1100
    before = exe_data[off6]
    mut = bytearray(exe_data)
    mut[off6] = 0xAA
    results = checker_mod.run_checks(data_override=bytes(mut))
    ok, fails = checker_mod.gate(results)
    mcs.append({"mc_id": "MC6_physical_offset_specificity",
                "corruption": f"DIRECT physical FILE offset 0x{off6:X} byte "
                              f"{before:#04X} -> 0xAA (in-memory TEST-OVERRIDE "
                              "copy; a .rsrc raw byte; NOT a read of VA "
                              "0x00BA1100; VA and file offset are separate units)",
                "expected": "every anchor gate stays PASS",
                "observed_gate": "PASS" if ok else "FAIL",
                "checks_total": len(results),
                "pass_count": sum(1 for r in results if r[1] == "PASS"),
                "failed_ids": [f[0] for f in fails]})
    return mcs


def run_w_record_mutation_gates(checker_mod):
    """The historical in-memory JSON-document mutation gates (raw-doc
    pins_override form preserved from the SOURCE_RUN)."""
    with open(SRC_PINS, "r", encoding="utf-8") as f:
        base_rec = json.load(f)["active_records"][0]
    gates = []
    for gate_id, field, val, exp_gate in (
            ("W_MUT_BYTES_ONLY", "BYTES", "E8 35 F0 02 00",
             "RECW:W_RECORD_BYTES"),
            ("W_MUT_REL32_ONLY", "SIGNED_REL32", "+0x2F035",
             "RECW:W_RECORD_REL32"),
            ("W_MUT_TARGET_ONLY", "TARGET_VA", "0x006FA870",
             "RECW:W_RECORD_TARGET")):
        r2 = copy.deepcopy(base_rec)
        r2[field] = val
        res = checker_mod.run_checks(pins_override={"active_records": [r2]})
        d = {r[0]: r[1] for r in res}
        ok, fails = checker_mod.gate(res)
        other_two = [k for k in ("RECW:W_RECORD_BYTES", "RECW:W_RECORD_REL32",
                                 "RECW:W_RECORD_TARGET") if k != exp_gate]
        gates.append({
            "gate_id": gate_id, "mutated_field": field, "mutated_value": val,
            "expected_gate_fail": exp_gate,
            "expected_gate_measured": d.get(exp_gate),
            "other_two_gates": {k: d.get(k) for k in other_two},
            "identity_gate": d.get("RECW:W_RECORD_IDENTITY"),
            "internal_consistency_gate": d.get("RECW:W_RECORD_INTERNAL_CONSISTENCY"),
            "historical_80_all_pass": all(v == "PASS" for (k, v) in d.items()
                                          if not k.startswith("RECW:")),
            "observed_fail_ids": [f[0] for f in fails],
            "pass": (d.get(exp_gate) == "FAIL"
                     and all(d.get(k) == "PASS" for k in other_two))})
    return gates


# ---------------------------------------------------------------------------
# Structured-col/names crossing control (historical MAP6 semantics)
# ---------------------------------------------------------------------------
def structured_crossing_control(v1_mod_or_v2, pe_cls, image_base=0x00400000):
    img = build_synthetic_pe([(".rdata", 0x1000, 0x100, 0x80, 0x400)],
                             file_size=0x500, filler=0xCC)
    buf = bytearray(img)
    vt_va = image_base + 0x1040
    col_va = image_base + 0x1000 + 0x78
    td_name_va = image_base + 0x1000 + 0x7C
    off = 0x400 + (vt_va - image_base - 0x1000) - 4
    struct.pack_into("<I", buf, off, col_va)
    pe = pe_cls(bytes(buf), image_base)
    out = {"u32_vtable_minus_4": None, "col20_read": None,
           "td_name_read": None}
    try:
        ptr = pe.u32(vt_va - 4)
        out["u32_vtable_minus_4"] = {"outcome": "RETURNED",
                                     "value": f"0x{ptr:08X}",
                                     "pass": ptr == col_va}
    except Exception as e:  # noqa: BLE001
        out["u32_vtable_minus_4"] = {"outcome": "EXCEPTION",
                                     "exception_type": type(e).__name__,
                                     "exception_message": str(e)}
    for key, va, n in (("col20_read", col_va, 20),
                       ("td_name_read", td_name_va, 5)):
        try:
            pe.read(va, n)
            out[key] = {"outcome": "RETURNED",
                        "note": "UNEXPECTED SUCCESS — boundary bypass"}
        except Exception as e:  # noqa: BLE001
            out[key] = {"outcome": "EXCEPTION",
                        "exception_type": type(e).__name__,
                        "exception_message": str(e)}
    return out


# ---------------------------------------------------------------------------
# PRE phase
# ---------------------------------------------------------------------------
def run_pre(stamp):
    pre_dir = os.path.join(PKG_ROOT, "00_PRE")
    scratch_dir = os.path.join(pre_dir, "scratch")

    identities = {
        "phase": "PRE",
        "run_id": RUN_ID,
        "stamp": stamp,
        "exe": verify_pin(EXE_PATH, EXE_SIZE, EXE_SHA256, "physical EXE"),
        "source_checker": {"path": os.path.relpath(SRC_CHECKER, REPO_ROOT).replace("\\", "/"),
                           "size": os.path.getsize(SRC_CHECKER),
                           "sha256": sha256_file(SRC_CHECKER)},
        "source_qc": {"path": os.path.relpath(SRC_QC, REPO_ROOT).replace("\\", "/"),
                      "size": os.path.getsize(SRC_QC),
                      "sha256": sha256_file(SRC_QC),
                      "access": "AST-EXTRACTION ONLY — the module is never "
                                "imported/executed at top level"},
        "source_pins_json": verify_pin(SRC_PINS, SRC_PINS_SIZE, SRC_PINS_SHA256,
                                        "SOURCE ACTIVE_CORRECTED_PINS.json"),
        "desktop_adversarial_counterchecks": verify_pin(
            DESKTOP_JSON, DESKTOP_JSON_SIZE, DESKTOP_JSON_SHA256,
            "Desktop ADVERSARIAL_COUNTERCHECKS.json"),
    }
    desktop = load_desktop_json()
    v1 = import_source_checker()
    qc_ns, qc_executed = ast_extract_qcpe()
    QCPE = qc_ns["QCPE"]

    with open(EXE_PATH, "rb") as f:
        exe_data = f.read()

    # ---- PRE baseline: the source checker clean run ----------------------
    baseline = {
        "description": "EXACT SOURCE checker clean run on the pinned physical "
                       "EXE (no overrides) — the PRE baseline state",
        "exe_identity": {"size": len(exe_data), "sha256": sha256_bytes(exe_data)},
        "results": None,
    }
    results = v1.run_checks()
    ok, fails = v1.gate(results)
    baseline["checks_total"] = len(results)
    baseline["pass_count"] = sum(1 for r in results if r[1] == "PASS")
    baseline["gate"] = "PASS" if ok else "FAIL"
    baseline["fail_ids"] = [f[0] for f in fails]
    baseline["results_raw"] = [list(r) for r in results]
    wjson(os.path.join(pre_dir, f"PRE_{stamp}_BASELINE_CLEAN.json"), baseline)

    # ---- PRE mapper P2-A cases -------------------------------------------
    mapper = {"phase": "PRE", "stamp": stamp,
              "executed_implementations": {
                  "production": "SOURCE 03_SCRIPTS/checker_plus4_successor.py "
                                "(importlib; exact source file)",
                  "qc": "historical QCPE AST-extracted from SOURCE "
                        "03_SCRIPTS/qc_countercheck.py (executed defs: "
                        + ", ".join(qc_executed) + ")"},
              "p2a_cases": [], "p2a_exe_cases": [], "p2a_input_type_cases": [],
              "desktop_parity": []}
    for (cid, dname, fixture, sections, ib, fsize, va, n,
         expected, basis) in p2a_cases():
        entry = {"case_id": cid, "desktop_case": dname,
                 "geometry": {"sections": [
                     {"name": nm, "rva": f"0x{s:08X}", "vsize": f"0x{vs:X}",
                      "rsize": f"0x{rs:X}", "roff": f"0x{ro:X}"}
                     for (nm, s, vs, rs, ro) in sections],
                     "image_base": f"0x{ib:08X}", "file_size": f"0x{fsize:X}"},
                 "request": {"va": fmt_va(va), "n": n},
                 "contract_expected": expected, "contract_basis": basis,
                 "oracle_expected": None,
                 "pre_production_v1": None, "pre_qc_v1": None}
        exp_cls, exp_why = oracle_expectation(sections, ib, fsize, va, n)
        entry["oracle_expected"] = {"classification": exp_cls, "basis": exp_why}
        entry["oracle_expected_matches_contract"] = (exp_cls == expected)
        v1_pe = v1.RangeSafePE(fixture, ib)
        qc_pe = QCPE(fixture, ib)
        entry["pre_production_v1"] = observe_read(v1_pe, va, n)
        entry["pre_qc_v1"] = observe_read(qc_pe, va, n)
        entry["fixture_sha256"] = sha256_bytes(fixture)
        mapper["p2a_cases"].append(entry)
        if dname is not None:
            d = next(x for x in desktop if x["name"] == dname)
            parity = {"case_id": cid, "desktop_name": dname,
                      "desktop_expected": d["expected"],
                      "desktop_production_outcome": d["production"]["outcome"],
                      "desktop_production_bytes": d["production"].get("bytes"),
                      "pre_production_outcome":
                          entry["pre_production_v1"]["read"]["outcome"],
                      "pre_production_bytes":
                          entry["pre_production_v1"]["read"].get("bytes_hex"),
                      "parity": (
                          entry["pre_production_v1"]["read"].get("bytes_hex")
                          == d["production"].get("bytes", "").replace(
                              " ", " ").strip().replace("41414141",
                                                        "41 41 41 41")
                          or (entry["pre_production_v1"]["read"]["outcome"]
                              == d["production"]["outcome"]))}
            mapper["desktop_parity"].append(parity)

    for (cid, dname, data, _s, ib, fsize, va, n, expected, basis) \
            in p2a_exe_cases(exe_data):
        entry = {"case_id": cid, "geometry": {
            "image": "the pinned physical EXE",
            "image_base": f"0x{ib:08X}", "file_size": f"0x{fsize:X}"},
            "request": {"va": fmt_va(va), "n": n},
            "contract_expected": expected, "contract_basis": basis}
        v1_pe = v1.RangeSafePE(data)
        qc_pe = QCPE(data)
        entry["pre_production_v1"] = observe_read(v1_pe, va, n)
        entry["pre_qc_v1"] = observe_read(qc_pe, va, n)
        mapper["p2a_exe_cases"].append(entry)

    f_cross = build_synthetic_pe(CROSS_SECTIONS, file_size=0x500, filler=0xCC)
    v1_pe = v1.RangeSafePE(f_cross)
    qc_pe = QCPE(f_cross)
    for cid, va, n in p2a_input_type_cases():
        entry = {"case_id": cid, "request": {"va": fmt_va(va), "n": n},
                 "contract_expected": "REJECTED_INVALID_INPUT",
                 "contract_basis": "P2-A validation before section matching"}
        entry["pre_production_v1"] = observe_read(v1_pe, va, n)
        entry["pre_qc_v1"] = observe_read(qc_pe, va, n)
        mapper["p2a_input_type_cases"].append(entry)
    wjson(os.path.join(pre_dir, f"PRE_{stamp}_MAPPER_P2A_RAW.json"), mapper)

    # ---- PRE P2-B header truncation cases --------------------------------
    full, truncs = p2b_fixtures()
    header = {"phase": "PRE", "stamp": stamp,
              "fixture_layout": ("e_lfanew=0x80; COFF at 0x84; Magic read at "
                                 "0x98; ImageBase read at 0xB4; "
                                 "SizeOfOptionalHeader 0xE0; section table "
                                 "at 0x1A0; one section .text (RVA 0x1000, "
                                 "vsize 0x100, rsize 0x100, roff 0x400); "
                                 "full file 0x500 bytes; truncations are "
                                 "total FILE sizes in bytes"),
              "header_field_expectations": header_field_expectations(),
              "positive_intact": {}, "truncations": {}, "probes": {}}
    header["positive_intact"]["pre_production_v1"] = observe_construct(
        "v1", v1.RangeSafePE, full)
    header["positive_intact"]["pre_qc_v1"] = observe_construct("qc", QCPE, full)
    header["positive_intact"]["read_first_section_byte"] = {
        "request": {"va": "0x00401000", "n": 1},
        "pre_production_v1": observe_read(v1.RangeSafePE(full), 0x00401000, 1),
        "pre_qc_v1": observe_read(QCPE(full), 0x00401000, 1)}
    for size in (0x98, 0x99, 0xB4, 0xB7):
        data = truncs[size]
        header["truncations"][f"0x{size:X}"] = {
            "file_size": f"0x{size:X}",
            "expected": "CONTROLLED_REJECT (REJECTED_INVALID_INPUT / QC_REJECT)",
            "pre_production_v1": observe_construct("v1", v1.RangeSafePE, data),
            "pre_qc_v1": observe_construct("qc", QCPE, data)}
    for size in (0x9A, 0xB8, 0x1C0):
        data = truncs[size]
        header["probes"][f"0x{size:X}"] = {
            "file_size": f"0x{size:X}",
            "expected": ("boundary-specific probe — confirm the exact failure "
                         "stage; do NOT assume a complete valid PE image"),
            "pre_production_v1": observe_construct("v1", v1.RangeSafePE, data),
            "pre_qc_v1": observe_construct("qc", QCPE, data)}
    wjson(os.path.join(pre_dir, f"PRE_{stamp}_HEADER_P2B_RAW.json"), header)

    # ---- PRE P3 wrong-callsite mutants ------------------------------------
    fixtures, orig_rec = make_mutant_fixtures(stamp, scratch_dir, v1)
    p3 = {"phase": "PRE", "stamp": stamp,
          "canonical_w_callsite": f"0x{W_CANONICAL_VA:08X}",
          "source_record": {k: orig_rec[k] for k in
                            ("RECORD_ID", "CALLSITE_VA", "BYTES",
                             "SIGNED_REL32", "NEXT_VA", "TARGET_VA",
                             "TARGET_FORMULA", "PHYSICAL_OFFSET")},
          "note": ("the ORIGINAL production checker has NO RECORD_ID<->"
                   "CALLSITE_VA identity gate (expected PRE false PASS per "
                   "the Desktop demonstration); the separate fixed-address "
                   "QC comparison catches the teleport (W1) but NOT the "
                   "RECORD_ID-only mutant (W2) — recorded honestly"),
          "mutants": {}}
    for key in ("W1", "W2", "W3"):
        doc, fix = fixtures[key]
        entry = {"fixture": fix,
                 "record": {k: doc["active_records"][0][k] for k in
                            ("RECORD_ID", "CALLSITE_VA", "BYTES",
                             "SIGNED_REL32", "NEXT_VA", "TARGET_VA",
                             "PHYSICAL_OFFSET")}}
        entry["pre_v1_production"] = replay_record_through_gate(
            v1, fix["path"] if os.path.isabs(fix["path"])
            else os.path.join(REPO_ROOT, fix["path"]), f"PRE {key} on v1")
        entry["pre_fixed_address_qc"] = fixed_address_qc_comparison(QCPE, doc)
        p3["mutants"][key] = entry
    clean_fix = fixtures["CLEAN"][1]
    p3["clean_scratch_copy"] = {
        "fixture": clean_fix,
        "pre_v1_production": replay_record_through_gate(
            v1, os.path.join(REPO_ROOT, clean_fix["path"]), "PRE CLEAN on v1")}
    wjson(os.path.join(pre_dir, f"PRE_{stamp}_WRONG_CALLSITE_P3_RAW.json"), p3)

    # ---- PRE preserved controls ------------------------------------------
    controls = {"phase": "PRE", "stamp": stamp,
                 "raw_to_bss_crossing": None, "declared_raw_past_eof": None,
                 "structured_col_name_crossing": None,
                 "mc1_to_mc6": run_mc_controls(v1, exe_data),
                 "w_record_mutation_gates": run_w_record_mutation_gates(v1)}
    img3 = build_synthetic_pe(CROSS_SECTIONS, file_size=0x500, filler=0xCC,
                              section_fills={".text": bytes(range(0x80))})
    v1_pe3 = v1.RangeSafePE(img3)
    qc_pe3 = QCPE(img3)
    first_va = 0x00401000
    last_va = 0x0040107F
    controls["raw_to_bss_crossing"] = {
        "first_raw_byte": {"pre_production_v1": observe_read(v1_pe3, first_va, 1),
                           "pre_qc_v1": observe_read(qc_pe3, first_va, 1)},
        "last_raw_byte": {"pre_production_v1": observe_read(v1_pe3, last_va, 1),
                          "pre_qc_v1": observe_read(qc_pe3, last_va, 1)},
        "crossing_read": {"pre_production_v1": observe_read(v1_pe3, last_va, 2),
                          "pre_qc_v1": observe_read(qc_pe3, last_va, 2)}}
    img4 = build_synthetic_pe([(".text", 0x1000, 0x100, 0x200, 0x400)],
                              file_size=0x500, filler=0xCC)
    v1_pe4 = v1.RangeSafePE(img4)
    qc_pe4 = QCPE(img4)
    controls["declared_raw_past_eof"] = {
        "request": {"va": "0x00401100", "n": 16},
        "pre_production_v1": observe_read(v1_pe4, 0x00401100, 16),
        "pre_qc_v1": observe_read(qc_pe4, 0x00401100, 16)}
    controls["structured_col_name_crossing"] = {
        "pre_production_v1": structured_crossing_control(v1, v1.RangeSafePE),
        "pre_qc_v1": structured_crossing_control(None, QCPE)}
    wjson(os.path.join(pre_dir, f"PRE_{stamp}_CONTROLS_RAW.json"), controls)

    # ---- identities wrap-up + SHA index ----------------------------------
    identities["exe_after_pre"] = {
        "size": os.path.getsize(EXE_PATH), "sha256": sha256_file(EXE_PATH),
        "unchanged": sha256_file(EXE_PATH) == EXE_SHA256}
    identities["source_pins_json_after_pre"] = {
        "sha256": sha256_file(SRC_PINS),
        "unchanged": sha256_file(SRC_PINS) == SRC_PINS_SHA256}
    wjson(os.path.join(pre_dir, f"PRE_{stamp}_RUN_HEADER.json"), identities)

    index = {"phase": "PRE", "stamp": stamp, "files": {}}
    for fn in sorted(os.listdir(pre_dir)):
        p = os.path.join(pre_dir, fn)
        if os.path.isfile(p):
            index["files"][fn] = {"size": os.path.getsize(p),
                                  "sha256": sha256_file(p)}
    for fn in sorted(os.listdir(scratch_dir)):
        p = os.path.join(scratch_dir, fn)
        index["files"]["scratch/" + fn] = {
            "size": os.path.getsize(p), "sha256": sha256_file(p)}
    index["note"] = ("this index is written LAST in the PRE phase; it does "
                     "not hash itself; PRE files are never overwritten "
                     "afterwards")
    wjson(os.path.join(pre_dir, f"PRE_{stamp}_SHA256_INDEX.json"), index)

    print("PRE phase complete (stamp", stamp + ")")
    print("  v1 clean baseline:", baseline["pass_count"], "/",
          baseline["checks_total"], "gate", baseline["gate"])
    return 0


# ---------------------------------------------------------------------------
# POST phase
# ---------------------------------------------------------------------------
def run_post(stamp):
    post_dir = os.path.join(PKG_ROOT, "00_POST")
    scratch_dir = os.path.join(post_dir, "scratch")
    pre_dir = os.path.join(PKG_ROOT, "00_PRE")

    identities = {
        "phase": "POST", "run_id": RUN_ID, "stamp": stamp,
        "exe": verify_pin(EXE_PATH, EXE_SIZE, EXE_SHA256, "physical EXE"),
        "v2_checker": {"path": os.path.relpath(V2_CHECKER, REPO_ROOT).replace("\\", "/"),
                       "size": os.path.getsize(V2_CHECKER),
                       "sha256": sha256_file(V2_CHECKER)},
        "source_checker_unchanged": {
            "sha256": sha256_file(SRC_CHECKER),
            "match": sha256_file(SRC_CHECKER) == SRC_CHECKER_SHA256},
        "source_qc_unchanged": {
            "sha256": sha256_file(SRC_QC),
            "match": sha256_file(SRC_QC) == SRC_QC_SHA256},
        "source_pins_json_unchanged": {
            "sha256": sha256_file(SRC_PINS),
            "match": sha256_file(SRC_PINS) == SRC_PINS_SHA256},
    }
    v1 = import_source_checker()
    v2 = import_v2_checker()
    qc_ns, qc_executed = ast_extract_qcpe()
    QCPE = qc_ns["QCPE"]

    with open(EXE_PATH, "rb") as f:
        exe_data = f.read()

    # ---- POST baseline: v2 clean run (default source pins path) ---------
    baseline = {
        "description": "v2 production clean run on the pinned physical EXE "
                       "via the DEFAULT source ACTIVE_CORRECTED_PINS.json "
                       "loader path",
        "exe_identity": {"size": len(exe_data), "sha256": sha256_bytes(exe_data)}}
    results = v2.run_checks()
    ok, fails = v2.gate(results)
    baseline["checks_total"] = len(results)
    baseline["pass_count"] = sum(1 for r in results if r[1] == "PASS")
    baseline["gate"] = "PASS" if ok else "FAIL"
    baseline["fail_ids"] = [f[0] for f in fails]
    baseline["id_census"] = {
        "historical_80": [r[0] for r in results if not r[0].startswith("RECW:")],
        "recw": [r[0] for r in results if r[0].startswith("RECW:")]}
    baseline["results_raw"] = [list(r) for r in results]
    wjson(os.path.join(post_dir, f"POST_{stamp}_BASELINE_CLEAN.json"), baseline)

    # ---- POST mapper P2-A cases -------------------------------------------
    mapper = {"phase": "POST", "stamp": stamp,
              "executed_implementations": {
                  "production": "03_SCRIPTS/checker_plus4_successor_v2.py "
                                "(corrected production)",
                  "qc": "historical QCPE v1 (AST-extracted; UNFIXED — the "
                        "fixed independent QC is the separate parent QC "
                        "phase; recorded for continuity, NOT presented as "
                        "the corrected QC)"},
              "p2a_cases": [], "p2a_exe_cases": [], "p2a_input_type_cases": []}
    for (cid, dname, fixture, sections, ib, fsize, va, n,
         expected, basis) in p2a_cases():
        exp_cls, exp_why = oracle_expectation(sections, ib, fsize, va, n)
        v2_pe = v2.RangeSafePE(fixture, ib)
        qc_pe = QCPE(fixture, ib)
        entry = {"case_id": cid, "request": {"va": fmt_va(va), "n": n},
                 "contract_expected": expected, "contract_basis": basis,
                 "oracle_expected": {"classification": exp_cls,
                                     "basis": exp_why},
                 "post_production_v2": observe_read(v2_pe, va, n),
                 "post_qc_v1_historical": observe_read(qc_pe, va, n),
                 "post_qc_v2_fixed": "DEFERRED_TO_QC_PHASE"}
        mapper["p2a_cases"].append(entry)
    for (cid, dname, data, _s, ib, fsize, va, n, expected, basis) \
            in p2a_exe_cases(exe_data):
        v2_pe = v2.RangeSafePE(data)
        qc_pe = QCPE(data)
        mapper["p2a_exe_cases"].append({
            "case_id": cid, "request": {"va": fmt_va(va), "n": n},
            "contract_expected": expected, "contract_basis": basis,
            "post_production_v2": observe_read(v2_pe, va, n),
            "post_qc_v1_historical": observe_read(qc_pe, va, n),
            "post_qc_v2_fixed": "DEFERRED_TO_QC_PHASE"})
    f_cross = build_synthetic_pe(CROSS_SECTIONS, file_size=0x500, filler=0xCC)
    v2_pe = v2.RangeSafePE(f_cross)
    qc_pe = QCPE(f_cross)
    for cid, va, n in p2a_input_type_cases():
        mapper["p2a_input_type_cases"].append({
            "case_id": cid, "request": {"va": fmt_va(va), "n": n},
            "contract_expected": "REJECTED_INVALID_INPUT",
            "post_production_v2": observe_read(v2_pe, va, n),
            "post_qc_v1_historical": observe_read(qc_pe, va, n)})
    wjson(os.path.join(post_dir, f"POST_{stamp}_MAPPER_P2A_RAW.json"), mapper)

    # ---- POST P2-B header truncation cases -------------------------------
    full, truncs = p2b_fixtures()
    header = {"phase": "POST", "stamp": stamp,
              "fixture_layout": "same Desktop layout as PRE",
              "positive_intact": {}, "truncations": {}, "probes": {}}
    header["positive_intact"]["post_production_v2"] = observe_construct(
        "v2", v2.RangeSafePE, full)
    header["positive_intact"]["post_qc_v1_historical"] = observe_construct(
        "qc", QCPE, full)
    # programmatic fixture-header verification (contract par. 3): the
    # constructed mapper's measured header values must equal the fixture
    try:
        v2_pe_full = v2.RangeSafePE(full)
        v2_secs = serialize_sections("v2", v2_pe_full)
        want_secs = [{"name": ".text", "rva": "0x00001000", "vsize": "0x100",
                      "raw_offset": "0x400", "raw_size": "0x100",
                      "member_end": "0x1100"}]
        checks = {
            "e_lfanew": {"measured": "0x%X" % struct.unpack_from("<I", full, 0x3C)[0],
                         "expected": "0x80",
                         "match": struct.unpack_from("<I", full, 0x3C)[0] == 0x80},
            "pe_signature": {"measured": repr(full[0x80:0x84]),
                             "expected": repr(b"PE\x00\x00"),
                             "match": full[0x80:0x84] == b"PE\x00\x00"},
            "machine": {"measured": "0x%04X" % struct.unpack_from("<H", full, 0x84)[0],
                        "expected": "0x14C",
                        "match": struct.unpack_from("<H", full, 0x84)[0] == 0x14C},
            "number_of_sections": {
                "measured": struct.unpack_from("<H", full, 0x86)[0],
                "expected": 1,
                "match": struct.unpack_from("<H", full, 0x86)[0] == 1},
            "size_of_optional_header": {
                "measured": "0x%X" % struct.unpack_from("<H", full, 0x94)[0],
                "expected": "0xE0",
                "match": struct.unpack_from("<H", full, 0x94)[0] == 0xE0},
            "optional_header_magic": {
                "measured": "0x%04X" % struct.unpack_from("<H", full, 0x98)[0],
                "expected": "0x10B (PE32)",
                "match": struct.unpack_from("<H", full, 0x98)[0] == 0x10B},
            "image_base": {"measured": "0x%08X" % struct.unpack_from("<I", full, 0xB4)[0],
                           "expected": "0x00400000",
                           "match": struct.unpack_from("<I", full, 0xB4)[0] == 0x00400000},
            "image_base_measured_via_mapper": {
                "measured": "0x%08X" % v2_pe_full.image_base,
                "expected": "0x00400000",
                "match": v2_pe_full.image_base == 0x00400000},
            "section": {"measured": v2_secs, "expected": want_secs,
                        "match": v2_secs == want_secs}}
        checks["all_match"] = all(v.get("match") for v in checks.values()
                                  if isinstance(v, dict))
        header["positive_intact"]["measured_vs_fixture_verification"] = checks
    except Exception as e:  # noqa: BLE001
        header["positive_intact"]["measured_vs_fixture_verification"] = {
            "error": f"{type(e).__name__}: {e}"}
    header["positive_intact"]["read_first_section_byte"] = {
        "request": {"va": "0x00401000", "n": 1},
        "post_production_v2": observe_read(v2.RangeSafePE(full), 0x00401000, 1),
        "post_qc_v1_historical": observe_read(QCPE(full), 0x00401000, 1)}
    for size in (0x98, 0x99, 0xB4, 0xB7):
        data = truncs[size]
        header["truncations"][f"0x{size:X}"] = {
            "file_size": f"0x{size:X}",
            "expected": "CONTROLLED_REJECT (ControlledReadError with a "
                        "stage-specific REJECTED_INVALID_INPUT reason)",
            "post_production_v2": observe_construct("v2", v2.RangeSafePE, data),
            "post_qc_v1_historical": observe_construct("qc", QCPE, data),
            "post_qc_v2_fixed": "DEFERRED_TO_QC_PHASE"}
    for size in (0x9A, 0xB8, 0x190, 0x1C0):
        data = truncs[size]
        header["probes"][f"0x{size:X}"] = {
            "file_size": f"0x{size:X}",
            "expected": ("controlled rejection at the exact failure stage "
                         "(0x190 is a POST-only probe: mid-section-table "
                         "truncation, table region 0x178..0x1A0)"),
            "post_production_v2": observe_construct("v2", v2.RangeSafePE, data),
            "post_qc_v1_historical": observe_construct("qc", QCPE, data)}
    wjson(os.path.join(post_dir, f"POST_{stamp}_HEADER_P2B_RAW.json"), header)

    # ---- POST P3 wrong-callsite mutants -----------------------------------
    fixtures, orig_rec = make_mutant_fixtures(stamp, scratch_dir, v2)
    p3 = {"phase": "POST", "stamp": stamp,
          "canonical_binding": "v2 CANONICAL_RECORD_IDENTITY = "
                               "{W_CTOR_CALL_AT_006CB836: 0x006CB836} — a "
                               "non-mutatable module constant independent of "
                               "the fixture JSON",
          "mutants": {}}
    for key in ("W1", "W2", "W3"):
        doc, fix = fixtures[key]
        entry = {"fixture": fix,
                 "record": {k: doc["active_records"][0][k] for k in
                            ("RECORD_ID", "CALLSITE_VA", "BYTES",
                             "SIGNED_REL32", "NEXT_VA", "TARGET_VA",
                             "PHYSICAL_OFFSET")}}
        entry["post_v2_production"] = replay_record_through_gate(
            v2, os.path.join(REPO_ROOT, fix["path"]), f"POST {key} on v2")
        p3["mutants"][key] = entry
    clean_fix = fixtures["CLEAN"][1]
    p3["clean_scratch_copy_v2"] = {
        "fixture": clean_fix,
        "post_v2_production": replay_record_through_gate(
            v2, os.path.join(REPO_ROOT, clean_fix["path"]),
            "POST CLEAN scratch copy on v2")}
    wjson(os.path.join(post_dir, f"POST_{stamp}_WRONG_CALLSITE_P3_RAW.json"), p3)

    # ---- POST preserved controls -----------------------------------------
    controls = {"phase": "POST", "stamp": stamp,
                "mc1_to_mc6": run_mc_controls(v2, exe_data),
                "w_record_mutation_gates": run_w_record_mutation_gates(v2)}
    img3 = build_synthetic_pe(CROSS_SECTIONS, file_size=0x500, filler=0xCC,
                              section_fills={".text": bytes(range(0x80))})
    v2_pe3 = v2.RangeSafePE(img3)
    controls["raw_to_bss_crossing"] = {
        "first_raw_byte": observe_read(v2_pe3, 0x00401000, 1),
        "last_raw_byte": observe_read(v2_pe3, 0x0040107F, 1),
        "crossing_read": observe_read(v2_pe3, 0x0040107F, 2)}
    img4 = build_synthetic_pe([(".text", 0x1000, 0x100, 0x200, 0x400)],
                              file_size=0x500, filler=0xCC)
    controls["declared_raw_past_eof"] = observe_read(
        v2.RangeSafePE(img4), 0x00401100, 16)
    controls["structured_col_name_crossing"] = structured_crossing_control(
        v2, v2.RangeSafePE)
    wjson(os.path.join(post_dir, f"POST_{stamp}_CONTROLS_RAW.json"), controls)

    # ---- POST regression ---------------------------------------------------
    hist_tables = ast_pin_tables(HIST_CHECKER, HIST_CHECKER_SHA256)
    src_tables = {"BYTE_PINS": v1.BYTE_PINS, "REL32_PINS": v1.REL32_PINS,
                  "RTTI_PINS": v1.RTTI_PINS, "STRING_PINS": v1.STRING_PINS}
    v2_tables = {"BYTE_PINS": v2.BYTE_PINS, "REL32_PINS": v2.REL32_PINS,
                 "RTTI_PINS": v2.RTTI_PINS, "STRING_PINS": v2.STRING_PINS}
    table_identity = {
        "hist_vs_src": {k: hist_tables[k] == src_tables[k]
                        for k in hist_tables},
        "v2_vs_hist": {k: v2_tables[k] == hist_tables[k]
                       for k in hist_tables},
        "v2_vs_src": {k: v2_tables[k] == src_tables[k] for k in hist_tables},
    }
    required_ids = required_80_ids(hist_tables)
    measured_ids = [r[0] for r in results if not r[0].startswith("RECW:")]
    recw_ids = [r[0] for r in results if r[0].startswith("RECW:")]
    regression = {
        "phase": "POST", "stamp": stamp,
        "hist_checker_identity": {
            "path": os.path.relpath(HIST_CHECKER, REPO_ROOT).replace("\\", "/"),
            "size": os.path.getsize(HIST_CHECKER),
            "sha256_measured": sha256_file(HIST_CHECKER),
            "sha256_pinned": HIST_CHECKER_SHA256,
            "access": "READ-ONLY AST parse (never executed)"},
        "required_id_source": "historical PROVENANCE checker tables + the "
                              "SOURCE_RUN successor tables",
        "required_check_id_count": len(required_ids),
        "required_check_ids": sorted(required_ids),
        "duplicate_required_ids": len(required_ids) != len(set(required_ids)),
        "table_identity": table_identity,
        "clean_baseline_v2": {
            "suite_total": len(results),
            "historical_80": {
                "count": len(measured_ids),
                "pass_count": sum(1 for r in results
                                  if not r[0].startswith("RECW:")
                                  and r[1] == "PASS"),
                "all_pass": all(r[1] == "PASS" for r in results
                                if not r[0].startswith("RECW:")),
                "missing_ids": sorted(set(required_ids) - set(measured_ids)),
                "extra_ids": sorted(set(measured_ids) - set(required_ids)),
                "duplicate_ids": len(measured_ids) != len(set(measured_ids))},
            "recw_old_6": {
                "ids": [i for i in recw_ids
                        if i != "RECW:W_RECORD_IDENTITY"],
                "pass_count": sum(1 for r in results
                                  if r[0].startswith("RECW:")
                                  and r[0] != "RECW:W_RECORD_IDENTITY"
                                  and r[1] == "PASS")},
            "new_identity_check": {
                "id": "RECW:W_RECORD_IDENTITY",
                "present": "RECW:W_RECORD_IDENTITY" in recw_ids,
                "verdict": next((r[1] for r in results
                                 if r[0] == "RECW:W_RECORD_IDENTITY"), "ABSENT"),
                "denominator_note": "the new check adds ONE gate: the clean "
                                    "baseline denominator rises from 86 to 87"},
            "gate": "PASS" if ok else "FAIL"},
        "separate_denominators": {
            "historical_80": 80, "recw_old": 6, "new_identity": 1,
            "total": 87},
        "target_formula_note": "TARGET_FORMULA stays a schema-required field "
                               "(REQUIRED_PIN_FIELDS) but is NOT promoted to "
                               "a separate P3 gate; the denominator is "
                               "honestly 87, and the identity gate is NOT "
                               "substituted by any formula check",
        "mc1_to_mc6_summary": controls["mc1_to_mc6"],
        "w_record_mutation_gates_summary": controls["w_record_mutation_gates"],
    }
    wjson(os.path.join(post_dir, f"POST_{stamp}_REGRESSION_RAW.json"),
          regression)

    # ---- assemble MAPPER_BOUNDARY_RESULTS.json ---------------------------
    pre_mapper_path = None
    pre_header_path = None
    pre_p3_path = None
    pre_p3_filename = None
    for fn in os.listdir(pre_dir):
        if fn.startswith("PRE_") and fn.endswith("_MAPPER_P2A_RAW.json"):
            pre_mapper_path = os.path.join(pre_dir, fn)
        elif fn.startswith("PRE_") and fn.endswith("_HEADER_P2B_RAW.json"):
            pre_header_path = os.path.join(pre_dir, fn)
        elif fn.startswith("PRE_") and fn.endswith("_WRONG_CALLSITE_P3_RAW.json"):
            pre_p3_path = os.path.join(pre_dir, fn)
            pre_p3_filename = fn
    with open(pre_mapper_path, "r", encoding="utf-8") as f:
        pre_mapper = json.load(f)
    with open(pre_header_path, "r", encoding="utf-8") as f:
        pre_header = json.load(f)
    with open(pre_p3_path, "r", encoding="utf-8") as f:
        pre_p3 = json.load(f)
    pre_by_id = {c["case_id"]: c for c in pre_mapper["p2a_cases"]}
    post_by_id = {c["case_id"]: c for c in mapper["p2a_cases"]}
    geom_by_id = {}
    for (cid, dname, fixture, sections, ib, fsize, va, n, expected,
         basis) in p2a_cases():
        geom_by_id[cid] = {
            "sections": [{"name": nm, "rva": f"0x{s:08X}",
                          "vsize": f"0x{vs:X}", "rsize": f"0x{rs:X}",
                          "roff": f"0x{ro:X}"}
                         for (nm, s, vs, rs, ro) in sections],
            "image_base": f"0x{ib:08X}", "file_size": f"0x{fsize:X}"}

    boundary = {
        "run_id": RUN_ID, "phase": "POST-ASSEMBLED", "stamp": stamp,
        "evidence_files": {
            "pre_mapper_raw": os.path.relpath(pre_mapper_path, REPO_ROOT).replace("\\", "/"),
            "pre_header_raw": os.path.relpath(pre_header_path, REPO_ROOT).replace("\\", "/"),
            "pre_p3_raw": os.path.relpath(pre_p3_path, REPO_ROOT).replace("\\", "/"),
            "post_mapper_raw": f"00_POST/POST_{stamp}_MAPPER_P2A_RAW.json",
            "post_header_raw": f"00_POST/POST_{stamp}_HEADER_P2B_RAW.json",
            "post_p3_raw": f"00_POST/POST_{stamp}_WRONG_CALLSITE_P3_RAW.json",
            "note": "00_PRE/ files are the immutable PRE record; this "
                    "assembled file merges PRE (v1) and POST (v2) "
                    "observations; PRE raws were never overwritten"},
        "policy": {
            "interval_semantics": "half-open VA intervals [VA, VA+n); all "
                                  "validation BEFORE PE section matching",
            "validation": "va/n integers not bool; 0 <= VA < 2**32; n > 0; "
                          "VA+n <= 2**32; VA underflow (< ImageBase) "
                          "rejected separately",
            "section_matching": "ANY-INTERSECTION: more than one "
                                 "intersecting section => REJECTED even if "
                                 "one fully contains the read; a single "
                                 "intersecting section must cover the WHOLE "
                                 "request; cross-section / partially "
                                 "unmapped intervals never yield bytes",
            "classification_values": ["RAW_BACKED", "VIRTUAL_BSS",
                                      "UNMAPPED", "REJECTED_INVALID_INPUT"],
            "raw_padding_policy": v2.RAW_PADDING_POLICY,
            "no_fabricated_zeros": True,
            "short_slice_is_not_success": True,
            "general_pe_mapper_correctness": "NOT_ESTABLISHED",
            "relabeled_overflow_control": "ImageBase+0x7FFFFFFF is UNMAPPED "
                                          "(far beyond the image, a VALID "
                                          "32-bit range); it is NOT a PE32 "
                                          "address-space overflow test; the "
                                          "real boundary tests are the 4GiB "
                                          "cases below",
        },
        "cases": []}
    for cid in [c[0] for c in p2a_cases()]:
        pre_c = pre_by_id.get(cid)
        post_c = post_by_id[cid]
        exp = post_c["oracle_expected"]["classification"]
        v2obs = post_c["post_production_v2"]
        v2cls = v2obs["classify"].get("classification")
        if pre_c is None:
            v1obs = {"note": "NOT_IN_PRE (runner case-design correction; "
                             "case added after the PRE run; disclosed)"}
            pre_qc = v1obs
            v1cls = "NOT_IN_PRE"
            v1_read_outcome = "NOT_IN_PRE"
        else:
            v1obs = pre_c["pre_production_v1"]
            pre_qc = pre_c["pre_qc_v1"]
            v1cls = v1obs["classify"].get("classification")
            v1_read_outcome = v1obs["read"]["outcome"]
        geometry = geom_by_id[cid]
        case = {
            "case_id": cid,
            "desktop_case": (pre_c or {}).get("desktop_case"),
            "geometry": geometry,
            "request": post_c["request"],
            "expected_classification": post_c["contract_expected"],
            "expected_basis": post_c["contract_basis"],
            "oracle_expected": post_c["oracle_expected"],
            "pre_production_v1": v1obs,
            "pre_qc_v1": pre_qc,
            "post_production_v2": v2obs,
            "post_qc_v1_historical": post_c["post_qc_v1_historical"],
            "post_qc_v2_fixed": "DEFERRED_TO_QC_PHASE (qc_countercheck_v2.py "
                                "is the fresh-QC worker's own implementation "
                                "— a separate parent phase)",
            "observed_classification_v1": v1cls,
            "observed_classification_v2": v2cls,
            "exception_class_v1": (v1obs["read"].get("exception_type")
                                  if "read" in v1obs else "NOT_IN_PRE"),
            "exception_class_v2": v2obs["read"].get("exception_type"),
            "returned_bytes_v1": (v1obs["read"].get("bytes_hex")
                                  if "read" in v1obs else None),
            "returned_bytes_v2": v2obs["read"].get("bytes_hex"),
            "verdict": "PASS" if (v2cls == exp == post_c["contract_expected"]
                                  and (exp != "RAW_BACKED"
                                       or v2obs["read"]["outcome"]
                                       == "RETURNED")
                                  and (exp == "RAW_BACKED"
                                       or v2obs["read"]["outcome"]
                                       == "EXCEPTION"))
                       else "FAIL",
            "pre_falsifier_demonstrated": (
                (v1_read_outcome == "RETURNED"
                 and post_c["contract_expected"] == "REJECTED_INVALID_INPUT")
                or (v1cls is not None and v1cls != "NOT_IN_PRE"
                    and v1cls != post_c["contract_expected"])),
            "negative_finding": None}
        if case["verdict"] != "PASS":
            case["negative_finding"] = (
                f"v2 classification {v2cls!r} != expected {exp!r}")
        boundary["cases"].append(case)
    for pre_c, post_c in zip(pre_mapper["p2a_exe_cases"],
                             mapper["p2a_exe_cases"]):
        v2obs = post_c["post_production_v2"]
        v2cls = v2obs["classify"].get("classification")
        exp = post_c["contract_expected"]
        case = {
            "case_id": post_c["case_id"],
            "geometry": pre_c["geometry"],
            "request": post_c["request"],
            "expected_classification": exp,
            "expected_basis": post_c["contract_basis"],
            "pre_production_v1": pre_c["pre_production_v1"],
            "pre_qc_v1": pre_c["pre_qc_v1"],
            "post_production_v2": v2obs,
            "post_qc_v1_historical": post_c["post_qc_v1_historical"],
            "post_qc_v2_fixed": "DEFERRED_TO_QC_PHASE",
            "observed_classification_v2": v2cls,
            "verdict": "PASS" if v2cls == exp else "FAIL",
            "negative_finding": None}
        if case["verdict"] != "PASS":
            case["negative_finding"] = f"v2 classification {v2cls!r} != {exp!r}"
        boundary["cases"].append(case)
    for pre_c, post_c in zip(pre_mapper["p2a_input_type_cases"],
                             mapper["p2a_input_type_cases"]):
        v2cls = post_c["post_production_v2"]["classify"].get("classification")
        case = {
            "case_id": post_c["case_id"],
            "request": post_c["request"],
            "expected_classification": "REJECTED_INVALID_INPUT",
            "pre_production_v1": pre_c["pre_production_v1"],
            "pre_qc_v1": pre_c["pre_qc_v1"],
            "post_production_v2": post_c["post_production_v2"],
            "post_qc_v1_historical": post_c["post_qc_v1_historical"],
            "observed_classification_v2": v2cls,
            "verdict": "PASS" if v2cls == "REJECTED_INVALID_INPUT" else "FAIL",
            "negative_finding": None}
        boundary["cases"].append(case)

    def trunc_case(size, kind):
        pre_key = pre_header["truncations"].get(f"0x{size:X}") if kind == "trunc" \
            else pre_header["probes"].get(f"0x{size:X}")
        if pre_key is None:
            pre_key = {"pre_production_v1": "NOT_IN_PRE (POST-only probe)",
                       "pre_qc_v1": "NOT_IN_PRE (POST-only probe)"}
        post_src = header["truncations"] if kind == "trunc" else header["probes"]
        post_c = post_src[f"0x{size:X}"]
        v2c = post_c["post_production_v2"]
        pre_obs = pre_key["pre_production_v1"]
        if isinstance(pre_obs, dict):
            obs_v1 = pre_obs["outcome"]
            exc_v1 = pre_obs.get("exception_type")
        else:
            obs_v1 = "NOT_IN_PRE (POST-only probe)"
            exc_v1 = "NOT_IN_PRE (POST-only probe)"
        oracle_c = oracle_constructor_expectation(size)
        verdict = "FAIL"
        if kind == "trunc":
            verdict = ("PASS" if v2c["outcome"] == "EXCEPTION"
                       and v2c.get("exception_type") == "ControlledReadError"
                       else "FAIL")
        else:
            verdict = ("PASS" if v2c["outcome"] == oracle_c["outcome"]
                       and (oracle_c["outcome"] == "CONSTRUCTED"
                            or v2c.get("exception_type")
                            == "ControlledReadError")
                       else "FAIL")
        return {
            "case_id": f"P2B-{kind.upper()}-{size:#X}",
            "geometry": {"total_synthetic_file_size_bytes": f"0x{size:X}",
                         "fixture_layout": header["fixture_layout"]},
            "request": {"operation": "construct the PE mapper (header parse)"},
            "expected_classification":
                "REJECTED_INVALID_INPUT (ControlledReadError)" if kind == "trunc"
                else f"probe oracle expectation: {oracle_c['outcome']}"
                     + (f" at stage '{oracle_c['failing_stage']}'"
                        if oracle_c["failing_stage"] else ""),
            "oracle_constructor_expectation": oracle_c,
            "pre_production_v1": pre_key["pre_production_v1"],
            "pre_qc_v1": pre_key["pre_qc_v1"],
            "post_production_v2": v2c,
            "post_qc_v1_historical": post_c["post_qc_v1_historical"],
            "post_qc_v2_fixed": "DEFERRED_TO_QC_PHASE",
            "observed_outcome_v1": obs_v1,
            "observed_exception_type_v1": exc_v1,
            "observed_outcome_v2": v2c["outcome"],
            "observed_exception_type_v2": v2c.get("exception_type"),
            "verdict": verdict,
            "negative_finding": None}
    boundary["header_positive_intact"] = {
        "pre_production_v1": pre_header["positive_intact"]["pre_production_v1"],
        "pre_qc_v1": pre_header["positive_intact"]["pre_qc_v1"],
        "post_production_v2": header["positive_intact"]["post_production_v2"],
        "measured_vs_fixture_verification":
            header["positive_intact"].get(
                "measured_vs_fixture_verification"),
        "header_field_expectations": header_field_expectations(),
        "verdict": "PASS" if header["positive_intact"]
        ["post_production_v2"]["outcome"] == "CONSTRUCTED" else "FAIL"}
    for size in (0x98, 0x99, 0xB4, 0xB7):
        boundary["cases"].append(trunc_case(size, "trunc"))
    for size in (0x9A, 0xB8, 0x1C0):
        boundary["cases"].append(trunc_case(size, "probe"))
    boundary["cases"].append(trunc_case(0x190, "probe"))
    boundary["oracle_discipline"] = {
        "measured_quantity": "classification + returned bytes of every "
                             "boundary request, and constructor behavior on "
                             "every truncated synthetic file",
        "independent_source_of_truth": "this runner's own interval/build "
                                       "arithmetic (oracle_expectation) + "
                                       "the constructed fixture bytes + the "
                                       "pinned Desktop expectations for the "
                                       "EXE pin cases (89 46 04 out-of-band "
                                       "pin) + the Desktop's recorded "
                                       "PRE observations",
        "why_non_circular": "the expected classification is computed by a "
                            "separate implementation of the contract rule "
                            "in THIS driver, never by replaying the mapper "
                            "under test; the historical QCPE is a second "
                            "mapper (PRE), and the fixed QC v2 is a separate "
                            "parent phase (never claimed here)",
        "failure_case_detected": "P2A-DESKTOP-1/2 (partial overlap), "
                                 "P2A-DESKTOP-3/4 (32-bit boundary), "
                                 "P2B truncations 0x98/0x99/0xB4/0xB7 — each "
                                 "failed on v1 (false PASS / raw "
                                 "struct.error) and is controlled on v2"}
    wjson(os.path.join(PKG_ROOT, "MAPPER_BOUNDARY_RESULTS.json"), boundary)

    # ---- assemble REGRESSION_RESULTS.json --------------------------------
    def p3_gate_summary(key):
        m = p3["mutants"][key]["post_v2_production"]
        return {
            "checks_total": m["checks_total"], "pass_count": m["pass_count"],
            "gate": m["gate"], "fail_ids": m["fail_ids"],
            "identity_gate_verdict":
                m["recw_verdicts"].get("RECW:W_RECORD_IDENTITY"),
            "other_recw_all_pass": all(
                v == "PASS" for (k, v) in m["recw_verdicts"].items()
                if k != "RECW:W_RECORD_IDENTITY"),
            "historical_80_all_pass": m["historical_80_all_pass"],
            "no_sha_mismatch_rescue":
                "EXE_IDENTITY" not in m["fail_ids"],
            "verdict": "PASS" if (m["gate"] == "FAIL"
                                  and m["fail_ids"] == ["RECW:W_RECORD_IDENTITY"]
                                  and m["historical_80_all_pass"]) else "FAIL"}
    regression_final = {
        "run_id": RUN_ID, "phase": "POST-ASSEMBLED", "stamp": stamp,
        "historical_80_id_regression": regression["clean_baseline_v2"]["historical_80"],
        "required_id_count": regression["required_check_id_count"],
        "required_check_ids": regression["required_check_ids"],
        "duplicate_required_ids": regression["duplicate_required_ids"],
        "table_identity": regression["table_identity"],
        "recw_old_6": regression["clean_baseline_v2"]["recw_old_6"],
        "new_identity_check": regression["clean_baseline_v2"]["new_identity_check"],
        "separate_denominators": regression["separate_denominators"],
        "target_formula_note": regression["target_formula_note"],
        "clean_baseline_v2_total": {
            "suite_total": baseline["checks_total"],
            "pass_count": baseline["pass_count"],
            "gate": baseline["gate"],
            "expected_new_baseline": 87},
        "mc1_to_mc6": controls["mc1_to_mc6"],
        "w_record_mutation_gates": controls["w_record_mutation_gates"],
        "prior_raw_bss_controls": {
            "raw_backed_pin_006E8FA5": next(
                c["post_production_v2"] for c in mapper["p2a_exe_cases"]
                if c["case_id"] == "P2A-REAL-PIN-6E8FA5"),
            "bss_00BA1100": next(
                c["post_production_v2"] for c in mapper["p2a_exe_cases"]
                if c["case_id"] == "P2A-REAL-BSS-BA1100"),
            "bss_00BA73BC": next(
                c["post_production_v2"] for c in mapper["p2a_exe_cases"]
                if c["case_id"] == "P2A-REAL-BSS-BA73BC"),
            "raw_to_bss_crossing": controls["raw_to_bss_crossing"],
            "declared_raw_past_eof": controls["declared_raw_past_eof"],
            "structured_col_name_crossing":
                controls["structured_col_name_crossing"],
            "ambiguous_overlapping_sections": next(
                c["post_production_v2"] for c in mapper["p2a_cases"]
                if c["case_id"] == "P2A-HIST-AMBIGUOUS")},
        "wrong_callsite_mutants": {
            "W1_teleport_006C97D8": p3_gate_summary("W1"),
            "W2_record_id_only": p3_gate_summary("W2"),
            "W3_generality_006CB7CF": p3_gate_summary("W3")},
        "pre_false_pass_record": {
            "source": f"00_PRE/{pre_p3_filename}",
            "W1_v1_gate": pre_p3["mutants"]["W1"]["pre_v1_production"]["gate"],
            "W1_v1_pass_count":
                pre_p3["mutants"]["W1"]["pre_v1_production"]["pass_count"],
            "W1_v1_checks_total":
                pre_p3["mutants"]["W1"]["pre_v1_production"]["checks_total"],
            "W1_v1_fixed_address_qc":
                pre_p3["mutants"]["W1"]["pre_fixed_address_qc"]["verdict"],
            "W2_v1_gate": pre_p3["mutants"]["W2"]["pre_v1_production"]["gate"],
            "W2_v1_fixed_address_qc":
                pre_p3["mutants"]["W2"]["pre_fixed_address_qc"]["verdict"],
            "W2_note": "the RECORD_ID-only mutant is NOT caught by the "
                       "fixed-address QC comparison (the callsite is still "
                       "canonical) — only the new identity gate catches it",
            "W3_v1_gate": pre_p3["mutants"]["W3"]["pre_v1_production"]["gate"]},
        "clean_scratch_copy_v2": p3["clean_scratch_copy_v2"]["post_v2_production"],
        "regression_verdict": None}
    all_ok = (regression["clean_baseline_v2"]["historical_80"]["all_pass"]
              and regression["clean_baseline_v2"]["historical_80"]["count"] == 80
              and len(regression["clean_baseline_v2"]["recw_old_6"]["ids"]) == 6
              and regression["clean_baseline_v2"]["recw_old_6"]["pass_count"] == 6
              and regression["clean_baseline_v2"]["new_identity_check"]["verdict"] == "PASS"
              and baseline["gate"] == "PASS"
              and all(m["fails_exactly_on_proper_anchor"]
                      for m in controls["mc1_to_mc6"][:5])
              and controls["mc1_to_mc6"][5]["observed_gate"] == "PASS"
              and all(g["pass"] for g in controls["w_record_mutation_gates"])
              and all(p3_gate_summary(k)["verdict"] == "PASS"
                      for k in ("W1", "W2", "W3"))
              and all(table_identity["v2_vs_hist"].values())
              and all(table_identity["v2_vs_src"].values())
              and not regression["duplicate_required_ids"])
    regression_final["regression_verdict"] = "PASS" if all_ok else "FAIL"
    wjson(os.path.join(PKG_ROOT, "REGRESSION_RESULTS.json"), regression_final)

    identities["exe_after_post"] = {
        "size": os.path.getsize(EXE_PATH), "sha256": sha256_file(EXE_PATH),
        "unchanged": sha256_file(EXE_PATH) == EXE_SHA256}
    wjson(os.path.join(post_dir, f"POST_{stamp}_RUN_HEADER.json"), identities)

    index = {"phase": "POST", "stamp": stamp, "files": {}}
    for fn in sorted(os.listdir(post_dir)):
        p = os.path.join(post_dir, fn)
        if os.path.isfile(p):
            index["files"][fn] = {"size": os.path.getsize(p),
                                  "sha256": sha256_file(p)}
    for fn in sorted(os.listdir(scratch_dir)):
        p = os.path.join(scratch_dir, fn)
        index["files"]["scratch/" + fn] = {
            "size": os.path.getsize(p), "sha256": sha256_file(p)}
    index["note"] = "this index is written LAST in the POST raws; it does " \
                    "not hash itself"
    wjson(os.path.join(post_dir, f"POST_{stamp}_SHA256_INDEX.json"), index)

    print("POST phase complete (stamp", stamp + ")")
    print("  v2 clean baseline:", baseline["pass_count"], "/",
          baseline["checks_total"], "gate", baseline["gate"])
    print("  regression verdict:", regression_final["regression_verdict"])
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True, choices=("PRE", "POST"))
    args = ap.parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if args.phase == "PRE":
        return run_pre(stamp)
    return run_post(stamp)


if __name__ == "__main__":
    sys.exit(main())
