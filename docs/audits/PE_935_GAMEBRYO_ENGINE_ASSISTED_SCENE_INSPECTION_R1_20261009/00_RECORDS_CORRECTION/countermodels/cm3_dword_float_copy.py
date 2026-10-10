#!/usr/bin/env python3
# CM-3 — DWORD-copy-carries-float-bits countermodel
# Run: PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009, Work Package A.
#
# LABEL: LOGICAL_COUNTERMODEL_REPRODUCTION — NOT actual execution of FUN_006C2E00.
# NO callback/helper body was opened. Independently written short Python logic
# demonstration reproducing the logical countermodel supplied in
# C:\Users\User\Documents\ChatGPT\PE\PE_TEMPLATE_FINAL_CONSUMER_DESKTOP_POST_AUDIT_F99FEBE_20261009\CLAIM_SUFFICIENCY_COUNTERMODELS.json
# (group "dword_float_copy"; attribution to Desktop preserved). Expected values
# below are the Desktop-supplied constants.
#
# Modeled shape: a generic two-DWORD copy loop (integer-width moves, like the
# fast-path pair stores [cursor]<-[result] / [cursor+4]<-[result+4]) transports
# IEEE-754 float BITS bit-identically with NO floating-point operation anywhere in
# the copy mechanism. Absence of FPU/SSE opcodes therefore does not exclude float
# transport; it also does not prove floats are present in the original container.

import json
import struct

# --- Desktop-supplied expected constants (CLAIM_SUFFICIENCY_COUNTERMODELS.json) ---
EXP_CASES = [
    {"source_float": 1234.5, "dword": "0x449a5000"},
    {"source_float": -42.25, "dword": "0xc2290000"},
]


def dword_copy_as_integer(bits_uint32):
    """Models the generic DWORD move: an INTEGER-width transfer.

    The value is carried as an opaque 32-bit integer; no floating-point
    arithmetic and no float type participates in the copy itself.
    """
    copied_uint32 = bits_uint32          # pure integer assignment == dword move
    return copied_uint32


def main():
    results, all_ok = [], True
    for exp in EXP_CASES:
        src = exp["source_float"]
        packed = struct.pack("<f", src)                  # float -> 4 bytes (bit image)
        bits = struct.unpack("<I", packed)[0]            # the same bits as a uint32
        copied = dword_copy_as_integer(bits)             # the generic DWORD copy
        copied_packed = struct.pack("<I", copied)        # bytes survive unchanged
        copied_float = struct.unpack("<f", copied_packed)[0]
        bit_identical = (packed == copied_packed)
        dword_hex = "0x%08x" % bits
        ok = (dword_hex == exp["dword"] and copied_float == src and bit_identical)
        all_ok = all_ok and ok
        results.append({
            "source_float": src,
            "dword": dword_hex,
            "copied_float": copied_float,
            "bit_identical": bit_identical,
            "float_ops_in_copy_mechanism": 0,
            "matches_desktop_expected": ok,
        })
    out = {
        "countermodel_id": "CM-3_DWORD_FLOAT_COPY",
        "label": "LOGICAL_COUNTERMODEL_REPRODUCTION - NOT actual execution of FUN_006C2E00; NO callback/helper body opened",
        "source": "Desktop CLAIM_SUFFICIENCY_COUNTERMODELS.json group 'dword_float_copy' (attribution preserved)",
        "cases": results,
        "ALL_CASES_REPRODUCED": all_ok,
        "interpretation": ("a two-DWORD integer copy carries float bits bit-identically "
                           "without any FPU/SSE operation; opcode-family absence cannot "
                           "exclude float transport - and does not prove it either"),
    }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
