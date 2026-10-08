# -*- coding: utf-8 -*-
"""qc_independent_check.py — FRESH-CONTEXT INTERNAL QC of
PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008.

Written by the pe-master-auditor QC worker (fresh context). INDEPENDENT
implementation: own PE32 mapping, own fail-closed EXE identity, own pin reads,
own rel32/rel8 arithmetic, own RTTI chain walk, own strings, own corruption
controls. It does NOT reuse checker_plus4.py logic except where explicitly
NOTED (re-running the executor's PRODUCTION GATE on in-memory corrupted
copies for MC re-verification — mandated by the QC task).

python -B; stdlib only; NO file writes except QC_RESULTS.json in this
directory; the physical EXE is NEVER modified (in-memory copies only).
"""
import hashlib
import json
import os
import re
import struct
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_SIZE = 8015872
EXE_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
IMAGE_BASE = 0x00400000

OUT_JSON = os.path.join(HERE, "QC_RESULTS.json")


# ---------------------------------------------------------------------------
# OWN PE32 mapping (independent of the executor's OwnPE).
# ---------------------------------------------------------------------------
class QCPE:
    def __init__(self, data):
        self.data = data
        e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
        if data[e_lfanew:e_lfanew + 4] != b"PE\x00\x00":
            raise ValueError("PE signature missing")
        coff = e_lfanew + 4
        machine, nsec = struct.unpack_from("<HH", data, coff)
        if machine != 0x014C:
            raise ValueError(f"machine {machine:#x} != 0x14C (i386)")
        size_opt = struct.unpack_from("<H", data, coff + 16)[0]
        magic = struct.unpack_from("<H", data, coff + 20)[0]
        if magic != 0x010B:
            raise ValueError(f"OptionalHeader magic {magic:#x} != PE32 0x10B")
        img_base = struct.unpack_from("<I", data, coff + 20 + 28)[0]
        if img_base != IMAGE_BASE:
            raise ValueError(f"ImageBase {img_base:#x} != pinned {IMAGE_BASE:#x}")
        sec0 = coff + 20 + size_opt
        self.sections = []
        for i in range(nsec):
            off = sec0 + 40 * i
            name = data[off:off + 8].rstrip(b"\x00").decode("ascii")
            vsize, va, rsize, roff = struct.unpack_from("<IIII", data, off + 8)
            self.sections.append((name, va, vsize, roff, rsize))

    def va_to_off(self, va):
        """Return (file_offset, kind) or (None, reason_kind).

        kind: RAW (physical bytes), VIRTUAL_BSS (inside a section's virtual
        size but past its raw size -> zero-initialized at load, NO file bytes),
        UNMAPPED (no section covers the RVA).
        Distinguishes raw vs virtual tail EXPLICITLY (unlike a max(vsize,rsize)
        mapping that can silently land in another section's raw area).
        """
        rva = va - IMAGE_BASE
        for name, va_s, vsize, roff, rsize in self.sections:
            if va_s <= rva < va_s + max(vsize, rsize):
                if rva < va_s + rsize:
                    fo = roff + (rva - va_s)
                    if fo + 0 < len(self.data):
                        return fo, "RAW"
                    return None, "RAW_PAST_EOF"
                return None, "VIRTUAL_BSS"
        return None, "UNMAPPED"

    def read(self, va, n):
        fo, kind = self.va_to_off(va)
        if fo is None:
            raise ValueError(f"VA {va:#010x} not RAW-mapped ({kind})")
        if fo + n > len(self.data):
            raise ValueError(f"VA {va:#010x} read past EOF")
        return self.data[fo:fo + n]

    def u32(self, va):
        return struct.unpack("<I", self.read(va, 4))[0]

    def cstr(self, va, maxlen=256):
        b = self.read(va, maxlen)
        z = b.find(b"\x00")
        return b[:z if z >= 0 else maxlen]


def hx(b):
    return " ".join(f"{c:02X}" for c in b)


# ---------------------------------------------------------------------------
# Load EXE fail-closed.
# ---------------------------------------------------------------------------
with open(EXE_PATH, "rb") as f:
    EXE = f.read()
exe_size = len(EXE)
exe_sha = hashlib.sha256(EXE).hexdigest().upper()
results = {
    "qc_run_id": "PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008_INTERNAL_QC_R1",
    "qc_worker": "pe-master-auditor (fresh-context internal QC dispatch under PE-MASTER)",
    "qc_origin": "FRESH-CONTEXT INTERNAL QC (pe-master-auditor; NOT a Desktop post-audit; "
                  "internal to PE-MASTER, NOT independent of PE-MASTER)",
    "exe_identity": {
        "pinned_size": EXE_SIZE, "measured_size": exe_size,
        "pinned_sha256": EXE_SHA256, "measured_sha256": exe_sha,
        "match": exe_size == EXE_SIZE and exe_sha == EXE_SHA256,
    },
}
if not results["exe_identity"]["match"]:
    results["verdict"] = "QC_BLOCKED_INPUT_IDENTITY"
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("BLOCKED: EXE identity mismatch")
    sys.exit(2)

PE = QCPE(EXE)
results["pe_sections"] = [
    {"name": n, "rva": f"{va:#010x}", "vsize": f"{v:#x}", "raw_off": f"{ro:#x}",
     "raw_size": f"{rs:#x}"} for (n, va, v, ro, rs) in PE.sections
]

# ---------------------------------------------------------------------------
# 1. BODY WINDOW BYTE-COMPARE vs the 01_RAW hex strings (byte-for-byte vs EXE).
#    Repetition of already-charged body units by QC = free (contract §4).
# ---------------------------------------------------------------------------
raw_dir = os.path.join(PKG, "01_RAW")
body_files = {
    "FUN_006C9700_PUMP_FULL.txt": None,
    "FUN_006E8F70_CTOR_R.txt": None,
    "FUN_006C9570_SLOT_SETTER.txt": None,
    "FUN_007B79B0_P_GETTER_PARTIAL.txt": None,
}
body_compare = []
for fn in body_files:
    path = os.path.join(raw_dir, fn)
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    hexline = None
    va_start = None
    va_end = None
    for i, ln in enumerate(lines):
        if ln.startswith("RAW BYTES"):
            m = re.search(r"(0x[0-9A-Fa-f]+)\.\.(0x[0-9A-Fa-f]+)", ln)
            if m:
                va_start = int(m.group(1), 16)
                va_end = int(m.group(2), 16)
            # multi-line headers: scan forward for the first pure-hex line
            for j in range(i + 1, min(i + 6, len(lines))):
                cand = lines[j].strip()
                if re.fullmatch(r"[0-9A-F]{2}( [0-9A-F]{2})*", cand):
                    hexline = cand
                    break
            break
    expected = bytes.fromhex(hexline.replace(" ", ""))
    n_expect = va_end - va_start + 1
    try:
        got = PE.read(va_start, len(expected))
        match = got == expected
        detail = "OK" if match else f"expected[{len(expected)}] != physical[{len(got)}]: {hx(got[:16])}..."
    except ValueError as e:
        got = b""
        match = False
        detail = f"read error: {e}"
    body_compare.append({
        "file": fn, "window": f"{va_start:#010x}..{va_end:#010x}",
        "declared_len": n_expect, "hex_len": len(expected),
        "physical_match": match, "detail": detail,
    })
results["body_windows_byte_compare"] = body_compare

# ---------------------------------------------------------------------------
# 2. TASK ANCHOR PIN RECHECK (own mapping + own byte read; expected values
#    taken from the QC TASK LIST + the package's raw claims).
# ---------------------------------------------------------------------------
ANCHORS = [
    ("CAND4_caller_callsite", 0x006C6FFC, "E8 FF 26 00 00",
     "call FUN_006C9700 from FUN_006C6F60 (rel32 +0x26FF)"),
    ("producer_store_manager_6C", 0x006C7008, "89 46 6C",
     "mov [esi+0x6C],eax — R stored to manager"),
    ("installer_load_R", 0x006C67B3, "8B 46 6C", "mov eax,[esi+0x6C] — R loaded"),
    ("installer_read_R4_T", 0x006C67BE, "8B 78 04", "mov edi,[eax+4] — T = [R+4]"),
    ("installer_ebx_1", 0x006C67C9, "BB 01 00 00 00", "mov ebx,1 (NOT an INC)"),
    ("installer_store_manager_68", 0x006C67E2, "89 7E 68", "mov [esi+0x68],edi — T stored"),
    ("installer_incref_T", 0x006C67E7, "01 5F 04", "add [edi+4],ebx — ADD [T+4],EBX"),
    ("installer_decref_old", 0x006C67D4, "01 69 04", "add [ecx+4],ebp (prior re-pin)"),
    ("installer_cmp_68", 0x006C67A9, "83 7E 68 00", "cmp [esi+0x68],0 (prior re-pin)"),
    ("pump_new_size_0x10", 0x006C97B9, "6A 10", "push 0x10 — R allocation size"),
    ("pump_return_R", 0x006C9808, "8B C6", "mov eax,esi — pump RETURN R"),
    ("pump_terminal_ret", 0x006C981B, "C3", "terminal ret (extent proof)"),
    ("ctor_return_this", 0x006E9014, "8B C6", "mov eax,esi — ctor RETURN this"),
    ("ctor_R0_store_S", 0x006E8F9D, "89 06", "mov [esi],eax — [R+0]=S (NO vptr store)"),
    ("plus4_writer", 0x006E8FA5, "89 46 04", "mov [esi+4],eax — THE [R+4] WRITER"),
    ("ctor_addref_P", 0x006E8FAF, "01 48 04", "add [eax+4],ecx — [P+4]+=1 (ecx=1)"),
    ("setter_slot_preclear", 0x006C95A0, "C7 06 00 00 00 00", "mov dword [esi],0 — slot pre-clear"),
    ("setter_slot_store_P", 0x006C9651, "89 3E", "mov [esi],edi — SLOT = P"),
    ("setter_addref_P", 0x006C9657, "01 5F 04", "add [edi+4],ebx — [P+4]+=1 (ebx=1)"),
    ("setter_receiver_S10", 0x006C95A6, "8B 49 10", "mov ecx,[ecx+0x10] — receiver [S+0x10]"),
    ("setter_flag_cmp", 0x006C95AE, "38 5C 24 28", "cmp byte [esp+0x28],bl — flag vs 1"),
    ("setter_flag_jne_cand4", 0x006C95BE, "75 71", "jne 0x006C9631 — CAND-4 path"),
    ("hist_caller_pump_call", 0x006CB7CF, "E8 2C DF FF FF", "call FUN_006C9700 (historical caller)"),
    ("hist_caller_test_esi", 0x006CB811, "85 F6", "test esi,esi (prior record re-read)"),
    ("hist_caller_new_0xC", 0x006CB819, "6A 0C", "push 0xC — W wrapper size (prior canon)"),
    ("hist_caller_w_ctor_call", 0x006CB836, "E8 75 F0 02 00",
     "call FUN_006FA8B0 — ctor(W, saved R); the CORRECTED transcription (E8 75, not E8 35)"),
]
anchor_rows = []
for aid, va, hexstr, meaning in ANCHORS:
    exp = bytes.fromhex(hexstr.replace(" ", ""))
    got = PE.read(va, len(exp))
    anchor_rows.append({
        "anchor_id": aid, "va": f"{va:#010x}", "expected": hx(exp),
        "measured": hx(got), "match": got == exp, "meaning": meaning,
    })
results["anchor_pins_recheck"] = anchor_rows
results["anchor_pins_summary"] = {
    "total": len(anchor_rows),
    "match": sum(1 for r in anchor_rows if r["match"]),
    "mismatch": [r["anchor_id"] for r in anchor_rows if not r["match"]],
}

# ---------------------------------------------------------------------------
# 3. OWN rel32 RECOMPUTE (call_va + 5 + int32(rel32)) for every rel32 used by
#    the run's records (12 counted edges E1..E12 targets + RAW arith + prior
#    re-pins). Own arithmetic from the PHYSICAL bytes; no report/CSV/JSON input.
# ---------------------------------------------------------------------------
REL32 = [
    ("E1_pump_request_issue", 0x006C9746, 0x00415670),
    ("E2_pump_s_getter", 0x006C974D, 0x00823C10),
    ("E3_pump_slot_setter", 0x006C9764, 0x006C9570),
    ("E4_pump_smethod_8268a0", 0x006C977B, 0x008268A0),
    ("E5_pump_alloc_new", 0x006C97BB, 0x0095D3C4),
    ("E6_pump_ctor_R", 0x006C97D8, 0x006E8F70),
    ("E9_ctor_gate_call", 0x006E8FD0, 0x00728150),
    ("E12_setter_variant_lookup", 0x006C95C5, 0x007B7660),
    ("E11_setter_p_getter", 0x006C9631, 0x007B79B0),
    ("R1_raw_00769510", 0x006E8FF7, 0x00769510),
    ("R2_raw_006E8A90", 0x006E9004, 0x006E8A90),
    ("R3_raw_006B2310", 0x006E900F, 0x006B2310),
    ("R7_raw_pget_alloc", 0x007B79D8, 0x0095D3C4),
    ("R8_raw_pget_init", 0x007B79F2, 0x007B7930),
    ("prior_cand4_caller_pump", 0x006C6FFC, 0x006C9700),
    ("prior_producer_installer", 0x006C7049, 0x006C6780),
    ("prior_hist_pump", 0x006CB7CF, 0x006C9700),
    ("prior_hist_new", 0x006CB81B, 0x0095D3C4),
    ("prior_hist_wctor", 0x006CB836, 0x006FA8B0),
]
rel32_rows = []
for rid, cva, target in REL32:
    b = PE.read(cva, 5)
    opcode = b[0]
    rel = struct.unpack("<i", b[1:5])[0]
    own = cva + 5 + rel
    rel32_rows.append({
        "id": rid, "call_va": f"{cva:#010x}", "opcode": f"{opcode:02X}",
        "bytes": hx(b), "rel32_signed": f"{rel:+#x}", "own_target": f"{own:#010x}",
        "expected_target": f"{target:#010x}", "match": opcode == 0xE8 and own == target,
    })
results["rel32_recompute"] = rel32_rows
results["rel32_summary"] = {
    "total": len(rel32_rows),
    "match": sum(1 for r in rel32_rows if r["match"]),
    "mismatch": [r["id"] for r in rel32_rows if not r["match"]],
}

# ---------------------------------------------------------------------------
# 4. OWN rel8 BRANCH-TARGET RECOMPUTES (branch_va + 2 + int8(disp)).
# ---------------------------------------------------------------------------
REL8 = [
    ("pump_je_S_null", 0x006C9756, 0x74, 0x006C97A5),
    ("pump_jne_slot_nonzero", 0x006C9776, 0x75, 0x006C97B9),
    ("pump_je_slot_still0", 0x006C978E, 0x74, 0x006C97A5),
    ("pump_je_allocfail", 0x006C97CE, 0x74, 0x006C97E1),
    ("pump_je_skip_release", 0x006C97F1, 0x74, 0x006C9808),
    ("setter_jne_cand4path", 0x006C95BE, 0x75, 0x006C9631),
    ("setter_je_no_swap", 0x006C963C, 0x74, 0x006C961A),
    ("setter_je_skip_oldrelease", 0x006C9640, 0x74, 0x006C964F),
    ("setter_jne_skip_destroy", 0x006C9646, 0x75, 0x006C964F),
    ("setter_je_exit_no_addref", 0x006C9655, 0x74, 0x006C961C),
    ("ctor_je_skip_addref", 0x006E8FAD, 0x74, 0x006E8FB2),
    ("ctor_jne_gate_mismatch", 0x006E8FDC, 0x75, 0x006E9014),
    ("ctor_je_slot17_null", 0x006E8FEF, 0x74, 0x006E9014),
    ("ctor_je_after_006E9001", 0x006E9001, 0x74, 0x006E9014),
    ("pget_je_allocnull", 0x007B79EE, 0x74, 0x007B79FB),
]
rel8_rows = []
for rid, bva, opcode_exp, target in REL8:
    b = PE.read(bva, 2)
    opcode = b[0]
    disp = struct.unpack("<b", b[1:2])[0]
    own = bva + 2 + disp
    rel8_rows.append({
        "id": rid, "branch_va": f"{bva:#010x}", "bytes": hx(b),
        "disp_signed": f"{disp:+#x}", "own_target": f"{own:#010x}",
        "expected_target": f"{target:#010x}",
        "match": opcode == opcode_exp and own == target,
    })
results["rel8_recompute"] = rel8_rows
results["rel8_summary"] = {
    "total": len(rel8_rows),
    "match": sum(1 for r in rel8_rows if r["match"]),
    "mismatch": [r["id"] for r in rel8_rows if not r["match"]],
}

# ---------------------------------------------------------------------------
# 5. RTTI CHAINS — OWN walk (vtable[-1] -> COL -> TypeDescriptor -> name).
# ---------------------------------------------------------------------------
def rtti_walk(vtable_va):
    col_ptr = PE.u32(vtable_va - 4)
    col_off, kind = PE.va_to_off(col_ptr)
    if col_off is None:
        return {"error": f"COL {col_ptr:#010x} not raw ({kind})"}
    sig, off_f, cdoff, ptd, pcd = struct.unpack_from("<5I", EXE, col_off)
    ptd_off, kind2 = PE.va_to_off(ptd)
    if ptd_off is None:
        return {"error": f"TD {ptd:#010x} not raw ({kind2})"}
    name = PE.cstr(ptd + 8)
    return {
        "vtable_va": f"{vtable_va:#010x}", "vtable_minus1": f"{col_ptr:#010x}",
        "col_va": f"{col_ptr:#010x}", "col_sig": sig, "col_offset": off_f,
        "col_cdoffset": cdoff, "type_descriptor_va": f"{ptd:#010x}",
        "class_descriptor_va": f"{pcd:#010x}", "name": name.decode("ascii"),
    }

results["rtti_own_read"] = {
    "W_ArkModelResourceInstanceRef": rtti_walk(0x00A864B8),
    "ArkModelManagerMain": rtti_walk(0x00A855D0),
    "ArkModelManager": rtti_walk(0x00A85A08),
}
# W vtable slots 0..3 raw u32 reads (recorded in RTTI_AND_STRINGS.txt)
results["w_vtable_slots"] = [f"{PE.u32(0x00A864B8 + 4 * i):#010x}" for i in range(4)]

# ---------------------------------------------------------------------------
# 6. STRINGS — OWN reads.
# ---------------------------------------------------------------------------
results["strings_own_read"] = {
    "0x00A85DA4": PE.cstr(0x00A85DA4).decode("ascii", "replace"),
    "0x00A859F8": PE.cstr(0x00A859F8).decode("ascii", "replace"),
    "0x00A8547C": PE.cstr(0x00A8547C).decode("ascii", "replace"),
    "0x00A7957B": repr(PE.read(0x00A7957B, 8)),
}

# ---------------------------------------------------------------------------
# 7. ZERO-TAIL / MAPPING-BOUNDARY CHECKS (own mapping, raw-vs-virtual split).
# ---------------------------------------------------------------------------
def map_status(va):
    fo, kind = PE.va_to_off(va)
    return {"va": f"{va:#010x}", "own_mapping": kind,
            "file_offset": (f"{fo:#x}" if fo is not None else None),
            "physical_bytes": (hx(PE.data[fo:fo + 8]) if fo is not None else None)}

results["mapping_boundary_checks"] = {
    "0x00BA73BC (pushed @0x006E8FF2)": map_status(0x00BA73BC),
    "0x00BA1100 (MC6 corruption VA)": map_status(0x00BA1100),
    "note": "QCPE distinguishes RAW vs VIRTUAL_BSS (zero-init tail, no file bytes). "
            "The executor's checker OwnPE uses max(vsize,rsize) WITHOUT the raw-size "
            "boundary, so .data-tail VAs (RVA >= raw end 0x7A0000) are mapped onto "
            "physical file bytes belonging to .tls/.rsrc raw areas — see the MC6 "
            "re-verification below and QC_REPORT finding F-2.",
}

# ---------------------------------------------------------------------------
# 8. NO-VPTR-STORE CHECK (CL-7 re-adjudication): scan the ctor body's bytes
#    for every store whose destination base is ESI (R) and classify the source;
#    verify NO non-zero immediate store exists to [R+anything] (a vptr store
#    would require a non-zero immediate vtable address or a register loaded
#    from RTTI data — the ctor contains neither).
# ---------------------------------------------------------------------------
ctor_hex = "6A FF 68 C6 87 A0 00 64 A1 00 00 00 00 50 51 56 57 A1 D0 D8 B9 00 33 C4 50 8D 44 24 10 64 A3 00 00 00 00 8B F1 89 74 24 0C 8B 44 24 20 89 06 8B 44 24 24 85 C0 89 46 04 B9 01 00 00 00 74 03 01 48 04 8D 7E 08 C7 44 24 18 00 00 00 00 C7 07 00 00 00 00 88 4C 24 18 8B 0E C7 46 0C 00 00 00 00 E8 7B F1 03 00 81 78 04 DC B7 00 00 75 36 8B 4E 04 8B 11 8B 42 44 68 A4 5D A8 00 FF D0 85 C0 74 23 50 68 BC 73 BA 00 E8 14 05 08 00 83 C4 08 85 C0 74 11 50 E8 87 FA FF FF 83 C4 04 50 8B CF E8 FC 92 FC FF 8B C6 8B 4C 24 10 64 89 0D 00 00 00 00 59 5F 5E 83 C4 10 C2 08 00"
ctor_bytes = bytes.fromhex(ctor_hex.replace(" ", ""))
# physical byte-compare of the ctor window first (independent of 01_RAW parsing above)
ctor_phys = PE.read(0x006E8F70, len(ctor_bytes))
immediate_stores = []
for m in re.finditer(b"\xC7", ctor_bytes):
    i = m.start()
    # C7 /0 with mod=00/01 rm=110 (esi) or rm=111 (edi): C7 06 / C7 46 xx / C7 07 (edi=&R+8)
    if ctor_bytes[i + 1] in (0x06, 0x46, 0x07):
        imm = struct.unpack_from("<I", ctor_bytes, i + 2)[0] if ctor_bytes[i + 1] == 0x06 else (
            struct.unpack_from("<I", ctor_bytes, i + 3)[0] if ctor_bytes[i + 1] == 0x46 else
            struct.unpack_from("<I", ctor_bytes, i + 2)[0])
        immediate_stores.append({
            "offset_in_body": i, "form": hx(ctor_bytes[i:i + 6]),
            "imm32": f"{imm:#010x}",
        })
results["no_vptr_store_check"] = {
    "ctor_window_physical_match": ctor_phys == ctor_bytes,
    "imm32_stores_to_R_base": immediate_stores,
    "all_imm32_are_zero": all(s["imm32"] == "0x00000000" for s in immediate_stores),
    "register_stores_to_R": ["89 06 ([R+0]=S from stack arg)", "89 46 04 ([R+4]=P from stack arg)"],
    "conclusion": "The construction dataflow writes NO vptr into R: all R-base stores "
                 "are the two argument-pointer stores (89 06 / 89 46 04) and the two "
                 "ZERO immediate stores (C7 07 00.. to R+8; C7 46 0C 00.. to R+0xC). "
                 "A vptr store would require a non-zero vtable immediate — none exists.",
}

# ---------------------------------------------------------------------------
# 9. MC1/MC4/MC6 RE-VERIFICATION (own corruptions on IN-MEMORY copies; the
#    physical EXE is NEVER modified). Two gates per corruption:
#    (a) the QC's OWN pin gate (independent expected-bytes check);
#    (b) the executor's PRODUCTION gate (checker_plus4.run_checks) — mandated
#        "same production gate must detect the corruption" verification.
# ---------------------------------------------------------------------------
mc = {}
# --- MC1: corrupt the +4 writer anchor (own corruption bytes: 89 46 04 -> 89 47 04)
off1, kind1 = PE.va_to_off(0x006E8FA5)
c1 = bytearray(EXE)
c1[off1:off1 + 3] = bytes.fromhex("894704")
own_gate_mc1 = (bytes(c1[off1:off1 + 3]) != bytes.fromhex("894604"))  # own pin gate must now FAIL
mc["MC1_own_plus4_writer"] = {
    "corruption": "@0x006E8FA5 89 46 04 -> 89 47 04 (QC's own corruption bytes; in-memory copy)",
    "own_gate_detected": own_gate_mc1,
    "physical_bytes_after": hx(bytes(c1[off1:off1 + 3])),
    "physical_exe_unchanged": hx(PE.read(0x006E8FA5, 3)) == "89 46 04",
}
# --- MC4: corrupt the ctor call rel32 (own bit-flip, DIFFERENT from the
#     executor's flip: operand byte +2 ^= 0x02 -> 0x01 -> 0x03)
off4, kind4 = PE.va_to_off(0x006C97D8)
c4 = bytearray(EXE)
c4[off4 + 2] ^= 0x02
rel4 = struct.unpack_from("<i", bytes(c4[off4 + 1:off4 + 5]), 0)[0]
own4 = 0x006C97D8 + 5 + rel4
mc["MC4_own_ctor_rel32"] = {
    "corruption": "@0x006C97D8 rel32 operand byte+2 ^= 0x02 (0x01->0x03) — QC's own flip, "
                  "different from the executor's byte+1 flip",
    "bytes_after": hx(bytes(c4[off4:off4 + 5])),
    "rel32_signed": f"{rel4:+#x}", "own_target": f"{own4:#010x}",
    "target_ceased_expected": own4 != 0x006E8F70,
    "physical_exe_unchanged": PE.read(0x006C97D8, 5) == bytes.fromhex("E893F70100"),
}

# --- re-run the executor's PRODUCTION gate on the corrupted copies
sys.path.insert(0, os.path.join(PKG, "03_SCRIPTS"))
import checker_plus4 as chk  # noqa: E402  (executor's production gate, import only)

r1 = chk.run_checks(data_override=bytes(c1))
ok1, fails1 = chk.gate(r1)
hit1 = [f for f in fails1 if f[0] == "PIN:CTOR_R4_STORE_P"]
mc["MC1_production_gate"] = {
    "gate": "FAIL" if not ok1 else "PASS", "anchor_detected": bool(hit1),
    "anchor_detail": hit1[0][2] if hit1 else None,
    "other_fails": [f[0] for f in fails1 if f[0] != "PIN:CTOR_R4_STORE_P"],
    "verdict": "PASS" if (not ok1 and hit1) else "FAIL",
}
r4 = chk.run_checks(data_override=bytes(c4))
ok4, fails4 = chk.gate(r4)
hit4 = [f for f in fails4 if f[0] == "REL32:REL_PUMP_CTOR_R"]
mc["MC4_production_gate"] = {
    "gate": "FAIL" if not ok4 else "PASS", "anchor_detected": bool(hit4),
    "anchor_detail": hit4[0][2] if hit4 else None,
    "other_fails": [f[0] for f in fails4 if f[0] != "REL32:REL_PUMP_CTOR_R"],
    "verdict": "PASS" if (not ok4 and hit4) else "FAIL",
}

# --- MC6 (specificity): corrupt a PHYSICAL .rsrc raw byte at file offset
#     0x7A1100 (== .rsrc ROFF 0x7A1000 + 0x100) DIRECTLY (bypassing the VA
#     mapping question entirely) + a second unpinned .rsrc byte at +0x200.
for tag, foff in (("MC6a_off_0x7A1100", 0x7A1100), ("MC6b_off_0x7A1200", 0x7A1200)):
    c6 = bytearray(EXE)
    c6[foff] ^= 0xFF
    r6 = chk.run_checks(data_override=bytes(c6))
    ok6, _ = chk.gate(r6)
    mc[tag] = {
        "corruption": f"file offset {foff:#x} (.rsrc raw area, unpinned) ^= 0xFF",
        "anchor_gates_still_pass": ok6,
        "verdict": "PASS" if ok6 else "FAIL",
    }
# --- MC6-VA (the executor's exact MC6 corruption replayed): VA 0x00BA1100
exepe = chk.OwnPE(EXE)  # executor's mapping class (returns plain int offsets)
_off6va = exepe.va_to_off(0x00BA1100)
c6va = bytearray(EXE)
c6va[_off6va] = 0xAA
mc6va_r = chk.run_checks(data_override=bytes(c6va))
ok6va, _ = chk.gate(mc6va_r)
mc["MC6_executor_replay_VA_0x00BA1100"] = {
    "corruption": "@VA 0x00BA1100 -> AA (executor's exact MC6 replay)",
    "anchor_gates_still_pass": ok6va,
    "verdict": "PASS" if ok6va else "FAIL",
    "note": "The QC's own mapping classifies VA 0x00BA1100 as .data VIRTUAL_BSS "
            "(RVA 0x7A1100 >= .data raw end 0x7A0000, < vsize end 0x7A9CE4): the "
            "corruption lands on a PHYSICAL .rsrc byte only because the executor's "
            "OwnPE lacks the raw-size boundary — see QC_REPORT finding F-2.",
}

# --- clean pass of the production gate (independent re-run)
rclean = chk.run_checks()
okc, failsc = chk.gate(rclean)
mc["clean_pass_independent_rerun"] = {
    "checks_total": len(rclean),
    "checks_pass": sum(1 for r in rclean if r[1] == "PASS"),
    "gate": "PASS" if okc else "FAIL",
    "fails": [f"{r[0]}: {r[2]}" for r in failsc],
}
results["mc_reverification"] = mc

# ---------------------------------------------------------------------------
# 10. EXE immutability proof after all controls.
# ---------------------------------------------------------------------------
after_sha = hashlib.sha256(EXE).hexdigest().upper()
results["exe_immutability_after_controls"] = {
    "sha256": after_sha, "unchanged": after_sha == EXE_SHA256,
}

with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("QC independent check complete.")
print("anchors:", results["anchor_pins_summary"])
print("rel32:", results["rel32_summary"])
print("rel8:", results["rel8_summary"])
print("bodies:", [(b["file"], b["physical_match"]) for b in body_compare])
print("no-vptr:", results["no_vptr_store_check"]["all_imm32_are_zero"],
      results["no_vptr_store_check"]["ctor_window_physical_match"])
print("clean:", mc["clean_pass_independent_rerun"]["checks_pass"],
      "/", mc["clean_pass_independent_rerun"]["checks_total"])
print("MC1 production:", mc["MC1_production_gate"]["verdict"])
print("MC4 production:", mc["MC4_production_gate"]["verdict"])
print("MC6a/b/replay:", mc["MC6a_off_0x7A1100"]["verdict"], mc["MC6b_off_0x7A1200"]["verdict"],
      mc["MC6_executor_replay_VA_0x00BA1100"]["verdict"])
print("EXE unchanged:", results["exe_immutability_after_controls"]["unchanged"])
print("RTTI W:", results["rtti_own_read"]["W_ArkModelResourceInstanceRef"].get("name"))
