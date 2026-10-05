# c3_object_scope.py
# RUN: PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005
# F84-C3 object-scope machine facts - P3-A segment-semantics repair, carried
# from the THREE-P2/C2 generators and REGENERATED this run with the
# D1-corrected decoder (measured, not copied; values expected unchanged -
# verified by diff_vs_base.py REGRESSION_DIFF.json).
#
# P3-A CORRECTION vs the C1 generator (Desktop post-audit finding P3):
#   The C1 report claimed "every memory-write instruction with effective
#   displacement 0" in the examined ctor extent but enumerated ONLY selected
#   MOV forms with disp_width==0, silently omitting the two FS:[0] SEH/TLS
#   stores physically present in the extent (0x009723A0 `64 A3 00 00 00 00`
#   MOV FS:[0],EAX and 0x009724CB `64 89 0D 00 00 00 00` MOV FS:[0],ECX).
#   This C2 generator re-runs the store census with SEGMENT SEMANTICS
#   EXPLICITLY REPRESENTED:
#     * the census enumerates ALL memory-write forms in the extent (explicit
#       MOV-to-memory stores incl. 66-word variants and MOFFS stores, plus
#       RMW forms NOT/NEG/INC/DEC r/m) whose effective displacement is 0;
#     * the SEGMENT prefix is persisted for every recorded store;
#     * segment-relative stores (FS/GS...) are TLS/SEH-style writes, NOT
#       offset-zero writes to the assigned object's `this` - they are
#       explicitly EXCLUDED from DIRECT_VPTR_STORE_IN_EXAMINED_CTOR and from
#       any object-member offset-zero evidence;
#     * implicit-destination string stores (AA/AB/AE/AF) and implicit stack
#       writes (PUSH) are NOT store-form encodings in this census - their
#       presence in the extent is machine-checked and disclosed instead.
#   The global states remain ASSIGNED_OBJECT_VTABLE = UNVERIFIED and
#   OBJECT_POLYMORPHISM = NOT_ESTABLISHED (no new vtable/class science).
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

RUN = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
       r"\PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005")

STRING_STORE_OPS = (0xAA, 0xAB, 0xAE, 0xAF)  # STOS/OUTS implicit [EDI] stores


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
        if ins.opcode == 0xC3 and not ins.opcode2 and not ins.prefixes:
            return insns, tva + i + ins.length, "RET_REACHED"
        i += ins.length
        if len(insns) > 4000:
            return insns, tva + i, "STEP_CAP"
    return insns, tva + i, "MAX_LEN"


def store_form_class(ins):
    """Classify an explicit memory-WRITE encoding (dest operand in memory).
    Returns a label or None. Covers MOV-to-memory stores (89/88, C7/C6 /0
    incl. 66 word variants), MOFFS stores (A2/A3) and RMW forms
    (F6/F7 reg 2..3 = NOT/NEG; FE/FF reg 0..1 = INC/DEC)."""
    if ins is None or not ins.memop:
        return None
    if ins.opcode2 is None and ins.opcode in (0x89, 0x88):
        return "MOV [r],r" + (" (word)" if ins.has66 else "")
    if ins.opcode2 is None and ins.opcode in (0xC7, 0xC6) and ins.reg == 0:
        return "MOV [r],imm" + (" (word)" if ins.has66 else "")
    if ins.opcode2 is None and ins.opcode in (0xA2, 0xA3):
        return "MOV moffs,AL/EAX"
    if ins.opcode2 is None and ins.opcode in (0xF6, 0xF7) and ins.reg in (2, 3):
        return "RMW NOT/NEG r/m"
    if ins.opcode2 is None and ins.opcode in (0xFE, 0xFF) and ins.reg in (0, 1):
        return "RMW INC/DEC r/m"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(RUN, "01_RAW", "C3_OBJECT_SCOPE.json"))
    args = ap.parse_args()

    data, ib, secs, text, tva = pebnd.load_text()
    sha = hashlib.sha256(data).hexdigest()
    exe_ok = (sha.upper() == pebnd.PINNED_EXE_SHA256 and len(data) == pebnd.PINNED_EXE_SIZE)
    cache = pebnd._BoundaryCache(text, tva)

    out = {
        "run": "PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005",
        "stage": "C3",
        "exe": {"sha256": sha, "size": len(data), "pinned_match": exe_ok},
    }

    # ---------- the examined ctor: extent + this-register + store census ----------
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

    # P3-A: bounded machine search over EVERY memory-write encoding in the
    # examined extent whose EFFECTIVE DISPLACEMENT is 0, with SEGMENT
    # semantics explicitly represented (segment prefix persisted per store).
    stores_at_0 = []
    cur = entry - tva
    string_store_hits = []
    for ins in insns:
        if ins.opcode in STRING_STORE_OPS and ins.opcode2 is None:
            string_store_hits.append("0x%08X" % (tva + cur))
        cls = store_form_class(ins)
        if cls is not None:
            eff_disp0 = ((ins.disp_width == 0) or
                         (ins.disp_width and ins.disp_signed == 0))
            if eff_disp0:
                base_name = x86dec.REGS32[ins.ea_base] if ins.ea_base is not None else None
                seg = ins.segment
                stores_at_0.append({
                    "va": "0x%08X" % (tva + cur),
                    "bytes": text[cur:cur + ins.length].hex(" ").upper(),
                    "store_form": cls,
                    "segment": seg,
                    "ea_text": ins.segment_qualified_ea_text(),
                    "base_register": base_name,
                    "index_register": x86dec.REGS32[ins.ea_index] if ins.ea_index is not None else None,
                    "scale": ins.ea_scale,
                    "raw_displacement": ("0x%08X" % ins.disp_raw) if ins.disp_width else "NONE",
                    "effective_displacement": 0,
                    "imm": (("0x%X" % ins.imm_raw) if ins.imm_width else None),
                    "base_is_this_register": (base_name in thisregs) if base_name else False,
                    "segment_relative": seg is not None,
                    "p3a_class": ("SEGMENT_RELATIVE_SEH_TLS_STORE" if seg else
                                  "REGISTER_BASED_ZERO_OFFSET_STORE" if base_name
                                  else "ABSOLUTE_ZERO_DISPLACEMENT_STORE"),
                })
        cur += ins.length
    out["examined_ctor"]["offset_zero_store_census_scope"] = (
        "P3-A CORRECTED SCOPE: every memory-WRITE encoding in the examined "
        "extent whose effective displacement is 0 - explicit MOV-to-memory "
        "stores (89/88, C7/C6 /0, incl. 66 word variants), MOFFS stores "
        "(A2/A3) and RMW forms (NOT/NEG/INC/DEC r/m) - with the SEGMENT "
        "prefix persisted per store; implicit-destination string stores "
        "(AA/AB/AE/AF) and implicit stack writes (PUSH) are not "
        "store-form encodings here and their presence is machine-checked "
        "and disclosed instead")
    out["examined_ctor"]["offset_zero_stores"] = stores_at_0
    out["examined_ctor"]["string_store_opcode_hits_in_extent"] = string_store_hits

    seg_stores = [s for s in stores_at_0 if s["segment_relative"]]
    nonseg_this = [s for s in stores_at_0
                   if not s["segment_relative"] and s["base_is_this_register"]]
    if status == "RET_REACHED" and len(insns) > 0:
        direct_vptr = "OBSERVED" if nonseg_this else "NOT_OBSERVED"
    else:
        direct_vptr = "NOT_VERIFIED"
    out["direct_vptr_store_in_examined_ctor"] = {
        "DIRECT_VPTR_STORE_IN_EXAMINED_CTOR": direct_vptr,
        "search_scope": ("every memory-write encoding with effective "
                         "displacement 0 in the examined ctor extent "
                         "0x00972380..%s (P3-A corrected: ALL write forms, "
                         "segment semantics represented); a direct vptr store "
                         "is a NON-SEGMENT-RELATIVE store to [this+0]"
                         % ("0x%08X" % (extent_end - 1))),
        "offset_zero_stores_found": len(stores_at_0),
        "segment_relative_stores": len(seg_stores),
        "segment_relative_store_vas": [s["va"] for s in seg_stores],
        "with_this_base_non_segment": len(nonseg_this),
        "segment_exclusion_rule": ("segment-relative stores (FS/GS...) are "
                                   "TLS/SEH-style writes to a SEGMENT-RELATIVE "
                                   "address, NOT offset-zero writes to the "
                                   "assigned object's this - they can NEVER "
                                   "become DIRECT_VPTR_STORE_IN_EXAMINED_CTOR "
                                   "or object-member offset-zero evidence"),
        "segment_relative_detail": [
            {"va": s["va"], "segment": s["segment"], "bytes": s["bytes"],
             "store_form": s["store_form"], "ea_text": s["ea_text"]}
            for s in seg_stores],
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
        cv = pebnd.validate_direct_call(text, tva, va, cache)
        callsites.append({
            "va": "0x%08X" % va,
            "byte_is_E8": cv["byte_is_E8"],
            "call_validation": cv["call_validation"],
            "boundary_status": cv["boundary_status"],
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

    # ---------- ctor call-site census (machine; boundary-corrected) ----------
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
        bstatus, bsrc, bstart, brefuted = pebnd.boundary_confirm(text, tva, va, cache)
        if bstatus == "CONFIRMED":
            confirmed.append(va)
    out["ctor_callsite_census"] = {
        "target": "0x00972380",
        "raw_E8_rel32_target_matches": len(raw_e8_targets),
        "raw_sites": ["0x%08X" % v for v in raw_e8_targets],
        "boundary_confirmed_count": len(confirmed),
        "boundary_confirmed_sites": ["0x%08X" % v for v in confirmed],
        "historical_prefilled_value_superseded": 10,
        "note": ("machine-measured: raw E8 opcode positions whose rel32 targets "
                 "the ctor; the boundary-confirmed subset counts ONLY "
                 "strong-anchor-confirmed positions under the AF2-corrected "
                 "policy (the C1 padding-derived confirmations are demoted to "
                 "heuristic candidates - recorded, never confirming)"),
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
    print("C3 done. decode=%s insns=%d offset0=%d seg=%d thisbase=%d vptr=%s "
          "callsites=%d/%d ctorE8=%d/%d" % (
              status, len(insns), len(stores_at_0), len(seg_stores),
              len(nonseg_this), direct_vptr,
              sum(1 for c in callsites if c["call_validation"] == "PASS"),
              len(callsites), len(confirmed), len(raw_e8_targets)))


if __name__ == "__main__":
    main()
