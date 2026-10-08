"""ctrl4_exact_endpoint.py — REBUILT CTRL_4 (caller-side EXACT final-argument predicate)
for PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007 (contract §3 of the
correction).

SUPERSEDED implementation: SOURCE_PACKAGE 03_SCRIPTS/qc_controls.py lines 150-199
(ctrl4_preservation). DEFECT (Desktop C4-C2): its push_edi boolean is satisfied by ANY
`push edi` in the window (the window contains an earlier push edi @0x0050A3D7), it does
NOT require the final child argument at the exact site 0x0050A3F6, and it does NOT bind
the join call endpoint at 0x0050A3F7 — so the mutants `0x0050A3F6: 57->56 (push esi)`
and `0x0050A3F6: 57->90 (nop)` FALSE-PASS it (Desktop CONTROL_COUNTERCHECKS.json).

THIS REBUILD requires ALL of the following SIMULTANEOUSLY, with instructions verified
at EXACT addresses on CORRECT decode boundaries (boundary-safe linear decode of the
whole window; a mnemonic anywhere in the window is never accepted as the endpoint):
  P1 exact head:        instruction starting @0x0050A3B7 == `mov edi, eax`   (bytes 8B F8)
  P2 no caller-side EDI write in the required range (0x0050A3B7, 0x0050A3F6) exclusive
  P3 exact final child argument: instruction starting @0x0050A3F6 == `push edi`      (byte 57)
  P4 exact join call endpoint:  instruction starting @0x0050A3F7 == `call edx` (bytes FF D2),
     without shift — a CALL mnemonic anywhere else in the window does NOT satisfy P4.

Required matrix (same checker, all cases; contract §3):
  REAL CLEAN (the published window bytes)               = PASS
  historical EDI-clobber mutant (@0x0050A3DD 8B 3D D0 D8 B9 00) = FAIL (P2)
  0x0050A3F6: push edi -> push esi (57 -> 56)            = FAIL (P3)
  0x0050A3F6: push edi -> nop      (57 -> 90)            = FAIL (P3)
ALL BUFFERS ARE SYNTHETIC / IN-MEMORY ONLY. No EXE access; no mutation is ever written
to any file (the EXE, SOURCE_PACKAGE, or any historical record).

The script ALSO reproduces the OLD checker's LOGIC (not its EXE reads or package writes)
over the same in-memory buffers, to document the two false PASS (the old boolean
semantics: first-instruction head check + ANY push edi + any EDI write detection).

Fixture provenance (INPUT_IDENTITIES.md §5): the clean window buffer is the 0x42 bytes
of WINDOW 0x0050A3B7..0x0050A3F8 exactly as published per-instruction in SOURCE_PACKAGE
01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt (verified: instruction lengths, both rel8 targets,
all four rel32 call targets and the total length 0x42 recompute correctly).

Writes: merges into CONTROL_RESULTS.json (package root; ctrl3_rebuilt.py wrote the
CTRL_3_REBUILT section first — this script reads, adds its sections, rewrites the file).
"""
import json
import os

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- fixtures
# The published §7 join window (SOURCE_PACKAGE 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt),
# 0x0050A3B7..0x0050A3F8 = 0x42 bytes, rebuilt from the per-instruction byte column:
CLEAN_WINDOW_HEX = (
    "8B F8"                      # 0x0050A3B7 mov edi, eax          (8B F8)
    " E8 D2 6B 1B 00"            # 0x0050A3B9 call 0x6C0F90
    " 84 C0"                      # 0x0050A3BE test al, al
    " 74 06"                      # 0x0050A3C0 je   0x50A3C8
    " 83 4E 2C 02"               # 0x0050A3C2 or   [esi+0x2C], 2
    " EB 04"                      # 0x0050A3C6 jmp  0x50A3CC
    " 83 66 2C FD"               # 0x0050A3C8 and  [esi+0x2C], 0xFFFFFFFD
    " 8B 4E 20"                  # 0x0050A3CC mov  ecx, [esi+0x20]
    " E8 DC 6C 1B 00"            # 0x0050A3CF call 0x6C10B0
    " 8B CE"                      # 0x0050A3D4 mov  ecx, esi
    " 50"                         # 0x0050A3D6 push eax
    " 57"                         # 0x0050A3D7 push edi            (earlier push — NOT the final site)
    " E8 03 FE FF FF"            # 0x0050A3D8 call 0x50A1E0
    " 8B 8E 8C 00 00 00"         # 0x0050A3DD mov  ecx, [esi+0x8C]
    " 56"                         # 0x0050A3E3 push esi
    " E8 F7 A2 01 00"            # 0x0050A3E4 call 0x5246E0
    " 8B 4E 30"                  # 0x0050A3E9 mov  ecx, [esi+0x30]
    " 8B 01"                      # 0x0050A3EC mov  eax, [ecx]
    " 8B 90 A4 00 00 00"         # 0x0050A3EE mov  edx, [eax+0xA4] (NiNode vtable slot 41)
    " 6A 00"                      # 0x0050A3F4 push 0
    " 57"                         # 0x0050A3F6 push edi            (THE FINAL JOIN CHILD ARGUMENT)
    " FF D2"                      # 0x0050A3F7 call edx            (THE JOIN CALL — exact endpoint)
)
WIN_VA = 0x0050A3B7
HEAD_VA = 0x0050A3B7
FINAL_PUSH_VA = 0x0050A3F6
JOIN_CALL_VA = 0x0050A3F7

CLEAN_WINDOW = bytes.fromhex(CLEAN_WINDOW_HEX)
assert len(CLEAN_WINDOW) == 0x42, f"clean window must be 0x42 bytes, got {len(CLEAN_WINDOW):X}"

CLOBBER_VA = 0x0050A3DD
CLOBBER_BYTES = bytes.fromhex("8B 3D D0 D8 B9 00")   # mov edi, dword ptr [0xB9D8D0] — the historical SYNTHETIC clobber


def make_clobber_mutant():
    buf = bytearray(CLEAN_WINDOW)
    off = CLOBBER_VA - WIN_VA
    assert buf[off:off + 6] == bytes.fromhex("8B 8E 8C 00 00 00")  # same 6-byte length: boundaries preserved
    buf[off:off + 6] = CLOBBER_BYTES
    return bytes(buf)


def make_final_arg_mutant(new_byte):
    assert new_byte in (0x56, 0x90)
    buf = bytearray(CLEAN_WINDOW)
    off = FINAL_PUSH_VA - WIN_VA
    assert buf[off] == 0x57
    buf[off] = new_byte
    return bytes(buf)


# ---------------------------------------------------------------- minimal x86-32 decoder
# Opcode coverage: exactly the forms present in the window + mutants (documented in
# INPUT_IDENTITIES.md §6). reg index: 0=eax 1=ecx 2=edx 3=ebx 4=esp 5=ebp 6=esi 7=edi
REG = ["eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi"]
GRP1 = ["add", "or", "adc", "sbb", "and", "sub", "xor", "cmp"]


class Insn:
    __slots__ = ("va", "size", "mnemonic", "op_str", "writes_edi", "bytes")

    def __init__(self, va, size, mnemonic, op_str, writes_edi, raw):
        self.va, self.size = va, size
        self.mnemonic, self.op_str = mnemonic, op_str
        self.writes_edi = writes_edi
        self.bytes = raw

    def hex(self):
        return " ".join(f"{b:02X}" for b in self.bytes)


def _modrm(b, i):
    m = b[i]
    return (m >> 6) & 3, (m >> 3) & 7, m & 7


def decode(buf, base_va):
    """Boundary-safe linear decode of the whole buffer. Returns {va: Insn}.

    Raises ValueError if any byte is outside the covered opcode set (fail-closed:
    an undecodable window FAILS the checker rather than skipping bytes).
    """
    out = {}
    i, va = 0, base_va
    while i < len(buf):
        start = i
        op = buf[i]
        writes_edi = False
        if op == 0x8B or op == 0x89 or op == 0x8D:          # mov r32,r/m32 | mov r/m32,r32 | lea
            mod, reg, rm = _modrm(buf, i + 1)
            if mod == 0b01:
                size, memoff = 3, buf[i + 2]
            elif mod == 0b10:
                size, memoff = 6, int.from_bytes(buf[i + 2:i + 6], "little")
            elif mod == 0b00 and rm == 0b101:
                size, memoff = 6, int.from_bytes(buf[i + 2:i + 6], "little")
            elif mod == 0b00:
                size, memoff = 2, 0
            else:
                size, memoff = 2, None
            if op == 0x8B:                                   # mov REG, r/m  -> writes REG
                writes_edi = (reg == 7)
                if memoff is None and mod == 0b11:
                    op_str = f"{REG[reg]}, {REG[rm]}"
                elif mod == 0b00 and rm == 0b101:
                    op_str = f"{REG[reg]}, dword ptr [0x{memoff:08x}]"
                elif mod == 0b00:
                    op_str = f"{REG[reg]}, [{REG[rm]}]"
                else:
                    op_str = f"{REG[reg]}, dword ptr [{REG[rm]} + 0x{memoff:x}]"
                mn = "mov"
            elif op == 0x89:                                 # mov r/m, REG  -> writes r/m (reg form: writes rm)
                writes_edi = (mod == 0b11 and rm == 7)
                if mod == 0b11:
                    op_str = f"{REG[rm]}, {REG[reg]}"
                elif mod == 0b00 and rm == 0b101:
                    op_str = f"dword ptr [0x{memoff:08x}], {REG[reg]}"
                elif mod == 0b00:
                    op_str = f"[{REG[rm]}], {REG[reg]}"
                else:
                    op_str = f"dword ptr [{REG[rm]} + 0x{memoff:x}], {REG[reg]}"
                mn = "mov"
            else:                                            # lea
                writes_edi = (reg == 7)
                op_str = f"{REG[reg]}, dword ptr [{REG[rm]} + 0x{memoff:x}]" if mod != 0b00 or rm != 0b101 \
                    else f"{REG[reg]}, [0x{memoff:08x}]"
                mn = "lea"
        elif op == 0x84:                                     # test r/m8, r8
            mod, reg, rm = _modrm(buf, i + 1)
            reg8 = ["al", "cl", "dl", "bl", "ah", "ch", "dh", "bh"]
            size = 2 if mod == 0b11 else (3 if mod == 0b01 else 6)
            op_str = f"{reg8[rm]}, {reg8[reg]}" if mod == 0b11 else f"byte ptr [...], {reg8[reg]}"
            mn = "test"
        elif op == 0x74 or op == 0xEB:                       # je rel8 / jmp rel8
            rel = buf[i + 1] if buf[i + 1] < 0x80 else buf[i + 1] - 0x100
            size, op_str, mn = 2, f"0x{va + 2 + rel:08x}", ("je" if op == 0x74 else "jmp")
        elif op == 0x83:                                     # grp1 r/m32, imm8 (sign-extended)
            mod, reg, rm = _modrm(buf, i + 1)
            imm = buf[i + 2] if buf[i + 2] < 0x80 else buf[i + 2] - 0x100
            if mod == 0b11:
                size, op_str = 3, f"{REG[rm]}, {imm & 0xFFFFFFFF:#x}"
                writes_edi = (rm == 7)
            elif mod == 0b01:
                size, op_str = 4, f"dword ptr [{REG[rm]} + 0x{buf[i + 2]:x}], {imm & 0xFFFFFFFF:#x}"
            else:
                raise ValueError(f"uncovered 0x83 mod={mod:02b}")
            mn = GRP1[reg]
        elif op == 0x6A:                                     # push imm8
            size, op_str, mn = 2, f"{buf[i + 1]}", "push"
        elif 0x50 <= op <= 0x57:                             # push r32 (reads the register)
            size, op_str, mn = 1, REG[op - 0x50], "push"
        elif 0x58 <= op <= 0x5F:                             # pop r32 (writes the register)
            size, op_str, mn = 1, REG[op - 0x58], "pop"
            writes_edi = (op == 0x5F)
        elif op == 0xBF:                                      # mov edi, imm32 (writes edi)
            size, op_str, mn = 5, f"edi, 0x{int.from_bytes(buf[i + 1:i + 5], 'little'):08x}", "mov"
            writes_edi = True
        elif op == 0xE8:                                     # call rel32
            rel = int.from_bytes(buf[i + 1:i + 5], "little", signed=True)
            size, op_str, mn = 5, f"0x{va + 5 + rel:08x}", "call"
        elif op == 0xFF:                                     # grp5; /2 = call r/m32
            mod, reg, rm = _modrm(buf, i + 1)
            if reg == 0b010 and mod == 0b11:
                size, op_str, mn = 2, REG[rm], "call"
            else:
                raise ValueError(f"uncovered FF /{reg} mod={mod:02b}")
        elif op == 0x90:                                     # nop
            size, op_str, mn = 1, "", "nop"
        else:
            raise ValueError(f"uncovered opcode {op:02X} @0x{va:08X}")
        out[va] = Insn(va, size, mn, op_str, writes_edi, buf[start:start + size])
        i += size
        va += size
    return out


# ---------------------------------------------------------------- rebuilt checker
def ctrl4_exact_endpoint(window_bytes, base_va=WIN_VA):
    """Return (ok, detail). PASS iff P1..P4 hold simultaneously."""
    try:
        insns = decode(window_bytes, base_va)
    except (ValueError, IndexError) as exc:
        return False, f"window not boundary-decodable ({exc}) — FAIL closed"
    # P1 exact head @0x0050A3B7 == mov edi, eax (bytes 8B F8)
    head = insns.get(HEAD_VA)
    if head is None or head.mnemonic != "mov" or head.op_str != "edi, eax" or head.bytes != b"\x8B\xF8":
        got = f"{head.mnemonic} {head.op_str} [{head.hex()}]" if head else "no instruction"
        return False, f"P1 FAIL: exact head mov edi,eax @0x0050A3B7 (8B F8) not found (got: {got})"
    # P2 no caller-side EDI write in (0x0050A3B7, 0x0050A3F6)
    for va in sorted(insns):
        if HEAD_VA < va < FINAL_PUSH_VA and insns[va].writes_edi:
            bad = insns[va]
            return False, f"P2 FAIL: caller-side EDI write @0x{va:08X} in the required range: '{bad.mnemonic} {bad.op_str}'"
    # P3 exact final child argument @0x0050A3F6 == push edi (byte 57)
    fin = insns.get(FINAL_PUSH_VA)
    if fin is None or fin.mnemonic != "push" or fin.op_str != "edi" or fin.bytes != b"\x57":
        got = f"{fin.mnemonic} {fin.op_str} [{fin.hex()}]" if fin else "no instruction"
        return False, f"P3 FAIL: exact final child argument push edi @0x0050A3F6 (57) not found (got: {got})"
    # P4 exact join call endpoint @0x0050A3F7 == call edx (bytes FF D2), no shift
    jcal = insns.get(JOIN_CALL_VA)
    if jcal is None or jcal.mnemonic != "call" or jcal.op_str != "edx" or jcal.bytes != b"\xFF\xD2":
        got = f"{jcal.mnemonic} {jcal.op_str} [{jcal.hex()}]" if jcal else "no instruction"
        return False, f"P4 FAIL: exact join call endpoint call edx @0x0050A3F7 (FF D2, no shift) not found (got: {got})"
    return True, ("PASS: P1 exact head mov edi,eax @0x0050A3B7 (8B F8); P2 no caller-side EDI write in "
                  "(0x0050A3B7, 0x0050A3F6); P3 exact final child argument push edi @0x0050A3F6 (57); "
                  "P4 exact join call endpoint call edx @0x0050A3F7 (FF D2) — all on verified decode boundaries")


# ---------------------------------------------------------------- old-logic reproduction
def ctrl4_OLD_logic(window_bytes, base_va=WIN_VA):
    """Faithful LOGIC reproduction of qc_controls.py ctrl4_preservation (lines 151-176):
    first instruction must be mov edi,eax; ANY `push edi` in the window sets push_edi;
    any EDI-writing instruction between head and push FAILs; otherwise PASS iff push_edi.
    (No EXE read; no package write — the buffer is an in-memory argument, exactly as the
    Desktop ran the extracted old function.)"""
    try:
        insns = decode(window_bytes, base_va)
        ordered = [insns[va] for va in sorted(insns)]
    except (ValueError, IndexError) as exc:
        return False, f"window not decodable ({exc})"
    first = ordered[0]
    if not (first.mnemonic == "mov" and "edi, eax" in first.op_str):
        return False, f"chain head missing (got '{first.mnemonic} {first.op_str}')"
    edi_write, push_edi = None, False
    for ins in ordered[1:]:
        if ins.mnemonic == "push" and ins.op_str == "edi":
            push_edi = True
            continue
        if ins.writes_edi:
            edi_write = edi_write or f"0x{ins.va:08x} {ins.mnemonic} {ins.op_str}"
    if edi_write:
        return False, f"EDI clobbered at {edi_write}"
    if not push_edi:
        return False, "push edi @0x0050A3F6 missing"
    return True, "chain intact: mov edi,eax; no EDI write before push edi; push edi present"


def run_and_write():
    CASES = [
        ("real_clean", CLEAN_WINDOW, "the published §7 window bytes (0x0050A3B7..0x0050A3F8, 0x42 B; SOURCE_PACKAGE 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt)", "PASS"),
        ("historical_edi_clobber", make_clobber_mutant(), "SYNTHETIC in-memory mutant: 6 bytes @0x0050A3DD replaced with 8B 3D D0 D8 B9 00 (mov edi,[0xB9D8D0]) — the historical clobber case", "FAIL"),
        ("final_push_esi", make_final_arg_mutant(0x56), "SYNTHETIC in-memory mutant @0x0050A3F6: 57 -> 56 (push edi -> push esi); the earlier push edi @0x0050A3D7 survives", "FAIL"),
        ("final_push_nop", make_final_arg_mutant(0x90), "SYNTHETIC in-memory mutant @0x0050A3F6: 57 -> 90 (push edi -> nop); the earlier push edi @0x0050A3D7 survives", "FAIL"),
    ]

    matrix = {}
    for name, buf, desc, expected in CASES:
        ok_new, det_new = ctrl4_exact_endpoint(buf)
        ok_old, det_old = ctrl4_OLD_logic(buf)
        matrix[name] = {
            "case": desc,
            "mutants_synthetic_memory_only": True,
            "expected_new_checker": expected,
            "new_exact_endpoint_checker": {
                "result": "PASS" if ok_new else "FAIL",
                "detail": det_new,
            },
            "old_checker_logic_reproduction": {
                "result": "PASS" if ok_old else "FAIL",
                "detail": det_old,
                "note": ("FALSE PASS of the superseded predicate (any push edi in the window keeps the boolean) — "
                         "reproduced from the old checker's logic over the same in-memory buffer"
                         if (name in ("final_push_esi", "final_push_nop") and ok_old)
                         else "consistent with the historical result of the old checker"),
            },
        }

    verdict_ok = (
        matrix["real_clean"]["new_exact_endpoint_checker"]["result"] == "PASS"
        and all(matrix[n]["new_exact_endpoint_checker"]["result"] == "FAIL"
                for n in ("historical_edi_clobber", "final_push_esi", "final_push_nop"))
        and matrix["real_clean"]["old_checker_logic_reproduction"]["result"] == "PASS"
        and matrix["historical_edi_clobber"]["old_checker_logic_reproduction"]["result"] == "FAIL"
        and all(matrix[n]["old_checker_logic_reproduction"]["result"] == "PASS"
                for n in ("final_push_esi", "final_push_nop"))
    )

    OUT_SECTION = {
        "CTRL_4_EXACT_ENDPOINT_REBUILT": {
            "checker": ("ctrl4_exact_endpoint (rebuilt; caller-side §7 chain: P1 exact head @0x0050A3B7 (8B F8) AND "
                        "P2 no EDI write in (0x0050A3B7, 0x0050A3F6) AND P3 exact final child argument push edi "
                        "@0x0050A3F6 (57) AND P4 exact join call endpoint call edx @0x0050A3F7 (FF D2, no shift); "
                        "exact-address instruction lookup on verified decode boundaries; ONE code path for all cases"),
            "rebuilt_because": ("the source-run implementation (qc_controls.py:150-199) accepted ANY push edi in the window "
                                "(the earlier push edi @0x0050A3D7 keeps its boolean) and did not bind the predicate to "
                                "the exact final-argument site / join call endpoint — two Desktop false-PASS mutants"),
            "exe_accessed": False,
            "clean_buffer_provenance": ("the 0x42 published window bytes of SOURCE_PACKAGE 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt "
                                        "(per-instruction byte column; lengths/rel8/rel32/total-length re-verified)"),
            "matrix": matrix,
            "verdict": "PASS" if verdict_ok else "FAIL",
            "range": ("same checker; same window range (0x0050A3B7..0x0050A3F8); clean = the published bytes; "
                      "mutants = synthetic in-memory byte edits at the exact endpoint sites"),
            "semantic_scope": ("CALLER-SIDE exact final-argument predicate ONLY — no claim about callee-preservation "
                               "completeness; the four intervening callee bodies (FUN_006C0F90/FUN_006C10B0/"
                               "FUN_0050A1E0/FUN_005246E0) remain UNOPENED; CHILD_TO_JOIN_IDENTITY stays "
                               "STRONGLY_SUPPORTED (NOT CONFIRMED); this control does not promote it"),
            "historical_results_preserved": ("the four historically executed test cases remain authentic measurements of the "
                                            "OLD checker (clean PASS and EDI-clobber FAIL did occur; see SUPERSESSION.md); "
                                            "what is superseded is the stronger claim that the old predicate checked the "
                                            "exact final child argument — the two false-PASS mutants and this rebuild "
                                            "disprove that"),
        }
    }

    path = os.path.join(PKG, "CONTROL_RESULTS.json")
    with open(path, encoding="utf-8") as f:
        out = json.load(f)
    out.update(OUT_SECTION)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(json.dumps(OUT_SECTION, indent=2, ensure_ascii=False))
    print(f"\nverdict: {OUT_SECTION['CTRL_4_EXACT_ENDPOINT_REBUILT']['verdict']}; wrote {path}")
    return OUT_SECTION


if __name__ == "__main__":
    run_and_write()
