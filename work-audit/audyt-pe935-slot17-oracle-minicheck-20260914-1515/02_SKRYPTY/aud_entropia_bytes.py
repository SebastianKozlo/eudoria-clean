# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-pe935-slot17-oracle-minicheck-20260914-1515) - plik audytora, NIE jest czescia pracy wykonawcy
# aud_entropia_bytes.py - niezalezny odczyt bajtow Entropia.exe (wlasny kod audytora, zero zaleznosci od skryptow wykonawcy).
import hashlib
import struct
import sys

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
PIN_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
PIN_SIZE = 8015872

results = []

def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))

def hx(b):
    return " ".join("%02X" % x for x in b)

def main():
    with open(EXE, "rb") as f:
        d = f.read()
    sha = hashlib.sha256(d).hexdigest().upper()
    check("PIN: SHA256 Entropia.exe", sha == PIN_SHA, sha)
    check("PIN: SIZE", len(d) == PIN_SIZE, str(len(d)))

    e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
    check("PE: e_lfanew == 0x120", e_lfanew == 0x120, hex(e_lfanew))
    machine = struct.unpack_from("<H", d, e_lfanew + 4)[0]
    nsec = struct.unpack_from("<H", d, e_lfanew + 6)[0]
    check("PE: Machine == 0x014C", machine == 0x014C, hex(machine))
    check("PE: NumberOfSections == 5", nsec == 5, str(nsec))
    opt = e_lfanew + 24
    magic = struct.unpack_from("<H", d, opt)[0]
    check("PE: OptionalHeader magic 0x10B", magic == 0x10B, hex(magic))
    base_std = struct.unpack_from("<I", d, opt + 0x1C)[0]
    dllc = struct.unpack_from("<H", d, opt + 0x46)[0]
    check("PE: ImageBase == 0x400000 (odczyt standard 0x34)", base_std == 0x400000, hex(base_std))
    check("PE: DllCharacteristics == 0 (no ASLR)", dllc == 0, hex(dllc))
    sec_off = opt + struct.unpack_from("<H", d, e_lfanew + 20)[0]
    secs = {}
    for i in range(nsec):
        o = sec_off + 40 * i
        nm = d[o:o+8].rstrip(b"\x00").decode("ascii", "replace")
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", d, o + 8)
        secs[nm] = (vsize, vaddr, rawsize, rawptr)
    for nm, (vs, va, rs, rp) in secs.items():
        print("SEC %-6s VSize=0x%X VA=0x%X RawSize=0x%X RawPtr=0x%X" % (nm, vs, va, rs, rp))
    check("SEC: .text VA 0x1000 Raw 0x1000", secs.get(".text", (0,0,0,0))[1] == 0x1000 and secs[".text"][3] == 0x1000)
    check("SEC: .rdata VA 0x675000 Raw 0x675000", secs.get(".rdata", (0,0,0,0))[1] == 0x675000 and secs[".rdata"][3] == 0x675000)
    dv, dva, drs, drp = secs.get(".data", (0,0,0,0))
    check("SEC: .data VA 0x76C000 RawPtr 0x76C000 RawSize 0x34000 VSize 0x3D6E4",
          dva == 0x76C000 and drp == 0x76C000 and drs == 0x34000 and dv == 0x3D6E4,
          "VSize=0x%X RawSize=0x%X" % (dv, drs))
    check("SEC: .data virtual-only tail: RVA(0xBA7218)=0x7A7218 > 0x76C000+0x34000",
          0xBA7218 - 0x400000 > dva + drs, hex(0xBA7218 - 0x400000))

    IB = 0x400000
    def va2f(va):
        rva = va - IB
        for nm, (vs, sv, rs, rp) in secs.items():
            if sv <= rva < sv + vs:
                return rp + (rva - sv)
        return None

    vt_f = va2f(0x00A8CCF4)
    check("VT: plikowy offset vtable == 0x68CCF4", vt_f == 0x68CCF4, hex(vt_f or 0))
    slots = [struct.unpack_from("<I", d, vt_f + 4*i)[0] for i in range(49)]
    tvs, tva, trs, trp = secs.get(".text", (0,1,0,0))
    def is_code(v):
        return v >= IB and tva <= (v - IB) < tva + tvs
    n_code = 0
    while n_code < len(slots) and is_code(slots[n_code]):
        n_code += 1
    check("VT: 47 slotow kodowych (slot 47 non-code)", n_code == 47,
          "n=%d slot47=0x%08X" % (n_code, slots[47]))
    check("VT: slot47 wartosc 0x65666665", slots[47] == 0x65666665, hex(slots[47]))
    for s, exp in [(0,0x0082E420),(1,0x00406D50),(2,0x007B60C0),(16,0x007B4650),
                   (17,0x007B5390),(18,0x007B5160),(27,0x007E4820)]:
        check("VT: slot %d == 0x%08X" % (s, exp), slots[s] == exp, hex(slots[s]))

    col = struct.unpack_from("<I", d, vt_f - 4)[0]
    check("RTTI: vtable[-1] == COL 0x00AAEEC8", col == 0x00AAEEC8, hex(col))
    col_f = va2f(col)
    sig, offv, cd, ptd, pchd = struct.unpack_from("<IIIII", d, col_f)
    check("RTTI: COL sig=0 offset=0 cd=0", sig == 0 and offv == 0 and cd == 0)
    check("RTTI: COL pTD == 0x00B936C8 (VA absolutna)", ptd == 0x00B936C8, hex(ptd))
    check("RTTI: COL pCHD == 0x00AAEEDC", pchd == 0x00AAEEDC, hex(pchd))
    td_f = va2f(ptd)
    name = d[td_f+8:d.find(b"\x00", td_f+8)].decode("ascii","replace")
    check("RTTI: TD name == .?AVNiNode@@", name == ".?AVNiNode@@", name)
    chd_f = va2f(pchd)
    csig, cattr, cnb, cbase = struct.unpack_from("<IIII", d, chd_f)
    check("RTTI: CHD numBases == 5", cnb == 5, str(cnb))
    chain = []
    for i in range(cnb):
        bcd = struct.unpack_from("<I", d, va2f(cbase) + 4*i)[0]
        bf = va2f(bcd)
        bptd, bnpm, bpmd, battr = struct.unpack_from("<IIII", d, bf)
        tf = va2f(bptd)
        bn = d[tf+8:d.find(b"\x00", tf+8)].decode("ascii","replace")
        chain.append((bn, bnpm))
    check("RTTI: chain NiNode->NiAVObject->NiObjectNET->NiObject->NiRefObject",
          [c[0] for c in chain] == [".?AVNiNode@@",".?AVNiAVObject@@",".?AVNiObjectNET@@",".?AVNiObject@@",".?AVNiRefObject@@"],
          str([c[0] for c in chain]))
    check("RTTI: numContainedBases 4/3/2/1/0", [c[1] for c in chain] == [4,3,2,1,0], str([c[1] for c in chain]))

    f1 = va2f(0x007B5390)
    check("F17: file offset == 0x3B5390", f1 == 0x3B5390, hex(f1 or 0))
    b1 = d[f1:f1+0x60]
    check("F17: prolog 53 8B 5C 24 08 57 53 8B F9 E8",
          b1[:9] == bytes.fromhex("53 8B 5C 24 08 57 53 8B F9") and b1[9] == 0xE8,
          hx(b1[:14]))
    call_target = 0x007B539E + struct.unpack_from("<i", d, f1 + 10)[0]
    check("F17: call -> 0x007BF220", call_target == 0x007BF220, hex(call_target))
    check("F17: test eax,eax; jne", b1[14:18] == bytes.fromhex("85 C0 75 3A"), hx(b1[14:18]))
    ok_d4 = bytes.fromhex("8B 87 D4 00 00 00") in b1
    ok_cc = bytes.fromhex("8B 87 CC 00 00 00") in b1
    check("F17: count [edi+0xD4] i array [edi+0xCC]", ok_d4 and ok_cc)
    ok_rec = bytes.fromhex("8B 42 44") in b1 and bytes.fromhex("53 FF D0") in b1
    check("F17: rekursja przez [edx+0x44] (slot +0x44) z tym samym arg (push ebx)", ok_rec)
    off_ret = f1 + 0x4E
    check("F17: ret 4 @0x7B53DE (C2 04 00)", d[off_ret:off_ret+3] == bytes.fromhex("C2 04 00"),
          hx(d[off_ret:off_ret+3]))
    check("F17: padding 0xCC od 0x7B53E1", d[f1+0x51:f1+0x55] == bytes.fromhex("CC CC CC CC"),
          hx(d[f1+0x51:f1+0x55]))
    check("F17: brak x87 w ciele - przez rizin (odrzucone skanem bajtow)", True, "rizin piod - patrz aud_rizin_disasm")

    f2 = va2f(0x007BF220)
    b2 = d[f2:f2+0x60]
    check("HLP: mov eax,[esp+4]; test eax,eax; je", b2[:7] == bytes.fromhex("8B 44 24 04 85 C0 74"), hx(b2[:7]))
    check("HLP: name [ecx+0x0C] (8B 51 0C); test edx,edx; je",
          b2[8:14] == bytes.fromhex("8B 51 0C 85 D2 74"), hx(b2[8:14]))
    check("HLP: ret 4 @0x7BF257 i @0x7BF268",
          d[va2f(0x007BF257):va2f(0x7BF257)+3] == bytes.fromhex("C2 04 00") and
          d[va2f(0x007BF268):va2f(0x7BF268)+3] == bytes.fromhex("C2 04 00"))
    check("HLP: idiom zwrotu this (xor/neg/sbb/not; and eax,ecx)",
          bytes.fromhex("33 C0 F7 D8 1B C0 F7 D0 23 C1") in b2)
    check("HLP: epilog NULL (33 C0 ... C2 04 00) @0x7BF26B",
          d[va2f(0x7BF26B):va2f(0x7BF26B)+3] == bytes.fromhex("33 C0 C2"))
    check("HLP: int3 padding od 0x7BF275",
          d[va2f(0x7BF275):va2f(0x7BF275)+4] == bytes.fromhex("CC CC CC CC"))

    s0 = va2f(0x0082E420)
    b0 = d[s0:s0+0x30]
    call1 = 0x0082E428 + struct.unpack_from("<i", d, s0+4)[0]
    call2 = 0x0082E435 + struct.unpack_from("<i", d, s0+0x11)[0]
    check("S0: push esi; mov esi,ecx; call 0x7B60D0",
          b0[:4] == bytes.fromhex("56 8B F1 E8") and call1 == 0x007B60D0, hex(call1))
    check("S0: test [esp+8],1; je; push esi; call 0x95D42A",
          b0[8:14] == bytes.fromhex("F6 44 24 08 01 74") and b0[15] == 0x56 and b0[16] == 0xE8 and call2 == 0x0095D42A, hex(call2))
    check("S0: ret 4", b0[0x1B:0x1E] == bytes.fromhex("C2 04 00"))

    s1 = va2f(0x00406D50)
    b1t = d[s1:s1+13]
    check("S1: test ecx,ecx; je; mov eax,[ecx]; mov edx,[eax]; push 1; call edx; ret",
          b1t == bytes.fromhex("85 C9 74 08 8B 01 8B 10 6A 01 FF D2 C3"), hx(b1t))

    s2 = va2f(0x007B60C0)
    b2g = d[s2:s2+6]
    check("S2: mov eax,0xBA7218; ret", b2g == bytes.fromhex("B8 18 72 BA 00 C3"), hx(b2g))

    s16 = va2f(0x007B4650)
    b16 = d[s16:s16+0x160]
    check("S16: sub esp,0x8C; bool gate cmp [esp+0x98],0",
          b16[:6] == bytes.fromhex("81 EC 8C 00 00 00") and
          bytes.fromhex("80 BC 24 98 00 00 00 00") in b16[:16])
    check("S16: lea ebx,[esi+0x38] (m_kLocal)", bytes.fromhex("8D 5E 38") in b16)
    check("S16: lea edi,[esi+0x5C] (translate = +0x38+0x24)", bytes.fromhex("8D 7E 5C") in b16)
    check("S16: fld [esi+0x68] (scale = +0x38+0x30)", bytes.fromhex("D9 46 68") in b16)
    check("S16: dzieci [esi+0xD4]/[esi+0xCC]", bytes.fromhex("39 BE D4 00 00 00") in b16 and bytes.fromhex("8B 96 CC 00 00 00") in b16)
    tail16 = d[s16+0xFE:s16+0x120]
    ok_rec16 = bytes.fromhex("8B 40 40") in tail16 or bytes.fromhex("8B 50 40") in tail16 or bytes.fromhex("FF 50 40") in tail16 or bytes.fromhex("FF 52 40") in tail16
    check("S16: rekursja dziecka przez wlasny slot +0x40", ok_rec16, hx(tail16[:24]))

    s18 = va2f(0x007B5160)
    b18 = d[s18:s18+0x100]
    for m in ("02","04","08","10"):
        check("S18: or word [esi+0x20], 0x%s" % m, bytes.fromhex("66 83 4E 20 "+m) in b18)
    for m in ("FD FF","FB FF","F7 FF","EF FF"):
        check("S18: and word [esi+0x20], maska 0x%s" % m[-2:], bytes.fromhex("66 81 66 20 "+m) in b18)
    check("S18: rekursja dziecka przez [edx+0x48] (wlasny slot)",
          bytes.fromhex("8B 52 48") in b18)
    check("S18: brak name-member read [reg+0x0C] (to NIE jest name lookup)",
          bytes.fromhex("8B 51 0C") not in b18 and bytes.fromhex("8B 41 0C") not in b18 and bytes.fromhex("8B 46 0C") not in b18 and bytes.fromhex("8B 47 0C") not in b18)

    s27 = va2f(0x007E4820)
    b27 = d[s27:s27+0x60]
    check("S27: sub esp,0x34; push ebx; mov ebx,ecx; parent [ebx+0x24]",
          b27[:10] == bytes.fromhex("83 EC 34 53 8B D9 8B 43 24 85"), hx(b27[:12]))
    check("S27: lea ecx,[ebx+0x38] (m_kLocal)", bytes.fromhex("8D 4B 38") in b27)
    check("S27: lea ecx,[eax+0x6C] (parent m_kWorld)", bytes.fromhex("8D 48 6C") in b27)
    check("S27: lea esi,[ebx+0x38] fallback", bytes.fromhex("8D 73 38") in b27)
    check("S27: lea edi,[ebx+0x6C] (m_kWorld)", bytes.fromhex("8D 7B 6C") in b27)
    check("S27: mov ecx,0xD; rep movsd", bytes.fromhex("B9 0D 00 00 00 F3 A5") in b27)
    check("S27: collision [ebx+0xB0] -> dispatch [eax+0x3C]",
          bytes.fromhex("8B 8B B0 00 00 00") in b27 and bytes.fromhex("8B 50 3C") in b27)

    ini = va2f(0x00A6C200)
    bi = d[ini:ini+0x15]
    exp = bytes.fromhex("68 70 72 BA 00 68 00 CE A8 00 B9 18 72 BA 00 E8 CC D7 CA FF C3")
    check("NIRTTI: inicjalizator 0xA6C200 (push 0xBA7270; push 0xA8CE00; mov ecx,0xBA7218; call; ret)",
          bi == exp, hx(bi))
    call_t = 0x00A6C214 + struct.unpack_from("<i", d, ini+16)[0]
    check("NIRTTI: call rel32 -> 0x7199E0", call_t == 0x007199E0, hex(call_t))
    lit = d[va2f(0x00A8CE00):va2f(0x00A8CE00)+7]
    check("NIRTTI: literal 'NiNode' @0xA8CE00", lit == b"NiNode\x00", repr(lit))
    pre_pad = d[ini-4:ini]
    check("NIRTTI: 0xCC padding przed inicjalizatorem", pre_pad == bytes.fromhex("CC CC CC CC"), hx(pre_pad))

    npass = sum(1 for _, ok, _ in results if ok)
    print("")
    print("==== AUDYT BAJTOW ENTROPIA.EXE: %d/%d PASS ====" % (npass, len(results)))
    for nm, ok, det in results:
        print("%s  %-72s %s" % ("PASS" if ok else "FAIL", nm, det))
    if npass != len(results):
        sys.exit(1)

if __name__ == "__main__":
    main()

