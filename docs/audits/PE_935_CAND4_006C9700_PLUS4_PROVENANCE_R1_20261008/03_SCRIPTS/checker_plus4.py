"""checker_plus4.py — the production gate of PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008.

A small checker that uses the PHYSICAL EXE with its OWN PE mapping and recomputation
(NOT the report/CSV/JSON): verifies the EXE identity (fail-closed), the used byte
windows (pin list), the rel32 arithmetic, the return/load/write anchors of the
analysis, and the RTTI pointer chains. Hash/pin PASS does NOT approve dataflow or
semantic role (contract §6): class/return/source adjudication is done by the
author/QC — the checker validates only the physical anchors.

python -B; no bytecode; stdlib only. The pins are the load-bearing anchors of this
run's evidence (01_RAW/PINS_AND_REL32.txt).
"""
import hashlib
import struct
import sys

EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_SIZE = 8015872
EXE_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
IMAGE_BASE = 0x00400000


class OwnPE:
    """Own independent PE32 mapping (sections from the physical headers)."""

    def __init__(self, data):
        self.data = data
        e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
        if data[e_lfanew:e_lfanew + 4] != b"PE\x00\x00":
            raise ValueError("PE signature missing")
        coff = e_lfanew + 4
        machine, nsec = struct.unpack_from("<HH", data, coff)
        if machine != 0x014C:
            raise ValueError(f"machine {machine:#x}")
        size_opt = struct.unpack_from("<H", data, coff + 16)[0]
        sec0 = coff + 20 + size_opt
        self.sections = []
        for i in range(nsec):
            off = sec0 + 40 * i
            vsize, va, rsize, roff = struct.unpack_from("<IIII", data, off + 8)
            self.sections.append((va, vsize, roff, rsize))

    def va_to_off(self, va):
        rva = va - IMAGE_BASE
        for va_s, vsize, roff, rsize in self.sections:
            if va_s <= rva < va_s + max(vsize, rsize):
                fo = roff + (rva - va_s)
                if fo < len(self.data):
                    return fo
                return None
        return None

    def read(self, va, n):
        fo = self.va_to_off(va)
        if fo is None:
            raise ValueError(f"VA {va:#010x} not mapped")
        return self.data[fo:fo + n]

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
# PIN TABLE: (pin_id, va, expected_bytes) — the load-bearing anchors of this run.
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

# ---------------------------------------------------------------------------
# REL32 TABLE: (id, call_va, expected_target) — recomputed from the physical bytes.
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# RTTI TABLE: (id, vtable_va, expected_name) — vtable[-1] -> COL -> TypeDescriptor
# (absolute-VA pointer fields in this build) -> name.
# ---------------------------------------------------------------------------
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


def run_checks(data_override=None):
    """Run all checks. data_override = an in-memory CORRUPTED copy (mechanical
    controls) — the same gates run against it; no file is ever modified."""
    results = []
    if data_override is None:
        try:
            data = load_pinned()
            results.append(("EXE_IDENTITY", "PASS", "physical EXE size+SHA256 == pinned"))
        except ValueError as e:
            results.append(("EXE_IDENTITY", "FAIL", str(e)))
            return results
    else:
        data = data_override
        if len(data) != EXE_SIZE:
            results.append(("EXE_IDENTITY_OVERRIDE_SIZE", "FAIL", f"size {len(data)}"))
            return results
        results.append(("EXE_IDENTITY", "PASS", "override buffer (size ok; identity check per caller)"))

    pe = OwnPE(data)

    # 1. byte pins
    for pin_id, va, hexstr in BYTE_PINS:
        expected = bytes.fromhex(hexstr.replace(" ", ""))
        try:
            got = pe.read(va, len(expected))
        except ValueError as e:
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
        except ValueError as e:
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

    # 3. RTTI chains (vtable[-1] -> COL -> TypeDescriptor(+8 name) )
    for rtti_id, vt, name in RTTI_PINS:
        try:
            col_ptr = pe.u32(vt - 4)
            col_off = pe.va_to_off(col_ptr)
            if col_off is None:
                results.append((f"RTTI:{rtti_id}", "FAIL",
                                f"vtable {vt:#010x} COL ptr {col_ptr:#010x} unmapped"))
                continue
            sig, _o, _cd, ptd, _pcd = struct.unpack_from("<5I", data, col_off)
            if sig != 0:
                results.append((f"RTTI:{rtti_id}", "FAIL", f"COL sig {sig:#x} != 0"))
                continue
            ptd_off = pe.va_to_off(ptd)
            if ptd_off is None:
                results.append((f"RTTI:{rtti_id}", "FAIL",
                                f"TypeDescriptor {ptd:#010x} unmapped"))
                continue
            got = data[ptd_off + 8:ptd_off + 8 + len(name) + 1]
            if got[:-1] == name and got[-1] == 0:
                results.append((f"RTTI:{rtti_id}", "PASS",
                                f"vtable {vt:#010x} -> COL {col_ptr:#010x} -> TD {ptd:#010x} -> {name.decode()}"))
            else:
                results.append((f"RTTI:{rtti_id}", "FAIL",
                                f"vtable {vt:#010x} name mismatch: {got!r}"))
        except ValueError as e:
            results.append((f"RTTI:{rtti_id}", "FAIL", str(e)))

    # 4. string pins
    for sid, va, s in STRING_PINS:
        try:
            got = pe.read(va, len(s) + 1)
            if got[:-1] == s and got[-1] == 0:
                results.append((f"STR:{sid}", "PASS", f"@{va:#010x} == {s.decode()}"))
            else:
                results.append((f"STR:{sid}", "FAIL", f"@{va:#010x} mismatch: {got!r}"))
        except ValueError as e:
            results.append((f"STR:{sid}", "FAIL", str(e)))

    return results


def gate(results):
    """The production gate: PASS only if every check PASSes."""
    fails = [r for r in results if r[1] != "PASS"]
    return (len(fails) == 0), fails


def main():
    results = run_checks()
    ok, fails = gate(results)
    npass = sum(1 for r in results if r[1] == "PASS")
    print(f"checker_plus4: {npass}/{len(results)} checks PASS")
    for rid, verdict, detail in results:
        if verdict != "PASS":
            print(f"  FAIL {rid}: {detail}")
    print("GATE:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
