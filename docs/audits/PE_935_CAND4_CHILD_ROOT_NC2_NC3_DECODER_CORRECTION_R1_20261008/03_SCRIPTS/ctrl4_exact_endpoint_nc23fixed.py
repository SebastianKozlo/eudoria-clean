"""ctrl4_exact_endpoint_nc23fixed.py — CORRECTED CTRL_4 production successor
(NC2 MEMORY-TEST + NC3-B LEA-REGISTER DECODER CORRECTION) for
PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008
(RECORDS_AND_QC_MACHINERY_CORRECTION; frozen human-authorized contract
OPENCODE_NC2_NC3_CORRECTION.md, SIZE 14069, SHA256
3E0BDB58A0CDC1488DE9477A855CEC04D712D492E147CC92CDB3C021B5143B8F).

SUCCESSOR OF (READ-ONLY, UNCHANGED, UNMODIFIED): SOURCE_PACKAGE
docs/audits/PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007/
03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py as published at
91598a9868037c4954e22e16c535d6a5a671771e (SHA256
44155437F20FA6DA9D6847A236F708C7F2A40F26BABE71424B21C325B4FB4405).

THE THREE CORRECTIONS OF THIS SUCCESSOR (all decoder-only; checker predicate,
fixtures and provenance unchanged):

NC2 — decode(), opcode 0x84 (TEST r/m8, r8): a memory TEST form is genuinely
2 bytes long in the simplest case (84 06 = test byte ptr [esi], al), but the
sibfixed length logic assigns 3 (mod=01) or 6 (mod=00/10) bytes and thereby
boundary-shifts a later writer out of P2's sight. Desktop residual test
NON_SIB_TEST_HIDDEN_EDI (CONTROL_COUNTERCHECKS.json, cited): the synthetic span
    @0x0050A3DD..0x0050A3E8:  84 06 BF AA BB CC E8 90 90 90 90 90
is TRUE-decoded (capstone 5.0.7 reference, cited) as
    0x0050A3DD: 84 06            test byte ptr [esi], al   (2 bytes)
    0x0050A3DF: BF AA BB CC E8   mov edi, 0xE8CCBBAA       (5 bytes — EDI WRITE
                          inside the prohibited P2 range (0x0050A3B7, 0x0050A3F6))
    0x0050A3E4..0x0050A3E8: 90 x5 (nops)
so the TRUE expected verdict is FAIL, while sibfixed mis-decodes the first 6
bytes (84 06 BF AA BB CC) as one TEST and FALSE-PASSES the buffer. CORRECTION:
ALL memory TEST forms (mod != 0b11) are now REJECTED FAIL-CLOSED BEFORE any
length computation:
    if mod != 0b11:
        raise ValueError(f"unsupported memory TEST form (mod={mod:02b}) — FAIL CLOSED")
Register TEST (84 C0, mod=11 — the form used by the clean window @0x0050A3BE)
STAYS SUPPORTED. Memory TEST decoding is NOT added (not required; fail-closed
rejection is the bounded correction — the contract-preferred minimal repair).

NC3-B — decode(), opcode 0x8D (LEA): LEA with mod=11 (register form, e.g. 8D C0)
is an INVALID x86 encoding. sibfixed computed size=2 / memoff=None for it and
then crashed INSIDE OPERAND FORMATTING with
    TypeError: unsupported format string passed to NoneType.__format__
which escapes the checker (its fail-closed catch is (ValueError, IndexError)
only) — an unexpected exception instead of a controlled verdict. CORRECTION:
LEA with mod=11 is now rejected EXPLICITLY, BEFORE operand formatting and
before any verdict computation:
    if op == 0x8D and mod == 0b11:
        raise ValueError("unsupported LEA register form (mod=11) — FAIL CLOSED")
so the CHECKER returns (False, diagnostic) — never a TypeError, never an
unexpected exception. Memory LEA forms remain supported exactly as before, and
the 0x8B/0x89 register forms remain supported exactly as before (verified by
03_SCRIPTS/run_nc23_matrix.py register-form support battery).

NC3 (0xFF branch, UNCHANGED BY THIS RUN — kept exactly as sibfixed): grp5
supports ONLY FF /2 (call r/m32) with mod=11 — the FF D2 join-call endpoint
required by P4. Every other FF form (including the invalid register far-call
form FF D8 = FF /3 with mod=11, Desktop residual test INVALID_FF_FAR_CALL_
REGISTER) raises ValueError("uncovered FF /{reg} mod={mod:02b}"). FF /6 and no
other forms are added (decoder coverage is NOT extended).

NC1 PRESERVED: the fail-closed SIB guard stays in EVERY memory-ModRM branch
(0x8B/0x89/0x8D; 0x84; 0x83; 0xFF):
    if mod != 0b11 and rm == 0b100:
        raise ValueError(f"unsupported SIB form (mod={mod:02b} rm=100) — FAIL CLOSED")
BEFORE any displacement/length computation (sibfixed contract §5 semantics,
unchanged). In the 0x84 branch the NC1 guard runs BEFORE the NC2 memory-TEST
rejection (SIB TEST forms report the NC1 mechanism; non-SIB memory TEST forms
report the NC2 mechanism — both fail-closed, both before any length math).

ALSO UNCHANGED from sibfixed:
- The P1-P4 exact-endpoint predicate (P1 exact head 8B F8 @0x0050A3B7; P2 no
  caller-side EDI write in the open range (0x0050A3B7, 0x0050A3F6); P3 exact
  57 @0x0050A3F6; P4 exact FF D2 @0x0050A3F7, no shift).
- The fail-closed decode design: bytes are never skipped and decode never
  continues past a rejected/unsupported form.
- The checker's catch is ONLY (ValueError, IndexError); any unexpected
  exception propagates (recorded as ERROR, never as an expected FAIL). No
  blanket catch of unexpected exceptions exists or is added.
- The P3_TOOLING_CLEANUP grp1-imm8 fix (0x83 mod=01 immediate read from
  opcode+3, after the disp8 at opcode+2).

Fixture provenance (identical to sibfixed — the very same published record):
the clean window buffer is the 0x42 bytes of WINDOW 0x0050A3B7..0x0050A3F8
exactly as published per-instruction in the PRIOR_SCIENCE_PACKAGE record
docs/audits/PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/01_RAW/
JOIN_WINDOW_50A3B7_REPIN.txt (BASE-blob-verified). All mutation cases are
SYNTHETIC / IN-MEMORY ONLY.

This module performs NO file I/O and NO EXE access of any kind; it is INERT at
import (only constant definitions and a fixture-length assert execute at module
level). No mutation is ever written to any file (the EXE, the SOURCE_PACKAGE,
the PRIOR packages, or any historical record).
"""

# ---------------------------------------------------------------- fixtures
# The published §7 join window (PRIOR_SCIENCE_PACKAGE 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt),
# 0x0050A3B7..0x0050A3F8 = 0x42 bytes, rebuilt from the per-instruction byte column
# (identical fixture definition to the READ-ONLY sibfixed production checker):
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

# NC1 synthetic counterexample (unchanged from sibfixed): 12 bytes replacing the clean span
# 0x0050A3DD..0x0050A3E8 (mov ecx,[esi+0x8C] + push esi + call 0x5246E0). The first
# instruction is a 7-byte MOV with ModRM rm=4 + SIB (8B 8C 24 disp32); the reference
# boundary set then decodes `mov edi, 0x90CCBBAA` at 0x0050A3E4 — an EDI write inside
# the prohibited P2 range that the old SIB-less length logic hid.
NC1_SIB_VA = 0x0050A3DD
NC1_SIB_SPAN_LEN = 12
NC1_SIB_ORIGINAL = bytes.fromhex("8B 8E 8C 00 00 00 56 E8 F7 A2 01 00")
NC1_SIB_BYTES = bytes.fromhex("8B 8C 24 8C 00 00 E8 BF AA BB CC 90")

# NC2/NC3 synthetic counterexamples (contract §4): the SAME 12-byte span
# 0x0050A3DD..0x0050A3E8, three variants. All three preserve the total window 0x42
# and the P1/P3/P4 bytes; only the 12 span bytes change.
NC23_SPAN_VA = 0x0050A3DD
NC23_SPAN_LEN = 12
NC23_SPAN_ORIGINAL = bytes.fromhex("8B 8E 8C 00 00 00 56 E8 F7 A2 01 00")
NC2_NON_SIB_TEST_BYTES = bytes.fromhex("84 06 BF AA BB CC E8 90 90 90 90 90")
NC3_INVALID_FF_BYTES = bytes.fromhex("FF D8 90 90 90 90 90 90 90 90 90 90")
NC3_INVALID_LEA_BYTES = bytes.fromhex("8D C0 90 90 90 90 90 90 90 90 90 90")


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


def make_nc1_sib_mutant():
    buf = bytearray(CLEAN_WINDOW)
    off = NC1_SIB_VA - WIN_VA
    assert len(NC1_SIB_BYTES) == NC1_SIB_SPAN_LEN
    assert buf[off:off + NC1_SIB_SPAN_LEN] == NC1_SIB_ORIGINAL  # 12-byte span: total window stays 0x42
    buf[off:off + NC1_SIB_SPAN_LEN] = NC1_SIB_BYTES
    return bytes(buf)


def make_nc23_span_mutant(replacement_bytes):
    """NC2/NC3 counterexample builder: replaces EXACTLY the 12 span bytes
    @0x0050A3DD..0x0050A3E8 (window total stays 0x42; P1/P3/P4 bytes preserved —
    asserted by run_nc23_matrix.py)."""
    assert len(replacement_bytes) == NC23_SPAN_LEN
    buf = bytearray(CLEAN_WINDOW)
    off = NC23_SPAN_VA - WIN_VA
    assert buf[off:off + NC23_SPAN_LEN] == NC23_SPAN_ORIGINAL
    buf[off:off + NC23_SPAN_LEN] = replacement_bytes
    return bytes(buf)


# ---------------------------------------------------------------- minimal x86-32 decoder
# Opcode coverage: exactly the forms present in the window + mutants (documented in
# INPUT_IDENTITIES.md §6). reg index: 0=eax 1=ecx 2=edx 3=ebx 4=esp 5=ebp 6=esi 7=edi
# NC1: every branch that consumes a memory ModRM operand rejects mod != 0b11 with
# rm == 0b100 (SIB) BEFORE any displacement/length computation — fail-closed.
# NC2: the 0x84 branch additionally rejects EVERY memory TEST form (mod != 0b11).
# NC3-B: the 0x8D register form (mod=11) is invalid and is rejected explicitly.
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


def _reject_sib(mod, rm):
    """NC1 guard (PRESERVED): a memory ModRM form with rm == 0b100 has a SIB byte the
    old length logic omitted; reject it before any displacement/length computation.
    Full SIB decoding is NOT implemented (fail-closed rejection is the bounded correction)."""
    if mod != 0b11 and rm == 0b100:
        raise ValueError(f"unsupported SIB form (mod={mod:02b} rm=100) — FAIL CLOSED")


def decode(buf, base_va):
    """Boundary-safe linear decode of the whole buffer. Returns {va: Insn}.

    Raises ValueError if any byte is outside the covered opcode set, an unsupported
    SIB form (mod != 0b11, rm == 0b100 — NC1), an unsupported memory TEST form
    (mod != 0b11 — NC2) or an invalid LEA register form (mod == 0b11 — NC3-B) is
    encountered (fail-closed: an undecodable window FAILS the checker rather than
    skipping bytes; the old length logic never runs for rejected forms)."""
    out = {}
    i, va = 0, base_va
    while i < len(buf):
        start = i
        op = buf[i]
        writes_edi = False
        if op == 0x8B or op == 0x89 or op == 0x8D:          # mov r32,r/m32 | mov r/m32,r32 | lea
            mod, reg, rm = _modrm(buf, i + 1)
            _reject_sib(mod, rm)                            # NC1 guard — BEFORE any disp/length computation
            if op == 0x8D and mod == 0b11:                  # NC3-B: LEA register form is INVALID — reject
                raise ValueError("unsupported LEA register form (mod=11) — FAIL CLOSED")
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
            else:                                            # lea (memory forms only — mod=11 rejected above)
                writes_edi = (reg == 7)
                op_str = f"{REG[reg]}, dword ptr [{REG[rm]} + 0x{memoff:x}]" if mod != 0b00 or rm != 0b101 \
                    else f"{REG[reg]}, [0x{memoff:08x}]"
                mn = "lea"
        elif op == 0x84:                                     # test r/m8, r8 — REGISTER FORMS ONLY
            mod, reg, rm = _modrm(buf, i + 1)
            _reject_sib(mod, rm)                            # NC1 guard — BEFORE any disp/length computation
            if mod != 0b11:                                 # NC2: EVERY memory TEST form rejected fail-closed
                raise ValueError(f"unsupported memory TEST form (mod={mod:02b}) — FAIL CLOSED")
            reg8 = ["al", "cl", "dl", "bl", "ah", "ch", "dh", "bh"]
            size = 2
            op_str = f"{reg8[rm]}, {reg8[reg]}"
            mn = "test"
        elif op == 0x74 or op == 0xEB:                       # je rel8 / jmp rel8
            rel = buf[i + 1] if buf[i + 1] < 0x80 else buf[i + 1] - 0x100
            size, op_str, mn = 2, f"0x{va + 2 + rel:08x}", ("je" if op == 0x74 else "jmp")
        elif op == 0x83:                                     # grp1 r/m32, imm8 (sign-extended)
            mod, reg, rm = _modrm(buf, i + 1)
            _reject_sib(mod, rm)                            # NC1 guard — BEFORE any disp/length computation
            if mod == 0b11:
                imm = buf[i + 2] if buf[i + 2] < 0x80 else buf[i + 2] - 0x100
                size, op_str = 3, f"{REG[rm]}, {imm & 0xFFFFFFFF:#x}"
                writes_edi = (rm == 7)
            elif mod == 0b01:
                # P3_TOOLING_CLEANUP (kept from sibfixed): imm8 is at opcode+3 (after the
                # disp8 at opcode+2); the pre-sibfixed code printed the disp byte as the
                # immediate. LENGTH unchanged (4).
                imm = buf[i + 3] if buf[i + 3] < 0x80 else buf[i + 3] - 0x100
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
        elif op == 0xFF:                                     # grp5; ONLY /2 (call r/m32) with mod=11
            mod, reg, rm = _modrm(buf, i + 1)
            _reject_sib(mod, rm)                            # NC1 guard — BEFORE any disp/length computation
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


# ---------------------------------------------------------------- corrected checker
def ctrl4_exact_endpoint(window_bytes, base_va=WIN_VA):
    """Return (ok, detail). PASS iff P1..P4 hold simultaneously. (Unchanged predicate;
    the NC1 SIB guard plus the NC2 memory-TEST rejection and the NC3-B LEA
    register-form rejection make the decoder fail-closed for those unsupported
    forms so a hidden EDI write can no longer be boundary-shifted out of P2's
    sight, and invalid LEA register forms yield a controlled (False, diagnostic)
    instead of a TypeError.)"""
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
