"""checker_plus4_successor.py — successor production gate of
PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008 (TOOL-MAP + REC-W).

Successor of the historical 03_SCRIPTS/checker_plus4.py of the source package
PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008 (READ_ONLY; NOT repaired in
place). The historical pin lists and the meaning of their mechanical gates are
preserved verbatim (BYTE_PINS/REL32_PINS/RTTI_PINS/STRING_PINS below are the
historical tables; run_correction_controls.py additionally cross-verifies them
element-by-element against the historical file itself). This is NOT a universal
PE/x86 framework: it is a small range-safe physical read layer plus the same
bounded mechanical gate.

TOOL-MAP (contract par. 4): classification is separated from physical read.

    RAW_BACKED                    the whole range is inside one section's raw
                                 (SizeOfRawData) range and inside the physical
                                 file; read() returns exactly n bytes
    VIRTUAL_BSS                  the range is inside the section's virtual
                                 extent (membership may use
                                 max(VirtualSize, SizeOfRawData)) but NOT
                                 wholly inside the raw range (e.g. the .data
                                 zero-init tail); read() raises a controlled
                                 error; zeros are NEVER fabricated as
                                 physical file bytes
    UNMAPPED                     no section contains the whole range (VAs
                                 below the first section — the PE header
                                 region — are UNMAPPED: the suite requires no
                                 header-VA reads)
    REJECTED_INVALID_INPUT       controlled error for a bad range: n <= 0,
                                 non-integer VA/n, VA underflow
                                 (va < ImageBase), a range ambiguously inside
                                 more than one section, or a declared raw
                                 range running past the physical end of the
                                 file (no silent short read)

Raw padding (SizeOfRawData > VirtualSize) may be classified RAW_BACKED per the
explicit PHYSICAL_FILE_MAPPER_POLICY — a policy about the physical file, NEVER
a runtime observation. A read that starts in raw and crosses into the virtual
tail is a controlled FAIL (VIRTUAL_BSS, cross reason). EVERY physical read in
this successor — including the RTTI COL 20-byte read and the
TypeDescriptor/name reads — goes through the same range-safe API.

REC-W (contract par. 3): the RECW:* record gates below validate
ACTIVE_CORRECTED_PINS.json against the physical bytes and this checker's own
arithmetic. The JSON actually drives the gates (no hardcoded byte/displacement/
target constant is used as the expectation); run_correction_controls.py proves
this by flipping each gate with a JSON-only mutation while the physical EXE
stays untouched.

python -B; stdlib only; no bytecode; the physical EXE is never modified
(mechanical-control corruptions are in-memory copies supplied by the caller).
"""
import hashlib
import json
import os
import struct
import sys

sys.dont_write_bytecode = True

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_SIZE = 8015872
EXE_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
IMAGE_BASE_PIN = 0x00400000  # measured ImageBase must equal this pin

PINS_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "..", "ACTIVE_CORRECTED_PINS.json")

RAW_BACKED = "RAW_BACKED"
VIRTUAL_BSS = "VIRTUAL_BSS"
UNMAPPED = "UNMAPPED"
REJECTED_INVALID_INPUT = "REJECTED_INVALID_INPUT"

RAW_PADDING_POLICY = ("PHYSICAL_FILE_MAPPER_POLICY: a range inside "
                      "SizeOfRawData but past VirtualSize is classified "
                      "RAW_BACKED per this explicit physical-file policy; this "
                      "is a statement about the physical FILE, never a "
                      "runtime observation.")


class ControlledReadError(Exception):
    """Controlled read error: classification + reason; never a silent short
    read, never fabricated zeros."""

    def __init__(self, classification, reason):
        self.classification = classification
        self.reason = reason
        super().__init__(f"[{classification}] {reason}")


class RangeSafePE:
    """Range-safe PE32 physical-file mapper.

    Every read checks the WHOLE range, not just the first byte:
      - proper PE32 header (MZ/PE signatures, machine 0x014C, optional-header
        magic 0x010B); measured ImageBase must match the pin; controlled
        errors for an incomplete header or section table;
      - n > 0 and integer VA/n; no VA/RVA underflow (va < ImageBase);
      - an UNAMBIGUOUS section for the whole range (overlapping ambiguous
        mappings are REJECTED, no arbitrary first-section choice);
      - delta = rva - section.VirtualAddress;
      - physical section read requires 0 <= delta AND delta + n <=
        SizeOfRawData AND PointerToRawData + delta + n <= physical file size;
      - returned data has exactly n bytes (a short slice is never success).
    """

    def __init__(self, data, expected_image_base=IMAGE_BASE_PIN):
        self.data = data
        if not isinstance(data, (bytes, bytearray)) or len(data) < 0x40:
            raise ControlledReadError(REJECTED_INVALID_INPUT,
                                      "image too small for a PE header")
        if data[0:2] != b"MZ":
            raise ControlledReadError(REJECTED_INVALID_INPUT,
                                      "DOS MZ signature missing")
        e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
        if e_lfanew <= 0 or e_lfanew + 24 > len(data):
            raise ControlledReadError(REJECTED_INVALID_INPUT,
                                      "incomplete PE header (bad e_lfanew)")
        if bytes(data[e_lfanew:e_lfanew + 4]) != b"PE\x00\x00":
            raise ControlledReadError(REJECTED_INVALID_INPUT,
                                      "PE signature missing")
        coff = e_lfanew + 4
        machine, nsec = struct.unpack_from("<HH", data, coff)
        if machine != 0x014C:
            raise ControlledReadError(REJECTED_INVALID_INPUT,
                                      f"machine {machine:#06x} != 0x014C (PE32)")
        size_opt = struct.unpack_from("<H", data, coff + 16)[0]
        if size_opt < 28 + 24:  # must contain ImageBase (offset 28) and enough
            raise ControlledReadError(REJECTED_INVALID_INPUT,
                                      "incomplete optional header")
        magic = struct.unpack_from("<H", data, coff + 20)[0]
        if magic != 0x010B:
            raise ControlledReadError(REJECTED_INVALID_INPUT,
                                      f"optional header magic {magic:#06x} != 0x010B (PE32)")
        self.image_base = struct.unpack_from("<I", data, coff + 20 + 28)[0]
        if self.image_base != expected_image_base:
            raise ControlledReadError(
                REJECTED_INVALID_INPUT,
                f"measured ImageBase {self.image_base:#010x} != pin "
                f"{expected_image_base:#010x}")
        sec0 = coff + 20 + size_opt
        if sec0 + 40 * nsec > len(data):
            raise ControlledReadError(REJECTED_INVALID_INPUT,
                                      "incomplete section table")
        self.sections = []
        for i in range(nsec):
            off = sec0 + 40 * i
            name = bytes(data[off:off + 8]).rstrip(b"\x00").decode("ascii", "replace")
            vsize, va, rsize, roff = struct.unpack_from("<IIII", data, off + 8)
            self.sections.append((name, va, vsize, roff, rsize))

    def classify(self, va, n):
        """Classify a read of n bytes at va WITHOUT reading. Returns
        (classification, detail). Never fabricates bytes."""
        if not isinstance(va, int) or isinstance(va, bool) \
                or not isinstance(n, int) or isinstance(n, bool):
            return (REJECTED_INVALID_INPUT,
                    "va/n must be integers "
                    f"(got va={va!r}, n={n!r})")
        if va < 0:
            return (REJECTED_INVALID_INPUT, f"negative VA {va}")
        if n <= 0:
            return (REJECTED_INVALID_INPUT, f"invalid length n={n} (must be > 0)")
        if va < self.image_base:
            return (REJECTED_INVALID_INPUT,
                    f"VA underflow: {va:#010x} < ImageBase {self.image_base:#010x}")
        rva = va - self.image_base
        hits = []
        for (name, sva, vsize, roff, rsize) in self.sections:
            member_end = sva + max(vsize, rsize)
            if sva <= rva and rva + n <= member_end:
                hits.append((name, sva, vsize, roff, rsize))
        if len(hits) == 0:
            return (UNMAPPED,
                    f"RVA range {rva:#x}..{rva + n - 1:#x} is inside no section "
                    "(PE-header VAs are UNMAPPED: the suite requires no header read)")
        if len(hits) > 1:
            names = "/".join(h[0] for h in hits)
            return (REJECTED_INVALID_INPUT,
                    f"ambiguous section mapping for RVA range "
                    f"{rva:#x}..{rva + n - 1:#x} (sections {names}); "
                    "no arbitrary first-section choice")
        (name, sva, vsize, roff, rsize) = hits[0]
        delta = rva - sva
        if delta + n <= rsize:
            if roff + delta + n <= len(self.data):
                note = ("raw padding included per " + RAW_PADDING_POLICY
                        if delta + n > vsize else "wholly inside the raw range")
                return (RAW_BACKED,
                        f"section {name}: delta={delta:#x}, raw end "
                        f"{roff + delta + n:#x} <= file size {len(self.data):#x}; {note}")
            return (REJECTED_INVALID_INPUT,
                    f"declared raw range of section {name} runs past the "
                    f"physical end of the file "
                    f"(PointerToRawData {roff:#x} + delta {delta:#x} + n {n} = "
                    f"{roff + delta + n:#x} > file size {len(self.data):#x}); "
                    "controlled FAIL, no silent short read")
        if delta < rsize:
            return (VIRTUAL_BSS,
                    f"read starts in the raw range of section {name} but "
                    f"CROSSES into the virtual tail (delta {delta:#x} < rsize "
                    f"{rsize:#x} but delta+n {delta + n:#x} > rsize); "
                    "controlled FAIL at the raw->BSS boundary")
        return (VIRTUAL_BSS,
                f"RVA {rva:#x} is inside the virtual extent of section {name} "
                f"but past its raw range (delta {delta:#x} >= rsize "
                f"{rsize:#x}); zero-init tail — physically absent from the file")

    def read(self, va, n):
        """Physical read through the range-safe gate: returns exactly n bytes
        or raises ControlledReadError. VIRTUAL_BSS/UNMAPPED/invalid never
        return fabricated bytes."""
        cls, detail = self.classify(va, n)
        if cls != RAW_BACKED:
            raise ControlledReadError(cls, detail)
        rva = va - self.image_base
        for (name, sva, vsize, roff, rsize) in self.sections:
            if sva <= rva and rva + n <= sva + max(vsize, rsize):
                delta = rva - sva
                out = bytes(self.data[roff + delta:roff + delta + n])
                if len(out) != n:
                    raise ControlledReadError(
                        REJECTED_INVALID_INPUT,
                        f"short slice for {va:#010x} (got {len(out)} of {n})")
                return out
        raise ControlledReadError(REJECTED_INVALID_INPUT, "unreachable")

    def raw_offset(self, va, n):
        """The physical file offset for a RAW_BACKED range (same range checks
        as read(); controlled error otherwise). Used by the in-memory
        mechanical-control mutations to locate anchor bytes."""
        cls, detail = self.classify(va, n)
        if cls != RAW_BACKED:
            raise ControlledReadError(cls, detail)
        rva = va - self.image_base
        for (name, sva, vsize, roff, rsize) in self.sections:
            if sva <= rva and rva + n <= sva + max(vsize, rsize):
                return roff + (rva - sva)
        raise ControlledReadError(REJECTED_INVALID_INPUT, "unreachable")

    def u32(self, va):
        return struct.unpack("<I", self.read(va, 4))[0]


def load_pinned():
    """Load the physical EXE and assert its pinned identity (fail-closed)."""
    with open(EXE_PATH, "rb") as f:
        data = f.read()
    if len(data) != EXE_SIZE:
        raise ValueError(f"EXE size {len(data)} != pinned {EXE_SIZE}")
    h = hashlib.sha256(data).hexdigest().upper()
    if h != EXE_SHA256:
        raise ValueError(f"EXE SHA256 {h} != pinned")
    return data


# ---------------------------------------------------------------------------
# HISTORICAL PIN TABLES — preserved verbatim from 03_SCRIPTS/checker_plus4.py
# of the source package (the pin lists and the meaning of the mechanical
# gates are kept; the historical file itself is NOT repaired in place).
# run_correction_controls.py cross-verifies these tables element-by-element
# against the historical file (read-only AST extraction) as part of the
# 80-check-ID regression.
# ---------------------------------------------------------------------------
BYTE_PINS = [
    # body #1: FUN_006C9700
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
    # body #2: FUN_006E8F70 (the ctor of R)
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
    # body #3: FUN_006C9570 (the slot setter)
    ("SETTER_SLOT_CLEAR", 0x006C95A0, "C7 06 00 00 00 00"),
    ("SETTER_RECEIVER_S10", 0x006C95A6, "8B 49 10"),
    ("SETTER_FLAG_CMP", 0x006C95AE, "38 5C 24 28"),
    ("SETTER_FLAG_JNE", 0x006C95BE, "75 71"),
    ("SETTER_SLOT_STORE_P", 0x006C9651, "89 3E"),
    ("SETTER_P_ADDREF", 0x006C9657, "01 5F 04"),
    ("SETTER_TERMINAL_RET8_A", 0x006C962E, "C2 08 00"),
    ("SETTER_TERMINAL_RET8_B", 0x006C966C, "C2 08 00"),
    # body #4 head: FUN_007B79B0
    ("PGET_RECEIVER_SAVE", 0x007B79D4, "8B F9"),
    ("PGET_ALLOC_SIZE_4", 0x007B79D6, "6A 04"),
    # prior-canon re-pins (installer / producer / historical caller)
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

REL32_PINS = [
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

RTTI_PINS = [
    ("RTTI_W_ARKMODELRESOURCEINSTANCEREF", 0x00A864B8, b".?AVArkModelResourceInstanceRef@@"),
    ("RTTI_MANAGER_MAIN", 0x00A855D0, b".?AVArkModelManagerMain@@"),
    ("RTTI_MANAGER_BASE", 0x00A85A08, b".?AVArkModelManager@@"),
]

STRING_PINS = [
    ("STR_GEOWATER0", 0x00A85DA4, b"Geowater:0"),
    ("STR_ARKTEXTURE", 0x00A859F8, b"ArkTexture"),
    ("STR_ARKANIMATION", 0x00A8547C, b"ArkAnimation"),
]

REQUIRED_PIN_FIELDS = ("CALLSITE_VA", "BYTES", "SIGNED_REL32", "NEXT_VA",
                       "TARGET_VA", "TARGET_FORMULA")


def parse_hex_bytes(s):
    return bytes.fromhex(s.replace(" ", ""))


def parse_signed_rel32(s):
    """Parse the SIGNED_REL32 record field (e.g. '+0x2F075')."""
    return int(s, 16)


def parse_va(s):
    return int(s, 16)


def load_active_corrected_pins(path=None):
    """Load + schema-validate ACTIVE_CORRECTED_PINS.json. Structural only:
    no expected VALUE is hardcoded here (the value gates are the RECW_*
    checks, driven by the JSON values against the physical bytes)."""
    p = os.path.abspath(path or PINS_JSON_PATH)
    if not os.path.isfile(p):
        raise ValueError(f"ACTIVE_CORRECTED_PINS.json missing: {p}")
    with open(p, "r", encoding="utf-8") as f:
        doc = json.load(f)
    if not isinstance(doc, dict) or not isinstance(doc.get("active_records"), list):
        raise ValueError("ACTIVE_CORRECTED_PINS.json: active_records list missing")
    if len(doc["active_records"]) != 1:
        raise ValueError(
            f"ACTIVE_CORRECTED_PINS.json: expected exactly 1 active record, "
            f"got {len(doc['active_records'])}")
    rec = doc["active_records"][0]
    if not isinstance(rec, dict) or "RECORD_ID" not in rec:
        raise ValueError("active record: RECORD_ID missing")
    for field in REQUIRED_PIN_FIELDS:
        if field not in rec or not isinstance(rec[field], str) or not rec[field]:
            raise ValueError(f"active record {rec.get('RECORD_ID')}: field {field} missing")
    parse_va(rec["CALLSITE_VA"])          # format check only
    parse_va(rec["NEXT_VA"])
    parse_va(rec["TARGET_VA"])
    b = parse_hex_bytes(rec["BYTES"])     # format check only
    if len(b) != 5 or b[0] != 0xE8:
        raise ValueError("active record BYTES: expected a 5-byte E8 call")
    parse_signed_rel32(rec["SIGNED_REL32"])
    return {"path": p, "record": rec}


def record_checks(pe, pins_doc):
    """REC-W record gates — the JSON drives every expectation below.

    RECW:RECORD_SCHEMA                 the JSON loads and is structurally valid
    RECW:W_RECORD_BYTES                physical read(CALLSITE_VA,5) == BYTES
    RECW:W_RECORD_REL32               own recompute int32(physical[1:5]) ==
                                       SIGNED_REL32 (JSON value vs physical)
    RECW:W_RECORD_NEXT_VA              CALLSITE_VA + 5 == NEXT_VA (JSON)
    RECW:W_RECORD_TARGET               own recompute CALLSITE_VA+5+
                                       int32(physical[1:5]) == TARGET_VA (JSON)
    RECW:W_RECORD_INTERNAL_CONSISTENCY  the JSON record is self-consistent
                                       (BYTES-derived rel32 == SIGNED_REL32;
                                       CALLSITE+5+REL32 == TARGET_VA)
    """
    results = []
    results.append(("RECW:RECORD_SCHEMA", "PASS",
                    "ACTIVE_CORRECTED_PINS.json loaded; exactly 1 active "
                    "record with all required fields (structural check only)"))
    rec = pins_doc["record"]
    callsite = parse_va(rec["CALLSITE_VA"])
    exp_bytes = parse_hex_bytes(rec["BYTES"])
    exp_rel = parse_signed_rel32(rec["SIGNED_REL32"])
    exp_next = parse_va(rec["NEXT_VA"])
    exp_target = parse_va(rec["TARGET_VA"])
    try:
        got = pe.read(callsite, 5)
    except ControlledReadError as e:
        results.append(("RECW:W_RECORD_BYTES", "FAIL",
                         f"@{callsite:#010x} range-safe read error: {e}"))
        results.append(("RECW:W_RECORD_REL32", "FAIL", "no physical bytes to recompute"))
        results.append(("RECW:W_RECORD_NEXT_VA", "PASS" if exp_next == callsite + 5 else "FAIL",
                         f"JSON NEXT_VA {rec['NEXT_VA']} vs CALLSITE_VA+5 {callsite + 5:#010x}"))
        results.append(("RECW:W_RECORD_TARGET", "FAIL", "no physical bytes to recompute"))
        results.append(("RECW:W_RECORD_INTERNAL_CONSISTENCY", "FAIL", "physical read failed"))
        return results
    if got == exp_bytes:
        results.append(("RECW:W_RECORD_BYTES", "PASS",
                         f"@{callsite:#010x} physical == JSON BYTES {rec['BYTES']}"))
    else:
        results.append(("RECW:W_RECORD_BYTES", "FAIL",
                         f"@{callsite:#010x} physical {got.hex(' ').upper()} != "
                         f"JSON BYTES {rec['BYTES']}"))
    phys_rel = struct.unpack("<i", got[1:5])[0]
    if phys_rel == exp_rel:
        results.append(("RECW:W_RECORD_REL32", "PASS",
                        f"own recompute int32(physical[1:5]) = {phys_rel:+#x} == "
                        f"JSON SIGNED_REL32 {rec['SIGNED_REL32']}"))
    else:
        results.append(("RECW:W_RECORD_REL32", "FAIL",
                        f"own recompute int32(physical[1:5]) = {phys_rel:+#x} != "
                        f"JSON SIGNED_REL32 {rec['SIGNED_REL32']}"))
    if exp_next == callsite + 5:
        results.append(("RECW:W_RECORD_NEXT_VA", "PASS",
                        f"JSON NEXT_VA {rec['NEXT_VA']} == CALLSITE_VA+5 {callsite + 5:#010x}"))
    else:
        results.append(("RECW:W_RECORD_NEXT_VA", "FAIL",
                        f"JSON NEXT_VA {rec['NEXT_VA']} != CALLSITE_VA+5 {callsite + 5:#010x}"))
    phys_target = callsite + 5 + phys_rel
    if phys_target == exp_target:
        results.append(("RECW:W_RECORD_TARGET", "PASS",
                        f"own recompute CALLSITE_VA+5+int32(physical[1:5]) = "
                        f"{phys_target:#010x} == JSON TARGET_VA {rec['TARGET_VA']} "
                        f"(formula: {rec['TARGET_FORMULA']})"))
    else:
        results.append(("RECW:W_RECORD_TARGET", "FAIL",
                        f"own recompute CALLSITE_VA+5+int32(physical[1:5]) = "
                        f"{phys_target:#010x} != JSON TARGET_VA {rec['TARGET_VA']}"))
    json_rel = struct.unpack("<i", exp_bytes[1:5])[0]
    consistent = (json_rel == exp_rel) and (callsite + 5 + exp_rel == exp_target)
    if consistent:
        results.append(("RECW:W_RECORD_INTERNAL_CONSISTENCY", "PASS",
                        f"JSON self-consistent: BYTES-derived rel32 {json_rel:+#x} == "
                        f"SIGNED_REL32; CALLSITE+5+REL32 == TARGET_VA"))
    else:
        results.append(("RECW:W_RECORD_INTERNAL_CONSISTENCY", "FAIL",
                        f"JSON inconsistent: BYTES-derived rel32 {json_rel:+#x} vs "
                        f"SIGNED_REL32 {rec['SIGNED_REL32']}; "
                        f"CALLSITE+5+REL32 {callsite + 5 + exp_rel:#010x} vs "
                        f"TARGET_VA {rec['TARGET_VA']}"))
    return results


def run_checks(data_override=None, pins_override=None):
    """Run all checks. data_override = an in-memory TEST-OVERRIDE copy
    (mechanical controls) — the physical file is never modified and the
    override is never reported as the SHA-identical physical EXE.
    pins_override = a mutated in-memory copy of the parsed
    ACTIVE_CORRECTED_PINS.json document (record mutation controls); the
    JSON file itself is never modified."""
    results = []
    if data_override is None:
        try:
            data = load_pinned()
            results.append(("EXE_IDENTITY", "PASS",
                            "physical EXE size+SHA256 == pinned"))
        except ValueError as e:
            results.append(("EXE_IDENTITY", "FAIL", str(e)))
            return results
    else:
        data = data_override
        if len(data) != EXE_SIZE:
            results.append(("EXE_IDENTITY_OVERRIDE_SIZE", "FAIL", f"size {len(data)}"))
            return results
        results.append(("EXE_IDENTITY", "PASS",
                        "TEST-OVERRIDE buffer (size ok; the physical EXE "
                        "identity is checked by the caller before/after; this "
                        "buffer is NOT the SHA-identical physical EXE)"))

    pe = RangeSafePE(data)

    # 1. byte pins (whole historical list, same meaning)
    for pin_id, va, hexstr in BYTE_PINS:
        expected = bytes.fromhex(hexstr.replace(" ", ""))
        try:
            got = pe.read(va, len(expected))
        except ControlledReadError as e:
            results.append((f"PIN:{pin_id}", "FAIL", f"@{va:#010x} read error: {e}"))
            continue
        if got == expected:
            results.append((f"PIN:{pin_id}", "PASS", f"@{va:#010x} == {hexstr}"))
        else:
            results.append((f"PIN:{pin_id}", "FAIL",
                            f"@{va:#010x} expected {hexstr}, got {got.hex(' ').upper()}"))

    # 2. rel32 recomputation (own arithmetic; must equal the expected target)
    for rel_id, call_va, target in REL32_PINS:
        try:
            b = pe.read(call_va, 5)
        except ControlledReadError as e:
            results.append((f"REL32:{rel_id}", "FAIL", f"@{call_va:#010x} read error: {e}"))
            continue
        if b[0] != 0xE8:
            results.append((f"REL32:{rel_id}", "FAIL",
                            f"@{call_va:#010x} opcode {b[0]:#04x} != E8"))
            continue
        rel = struct.unpack("<i", b[1:5])[0]
        own = call_va + 5 + rel
        if own == target:
            results.append((f"REL32:{rel_id}", "PASS",
                            f"@{call_va:#010x} E8 rel32 {rel:+#x} -> {own:#010x} == expected"))
        else:
            results.append((f"REL32:{rel_id}", "FAIL",
                            f"@{call_va:#010x} rel32 {rel:+#x} -> {own:#010x} != expected {target:#010x}"))

    # 3. RTTI chains — vtable[-1] -> COL (20 B) -> TypeDescriptor (+8 name);
    #    EVERY read below goes through the same range-safe API.
    for rtti_id, vt, name in RTTI_PINS:
        try:
            col_ptr = pe.u32(vt - 4)
            col = pe.read(col_ptr, 20)
            sig, _o, _cd, ptd, _pcd = struct.unpack("<5I", col)
            if sig != 0:
                results.append((f"RTTI:{rtti_id}", "FAIL", f"COL sig {sig:#x} != 0"))
                continue
            got = pe.read(ptd + 8, len(name) + 1)
            if got[:-1] == name and got[-1] == 0:
                results.append((f"RTTI:{rtti_id}", "PASS",
                                f"vtable {vt:#010x} -> COL {col_ptr:#010x} (20 B, "
                                f"range-safe) -> TD {ptd:#010x} -> {name.decode()}"))
            else:
                results.append((f"RTTI:{rtti_id}", "FAIL",
                                f"vtable {vt:#010x} name mismatch: {got!r}"))
        except ControlledReadError as e:
            results.append((f"RTTI:{rtti_id}", "FAIL", str(e)))

    # 4. string pins
    for sid, va, s in STRING_PINS:
        try:
            got = pe.read(va, len(s) + 1)
            if got[:-1] == s and got[-1] == 0:
                results.append((f"STR:{sid}", "PASS", f"@{va:#010x} == {s.decode()}"))
            else:
                results.append((f"STR:{sid}", "FAIL", f"@{va:#010x} mismatch: {got!r}"))
        except ControlledReadError as e:
            results.append((f"STR:{sid}", "FAIL", str(e)))

    # 5. REC-W record gates — driven by ACTIVE_CORRECTED_PINS.json
    try:
        pins_doc = pins_override if pins_override is not None \
            else load_active_corrected_pins()
        if "record" not in pins_doc:
            # a raw mutated document was supplied (mutation controls)
            rec = pins_doc["active_records"][0]
            pins_doc = {"path": "IN-MEMORY TEST OVERRIDE (mutation control)",
                       "record": rec}
        results.extend(record_checks(pe, pins_doc))
    except ValueError as e:
        results.append(("RECW:RECORD_SCHEMA", "FAIL", str(e)))

    return results


def gate(results):
    """The production gate: PASS only if every check PASSes."""
    fails = [r for r in results if r[1] != "PASS"]
    return (len(fails) == 0), fails


def main():
    results = run_checks()
    ok, fails = gate(results)
    npass = sum(1 for r in results if r[1] == "PASS")
    print(f"checker_plus4_successor: {npass}/{len(results)} checks PASS")
    for rid, verdict, detail in results:
        if verdict != "PASS":
            print(f"  FAIL {rid}: {detail}")
    print("GATE:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
