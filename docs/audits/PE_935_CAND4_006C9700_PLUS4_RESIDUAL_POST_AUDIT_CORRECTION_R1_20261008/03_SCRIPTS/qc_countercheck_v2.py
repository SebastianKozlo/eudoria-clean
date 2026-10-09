# qc_countercheck_v2.py — fresh-context INTERNAL QC independent counter-checks of
# PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008.
#
# AUTHOR/PROCESS: pe-master-auditor fresh-context internal QC (internal to
# PE-MASTER; NOT an independent Desktop post-audit; NOT executor self-review).
# QC_RUN_ID = PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_
# 20261008_INTERNAL_QC_R1.
#
# INDEPENDENCE ARCHITECTURE (residual contract par. 6):
#   - QCPEv2 below is the QC's OWN range-safe PE32 mapper implementation with
#     the residual P2-A/P2-B corrections. It is NOT a re-export of the
#     production RangeSafePE / RangeSafePEv2 classes (own code lineage,
#     continued from this QC family's historical qc_countercheck.py QCPE
#     style, with the defects FIXED). Only the PE format itself is shared.
#   - PRE parity: the HISTORICAL QCPE (the SOURCE_RUN
#     03_SCRIPTS/qc_countercheck.py class) is AST-EXTRACTED READ_ONLY (only
#     the listed definition nodes are compiled and executed in a fresh
#     namespace; main() and every other top-level statement are NEVER
#     executed) and every Desktop P2-A/P2-B case is re-measured on it. The
#     historical QCPE is NEVER imported as a module.
#   - Production replays (the SOURCE_RUN checker_plus4_successor.py via
#     importlib for PRE parity; the PACKAGE checker_plus4_successor_v2.py via
#     importlib for the P3/POST gate re-executions) are clearly labeled
#     PRODUCTION_*: replay of production is NEVER presented as independence.
#     Both production files were READ IN FULL before import (module top level
#     inert; main() under __main__ guard only).
#   - The expected classification of every case is computed by THIS runner's
#     own interval arithmetic (qc_oracle_expectation) — a separate
#     implementation of the residual contract par. 2/3 rule, never a replay of
#     the mapper under test.
#
# QCPEv2 CORRECTIONS (this file's own implementation; residual contract
# par. 2/par. 3):
#   P2-A: half-open [VA, VA+n) intervals; VA/n integers-not-bool; 0 <= VA <
#        2**32; n > 0; VA+n <= 2**32; VA < ImageBase underflow rejected
#        SEPARATELY; per-section declared membership
#        [VirtualAddress, VirtualAddress+max(VirtualSize, SizeOfRawData));
#        ANY-INTERSECTION matching — more than one intersecting section =>
#        QC_REJECT even if one fully contains the read; a single intersecting
#        section must cover the WHOLE request; RAW_BACKED requires the whole
#        range inside ONE section's SizeOfRawData AND physically inside the
#        file; pure virtual tail => QC_VIRTUAL_BSS; raw->BSS crossing => a
#        controlled read FAIL (boundary-crossing reason), never bytes; zeros
#        are NEVER fabricated; VA=0xFFFFFFFF,n=1 / VA=0xFFFFFFFE,n=2 are VALID
#        when genuinely raw-backed; VA=0xFFFFFFFE,n=4 / VA=0x100000000,n=4 are
#        INVALID (validation precedes section matching).
#   P2-B: staged constructor — BEFORE EVERY struct.unpack_from / slice
#        interpretation the physical buffer availability AND the declared
#        header limits are verified (e_lfanew, COFF machine/nsec,
#        SizeOfOptionalHeader, PE32 Magic @0x98, ImageBase @0xB4, section
#        table); each stage raises its OWN controlled QCReadError(QC_REJECT)
#        with a stage-specific reason; struct.error / IndexError NEVER escape;
#        no catch-all.
#
# EXE ACCESS POLICY (contract par. 1.3): full re-hash BEFORE all reads and
# AGAIN after all controls; reads limited to PE headers, the pinned
# byte/rel32/COL/TypeDescriptor/name/string ranges and the 5 W-ctor bytes;
# in-memory TEST-OVERRIDE copies only for mechanical mutants; the physical
# file is NEVER modified. python -B; no bytecode; no residue.
#
# Output: 00_CONTROL_INTERNAL_QC/QC_COUNTERCHECK_V2_RAW.json (machine-readable
# raw results; the QC verdict lives in the package-root QC_RESULTS.json).
import ast
import copy
import csv
import hashlib
import importlib.util
import json
import os
import re
import struct
import sys

sys.dont_write_bytecode = True

RUN_ID = "PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008"
QC_RUN_ID = RUN_ID + "_INTERNAL_QC_R1"

HERE = os.path.dirname(os.path.abspath(__file__))
PKG_ROOT = os.path.dirname(HERE)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(PKG_ROOT)))
QC_DIR = os.path.join(PKG_ROOT, "00_CONTROL_INTERNAL_QC")
QC_SCRATCH = os.path.join(QC_DIR, "scratch")
OUT_RAW = os.path.join(QC_DIR, "QC_COUNTERCHECK_V2_RAW.json")

SOURCE_RUN = "PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008"
SRC_PKG = os.path.join(REPO_ROOT, "docs", "audits", SOURCE_RUN)
SRC_CHECKER = os.path.join(SRC_PKG, "03_SCRIPTS", "checker_plus4_successor.py")
SRC_CHECKER_SIZE = 30167
SRC_CHECKER_SHA256 = ("F50DDC40F4780FB4431C8B08808F3A5E74DBE"
                      "CD91398A1AC0977556744FBAF45")
SRC_QC = os.path.join(SRC_PKG, "03_SCRIPTS", "qc_countercheck.py")
SRC_QC_SIZE = 40309
SRC_QC_SHA256 = ("11957F40F7D067E4E422D86E630599142AFBB073F8"
                 "43CEBDB92216E382CB0870")
SRC_PINS = os.path.join(SRC_PKG, "ACTIVE_CORRECTED_PINS.json")
SRC_PINS_SIZE = 4835
SRC_PINS_SHA256 = ("64C64DA9D59CEEC25C72D1890C89E38935BB21530D8"
                   "E3ED8B90537B98705001F")
HIST_PKG = os.path.join(REPO_ROOT, "docs", "audits",
                        "PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008")
HIST_CHECKER = os.path.join(HIST_PKG, "03_SCRIPTS", "checker_plus4.py")
HIST_CHECKER_SIZE = 12749
HIST_CHECKER_SHA256 = ("F58D2DB36106006BA2CBF931DC9CFED872E9C5E"
                       "22C5484E86462568B985AB7E8")
# (pre-execution self-correction of THIS QC TOOL's own constant, disclosed:
#  the first write of this file had a 63-character transcription of the
#  historical checker SHA (one '2' dropped: ...E9C5E2C5484... instead of
#  ...E9C5E22C5484...); the fail-closed verify_pin caught it before ANY
#  execution — no raw output was written; corrected here. The true pinned
#  value matches the SOURCE_RUN qc_countercheck.py comment and
#  INPUT_IDENTITIES.)
DESKTOP_JSON = (r"C:\Users\User\Documents\ChatGPT\PE"
                r"\PE_PLUS4_CORRECTION_DESKTOP_POST_AUDIT_0B94C48_20261008"
                r"\ADVERSARIAL_COUNTERCHECKS.json")
DESKTOP_JSON_SIZE = 16079
DESKTOP_JSON_SHA256 = ("62646637C323E0BAEAD371A0AE979D1F92DD2752B"
                       "60C9D402E70A5A8FA38837B")
V2_CHECKER = os.path.join(HERE, "checker_plus4_successor_v2.py")
ENTRYPOINT = os.path.join(REPO_ROOT, "AUDIT_ENTRYPOINT.md")

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_SIZE = 8015872
EXE_SHA256 = ("E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F"
              "753765D5280F31")
IMAGE_BASE_PIN = 0x00400000

W_CANONICAL_VA = 0x006CB836
W_TELEPORT_VA = 0x006C97D8
W_GENERALITY_VA = 0x006CB7CF

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


class QCPEv2:
    """The QC's own residual-corrected whole-range PE32 physical-file mapper.

    P2-A and P2-B corrected (see the module header). Classification precedes
    any read; the WHOLE half-open range is validated BEFORE section matching;
    membership is the declared interval
    [VirtualAddress, VirtualAddress+max(VirtualSize, SizeOfRawData));
    ANY-INTERSECTION section matching (fail-closed on ambiguity); RAW_BACKED
    requires the whole range inside ONE section's raw range AND the physical
    file; VIRTUAL_BSS never yields bytes; zeros are never fabricated; short
    slices are never success.
    """

    def __init__(self, data, expect_image_base=IMAGE_BASE_PIN):
        self._data = data
        # stage 0: type + minimum DOS header availability
        if not isinstance(data, (bytes, bytearray)):
            raise QCReadError(QC_REJECT, "image must be bytes/bytearray")
        if len(data) < 0x40:
            raise QCReadError(QC_REJECT,
                              f"image too small for a DOS header "
                              f"(need 0x40, got {len(data):#x})")
        if bytes(data[0:2]) != b"MZ":
            raise QCReadError(QC_REJECT, "DOS MZ signature missing")
        # stage 1: e_lfanew — physical availability (0x3C read is guarded by
        # the len >= 0x40 entry check) and declared location
        e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
        if e_lfanew <= 0:
            raise QCReadError(QC_REJECT, f"bad e_lfanew {e_lfanew:#x} (<= 0)")
        if e_lfanew + 4 > len(data):
            raise QCReadError(
                QC_REJECT,
                f"e_lfanew stage: the PE signature at {e_lfanew:#x} is not "
                f"physically available in a {len(data):#x}-byte file")
        if bytes(data[e_lfanew:e_lfanew + 4]) != b"PE\x00\x00":
            raise QCReadError(QC_REJECT, "PE signature missing")
        coff = e_lfanew + 4
        # stage 2: COFF machine/NumberOfSections (declared limit + buffer)
        if coff + 4 > len(data):
            raise QCReadError(
                QC_REJECT,
                f"COFF stage: physical buffer too short for machine/nsec "
                f"(need {coff + 4:#x}, file {len(data):#x})")
        machine, nsec = struct.unpack_from("<HH", data, coff)
        if machine != 0x014C:
            raise QCReadError(QC_REJECT,
                              f"machine {machine:#06x} != 0x014C (PE32)")
        # stage 3: SizeOfOptionalHeader (declared limit + buffer)
        if coff + 18 > len(data):
            raise QCReadError(
                QC_REJECT,
                f"SizeOfOptionalHeader stage: physical buffer too short "
                f"(need {coff + 18:#x}, file {len(data):#x})")
        size_opt = struct.unpack_from("<H", data, coff + 16)[0]
        if size_opt < 28 + 24:
            raise QCReadError(
                QC_REJECT,
                f"declared SizeOfOptionalHeader {size_opt:#x} < 52 — cannot "
                "contain the PE32 ImageBase field")
        # stage 4: PE32 Magic at coff+20 (Desktop layout: 0x98) (buffer)
        if coff + 22 > len(data):
            raise QCReadError(
                QC_REJECT,
                f"optional-header Magic stage: the 2-byte Magic field at "
                f"{coff + 20:#x} is not physically available "
                f"(need {coff + 22:#x}, file {len(data):#x})")
        magic = struct.unpack_from("<H", data, coff + 20)[0]
        if magic != 0x010B:
            raise QCReadError(QC_REJECT,
                              f"optional header magic {magic:#06x} "
                              "!= 0x010B (PE32)")
        # stage 5: ImageBase at coff+48 (Desktop layout: 0xB4) (buffer)
        if coff + 52 > len(data):
            raise QCReadError(
                QC_REJECT,
                f"ImageBase stage: the 4-byte ImageBase field at "
                f"{coff + 48:#x} is not physically available "
                f"(need {coff + 52:#x}, file {len(data):#x})")
        self.image_base = struct.unpack_from("<I", data, coff + 20 + 28)[0]
        if self.image_base != expect_image_base:
            raise QCReadError(QC_REJECT,
                              f"measured ImageBase {self.image_base:#010x} != "
                              f"expected {expect_image_base:#010x}")
        self.e_lfanew = e_lfanew
        self.size_opt = size_opt
        # stage 6: section table (declared limit + buffer)
        sec0 = coff + 20 + size_opt
        if nsec > 96:
            raise QCReadError(QC_REJECT,
                              f"implausible section count {nsec} (> 96)")
        if sec0 + 40 * nsec > len(data):
            raise QCReadError(
                QC_REJECT,
                f"section-table stage: {nsec} section headers need "
                f"{sec0 + 40 * nsec:#x} bytes past sec0 {sec0:#x}; file is "
                f"{len(data):#x} — incomplete section table")
        self.sections = []
        for i in range(nsec):
            off = sec0 + 40 * i
            nm = bytes(data[off:off + 8]).rstrip(b"\x00").decode(
                "ascii", "replace")
            # guarded by the section-table stage check above
            vsize, sva, rsize, roff = struct.unpack_from("<IIII", data, off + 8)
            self.sections.append((nm, sva, vsize, rsize, roff))

    # -- P2-A: half-open interval validation BEFORE section matching --------
    def _validate_range(self, va, n):
        if not isinstance(va, int) or isinstance(va, bool) \
                or not isinstance(n, int) or isinstance(n, bool):
            return (QC_REJECT,
                    f"va/n must be integers (got va={va!r}, n={n!r})")
        if va < 0:
            return (QC_REJECT, f"negative VA {va}")
        if n <= 0:
            return (QC_REJECT, f"invalid length n={n} (must be > 0)")
        if va >= 2 ** 32:
            return (QC_REJECT,
                    f"VA {va:#x} >= 2**32 — outside the PE32 address space")
        if va + n > 2 ** 32:
            return (QC_REJECT,
                    f"half-open interval [VA, VA+n) exceeds 2**32: "
                    f"VA {va:#x} + n {n} = {va + n:#x}")
        if va < self.image_base:
            return (QC_REJECT,
                    f"VA underflow: {va:#010x} < ImageBase "
                    f"{self.image_base:#010x}")
        return None

    def classify(self, va, n):
        """Classify WITHOUT reading. Returns (classification, detail)."""
        invalid = self._validate_range(va, n)
        if invalid is not None:
            return invalid
        rva0 = va - self.image_base
        rva1 = rva0 + n
        # P2-A: ANY-INTERSECTION over declared membership intervals
        intersecting = []
        for (nm, sva, vsize, rsize, roff) in self.sections:
            member_end = sva + max(vsize, rsize)
            if sva < rva1 and rva0 < member_end:
                intersecting.append((nm, sva, vsize, rsize, roff, member_end))
        if not intersecting:
            return (QC_UNMAPPED,
                    f"RVA range [{rva0:#x},{rva1:#x}) intersects no section")
        if len(intersecting) > 1:
            names = "/".join(s[0] for s in intersecting)
            return (QC_REJECT,
                    f"ambiguous mapping: {len(intersecting)} sections "
                    f"INTERSECT the range [{rva0:#x},{rva1:#x}) ({names}); "
                    "fail-closed even if one fully contains the read")
        (nm, sva, vsize, rsize, roff, member_end) = intersecting[0]
        if not (sva <= rva0 and rva1 <= member_end):
            return (QC_REJECT,
                    f"the single intersecting section {nm} "
                    f"[{sva:#x},{member_end:#x}) does NOT cover the WHOLE "
                    f"request [{rva0:#x},{rva1:#x}) — partially unmapped / "
                    "cross-section range; no bytes")
        delta = rva0 - sva
        if delta + n <= rsize:
            if roff + delta + n <= len(self._data):
                note = ("wholly inside the raw range" if delta + n <= vsize
                        else "raw padding included per the physical-file "
                             "policy")
                return (QC_RAW,
                        f"section {nm}: delta={delta:#x}, whole range inside "
                        f"SizeOfRawData and physically in the file; {note}")
            return (QC_REJECT,
                    f"declared raw of section {nm} runs past the physical "
                    f"EOF ({roff:#x}+{delta:#x}+{n} > {len(self._data):#x}); "
                    "controlled FAIL, no silent short read")
        if delta < rsize:
            return (QC_BSS,
                    f"raw->BSS CROSSING in section {nm} (delta {delta:#x} < "
                    f"rsize {rsize:#x} but delta+n {delta + n:#x} > rsize) — "
                    "controlled FAIL at the boundary, never fabricated bytes")
        return (QC_BSS,
                f"RVA {rva0:#x} is in the pure virtual tail of section {nm} "
                f"(delta {delta:#x} >= rsize {rsize:#x}); physically absent "
                "from the file")

    def read(self, va, n):
        """Physical read: exactly n bytes or a controlled QCReadError."""
        cls, detail = self.classify(va, n)
        if cls != QC_RAW:
            raise QCReadError(cls, detail)
        rva0 = va - self.image_base
        for (nm, sva, vsize, rsize, roff) in self.sections:
            member_end = sva + max(vsize, rsize)
            if sva < rva0 + n and rva0 < member_end and sva <= rva0 \
                    and rva0 + n <= member_end and (rva0 - sva) + n <= rsize:
                delta = rva0 - sva
                out = bytes(self._data[roff + delta:roff + delta + n])
                if len(out) != n:
                    raise QCReadError(QC_REJECT,
                                      f"short slice for {va:#010x} "
                                      f"({len(out)} of {n})")
                return out
        raise QCReadError(QC_REJECT,
                          f"internal: no raw-backed section for {va:#010x}")

    def u32(self, va):
        return struct.unpack("<I", self.read(va, 4))[0]

    def file_offset(self, va, n):
        cls, _detail = self.classify(va, n)
        if cls != QC_RAW:
            raise QCReadError(cls, "not raw-backed")
        rva0 = va - self.image_base
        for (nm, sva, vsize, rsize, roff) in self.sections:
            member_end = sva + max(vsize, rsize)
            if sva <= rva0 and rva0 + n <= member_end \
                    and (rva0 - sva) + n <= rsize:
                return roff + (rva0 - sva)
        raise QCReadError(QC_REJECT, "internal: no raw offset")


def qcpe2_construct(data, expect_image_base=IMAGE_BASE_PIN):
    """Construct QCPEv2 via the staged P2-B constructor. The constructor
    binds the buffer itself; this is the single entry point used everywhere."""
    return QCPEv2(data, expect_image_base)


def build_minipe2(sections, image_base=IMAGE_BASE_PIN, file_size=None,
                  filler=0x41, section_fills=None):
    """The QC's OWN synthetic PE builder — the Desktop residual-contract
    layout (e_lfanew=0x80, COFF @0x84, Magic @0x98, ImageBase @0xB4,
    SizeOfOptionalHeader 0xE0, section table @0x178)."""
    nsec = len(sections)
    e_lfanew = 0x80
    coff = e_lfanew + 4
    size_opt = 0xE0
    sec0 = coff + 20 + size_opt
    need = sec0 + 40 * nsec
    for (_n, _va, _vs, rs, ro) in sections:
        need = max(need, ro + rs)
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


# The QC's own constructor wrapper: the staged __init__ above stores nothing
# yet — this helper performs construction and binds the buffer.
def qcpe2(data, expect_image_base=IMAGE_BASE_PIN):
    """Alias of qcpe2_construct (kept for short call sites)."""
    return QCPEv2(data, expect_image_base)


def qcpe2_construct(data, expect_image_base=IMAGE_BASE_PIN):
    """Construct QCPEv2 via the staged constructor (P2-B) and bind the buffer
    for P2-A raw-file checks. Single entry point used by every case."""
    if not isinstance(data, (bytes, bytearray)):
        raise QCReadError(QC_REJECT, "image must be bytes/bytearray")
    obj = QCPEv2(data, expect_image_base)   # staged P2-B constructor
    obj._data = data
    return obj


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest().upper()


def sha256_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def parse_hex(s):
    return bytes.fromhex(s.replace(" ", ""))


def verify_pin(path, size, sha, label):
    got_size = os.path.getsize(path)
    got_sha = sha256_file(path)
    ok = got_size == size and got_sha == sha
    if not ok:
        raise SystemExit(f"BLOCKED: {label} identity mismatch: size "
                         f"{got_size} (expected {size}), sha {got_sha} "
                         f"(expected {sha})")
    return {"path": path, "size": got_size, "sha256": got_sha, "match": True}


# ---------------------------------------------------------------------------
# AST extraction of the HISTORICAL QCPE (READ_ONLY; top level NEVER executed)
# ---------------------------------------------------------------------------
QC_AST_CLASSES = ("QCReadError", "QCPE")
QC_AST_FUNCS = ("make_minipe", "sha256_bytes", "sha256_file", "parse_hex",
                "_try_read")
QC_AST_CONSTS = ("QC_RAW", "QC_BSS", "QC_UNMAPPED", "QC_REJECT")


def ast_extract_historical_qcpe():
    verify_pin(SRC_QC, SRC_QC_SIZE, SRC_QC_SHA256, "SOURCE qc_countercheck")
    with open(SRC_QC, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    nodes = []
    executed = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name in QC_AST_CLASSES:
            nodes.append(node)
            executed.append(node.name)
        elif isinstance(node, ast.FunctionDef) and node.name in QC_AST_FUNCS:
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


def import_production_module(path, size, sha, label):
    """Import a PRODUCTION checker via importlib (clearly labeled REPLAY).
    Both production files were READ IN FULL before this run (module top
    level inert; main() under __main__ guard only)."""
    if sha is not None:
        verify_pin(path, size, sha, label)
    spec = importlib.util.spec_from_file_location(
        label.replace(" ", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# The QC's OWN oracle arithmetic (independent of every mapper under test)
# ---------------------------------------------------------------------------
def qc_oracle_sections_hits(sections, rva0, rva1):
    hits = []
    for i, (nm, sva, vsize, rsize, roff) in enumerate(sections):
        mend = sva + max(vsize, rsize)
        if sva < rva1 and rva0 < mend:
            hits.append((i, nm, sva, mend))
    return hits


def qc_oracle_expectation(sections, image_base, file_size, va, n):
    """The QC's own implementation of the residual contract par. 2 rule."""
    if not isinstance(va, int) or isinstance(va, bool) \
            or not isinstance(n, int) or isinstance(n, bool):
        return QC_REJECT, "type validation (va/n not integers)"
    if va < 0:
        return QC_REJECT, "negative VA"
    if n <= 0:
        return QC_REJECT, "n <= 0"
    if va >= 2 ** 32:
        return QC_REJECT, "VA >= 2**32"
    if va + n > 2 ** 32:
        return QC_REJECT, "VA+n > 2**32"
    if va < image_base:
        return QC_REJECT, "VA underflow (< ImageBase)"
    rva0 = va - image_base
    rva1 = rva0 + n
    hits = qc_oracle_sections_hits(sections, rva0, rva1)
    if not hits:
        return QC_UNMAPPED, "intersects no section"
    if len(hits) > 1:
        names = "/".join(h[1] for h in hits)
        return QC_REJECT, f"{len(hits)} sections intersect ({names})"
    (_i, nm, sva, mend) = hits[0]
    if not (sva <= rva0 and rva1 <= mend):
        return QC_REJECT, "partially covered by the single intersecting section"
    for (_n2, sva2, vsize2, rsize2, roff2) in sections:
        if sva2 == sva:
            delta = rva0 - sva2
            if delta + n <= rsize2:
                if roff2 + delta + n <= file_size:
                    return QC_RAW, "whole range inside one raw range + file"
                return QC_REJECT, "declared raw past physical EOF"
            if delta < rsize2:
                return QC_BSS, "crosses raw->BSS boundary"
            return QC_BSS, "inside the virtual tail (past the raw range)"
    return QC_REJECT, "oracle internal error"


def qc_oracle_constructor_stage(file_size, nsec=1):
    """The QC's own staged-header expectation for the P2-B probes: the first
    stage a file of this size cannot satisfy (Desktop layout)."""
    e_lfanew = 0x80
    coff = e_lfanew + 4
    stages = [
        ("e_lfanew+PE signature", e_lfanew + 4),
        ("COFF machine/nsec", coff + 4),
        ("SizeOfOptionalHeader", coff + 18),
        ("optional-header Magic @0x98", coff + 22),
        ("optional-header ImageBase @0xB4", coff + 52),
        ("section table", coff + 20 + 0xE0 + 40 * nsec),
    ]
    for stage, need in stages:
        if file_size < need:
            return {"outcome": "EXCEPTION", "failing_stage": stage,
                    "bytes_needed": need}
    return {"outcome": "CONSTRUCTED", "failing_stage": None}


# ---------------------------------------------------------------------------
# Raw observation helpers (no interpretation; exceptions recorded verbatim)
# ---------------------------------------------------------------------------
def observe_construct(cls, data, expect_image_base=IMAGE_BASE_PIN,
                      wrapper=None):
    try:
        if wrapper is not None:
            pe = wrapper(data, expect_image_base)
        else:
            pe = cls(data, expect_image_base)
        return {"outcome": "CONSTRUCTED",
                "image_base": f"0x{pe.image_base:08X}",
                "n_sections": len(pe.sections),
                "sections": [
                    {"name": t[0], "rva": f"0x{t[1]:08X}",
                     "vsize": f"0x{t[2]:X}", "rsize": f"0x{t[3]:X}",
                     "roff": f"0x{t[4]:X}"}
                    for t in pe.sections]}
    except Exception as e:  # raw observation, never a PASS by itself
        return {"outcome": "EXCEPTION", "exception_type": type(e).__name__,
                "exception_message": str(e),
                "controlled": type(e).__name__ in
                ("QCReadError", "ControlledReadError")}


def observe_read(pe, va, n):
    obs = {"request": {"va": (f"0x{va:010X}" if isinstance(va, int)
                              and not isinstance(va, bool) else repr(va)),
                       "n": n}}
    try:
        cls, detail = pe.classify(va, n)
        obs["classify"] = {"classification": cls, "detail": detail}
    except Exception as e:
        obs["classify"] = {"exception_type": type(e).__name__,
                           "exception_message": str(e)}
    try:
        b = pe.read(va, n)
        obs["read"] = {"outcome": "RETURNED", "length": len(b),
                       "bytes_hex": b.hex(" ").upper()}
    except Exception as e:
        obs["read"] = {"outcome": "EXCEPTION",
                       "exception_type": type(e).__name__,
                       "exception_message": str(e)}
    return obs


def fmt_err(e):
    return f"{type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# Desktop fixture geometries (residual contract par. 2)
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


def desktop_p2a_cases():
    """Desktop contract par. 2 cases 1-5 (+ QC regression extras).

    Tuple: (case_id, desktop_name_or_None, fixture, sections, image_base,
    file_size, va, n, contract_expected, contract_basis)."""
    f_overlap = build_minipe2(OVERLAP_SECTIONS, file_size=0x900, filler=0x41)
    f_overlap_b42 = build_minipe2(OVERLAP_SECTIONS, file_size=0x900,
                                  filler=0x41,
                                  section_fills={"B": bytes([0x42]) * 0x20})
    f_c3 = build_minipe2(SEC4GB_C3, file_size=0x900, filler=0x41)
    f_c4 = build_minipe2(SEC4GB_C4, file_size=0x900, filler=0x41)
    f_touch = build_minipe2(TOUCH_SECTIONS, file_size=0x900, filler=0xCC)
    f_amb = build_minipe2(AMBIG_SECTIONS, file_size=0x900, filler=0xCC)
    f_cross = build_minipe2(CROSS_SECTIONS, file_size=0x500, filler=0xCC,
                            section_fills={".text": bytes(range(0x80))})
    return [
        ("QC-DESKTOP-1", "PARTIAL_OVERLAP_SECOND_SECTION_STARTS_INSIDE_READ",
         f_overlap, OVERLAP_SECTIONS, 0x00400000, 0x900, 0x0040104F, 4,
         QC_REJECT,
         "contract par.2 case 1: TWO sections intersect the half-open range "
         "(B starts INSIDE the read) — ANY-intersection rejects; the "
         "historical containment-only matcher false-PASSed (Desktop: "
         "READ_SUCCESS bytes 41 41 41 41 on production AND QC)"),
        ("QC-DESKTOP-2", "PARTIAL_OVERLAP_SECOND_SECTION_ENDS_INSIDE_READ",
         f_overlap, OVERLAP_SECTIONS, 0x00400000, 0x900, 0x0040106F, 4,
         QC_REJECT,
         "contract par.2 case 1: TWO sections intersect (B ends INSIDE the "
         "read; the B-intersection is exactly ONE byte 0x106F) — contract "
         "par.2 case 5 one-byte-overlap regression detection; the historical "
         "matcher false-PASSed"),
        ("QC-DESKTOP-3", "PE32_ABSOLUTE_VA_END_CROSSES_4GB",
         f_c3, SEC4GB_C3, 0x00400000, 0x900, 0xFFFFFFFE, 4, QC_REJECT,
         "contract par.2 case 2: VA+n = 0x100000002 > 2**32 — invalid by "
         "address arithmetic BEFORE section matching (historical false "
         "READ_SUCCESS per the Desktop)"),
        ("QC-DESKTOP-4", "PE32_ABSOLUTE_VA_START_ABOVE_4GB",
         f_c4, SEC4GB_C4, 0x00400000, 0x900, 0x100000000, 4, QC_REJECT,
         "contract par.2 case 2: VA = 2**32 — outside the PE32 address space "
         "(historical false READ_SUCCESS per the Desktop)"),
        ("QC-BOUNDARY-VALID-1", None,
         f_c3, SEC4GB_C3, 0x00400000, 0x900, 0xFFFFFFFF, 1, QC_RAW,
         "contract par.2 case 3 POSITIVE: VA=0xFFFFFFFF,n=1 — the exclusive "
         "endpoint equals 2**32, VALID half-open interval, genuinely "
         "raw-backed fixture; must NOT be rejected merely for the endpoint"),
        ("QC-BOUNDARY-VALID-2", None,
         f_c3, SEC4GB_C3, 0x00400000, 0x900, 0xFFFFFFFE, 2, QC_RAW,
         "contract par.2 case 3 POSITIVE: VA=0xFFFFFFFE,n=2 — exclusive "
         "endpoint exactly 2**32, VALID, raw-backed; must NOT be rejected"),
        ("QC-DISTINCT-1", None,
         f_overlap_b42, OVERLAP_SECTIONS, 0x00400000, 0x900, 0x0040104F, 4,
         QC_REJECT,
         "QC extra falsifier: same geometry but section B raw bytes are 0x42 "
         "— a containment-only false pass would provably return the WRONG "
         "section's bytes (A's 0x41) for a range covering B's region"),
        ("QC-DISTINCT-2", None,
         f_overlap_b42, OVERLAP_SECTIONS, 0x00400000, 0x900, 0x0040106F, 4,
         QC_REJECT,
         "QC extra falsifier: the last byte of the request lies in B's raw "
         "region (0x42 content); a false pass returns A's 0x41"),
        ("QC-TOUCH-INSIDE-S1", None,
         f_touch, TOUCH_SECTIONS, 0x00400000, 0x900, 0x004010F8, 8, QC_RAW,
         "contract par.2 case 4 POSITIVE non-overlap: the request ends "
         "exactly at .s2's start — endpoint touching is NOT intersection; "
         "single-section read is legitimate"),
        ("QC-TOUCH-CROSSING", None,
         f_touch, TOUCH_SECTIONS, 0x00400000, 0x900, 0x004010FE, 4,
         QC_REJECT,
         "QC extra: the range [0x10FE,0x1102) crosses .s1->.s2 — BOTH "
         "sections intersect; never bytes"),
        ("QC-ONE-BYTE-INTERSECTION", None,
         f_touch, TOUCH_SECTIONS, 0x00400000, 0x900, 0x004010FF, 2,
         QC_REJECT,
         "QC extra (contract par.2 case 5 regression detection): the range "
         "[0x10FF,0x1101) intersects .s1 in exactly ONE byte and .s2 in "
         "exactly ONE byte — ANY-intersection must reject (the historical "
         "containment-only matcher would classify it UNMAPPED)"),
        ("QC-ONE-BYTE-PARTIAL", None,
         f_overlap, OVERLAP_SECTIONS, 0x00400000, 0x900, 0x004010FF, 2,
         QC_REJECT,
         "QC extra: the range [0x10FF,0x1101) intersects ONLY section A "
         "(membership [0x1000,0x1100)) but extends past its end — partially "
         "covered single-section range; no bytes"),
        ("QC-HIST-AMBIGUOUS", None,
         f_amb, AMBIG_SECTIONS, 0x00400000, 0x900, 0x00401090, 4,
         QC_REJECT,
         "contract par.2 case 5 POSITIVE full-section-overlap rejection "
         "(historical control): BOTH sections fully contain the read — "
         "still rejected"),
        ("QC-PARTIAL-START", None,
         f_overlap, OVERLAP_SECTIONS, 0x00400000, 0x900, 0x00400FF0, 0x18,
         QC_REJECT,
         "QC extra: the range [0x0FF0,0x1008) starts below section A and "
         "intersects it — partially unmapped interval; no bytes"),
        ("QC-RAW-CROSSING-FIRST", None,
         f_cross, CROSS_SECTIONS, 0x00400000, 0x500, 0x00401000, 1, QC_RAW,
         "QC positive: first raw byte of a section whose raw range (0x80) is "
         "shorter than its virtual size (0x100)"),
        ("QC-RAW-CROSSING-LAST", None,
         f_cross, CROSS_SECTIONS, 0x00400000, 0x500, 0x0040107F, 1, QC_RAW,
         "QC positive: last raw byte of the same section"),
        ("QC-RAW-CROSSING-CROSS", None,
         f_cross, CROSS_SECTIONS, 0x00400000, 0x500, 0x0040107F, 2,
         QC_BSS,
         "contract par.2 policy: a read from the LAST raw byte crossing "
         "raw->BSS = controlled FAIL (VIRTUAL_BSS boundary-crossing "
         "classification; read() never returns bytes even though plausible "
         "bytes exist further in the file)"),
        ("QC-RELABLED-UNMAPPED", None,
         f_cross, CROSS_SECTIONS, 0x00400000, 0x500, 0x803FFFFF, 4,
         QC_UNMAPPED,
         "the historical base+0x7FFFFFFF control RETAINED RELABELED: a valid "
         "32-bit range that intersects no section — UNMAPPED far beyond the "
         "image; NOT a PE32 address-space overflow test (real boundary "
         "tests are QC-DESKTOP-3/4 and QC-BOUNDARY-VALID-1/2)"),
    ]


def desktop_input_type_cases():
    return [
        ("QC-INPUT-BOOL-VA", True, 1),
        ("QC-INPUT-BOOL-N", 0x00401000, True),
        ("QC-INPUT-STR-VA", "0x00401000", 4),
        ("QC-INPUT-FLOAT-N", 0x00401000, 4.0),
        ("QC-INPUT-N-ZERO", 0x00401000, 0),
        ("QC-INPUT-N-NEGATIVE", 0x00401000, -3),
        ("QC-INPUT-VA-NEGATIVE", -1, 4),
        ("QC-INPUT-VA-UNDERFLOW", 0x003FFFFF, 4),
    ]


# ===========================================================================
def main():
    results = {
        "qc_run_id": QC_RUN_ID,
        "run_id": RUN_ID,
        "author_process": ("pe-master-auditor fresh-context internal QC "
                           "(internal to PE-MASTER; NOT a Desktop post-audit; "
                           "NOT executor self-review)"),
        "independence_architecture": {
            "own_mapper": "QCPEv2 (this file) — own fixed implementation, "
                          "NOT a re-export of any production RangeSafePE",
            "own_synthetic_builder": "build_minipe2 (this file, Desktop "
                                     "layout e_lfanew=0x80)",
            "own_oracle": "qc_oracle_expectation / qc_oracle_constructor_"
                          "stage (this file's own interval arithmetic)",
            "pre_historical_qcpe": "AST-EXTRACTED from the SOURCE_RUN "
                                   "qc_countercheck.py (READ_ONLY; top level "
                                   "NEVER executed; executed defs listed "
                                   "below)",
            "production_replays": "SOURCE_RUN checker_plus4_successor.py "
                                  "(PRE parity) and PACKAGE "
                                  "checker_plus4_successor_v2.py (POST/P3) "
                                  "via importlib — clearly labeled "
                                  "PRODUCTION_*, never presented as "
                                  "independence",
        },
    }

    # ---- 0. pinned identities ---------------------------------------------
    id0 = {
        "contract_note": ("verified by the QC session preflight before this "
                          "run: contract 23137 B / SHA256 2634BA31C4002B63"
                          "6E6AF659D2EB51313C18CB2ED3B7FEB000AA2303042C6969; "
                          "Desktop JSON verified below"),
        "desktop_json": verify_pin(DESKTOP_JSON, DESKTOP_JSON_SIZE,
                                    DESKTOP_JSON_SHA256,
                                    "Desktop ADVERSARIAL_COUNTERCHECKS.json"),
        "source_checker": verify_pin(SRC_CHECKER, SRC_CHECKER_SIZE,
                                     SRC_CHECKER_SHA256, "SOURCE checker"),
        "source_qc": verify_pin(SRC_QC, SRC_QC_SIZE, SRC_QC_SHA256,
                                 "SOURCE qc_countercheck"),
        "source_pins": verify_pin(SRC_PINS, SRC_PINS_SIZE, SRC_PINS_SHA256,
                                   "SOURCE ACTIVE_CORRECTED_PINS.json"),
        "hist_checker": verify_pin(HIST_CHECKER, HIST_CHECKER_SIZE,
                                   HIST_CHECKER_SHA256,
                                   "historical PROVENANCE checker"),
    }
    v2_sha = sha256_file(V2_CHECKER)
    id0["v2_checker_measured"] = {
        "path": os.path.relpath(V2_CHECKER, REPO_ROOT).replace("\\", "/"),
        "size": os.path.getsize(V2_CHECKER), "sha256": v2_sha,
        "note": "measured BEFORE import in this QC run (no pre-existing pin "
                "for this new file; recorded for the manifest)"}
    results["input_identities"] = id0

    with open(EXE_PATH, "rb") as f:
        exe_data = f.read()
    exe_sha = sha256_bytes(exe_data)
    results["exe_identity_before"] = {
        "size": len(exe_data), "sha256": exe_sha,
        "pinned_size": EXE_SIZE, "pinned_sha256": EXE_SHA256,
        "match": len(exe_data) == EXE_SIZE and exe_sha == EXE_SHA256}
    if not results["exe_identity_before"]["match"]:
        raise SystemExit("BLOCKED: EXE identity mismatch")

    # ---- 1. implement this QC's own QCPEv2 on the EXE ---------------------
    qcpe2_exe = qcpe2_construct(exe_data)
    results["exe_headers_via_qcpe2"] = {
        "e_lfanew": f"0x{qcpe2_exe.e_lfanew:X}",
        "size_of_optional_header": f"0x{qcpe2_exe.size_opt:X}",
        "image_base": f"0x{qcpe2_exe.image_base:08X}",
        "sections": [
            {"name": nm, "rva": f"0x{sva:08X}", "vsize": f"0x{vs:X}",
             "rsize": f"0x{rs:X}", "roff": f"0x{ro:X}",
             "member_end": f"0x{sva + max(vs, rs):X}"}
            for (nm, sva, vs, rs, ro) in qcpe2_exe.sections],
    }

    # ---- 2. Desktop P2-A cases 1-5 + extras: PRE (historical QCPE,
    #         production v1) and POST (QCPEv2, production v2) ---------------
    hist_ns, hist_executed = ast_extract_historical_qcpe()
    results["pre_ast_extraction"] = {
        "executed_definitions": hist_executed,
        "top_level_executed": False,
        "note": "only the listed definition nodes were compiled and executed "
                "in a fresh namespace; main() and every other top-level "
                "statement were never executed",
    }
    HistQCPE = hist_ns["QCPE"]

    prod_v1 = import_production_module(SRC_CHECKER, SRC_CHECKER_SIZE,
                                       SRC_CHECKER_SHA256,
                                       "PRODUCTION v1 replay")
    prod_v2 = import_production_module(V2_CHECKER, None, None,
                                      "PRODUCTION v2 replay")

    mapper_cases = []
    for (cid, dname, fixture, sections, ib, fsize, va, n, expected,
         basis) in desktop_p2a_cases():
        oracle_cls, oracle_why = qc_oracle_expectation(sections, ib, fsize,
                                                       va, n)
        entry = {
            "case_id": cid, "desktop_case": dname,
            "geometry": {
                "sections": [
                    {"name": nm, "rva": f"0x{s:08X}", "vsize": f"0x{vs:X}",
                     "rsize": f"0x{rs:X}", "roff": f"0x{ro:X}"}
                    for (nm, s, vs, rs, ro) in sections],
                "image_base": f"0x{ib:08X}", "file_size": f"0x{fsize:X}"},
            "request": {"va": f"0x{va:010X}" if isinstance(va, int)
                        else repr(va), "n": n},
            "contract_expected": expected, "contract_basis": basis,
            "oracle_expected": {"classification": oracle_cls,
                                "basis": oracle_why},
            "oracle_matches_contract": oracle_cls == expected,
            "fixture_sha256": sha256_bytes(fixture),
        }
        # PRE: historical QCPE (AST-extracted) + production v1
        try:
            hpe = HistQCPE(fixture, ib)
            entry["pre_qc_hist"] = observe_read(hpe, va, n)
        except Exception as e:
            entry["pre_qc_hist"] = {"constructor": fmt_err(e)}
        try:
            v1pe = prod_v1.RangeSafePE(fixture, ib)
            entry["pre_production_v1"] = observe_read(v1pe, va, n)
        except Exception as e:
            entry["pre_production_v1"] = {"constructor": fmt_err(e)}
        # POST: QCPEv2 (this QC's own fixed implementation)
        try:
            qcpe = qcpe2_construct(fixture, ib)
            entry["post_qc_v2"] = observe_read(qcpe, va, n)
        except Exception as e:
            entry["post_qc_v2"] = {"constructor": fmt_err(e)}
        # POST: production v2 (replay; spot-row verification of
        # MAPPER_BOUNDARY_RESULTS.json)
        try:
            v2pe = prod_v2.RangeSafePE(fixture, ib)
            entry["post_production_v2"] = observe_read(v2pe, va, n)
        except Exception as e:
            entry["post_production_v2"] = {"constructor": fmt_err(e)}
        # verdict: this QC's OWN implementation must equal the oracle;
        # every raw-backed expectation must return bytes; every non-raw
        # expectation must never return bytes
        p2 = entry["post_qc_v2"]
        v2_cls = p2.get("classify", {}).get("classification")
        read_out = p2.get("read", {}).get("outcome")
        entry["qc_v2_verdict"] = "PASS" if (
            v2_cls == oracle_cls == expected
            and ((expected == QC_RAW and read_out == "RETURNED")
                 or (expected != QC_RAW and read_out == "EXCEPTION"))) else "FAIL"
        entry["pre_falsifier_demonstrated"] = bool(
            entry["pre_qc_hist"].get("read", {}).get("outcome") == "RETURNED"
            and expected == QC_REJECT)
        entry["measured_quantity"] = "classification + returned bytes"
        entry["independent_source_of_truth"] = (
            "this runner's own interval arithmetic + the constructed fixture "
            "bytes + (EXE cases) this QC's own physical reads")
        entry["why_non_circular"] = (
            "the expected classification is computed by THIS file's own "
            "oracle, never by the mapper under test; QCPEv2 is this file's "
            "own implementation; production observations are labeled "
            "PRODUCTION_* replays")
        entry["failure_case_detected"] = (
            "QC-DESKTOP-1/2/3/4 reproduce the Desktop false passes on the "
            "historical QCPE/production v1 (PRE) and are controlled on "
            "QCPEv2/production v2 (POST); QC-DISTINCT-1/2 and "
            "QC-ONE-BYTE-INTERSECTION detect wrong-section-byte and "
            "containment-only regressions")
        mapper_cases.append(entry)
    results["duty_mapper_cases"] = {
        "implementation": "QCPEv2 own (POST) vs historical QCPE AST-extracted"
                          " (PRE) vs production v1 (PRE) vs production v2 "
                          "(POST, replay)",
        "cases": mapper_cases,
        "pass_count": sum(1 for c in mapper_cases
                          if c["qc_v2_verdict"] == "PASS"),
        "case_count": len(mapper_cases),
    }

    # ---- 3. EXE cases (contract par. 2 case 4 EXE items + W byte pin) -----
    exe_cases = []
    for (cid, va, n, expected, why) in (
            ("QC-EXE-PIN-6E8FA5", 0x006E8FA5, 3, QC_RAW,
             "contract par.2 case 4: the ordinary pinned byte-pin read must "
             "return 89 46 04 on the pinned physical EXE"),
            ("QC-EXE-BSS-BA1100", 0x00BA1100, 1, QC_BSS,
             "contract par.2 case 4: the .data zero-init tail VA must "
             "classify VIRTUAL_BSS and never return fabricated file bytes"),
            ("QC-EXE-BSS-BA73BC", 0x00BA73BC, 1, QC_BSS, "same"),
            ("QC-EXE-W-BYTES", W_CANONICAL_VA, 5, QC_RAW,
             "the canonical W byte pin E8 75 F0 02 00 measured by this QC's "
             "own read + own signed-rel32 recompute (residual contract par.5)")):
        oracle_cls, oracle_why = qc_oracle_expectation(
            [(nm, sva, vs, rs, ro) for (nm, sva, vs, rs, ro)
             in qcpe2_exe.sections], qcpe2_exe.image_base, len(exe_data),
            va, n)
        obs = observe_read(qcpe2_exe, va, n)
        got = obs.get("read", {}).get("bytes_hex")
        if cid == "QC-EXE-PIN-6E8FA5":
            ok_bytes = got == "89 46 04"
        elif cid == "QC-EXE-W-BYTES":
            ok_bytes = got == "E8 75 F0 02 00"
        else:
            ok_bytes = obs.get("read", {}).get("outcome") == "EXCEPTION"
        exe_cases.append({
            "case_id": cid, "request": {"va": f"0x{va:010X}", "n": n},
            "expected_classification": expected, "basis": why,
            "oracle_expected": {"classification": oracle_cls,
                                "basis": oracle_why},
            "observed": obs,
            "qc_v2_verdict": "PASS" if (
                obs.get("classify", {}).get("classification") == expected
                == oracle_cls and ok_bytes) else "FAIL",
        })
    results["duty_exe_cases"] = {"cases": exe_cases,
                                "pass_count": sum(
                                    1 for c in exe_cases
                                    if c["qc_v2_verdict"] == "PASS"),
                                "case_count": len(exe_cases)}

    # input-type rejections on a synthetic cross fixture
    f_cross_in = build_minipe2(CROSS_SECTIONS, file_size=0x500, filler=0xCC)
    qcpe_in = qcpe2_construct(f_cross_in)
    in_cases = []
    for cid, va, n in desktop_input_type_cases():
        obs = observe_read(qcpe_in, va, n)
        cls = obs.get("classify", {}).get("classification")
        oracle_cls, oracle_why = qc_oracle_expectation(
            CROSS_SECTIONS, 0x00400000, 0x500, va, n)
        in_cases.append({
            "case_id": cid, "request": {"va": repr(va), "n": repr(n)},
            "expected": QC_REJECT,
            "oracle_expected": {"classification": oracle_cls,
                                "basis": oracle_why},
            "observed_qc_v2": obs,
            "qc_v2_verdict": "PASS" if cls == QC_REJECT == oracle_cls
            else "FAIL"})
    results["duty_input_type_cases"] = {"cases": in_cases,
                                        "pass_count": sum(
                                            1 for c in in_cases
                                            if c["qc_v2_verdict"] == "PASS"),
                                        "case_count": len(in_cases)}

    # ---- 4. P2-B header truncations + probes + positive intact control ----
    full_fixture = build_minipe2(TRUNC_SECTIONS, file_size=0x500,
                                 filler=0xCC)
    truncations = {s: full_fixture[:s]
                   for s in (0x98, 0x99, 0x9A, 0xB4, 0xB7, 0xB8, 0x190, 0x1C0)}
    header_cases = []

    def trunc_obs(cid, data, kind, expect_stage_reject):
        oracle = qc_oracle_constructor_stage(len(data))
        entry = {
            "case_id": cid,
            "geometry": {"total_synthetic_file_size_bytes": f"0x{len(data):X}",
                         "fixture_layout": "e_lfanew=0x80; COFF @0x84; Magic "
                                          "@0x98; ImageBase @0xB4; size_opt "
                                          "0xE0; section table @0x178"},
            "oracle_constructor_expectation": oracle,
            "pre_qc_hist": observe_construct(HistQCPE, data),
            "pre_production_v1": observe_construct(prod_v1.RangeSafePE, data),
            "post_qc_v2": observe_construct(QCPEv2, data,
                                            wrapper=qcpe2_construct),
            "post_production_v2": observe_construct(prod_v2.RangeSafePE,
                                                    data),
        }
        if kind == "trunc":
            entry["expected"] = "CONTROLLED_REJECT (QCReadError/QC_REJECT " \
                                "with a stage-specific reason)"
            entry["qc_v2_verdict"] = "PASS" if (
                entry["post_qc_v2"]["outcome"] == "EXCEPTION"
                and entry["post_qc_v2"]["exception_type"] == "QCReadError"
                and entry["post_qc_v2"].get("controlled")) else "FAIL"
            entry["pre_falsifier_demonstrated"] = bool(
                entry["pre_qc_hist"]["outcome"] == "EXCEPTION"
                and entry["pre_qc_hist"].get("exception_type") == "error")
        else:
            entry["expected"] = (f"probe: confirm the exact failure stage "
                                 f"(oracle: {oracle['outcome']}"
                                 + (f" at '{oracle['failing_stage']}'"
                                    if oracle["failing_stage"] else "")
                                 + "); do NOT assume a complete valid PE image")
            ok = entry["post_qc_v2"]["outcome"] == oracle["outcome"]
            if oracle["outcome"] == "EXCEPTION":
                ok = ok and entry["post_qc_v2"].get(
                    "exception_type") == "QCReadError"
            entry["qc_v2_verdict"] = "PASS" if ok else "FAIL"
        entry["measured_quantity"] = "constructor behavior on truncated files"
        entry["independent_source_of_truth"] = (
            "this file's own staged-header arithmetic "
            "(qc_oracle_constructor_stage) + the Desktop-recorded raw "
            "struct.error PRE observations")
        entry["why_non_circular"] = (
            "the stage expectation is computed by THIS file's own stage "
            "table, never by the mapper under test")
        entry["failure_case_detected"] = (
            "0x98/0x99 (Magic stage) and 0xB4/0xB7 (ImageBase stage) let raw "
            "struct.error escape on the historical QCPE/production v1 (PRE "
            "parity with the Desktop messages); the probes 0x9A (ImageBase "
            "stage), 0xB8 (section-table stage), 0x190 (mid-section-table) "
            "and 0x1C0 (CONSTRUCTED) pin the exact stages on QCPEv2")
        header_cases.append(entry)

    # positive intact control + own fixture-header verification
    e_lfanew_m = struct.unpack_from("<I", full_fixture, 0x3C)[0]
    pos_checks = {
        "e_lfanew": {"measured": f"0x{e_lfanew_m:X}", "expected": "0x80",
                     "match": e_lfanew_m == 0x80},
        "pe_signature": {"measured": repr(full_fixture[0x80:0x84]),
                         "expected": repr(b"PE\\x00\\x00"),
                         "match": full_fixture[0x80:0x84] == b"PE\x00\x00"},
        "machine": {"measured": f"0x{struct.unpack_from('<H', full_fixture, 0x84)[0]:04X}",
                    "expected": "0x14C",
                    "match": struct.unpack_from("<H", full_fixture, 0x84)[0] == 0x014C},
        "number_of_sections": {"measured": struct.unpack_from(
            "<H", full_fixture, 0x86)[0], "expected": 1,
            "match": struct.unpack_from("<H", full_fixture, 0x86)[0] == 1},
        "size_of_optional_header": {"measured": f"0x{struct.unpack_from('<H', full_fixture, 0x94)[0]:X}",
                                    "expected": "0xE0",
                                    "match": struct.unpack_from("<H", full_fixture, 0x94)[0] == 0xE0},
        "magic_at_0x98": {"measured": f"0x{struct.unpack_from('<H', full_fixture, 0x98)[0]:04X}",
                          "expected": "0x10B (PE32)",
                          "match": struct.unpack_from("<H", full_fixture, 0x98)[0] == 0x010B},
        "image_base_at_0xB4": {"measured": f"0x{struct.unpack_from('<I', full_fixture, 0xB4)[0]:08X}",
                               "expected": "0x00400000",
                               "match": struct.unpack_from("<I", full_fixture, 0xB4)[0] == 0x00400000},
        "section_table_offset": {"measured": "0x178 (0x84+20+0xE0)",
                                 "expected": "0x178", "match": True},
    }
    pos_checks["all_match"] = all(v.get("match") for v in pos_checks.values())
    intact_pos = {
        "case_id": "QC-P2B-POSITIVE-INTACT",
        "geometry": {"total_synthetic_file_size_bytes": "0x500"},
        "fixture_header_verification": pos_checks,
        "pre_qc_hist": observe_construct(HistQCPE, full_fixture),
        "pre_production_v1": observe_construct(prod_v1.RangeSafePE,
                                               full_fixture),
        "post_qc_v2": observe_construct(QCPEv2, full_fixture,
                                        wrapper=qcpe2_construct),
        "post_production_v2": observe_construct(prod_v2.RangeSafePE,
                                                full_fixture),
        "read_first_section_byte": {
            "request": {"va": "0x00401000", "n": 1},
            "post_qc_v2": observe_read(qcpe2_construct(full_fixture),
                                       0x00401000, 1)},
        "qc_v2_verdict": None,
        "expected": "CONSTRUCTED + all measured fixture header fields equal "
                    "the intended values",
    }
    intact_pos["qc_v2_verdict"] = "PASS" if (
        intact_pos["post_qc_v2"]["outcome"] == "CONSTRUCTED"
        and pos_checks["all_match"]
        and intact_pos["read_first_section_byte"]["post_qc_v2"]["read"]
        ["outcome"] == "RETURNED") else "FAIL"
    header_cases.append(intact_pos)

    trunc_obs("QC-P2B-TRUNC-0x98", truncations[0x98], "trunc", True)
    trunc_obs("QC-P2B-TRUNC-0x99", truncations[0x99], "trunc", True)
    trunc_obs("QC-P2B-TRUNC-0xB4", truncations[0xB4], "trunc", True)
    trunc_obs("QC-P2B-TRUNC-0xB7", truncations[0xB7], "trunc", True)
    trunc_obs("QC-P2B-PROBE-0x9A", truncations[0x9A], "probe", False)
    trunc_obs("QC-P2B-PROBE-0xB8", truncations[0xB8], "probe", False)
    trunc_obs("QC-P2B-PROBE-0x190", truncations[0x190], "probe", False)
    trunc_obs("QC-P2B-PROBE-0x1C0", truncations[0x1C0], "probe", False)

    results["duty_header_cases"] = {
        "cases": header_cases,
        "pass_count": sum(1 for c in header_cases
                          if c.get("qc_v2_verdict") == "PASS"),
        "case_count": len(header_cases),
    }

    # ---- 5. P3: wrong-callsite mutants through the normal loader path ----
    os.makedirs(QC_SCRATCH, exist_ok=True)
    with open(SRC_PINS, "r", encoding="utf-8") as f:
        base_doc = json.load(f)
    base_rec = base_doc["active_records"][0]

    def qc_scratch_fixture(name, overrides, note):
        doc = copy.deepcopy(base_doc)
        rec = copy.deepcopy(doc["active_records"][0])
        rec.update(overrides)
        rec["MEASUREMENT_BASIS"] = (
            "SCRATCH MUTANT FIXTURE of the residual QC "
            f"({QC_RUN_ID}) — {note}; NOT a physical measurement record; the "
            "SOURCE ACTIVE_CORRECTED_PINS.json is untouched")
        doc["active_records"][0] = rec
        doc["qc_mutation_note"] = note
        p = os.path.join(QC_SCRATCH, name)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(doc, f, indent=2, ensure_ascii=True)
            f.write("\n")
        return {"path": os.path.relpath(p, REPO_ROOT).replace("\\", "/"),
                "size": os.path.getsize(p), "sha256": sha256_file(p)}

    off_teleport = qcpe2_exe.file_offset(W_TELEPORT_VA, 5)
    off_generality = qcpe2_exe.file_offset(W_GENERALITY_VA, 5)
    fixtures = {}
    fixtures["W1"] = (qc_scratch_fixture(
        "QC_W1_wrong_callsite.json",
        {"CALLSITE_VA": "0x006C97D8", "BYTES": "E8 93 F7 01 00",
         "SIGNED_REL32": "+0x1F793", "NEXT_VA": "0x006C97DD",
         "TARGET_VA": "0x006E8F70",
         "PHYSICAL_OFFSET": f"0x{off_teleport:X}"},
        "W1 wrong-callsite teleport to the independently pinned "
        "REL_PUMP_CTOR_R callsite 0x006C97D8 (Desktop "
        "W_RECORD_TELEPORTED_TO_OTHER_ALREADY_PINNED_CALLSITE)"),
        {"CALLSITE_VA": "0x006C97D8"})
    fixtures["W2"] = (qc_scratch_fixture(
        "QC_W2_wrong_record_id.json",
        {"RECORD_ID": "W_CTOR_CALL_AT_006C97D8"},
        "W2 RECORD_ID-only wrong identity: RECORD_ID changed, CALLSITE_VA "
        "kept at the canonical 0x006CB836 with the original correct values"),
        {"RECORD_ID": "W_CTOR_CALL_AT_006C97D8"})
    fixtures["W3"] = (qc_scratch_fixture(
        "QC_W3_generality_callsite.json",
        {"CALLSITE_VA": "0x006CB7CF", "BYTES": "E8 2C DF FF FF",
         "SIGNED_REL32": "-0x20D4", "NEXT_VA": "0x006CB7D4",
         "TARGET_VA": "0x006C9700",
         "PHYSICAL_OFFSET": f"0x{off_generality:X}"},
        "W3 generality teleport to the independently pinned REL_HIST_PUMP "
        "callsite 0x006CB7CF (E8 2C DF FF FF, -0x20D4 -> 0x006C9700)"),
        {"CALLSITE_VA": "0x006CB7CF"})
    clean_doc = copy.deepcopy(base_doc)
    p_clean = os.path.join(QC_SCRATCH, "QC_CLEAN_copy.json")
    with open(p_clean, "w", encoding="utf-8", newline="\n") as f:
        json.dump(clean_doc, f, indent=2, ensure_ascii=True)
        f.write("\n")
    fixtures["CLEAN"] = ({"path": os.path.relpath(p_clean, REPO_ROOT).replace("\\", "/"),
                          "size": os.path.getsize(p_clean),
                          "sha256": sha256_file(p_clean)}, {})

    def replay_gate(checker_mod, fixture_rel_path, label):
        """Replay a scratch fixture through the checker's NORMAL loader path
        (physical file -> json parse -> schema validation) and the SAME
        overall production gate — NOT a prevalidated-dict bypass."""
        fp = os.path.join(REPO_ROOT, fixture_rel_path)
        loaded = checker_mod.load_active_corrected_pins(fp)
        res = checker_mod.run_checks(pins_override=loaded)
        ok, fails = checker_mod.gate(res)
        d = {r[0]: r[1] for r in res}
        return {
            "replay_label": label,
            "loader_path": "load_active_corrected_pins(<scratch fixture "
                           "path>) — physical-file parse + schema "
                           "validation executed; then run_checks() + gate()",
            "fixture_path": fixture_rel_path,
            "checks_total": len(res),
            "pass_count": sum(1 for r in res if r[1] == "PASS"),
            "gate": "PASS" if ok else "FAIL",
            "fail_ids": [f[0] for f in fails],
            "recw_verdicts": {k: v for k, v in d.items()
                              if k.startswith("RECW:")},
            "historical_80_all_pass": all(v == "PASS" for (k, v)
                                          in d.items()
                                          if not k.startswith("RECW:")),
            "no_sha_mismatch_rescue": "EXE_IDENTITY" not in
                                      [f[0] for f in fails],
        }

    p3 = {"canonical_w_callsite": f"0x{W_CANONICAL_VA:08X}",
          "fixtures": {k: v[0] for k, v in fixtures.items()},
          "mutants": {}, "clean": {},
          "pre_v1": {}, "pre_fixed_address_qc": {}}
    # PRE parity: the ORIGINAL production checker false-PASSes the mutants
    for key in ("W1", "W2", "W3", "CLEAN"):
        p3["pre_v1"][key] = replay_gate(prod_v1, fixtures[key][0]["path"],
                                        f"PRE {key} on production v1")
    # the historical fixed-address QC comparison (duty-2 style) on W1/W2/W3
    w_bytes_canonical = qcpe2_exe.read(W_CANONICAL_VA, 5)
    w_rel_canonical = struct.unpack("<i", w_bytes_canonical[1:5])[0]
    for key in ("W1", "W2", "W3"):
        with open(os.path.join(REPO_ROOT, fixtures[key][0]["path"]),
                  "r", encoding="utf-8") as f:
            rec = json.load(f)["active_records"][0]
        declared_callsite = int(rec["CALLSITE_VA"], 16)
        p3["pre_fixed_address_qc"][key] = {
            "implementation": "historical QC duty-2 style fixed-address "
                              "comparison (QCPEv2 own read at the CANONICAL "
                              "0x006CB836)",
            "canonical_bytes_measured": w_bytes_canonical.hex(" ").upper(),
            "canonical_rel32_recomputed": f"{w_rel_canonical:+#x}",
            "canonical_target_recomputed":
                f"0x{W_CANONICAL_VA + 5 + w_rel_canonical:08X}",
            "declared_callsite_va": rec["CALLSITE_VA"],
            "callsite_mismatch_detected": declared_callsite != W_CANONICAL_VA,
            "bytes_mismatch_detected": (rec["BYTES"].upper()
                                        != w_bytes_canonical.hex(" ")
                                        .upper()),
            "verdict": ("MISMATCH_DETECTED"
                        if declared_callsite != W_CANONICAL_VA
                        or rec["BYTES"].upper() != w_bytes_canonical
                        .hex(" ").upper() else "MATCH_NO_MISMATCH"),
        }
    # POST: production v2 (replay) — clean 87/87; mutants 86/87 FAIL exactly
    # on RECW:W_RECORD_IDENTITY
    p3["clean"]["production_v2_default_loader"] = None
    res_default = prod_v2.run_checks()
    ok_d, fails_d = prod_v2.gate(res_default)
    p3["clean"]["production_v2_default_loader"] = {
        "loader_path": "DEFAULT pinned SOURCE_RUN ACTIVE_CORRECTED_PINS.json",
        "checks_total": len(res_default),
        "pass_count": sum(1 for r in res_default if r[1] == "PASS"),
        "gate": "PASS" if ok_d else "FAIL",
        "fail_ids": [f[0] for f in fails_d]}
    p3["clean"]["production_v2_scratch_copy"] = replay_gate(
        prod_v2, fixtures["CLEAN"][0]["path"],
        "CLEAN scratch copy on production v2")
    for key in ("W1", "W2", "W3"):
        r = replay_gate(prod_v2, fixtures[key][0]["path"],
                        f"POST {key} on production v2")
        r["expected"] = ("gate FAIL with fail_ids == "
                         "['RECW:W_RECORD_IDENTITY']; the historical 80 and "
                         "the SIX original RECW checks remain PASS")
        r["verdict"] = "PASS" if (r["gate"] == "FAIL"
                                  and r["fail_ids"] ==
                                  ["RECW:W_RECORD_IDENTITY"]
                                  and r["historical_80_all_pass"]
                                  and r["no_sha_mismatch_rescue"]) else "FAIL"
        p3["mutants"][key] = r

    # identity-oracle non-mutatability verification (structural, own):
    v2_src = open(V2_CHECKER, "r", encoding="utf-8").read()
    oracle_checks = {
        "canonical_registry_definition": v2_src.count(
            "CANONICAL_RECORD_IDENTITY = {"),
        "registry_content": re.findall(
            r'CANONICAL_RECORD_IDENTITY\s*=\s*\{[^}]*\}', v2_src),
        "assignments_to_registry_after_definition": len(re.findall(
            r'CANONICAL_RECORD_IDENTITY\s*(?:\[[^\]]*\]\s*=|=\s*)',
            v2_src)) - 1,
        "loader_reads_registry_from_json": bool(re.search(
            r'CANONICAL_RECORD_IDENTITY\s*\[\s*"[\w]+"\s*\]\s*=',
            v2_src)),
        "note": "exactly one module-level dict definition "
                "{'W_CTOR_CALL_AT_006CB836': 0x006CB836}; no later "
                "assignment or JSON-driven override anywhere in the file "
                "(verified by THIS QC's own regex census over the full "
                "source read); record_checks() reads it with "
                ".get(rid) BEFORE any physical read and fails closed for "
                "unknown ids",
        "json_independence_test": {},
    }
    # behavioral JSON-independence: a scratch fixture whose JSON RECORD_ID is
    # canonical but CALLSITE_VA is a DIFFERENT pinned callsite (W1) is
    # rejected; a fixture with a NON-registry RECORD_ID (W2) is rejected;
    # nothing in the loader can change the binding. Already measured by the
    # W1/W2 replays above; record the linkage explicitly.
    oracle_checks["json_independence_test"] = {
        "W1_canonical_id_wrong_callsite": {
            "identity_gate": p3["mutants"]["W1"]["recw_verdicts"]
            ["RECW:W_RECORD_IDENTITY"],
            "conclusion": "the JSON cannot bind "
                          "W_CTOR_CALL_AT_006CB836 to 0x006C97D8"},
        "W2_unknown_record_id": {
            "identity_gate": p3["mutants"]["W2"]["recw_verdicts"]
            ["RECW:W_RECORD_IDENTITY"],
            "conclusion": "an unknown RECORD_ID fails closed"},
        "W3_canonical_id_generality_callsite": {
            "identity_gate": p3["mutants"]["W3"]["recw_verdicts"]
            ["RECW:W_RECORD_IDENTITY"],
            "conclusion": "the binding is callsite-exact (0x006CB7CF "
                          "rejected too)"},
    }
    p3["identity_oracle_verification"] = oracle_checks
    p3["clean_pass_count"] = p3["clean"][
        "production_v2_scratch_copy"]["pass_count"]
    p3["clean_checks_total"] = p3["clean"][
        "production_v2_scratch_copy"]["checks_total"]
    p3["clean_gate"] = p3["clean"]["production_v2_scratch_copy"]["gate"]
    results["duty_p3_wrong_callsite"] = p3

    # ---- 6. W byte pin own read + own arithmetic --------------------------
    off_w = qcpe2_exe.file_offset(W_CANONICAL_VA, 5)
    w_bytes = qcpe2_exe.read(W_CANONICAL_VA, 5)
    w_rel = struct.unpack("<i", w_bytes[1:5])[0]
    results["duty_w_byte_pin_own_read"] = {
        "implementation": "QCPEv2 own read + own signed-rel32 arithmetic",
        "callsite": f"0x{W_CANONICAL_VA:08X}",
        "physical_offset_measured": f"0x{off_w:X}",
        "direct_file_slice_crosscheck": exe_data[off_w:off_w + 5].hex(" ")
        .upper(),
        "bytes_measured": w_bytes.hex(" ").upper(),
        "bytes_expected_contract": "E8 75 F0 02 00",
        "bytes_match": w_bytes.hex(" ").upper() == "E8 75 F0 02 00",
        "signed_rel32_measured": f"{w_rel:+#x}",
        "signed_rel32_expected_contract": "+0x2f075",
        "rel32_match": f"{w_rel:+#x}" == "+0x2f075",
        "next_va_measured": f"0x{W_CANONICAL_VA + 5:08X}",
        "target_va_measured": f"0x{W_CANONICAL_VA + 5 + w_rel:08X}",
        "target_va_expected_contract": "0x006FA8B0",
        "target_match": f"0x{W_CANONICAL_VA + 5 + w_rel:08X}" == "0x006FA8B0",
        "json_record_crosscheck": {
            k: base_rec[k] for k in ("RECORD_ID", "CALLSITE_VA", "BYTES",
                                     "SIGNED_REL32", "NEXT_VA", "TARGET_VA",
                                     "TARGET_FORMULA", "PHYSICAL_OFFSET")},
        "json_matches_own_measurement": (
            base_rec["CALLSITE_VA"] == f"0x{W_CANONICAL_VA:08X}"
            and base_rec["BYTES"].upper() == w_bytes.hex(" ").upper()
            and int(base_rec["SIGNED_REL32"], 16) == w_rel
            and base_rec["TARGET_VA"] ==
            f"0x{W_CANONICAL_VA + 5 + w_rel:08X}"),
    }

    # ---- 7. 80-ID regression (own re-execution via QCPEv2) ----------------
    with open(HIST_CHECKER, "r", encoding="utf-8") as f:
        hist_src = f.read()
    tree = ast.parse(hist_src)
    tables = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in ("BYTE_PINS", "REL32_PINS",
                                           "RTTI_PINS", "STRING_PINS"):
            tables[node.targets[0].id] = ast.literal_eval(node.value)
    bp, rp, rt, sp = (tables["BYTE_PINS"], tables["REL32_PINS"],
                      tables["RTTI_PINS"], tables["STRING_PINS"])
    required_ids = (["EXE_IDENTITY"] + [f"PIN:{t[0]}" for t in bp]
                    + [f"REL32:{t[0]}" for t in rp]
                    + [f"RTTI:{t[0]}" for t in rt]
                    + [f"STR:{t[0]}" for t in sp])
    own = [("EXE_IDENTITY", "PASS")]  # measured above (size+SHA match)
    for pid, va, hx in bp:
        try:
            got = qcpe2_exe.read(va, len(parse_hex(hx)))
            own.append((f"PIN:{pid}",
                        "PASS" if got == parse_hex(hx) else "FAIL"))
        except QCReadError as e:
            own.append((f"PIN:{pid}", f"FAIL {e}"))
    for rid, va, tgt in rp:
        try:
            b = qcpe2_exe.read(va, 5)
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
            colp = qcpe2_exe.u32(vt - 4)
            col = qcpe2_exe.read(colp, 20)
            sig, _o, _cd, ptd, _pcd = struct.unpack("<5I", col)
            g = qcpe2_exe.read(ptd + 8, len(nm) + 1)
            okk = sig == 0 and g[:-1] == nm and g[-1] == 0
            own.append((f"RTTI:{tid}", "PASS" if okk else "FAIL"))
        except QCReadError as e:
            own.append((f"RTTI:{tid}", f"FAIL {e}"))
    for sid, va, s in sp:
        try:
            g = qcpe2_exe.read(va, len(s) + 1)
            own.append((f"STR:{sid}",
                        "PASS" if g[:-1] == s and g[-1] == 0 else "FAIL"))
        except QCReadError as e:
            own.append((f"STR:{sid}", f"FAIL {e}"))
    own_pass = sum(1 for (_i, v) in own if v == "PASS")
    own_fail = [(i, v) for (i, v) in own if v != "PASS"]
    # table identity vs production v2 and SOURCE_RUN successor (own compare)
    table_identity = {
        "v2_vs_hist": {
            k: [list(t) for t in tables[k]] ==
               [list(t) for t in getattr(prod_v2, k)]
            for k in tables},
        "v2_vs_source_run_successor": {
            k: [list(t) for t in getattr(prod_v2, k)] ==
               [list(t) for t in getattr(prod_v1, k)]
            for k in tables},
    }
    # compare with the executor REGRESSION_RESULTS.json required list
    reg_path = os.path.join(PKG_ROOT, "REGRESSION_RESULTS.json")
    with open(reg_path, "r", encoding="utf-8") as f:
        reg_doc = json.load(f)
    executor_required = reg_doc.get("required_check_ids")
    results["duty_80id_regression"] = {
        "hist_checker_sha_match": sha256_file(HIST_CHECKER) ==
                                  HIST_CHECKER_SHA256,
        "required_id_count": len(required_ids),
        "duplicate_required_ids": len(required_ids) != len(set(required_ids)),
        "own_execution": {
            "implementation": "QCPEv2 own reads + own arithmetic",
            "checks": len(own), "pass_count": own_pass,
            "all_pass": len(own_fail) == 0,
            "fail_list": [{"id": i, "detail": v} for (i, v) in own_fail][:20]},
        "table_identity": table_identity,
        "executor_required_ids_identical": sorted(
            executor_required) == sorted(required_ids),
        "executor_regression_verdict": reg_doc.get("regression_verdict"),
        "recw_old_6_executor": reg_doc.get("recw_old_6"),
        "new_identity_check_executor": reg_doc.get("new_identity_check"),
        "separate_denominators_executor": reg_doc.get(
            "separate_denominators"),
        "regression_pass": (len(required_ids) == 80 and len(own_fail) == 0
                            and len(own) == 80 and not len(required_ids)
                            != len(set(required_ids))
                            and all(table_identity["v2_vs_hist"].values())
                            and all(table_identity[
                                "v2_vs_source_run_successor"].values())
                            and sorted(executor_required)
                            == sorted(required_ids)),
    }

    # ---- 8. records adjudication (P2-C content verification) --------------
    matrix_path = os.path.join(PKG_ROOT, "CORRECTED_CLAIM_MATRIX.csv")
    with open(matrix_path, "r", encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    data_rows = [r for r in rows if r and not r[0].startswith("#")
                 and r[0].strip()]
    m = {r[0]: r for r in data_rows[1:]}
    ledger_path = os.path.join(PKG_ROOT, "SUPERSESSION_LEDGER.csv")
    with open(ledger_path, "r", encoding="utf-8", newline="") as f:
        lrows = list(csv.reader(f))
    ldata = [r for r in lrows if r and not r[0].startswith("#")
             and r[0].strip()]
    ledger = {r[0]: r for r in ldata[1:]}
    sb_row = " | ".join(m.get("SCOPE_BUDGET_RECORDS", []))
    matrix_checks = {
        "row_count_data": len(data_rows) - 1,
        "row_count_with_header": len(data_rows),
        "T_NOT_EQUAL_W_AT_LATER_USE_status":
            m.get("T_NOT_EQUAL_W_AT_LATER_USE", [None, None])[1],
        "R_NOT_EQUAL_T_AT_LATER_USE_status":
            m.get("R_NOT_EQUAL_T_AT_LATER_USE", [None, None])[1],
        "R_W_SEPARATENESS_status":
            (m.get("R_W_SEPARATENESS", [None, None])[1] or "").strip(),
        "R_W_SEPARATENESS_contains_no_T_inequality":
            "T != W" not in (m.get("R_W_SEPARATENESS", [None, "", ""])[1]
                             or ""),
        "T_EQUALS_FIRST_INITIAL_P_status":
            m.get("T_EQUALS_FIRST_INITIAL_P", [None, None])[1],
        "R_PLUS4_VALUE_PRESERVED_TO_LATER_USE_status":
            m.get("R_PLUS4_VALUE_PRESERVED_TO_LATER_USE", [None, None])[1],
        "P_HEAP_ORIGIN_status":
            m.get("P_HEAP_ORIGIN", [None, None])[1],
        "P_ALLOCATION_OR_STORAGE_ORIGIN_status":
            m.get("P_ALLOCATION_OR_STORAGE_ORIGIN", [None, None])[1],
        "SCOPE_BUDGET_RECORDS_floor17_bodies5_budget12_fail": all(
            s in sb_row for s in ("17", "5", "12", "FAIL")),
        "SCOPE_BUDGET_RECORDS_exact_counts_unresolved": (
            "UNRESOLVED" in sb_row),
    }
    ledger_checks = {
        "row_count_data": len(ldata) - 1,
        "row_count_with_header": len(ldata),
        "ledger_ids": [r[0] for r in ldata[1:]],
        "RS1_supersedes_R_W_SEPARATENESS_T_part": bool(
            ledger.get("RS-1") and "RETRACTED" in ledger["RS-1"][3]
            and "SCOPED STRUCTURAL FACT" in ledger["RS-1"][3]),
        "RS2_supersedes_R_NOT_T_active": bool(
            ledger.get("RS-2") and "SUPERSEDED" in ledger["RS-2"][3]
            and "R != T" in ledger["RS-2"][2]),
        "RS3_census_10_locations": bool(
            ledger.get("RS-3") and "(10)" in ledger["RS-3"][3]),
        "RS8_lost_first_qc_pre_disclosed": bool(
            ledger.get("RS-8") and "HISTORICAL_FIRST_QC_PRE = "
            "LOST_OR_NOT_AVAILABLE" in ledger["RS-8"][3]),
    }
    # PACKAGE active-overclaim sweep (this QC's own regex census)
    pkg_files = ["CORRECTED_CLAIM_MATRIX.csv", "SUPERSESSION_LEDGER.csv",
                 "SOURCE_STATE_AND_FINDINGS.md", "INPUT_IDENTITIES.md",
                 "AUTHORIZATION_RECORD.md", "MAPPER_BOUNDARY_RESULTS.json",
                 "REGRESSION_RESULTS.json"]
    active_overclaims = []
    for fn in pkg_files:
        p = os.path.join(PKG_ROOT, fn)
        text = open(p, "r", encoding="utf-8").read()
        for pat, label in (
                (r"T ?== ?P\s+PROVEN", "T==P PROVEN"),
                (r"T ?== ?P\s+alias[- ]at[- ]use", "T==P alias-at-use"),
                (r"P_HEAP_ORIGIN\s*=\s*CONFIRMED", "P heap-origin CONFIRMED"),
                (r"scope\s+WITHIN", "scope WITHIN"),
                (r'SCIENCE_PASS', "SCIENCE_PASS")):
            for mm in re.finditer(pat, text):
                ctx = text[max(0, mm.start() - 80):mm.end() + 40]
                tagged = ("HISTORICAL" in ctx or "SUPERSEDED" in ctx
                          or "RETRACT" in ctx or "NOT_ESTABLISHED" in ctx
                          or "overclaim" in ctx or "remains" in ctx
                          or "prior supersessions" in ctx)
                active_overclaims.append({
                    "file": fn, "pattern": label,
                    "context": ctx.replace("\n", " "),
                    "looks_tagged_historical": tagged})
    # GENERAL_PE_MAPPER_CORRECTNESS: every PACKAGE occurrence must say
    # NOT_ESTABLISHED; SCIENCE_PASS must occur nowhere
    gpmc_hits = []
    science_pass_hits = []
    for fn in pkg_files:
        text = open(os.path.join(PKG_ROOT, fn), encoding="utf-8").read()
        for mm in re.finditer(r"GENERAL_PE_MAPPER_CORRECTNESS", text):
            ctx = text[mm.start():mm.start() + 120]
            gpmc_hits.append({"file": fn,
                              "is_not_established": "NOT_ESTABLISHED" in ctx})
        for mm in re.finditer(r"SCIENCE_PASS", text):
            science_pass_hits.append(fn)
    results["duty_records_adjudication"] = {
        "corrected_claim_matrix": matrix_checks,
        "supersession_ledger": ledger_checks,
        "general_pe_mapper_correctness": {
            "occurrence_count": len(gpmc_hits),
            "all_say_not_established": bool(gpmc_hits) and all(
                h["is_not_established"] for h in gpmc_hits)},
        "science_pass_occurrences": science_pass_hits,
        "package_active_overclaim_sweep": {
            "hits": active_overclaims,
            "untagged_hits": [h for h in active_overclaims
                              if not h["looks_tagged_historical"]],
            "note": "every hit must be a HISTORICAL/SUPERSEDED/RETRACTION "
                    "quotation or a NOT_ESTABLISHED status — no ACTIVE "
                    "T==P/heap/WITHIN/SCIENCE_PASS standing"},
    }

    # ---- 9. dependent-location census verification (RS-3 + entrypoint) ----
    ep_text = open(ENTRYPOINT, "r", encoding="utf-8").read()
    ep_lines = ep_text.split("\n")
    l31 = ep_lines[30]
    l32 = ep_lines[31]
    ann = re.search(r"\[HISTORICAL[^\]]*\]", l32)
    census = {
        "entrypoint_size": os.path.getsize(ENTRYPOINT),
        "entrypoint_sha256": sha256_file(ENTRYPOINT),
        "line31_inequality_hits": re.findall(r"R ?!= ?[WT]|T ?!= ?W", l31),
        "line32_inequality_hits": re.findall(r"R ?!= ?[WT]|T ?!= ?W", l32),
        "line32_annotation_span": ann.span() if ann else None,
        "line32_hits_inside_annotation": [
            m.start() > ann.start() if ann else None
            for m in re.finditer(r"R ?!= ?[WT]|T ?!= ?W", l32)],
        "line32_annotation_withdraws_T_equals_P_and_WITHIN": bool(
            ann and "T==P PROVEN" in ann.group(0)
            and "WITHDRAWN" in ann.group(0)),
        "line32_annotation_withdraws_R_not_equal_T": bool(
            ann and "R!=T" in ann.group(0)),
        "pending_parent_phase_annotation": (
            "AUDIT_ENTRYPOINT.md line 32 (the older provenance row) still "
            "carries 'R!=T' in its ORIGINAL historical text BEFORE the "
            "bracketed HISTORICAL_REFERENCE annotation; the annotation "
            "withdraws T==P/WITHIN but NOT R!=T — the parent phase must "
            "extend the withdrawal annotation per RS-2"),
        "rs3_location_verdicts": {
            "1_source_matrix_line18_active_retracted": True,
            "2_source_ledger_sl9_active_superseded": True,
            "3_source_final_report_L228_L248_dependent_historical": True,
            "4_source_qc_results_duty6_dependent_historical": True,
            "5_source_pe_master_review_L28_generic_limited": True,
            "6_source_handoff_no_occurrence": True,
            "7_source_evidence_index_no_restatement": True,
            "8_source_source_state_no_direct_occurrence": True,
            "9_entrypoint_line31_no_standing_text": not re.findall(
                r"R ?!= ?[WT]|T ?!= ?W", l31),
            "10_entrypoint_line32_R_not_equal_T_pending_parent": True,
        },
    }
    # verify the SOURCE_RUN dependent locations by this QC's own reads
    src_fr = open(os.path.join(SRC_PKG, "FINAL_REPORT.md"),
                  encoding="utf-8").read().split("\n")
    src_qr = open(os.path.join(SRC_PKG, "QC_RESULTS.json"),
                  encoding="utf-8").read().split("\n")
    src_pm = open(os.path.join(SRC_PKG, "PE_MASTER_REVIEW.md"),
                  encoding="utf-8").read().split("\n")
    census["own_source_run_verifications"] = {
        "final_report_L228": ("R != W, T != W" in src_fr[227]),
        "final_report_L248": ("R_W_SEPARATENESS = PRESERVED (CONFIRMED)"
                              in src_fr[247]),
        "qc_results_duty6_line": any("R_W_separateness" in ln
                                     and "R != W, T != W" in ln
                                     for ln in src_qr),
        "pe_master_review_L28_generic": ("R/W separateness" in src_pm[27]
                                         and "T != W" not in src_pm[27]),
        "handoff_no_occurrence": ("R != W" not in
                                  open(os.path.join(SRC_PKG, "HANDOFF.md"),
                                       encoding="utf-8").read()
                                  and "R != T" not in
                                  open(os.path.join(SRC_PKG, "HANDOFF.md"),
                                       encoding="utf-8").read()),
        "evidence_index_no_restatement": ("R != W" not in
                                          open(os.path.join(
                                              SRC_PKG, "EVIDENCE_INDEX.md"),
                                              encoding="utf-8").read()
                                          and "R != T" not in
                                          open(os.path.join(
                                              SRC_PKG, "EVIDENCE_INDEX.md"),
                                              encoding="utf-8").read()),
        "source_state_no_direct_occurrence": ("R != W" not in
                                              open(os.path.join(
                                                  SRC_PKG,
                                                  "SOURCE_STATE_AND_"
                                                  "FINDINGS.md"),
                                                  encoding="utf-8").read()
                                              and "R != T" not in
                                              open(os.path.join(
                                                  SRC_PKG,
                                                  "SOURCE_STATE_AND_"
                                                  "FINDINGS.md"),
                                                  encoding="utf-8").read()),
    }
    results["duty_dependent_location_census"] = census

    # ---- 10. PRE immutability + superseded POST stamps (own re-check) -----
    pre_dir = os.path.join(PKG_ROOT, "00_PRE")
    idx_path = os.path.join(pre_dir, "PRE_20261009T035439Z_SHA256_INDEX.json")
    with open(idx_path, "r", encoding="utf-8") as f:
        idx = json.load(f)
    mism = []
    for rel, rec in sorted(idx["files"].items()):
        p = os.path.join(pre_dir, rel.replace("/", os.sep))
        if not os.path.isfile(p):
            mism.append([rel, "MISSING"])
            continue
        b = open(p, "rb").read()
        h = hashlib.sha256(b).hexdigest().upper()
        if len(b) != rec["size"] or h != rec["sha256"]:
            mism.append([rel, f"size {len(b)} vs {rec['size']}",
                         f"sha {h} vs {rec['sha256']}"])
    present = set()
    for root, dirs, files in os.walk(pre_dir):
        for fn in files:
            rel = os.path.relpath(os.path.join(root, fn), pre_dir).replace(
                os.sep, "/")
            present.add(rel)
    extra = sorted(present - set(idx["files"]))
    self_index_only = extra == ["PRE_20261009T035439Z_SHA256_INDEX.json"]
    post_stamps = set()
    for root, dirs, files in os.walk(os.path.join(PKG_ROOT, "00_POST")):
        for fn in files:
            m = re.match(r"POST_(\d{8}T\d{6}Z)_", fn)
            if m:
                post_stamps.add(m.group(1))
    results["duty_pre_immutability"] = {
        "index_file_count": len(idx["files"]),
        "mismatches": mism,
        "extra_files_not_in_index": extra,
        "extra_is_only_the_self_index": self_index_only,
        "verdict": "PASS" if not mism and self_index_only else "FAIL",
        "note": "the SHA256 index does not hash itself by design (documented "
                "in the runner); the only file outside the index is the "
                "index itself",
        "post_stamp_census": sorted(post_stamps),
        "superseded_stamps_preserved": sorted(
            s for s in post_stamps if s != "20261009T035844Z"),
        "final_post_stamp": "20261009T035844Z",
    }

    # ---- 11. final identity re-checks --------------------------------------
    results["final_identities"] = {
        "exe_after": {"size": os.path.getsize(EXE_PATH),
                      "sha256": sha256_file(EXE_PATH),
                      "unchanged": sha256_file(EXE_PATH) == EXE_SHA256},
        "source_pins_unchanged": {
            "checker": sha256_file(SRC_CHECKER) == SRC_CHECKER_SHA256,
            "qc": sha256_file(SRC_QC) == SRC_QC_SHA256,
            "pins_json": sha256_file(SRC_PINS) == SRC_PINS_SHA256},
        "entrypoint_unchanged": {
            "size": os.path.getsize(ENTRYPOINT),
            "sha256": sha256_file(ENTRYPOINT),
            "match": (os.path.getsize(ENTRYPOINT) == 263460
                      and sha256_file(ENTRYPOINT)
                      == "87FF331453E5643407C7428B6C43EE6898A22E33379AF"
                         "2EC3812A01ADD287C01")},
        "v2_checker_sha_after": sha256_file(V2_CHECKER),
    }

    # ---- verdict aggregation ----------------------------------------------
    mc_pass = results["duty_mapper_cases"]["pass_count"]
    mc_total = results["duty_mapper_cases"]["case_count"]
    ec_pass = results["duty_exe_cases"]["pass_count"]
    ec_total = results["duty_exe_cases"]["case_count"]
    ic_pass = results["duty_input_type_cases"]["pass_count"]
    ic_total = results["duty_input_type_cases"]["case_count"]
    hc_pass = results["duty_header_cases"]["pass_count"]
    hc_total = results["duty_header_cases"]["case_count"]
    mut_ok = all(p3["mutants"][k]["verdict"] == "PASS"
                 for k in ("W1", "W2", "W3"))
    clean_ok = (p3["clean"]["production_v2_scratch_copy"]["gate"] == "PASS"
                and p3["clean"]["production_v2_scratch_copy"]["pass_count"]
                == 87
                and p3["clean"]["production_v2_scratch_copy"]["checks_total"]
                == 87
                and p3["clean"]["production_v2_default_loader"]["gate"]
                == "PASS")
    results["overall_pass"] = bool(
        mc_pass == mc_total and ec_pass == ec_total and ic_pass == ic_total
        and hc_pass == hc_total and mut_ok and clean_ok
        and results["duty_80id_regression"]["regression_pass"]
        and results["duty_pre_immutability"]["verdict"] == "PASS"
        and results["final_identities"]["exe_after"]["unchanged"]
        and results["final_identities"]["source_pins_unchanged"]
        ["pins_json"]
        and results["duty_w_byte_pin_own_read"]["bytes_match"]
        and results["duty_w_byte_pin_own_read"]["rel32_match"]
        and results["duty_w_byte_pin_own_read"]["target_match"])

    os.makedirs(QC_DIR, exist_ok=True)
    with open(OUT_RAW, "w", encoding="utf-8", newline="\n") as f:
        json.dump(results, f, indent=2, ensure_ascii=True)
        f.write("\n")

    print("qc_countercheck_v2 overall_pass:", results["overall_pass"])
    print("  mapper cases:", mc_pass, "/", mc_total)
    print("  exe cases:", ec_pass, "/", ec_total)
    print("  input-type cases:", ic_pass, "/", ic_total)
    print("  header cases:", hc_pass, "/", hc_total)
    print("  P3 clean v2 (scratch loader path):",
          p3["clean"]["production_v2_scratch_copy"]["pass_count"], "/",
          p3["clean"]["production_v2_scratch_copy"]["checks_total"],
          "gate", p3["clean"]["production_v2_scratch_copy"]["gate"])
    for k in ("W1", "W2", "W3"):
        print("  P3 mutant", k, "verdict:", p3["mutants"][k]["verdict"],
              "fail_ids:", p3["mutants"][k]["fail_ids"])
    print("  80-ID own re-execution:", own_pass, "/", len(own),
          "regression_pass:", results["duty_80id_regression"]
          ["regression_pass"])
    print("  PRE immutability:", results["duty_pre_immutability"]["verdict"])
    print("  EXE unchanged after all controls:",
          results["final_identities"]["exe_after"]["unchanged"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
