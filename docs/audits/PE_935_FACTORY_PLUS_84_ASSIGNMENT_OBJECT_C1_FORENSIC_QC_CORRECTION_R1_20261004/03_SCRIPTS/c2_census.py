# c2_census.py
# RUN: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004
# F84-C2 CENSUS REPAIR: freshly recomputed from the pinned EXE. The published
# census counts/classification distribution are SUPERSEDED; nothing is
# target-matched to historical values.
#
# Corrected semantics:
#   * MOD01 disp8 is SIGNED: raw 0x84 == -124 == -0x7C (NEVER +0x84). Such rows
#     are NEGATIVE_DISP8_MINUS_0x7C_CONTROL rows - an encoding-level property
#     (a +132 displacement cannot be encoded as disp8 under ANY decoding), so
#     the control status is interpretation-independent and needs no boundary.
#   * POSITIVE_PLUS_84 requires an actual effective signed displacement +132
#     (MOD10 disp32 == 0x00000084, SIB or non-SIB).
#   * BOUNDARY_CONFIRMED only from a declared trusted source (KNOWN_FUNCTION_ENTRY
#     or CC_PADDING_DELIMITED_START + exact-landing sequential decode). No
#     NOT_AN_INSTRUCTION/IMMEDIATE_DATA inference from failed decodes.
#   * No rejection from register naming: ESP/EBP-based rows get
#     ADDRESS_PROVENANCE=UNRESOLVED and classification UNRESOLVED (unless a
#     separate provenance proof applies). EBP is never rejected by name.
#   * Full EA decode per row: operand_width, base_register, index_register,
#     scale, raw_displacement, signed_displacement, effective_displacement,
#     address_provenance_status.
#
# Declared examined encoding families (enumerated explicitly; the historical
# examined scope, byte-by-byte coverage of every .text position):
#   F1 89 r/m32,r32 mod01/mod10 (+SIB)  | F2 8B r32,r/m32 mod01/mod10 (+SIB)
#   F3 39 r/m32,r32 mod01/mod10 (+SIB)  | F4 8D r32,m mod01/mod10 (+SIB)
#   F5 C7 /0 mod01/mod10 (+SIB)        | F6 88 r/m8,r8 mod01/mod10 (+SIB)
#   F7 C6 /0 mod01/mod10 (+SIB)        | F8 66 89 mod01/mod10 NON-SIB (word)
#   F9 66 C7 /0 mod01/mod10 NON-SIB (word)
# 66-form SIB variants were NOT in the historical examined families and remain
# outside this enumeration (disclosed scope boundary of the closure claim).
#
# EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE = NOT_ESTABLISHED (invariant; even
# full resolution of every corrected-scanner row cannot exclude alias writes,
# helper-mediated writes, bulk/memory-copy writes, other address constructions,
# unexamined encodings or runtime mutation).
#
# Outputs: CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv + 01_RAW/C2_CENSUS.json
# (--csv/--out override for auditor re-runs). READ-ONLY vs the pinned EXE.

import argparse
import csv
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pebnd  # noqa: E402
import x86dec  # noqa: E402

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004"

KNOWN_STORES = {
    0x0070D013: ("INITIALIZATION_NULL",
                 "factory base ctor FUN_0070CF80: MOV [ESI+0x84],EBX, EBX=0 "
                 "(XOR EBX,EBX @0x0070CFBC); executes for every factory class "
                 "construction incl. 20006 (derived ctor FUN_0073B820 CALL "
                 "FUN_0070CF80 @0x0073B87D); physically re-pinned this run"),
    0x0070C71E: ("CONDITIONAL_OBJECT_OR_NULL_ATTACH_STORE",
                 "stream-attach setter FUN_0070C680: MOV [ESI+0x84],EAX, "
                 "EAX = new(0xA4) object constructed by FUN_00972380 (CALL "
                 "@0x0070C715) or 0 on allocation failure (XOR EAX,EAX "
                 "@0x0070C71C); guarded by the entry check CMP "
                 "[ESI+0x84],EDI @0x0070C6BE; physically re-pinned this run"),
}

FACTORY_THIS_FUNCTIONS = (0x0070CF80, 0x0070C680, 0x0073B820)

# The four layout-evidence natural controls (historical window evidence,
# re-verified byte-for-byte this run; provenance basis recorded per row).
LAYOUT_CONTROLS = {
    0x0074955A: ("WINDOW_LAYOUT_EVIDENCE",
                 [b"\x88\x9e\x88\x00\x00\x00", b"\x88\x9e\x89\x00\x00\x00"],
                 "sibling-class ctor: byte stores at the SAME base +0x88/+0x89 "
                 "(MOV BYTE [ESI+0x88],r8 / [ESI+0x89],r8) vs the factory class "
                 "dword slot-array vector at +0x88 (prior canon "
                 "FUN_0070E2F0/FUN_0070C180); class-layout mismatch, "
                 "different object"),
    0x006D4F88: ("WINDOW_VALUE_GRAMMAR_EVIDENCE",
                 [b"\xbe\x04\x00\x00\x00"],
                 "class ctor writing the integer 4 (MOV ESI,4) into +0x84 of "
                 "its base; the factory +0x84 is a pointer member written from "
                 "a ctor'd object pointer or NULL (the two known stores); "
                 "value-grammar mismatch, different object"),
    0x0075138F: ("WINDOW_LAYOUT_EVIDENCE",
                 [b"\x8d\x8e\x88\x00\x00\x00"],
                 "class initializing a helper-object pointer at its +0x88 "
                 "(LEA ECX,[ESI+0x88] + helper CALL) vs the factory dword "
                 "slot-array vector at +0x88 (prior canon); class-layout "
                 "mismatch, different object"),
    0x007196AA: ("WINDOW_INIT_GRAMMAR_EVIDENCE",
                 [b"\x1c\x92\xba\x00", b"\x20\x92\xba\x00", b"\x24\x92\xba\x00"],
                 "static globals 0x00BA921C/0x00BA9220/0x00BA9224 copied into "
                 "+0x84/+0x88/+0x8C of the base; the factory ctor writes +0x84 "
                 "from a zeroed register and builds its +0x88 vector via "
                 "FUN_0070E2F0; different init grammar, different object"),
}

KNOWN_READS = {
    0x0070DD1A: "consumer NULL gate CMP (FUN_0070DCF0)",
    0x0070DD6A: "consumer stream load 1 (FUN_0070DCF0)",
    0x0070DD7E: "consumer stream load 2 (FUN_0070DCF0)",
    0x0070C6BE: "setter entry guard CMP (FUN_0070C680)",
    0x0070BFD0: "stream bridge method load (FUN_0070BFD0)",
}


def scan_raw_rows(text, tva):
    """Byte-by-byte enumeration of the declared families. Every position is
    tested against every family (no skip-ahead: overlapping occurrences are
    all recorded)."""
    n = len(text)
    rows = []
    i = 0
    while i < n:
        b0 = text[i]
        fam = None
        modrm_pos = None
        if b0 == 0x66 and i + 2 < n and text[i + 1] in (0x89, 0xC7):
            op = text[i + 1]
            m = text[i + 2]
            mod = m >> 6
            rm = m & 7
            regf = (m >> 3) & 7
            if mod in (1, 2) and rm != 4:
                if op == 0xC7 and regf != 0:
                    i += 1
                    continue
                dp = i + 3
                if mod == 1:
                    hit = dp < n and text[dp] == 0x84
                else:
                    hit = dp + 4 <= n and text[dp:dp + 4] == b"\x84\x00\x00\x00"
                if hit:
                    fam = "F8_6689_WORD" if op == 0x89 else "F9_66C7_WORD"
                    rows.append((fam, i, mod, rm, regf, dp, 1 if mod == 1 else 4))
        elif b0 in (0x89, 0x8B, 0x39, 0x8D, 0x88, 0xC6, 0xC7):
            if i + 1 < n:
                m = text[i + 1]
                mod = m >> 6
                rm = m & 7
                regf = (m >> 3) & 7
                if mod in (1, 2):
                    if b0 in (0xC6, 0xC7) and regf != 0:
                        i += 1
                        continue
                    dp = i + 3 if rm == 4 else i + 2
                    if mod == 1:
                        hit = dp < n and text[dp] == 0x84
                    else:
                        hit = dp + 4 <= n and text[dp:dp + 4] == b"\x84\x00\x00\x00"
                    if hit:
                        base = {0x89: "F1_89", 0x8B: "F2_8B", 0x39: "F3_39",
                                0x8D: "F4_8D", 0x88: "F6_88", 0xC6: "F7_C6",
                                0xC7: "F5_C7"}[b0]
                        fam = base + ("_MOD01" if mod == 1 else "_MOD10") + \
                              ("_SIB" if rm == 4 else "")
                        rows.append((fam, i, mod, rm, regf, dp, 1 if mod == 1 else 4))
        i += 1
    return rows


def lea_link_store(text, tva, ins_va, ins, max_span=24, max_ins=8):
    """Bounded LEA-linkage: a store through the LEA destination register
    (MOV [dst],src mod=00, rm=dst, non-SIB) within max_span bytes, stepping
    with the decoder. Returns the linked-store offset or None."""
    dst = ins.reg
    j = (ins_va - tva) + ins.length
    end = j + max_span
    steps = 0
    while j < end and steps < max_ins:
        nx = x86dec.decode(text, j)
        if nx is None or nx.length <= 0:
            return None
        if (not nx.prefixes and nx.opcode == 0x89 and nx.mod == 0
                and nx.rm == dst and nx.rm != 4):
            return j
        j += nx.length
        steps += 1
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=os.path.join(RUN, "CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv"))
    ap.add_argument("--out", default=os.path.join(RUN, "01_RAW", "C2_CENSUS.json"))
    args = ap.parse_args()

    data, ib, secs, text, tva = pebnd.load_text()
    sha = hashlib.sha256(data).hexdigest()
    exe_ok = (sha.upper() == pebnd.PINNED_EXE_SHA256 and len(data) == pebnd.PINNED_EXE_SIZE)
    cache = pebnd._BoundaryCache(text, tva)
    n = len(text)

    raw = scan_raw_rows(text, tva)

    # entry this-flow map for known entries (machine-checked, reused)
    thisflow = {e: pebnd_entry_this(text, tva, e) for e in pebnd.KNOWN_ENTRIES}

    out_rows = []
    stats = {
        "raw_pattern_rows": 0,
        "positive_plus_84_encoding_rows": 0,
        "negative_disp8_minus_0x7c_control_rows": 0,
        "boundary_confirmed_positive_rows": 0,
        "known_confirmed_writes": 0,
        "census_unresolved_rows": 0,
        "unresolved_write_candidates": 0,
        "rejected_wrong_object_proven": 0,
        "rejected_read_not_write": 0,
        "address_provenance_unresolved": 0,
        "decoder_reject_rows": 0,
    }

    def prov_for(ins, confirmed, bsrc, bstart):
        if ins is None or not ins.memop:
            return "N_A"
        if not confirmed:
            return "UNRESOLVED"
        if ins.ea_base is None and ins.ea_index is None:
            return "ABSOLUTE_STATIC_ADDRESS"
        if ins.ea_base is not None:
            bn = x86dec.REGS32[ins.ea_base]
            if bsrc == "KNOWN_FUNCTION_ENTRY" and bstart in pebnd.KNOWN_ENTRIES:
                if bn in thisflow[bstart]:
                    return "THIS_OF_KNOWN_FUNCTION:" + pebnd.KNOWN_ENTRIES[bstart]
            return "UNRESOLVED"
        return "UNRESOLVED"

    for (fam, i, mod, rm, regf, dp, dw) in raw:
        va = tva + i
        ins = x86dec.decode(text, i)
        dec_status = "OK" if ins is not None else "REJECT"
        row = {
            "va": "0x%08X" % va, "pattern_family": fam,
            "decoder_status": dec_status,
            "base_register": "", "index_register": "", "scale": "",
            "raw_displacement": "", "signed_displacement": "",
            "effective_displacement": "", "operand_width": "",
            "address_provenance_status": "", "boundary_source": "",
            "boundary_status": "", "containing_function": "",
            "lea_linked_store_va": "", "write_form": "", "classification": "",
            "row_resolution": "", "reason": "",
        }
        row["opcode_bytes"] = text[i:i + (ins.length if ins else 1)].hex(" ").upper()
        row["instruction_length"] = ins.length if ins else ""
        if ins is not None and ins.memop:
            row["base_register"] = x86dec.REGS32[ins.ea_base] if ins.ea_base is not None else "NONE"
            row["index_register"] = x86dec.REGS32[ins.ea_index] if ins.ea_index is not None else "NONE"
            row["scale"] = ins.ea_scale
            row["raw_displacement"] = ("0x%08X" % ins.disp_raw) if ins.disp_width else ("0x84" if dw == 1 else "0x00000084")
            row["signed_displacement"] = ins.disp_signed if ins.disp_width else (-124 if dw == 1 else 132)
            row["effective_displacement"] = row["signed_displacement"]
            row["operand_width"] = (16 if ins.has66 else (8 if ins.opcode in (0x88, 0xC6) and not ins.has66 else 32))
        stats["raw_pattern_rows"] += 1
        if ins is None:
            stats["decoder_reject_rows"] += 1
            row["classification"] = "UNRESOLVED"
            row["row_resolution"] = "UNRESOLVED"
            row["reason"] = "DECODER_REJECT: corrected fail-closed decoder could not decode the pattern (truncated/unsupported); no classification fabricated"
            out_rows.append(row)
            stats["census_unresolved_rows"] += 1
            continue

        is_positive = (dw == 4)  # mod10 disp32 == +132
        # ---- NEGATIVE DISP8 CONTROLS: encoding-level, boundary-free ----
        if not is_positive:
            stats["negative_disp8_minus_0x7c_control_rows"] += 1
            row["boundary_status"] = "NOT_ASSESSED_ENCODING_CONTROL"
            row["classification"] = "NEGATIVE_DISP8_MINUS_0x7C_CONTROL"
            row["row_resolution"] = "RESOLVED_CONTROL"
            row["reason"] = ("MOD01 disp8 is SIGNED: raw 0x84 = -124 = -0x7C; a "
                             "+132 displacement cannot be encoded as disp8 under "
                             "any decoding, so this position cannot host a "
                             "[reg+0x84] access (encoding-level property, "
                             "interpretation-independent)")
            row["address_provenance_status"] = "N_A_ENCODING_CONTROL"
            out_rows.append(row)
            continue

        # ---- POSITIVE (+132 effective displacement) rows ----
        stats["positive_plus_84_encoding_rows"] += 1
        confirmed, bsrc, bstart = pebnd.boundary_confirm(text, tva, va, cache)
        row["boundary_status"] = "CONFIRMED" if confirmed else "UNRESOLVED"
        row["boundary_source"] = bsrc or ""
        if confirmed:
            stats["boundary_confirmed_positive_rows"] += 1
            if bsrc == "KNOWN_FUNCTION_ENTRY" and bstart in pebnd.KNOWN_ENTRIES:
                row["containing_function"] = pebnd.KNOWN_ENTRIES[bstart]
            elif bstart:
                row["containing_function"] = "entry~0x%08X" % bstart
        prov = prov_for(ins, confirmed, bsrc, bstart)
        row["address_provenance_status"] = prov

        op = ins.opcode
        kind = None
        if op in (0x8B, 0x39):
            kind = "read"
        elif op == 0x8D:
            link = lea_link_store(text, tva, va, ins)
            if link is not None:
                kind = "lea_linked_write"
                row["lea_linked_store_va"] = "0x%08X" % (tva + link)
            else:
                kind = "lea_unlinked"
        else:
            kind = "write"
        row["write_form"] = kind

        if kind == "read":
            if confirmed:
                note = KNOWN_READS.get(va)
                row["classification"] = "REJECTED_READ_NOT_WRITE"
                row["row_resolution"] = "RESOLVED_NO_WRITE"
                row["reason"] = ("boundary-confirmed read/CMP form: no memory "
                                 "write occurs" + ((" (" + note + ")") if note else ""))
                stats["rejected_read_not_write"] += 1
            else:
                row["classification"] = "UNRESOLVED"
                row["row_resolution"] = "UNRESOLVED"
                row["reason"] = ("BOUNDARY_UNRESOLVED_NO_WRITE_ESTABLISHED: no "
                                 "trusted decode reaches this position, so the "
                                 "instruction-level read identity is unproven; "
                                 "no +0x84 write is established here either "
                                 "(no inference is drawn from the failed decodes)")
                stats["census_unresolved_rows"] += 1
            out_rows.append(row)
            continue

        if kind == "lea_unlinked":
            if confirmed:
                row["classification"] = "REJECTED_READ_NOT_WRITE"
                row["row_resolution"] = "RESOLVED_NO_WRITE"
                row["reason"] = ("boundary-confirmed LEA without a linked store "
                                 "through the destination register within the "
                                 "bounded window: address computation only, no "
                                 "memory write occurs at this position")
                stats["rejected_read_not_write"] += 1
            else:
                row["classification"] = "UNRESOLVED"
                row["row_resolution"] = "UNRESOLVED"
                row["reason"] = ("BOUNDARY_UNRESOLVED_NO_WRITE_ESTABLISHED: LEA "
                                 "form without trusted boundary; no write "
                                 "established (no inference is drawn from the "
                                 "failed decodes)")
                stats["census_unresolved_rows"] += 1
            out_rows.append(row)
            continue

        # ---- write-candidate rows (write / lea_linked_write) ----
        if not confirmed:
            row["classification"] = "UNRESOLVED"
            row["row_resolution"] = "UNRESOLVED"
            row["reason"] = ("BOUNDARY_UNRESOLVED_WRITE_PATTERN: +0x84-effective "
                             "write-form pattern with no trusted boundary; "
                             "instruction status neither asserted nor denied "
                             "(no inference is drawn from the failed decodes); "
                             "honest unresolved write candidate")
            stats["census_unresolved_rows"] += 1
            stats["unresolved_write_candidates"] += 1
            if prov == "UNRESOLVED":
                stats["address_provenance_unresolved"] += 1
            out_rows.append(row)
            continue

        # boundary confirmed
        if va in KNOWN_STORES:
            store_class, basis = KNOWN_STORES[va]
            row["classification"] = "KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITE"
            row["row_resolution"] = "RESOLVED_CONFIRMED"
            row["reason"] = "store_class=%s; %s; address provenance %s (containing function + machine-checked entry this-flow; the identity chain is preserved prior canon)" % (store_class, basis, prov)
            stats["known_confirmed_writes"] += 1
            out_rows.append(row)
            continue

        if va in LAYOUT_CONTROLS:
            basis_kind, pats, basis = LAYOUT_CONTROLS[va]
            wlo = max(0, i - 32)
            whi = min(n, i + 32)
            win = text[wlo:whi]
            found = [p.hex(" ").upper() for p in pats if p in win]
            if found:
                row["classification"] = "REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE"
                row["row_resolution"] = "RESOLVED_REJECTED"
                row["reason"] = ("provenance_basis=%s; window-verified byte "
                                 "patterns %s; %s" % (basis_kind, found, basis))
                stats["rejected_wrong_object_proven"] += 1
            else:
                row["classification"] = "UNRESOLVED"
                row["row_resolution"] = "UNRESOLVED"
                row["reason"] = ("layout-control window evidence NOT re-verified "
                                 "byte-for-byte this run; downgraded to honest "
                                 "UNRESOLVED (no rejection without re-verified "
                                 "provenance)")
                stats["census_unresolved_rows"] += 1
                stats["unresolved_write_candidates"] += 1
            out_rows.append(row)
            continue

        # proven-this rows in factory-family functions -> additional confirmed
        if (prov.startswith("THIS_OF_KNOWN_FUNCTION:")
                and bstart in FACTORY_THIS_FUNCTIONS):
            row["classification"] = "KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITE"
            row["row_resolution"] = "RESOLVED_CONFIRMED"
            row["reason"] = ("store_class=ADDITIONAL_CONFIRMED_FACTORY_THIS_STORE; "
                             "boundary-confirmed +0x84 write with machine-proven "
                             "this-base inside factory-family function %s "
                             "(structural confirmation at the same standard as "
                             "the two known stores; disclosed as an additional "
                             "positive observation)" % row["containing_function"])
            stats["known_confirmed_writes"] += 1
            out_rows.append(row)
            continue

        # manager-ctor this-base -> proven wrong object (manager != factory)
        if (prov.startswith("THIS_OF_KNOWN_FUNCTION:")
                and bstart == 0x00707E50):
            row["classification"] = "REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE"
            row["row_resolution"] = "RESOLVED_REJECTED"
            row["reason"] = ("provenance_basis=MANAGER_CTOR_THIS_FLOW; the base "
                             "object is the manager (this of FUN_00707E50, "
                             "machine-checked entry this-flow; manager class "
                             "0x100 B singleton 0x00BA12E4 is distinct from the "
                             "factory class 0x118 B singleton 0x00BA590C, prior "
                             "canon); a manager+0x84 access is not the factory "
                             "member")
            stats["rejected_wrong_object_proven"] += 1
            out_rows.append(row)
            continue

        # unresolved provenance: ESP/EBP (register naming is NOT proof) or
        # non-stack base without object provenance
        base_is_stackname = (row["base_register"] in ("ESP", "EBP"))
        if prov == "UNRESOLVED":
            stats["address_provenance_unresolved"] += 1
        if base_is_stackname:
            row["classification"] = "UNRESOLVED"
            row["row_resolution"] = "UNRESOLVED"
            row["reason"] = ("ADDRESS_PROVENANCE_UNRESOLVED: %s-based effective "
                             "address; per the effective-address discipline a "
                             "register NAME is not provenance (EBP is not "
                             "automatically a frame pointer; ESP with an "
                             "unresolved SIB index is not automatically a pure "
                             "stack slot); no stack-frame/dataflow proof was "
                             "attempted; NOT rejected as wrong object"
                             % row["base_register"])
        else:
            row["classification"] = "UNRESOLVED"
            row["row_resolution"] = "UNRESOLVED"
            row["reason"] = ("OBJECT_PROVENANCE_UNRESOLVED: boundary-confirmed "
                             "+0x84 write with base %s not resolved to any "
                             "factory object within the window-level provenance "
                             "bound; no claim made (not a factory+0x84 write "
                             "claim, not a wrong-object rejection)"
                             % row["base_register"])
        stats["census_unresolved_rows"] += 1
        stats["unresolved_write_candidates"] += 1
        out_rows.append(row)

    # ---- closure + summary ----
    # The scanner loop advances i += 1 through EVERY .text position and tests
    # each against every declared family (no skip-ahead), so the ENUMERATION is
    # closed within the declared encodings; unresolved classifications inside
    # the enumeration do not block enumeration closure (and the EXHAUSTIVE
    # invariant stays NOT_ESTABLISHED regardless).
    scan_coverage = {"positions_tested": n, "text_size": n, "declared_families": 10,
                     "skip_ahead": False}
    scan_exhaustive = (n == len(text) and not scan_coverage["skip_ahead"])
    closure = "CLOSED" if scan_exhaustive else "NOT_ESTABLISHED"
    known_store_rows = [r for r in out_rows if r["classification"] == "KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITE"]
    summary = {
        "run": "PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004",
        "stage": "C2",
        "exe": {"sha256": sha, "size": len(data), "pinned_match": exe_ok},
        "declared_examined_encoding_families": [
            "F1 89 r/m32,r32 mod01/mod10 incl SIB", "F2 8B r32,r/m32 mod01/mod10 incl SIB",
            "F3 39 r/m32,r32 mod01/mod10 incl SIB", "F4 8D r32,m mod01/mod10 incl SIB",
            "F5 C7 /0 mod01/mod10 incl SIB", "F6 88 r/m8,r8 mod01/mod10 incl SIB",
            "F7 C6 /0 mod01/mod10 incl SIB", "F8 66 89 mod01/mod10 NON-SIB",
            "F9 66 C7 /0 mod01/mod10 NON-SIB",
        ],
        "scope_note": ("66-form SIB variants were not in the historical examined "
                       "families and remain outside this enumeration; mod00 "
                       "absolute forms ([disp32]) are not object+0x84 encodings "
                       "and were never in the examined families"),
        "measured_quantities": {
            "RAW_PATTERN_ROWS": stats["raw_pattern_rows"],
            "POSITIVE_PLUS_84_ENCODING_ROWS": stats["positive_plus_84_encoding_rows"],
            "NEGATIVE_DISP8_MINUS_0x7C_CONTROL_ROWS": stats["negative_disp8_minus_0x7c_control_rows"],
            "BOUNDARY_CONFIRMED_POSITIVE_PLUS_84_ROWS": stats["boundary_confirmed_positive_rows"],
            "KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITES": stats["known_confirmed_writes"],
            "CENSUS_UNRESOLVED_ROWS": stats["census_unresolved_rows"],
            "FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES": stats["unresolved_write_candidates"],
            "REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE": stats["rejected_wrong_object_proven"],
            "REJECTED_READ_NOT_WRITE": stats["rejected_read_not_write"],
            "ADDRESS_PROVENANCE_UNRESOLVED": stats["address_provenance_unresolved"],
            "DECODER_REJECT_ROWS": stats["decoder_reject_rows"],
        },
        "definitions": {
            "CENSUS_UNRESOLVED_ROWS": ("all census rows with row_resolution=UNRESOLVED: "
                                       "boundary-unresolved read/LEA rows (no write "
                                       "established but instruction identity unproven) "
                                       "PLUS all unresolved write candidates"),
            "FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES": ("write-form positive-encoding "
                                                            "rows (incl. linked-LEA) not "
                                                            "resolved to a confirmed "
                                                            "factory write or a proven "
                                                            "wrong-object rejection"),
            "EXAMINED_ENCODING_CANDIDATE_CLOSURE": ("CLOSED = every byte position of "
                                                    ".text was tested against every "
                                                    "declared family with the validated "
                                                    "decoder; it does NOT mean all "
                                                    "candidates were classified, and it "
                                                    "is scoped to the declared "
                                                    "encodings/effective-address forms "
                                                    "only"),
        },
        "closure": {
            "EXAMINED_ENCODING_CANDIDATE_CLOSURE": closure,
            "scan_coverage": scan_coverage,
            "EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE": "NOT_ESTABLISHED",
            "exhaustive_note": ("invariant: even complete resolution of every "
                                "corrected-scanner row cannot exclude alias writes, "
                                "helper-mediated writes, bulk/memory-copy writes, "
                                "other address constructions, unexamined encodings "
                                "or runtime mutation"),
        },
        "known_stores": {
            r["va"]: {"store_class": KNOWN_STORES[int(r["va"], 16)][0],
                      "classification": r["classification"],
                      "boundary": r["boundary_status"],
                      "containing_function": r["containing_function"],
                      "base_register": r["base_register"],
                      "signed_displacement": r["signed_displacement"],
                      "address_provenance_status": r["address_provenance_status"]}
            for r in known_store_rows
        },
        "clear_reset_confirmed_count": sum(
            1 for r in known_store_rows if "clear" in r["reason"].lower()),
        "clear_reset_note": ("CLEAR_RESET_CONFIRMED_COUNT=0 means no clear/reset "
                             "store of the member was CONFIRMED within the "
                             "examined census; it does NOT mean clear/reset is "
                             "proven absent"),
    }

    # classification tally cross-check
    tally = {}
    for r in out_rows:
        tally[r["classification"]] = tally.get(r["classification"], 0) + 1
    summary["classification_tally"] = tally

    with open(args.out, "w", newline="\n") as f:
        json.dump(summary, f, indent=1)

    hdr = ["row_id", "va", "pattern_family", "opcode_bytes", "instruction_length",
           "decoder_status", "write_form", "operand_width", "base_register",
           "index_register", "scale", "raw_displacement", "signed_displacement",
           "effective_displacement", "address_provenance_status",
           "boundary_source", "boundary_status", "containing_function",
           "lea_linked_store_va", "classification", "row_resolution", "reason"]
    with open(args.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(hdr)
        for k, r in enumerate(out_rows, 1):
            w.writerow([k, r["va"], r["pattern_family"], r["opcode_bytes"],
                        r["instruction_length"], r["decoder_status"],
                        r["write_form"], r["operand_width"], r["base_register"],
                        r["index_register"], r["scale"], r["raw_displacement"],
                        r["signed_displacement"], r["effective_displacement"],
                        r["address_provenance_status"], r["boundary_source"],
                        r["boundary_status"], r["containing_function"],
                        r["lea_linked_store_va"], r["classification"],
                        r["row_resolution"], r["reason"]])

    mq = summary["measured_quantities"]
    print("C2 done. raw=%d pos=%d negctl=%d bndpos=%d known=%d unres=%d w cand=%d "
          "wrongobj=%d read=%d provunres=%d" % (
              mq["RAW_PATTERN_ROWS"], mq["POSITIVE_PLUS_84_ENCODING_ROWS"],
              mq["NEGATIVE_DISP8_MINUS_0x7C_CONTROL_ROWS"],
              mq["BOUNDARY_CONFIRMED_POSITIVE_PLUS_84_ROWS"],
              mq["KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITES"],
              mq["CENSUS_UNRESOLVED_ROWS"],
              mq["FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES"],
              mq["REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE"],
              mq["REJECTED_READ_NOT_WRITE"],
              mq["ADDRESS_PROVENANCE_UNRESOLVED"]))


def pebnd_entry_this(text, tva, entry_va, win=0x40):
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


if __name__ == "__main__":
    main()
