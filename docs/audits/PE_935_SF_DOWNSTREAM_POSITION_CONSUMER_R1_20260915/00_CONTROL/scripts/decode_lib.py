"""decode_lib.py — shared PE loader + capstone decode helpers (run-local, PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915).

Read-only on D:/Eudoria_Reconstruction/pcg_install/Entropia.exe.
Every generated raw file must call lib.measured_env() and print it in its header.
"""
import struct
import sys

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
PIN_SIZE = 8015872
PIN_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
PIN_IMAGEBASE = 0x00400000


def _fail_closed_check(data):
    import hashlib
    if len(data) != PIN_SIZE:
        raise SystemExit("S0 FAIL-CLOSED: size %d != pin %d" % (len(data), PIN_SIZE))
    sha = hashlib.sha256(data).hexdigest().upper()
    if sha != PIN_SHA256:
        raise SystemExit("S0 FAIL-CLOSED: sha256 %s != pin %s" % (sha, PIN_SHA256))
    e = struct.unpack_from("<I", data, 0x3C)[0]
    if data[e:e + 4] != b"PE\x00\x00":
        raise SystemExit("S0 FAIL-CLOSED: bad PE sig")
    mach = struct.unpack_from("<H", data, e + 4)[0]
    if mach != 0x14C:
        raise SystemExit("S0 FAIL-CLOSED: machine %#x != i386" % mach)
    magic = struct.unpack_from("<H", data, e + 24)[0]
    if magic != 0x10B:
        raise SystemExit("S0 FAIL-CLOSED: not PE32")
    imagebase = struct.unpack_from("<I", data, e + 24 + 28)[0]
    if imagebase != PIN_IMAGEBASE:
        raise SystemExit("S0 FAIL-CLOSED: imagebase %#x != %#x" % (imagebase, PIN_IMAGEBASE))
    nsec = struct.unpack_from("<H", data, e + 6)[0]
    secs = []
    for i in range(nsec):
        off = e + 24 + 224 + i * 40
        nm = data[off:off + 8].rstrip(b"\x00").decode("ascii")
        vs, va, rs, ro = struct.unpack_from("<IIII", data, off + 8)
        secs.append((nm, va, vs, ro, rs))
    return sha, secs


class Image:
    def __init__(self):
        with open(EXE_PATH, "rb") as f:
            self.data = f.read()
        self.sha256, self.sections = _fail_closed_check(self.data)
        self.imagebase = PIN_IMAGEBASE

    def va_to_off(self, va):
        rva = va - self.imagebase
        for nm, va_s, vs, ro, rs in self.sections:
            if va_s <= rva < va_s + vs:
                if rva - va_s < rs:  # within raw data
                    return ro + (rva - va_s)
                return None  # in virtual-only tail (uninitialized)
        raise ValueError("VA %#x not in any section" % va)

    def read(self, va, n):
        off = self.va_to_off(va)
        if off is None:
            raise ValueError("VA %#x has no raw backing" % va)
        return self.data[off:off + n]

    def is_executable_section(self, va):
        rva = va - self.imagebase
        for nm, va_s, vs, ro, rs in self.sections:
            if nm == ".text" and va_s <= rva < va_s + vs:
                return True
        return False


def measured_env(img=None):
    import capstone
    lines = []
    lines.append("python: %s" % sys.version.replace("\n", " "))
    lines.append("python_exe: %s" % sys.executable)
    lines.append("capstone: %s (cs_version=%s)" % (capstone.__version__, capstone.cs_version()))
    if img is not None:
        lines.append("source: %s" % EXE_PATH)
        lines.append("source_size: %d" % PIN_SIZE)
        lines.append("source_sha256_measured: %s" % img.sha256)
        lines.append("source_sha256_pin: %s (MATCH)" % PIN_SHA256)
        lines.append("imagebase: %#x (i386 PE32, S0 fail-closed verified at script start)" % PIN_IMAGEBASE)
    return "\n".join(lines)


def make_disassembler():
    import capstone
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.detail = True
    return md


def fmt_ins(ins):
    bs = " ".join("%02x" % b for b in ins.bytes)
    return "0x%08X  %-24s  %-8s %s" % (ins.address, bs, ins.mnemonic, ins.op_str)


def disasm_range(md, img, start_va, end_va):
    """Linear decode of [start_va, end_va). Returns list of instructions."""
    code = img.read(start_va, end_va - start_va)
    out = []
    for ins in md.disasm(code, start_va):
        out.append(ins)
    return out


TERMINAL_MNEMONICS = {"ret", "retf", "iretd", "hlt", "ud2"}


def decode_function(md, img, start_va, max_len=0x2000):
    """Decode forward from start_va until a terminal instruction, then measure
    padding after the terminal (terminal+padding rule for extent)."""
    code = img.read(start_va, max_len)
    ins_list = []
    term_idx = None
    pos = 0
    for ins in md.disasm(code, start_va):
        ins_list.append(ins)
        if ins.mnemonic in TERMINAL_MNEMONICS or (ins.mnemonic == "jmp" and ins.operands and ins.op_str.startswith("0x")):
            # unconditional jmp to a fixed target outside window = terminal candidate too,
            # but for extent purposes we stop at first ret/jmp-family terminal; caller decides.
            term_idx = len(ins_list) - 1
            break
        pos += ins.size
    if term_idx is None:
        raise SystemExit("no terminal instruction found within %#x bytes from %#x" % (max_len, start_va))
    term = ins_list[term_idx]
    end_after_term = term.address + term.size
    # padding after terminal: CC (int3) or 00 or 90 until next non-padding
    pad_start = end_after_term
    pad_bytes = img.read(pad_start, 16)
    pad_classified = []
    pad_end = pad_start
    for b in pad_bytes:
        if b in (0xCC, 0x00, 0x90):
            pad_classified.append(b)
            pad_end += 1
        else:
            break
    return ins_list, term, pad_start, pad_end, pad_classified


def scan_calls(img, target_va, limit_sections=(".text",)):
    """Scan .text for E8/E9 rel32 whose effective target == target_va.
    Also scan for imm32 occurrences of target_va (address-takers)."""
    import capstone
    out_e8 = []
    out_e9 = []
    out_imm32 = []
    for nm, va_s, vs, ro, rs in img.sections:
        if nm not in limit_sections:
            continue
        raw = img.data[ro:ro + rs]
        base_va = img.imagebase + va_s
        # E8/E9 rel32
        for i in range(len(raw) - 5):
            op = raw[i]
            if op == 0xE8 or op == 0xE9:
                rel = struct.unpack_from("<i", raw, i + 1)[0]
                src = base_va + i
                tgt = src + 5 + rel
                if tgt == target_va:
                    (out_e8 if op == 0xE8 else out_e9).append(src)
        # imm32 address-takers (exclude E8/E9 encodings already found)
    for nm, va_s, vs, ro, rs in img.sections:
        if nm not in limit_sections:
            continue
        raw = img.data[ro:ro + rs]
        base_va = img.imagebase + va_s
        tgt_le = struct.pack("<I", target_va)
        idx = 0
        while True:
            j = raw.find(tgt_le, idx)
            if j < 0:
                break
            src = base_va + j
            # skip if this imm32 is the operand of an E8/E9 at j-1
            if j >= 1 and raw[j - 1] in (0xE8, 0xE9):
                idx = j + 1
                continue
            out_imm32.append(src)
            idx = j + 1
    return sorted(out_e8), sorted(out_e9), sorted(out_imm32)


def scan_pattern_calls(img, target_va):
    """imm32 occurrences of target_va in the WHOLE image (all sections), with section attribution."""
    res = []
    for nm, va_s, vs, ro, rs in img.sections:
        raw = img.data[ro:ro + rs]
        base_va = img.imagebase + va_s
        tgt_le = struct.pack("<I", target_va)
        idx = 0
        while True:
            j = raw.find(tgt_le, idx)
            if j < 0:
                break
            res.append((nm, base_va + j))
            idx = j + 1
    return res
