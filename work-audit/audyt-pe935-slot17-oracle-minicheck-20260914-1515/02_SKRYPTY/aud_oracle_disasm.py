# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-pe935-slot17-oracle-minicheck-20260914-1515) - plik audytora, NIE jest czescia pracy wykonawcy
# aud_oracle_disasm.py - wlasny audytorski disasm funkcji oracli GB112 (z NiMain.lib) i GB12 (z .obj).
# Weryfikuje: GB112 ctor lea +0x38/+0x6C; GB112 UWD rep movsd x13 -> +0x6C; GB12 UWD +0x8C/+0x90/+0x94/+0x98 i write +0x68;
# GB112/GB12 NiNode::GetObjectByName (call [edx+0x40] / [eax+0x48], dzieci +0xB8/+0xC0 vs +0xB4/+0xBC, name +0x0C vs +0x08).
import struct
import sys
import capstone

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)

def coff_parse(data):
    machine, nsec, tds, symptr, nsyms, optsize, chars = struct.unpack_from("<HHIIIHH", data, 0)
    strtab = symptr + nsyms * 18
    syms = [None] * nsyms
    idx = 0
    off = symptr
    while idx < nsyms:
        z = struct.unpack_from("<I", data, off)[0]
        if z == 0:
            so = struct.unpack_from("<I", data, off + 4)[0]
            s = strtab + so
            e = data.index(b"\x00", s)
            name = data[s:e].decode("ascii", "replace")
        else:
            name = data[off:off+8].rstrip(b"\x00").decode("ascii", "replace")
        val, secn, typ, cls, naux = struct.unpack_from("<IhHBB", data, off + 8)
        syms[idx] = (name, val, secn, naux)
        off += 18 * (1 + naux)
        idx += 1 + naux
    sections = []
    so = 20 + optsize
    for i in range(nsec):
        nm = data[so:so+8].rstrip(b"\x00").decode("ascii", "replace")
        vsz, va, rsz, rptr, relptr, lnptr, nrel, nln, sc = struct.unpack_from("<IIIIIIHHI", data, so + 8)
        sections.append((nm, va, rsz, rptr, relptr, nrel))
        so += 40
    return sections, syms

def find_sym_disasm(data, sections, syms, prefix, maxb=0x120):
    for s in syms:
        if s and s[0].startswith(prefix) and s[2] > 0:
            nm, val, secn, naux = s
            sec = sections[secn - 1]
            start = sec[3] + val
            code = data[start:start+maxb]
            out = []
            for ins in md.disasm(code, 0):
                out.append((ins.address, ins.mnemonic, ins.op_str))
                if ins.mnemonic in ("ret", "retn"):
                    break
            return nm, out
    return None, None

def has_seq(out, mnem, substr):
    return any(m == mnem and substr in o for a, m, o in out)

print("=== GB112 NiMain.lib: ctor NiAVObject + UWD + NiNode::GetObjectByName + NiAVObject::GetObjectByName ===")
with open(r"D:\gamebyroengine\Gamebryo 1.1.2 Evaluation\SDK\Win32\Lib\VC71\ReleaseLib\NiMain.lib", "rb") as f:
    lib = f.read()
longnames = b""
off = 8
targets_done = set()
while off + 60 <= len(lib):
    hdr = lib[off:off+60]
    rawname = hdr[0:16].decode("ascii", "replace")
    size = int(hdr[48:58].decode("ascii", "replace").strip())
    body = lib[off+60:off+60+size]
    off += 60 + size + (size & 1)
    if rawname.rstrip(" ") == "//":
        longnames = body
        continue
    if rawname.rstrip(" ").rstrip("/") == "" or rawname.rstrip(" ") == "/":
        continue
    if len(body) < 20 or struct.unpack_from("<H", body, 0)[0] != 0x014C:
        continue
    try:
        sections, syms = coff_parse(body)
    except Exception:
        continue
    for pref, checks in [
        ("??0NiAVObject@@IAE@XZ", "CTOR"),
        ("?UpdateWorldData@NiAVObject@@", "UWD"),
        ("?GetObjectByName@NiNode@@", "GBN"),
        ("?GetObjectByName@NiAVObject@@", "GBA"),
    ]:
        nm, out = find_sym_disasm(body, sections, syms, pref)
        if nm and (pref not in targets_done):
            targets_done.add(pref)
            print("MEMBER %s :: %s" % (rawname.rstrip(), nm))
            if checks == "CTOR":
                print("  lea ecx,[esi+0x38]:", has_seq(out, "lea", "esi + 0x38"))
                print("  lea ecx,[esi+0x6c]:", has_seq(out, "lea", "esi + 0x6c"))
                print("  mov word [esi+0x20]:", has_seq(out, "mov", "word ptr [esi + 0x20]"))
                print("  mov [esi+0x24]:", has_seq(out, "mov", "[esi + 0x24]"))
                print("  lea eax,[esi+0x28]:", has_seq(out, "lea", "esi + 0x28"))
                print("  store 0xa0:", has_seq(out, "mov", "[esi + 0xa0]"))
                print("  store 0xb0:", has_seq(out, "mov", "[esi + 0xb0]"))
            elif checks == "UWD":
                print("  mov eax,[ebx+0x24]:", has_seq(out, "mov", "[ebx + 0x24]"))
                print("  lea ecx,[ebx+0x38]:", has_seq(out, "lea", "ebx + 0x38"))
                print("  lea ecx,[eax+0x6c]:", has_seq(out, "lea", "eax + 0x6c"))
                print("  lea edi,[ebx+0x6c]:", has_seq(out, "lea", "ebx + 0x6c"))
                print("  mov ecx,0xd:", has_seq(out, "mov", "ecx, 0xd"))
                print("  rep movsd:", has_seq(out, "rep", "movsd"))
                print("  [ebx+0xb0]:", has_seq(out, "mov", "[ebx + 0xb0]"))
                print("  call [eax+0x38]:", has_seq(out, "call", "[eax + 0x38]"))
            elif checks == "GBN":
                print("  mov ebx,[esp+8]:", has_seq(out, "mov", "[esp + 8]"))
                print("  mov eax,[edi+0xc0]:", has_seq(out, "mov", "[edi + 0xc0]"))
                print("  mov eax,[edi+0xb8]:", has_seq(out, "mov", "[edi + 0xb8]"))
                print("  call [edx+0x40]:", has_seq(out, "call", "[edx + 0x40]"))
                print("  ret 4:", has_seq(out, "ret", "4"))
                print("  inc esi:", has_seq(out, "inc", "esi"))
            elif checks == "GBA":
                print("  mov esi,[edi+0xc]:", has_seq(out, "mov", "[edi + 0xc]"))
                print("  ret 4:", has_seq(out, "ret", "4"))

print("")
print("=== GB12 .obj ===")
for fn in ["NiAVObject", "NiAVObject_Win32", "NiNode"]:
    with open(r"D:\gamebyroengine\extracted\gb12_build\build\NiMain\%s.obj" % fn, "rb") as f:
        data = f.read()
    sections, syms = coff_parse(data)
    if fn == "NiAVObject":
        nm, out = find_sym_disasm(data, sections, syms, "??0NiAVObject@@IAE@XZ")
        print("%s :: %s" % (fn, nm))
        print("  lea ecx,[esi+0x34]:", has_seq(out, "lea", "esi + 0x34"))
        print("  lea ecx,[esi+0x68]:", has_seq(out, "lea", "esi + 0x68"))
        print("  mov word [esi+0x1c]:", has_seq(out, "mov", "word ptr [esi + 0x1c]"))
        print("  mov [esi+0x20]:", has_seq(out, "mov", "[esi + 0x20]"))
        print("  movq [esi+0x24]:", has_seq(out, "movq", "[esi + 0x24]"))
        print("  store 0x9c:", has_seq(out, "mov", "[esi + 0x9c]"))
        print("  store 0xac:", has_seq(out, "mov", "[esi + 0xac]"))
        nm, out = find_sym_disasm(data, sections, syms, "?GetObjectByName@NiAVObject@@")
        print("%s :: %s" % (fn, nm))
        print("  mov eax,[esi+8]:", has_seq(out, "mov", "[esi + 8]"))
        print("  ret 4:", has_seq(out, "ret", "4"))
    if fn == "NiAVObject_Win32":
        nm, out = find_sym_disasm(data, sections, syms, "?UpdateWorldData@NiAVObject@@")
        print("%s :: %s" % (fn, nm))
        print("  mov esi,[edi+0x20]:", has_seq(out, "mov", "[edi + 0x20]"))
        print("  lea ebx,[edi+0x34]:", has_seq(out, "lea", "edi + 0x34"))
        print("  addss xmm2,[esi+0x8c]:", has_seq(out, "addss", "[esi + 0x8c]"))
        print("  addss xmm0,[esi+0x90]:", has_seq(out, "addss", "[esi + 0x90]"))
        print("  addss xmm1,[esi+0x94]:", has_seq(out, "addss", "[esi + 0x94]"))
        print("  mulss xmm1,[esi+0x98]:", has_seq(out, "mulss", "[esi + 0x98]") or has_seq(out, "movss", "[esi + 0x98]"))
        print("  write [edi+0x68]:", has_seq(out, "movups", "[edi + 0x68]"))
        print("  collision [edi+0xac]:", has_seq(out, "mov", "[edi + 0xac]"))
        print("  call [eax+0x40]:", has_seq(out, "call", "[eax + 0x40]"))
    if fn == "NiNode":
        nm, out = find_sym_disasm(data, sections, syms, "?GetObjectByName@NiNode@@")
        print("%s :: %s" % (fn, nm))
        print("  mov ebx,[esp+8]:", has_seq(out, "mov", "[esp + 8]"))
        print("  mov eax,[edi+0xbc]:", has_seq(out, "mov", "[edi + 0xbc]"))
        print("  mov eax,[edi+0xb4]:", has_seq(out, "mov", "[edi + 0xb4]"))
        print("  call [eax+0x48]:", has_seq(out, "call", "[eax + 0x48]"))
        print("  ret 4:", has_seq(out, "ret", "4"))


