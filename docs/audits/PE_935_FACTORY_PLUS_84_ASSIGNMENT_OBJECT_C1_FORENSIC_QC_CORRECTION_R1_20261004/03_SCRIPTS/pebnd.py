# pebnd.py
# RUN: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004
# Shared PE loader + DECLARED TRUSTED BOUNDARY machinery (F84-C1/F84-C2 policy).
#
# BOUNDARY POLICY (corrected): a raw byte position is NOT automatically an
# instruction boundary; a byte equal to E8 is NOT automatically a CALL; a
# multi-start path beginning inside another instruction establishes NOTHING.
# BOUNDARY_CONFIRMED requires a decode from an EXPLICITLY DECLARED trusted
# boundary source that lands exactly on the candidate. Declared trusted
# sources here:
#   (T1) KNOWN_FUNCTION_ENTRY - the prior-canon function entry table below;
#        sequential decode from the entry must land exactly on the candidate.
#   (T2) CC_PADDING_DELIMITED_START - the first non-CC byte after a >=2-CC
#        int3 padding run (padding never participates in an instruction);
#        sequential decode from that start must land exactly on the candidate.
#   (T3) RET_DELIMITED_START - the first non-CC byte after a >=1-CC padding
#        run that IMMEDIATELY follows a function-terminating instruction
#        (C3 RET / C2 RET imm16) - the standard MSVC function boundary where
#        the alignment padding between functions is a single int3 byte;
#        sequential decode from that start must land exactly on the candidate.
# If no trusted decode reaches the candidate -> BOUNDARY_STATUS=UNRESOLVED.
# The decode does NOT abort on RET/C2 (multi-exit functions are normal);
# it aborts on CC (padding breaks the linear stream) and on any undecodable
# byte (fail-closed decoder). No "NOT_AN_INSTRUCTION" inference is EVER made
# from a failed decode. In every case the EXACT-LANDING sequential decode is
# the safeguard against a mis-identified start.

import struct

import x86dec

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
PINNED_EXE_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
PINNED_EXE_SIZE = 8015872

# Declared trusted boundary sources (T1): prior-canon function entries.
KNOWN_ENTRIES = {
    0x0070DCF0: "FUN_0070DCF0_consumer_record_reader",
    0x0070CF80: "FUN_0070CF80_factory_base_ctor",
    0x0070C680: "FUN_0070C680_stream_attach_setter",
    0x00703E80: "FUN_00703E80_bulk_attach_loop",
    0x004B0980: "FUN_004B0980_attach_driver",
    0x00707FB0: "FUN_00707FB0_register_factory",
    0x007080C0: "FUN_007080C0_manager_mode_and_class_enum",
    0x00972380: "FUN_00972380_stream_ctor",
    0x00703CD0: "FUN_00703CD0_manager_mode_cond",
    0x0070CC80: "FUN_0070CC80_slot_predicate_scan",
    0x00707E50: "FUN_00707E50_manager_ctor",
    0x00415470: "FUN_00415470_manager_getter",
    0x0073C870: "FUN_0073C870_class_dispatcher",
    0x0073C8D8: "FUN_0073C8D8_factory20006_getter",
    0x0073B820: "FUN_0073B820_factory20006_ctor",
    0x0073B8C0: "FUN_0073B8C0_factory20006_create_component",
    0x0073C6C0: "FUN_0073C6C0_factory20006_dtor",
    0x0070D990: "FUN_0070D990_component_creator",
    0x0070DC20: "FUN_0070DC20_record_apply",
    0x0070DE10: "FUN_0070DE10_cache_miss_creator",
    0x0070E100: "FUN_0070E100_component_get_or_create",
    0x0070C150: "FUN_0070C150_factory_finalize",
    0x0070BF10: "FUN_0070BF10_ready_flag_reader",
    0x0070BF20: "FUN_0070BF20_flag_or_setter",
    0x0070BF40: "FUN_0070BF40_flag_bit_test",
    0x0070C180: "FUN_0070C180_slot_addr_getter",
    0x007374F0: "FUN_007374F0_schema_init",
    0x0070CBC0: "FUN_0070CBC0_slot_add",
    0x0070E2F0: "FUN_0070E2F0_factory_vec_init",
    0x0071B820: "FUN_0071B820_UNKNOWN",
    0x00971AD0: "FUN_00971AD0_record_reader",
    0x00971650: "FUN_00971650_stream_advance",
    0x0070BFD0: "FUN_0070BFD0_stream_bridge_method",
    0x0072FA30: "FUN_0072FA30_templates_reader_region",
}

TRUSTED_EXTENT = 0x2000   # max candidate-to-entry distance for a trusted decode
PADDING_LOOKBACK = 0x800  # max backward scan for a CC padding run
SEQ_STEP_CAP = 20000


def load_text(path=EXE_PATH):
    d = open(path, "rb").read()
    e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
    if d[e_lfanew:e_lfanew + 4] != b"PE\x00\x00":
        raise SystemExit("not a PE")
    coff = e_lfanew + 4
    nsec = struct.unpack_from("<H", d, coff + 2)[0]
    opt_size = struct.unpack_from("<H", d, coff + 16)[0]
    opt = coff + 20
    image_base = struct.unpack_from("<I", d, opt + 28)[0]
    sec0 = opt + opt_size
    secs = []
    for i in range(nsec):
        s = sec0 + 40 * i
        name = d[s:s + 8].rstrip(b"\x00").decode("ascii", "replace")
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", d, s + 8)
        secs.append({"name": name, "vaddr": vaddr, "vsize": vsize,
                     "rawptr": rawptr, "rawsize": rawsize})
    for s in secs:
        if s["name"] == ".text":
            text = d[s["rawptr"]:s["rawptr"] + s["rawsize"]]
            return d, image_base, secs, text, image_base + s["vaddr"]
    raise SystemExit("no .text")


def va_to_off(image_base, secs, va):
    rva = va - image_base
    for s in secs:
        if s["vaddr"] <= rva < s["vaddr"] + max(s["vsize"], s["rawsize"]):
            if rva - s["vaddr"] < s["rawsize"]:
                return s["rawptr"] + (rva - s["vaddr"])
    return None


def read_win(data, image_base, secs, va, size):
    off = va_to_off(image_base, secs, va)
    if off is None:
        return None
    w = data[off:off + size]
    return w.hex(" ").upper() if len(w) == size else None


def find_padding_start(text, tva, va, lookback=PADDING_LOOKBACK, max_cands=8):
    """Collect declared trusted boundary candidates below va, NEAREST FIRST.
    (T2) first non-CC byte after every >=2-CC padding run in the lookback.
    (T3) first non-CC byte after every >=1-CC run that immediately follows a
    function-terminating RET/C3 / RET imm16/C2 (single-byte MSVC padding).
    The EXACT-LANDING sequential decode in boundary_confirm is the safeguard
    against a mis-identified start; a failed candidate is simply skipped."""
    hi = va - tva
    lo = max(0, hi - lookback)
    cands = []
    j = hi - 1
    while j >= lo + 1 and len(cands) < max_cands:
        if text[j] == 0xCC:
            # walk to the top of this CC run
            k = j
            while k + 1 < len(text) and text[k + 1] == 0xCC:
                k += 1
            # walk to the bottom of the run
            r0 = j
            while r0 - 1 >= 0 and text[r0 - 1] == 0xCC:
                r0 -= 1
            run_len = k - r0 + 1
            start = tva + k + 1
            if run_len >= 2:
                cands.append((start, "CC_PADDING_DELIMITED_START"))
            else:
                prev = r0 - 1
                if prev >= 0 and (text[prev] == 0xC3 or
                                  (prev >= 2 and text[prev - 2] == 0xC2)):
                    cands.append((start, "RET_DELIMITED_START"))
            j = r0 - 1
        else:
            j -= 1
    if not cands:
        return None, None
    return cands[0]


def seq_decode_lands(text, start_off, target_off, cap=SEQ_STEP_CAP):
    """Linear fail-closed decode from start_off; True iff it lands exactly on
    target_off. Aborts on CC (padding) or undecodable byte. Never aborts on RET."""
    i = start_off
    steps = 0
    while i < target_off:
        if text[i] == 0xCC:
            return False
        ins = x86dec.decode(text, i)
        if ins is None or ins.length <= 0:
            return False
        i += ins.length
        steps += 1
        if steps > cap:
            return False
    return i == target_off


class _BoundaryCache(object):
    """Per-start memoized linear decode position sets (speed only; results
    identical to an uncached sequential decode)."""

    def __init__(self, text, tva):
        self.text = text
        self.tva = tva
        self._starts = {}

    def positions(self, start_va):
        if start_va in self._starts:
            return self._starts[start_va]
        s = self._starts[start_va] = set()
        i = start_va - self.tva
        text = self.text
        steps = 0
        while i < len(text) and steps < SEQ_STEP_CAP:
            if text[i] == 0xCC:
                break
            s.add(i)
            ins = x86dec.decode(text, i)
            if ins is None or ins.length <= 0:
                break
            i += ins.length
            steps += 1
        return s


def boundary_confirm(text, tva, va, cache=None):
    """Returns (confirmed: bool, source: str, start_va: int|None).
    Declared trusted sources ONLY; multi-start is NOT a trusted source.
    Candidates are tried nearest-first; the first EXACT-LANDING sequential
    decode confirms the boundary."""
    cands = []
    for entry in KNOWN_ENTRIES:
        if entry <= va and va - entry <= TRUSTED_EXTENT:
            cands.append((entry, "KNOWN_FUNCTION_ENTRY"))
    for start, source in (find_boundary_cands(text, tva, va) or []):
        if start is not None and start <= va and va - start <= TRUSTED_EXTENT:
            cands.append((start, source))
    cands.sort(key=lambda c: -c[0])  # nearest start first
    for start, source in cands:
        if cache is not None:
            ok = (va - tva) in cache.positions(start)
        else:
            ok = seq_decode_lands(text, start - tva, va - tva)
        if ok:
            return True, source, start
    return False, None, None


def find_boundary_cands(text, tva, va):
    """Multi-candidate wrapper around find_padding_start internals (list form)."""
    hi = va - tva
    lo = max(0, hi - PADDING_LOOKBACK)
    cands = []
    j = hi - 1
    while j >= lo + 1 and len(cands) < 8:
        if text[j] == 0xCC:
            k = j
            while k + 1 < len(text) and text[k + 1] == 0xCC:
                k += 1
            r0 = j
            while r0 - 1 >= 0 and text[r0 - 1] == 0xCC:
                r0 -= 1
            run_len = k - r0 + 1
            start = tva + k + 1
            if run_len >= 2:
                cands.append((start, "CC_PADDING_DELIMITED_START"))
            else:
                prev = r0 - 1
                if prev >= 0 and (text[prev] == 0xC3 or
                                  (prev >= 2 and text[prev - 2] == 0xC2)):
                    cands.append((start, "RET_DELIMITED_START"))
            j = r0 - 1
        else:
            j -= 1
    return cands


def validate_direct_call(text, tva, va, cache=None):
    """F84-C1 DIRECT CALL VALIDATION.
    Returns dict: byte_is_E8, operand_complete, boundary_status, boundary_source,
    call_validation (PASS|FAIL|NOT_VERIFIED), target (only when PASS)."""
    res = {"va": va, "byte_is_E8": False, "operand_complete": False,
           "boundary_status": "UNRESOLVED", "boundary_source": None,
           "call_validation": "FAIL", "target": None}
    off = va - tva
    if off < 0 or off >= len(text):
        return res
    res["byte_is_E8"] = (text[off] == 0xE8)
    if not res["byte_is_E8"]:
        res["call_validation"] = "FAIL"
        return res
    if off + 5 > len(text):
        res["call_validation"] = "FAIL"  # operand bytes incomplete
        return res
    res["operand_complete"] = True
    confirmed, source, _ = boundary_confirm(text, tva, va, cache)
    res["boundary_status"] = "CONFIRMED" if confirmed else "UNRESOLVED"
    res["boundary_source"] = source
    if not confirmed:
        res["call_validation"] = "NOT_VERIFIED"  # no target promoted
        return res
    rel = x86dec.call_operand_rel32(text, off)
    res["call_validation"] = "PASS"
    res["target"] = va + 5 + rel
    return res
