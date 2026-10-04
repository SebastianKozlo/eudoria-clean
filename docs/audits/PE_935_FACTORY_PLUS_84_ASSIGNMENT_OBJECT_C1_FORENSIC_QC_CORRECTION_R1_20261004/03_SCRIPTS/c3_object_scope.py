# c3_object_scope.py
# RUN: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004
# F84-C3 VTABLE/POLYMORPHISM CLAIM-SCOPE REPAIR + object-scope machine facts.
#
#   * Supersedes the unsupported global claims "ASSIGNED_OBJECT_VTABLE = NONE"
#     and "OBJECT_IS_NON_POLYMORPHIC = CONFIRMED": the historical generator
#     stored vtable_store_found=False as a PREFILLED value; that is not a
#     measurement. This script performs a BOUNDED MACHINE SEARCH over the
#     EXAMINED ctor extent only (FUN_00972380): sequential decode from the
#     known entry, every dword/word/byte store whose effective displacement
#     is 0 recorded, flagged when its base register is the machine-checked
#     this-register. Direct observation only:
#       DIRECT_VPTR_STORE_IN_EXAMINED_CTOR = NOT_OBSERVED | OBSERVED | NOT_VERIFIED
#     Global fields remain ASSIGNED_OBJECT_VTABLE=UNVERIFIED and
#     OBJECT_POLYMORPHISM=NOT_ESTABLISHED. No helper/base-constructor bodies
#     are entered to force closure.
#   * KNOWN_EXAMINED_CALLSITES_ARE_DIRECT: the examined callsites of the
#     object's methods are machine-checked for direct E8 (rel32) form.
#   * Machine-measured ctor call-site census (supersedes the prefilled
#     "ctor_callsites_count: 10").
#   * FUN_0070BF40 hygiene: literal transcription of its examined operation
#     ONLY (no semantic-role promotion).
#   * P3: 0xA4 = 164 (the ASSIGNED OBJECT allocation); 0x118 = 280 (the
#     FACTORY allocation) - both re-measured from the same-VA pins.
#
# Output: 01_RAW/C3_OBJECT_SCOPE.json (--out override). READ-ONLY vs EXE.

import argparse
import hashlib
import json
import os
import struct
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pebnd  # noqa: E402
import x86dec  # noqa: E402

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004"


def entry_this_regs(text, tva, entry_va, win=0x40):
    regs = set()
    i = entry_va - tva
    end = i + win
    steps = 0
    while i < end and i < len(text) and steps < 64:
        ins = x86dec.decode(text, i)
        if ins is None:
            break
        if (not ins.prefixes and ins.opcode == 0x8B and ins.mod == 3
                and ins.rm == 1):
            regs.add(x86dec.REGS32[ins.reg])
        i += ins.length
        steps += 1
    return regs


def decode_extent(text, tva, entry, max_len=0x400):
    """Sequential decode from entry; returns (insns, end_va, status)."""
    insns = []
    i = entry - tva
    end = i + max_len
    while i < end:
        if text[i] == 0xCC:
            return insns, tva + i, "CC_PADDING"
        ins = x86dec.decode(text, i)
        if ins is None:
            return insns, tva + i, "DECODE_FAIL"
        insns.append(ins)
        if ins.opcode == 0xC3 and not ins.opcode2:
            return insns, tva + i + ins.length, "RET_REACHED"
        if (ins.opcode == 0xC2 and not ins.opcode2):
            # RET imm16 ends the fall-through path; continue linearly
            pass
        i += ins.length
        if len(insns) > 4000:
            return insns, tva + i, "STEP_CAP"
    return insns, tva + i, "MAX_LEN"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(RUN, "01_RAW", "C3_OBJECT_SCOPE.json"))
    args = ap.parse_args()

    data, ib, secs, text, tva = pebnd.load_text()
    sha = hashlib.sha256(data).hexdigest()
    exe_ok = (sha.upper() == pebnd.PINNED_EXE_SHA256 and len(data) == pebnd.PINNED_EXE_SIZE)

    out = {
        "run": "PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004",
        "stage": "C3",
        "exe": {"sha256": sha, "size": len(data), "pinned_match": exe_ok},
    }

    # ---------- the examined ctor: extent + this-register + offset-0 stores ----------
    entry = 0x00972380
    thisregs = entry_this_regs(text, tva, entry)
    insns, extent_end, status = decode_extent(text, tva, entry)
    out["examined_ctor"] = {
        "entry": "0x00972380",
        "known_label": pebnd.KNOWN_ENTRIES[entry],
        "decode_status": status,
        "insn_count": len(insns),
        "extent_end": "0x%08X" % extent_end,
        "extent_end_note": ("the extent end = the first RET (C3) reached by the "
                            "sequential decode; first CC padding after it is the "
                            "function boundary"),
        "this_registers_from_entry_mov_ecx": sorted(thisregs),
    }
    # find the first CC pair after the extent end (padding marker)
    i = extent_end - tva
    while i < len(text) - 1 and not (text[i] == 0xCC and text[i + 1] == 0xCC):
        if text[i] == 0xCC and text[i + 1] == 0xCC:
            break
        i += 1
    out["examined_ctor"]["first_cc_pair_after"] = "0x%08X" % (tva + i)

    # bounded machine search: every memory-write instruction with effective
    # displacement 0 in the examined extent, with base-register identity
    stores_at_0 = []
    cur = entry - tva
    for ins in insns:
        is_store = (not ins.opcode2 and ins.opcode in (0x89, 0x88, 0xC7, 0xC6)) \
                   or (ins.prefixes and ins.prefixes[0] == 0x66 and ins.opcode in (0x89, 0xC7))
        if is_store and ins.memop and ins.disp_signed == 0 and ins.disp_width == 0:
            base_name = x86dec.REGS32[ins.ea_base] if ins.ea_base is not None else None
            stores_at_0.append({
                "va": "0x%08X" % (tva + cur),
                "bytes": text[cur:cur + ins.length].hex(" ").upper(),
                "mnemonic_class": ("MOV [r],r" if ins.opcode in (0x89, 0x88) else
                                   "MOV [r],imm" if ins.opcode in (0xC7, 0xC6) else "other"),
                "base_register": base_name,
                "index_register": x86dec.REGS32[ins.ea_index] if ins.ea_index is not None else None,
                "scale": ins.ea_scale,
                "imm": (("0x%X" % ins.imm_raw) if ins.imm_width else None),
                "base_is_this_register": base_name in thisregs if base_name else False,
            })
        cur += ins.length
    out["examined_ctor"]["offset_zero_stores"] = stores_at_0
    vptr_hits = [s for s in stores_at_0 if s["base_is_this_register"]]
    if status == "RET_REACHED" and len(insns) > 0:
        direct_vptr = "OBSERVED" if vptr_hits else "NOT_OBSERVED"
    else:
        direct_vptr = "NOT_VERIFIED"
    out["direct_vptr_store_in_examined_ctor"] = {
        "DIRECT_VPTR_STORE_IN_EXAMINED_CTOR": direct_vptr,
        "search_scope": ("every memory-write instruction with effective "
                         "displacement 0 in the examined ctor extent "
                         "0x00972380..%s; a direct vptr store is a store to "
                         "[this+0]" % ("0x%08X" % (extent_end - 1))),
        "offset_zero_stores_found": len(stores_at_0),
        "with_this_base": len(vptr_hits),
        "note": ("NOT_OBSERVED is a direct observation over the EXAMINED ctor "
                 "extent only; the object may delegate vptr installation to a "
                 "base/helper constructor (not entered here), so the global "
                 "fields stay ASSIGNED_OBJECT_VTABLE=UNVERIFIED and "
                 "OBJECT_POLYMORPHISM=NOT_ESTABLISHED"),
    }

    # ---------- KNOWN_EXAMINED_CALLSITES_ARE_DIRECT ----------
    callsites = []
    for va in (0x0070DD75, 0x0070DD84, 0x0070C742):
        off = va - tva
        cv = pebnd.validate_direct_call(text, tva, va)
        callsites.append({
            "va": "0x%08X" % va,
            "byte_is_E8": cv["byte_is_E8"],
            "call_validation": cv["call_validation"],
            "target": ("0x%08X" % cv["target"]) if cv["target"] else None,
            "indirect_FF2": (text[off] == 0xFF and off + 1 < len(text)
                             and ((text[off + 1] >> 3) & 7) == 2),
        })
    out["known_examined_callsites_direct"] = {
        "KNOWN_EXAMINED_CALLSITES_ARE_DIRECT": ("YES" if all(
            c["call_validation"] == "PASS" for c in callsites) else "NO"),
        "callsites": callsites,
        "note": ("measured over the EXAMINED callsites only (the consumer's "
                 "two stream-method calls + the setter's post-attach call); "
                 "NO claim about 'all methods' of the object"),
    }

    # ---------- ctor call-site census (machine; supersedes prefilled 10) ----------
    raw_e8_targets = []
    n = len(text)
    target = 0x00972380
    i = 0
    while i < n - 4:
        if text[i] == 0xE8:
            rel = struct.unpack_from("<i", text, i + 1)[0]
            if tva + i + 5 + rel == target:
                raw_e8_targets.append(tva + i)
        i += 1
    confirmed = []
    for va in raw_e8_targets:
        ok, src, _ = pebnd.boundary_confirm(text, tva, va)
        if ok:
            confirmed.append(va)
    out["ctor_callsite_census"] = {
        "target": "0x00972380",
        "raw_E8_rel32_target_matches": len(raw_e8_targets),
        "raw_sites": ["0x%08X" % v for v in raw_e8_targets],
        "boundary_confirmed_count": len(confirmed),
        "boundary_confirmed_sites": ["0x%08X" % v for v in confirmed],
        "historical_prefilled_value_superseded": 10,
        "note": ("machine-measured: raw E8 opcode positions whose rel32 targets "
                 "the ctor, with the boundary-confirmed subset counted "
                 "separately (the historical 'ctor_callsites_count: 10' was a "
                 "prefilled value)"),
    }

    # ---------- FUN_0070BF40 hygiene: literal transcription only ----------
    bf40 = []
    i = 0x0070BF40 - tva
    steps = 0
    while steps < 12:
        if text[i] == 0xCC:
            break
        ins = x86dec.decode(text, i)
        if ins is None:
            bf40.append({"va": "0x%08X" % (tva + i), "decode": "FAIL"})
            break
        bf40.append({"va": "0x%08X" % (tva + i),
                     "bytes": text[i:i + ins.length].hex(" ").upper(),
                     "opcode": "0x%02X" % ins.opcode,
                     "memop": ins.memop and ins.ea_text() or None,
                     "imm": (("0x%X" % ins.imm_raw) if ins.imm_width else None)})
        i += ins.length
        steps += 1
    out["fun_0070bf40_literal_transcription"] = {
        "instructions": bf40,
        "literal_operation": ("loads [ECX+4]; ANDs with the supplied argument; "
                              "normalizes the result to a boolean-like return "
                              "(measured transcription; NO semantic-role "
                              "promotion beyond the literal examined operation)"),
        "function_ledger_hygiene": {
            "HISTORICAL_FUNCTION_BUDGET_COUNT": "8_DECLARED_AND_MECHANICALLY_REPRODUCED",
            "PRE_ANALYSIS_CHRONOLOGY_INDEPENDENTLY_ESTABLISHED": "NO",
            "ACTUAL_HISTORICAL_BUDGET_OVERRUN": "NOT_ESTABLISHED",
            "note": ("the existing historical ledger mechanically reproduces 8 "
                     "counted + 10 excluded rows; this correction does NOT "
                     "claim a historical budget overrun"),
        },
    }

    # ---------- P3: allocation-size facts from the same-VA pins ----------
    def imm_at(va, expect_bytes):
        off = va - tva
        nb = len(expect_bytes.split())
        b = text[off:off + nb]
        if b.hex(" ").upper() != expect_bytes:
            return None
        ins = x86dec.decode(text, off)
        return ins.imm_raw if ins and ins.imm_width else None
    a4 = imm_at(0x0070C6F9, "68 A4 00 00 00")
    x118 = imm_at(0x0073E2CC, "68 18 01 00 00")
    out["allocation_size_facts"] = {
        "ASSIGNED_OBJECT_SIZE_HEX": ("0x%X" % a4) if a4 else None,
        "ASSIGNED_OBJECT_SIZE_DECIMAL": a4,
        "P3_note": ("0xA4 = 164 bytes (the ASSIGNED OBJECT allocation at the "
                    "setter); the historical '0xA4 bytes (280)' decimal was "
                    "wrong - 280 = 0x118 is the FACTORY allocation size"),
        "FACTORY_SIZE_HEX": ("0x%X" % x118) if x118 else None,
        "FACTORY_SIZE_DECIMAL": x118,
    }

    # preserved structural facts re-measured (ctor tail stores, from the same-VA
    # pins in C1; recorded here for the object-scope summary)
    out["preserved_structural_facts"] = {
        "ASSIGNED_OBJECT_CONSTRUCTOR": "FUN_00972380",
        "measured_cursor_plus_0x3C": "LEA EDI,[ESI+0x3C] @0x00972427; size store "
                                     "[EDI+4]=0x80 @0x00972443; buffer new(0x80) "
                                     "CALL @0x0097244A -> 0x0095D3BE; buffer "
                                     "store [EDI]=EAX @0x00972452; flag "
                                     "[EDI+0x11]=1 @0x00972454",
        "measured_tail_stores": "+0x88<-dword @0x00972499; +0x8C<-0x80 imm32 "
                                "@0x0097249F; +0x90 @0x009724A9; +0x94 "
                                "@0x009724AF; +0x98<-0x80 imm32 @0x009724B5; "
                                "+0x9C @0x009724BF",
        "constructor_returns_this": "MOV EAX,ESI @0x009724C5; RET @0x009724D9",
        "ASSIGNED_OBJECT_STRUCTURAL_IDENTITY": "CONFIRMED_WITHIN_EXAMINED_LAYOUT",
        "FINAL_SEMANTIC_ROLE_RECORD_STREAM": "STRONGLY_SUPPORTED",
        "terminology_note": ("structural identity confirmed WITHIN THE EXAMINED "
                             "LAYOUT (0xA4 allocation + FUN_00972380 construction "
                             "+ examined internal stores + embedded cursor/buffer "
                             "+ known direct callsites); 'record-stream' is "
                             "semantic NAMING, STRONGLY_SUPPORTED not CONFIRMED "
                             "from structural observations alone"),
    }

    with open(args.out, "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("C3 done. decode=%s insns=%d offset0=%d thisbase=%d vptr=%s callsites=%d "
          "ctorE8=%d/%d" % (status, len(insns), len(stores_at_0), len(vptr_hits),
                            direct_vptr, len(callsites),
                            len(confirmed), len(raw_e8_targets)))


if __name__ == "__main__":
    main()
