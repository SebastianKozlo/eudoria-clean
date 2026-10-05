# pebnd.py
# RUN: PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005
# Shared PE loader + CORRECTED boundary machinery.
# Copy lineage: the C2 AF2-corrected strong-anchor boundary machinery + THIS
# run's P2-1 repair (Desktop post-audit PE_935_F84_C2_DESKTOP_POST_AUDIT_20261004
# finding C2-C1/P2).
#
# P2-1 REPAIR vs the C2 machinery (_BoundaryCache.coverage defect):
#   * The C2 _BoundaryCache stored extents as a SET and
#     covers_mid_instruction early-broke at `a >= target_off` over UNORDERED
#     set iteration. The covering extent can be visited after a
#     later-starting extent already triggered the break, so real coverage
#     was MISSED: (a) REFUTED_MID_INSTRUCTION was UNDERCLAIMED (real
#     manifestations re-derived this run: the driver pins 0x004B0A02
#     interior to `BB 01 00 00 00` @0x004B0A01 and 0x004B0A21 interior to
#     `E8 4D 14 F5 FF` @0x004B0A1E, anchor 0x004B0980), and (b) ANCHOR
#     CONFLICT was SUPPRESSED: when anchor A covers the candidate
#     mid-instruction and anchor B lands exactly on it, the honest result is
#     UNRESOLVED/ANCHOR_CONFLICT with CALL_VALIDATION != PASS and the target
#     NOT promoted - hiding A's coverage let B's exact landing yield
#     CONFIRMED and a FALSE CALL promotion (Desktop NEW-F fixture:
#     `B8 00 E8 01 00 00 00 90 CC`, anchor A=start+0, anchor B=start+2,
#     candidate E8=start+2 -> correct result UNRESOLVED/ANCHOR_CONFLICT,
#     target NOT promoted).
#   * FIX: extents are STORED and ITERATED SORTED (the scan function sorts
#     its input, making the result provably independent of insertion/
#     iteration order; the order-permutation proofs are persisted in the QC
#     battery). The early break remains VALID only over a sorted scan. The
#     anchor-conflict POLICY is NOT weakened: lands+refutes => UNRESOLVED/
#     ANCHOR_CONFLICT with no promotion stays exactly as before.
#
# AF2 CORRECTION vs the C1 machinery (Desktop post-audit finding AF2/P2):
#   * The C1 T2/T3 classes promoted raw CC-padding / C3-CC / RET+CC patterns to
#     "trusted boundary sources" (CC_PADDING_DELIMITED_START /
#     RET_DELIMITED_START) and let them CONFIRM boundaries and promote CALLs.
#     That policy is INVALID: a raw delimiter/padding pattern is only a
#     HEURISTIC_START_CANDIDATE unless separate existing physical evidence
#     independently establishes the alignment. In this corrected machinery
#     heuristic starts are ENUMERATED and RECORDED but can NEVER confirm a
#     boundary, can NEVER win against a conflicting proven decode, and can
#     NEVER promote a CALL target.
#   * Strong anchors are ONLY the prior-canon KNOWN_FUNCTION_ENTRY table
#     (ANCHOR_REGISTRY below), each recorded with ANCHOR_VA / ANCHOR_CLASS /
#     EXISTING_PHYSICAL_EVIDENCE / EVIDENCE_SOURCE / EVIDENCE_STATUS. The
#     evidence for each anchor is prior canonical runs' pinned chains plus
#     this run's same-VA byte re-verification - INDEPENDENT of every candidate
#     validated against the anchor (no circular proof: a candidate is never
#     itself promoted to anchor status).
#   * A sequential fail-closed decode from a strong anchor that lands exactly
#     on the candidate -> BOUNDARY_STATUS=CONFIRMED (source=KNOWN_FUNCTION_ENTRY).
#   * A sequential decode from a strong anchor that COVERS the candidate
#     strictly inside one of its instructions -> BOUNDARY_STATUS=
#     REFUTED_MID_INSTRUCTION: the candidate is operand/interior data on that
#     PROVEN decode path. This is a successful-decode refutation, NOT an
#     inference from a failed decode. A conflicting heuristic start NEVER
#     overrides it (contract precedence rule).
#   * If one strong anchor lands exactly and another covers mid-instruction
#     (anchor conflict) -> UNRESOLVED (no confirmation; disclosed).
#   * No strong anchor reaching the candidate and no proven refutation ->
#     BOUNDARY_STATUS=UNRESOLVED with BOUNDARY_SOURCE=HEURISTIC_START_CANDIDATE
#     (if a heuristic start exists) or empty.
# The decode aborts on CC (padding breaks the linear stream) and on any
# undecodable byte (fail-closed decoder); it does NOT abort on RET/C2
# (multi-exit functions). No whole-binary function-discovery sweep is performed
# and no new anchors are invented by this run.

import struct

import x86dec

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
PINNED_EXE_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
PINNED_EXE_SIZE = 8015872

# ---------------------------------------------------------------------------
# ANCHOR_REGISTRY - the ONLY strong boundary sources (T1). Every entry records
# its provenance per the AF2 contract. EVIDENCE_SOURCE names the prior-canon
# committed packages that physically pinned the entry (byte-level entry decode
# + pinned function chains); EVIDENCE_STATUS states the class honestly.
# ---------------------------------------------------------------------------
_PRIOR_CANON_NOTE = ("prior-canon function entry table carried by the F84 chain "
                     "packages (R1 FUNCTION_LEDGER anchor battery / C1 same-VA "
                     "pin chains); entry bytes re-verified this run at the "
                     "pinned VA; used ONLY as a decode origin, independent of "
                     "every candidate validated against it")
_EVIDENCE_SOURCE = ("docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004 "
                    "+ docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_"
                    "FORENSIC_QC_CORRECTION_R1_20261004 (committed prior canon) "
                    "+ THIS run same-VA byte re-verification")
_EVIDENCE_STATUS = "PRIOR_CANON_ENTRY_BYTE_REVERIFIED_THIS_RUN"

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


def anchor_registry():
    """ANCHOR_VA / ANCHOR_CLASS / EXISTING_PHYSICAL_EVIDENCE / EVIDENCE_SOURCE /
    EVIDENCE_STATUS per strong anchor (AF2 contract persistence)."""
    return [{"ANCHOR_VA": "0x%08X" % va,
             "ANCHOR_CLASS": "KNOWN_FUNCTION_ENTRY",
             "ANCHOR_NAME": name,
             "EXISTING_PHYSICAL_EVIDENCE": _PRIOR_CANON_NOTE,
             "EVIDENCE_SOURCE": _EVIDENCE_SOURCE,
             "EVIDENCE_STATUS": _EVIDENCE_STATUS}
            for va, name in sorted(KNOWN_ENTRIES.items())]


TRUSTED_EXTENT = 0x2000   # max candidate-to-entry distance for a trusted decode
PADDING_LOOKBACK = 0x800  # max backward scan for heuristic CC runs
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


def find_heuristic_starts(text, tva, va, lookback=PADDING_LOOKBACK, max_cands=8):
    """Enumerate HEURISTIC_START_CANDIDATE positions below va (AF2 disclosure).
    (H2) first non-CC byte after every >=2-CC run; (H3) first non-CC byte after
    every >=1-CC run that immediately follows C3 / C2 imm16. These are the C1
    T2/T3 classes, DEMOTED to heuristic: they are recorded per candidate but can
    NEVER confirm a boundary or promote a CALL in this machinery."""
    hi = va - tva
    lo = max(0, hi - lookback)
    cands = []
    j = hi - 1
    while j >= lo + 1 and len(cands) < max_cands:
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


def covers_mid_instruction(extents_iterable, target_off):
    """True iff some instruction extent (a, b) strictly covers target_off
    (a < target_off < b). ORDER-INDEPENDENT (P2-1): the input is SORTED
    before scanning, so the caller's insertion/iteration order can never
    change the result; the early break at a >= target_off is valid only
    over this sorted scan (the C2 version early-broke over an unordered
    set and missed real coverage -> underclaimed REFUTED_MID_INSTRUCTION
    and suppressed ANCHOR_CONFLICT)."""
    for (a, b) in sorted(extents_iterable):
        if a >= target_off:
            return False
        if b > target_off:
            return True
    return False


class _BoundaryCache(object):
    """Per-start memoized linear decode (positions + instruction extents).
    Speed only; results identical to an uncached sequential decode.
    extents = SORTED list of (insn_start_off, insn_end_off) for
    coverage/mid-instruction refutation (P2-1: stored sorted, scanned via
    covers_mid_instruction which sorts again - order-independent by
    construction); positions = set of instruction-start offsets (pure
    membership test, order-free by nature)."""

    def __init__(self, text, tva, entries=None):
        self.text = text
        self.tva = tva
        self._entries = entries if entries is not None else KNOWN_ENTRIES
        self._starts = {}

    def _build(self, start_va):
        s = self._starts[start_va] = {"positions": set(), "extents": []}
        i = start_va - self.tva
        text = self.text
        steps = 0
        while i < len(text) and steps < SEQ_STEP_CAP:
            if text[i] == 0xCC:
                break
            ins = x86dec.decode(text, i)
            if ins is None or ins.length <= 0:
                break
            s["positions"].add(i)
            s["extents"].append((i, i + ins.length))
            i += ins.length
            steps += 1
        # P2-1: store SORTED (the stream is already sequential; the explicit
        # sort documents and enforces the invariant the coverage scan relies on)
        s["extents"].sort()
        return s

    def positions(self, start_va):
        if start_va not in self._starts:
            self._build(start_va)
        return self._starts[start_va]["positions"]

    def extents(self, start_va):
        if start_va not in self._starts:
            self._build(start_va)
        return self._starts[start_va]["extents"]

    def covers_mid_instruction(self, start_va, target_off):
        """True iff the proven decode stream from start_va contains an
        instruction (a,b) with a < target_off < b (strictly interior).
        Delegates to the order-independent sorted scan (P2-1)."""
        return covers_mid_instruction(self.extents(start_va), target_off)


def boundary_confirm(text, tva, va, cache=None, entries=None):
    """CORRECTED strong-provenance boundary determination.
    Returns (status, source, start_va, refuted_by_start):
      status: 'CONFIRMED' | 'REFUTED_MID_INSTRUCTION' | 'UNRESOLVED'
      source: 'KNOWN_FUNCTION_ENTRY' when CONFIRMED/REFUTED; the heuristic
              class when only heuristic starts exist (UNRESOLVED); else None
      start_va: the confirming/refuting anchor VA (int) or None
      refuted_by_start: the anchor whose proven decode covered va mid-instruction
                        (only for REFUTED_MID_INSTRUCTION)
    Heuristic starts (C1 T2/T3) NEVER confirm. Precedence: a proven decode that
    covers va mid-instruction REFUTES; a conflicting heuristic start cannot
    override it. A CONFIRMED landing plus any REFUTATION is an anchor conflict
    -> UNRESOLVED (disclosed, never silently resolved)."""
    ent = entries if entries is not None else KNOWN_ENTRIES
    off = va - tva
    candidates = [e for e in ent if e <= va and va - e <= TRUSTED_EXTENT]
    confirmed = None
    refuted = None
    for entry in sorted(candidates):
        if cache is not None and entries is None:
            lands = off in cache.positions(entry)
            covers = cache.covers_mid_instruction(entry, off)
        else:
            lands = seq_decode_lands(text, entry - tva, off)
            covers = False
            if not lands:
                # uncached: check coverage by walking with early exit
                i = entry - tva
                steps = 0
                while i < off:
                    if text[i] == 0xCC:
                        break
                    ins = x86dec.decode(text, i)
                    if ins is None or ins.length <= 0:
                        break
                    if i + ins.length > off:
                        covers = True
                        break
                    i += ins.length
                    steps += 1
                    if steps > SEQ_STEP_CAP:
                        break
        if lands:
            if refuted is not None:
                # anchor conflict: one lands, another refutes -> UNRESOLVED
                return "UNRESOLVED", "ANCHOR_CONFLICT", None, None
            confirmed = (confirmed or entry)
        elif covers:
            if confirmed is not None:
                return "UNRESOLVED", "ANCHOR_CONFLICT", None, None
            refuted = refuted or entry
    if confirmed is not None:
        return "CONFIRMED", "KNOWN_FUNCTION_ENTRY", confirmed, None
    if refuted is not None:
        return "REFUTED_MID_INSTRUCTION", "KNOWN_FUNCTION_ENTRY", refuted, refuted
    # no strong evidence either way: heuristic starts recorded, never confirming
    hc = find_heuristic_starts(text, tva, va)
    if hc:
        return "UNRESOLVED", "HEURISTIC_START_CANDIDATE", None, None
    return "UNRESOLVED", None, None, None


def validate_direct_call(text, tva, va, cache=None, entries=None):
    """F84-C2 DIRECT CALL VALIDATION (corrected).
    Promotion of TARGET = VA+5+signed_rel32(VA+1) requires ALL of:
      * byte[VA] == 0xE8 AND the 5-byte form is unprefixed (a 66 E8 rel16
        near branch is a DIFFERENT encoding - handled at its actual width by
        the decoder but NEVER promoted as an ordinary five-byte E8 rel32);
      * all 5 operand bytes present;
      * BOUNDARY CONFIRMED from a strong anchor (KNOWN_FUNCTION_ENTRY with
        recorded provenance). Heuristic starts NEVER promote.
    A proven decode covering VA mid-instruction -> FAIL_MID_INSTRUCTION (the
    E8 byte is operand/interior data on a proven path).
    Returns dict with: byte_is_E8, prefixed_form, operand_complete,
    boundary_status, boundary_source, call_validation
    (PASS|FAIL|FAIL_MID_INSTRUCTION|FAIL_PREFIXED|NOT_VERIFIED), target,
    apparent_target_not_promoted."""
    res = {"va": va, "byte_is_E8": False, "prefixed_form": False,
           "operand_complete": False, "boundary_status": "UNRESOLVED",
           "boundary_source": None, "call_validation": "FAIL", "target": None,
           "apparent_target_not_promoted": None}
    off = va - tva
    if off < 0 or off >= len(text):
        return res
    res["byte_is_E8"] = (text[off] == 0xE8)
    if not res["byte_is_E8"]:
        res["call_validation"] = "FAIL"
        return res
    # prefix check: any prefix byte at the instruction containing VA?  The
    # sanctioned promotion form is an UNPREFIXED 5-byte E8 rel32.  Decode the
    # instruction at its own start is impossible without the boundary, so we
    # scan backward over prefix bytes: if VA is preceded by prefix bytes that
    # form a prefixed E8 encoding, the form is not the examined 5-byte CALL.
    # (The boundary decode is the authoritative check; this is the same rule.)
    status, source, start, refuted_by = boundary_confirm(text, tva, va, cache, entries)
    res["boundary_status"] = status
    res["boundary_source"] = source
    if status == "REFUTED_MID_INSTRUCTION":
        # the E8 byte lies strictly inside an instruction of the proven decode
        # stream: it is operand/interior data, never a CALL at this position
        res["call_validation"] = "FAIL_MID_INSTRUCTION"
        return res
    if status != "CONFIRMED":
        res["call_validation"] = "NOT_VERIFIED"
        if off + 5 <= len(text):
            res["apparent_target_not_promoted"] = (
                "0x%08X" % (va + 5 + x86dec.call_operand_rel32(text, off)))
        return res
    # boundary CONFIRMED from a strong anchor: decode the instruction AT va to
    # verify the actual encoding (prefixes/width) before promotion
    ins = x86dec.decode(text, off)
    if ins is None or ins.prefixes:
        # prefixed E8 (e.g. 66 E8 rel16) or undecodable: never promote as the
        # ordinary five-byte E8 rel32 CALL
        res["prefixed_form"] = bool(ins and ins.prefixes)
        res["call_validation"] = "FAIL_PREFIXED" if (ins and ins.prefixes) else "FAIL"
        if ins is not None and ins.prefixes and off + ins.length <= len(text):
            res["apparent_target_not_promoted"] = "0x%08X" % (
                va + ins.length + (ins.imm_signed or 0))
        return res
    if ins.opcode != 0xE8 or ins.length != 5:
        res["call_validation"] = "FAIL"
        return res
    rel = x86dec.call_operand_rel32(text, off)
    res["operand_complete"] = True
    res["call_validation"] = "PASS"
    res["target"] = va + 5 + rel
    return res
