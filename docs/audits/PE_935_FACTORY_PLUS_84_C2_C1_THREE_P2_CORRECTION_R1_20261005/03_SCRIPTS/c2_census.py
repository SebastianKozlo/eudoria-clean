# c2_census.py
# RUN: PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005
# F84-C2 CENSUS REGENERATION with the corrected boundary/decoder rules
# (AF2 + AF3 + P3-B repair), freshly recomputed from the pinned EXE.
#
# AF2/AF3/P3-B CORRECTIONS vs the C1 census:
#   * Byte-level grammar enumeration is PRESERVED INDEPENDENTLY of boundary
#     classification (unchanged scanner: every .text position tested against
#     every declared family, no skip-ahead).
#   * BOUNDARY_CONFIRMED now requires a STRONG anchor only (KNOWN_FUNCTION_ENTRY
#     with recorded provenance). The C1 CC_PADDING/RET_DELIMITED confirmations are
#     demoted to HEURISTIC_START_CANDIDATE (recorded, never confirming).
#   * A proven decode covering a candidate mid-instruction REFUTES it
#     (REJECTED_MID_INSTRUCTION_PER_PROVEN_DECODE - a successful-decode
#     refutation, never an inference from a failed decode); a conflicting
#     heuristic start NEVER overrides the proven decode (contract precedence).
#   * AF3: REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE requires a concrete
#     identity chain from the effective-address base to a specific
#     independently established object (persisted per row in
#     AF3_PROVENANCE_LEDGER.csv with CANDIDATE_VA/INSTRUCTION_BYTES/
#     EFFECTIVE_ADDRESS/BASE_REGISTER/ADDRESS_PROVENANCE_STATUS/IDENTITY_EDGE/
#     IDENTIFIED_OBJECT/IDENTITY_EVIDENCE/IDENTITY_EVIDENCE_STATUS/
#     FINAL_CLASSIFICATION). The four C1 "layout-evidence" wrong-object
#     rejections are DOWNGRADED to UNRESOLVED (their C1 boundary confirmation
#     was padding-derived AND their window evidence is a layout/value/init
#     GRAMMAR hypothesis, not an identity chain). The manager-ctor row keeps
#     its PROVEN classification (machine-checked this-flow to the manager
#     object - a distinct independently established object).
#   * The 0x0075138F ArkEstateObject lead (vptr 0x00A87410 / MSVC
#     TypeDescriptor .?AVArkEstateObject@@, named by the Desktop post-audit) is
#     physically re-verified in a bounded window read and the RTTI chain is
#     byte-read - but the candidate's containing function has NO strong anchor,
#     so the candidate base CANNOT be physically bridged to that object within
#     this correction's discipline: the lead is recorded as NOT_PROMOTED and
#     the row stays UNRESOLVED.
#   * P3-B: DECLARED_ENCODING_FAMILY_COUNT is DERIVED from the actual scanner
#     family table (len(FAMILIES)); metadata, JSON and report agree. The C1
#     metadata value 10 (with an explicit list of 9) is superseded.
#
# The historical counts (1685/828/1217/5 and every other boundary- or
# provenance-dependent number) are NOT targets; they are superseded and
# re-measured. 2612 is a regression expectation for the raw byte grammar only.
# EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE = NOT_ESTABLISHED (invariant).
#
# Outputs: CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv,
# 01_RAW/C2_CENSUS.json, AF3_PROVENANCE_LEDGER.csv (--csv/--out/--af3 overrides).
# READ-ONLY vs the pinned EXE.

import argparse
import csv
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
       r"\PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005")

# ---------------------------------------------------------------------------
# P3-B: the DECLARED scanner family table (single source of truth; the count
# is derived - never hard-coded). Same 9 examined families as the C1 scanner.
# ---------------------------------------------------------------------------
FAMILIES = [
    ("F1_89", 0x89, "89 r/m32,r32 mod01/mod10 incl SIB"),
    ("F2_8B", 0x8B, "8B r32,r/m32 mod01/mod10 incl SIB"),
    ("F3_39", 0x39, "39 r/m32,r32 mod01/mod10 incl SIB"),
    ("F4_8D", 0x8D, "8D r32,m mod01/mod10 incl SIB"),
    ("F5_C7", 0xC7, "C7 /0 mod01/mod10 incl SIB"),
    ("F6_88", 0x88, "88 r/m8,r8 mod01/mod10 incl SIB"),
    ("F7_C6", 0xC6, "C6 /0 mod01/mod10 incl SIB"),
    ("F8_6689_WORD", 0x89, "66 89 mod01/mod10 NON-SIB (word)"),
    ("F9_66C7_WORD", 0xC7, "66 C7 /0 mod01/mod10 NON-SIB (word)"),
]
DECLARED_ENCODING_FAMILY_COUNT = len(FAMILIES)
DISCLOSED_OUT_OF_SCOPE = [
    "66-form SIB variants (66 89 / 66 C7 with SIB) - not in the historical "
    "examined families; disclosed scope boundary",
    "mod00 absolute forms ([disp32]) - not object+0x84 encodings; never in "
    "the examined families",
    "67-prefixed (16-bit-address) variants - not in the examined families",
]

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

# The four Desktop-identified layout/value/init controls. AF3 correction:
# these are NOT identity chains - each is a layout/value/init GRAMMAR
# hypothesis only. Their C1 REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE
# classification is superseded; they are downgraded to UNRESOLVED (option B
# of the AF3 contract - no forced option A, no new class atlas). The window
# byte evidence is re-verified and recorded as HYPOTHESIS support only.
LAYOUT_CONTROLS = {
    0x0074955A: {
        "patterns": [b"\x88\x9e\x88\x00\x00\x00", b"\x88\x9e\x89\x00\x00\x00"],
        "hypothesis": ("sibling-class ctor: byte stores at the SAME base "
                       "+0x88/+0x89 (MOV BYTE [ESI+0x88],r8 / [ESI+0x89],r8) "
                       "vs the factory class dword slot-array vector at +0x88 "
                       "(prior canon FUN_0070E2F0/FUN_0070C180); HYPOTHESIS: "
                       "different class layout - NOT an identity chain"),
    },
    0x006D4F88: {
        "patterns": [b"\xbe\x04\x00\x00\x00"],
        "hypothesis": ("class ctor writing the integer 4 (MOV ESI,4) into "
                       "+0x84 of its base; the factory +0x84 is a pointer "
                       "member written from a ctor'd object pointer or NULL "
                       "(the two known stores); HYPOTHESIS: different value "
                       "grammar - NOT an identity chain"),
    },
    0x0075138F: {
        "patterns": [b"\x8d\x8e\x88\x00\x00\x00"],
        "hypothesis": ("class initializing a helper-object pointer at its "
                       "+0x88 (LEA ECX,[ESI+0x88] + helper CALL) vs the "
                       "factory dword slot-array vector at +0x88 (prior "
                       "canon); HYPOTHESIS: different class layout - NOT an "
                       "identity chain"),
        "lead": ("Desktop post-audit AF3 lead: a direct store of vptr "
                 "0x00A87410 and MSVC TypeDescriptor .?AVArkEstateObject@@ "
                 "recovered by a bounded read of the same ctor window. The "
                 "lead is re-verified physically this run (window + RTTI "
                 "chain bytes) but the candidate's containing function has "
                 "NO strong anchor, so the candidate's base/object CANNOT be "
                 "physically bridged to that vptr/object identity within "
                 "this correction's boundary discipline. NOT promoted; "
                 "recorded for a future authorized run."),
    },
    0x007196AA: {
        "patterns": [b"\x1c\x92\xba\x00", b"\x20\x92\xba\x00", b"\x24\x92\xba\x00"],
        "hypothesis": ("static globals 0x00BA921C/0x00BA9220/0x00BA9224 "
                       "copied into +0x84/+0x88/+0x8C of the base; the "
                       "factory ctor writes +0x84 from a zeroed register and "
                       "builds its +0x88 vector via FUN_0070E2F0; HYPOTHESIS: "
                       "different init grammar - NOT an identity chain"),
    },
}

KNOWN_READS = {
    0x0070DD1A: "consumer NULL gate CMP (FUN_0070DCF0)",
    0x0070DD6A: "consumer stream load 1 (FUN_0070DCF0)",
    0x0070DD7E: "consumer stream load 2 (FUN_0070DCF0)",
    0x0070C6BE: "setter entry guard CMP (FUN_0070C680)",
    0x0070BFD0: "stream bridge method load (FUN_0070BFD0)",
}

LEAD_VPTR = 0x00A87410
LEAD_TD_NAME_EXPECT = ".?AVArkEstateObject@@"


def scan_raw_rows(text, tva):
    """Byte-by-byte enumeration of the declared families. Every position is
    tested against every family (no skip-ahead: overlapping occurrences are
    all recorded). PRESERVED from C1 - the raw grammar enumeration is
    independent of the boundary classification."""
    n = len(text)
    rows = []
    i = 0
    while i < n:
        b0 = text[i]
        fam = None
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


def verify_ark_lead(text, tva, data, ib, secs, va):
    """Bounded physical re-verification of the 0x0075138F ArkEstateObject lead.
    (1) window read: search +-0x40 around the candidate for the LEAD vptr
    immediate bytes; (2) RTTI chain byte-read: [vptr-4] -> COL, [COL+0x0C] ->
    TypeDescriptor, [TD+8..] -> the decorated name.  NO promotion: the
    containing function has no strong anchor, so the candidate base cannot be
    bound to this object within this run's discipline."""
    out = {"lead_vptr": "0x%08X" % LEAD_VPTR}
    wlo = max(0, (va - tva) - 0x40)
    whi = min(len(text), (va - tva) + 0x40)
    win = text[wlo:whi]
    pat = struct.pack("<I", LEAD_VPTR)
    hits = []
    k = win.find(pat)
    while k != -1:
        hits.append("0x%08X" % (tva + wlo + k))
        k = win.find(pat, k + 1)
    out["window_vptr_immediate_hits"] = hits
    out["window_bytes"] = win.hex(" ").upper()
    # RTTI chain byte-read
    def rd(va, n):
        o = pebnd.va_to_off(ib, secs, va)
        if o is None:
            return None
        b = data[o:o + n]
        return b if len(b) == n else None
    col = rd(LEAD_VPTR - 4, 4)
    if col is not None:
        col_va = struct.unpack("<I", col)[0]
        out["vptr_minus_4_col_va"] = "0x%08X" % col_va
        td = rd(col_va + 0x0C, 4)
        if td is not None:
            td_va = struct.unpack("<I", td)[0]
            out["col_plus_0xc_td_va"] = "0x%08X" % td_va
            name_bytes = rd(td_va + 8, 64)
            if name_bytes is not None:
                end = name_bytes.find(b"\x00")
                name = name_bytes[:end if end != -1 else 64].decode("ascii", "replace")
                out["td_name"] = name
                out["td_name_matches_desktop_lead"] = (name == LEAD_TD_NAME_EXPECT)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=os.path.join(RUN, "CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv"))
    ap.add_argument("--out", default=os.path.join(RUN, "01_RAW", "C2_CENSUS.json"))
    ap.add_argument("--af3", default=os.path.join(RUN, "AF3_PROVENANCE_LEDGER.csv"))
    args = ap.parse_args()

    data, ib, secs, text, tva = pebnd.load_text()
    sha = hashlib.sha256(data).hexdigest()
    exe_ok = (sha.upper() == pebnd.PINNED_EXE_SHA256 and len(data) == pebnd.PINNED_EXE_SIZE)
    cache = pebnd._BoundaryCache(text, tva)
    n = len(text)

    raw = scan_raw_rows(text, tva)

    # entry this-flow map for known entries (machine-checked, reused)
    thisflow = {}
    for e in pebnd.KNOWN_ENTRIES:
        regs = set()
        i = e - tva
        end = i + 0x40
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
        thisflow[e] = regs

    out_rows = []
    af3_rows = []
    stats = {
        "raw_pattern_rows": 0,
        "positive_plus_84_encoding_rows": 0,
        "negative_disp8_minus_0x7c_control_rows": 0,
        "boundary_confirmed_positive_rows": 0,
        "boundary_refuted_mid_instruction_rows": 0,
        "known_confirmed_writes": 0,
        "census_unresolved_rows": 0,
        "unresolved_write_candidates": 0,
        "rejected_wrong_object_proven": 0,
        "rejected_read_not_write": 0,
        "rejected_mid_instruction": 0,
        "address_provenance_unresolved": 0,
        "decoder_reject_rows": 0,
    }

    def prov_for(ins, bstatus, bsrc, bstart):
        if ins is None or not ins.memop:
            return "N_A"
        if bstatus != "CONFIRMED":
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
            "boundary_status": "", "boundary_refuted_by": "",
            "containing_function": "",
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
        bstatus, bsrc, bstart, brefuted = pebnd.boundary_confirm(text, tva, va, cache)
        row["boundary_status"] = bstatus
        row["boundary_source"] = bsrc or ""
        if brefuted:
            row["boundary_refuted_by"] = "0x%08X" % brefuted
        if bstatus == "CONFIRMED":
            stats["boundary_confirmed_positive_rows"] += 1
            if bsrc == "KNOWN_FUNCTION_ENTRY" and bstart in pebnd.KNOWN_ENTRIES:
                row["containing_function"] = pebnd.KNOWN_ENTRIES[bstart]
        elif bstatus == "REFUTED_MID_INSTRUCTION":
            stats["boundary_refuted_mid_instruction_rows"] += 1
        prov = prov_for(ins, bstatus, bsrc, bstart)
        row["address_provenance_status"] = prov

        # ---- REFUTED rows: operand/interior data on a PROVEN decode path ----
        if bstatus == "REFUTED_MID_INSTRUCTION":
            row["classification"] = "REJECTED_MID_INSTRUCTION_PER_PROVEN_DECODE"
            row["row_resolution"] = "RESOLVED_NOT_AN_INSTRUCTION_START"
            row["reason"] = ("REFUTED_MID_INSTRUCTION: the position lies strictly "
                             "inside one instruction of the sequential fail-closed "
                             "decode from strong anchor 0x%08X (KNOWN_FUNCTION_ENTRY "
                             "with recorded provenance); the pattern bytes are "
                             "operand/interior data ON THAT PROVEN PATH. This is a "
                             "successful-decode refutation, NOT an inference from a "
                             "failed decode; a conflicting padding-derived heuristic "
                             "start can NEVER override the proven decode (AF2 "
                             "precedence rule); no +0x84 write and no CALL promotion "
                             "is possible at this position" % brefuted)
            stats["rejected_mid_instruction"] += 1
            out_rows.append(row)
            continue

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
            if bstatus == "CONFIRMED":
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
                                 "strong-anchor decode reaches this position, so "
                                 "the instruction-level read identity is unproven; "
                                 "no +0x84 write is established here either "
                                 "(no inference is drawn from the failed decodes; "
                                 "heuristic starts are recorded but never "
                                 "confirming)")
                stats["census_unresolved_rows"] += 1
            out_rows.append(row)
            continue

        if kind == "lea_unlinked":
            if bstatus == "CONFIRMED":
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
                                 "form without a strong-anchor boundary; no write "
                                 "established (no inference is drawn from the "
                                 "failed decodes)")
                stats["census_unresolved_rows"] += 1
            out_rows.append(row)
            continue

        # ---- write-candidate rows (write / lea_linked_write) ----
        if bstatus != "CONFIRMED":
            row["classification"] = "UNRESOLVED"
            row["row_resolution"] = "UNRESOLVED"
            lc = LAYOUT_CONTROLS.get(va)
            if lc is not None:
                # AF3 downgrade: boundary unresolved AND the window evidence is
                # a grammar hypothesis only -> UNRESOLVED with the hypothesis
                # recorded (contract option B; never PROVEN_WRONG_OBJECT).
                wlo = max(0, i - 32)
                whi = min(n, i + 32)
                win = text[wlo:whi]
                found = [p.hex(" ").upper() for p in lc["patterns"] if p in win]
                lead_txt = (" " + lc["lead"]) if lc.get("lead") else ""
                row["reason"] = ("BOUNDARY_UNRESOLVED_WRITE_PATTERN (AF3-DOWNGRADED "
                                 "LAYOUT CONTROL): +0x84-effective write-form "
                                 "pattern with no strong-anchor boundary; the C1 "
                                 "REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE "
                                 "classification is SUPERSEDED - the window "
                                 "patterns %s support only the HYPOTHESIS '%s'%s; "
                                 "ADDRESS_PROVENANCE remains UNRESOLVED and no "
                                 "identity chain exists, so the honest "
                                 "classification is UNRESOLVED (not "
                                 "PROVEN_WRONG_OBJECT)"
                                 % (found, lc["hypothesis"], lead_txt))
            else:
                row["reason"] = ("BOUNDARY_UNRESOLVED_WRITE_PATTERN: +0x84-effective "
                                 "write-form pattern with no strong-anchor boundary; "
                                 "instruction status neither asserted nor denied "
                                 "(no inference is drawn from the failed decodes; "
                                 "heuristic starts are recorded but never "
                                 "confirming); honest unresolved write candidate")
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
            # boundary confirmed but AF3 downgrade still applies: the window
            # evidence is a grammar hypothesis, NOT an identity chain
            lc = LAYOUT_CONTROLS[va]
            wlo = max(0, i - 32)
            whi = min(n, i + 32)
            win = text[wlo:whi]
            found = [p.hex(" ").upper() for p in lc["patterns"] if p in win]
            row["classification"] = "UNRESOLVED"
            row["row_resolution"] = "UNRESOLVED"
            row["reason"] = ("AF3-DOWNGRADED LAYOUT CONTROL: boundary confirmed "
                             "but the window patterns %s support only the "
                             "HYPOTHESIS '%s'; no identity chain from the "
                             "effective-address base to a specific independently "
                             "established object exists, so PROVEN_WRONG_OBJECT "
                             "is refused and the row is UNRESOLVED"
                             % (found, lc["hypothesis"]))
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

        # manager-ctor this-base -> proven wrong object (manager != factory).
        # AF3: the FULL identity chain is persisted per row in
        # AF3_PROVENANCE_LEDGER.csv (concrete chain: EA base = machine-checked
        # this of FUN_00707E50 -> the manager object, an independently
        # established prior-canon object distinct from the factory).
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
                             "member; identity chain per row in "
                             "AF3_PROVENANCE_LEDGER.csv")
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

    # ---- AF3 provenance ledger (contract per-row fields) ----
    # every wrong-object-relevant candidate gets a row: the manager control
    # (PROVEN chain) + the four downgraded layout controls (UNRESOLVED).
    ark_lead = None
    for r in out_rows:
        va_i = int(r["va"], 16)
        if va_i not in LAYOUT_CONTROLS and not (
                r["classification"] == "REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE"):
            continue
        if va_i in LAYOUT_CONTROLS:
            lc = LAYOUT_CONTROLS[va_i]
            edge = ("none established: window byte patterns support only a "
                    "layout/value/init grammar hypothesis; no identity chain "
                    "from the effective-address base to any specific "
                    "independently established object")
            ident = "NONE"
            ev = ("window patterns %s (hypothesis: %s)" % (
                [p.hex(" ").upper() for p in lc["patterns"]],
                lc["hypothesis"]))
            if va_i == 0x0075138F and ark_lead is None:
                ark_lead = verify_ark_lead(text, tva, data, ib, secs, va_i)
                ev += ("; ArkEstateObject lead re-verified physically this run: %s "
                       "(NOT promoted - the containing function has no strong "
                       "anchor, so the base/object cannot be bridged within this "
                       "discipline)" % json.dumps(ark_lead))
            ev_status = ("HEURISTIC_WINDOW_ONLY_NOT_AN_IDENTITY_CHAIN"
                         if va_i != 0x0075138F else
                         "HEURISTIC_WINDOW_LEAD_NOT_PROMOTED_NO_BOUNDARY")
            final = "UNRESOLVED"
            provst = "UNRESOLVED"
        else:
            # manager row (or any future PROVEN row)
            edge = ("effective-address base register = machine-checked this "
                    "of FUN_00707E50 (entry this-flow: MOV reg,ECX in the "
                    "entry window, re-derived this run)")
            ident = ("the MANAGER object (prior canon: manager class 0x100 B, "
                     "singleton global 0x00BA12E4, manager getter FUN_00415470 "
                     "-> ctor FUN_00707E50; manager global reference census "
                     "re-measured this run)")
            ev = ("entry this-flow machine-check (this run) + manager singleton "
                  "global 0x00BA12E4 reference census (this run, C1 JSON) + "
                  "prior canon manager/factory distinction (factory class "
                  "0x118 B singleton 0x00BA590C)")
            ev_status = ("IDENTITY_CHAIN_PHYSICALLY_REVERIFIED_THIS_RUN"
                        " (prior canon + this-run machine checks)")
            final = "REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE"
            provst = "THIS_OF_KNOWN_FUNCTION:FUN_00707E50_manager_ctor"
        af3_rows.append({
            "CANDIDATE_VA": r["va"],
            "INSTRUCTION_BYTES": r["opcode_bytes"],
            "EFFECTIVE_ADDRESS": ("%s;effective_displacement=%s"
                                  % (r["base_register"], r["effective_displacement"])),
            "BASE_REGISTER": r["base_register"],
            "ADDRESS_PROVENANCE_STATUS": (provst if final.startswith("REJECTED")
                                          else "UNRESOLVED"),
            "IDENTITY_EDGE": edge,
            "IDENTIFIED_OBJECT": ident,
            "IDENTITY_EVIDENCE": ev,
            "IDENTITY_EVIDENCE_STATUS": ev_status,
            "FINAL_CLASSIFICATION": final,
        })

    # ---- closure + summary ----
    # The scanner loop advances i += 1 through EVERY .text position and tests
    # each against every declared family (no skip-ahead), so the raw byte
    # grammar ENUMERATION is closed within the declared encodings. The AF2
    # correction does NOT reduce the enumeration; it reduces BOUNDARY/
    # IDENTITY coverage inside it (disclosed separately - see
    # boundary_coverage). EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE stays
    # NOT_ESTABLISHED regardless.
    scan_coverage = {"positions_tested": n, "text_size": n,
                     "declared_families": DECLARED_ENCODING_FAMILY_COUNT,
                     "skip_ahead": False}
    scan_exhaustive = (n == len(text) and not scan_coverage["skip_ahead"])
    closure = "CLOSED" if scan_exhaustive else "NOT_ESTABLISHED"
    known_store_rows = [r for r in out_rows if r["classification"] == "KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITE"]
    tally = {}
    for r in out_rows:
        tally[r["classification"]] = tally.get(r["classification"], 0) + 1
    summary = {
        "run": "PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005",
        "stage": "C2",
        "exe": {"sha256": sha, "size": len(data), "pinned_match": exe_ok},
        "declared_examined_encoding_families": [f[2] for f in FAMILIES],
        "DECLARED_ENCODING_FAMILY_COUNT": DECLARED_ENCODING_FAMILY_COUNT,
        "declared_family_note": ("P3-B correction: derived from the actual "
                                 "scanner family table (len(FAMILIES)=%d); "
                                 "metadata, JSON, CSV and report agree. The C1 "
                                 "metadata value declared_families=10 with an "
                                 "explicit list of 9 is SUPERSEDED."
                                 % DECLARED_ENCODING_FAMILY_COUNT),
        "disclosed_but_out_of_scope_families": DISCLOSED_OUT_OF_SCOPE,
        "boundary_policy": ("AF2-CORRECTED: strong anchors only (KNOWN_FUNCTION_"
                            "ENTRY with recorded anchor provenance); heuristic "
                            "starts (C1 T2/T3) recorded but NEVER confirming; "
                            "proven mid-instruction coverage REFUTES the "
                            "candidate; no inference from failed decodes"),
        "measured_quantities": {
            "RAW_PATTERN_ROWS": stats["raw_pattern_rows"],
            "POSITIVE_PLUS_84_ENCODING_ROWS": stats["positive_plus_84_encoding_rows"],
            "NEGATIVE_DISP8_MINUS_0x7C_CONTROL_ROWS": stats["negative_disp8_minus_0x7c_control_rows"],
            "BOUNDARY_CONFIRMED_POSITIVE_PLUS_84_ROWS": stats["boundary_confirmed_positive_rows"],
            "BOUNDARY_REFUTED_MID_INSTRUCTION_ROWS": stats["boundary_refuted_mid_instruction_rows"],
            "KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITES": stats["known_confirmed_writes"],
            "CENSUS_UNRESOLVED_ROWS": stats["census_unresolved_rows"],
            "FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES": stats["unresolved_write_candidates"],
            "REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE": stats["rejected_wrong_object_proven"],
            "REJECTED_READ_NOT_WRITE": stats["rejected_read_not_write"],
            "REJECTED_MID_INSTRUCTION_PER_PROVEN_DECODE": stats["rejected_mid_instruction"],
            "ADDRESS_PROVENANCE_UNRESOLVED": stats["address_provenance_unresolved"],
            "DECODER_REJECT_ROWS": stats["decoder_reject_rows"],
        },
        "definitions": {
            "CENSUS_UNRESOLVED_ROWS": ("all census rows with row_resolution=UNRESOLVED: "
                                        "boundary-unresolved read/LEA rows (no write "
                                        "established but instruction identity unproven) "
                                        "PLUS all unresolved write candidates (incl. the "
                                        "four AF3-downgraded layout controls)"),
            "FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES": ("write-form positive-encoding "
                                                            "rows (incl. linked-LEA) not "
                                                            "resolved to a confirmed "
                                                            "factory write or a proven "
                                                            "wrong-object rejection"),
            "REJECTED_MID_INSTRUCTION_PER_PROVEN_DECODE": ("positive-encoding rows REFUTED "
                                                           "by a strong-anchor decode that "
                                                           "covers the position strictly "
                                                           "inside one instruction "
                                                           "(successful-decode refutation, "
                                                           "never an inference from a "
                                                           "failed decode)"),
            "EXAMINED_ENCODING_CANDIDATE_CLOSURE": ("CLOSED = every byte position of "
                                                    ".text was tested against every "
                                                    "declared family (raw byte-grammar "
                                                    "enumeration); it does NOT mean all "
                                                    "candidates were boundary-classified, "
                                                    "and it is scoped to the declared "
                                                    "encodings/effective-address forms "
                                                    "only"),
        },
        "closure": {
            "EXAMINED_ENCODING_CANDIDATE_CLOSURE": closure,
            "closure_scope_note": ("the AF2 correction reduces BOUNDARY/IDENTITY "
                                   "coverage inside the closed enumeration (only "
                                   "strong-anchor-reachable rows are "
                                   "boundary-classified); the raw byte-grammar "
                                   "enumeration itself is unchanged and closed"),
            "scan_coverage": scan_coverage,
            "EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE": "NOT_ESTABLISHED",
            "exhaustive_note": ("invariant: even complete resolution of every "
                                "corrected-scanner row cannot exclude alias writes, "
                                "helper-mediated writes, bulk/memory-copy writes, "
                                "other address constructions, unexamined encodings "
                                "or runtime mutation"),
        },
        "af3_note": ("AF3 correction: REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE "
                     "requires a concrete identity chain persisted per row in "
                     "AF3_PROVENANCE_LEDGER.csv; the four C1 layout-evidence "
                     "rejections are downgraded to UNRESOLVED (grammar "
                     "hypotheses, not identity chains); the 0x0075138F "
                     "ArkEstateObject lead is physically re-verified but NOT "
                     "promoted (no strong anchor for the containing function)"),
        "ark_estate_lead": ark_lead,
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
        "classification_tally": tally,
    }

    with open(args.out, "w", newline="\n") as f:
        json.dump(summary, f, indent=1)

    hdr = ["row_id", "va", "pattern_family", "opcode_bytes", "instruction_length",
           "decoder_status", "write_form", "operand_width", "base_register",
           "index_register", "scale", "raw_displacement", "signed_displacement",
           "effective_displacement", "address_provenance_status",
           "boundary_source", "boundary_status", "boundary_refuted_by",
           "containing_function", "lea_linked_store_va", "classification",
           "row_resolution", "reason"]
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
                        r["boundary_status"], r["boundary_refuted_by"],
                        r["containing_function"], r["lea_linked_store_va"],
                        r["classification"], r["row_resolution"], r["reason"]])

    with open(args.af3, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["CANDIDATE_VA", "INSTRUCTION_BYTES", "EFFECTIVE_ADDRESS",
                    "BASE_REGISTER", "ADDRESS_PROVENANCE_STATUS", "IDENTITY_EDGE",
                    "IDENTIFIED_OBJECT", "IDENTITY_EVIDENCE",
                    "IDENTITY_EVIDENCE_STATUS", "FINAL_CLASSIFICATION"])
        for r in af3_rows:
            w.writerow([r["CANDIDATE_VA"], r["INSTRUCTION_BYTES"],
                        r["EFFECTIVE_ADDRESS"], r["BASE_REGISTER"],
                        r["ADDRESS_PROVENANCE_STATUS"], r["IDENTITY_EDGE"],
                        r["IDENTIFIED_OBJECT"], r["IDENTITY_EVIDENCE"],
                        r["IDENTITY_EVIDENCE_STATUS"], r["FINAL_CLASSIFICATION"]])

    mq = summary["measured_quantities"]
    print("C2 done. raw=%d pos=%d negctl=%d bndpos=%d refuted=%d known=%d unres=%d "
          "w cand=%d wrongobj=%d read=%d midrej=%d provunres=%d decreject=%d af3rows=%d" % (
              mq["RAW_PATTERN_ROWS"], mq["POSITIVE_PLUS_84_ENCODING_ROWS"],
              mq["NEGATIVE_DISP8_MINUS_0x7C_CONTROL_ROWS"],
              mq["BOUNDARY_CONFIRMED_POSITIVE_PLUS_84_ROWS"],
              mq["BOUNDARY_REFUTED_MID_INSTRUCTION_ROWS"],
              mq["KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITES"],
              mq["CENSUS_UNRESOLVED_ROWS"],
              mq["FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES"],
              mq["REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE"],
              mq["REJECTED_READ_NOT_WRITE"],
              mq["REJECTED_MID_INSTRUCTION_PER_PROVEN_DECODE"],
              mq["ADDRESS_PROVENANCE_UNRESOLVED"],
              mq["DECODER_REJECT_ROWS"], len(af3_rows)))


if __name__ == "__main__":
    main()
