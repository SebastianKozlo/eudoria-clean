# -*- coding: utf-8 -*-
"""QC_R3 shared probe library (PE-MASTER-AUDITOR, fresh-context internal QC).

Independent re-derivation of the PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1
science. STATIC-ONLY: the client binary is never executed; all evidence is
decoded from the on-disk bytes of the pinned Entropia.exe.

S0 fail-closed: every probe re-verifies SIZE + SHA256 + PE32 i386 +
ImageBase 0x00400000 BEFORE any decoding. A pin mismatch aborts the probe.
"""
import hashlib
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXPECT_SIZE = 8015872
EXPECT_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
EXPECT_IMAGE_BASE = 0x00400000
EXPECT_MACHINE = 0x014C   # i386
EXPECT_OPT_MAGIC = 0x010B  # PE32

IMAGE_SCN_MEM_EXECUTE = 0x20000000


class PinError(Exception):
    pass


def load_pinned():
    """S0: load the binary and verify every identity pin. Fail closed."""
    with open(EXE_PATH, "rb") as f:
        data = f.read()
    if len(data) != EXPECT_SIZE:
        raise PinError("SIZE mismatch: %d != %d" % (len(data), EXPECT_SIZE))
    h = hashlib.sha256(data).hexdigest().upper()
    if h != EXPECT_SHA256:
        raise PinError("SHA256 mismatch: %s" % h)
    if data[:2] != b"MZ":
        raise PinError("no MZ magic")
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    if data[e_lfanew:e_lfanew + 4] != b"PE\x00\x00":
        raise PinError("no PE signature")
    machine = struct.unpack_from("<H", data, e_lfanew + 4)[0]
    if machine != EXPECT_MACHINE:
        raise PinError("machine 0x%04X" % machine)
    opt_magic = struct.unpack_from("<H", data, e_lfanew + 0x18)[0]
    if opt_magic != EXPECT_OPT_MAGIC:
        raise PinError("optional header magic 0x%04X" % opt_magic)
    image_base = struct.unpack_from("<I", data, e_lfanew + 0x34)[0]
    if image_base != EXPECT_IMAGE_BASE:
        raise PinError("ImageBase 0x%08X" % image_base)
    num_sec = struct.unpack_from("<H", data, e_lfanew + 6)[0]
    opt_size = struct.unpack_from("<H", data, e_lfanew + 20)[0]
    sec_off = e_lfanew + 24 + opt_size
    sections = []
    for i in range(num_sec):
        o = sec_off + i * 40
        name = data[o:o + 8].rstrip(b"\x00").decode("latin1")
        vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", data, o + 8)
        chars = struct.unpack_from("<I", data, o + 36)[0]
        sections.append(dict(name=name, vsize=vsize, vaddr=vaddr,
                             rsize=rsize, rptr=rptr, chars=chars))
    return data, sections


def off_to_va(sections, off):
    for s in sections:
        if s["rptr"] <= off < s["rptr"] + s["rsize"]:
            return 0x400000 + s["vaddr"] + (off - s["rptr"]), s
    return None, None


def va_to_off(sections, va):
    """Map VA to file offset. Returns (offset, section) or (None, section)."""
    rva = va - 0x400000
    for s in sections:
        if s["vaddr"] <= rva < s["vaddr"] + max(s["vsize"], s["rsize"]):
            if (rva - s["vaddr"]) < s["rsize"]:
                return s["rptr"] + (rva - s["vaddr"]), s
            return None, s  # virtual-only tail (e.g. .bss)
    return None, None


def read_va(data, sections, va, n):
    off, s = va_to_off(sections, va)
    if off is None:
        return None
    return data[off:off + n]


def fmt_ins(ins):
    return "%s %-24s %s %s" % ("0x%08X" % ins.address,
                               ins.bytes.hex(),
                               ins.mnemonic, ins.op_str)


class Dis:
    """Capstone wrapper: batch decode (fast path) + detail mode on demand."""

    def __init__(self):
        self.md = Cs(CS_ARCH_X86, CS_MODE_32)
        self.md.detail = True
        self.fast = Cs(CS_ARCH_X86, CS_MODE_32)
        self.fast.detail = False

    def stream(self, data, sections, va, max_bytes, max_ins=100000, detail=False):
        """Batch linear decode. Returns (list_of_ins, stop_reason).

        stop_reason in: 'ok', 'invalid', 'unmapped'.
        """
        off, sec = va_to_off(sections, va)
        if off is None:
            return [], "unmapped"
        code = data[off:off + max_bytes]
        out = []
        md = self.md if detail else self.fast
        end = va
        for ins in md.disasm(code, va):
            out.append(ins)
            end = ins.address + ins.size
            if len(out) >= max_ins:
                return out, "ok"
        if end < va + len(code):
            # capstone stopped before the buffer end: invalid instruction at end
            return out, "invalid"
        return out, "ok"


def imm32_census(data, sections, value):
    """All whole-file occurrences of the little-endian dword `value`."""
    pat = struct.pack("<I", value)
    out = []
    pos = 0
    while True:
        i = data.find(pat, pos)
        if i < 0:
            break
        va, sec = off_to_va(sections, i)
        out.append((i, va, sec["name"] if sec else "<unmapped>"))
        pos = i + 1
    return out


def xfer_census(data, sections, target, opcode=0xE8):
    """RAW byte-pattern candidates: opcode rel32 with va+5+rel == target,
    restricted to executable sections. NOT yet decode-verified."""
    out = []
    for s in sections:
        if not (s["chars"] & IMAGE_SCN_MEM_EXECUTE):
            continue
        base_off, base_va = s["rptr"], 0x400000 + s["vaddr"]
        raw = data[base_off:base_off + s["rsize"]]
        pos = 0
        while True:
            i = raw.find(bytes([opcode]), pos)
            if i < 0:
                break
            va = base_va + i
            rel = struct.unpack_from("<i", raw, i + 1)[0]
            if va + 5 + rel == target:
                out.append(va)
            pos = i + 1
    return out


def decodes_to(dis, data, sections, start_va, site_va):
    """Batch decode from start_va; True iff every byte between decodes
    cleanly and an instruction boundary lands exactly on site_va."""
    off_s, _s1 = va_to_off(sections, start_va)
    off_t, _s2 = va_to_off(sections, site_va)
    if off_s is None or off_t is None or off_s > off_t:
        return False
    code = data[off_s:off_t + 16]
    for ins in dis.fast.disasm(code, start_va):
        if ins.address == site_va:
            return True
        if ins.address + ins.size > site_va:
            return False
    return False


_fn_start_cache = {}


def _ret_ends_at(data, i):
    """True if a ret-family instruction ends exactly at byte index i
    (i.e. the byte AFTER a ret). C3 ret / C2 imm16."""
    if i >= 1 and data[i - 1] == 0xC3:
        return True
    if i >= 3 and data[i - 3] == 0xC2:
        return True
    return False


def find_function_start(dis, data, sections, site_va, max_back=0x4000):
    """Find the start of the function containing site_va (decode-verified).

    Hardened candidate rules (mid-instruction 0x90/0xCC bytes inside
    displacement/immediate operands are NOT padding):
      C1. first byte after a CC/90 padding run of length >= 2;
      C2. first byte after a padding run of length 1 that directly follows
          the end of a ret-family instruction;
      C3. first byte directly after a bare ret (no padding) that is not
          itself a ret/padding byte.
    Every candidate must (a) decode cleanly to site_va exactly and
    (b) begin with a plausible function prologue instruction.
    The LATEST qualifying candidate wins. Results cached per site_va.
    """
    key = site_va
    if key in _fn_start_cache:
        return _fn_start_cache[key]
    off, sec = va_to_off(sections, site_va)
    result = (None, "site unmapped")
    if off is not None:
        lo = max(sec["rptr"], off - max_back)
        cands = []  # (va, runlen, ret_adjacent)

        i = off - 1
        while i >= lo:
            b = data[i]
            if b in (0xCC, 0x90):
                re = i
                rs = i
                while rs > lo and data[rs - 1] in (0xCC, 0x90):
                    rs -= 1
                runlen = re - rs + 1
                ret_adj = (rs >= 1 and data[rs - 1] == 0xC3) or \
                          (rs >= 3 and data[rs - 3] == 0xC2)
                if runlen >= 2 or ret_adj:
                    a_off = re + 1
                    if a_off < off:
                        a_va, _s = off_to_va(sections, a_off)
                        if a_va is not None:
                            cands.append((a_va, runlen, ret_adj))
                i = rs - 1
            else:
                i -= 1
        cands.sort(key=lambda t: -t[0])
        found = None
        prologue_ok = set(("push", "sub", "mov", "xor", "lea", "cmp", "test",
                           "add", "or", "and", "xchg", "call",
                           "fldz", "fld", "fld1", "fild", "fnop", "nop"))
        for a, runlen, ret_adj in cands:
            a_off = va_to_off(sections, a)[0]
            if a_off is None:
                continue
            try:
                head = next(dis.fast.disasm(data[a_off:a_off + 16], a))
            except StopIteration:
                continue
            if head.mnemonic not in prologue_ok:
                continue
            if decodes_to(dis, data, sections, a, site_va):
                found = a
                note = "run=%d" % runlen + ("+ret-adjacent" if ret_adj else "")
                if runlen == 1:
                    note += " [1-BYTE-RUN: manual review required]"
                result = (found, "start 0x%08X (padded %s; clean decode reaches site exactly)"
                          % (found, note))
                break
        if found is None:
            result = (None, "no hardened padded start decodes to site within 0x%X bytes"
                      % max_back)
    _fn_start_cache[key] = result
    return result


def function_extent(dis, data, sections, start_va, cap_bytes=0x10000):
    """Decode from start_va; return (end_va_exclusive, n_ins, stop_reason).

    Extent rule: linear decode; ends at the first `ret`/`retf` whose
    following bytes are padding (CC/90), or at a run of >=3 CC, or at an
    invalid instruction, or at the cap.
    """
    ins_list, stop = dis.stream(data, sections, start_va, cap_bytes, 40000)
    if not ins_list:
        return None, 0, "unmapped-or-invalid"
    off, _s = va_to_off(sections, start_va)
    if off is None:
        return None, 0, "unmapped"
    for idx, ins in enumerate(ins_list):
        ins_off = off + (ins.address - start_va)
        nxt = data[ins_off + ins.size: ins_off + ins.size + 1]
        if ins.mnemonic in ("ret", "retf", "iret", "iretd"):
            if len(nxt) < 1 or nxt[0] in (0xCC, 0x90):
                return ins.address + ins.size, idx + 1, "ret+padding"
        if data[ins_off: ins_off + 3] == b"\xCC\xCC\xCC":
            return ins.address, idx, "cc-run"
    return ins_list[-1].address + ins_list[-1].size, len(ins_list), stop


def anchor_classify(dis, data, sections, occ_va, back=32):
    """Fallback classification when no padded function start verifies:
    try decode anchors occ_va-1 .. occ_va-back; accept the first clean
    decode whose instruction CONTAINS occ_va and continues cleanly."""
    off, _s = va_to_off(sections, occ_va)
    if off is None:
        return None, "unmapped"
    best = None
    for back_i in range(1, back + 1):
        s_va = occ_va - back_i
        s_off, _s2 = va_to_off(sections, s_va)
        if s_off is None:
            continue
        ins_list, stop = dis.stream(data, sections, s_va, back_i + 64, 24)
        if stop == "invalid":
            continue
        for ins in ins_list:
            if ins.address <= occ_va < ins.address + ins.size:
                if best is None:
                    best = ins
                break
            if ins.address > occ_va:
                break
        if best is not None:
            return best, "anchor-fallback"
    return None, "no-anchor"


def classify_occurrence(dis, data, sections, occ_va):
    """For an imm32 occurrence at occ_va (in a code section), find the
    containing instruction via the (cached) function start; fall back to
    the anchor method. Returns (instruction or None, classification)."""
    start, ev = find_function_start(dis, data, sections, occ_va)
    if start is not None and start <= occ_va:
        ins_list, stop = dis.stream(data, sections, start,
                                    occ_va - start + 16, 200000)
        for ins in ins_list:
            if ins.address <= occ_va < ins.address + ins.size:
                return ins, "in-fn-0x%08X" % start
            if ins.address > occ_va:
                return None, "not-covered"
    return anchor_classify(dis, data, sections, occ_va)
