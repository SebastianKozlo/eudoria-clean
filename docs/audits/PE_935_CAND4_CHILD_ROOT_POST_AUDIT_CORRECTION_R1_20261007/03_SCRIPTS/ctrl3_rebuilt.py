"""ctrl3_rebuilt.py — REBUILT CTRL_3 (wrong-manager-field predicate) for
PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007 (contract §2 of the
correction).

SUPERSEDED implementation: SOURCE_PACKAGE 03_SCRIPTS/qc_controls.py lines 117-143
(ctrl3_provenance) read REAL EXE bytes at TWO entry VAs (clean: FUN_006C66D0 — an
already-budgeted opened body; mutated: FUN_006C0EE0 — an UNDECLARED real foreign body,
8 bytes, interpreted as the manager+0x120 getter). The mutated-case read was a NEW
real-body probe outside the source run's 6/6 declaration and is now HISTORICALLY
ACCOUNTED as the proven 7th real-body opening (FUNCTION_BODY_ACCOUNTING.csv row 7;
MINIMUM_NEW_FUNCTION_BODIES_OPENED >= 7; ORIGINAL_FUNCTION_BODY_BUDGET_COMPLIANCE = FAIL).

THIS REBUILD (per correction contract §2): the same predicate, run over SYNTHETIC
FIXTURES / PERSISTED PRIOR PINS ONLY — byte constants pinned to published records;
ZERO EXE access; ZERO new real-body discovery. One code path for clean and mutated.

Predicate (unchanged semantics): the provenance predicate binds the GETTER's field
offset to the PRODUCER's written field offset (0x68). Correct bytes of a foreign
manager field must NOT qualify as provenance of THIS getter.

Fixtures (INPUT_IDENTITIES.md §5):
  CLEAN_GETTER_FIXTURE     = 8B 41 68 C3 CC CC CC CC
      (persisted prior pin: SOURCE_PACKAGE 01_RAW/FUN_006C66D0_GETTER_FULL.txt RAW BYTES,
       first 8 bytes of the 96-byte window @0x006C66D0 — the already-budgeted body #1;
       mov eax,[ecx+0x68]; ret)
  FOREIGN_ACCESSOR_FIXTURE = 8B 81 20 01 00 00 C3 CC
      (persisted recorded constant of the HISTORICAL probe: SOURCE_PACKAGE
       CONTROL_RESULTS.json CTRL_3 mutated_case + Desktop CONTROL_COUNTERCHECKS.json
       foreign_accessor_bytes; mov eax,[ecx+0x120]; ret; int3)

Decoder: minimal in-script ModRM decode of the 8B /r (mov r32, r/m32) form — mod=01 ->
[rm + disp8]; mod=10 -> [rm + disp32]; mod=00 rm=101 -> [disp32]; mod=11 -> register form.
No capstone, no pe_reader, no EXE.

Writes: CONTROL_RESULTS.json (package root) — merged with ctrl4_exact_endpoint.py output
(ctrl3 runs first, writes the file; ctrl4 reads/merges it; see CONTROL_RESULTS.json
generation note in the file itself).
"""
import json
import os

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PRODUCER_WRITTEN_FIELD_OFFSET = 0x68  # measured by the source run (writer store 89 7E 68 @0x006C67E2)

CLEAN_GETTER_FIXTURE = bytes.fromhex("8B 41 68 C3 CC CC CC CC")
FOREIGN_ACCESSOR_FIXTURE = bytes.fromhex("8B 81 20 01 00 00 C3 CC")

REG_NAMES = ["eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi"]


def decode_mov_load(buf):
    """Decode one `8B /r  mov r32, r/m32` instruction from buf.

    Returns (dst_reg_name, operand_str, reads_ecx_offset_or_None, instr_len).
    Raises ValueError on any byte that is not the covered mov-load form.
    """
    if buf[0] != 0x8B:
        raise ValueError(f"opcode {buf[0]:02X} is not the 8B mov r32,r/m32 form")
    modrm = buf[1]
    mod = (modrm >> 6) & 3
    reg = (modrm >> 3) & 7
    rm = modrm & 7
    if mod == 0b01:            # [reg + disp8]
        disp = buf[2]
        operand = f"[{REG_NAMES[rm]} + 0x{disp:x}]"
        reads_ecx_off = disp if rm == 1 else None
        length = 3
    elif mod == 0b10:          # [reg + disp32]
        disp = int.from_bytes(buf[2:6], "little")
        operand = f"[{REG_NAMES[rm]} + 0x{disp:x}]"
        reads_ecx_off = disp if rm == 1 else None
        length = 6
    elif mod == 0b00 and rm == 0b101:   # [disp32] (moffs)
        disp = int.from_bytes(buf[2:6], "little")
        operand = f"[0x{disp:08x}]"
        reads_ecx_off = None
        length = 6
    elif mod == 0b11:          # register, register
        operand = REG_NAMES[rm]
        reads_ecx_off = None
        length = 2
    else:                      # mod=00 with rm != 101: [reg] — not present in the fixtures
        operand = f"[{REG_NAMES[rm]}]"
        reads_ecx_off = None
        length = 2
    return REG_NAMES[reg], operand, reads_ecx_off, length


def ctrl3_provenance(fixture_bytes):
    """ONE code path for clean and mutated. Returns (ok: bool, detail: str).

    PASS iff the accessor reads [ecx + 0x68] — the producer-written field.
    Correct bytes of a foreign field (e.g. [ecx + 0x120]) must FAIL.
    """
    try:
        dst, operand, reads_ecx_off, _ = decode_mov_load(fixture_bytes)
    except (ValueError, IndexError) as exc:
        return False, f"fixture not decodable as a mov-load accessor: {exc}"
    if reads_ecx_off == PRODUCER_WRITTEN_FIELD_OFFSET:
        return True, f"accessor reads {operand} == the producer-written field [ecx+0x{PRODUCER_WRITTEN_FIELD_OFFSET:x}]"
    return False, f"accessor 'mov {dst}, {operand}' does not read [ecx+0x{PRODUCER_WRITTEN_FIELD_OFFSET:x}]"


def run_and_write():
    ok_clean, det_clean = ctrl3_provenance(CLEAN_GETTER_FIXTURE)
    ok_mut, det_mut = ctrl3_provenance(FOREIGN_ACCESSOR_FIXTURE)

    OUT = {
        "CTRL_3_REBUILT": {
            "checker": "ctrl3_provenance (rebuilt; getter field offset == producer-written offset 0x68; ONE code path for clean/mutated)",
            "rebuilt_because": "the source-run implementation (qc_controls.py:117-143) used the REAL foreign EXE accessor FUN_006C0EE0 as the mutated case — an undeclared 8-byte real-body probe (the accounted 7th body opening); the rebuild uses synthetic fixtures / persisted prior pins only, with no new real EXE accessor discovery",
            "exe_accessed": False,
            "fixtures": {
                "clean": {
                    "bytes": "8B 41 68 C3 CC CC CC CC",
                    "provenance": "persisted prior pin: SOURCE_PACKAGE 01_RAW/FUN_006C66D0_GETTER_FULL.txt RAW BYTES (body #1 of the source run, already budgeted); synthetic use: in-memory constant",
                    "input_kind": "PERSISTED_PRIOR_PIN__SYNTHETIC_IN_MEMORY",
                },
                "mutated": {
                    "bytes": "8B 81 20 01 00 00 C3 CC",
                    "provenance": "persisted recorded constant of the HISTORICAL probe (SOURCE_PACKAGE CONTROL_RESULTS.json CTRL_3 mutated_case; Desktop CONTROL_COUNTERCHECKS.json foreign_accessor_bytes); used as a recorded constant — NO new EXE read; the historical probe itself is accounted in FUNCTION_BODY_ACCOUNTING.csv row 7",
                    "input_kind": "PERSISTED_RECORDED_CONSTANT__SYNTHETIC_IN_MEMORY",
                },
            },
            "clean_case": {
                "input_bytes": "8B 41 68 C3 CC CC CC CC",
                "result": "PASS" if ok_clean else "FAIL",
                "expected": "PASS",
                "detail": det_clean,
            },
            "mutated_case": {
                "input_bytes": "8B 81 20 01 00 00 C3 CC",
                "mutation": "the accessor substituted with the recorded bytes of a foreign manager-field accessor ([+0x120] getter of the same class family) — SYNTHETIC/in-memory fixture, not an EXE read",
                "result": "PASS" if ok_mut else "FAIL",
                "expected": "FAIL",
                "detail": det_mut,
                "cause": "correct bytes of a foreign field do not qualify as provenance of THIS getter (+0x68)",
            },
            "verdict": "PASS" if (ok_clean and not ok_mut) else "FAIL",
            "range": "same checker; same accessor instruction shape (8B /r mov r32,[ecx+disp]); clean = the persisted getter pin; mutated = the recorded foreign-accessor constant",
            "ctrl3_synthetic_or_prior_pin_status": "SYNTHETIC_FIXTURES_AND_PERSISTED_PRIOR_PINS_ONLY (no EXE access; no new real accessor discovery; NEW_PCG_FUNCTION_BODIES_ALLOWED = 0 honored)",
        }
    }

    path = os.path.join(PKG, "CONTROL_RESULTS.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(OUT, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(json.dumps(OUT["CTRL_3_REBUILT"], indent=2, ensure_ascii=False))
    print(f"\nwrote {path}")
    return OUT


if __name__ == "__main__":
    run_and_write()
