# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-935-link30-identity-20260914-1101) - plik audytora, NIE jest czescia pracy wykonawcy
# verify_link30.py - own independent verification of PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914
import hashlib, struct, sys, os, csv, json, re
sys.path.insert(0, r"D:\TESTAI\audits\work-audit\audyt-935-pub-persist-20260914-0648\pylibs")
import capstone
print("capstone", capstone.__version__)
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914"
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
RES = []
def rep(name, ok, detail=""):
    RES.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(detail) if detail else ""))

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()

# ============ A. FILE HASHES ============
man_path = os.path.join(PKG, "06_REPORT", "MANIFEST_SHA256.csv")
rows_man = list(csv.reader(open(man_path, encoding="utf-8")))
hdr, data = rows_man[0], rows_man[1:]
rep("A1 manifest rows == 32 (33 files - self)", len(data) == 32, len(data))
bad = []
for rel, h in data:
    p = os.path.join(PKG, rel.replace("/", os.sep))
    if not os.path.exists(p):
        bad.append((rel, "MISSING")); continue
    a = sha256_file(p)
    if a != h.lower():
        bad.append((rel, h, a))
rep("A2 manifest re-hash 32/32", len(bad) == 0, bad if bad else "all match")
pmr = sha256_file(os.path.join(PKG, "06_REPORT", "PE_MASTER_REVIEW.md"))
rep("A3 PE_MASTER_REVIEW SHA == 411e4717...", pmr == "411e471701161013ce0f7b3067cd8d099248745107c17126e01c1fda5892b7f0", pmr)
aml = sha256_file(os.path.join(PKG, "06_REPORT", "AMEND_LOG_R1.md"))
rep("A4 AMEND_LOG SHA == 52b19b44... (manifest row)", aml == "52b19b44c50eb924a2e7b6967ec9b26d4224959ade02019581acbc41d3d2ad2d", aml)
scr = list(csv.reader(open(os.path.join(PKG, "00_CONTROL", "SCRIPT_SHA256.csv"), encoding="utf-8")))
bad2 = []
for r in scr[1:]:
    p = os.path.join(PKG, "00_CONTROL", r[0])
    if sha256_file(p) != r[2]:
        bad2.append(r[0])
rep("A5 SCRIPT_SHA256 4/4 re-hash", len(scr)-1 == 4 and not bad2, bad2)
qc_inv = {
 "qc1_counters.py": "BB7FF3AD8B19A635A79C843797A3E20781AE9F3A9D5D37397BFFF5EC9338AA65",
 "qc2_bytes.py": "DCE9091AB93877B78E39309E7B2AFD244C630BA7D31F32E5FB591C7EC6E6C98B",
 "qc3_sweep.py": "9AF5B188D3A21FB7A6BDAB4E2D2FD21ACFA69548FD14A8BEEC8F96F6B8601E8D",
 "qc4_sample_scope.py": "22E9AC4CF76625026FA7B2D5E8EA200BCC041B8A20FC15B07634A29D49B3D942",
 "qc4b_scope_bytes.py": "430B80CE6AB7B52D2B4F456B15B86552FD0C7D11B3FAEDE5BBB4C16270DD8959",
 "qc5_final.py": "2DDAD0CB40384D3D040F568E0039BE04B5752FF19AD141B56957DF5FFA56E1B0",
 "out_qc1_counters.txt": "DFE4B37D71CDBAADDC28DBD0C422207F359C1FA1881ECFE2B0BEADAE4001E0B4",
 "out_qc2_bytes.txt": "DB3BC4CF5C79181A4EAC01DA5FBFF5FF57598F96A9A33300A14796A3FA5D0BBE",
 "out_qc3_sweep.txt": "05509B777DBB9CCCE3C945B816951C487C0FC7E8D3A1E343A8E18035F3DAAA46",
 "out_qc4_sample_scope.txt": "6786160F8597510EAE019B930372865980ECAC40A857AA54B37A0AC612A2F466",
 "out_qc4b_scope_bytes.txt": "741CFF6084A5D7A8BC52AFA9B2AEC3663C96F34D9CC8CD4E0542E909F020B5A3",
 "out_qc5_final.txt": "71B99BC7403497FA9F7F63544FD4F8F99EFC8ED5905320481EAFB2C6A0128AC0"}
bad3 = [(k, sha256_file(os.path.join(PKG, "00_CONTROL", "qc_probe", k))) for k in qc_inv
        if sha256_file(os.path.join(PKG, "00_CONTROL", "qc_probe", k)) != qc_inv[k].lower()]
rep("A6 qc_probe 12/12 == QC s9 inventory", not bad3, bad3)
refs = [("docs/audits/PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914/06_REPORT/REPORT.md", "106056266d7c2e6f9c505f06ceee8329f4240143b21d1fcd5a6d0c143ee8e5b3"),
        ("docs/audits/PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914/01_RAW/SLOT_DISASSEMBLY.txt", "9ae750f5596304b599eead6eb73e8c89c9e8197210433447c3a0beff13ce4e72"),
        ("docs/audits/PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913/06_REPORT/REPORT.md", "9373716d3545f5327cb1d363de701a3609050a94707bea6f755864c74dbc60b8")]
bad4 = [(r, sha256_file(os.path.join(REPO, r.replace("/", os.sep)))) for r, e in refs if sha256_file(os.path.join(REPO, r.replace("/", os.sep))) != e]
rep("A7 prior-run reference hashes 3/3", not bad4, bad4)
gates_h = sha256_file(os.path.join(PKG, "06_REPORT", "STAGE_ACCEPTANCE_GATES.csv"))
rep("A8 gates CSV SHA == 375798e8...", gates_h == "375798e82c80e7ed4ec388db486a22856c9409a5a397ff10582e1d0188121968", gates_h)
csv_h = sha256_file(os.path.join(PKG, "02_ANALYSIS", "SF30_WRITER_CENSUS.csv"))
rep("A9 census CSV SHA == 71552e2a... (AMEND determinism)", csv_h == "71552e2a4bfc120da0be1a7e108a41a03c873addd238637dd7c18f3c968824d0", csv_h)

# ============ B. PE PARSE (own) ============
d = open(EXE, "rb").read()
exe_sha = hashlib.sha256(d).hexdigest().upper()
rep("B1 EXE SHA == E7785430...F31", exe_sha == "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31", exe_sha[:16])
rep("B2 EXE size == 8015872", len(d) == 8015872, len(d))
e = struct.unpack_from("<I", d, 0x3C)[0]
assert struct.unpack_from("<I", d, e)[0] == 0x4550
coff = e + 4
machine, nsec = struct.unpack_from("<HH", d, coff)
optsz = struct.unpack_from("<H", d, coff + 16)[0]
opt = coff + 20
magic = struct.unpack_from("<H", d, opt)[0]
imgbase = struct.unpack_from("<I", d, opt + 28)[0]
dllchar = struct.unpack_from("<H", d, opt + 70)[0]
import_rva = struct.unpack_from("<I", d, opt + 96 + 8)[0]
rep("B3 machine 0x14C / magic 0x10B / base 0x400000 / no ASLR", machine == 0x14C and magic == 0x10B and imgbase == 0x400000 and (dllchar & 0x40) == 0)
secs = []
so = opt + optsz
for i in range(nsec):
    o = so + i * 40
    name = d[o:o+8].rstrip(b"\x00").decode()
    vs, va, rs, rp = struct.unpack_from("<IIII", d, o + 8)
    secs.append((name, vs, va, rs, rp))
text = [s for s in secs if s[0] == ".text"][0]
rep("B4 .text vaddr=0x1000 rsize=0x674000", text[2] == 0x1000 and text[3] == 0x674000, hex(text[3]))
def off(va):
    rva = va - imgbase
    for name, vs, sva, rs, rp in secs:
        if sva <= rva < sva + rs:
            return rp + (rva - sva)
    return None
def rd(va, n):
    o = off(va)
    return d[o:o+n] if o is not None else None
def rd32(va):
    b = rd(va, 4)
    return struct.unpack("<I", b)[0] if b and len(b) == 4 else None
def in_text(va):
    return 0x401000 <= va < 0x401000 + text[3]

# ============ C. BYTE PINS ============
pins = {
 0x509330: "6aff", 0x509357: "8be9", 0x509366: "c7450058d4a700", 0x509376: "6818010000",
 0x5093A0: "e81f404500", 0x5093A5: "83c404", 0x5093AC: "3bc3", 0x5093B5: "53",
 0x5093B6: "8bc8", 0x5093B8: "e843cc2a00", 0x5093BD: "eb02", 0x5093BF: "33c0",
 0x5093C1: "3bc3", 0x5093C3: "894530", 0x5093C6: "7404", 0x5093C8: "83400401",
 0x50A263: "8bf1", 0x50A269: "c70658d4a700", 0x50A272: "33db", 0x50A2BD: "8b4e30",
 0x50A2C0: "3bcb", 0x50A2C4: "834104ff", 0x50A2C8: "7507", 0x50A2CA: "8b01",
 0x50A2CC: "8b5004", 0x50A2CF: "ffd2", 0x50A2D1: "895e30", 0x50A2D4: "8b4e30",
 0x50A463: "e8d8fdffff",
 0x7B6023: "8bf1", 0x7B6029: "e8a2a20000", 0x7B6037: "8d8ec8000000",
 0x7B6041: "c706f4cca800", 0x7B6047: "e83424fdff", 0x7B605E: "c786e0000000e0cca800",
 0x7B609F: "8bc6",
 0x50A057: "8bf1", 0x50A05B: "8b4e30", 0x50A05E: "8b11", 0x50A060: "50",
 0x50A061: "8b4244", 0x50A064: "ffd0", 0x50A066: "85c0", 0x50A068: "741d",
 0x50A06A: "8b742408", 0x50A06E: "0590000000", 0x50A073: "50", 0x50A074: "56",
 0x50A075: "e8f6def2ff", 0x50A07A: "8bc8", 0x50A07C: "e81f153200",
 0x5247E7: "6898000000", 0x5247EC: "e8d38b4300", 0x52480D: "8bc8",
 0x52480F: "e81c4bfeff", 0x524814: "8bf0",
 0x47CFC6: "6898000000", 0x47CFDE: "e8e1034e00", 0x47CFE3: "8bf8", 0x47D03A: "8bcf",
 0x47D043: "e8e8c20800", 0x47D048: "8bd8", 0x47D04A: "89442460",
 0x52901A: "8b8ec0000000", 0x529020: "e89b04feff",
 0x67B8E4: "8b4e04", 0x67B8E8: "e8", 0x67C8A4: "8b4e04", 0x6A3A29: "8b4e18",
 0x44D62E: "89460c", 0x44D680: "894610", 0x44D6D1: "894614", 0x528FEA: "8986c0000000",
 0x67B8AD: "894604", 0x67C86D: "894604", 0x6A39F6: "894618",
 0x95D3C4: "ff255453a700", 0x95D42A: "ff255c53a700",
}
badp = []
for va, hx in pins.items():
    b = rd(va, len(hx)//2)
    if b is None or b.hex() != hx:
        badp.append((hex(va), hx, None if b is None else b.hex()))
rep("C1 all %d byte pins exact" % len(pins), not badp, badp)
# call targets
def call_target(va):
    b = rd(va, 5)
    return va + 5 + struct.unpack("<i", b[1:5])[0]
tg = {0x5093A0: 0x95D3C4, 0x5093B8: 0x7B6000, 0x50A463: 0x50A240, 0x7B6029: 0x7C02D0,
      0x7B6047: 0x788480, 0x50A075: 0x437F70, 0x50A07C: 0x82B5A0, 0x52480F: 0x509330,
      0x47D043: 0x509330, 0x529020: 0x5094C0}
badt = [(hex(v), hex(call_target(v))) for v, exp in tg.items() if call_target(v) != exp]
rep("C2 call rel32 targets 10/10", not badt, badt)
# imports (own walk)
imp = {}
rva = import_rva
while True:
    o = off(imgbase + rva)
    if o is None: break
    ilt, ts, fc, nrva, iatrva = struct.unpack_from("<IIIII", d, o)
    if ilt == 0 and nrva == 0 and iatrva == 0: break
    no = off(imgbase + nrva)
    dll = d[no:d.index(b"\x00", no)].decode()
    k = 0
    while True:
        iat_va = imgbase + iatrva + 4*k
        o2 = off(iat_va)
        val = struct.unpack_from("<I", d, o2)[0]
        if val == 0: break
        if val & 0x80000000:
            imp[iat_va] = "%s.#%d" % (dll, val & 0xFFFF)
        else:
            xo = off(imgbase + val + 2)
            nm = d[xo:d.index(b"\x00", xo)].decode()
            imp[iat_va] = "%s.%s" % (dll, nm)
        k += 1
    rva += 20
rep("C3 thunk 0x95D3C4 -> MSVCR80 ??2@YAPAXI@Z", imp.get(0xA75354) == "MSVCR80.dll.??2@YAPAXI@Z", imp.get(0xA75354))
rep("C4 thunk 0x95D42A -> MSVCR80 ??3@YAXPAX@Z", imp.get(0xA7535C) == "MSVCR80.dll.??3@YAXPAX@Z", imp.get(0xA7535C))
# ecx clobber window + ebp/esi single defs
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32); md.detail = True
def dis1(va):
    b = rd(va, 16)
    try:
        i = next(md.disasm(b, va))
    except StopIteration:
        return None
    return i
def diswin(va, n):
    out = []
    b = rd(va, n)
    for i in md.disasm(b, va):
        out.append(i)
    return out
win = diswin(0x50A05E, 6)
clo = [i.mnemonic + " " + i.op_str for i in win if i.op_str.startswith("ecx,") and i.mnemonic != "call"]
rep("C5 ECX unmodified 0x50A05E..0x50A064", len(win) == 3 and not clo, [i.mnemonic for i in win])
ebp_defs = []; va = 0x509330
while va < 0x5093C3:
    i = dis1(va)
    if i.op_str.startswith("ebp,"): ebp_defs.append((hex(va), i.mnemonic + " " + i.op_str))
    va += i.size
rep("C6 ebp defs in ctor == exactly 1 (mov ebp,ecx)", ebp_defs == [("0x509357", "mov ebp, ecx")], ebp_defs)
esi_defs = []; va = 0x50A240
while va < 0x50A2D1:
    i = dis1(va)
    if i.op_str.startswith("esi,"): esi_defs.append((hex(va), i.mnemonic + " " + i.op_str))
    va += i.size
rep("C7 esi defs in dtor body == exactly 1 (mov esi,ecx)", esi_defs == [("0x50a263", "mov esi, ecx")], esi_defs)
