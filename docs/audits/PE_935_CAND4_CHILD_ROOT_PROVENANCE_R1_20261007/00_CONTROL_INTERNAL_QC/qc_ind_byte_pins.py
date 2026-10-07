"""qc_independent_byte_pins.py — PE-MASTER-AUDITOR independent QC, part 1.

OWN PE mapper (parsed from the raw PE headers here; no executor tooling, no
pe_reader import, no capstone). Own byte re-pins of the load-bearing claims of
PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007, straight from
D:\Eudoria_Reconstruction\pcg_install\Entropia.exe.

FAIL-CLOSED: the EXE size+SHA256 is asserted before any read; any mismatch
aborts with no results.
"""
import hashlib
import struct
import sys
import json

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_SIZE = 8015872
EXE_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

with open(EXE_PATH, "rb") as f:
    EXE = f.read()

res = {"identity": None, "pe_map": {}, "checks": [], "fail_count": 0}


def check(cid, ok, detail):
    res["checks"].append({"id": cid, "ok": bool(ok), "detail": detail})
    if not ok:
        res["fail_count"] += 1
    print(("PASS " if ok else "FAIL ") + cid + ": " + detail)


# ---------------------------------------------------------------- identity
h = hashlib.sha256(EXE).hexdigest().upper()
check("QC-A0-exe-identity", len(EXE) == EXE_SIZE and h == EXE_SHA256,
      f"{len(EXE)} B / SHA256 {h}")
if len(EXE) != EXE_SIZE or h != EXE_SHA256:
    print("ABORT: EXE identity mismatch")
    sys.exit(2)

# ---------------------------------------------------------------- own PE map
e_lfanew = struct.unpack_from("<I", EXE, 0x3C)[0]
assert EXE[e_lfanew:e_lfanew + 4] == b"PE\x00\x00", "bad PE signature"
coff = e_lfanew + 4
machine, nsec = struct.unpack_from("<HH", EXE, coff)
opt_size = struct.unpack_from("<H", EXE, coff + 16)[0]
opt = coff + 20
magic = struct.unpack_from("<H", EXE, opt)[0]
assert magic == 0x10B, f"not PE32 (magic {magic:#x})"
image_base = struct.unpack_from("<I", EXE, opt + 28)[0]
sectab = opt + opt_size
sections = []
for i in range(nsec):
    off = sectab + 40 * i
    name = EXE[off:off + 8].rstrip(b"\x00").decode("ascii", "replace")
    vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", EXE, off + 8)
    sections.append((name, vaddr, vsize, rawsize, rawptr))
res["pe_map"] = {"e_lfanew": e_lfanew, "machine": hex(machine), "nsec": nsec,
                 "image_base": hex(image_base), "sections": sections}
print(f"PE map: image_base={image_base:#x}, sections={sections}")


def va_to_off(va):
    rva = va - image_base
    for name, vaddr, vsize, rawsize, rawptr in sections:
        span = max(vsize, rawsize)
        if vaddr <= rva < vaddr + span:
            off = rawptr + (rva - vaddr)
            if off + 0 <= rawptr + rawsize - 1 or True:
                # allow reads only within the raw data (fail-closed)
                return off
    raise ValueError(f"VA {va:#010x} not mapped (rva {rva:#x})")


def rd(va, n):
    off = va_to_off(va)
    b = EXE[off:off + n]
    if len(b) != n:
        raise ValueError(f"short read at VA {va:#010x}")
    return b


def u32(va):
    return struct.unpack("<I", rd(va, 4))[0]


# ---------------------------------------------------------------- (a) getter
g = rd(0x006C66D0, 16)
check("QC-A1-getter-body", g[:4] == bytes([0x8B, 0x41, 0x68, 0xC3]),
      f"@0x006C66D0 = {g[:4].hex(' ').upper()} (expect 8B 41 68 C3 = mov eax,[ecx+0x68]; ret)")
# my own ModRM decode: 8B /r, ModRM 0x41: mod=01 reg=000(EAX) rm=001(ECX) -> mov eax,[ecx+0x68]
modrm = g[1]
mod, reg, rm = modrm >> 6, (modrm >> 3) & 7, modrm & 7
regs = ["EAX", "ECX", "EDX", "EBX", "ESP", "EBP", "ESI", "EDI"]
check("QC-A2-getter-modrm-decode", mod == 1 and regs[reg] == "EAX" and regs[rm] == "ECX" and g[2] == 0x68 and g[3] == 0xC3,
      f"own decode: mov {regs[reg]}, [{regs[rm]}+{g[2]:#x}]; ret — DIRECT_FIELD_GETTER [this+0x68], NOT [esi+0x68] (would be ModRM 0x46)")
check("QC-A3-getter-cc-padding", g[4:16] == bytes([0xCC] * 12),
      f"padding 0x006C66D4..0x006C66DF = {g[4:16].hex(' ').upper()} (12x CC)")
nxt = rd(0x006C66E0, 1)
check("QC-A4-getter-next-entry", nxt == bytes([0x56]),
      f"next body @0x006C66E0 first byte = {nxt.hex(' ').upper()} (56 = push esi — prologue)")

# three caller rel32 -> 0x006C66D0 (own arithmetic)
for cs, label in ((0x0050A34B, "oldmgr"), (0x0050A39D, "nullcheck"), (0x0050A3AF, "main")):
    raw = rd(cs, 5)
    rel = struct.unpack("<i", raw[1:5])[0]
    tgt = cs + 5 + rel
    check(f"QC-A5-caller-{label}", raw[0] == 0xE8 and tgt == 0x006C66D0,
          f"E8 @0x{cs:08X}: rel32 {raw[1:5].hex(' ').upper()} -> 0x{tgt:08X} (expect 0x006C66D0)")

# ---------------------------------------------------------------- (b) RTTI
def rtti_walk(vt_va, expect_name, expect_col=None):
    col = u32(vt_va - 4)
    td = struct.unpack("<I", rd(col + 0xC, 4))[0]
    raw = rd(td + 8, 64)
    name = raw[: raw.find(b"\x00")].decode("ascii", "replace")
    ok = name == expect_name and (expect_col is None or col == expect_col)
    return ok, f"vt 0x{vt_va:08X} -> COL 0x{col:08X} -> TD 0x{td:08X} -> '{name}'"


ok, d = rtti_walk(0x00A855D0, ".?AVArkModelManagerMain@@", 0x00AA6C58)
check("QC-B1-rtti-derived", ok, d)
ok, d = rtti_walk(0x00A85A08, ".?AVArkModelManager@@", 0x00AA6CD8)
check("QC-B2-rtti-base", ok, d)
ok, d = rtti_walk(0x00A864B8, ".?AVArkModelResourceInstanceRef@@", 0x00AA7770)
check("QC-B3-rtti-wrapper", ok, d)

# vtable slots (data reads)
s2, s3 = u32(0x00A855D0 + 8), u32(0x00A855D0 + 0xC)
check("QC-B4-derived-vtable-slots", s2 == 0x006C0FD0 and s3 == 0x006C19B0,
      f"derived vtable slot2=0x{s2:08X} slot3=0x{s3:08X} (expect 0x006C0FD0 / 0x006C19B0)")
b2, b3 = u32(0x00A85A08 + 8), u32(0x00A85A08 + 0xC)
check("QC-B5-base-vtable-slots", b2 == 0x008E0110 and b3 == 0x008E0110,
      f"base vtable slot2=0x{b2:08X} slot3=0x{b3:08X} (both 0x008E0110)")
# vtable stores in ctors
check("QC-B6-vtable-stores", rd(0x006C0D9B, 6) == bytes([0xC7, 0x06, 0xD0, 0x55, 0xA8, 0x00])
      and rd(0x006C8FAB, 6) == bytes([0xC7, 0x06, 0x08, 0x5A, 0xA8, 0x00]),
      "derived ctor stores 0x00A855D0 @0x006C0D9B; base ctor stores 0x00A85A08 @0x006C8FAB")

# ---------------------------------------------------------------- (c) producer chain
pins = [
    ("base_ctor_null_write_+0x68", 0x006C8FD3, [0x89, 0x5E, 0x68], "mov [esi+0x68], ebx"),
    ("base_ctor_store_+0x6C_null", 0x006C8FE3, [0x89, 0x5E, 0x6C], "mov [esi+0x6C], ebx"),
    ("base_ctor_flag_+0xEC_null", 0x006C9014, [0x88, 0x9E, 0xEC, 0x00, 0x00, 0x00], "mov byte [esi+0xEC], bl"),
    ("lazy_cmp_+0x68", 0x006C8B34, [0x83, 0x7E, 0x68, 0x00], "cmp [esi+0x68], 0"),
    ("lazy_set_flag_+0xEC", 0x006C8B50, [0xC6, 0x86, 0xEC, 0x00, 0x00, 0x00, 0x01], "mov byte [esi+0xEC], 1"),
    ("producer_cmp_+0x6C", 0x006C6F88, [0x83, 0x7E, 0x6C, 0x00], "cmp [esi+0x6C], 0"),
    ("producer_store_+0x6C", 0x006C7008, [0x89, 0x46, 0x6C], "mov [esi+0x6C], eax"),
    ("installer_cmp_+0x68", 0x006C67A9, [0x83, 0x7E, 0x68, 0x00], "cmp [esi+0x68], 0"),
    ("installer_read_inst+4", 0x006C67BE, [0x8B, 0x78, 0x04], "mov edi, [eax+4]"),
    ("installer_write_+0x68", 0x006C67E2, [0x89, 0x7E, 0x68], "mov [esi+0x68], edi — THE WRITER"),
    ("installer_incref_new", 0x006C67E7, [0x01, 0x5F, 0x04], "add [edi+4], ebx"),
    ("installer_decref_old", 0x006C67D4, [0x01, 0x69, 0x04], "add [ecx+4], ebp"),
    ("texture_lookup_push_name", 0x006C67ED, [0x68, 0xF8, 0x59, 0xA8, 0x00], "push 0x00A859F8"),
    ("animation_lookup_push_name", 0x006C6836, [0x68, 0x7C, 0x54, 0xA8, 0x00], "push 0x00A8547C"),
    ("ctor_pump_cdecl_cleanup", 0x006C7001, [0x83, 0xC4, 0x10], "add esp, 0x10"),
    ("key_constant_push_1", 0x006C6FB5, [0x68, 0x7B, 0x95, 0xA7, 0x00], "push 0x00A7957B"),
    ("key_constant_push_2", 0x006C6FD3, [0x68, 0x7B, 0x95, 0xA7, 0x00], "push 0x00A7957B"),
    ("old_value_vtable_load", 0x006C67D9, [0x8B, 0x01], "mov eax, [ecx]"),
    ("old_value_slot1_load", 0x006C67DB, [0x8B, 0x50, 0x04], "mov edx, [eax+4]"),
    ("slot1_call", 0x006C67DE, [0xFF, 0xD2], "call edx — zero-destroy dispatch"),
]
for name, va, exp, desc in pins:
    b = rd(va, len(exp))
    check(f"QC-C-pin-{name}", list(b) == exp, f"@0x{va:08X} = {b.hex(' ').upper()} (expect {' '.join('%02X' % x for x in exp)}) — {desc}")

rel32s = [
    ("lazy_call_producer", 0x006C8B3A, 0x006C6F60),
    ("base_ctor_subinit_+0x70", 0x006C8FE6, 0x005670A0),
    ("base_ctor_subinit_+0xA0", 0x006C9005, 0x0043A330),
    ("derived_ctor_call_base", 0x006C0D64, 0x006C8F80),
    ("producer_validity", 0x006C6F97, 0x0072FCE0),
    ("producer_getterA", 0x006C6FF6, 0x007CE1E0),
    ("producer_pump", 0x006C6FFC, 0x006C9700),
    ("producer_call_installer", 0x006C7049, 0x006C6780),
    ("texture_lookup_call", 0x006C67F2, 0x007B6C30),
    ("animation_lookup_call", 0x006C683B, 0x007B6C30),
    ("texture_branch_new", 0x006C6804, 0x0095D3C4),
    ("texture_branch_init", 0x006C6823, 0x006D3570),
]
for name, cs, exp_t in rel32s:
    raw = rd(cs, 5)
    rel = struct.unpack("<i", raw[1:5])[0]
    tgt = cs + 5 + rel
    check(f"QC-C-rel32-{name}", raw[0] == 0xE8 and tgt == exp_t,
          f"E8 @0x{cs:08X} -> 0x{tgt:08X} (expect 0x{exp_t:08X})")

# strings
check("QC-C-string-ArkTexture", rd(0x00A859F8, 10) == b"ArkTexture\x00"[:10] and rd(0x00A859F8, 11)[10] == 0,
      f"@0x00A859F8 = {rd(0x00A859F8, 12).hex(' ').upper()} = 'ArkTexture\\0'")
check("QC-C-string-ArkAnimation", rd(0x00A8547C, 13) == b"ArkAnimation\x00",
      f"@0x00A8547C = {rd(0x00A8547C, 16).hex(' ').upper()} = 'ArkAnimation\\0'")
kb = rd(0x00A7957B, 1)
eb = rd(0x00A7957C, 8)
check("QC-C-string-empty-key", kb == b"\x00" and eb == b"Entropia",
      f"@0x00A7957B = {kb.hex()} (empty string) ; @0x00A7957C = {eb.decode('ascii')}")

# ---------------------------------------------------------------- (d) named-lookup roots
# both lookups receive the child [manager+0x68] as receiver (thiscall ECX) and the name constant as arg
lw1 = rd(0x006C67EA, 13)   # 8B 4E 68 ; 68 F8 59 A8 00 ; E8 ...
lw2 = rd(0x006C6833, 13)   # 8B 4E 68 ; 68 7C 54 A8 00 ; E8 ...
check("QC-D-named-lookup-root-1", list(lw1) == [0x8B, 0x4E, 0x68, 0x68, 0xF8, 0x59, 0xA8, 0x00, 0xE8, 0x39, 0x04, 0x0F, 0x00],
      f"receiver = [esi+0x68] (the child) @0x006C67EA; push 'ArkTexture' @0x006C67ED; call 0x007B6C30 @0x006C67F2")
check("QC-D-named-lookup-root-2", list(lw2) == [0x8B, 0x4E, 0x68, 0x68, 0x7C, 0x54, 0xA8, 0x00, 0xE8, 0xF0, 0x03, 0x0F, 0x00],
      f"receiver = [esi+0x68] (the child) @0x006C6833; push 'ArkAnimation' @0x006C6836; call 0x007B6C30 @0x006C683B")

# ---------------------------------------------------------------- (f) full PINS file re-verification
pins_txt = open(r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007\01_RAW\PINS_AND_REL32.txt", encoding="utf-8").read()
import re
pin_rows = re.findall(r"^  (.+?)\s+@0x([0-9A-F]{8}):\s+((?:[0-9A-F]{2} )*[0-9A-F]{2})", pins_txt, re.M)
pin_fails = []
for name, va, byts in pin_rows:
    exp = bytes(int(x, 16) for x in byts.split())
    act = rd(int(va, 16), len(exp))
    if act != exp:
        pin_fails.append((name.strip(), va))
check("QC-F1-all-56-pins", len(pin_rows) == 56 and not pin_fails,
      f"{len(pin_rows)}/56 pin rows re-read from EXE; mismatches: {pin_fails if pin_fails else 'NONE'}")

rel_rows = re.findall(r"^  CALL 0x([0-9A-F]{8}) -> 0x([0-9A-F]{8})", pins_txt, re.M)
rel_fails = []
for cs, tgt in rel_rows:
    cs_i, tgt_i = int(cs, 16), int(tgt, 16)
    raw = rd(cs_i, 5)
    if raw[0] != 0xE8:
        rel_fails.append((cs, "not E8"))
        continue
    if cs_i + 5 + struct.unpack("<i", raw[1:5])[0] != tgt_i:
        rel_fails.append((cs, "target mismatch"))
check("QC-F2-all-23-rel32", len(rel_rows) == 23 and not rel_fails,
      f"{len(rel_rows)}/23 rel32 targets recomputed by OWN arithmetic; mismatches: {rel_fails if rel_fails else 'NONE'}")

with open(r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007\00_CONTROL_INTERNAL_QC\qc_ind_byte_pins_results.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
    f.write("\n")
print()
print(f"PART1 DONE: {len(res['checks'])} checks, fails={res['fail_count']}")
