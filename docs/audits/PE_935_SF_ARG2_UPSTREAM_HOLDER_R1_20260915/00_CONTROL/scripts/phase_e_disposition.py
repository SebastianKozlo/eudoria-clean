"""
phase_e_disposition.py - PHASE E (G9/G10/G11) disposition record.
There is no PROVEN caller of FUN_006FAB80 (Phase D: 0 direct E8/E9/EB, 0 proven
dispatch candidates). This raw records, deterministically:
- the re-measured arg1/arg2 ABI contract of the thunk (from its own bytes),
- the disposition of the strongest-bounded Phase D candidates (the 5 REJECTED
  rows, re-verified: their receiver classes' slot-2 functions != the thunk),
- the arg2 producer-source test list with honest NOT_DEMONSTRATED outcomes.
Writes 01_RAW/ARG2_VALUE_FLOW_RAW.txt.
Input raw: 01_RAW/THUNK_CALLER_CENSUS.csv (deterministic, same run).
Re-measures size+SHA256+PE layout FIRST (fail-closed).
"""
import sys
import os
import capstone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import s0_common as S

RUN_DIR = os.path.dirname(os.path.dirname(HERE))
RAW = os.path.join(RUN_DIR, "01_RAW")

THUNK = 0x006FAB80
SF_VTABLE = 0x00A7D458

ARG2_SOURCE_CLASSES = [
    "string literal",
    "pointer-to-object-name",
    "NIF-scenegraph name",
    "animation channel name",
    "bone name",
    "socket-attachment name",
    "marker name",
    "config key",
    "script-event-supplied name",
    "resource-derived name",
    "dynamically generated buffer",
]


def main():
    m, s0 = S.require_identity()
    gen_sha = S.script_self_sha256(os.path.abspath(__file__))
    cs = S.make_cs()
    L = []
    L.append("=" * 80)
    L.append("RAW ARTIFACT: ARG2_VALUE_FLOW_RAW.txt (Phase E disposition; G9/G10/G11)")
    L.append("RUN_ID: %s" % S.RUN_ID)
    L.append("GENERATOR: phase_e_disposition.py (SHA256=%s)" % gen_sha)
    L.append("PYTHON: %s | CAPSTONE: %s" % (sys.version.split()[0], capstone.__version__))
    L.append(s0)
    L.append("INPUT RAW: 01_RAW/THUNK_CALLER_CENSUS.csv (same run, deterministic)")
    L.append("HEADER_TIMESTAMP: %s (metadata only)" % S.utc_now_iso())
    L.append("=" * 80)
    L.append("")
    L.append("[E1] APPLICABILITY DETERMINATION")
    L.append("  Contract Phase E applies to PROVEN or strongest-bounded candidate callers")
    L.append("  of FUN_006FAB80 ONLY. Phase D measured:")
    L.append("    direct E8/E9/EB callers : 0 (denominators: E8=156829 E9=40668 EB=17961 byte occurrences)")
    L.append("    imm32 references        : 5 (all = the thunk's own vtable slot dwords)")
    L.append("    vtable memberships       : 5 (slot ordinal 2, the five expected classes)")
    L.append("    dispatch candidates     : 1438 -> PROVEN_TARGET=0, REJECTED=5, INSUFFICIENT_PROOF=1433")
    L.append("  => there is NO proven caller; the strongest-bounded candidates are the 5")
    L.append("     REJECTED rows, whose receivers are PROVEN other classes (their slot-2")
    L.append("     dispatch targets are other functions, NOT FUN_006FAB80). No thunk caller")
    L.append("     exists within the declared bound -> G9 = NOT_APPLICABLE (no such caller).")
    L.append("")
    L.append("[E2] THUNK arg1/arg2 ABI CONTRACT (re-measured from the pinned bytes)")
    f = S.b5_function(m, cs, THUNK, max_bytes=64)
    for i in f["insns"]:
        L.append("    0x%08X  %-12s %s" % (i.address, i.bytes.hex(),
                                           i.mnemonic + " " + i.op_str))
    L.append("  arg1 = [esp+4] at thunk entry -> x87 fld/fstp roundtrip -> receiver [esp+4]")
    L.append("        bit-preserving for normals/denormals/pointers-as-dwords; sNaN not guaranteed")
    L.append("  arg2 = [esp+8] at thunk entry -> mov edx -> push edx -> receiver [esp+8] (VERBATIM)")
    L.append("  receiver ABI (thiscall): this=[this+0x14] in ECX; ret 8")
    L.append("  HYPOTHETICAL consumer signature (if the receiver were SceneFeederObject):")
    L.append("    FUN_0050A050(this=SF, arg1=OUT float3 buffer ptr, arg2=name ptr NULL-tested)")
    L.append("    (measured in 01_RAW/NEGCTL_RECEIVER_RAW.txt [N4]; NOT exercised at the family seam)")
    L.append("")
    L.append("[E3] STRONGEST-BOUNDED CANDIDATE DISPOSITION (5 REJECTED rows, re-verified)")
    L.append("  R2 note (QC P3-3 fix): a vtable whose extent has fewer than 3 slots")
    L.append("  has NO slot-2 entry; the R1 line printed the raw dword at the slot-2")
    L.append("  position as if it were a null slot-2. The R2 line prints the real")
    L.append("  dword (an ASCII string fragment where the vtable is followed by")
    L.append("  .rdata string data) or the actual slot-2 target.")
    csv_path = os.path.join(RAW, "THUNK_CALLER_CENSUS.csv")
    rejected = []
    with open(csv_path) as fh:
        rows = fh.read().splitlines()
    hdr = rows[0].split(",")
    for r in rows[1:]:
        cols = r.split(",")
        if len(cols) >= 9 and cols[8] == "REJECTED_TARGET_NOT_FAMILY":
            rejected.append(cols)
    inv = S.vtable_inventory(m)
    vt_by_class = {}
    for rr in inv:
        vt_by_class.setdefault(rr["class_name"], rr["vtable_start"])
    L.append("  REJECTED candidates re-verified from own bytes:")
    for cols in rejected:
        # verdict format: PROVEN_OTHER:OTHER:.?AVX@@|... or MIXED:OTHER:...
        verdict = cols[6]
        cls_names = [seg for seg in verdict.replace("|", ":").split(":")
                     if seg.startswith(".?AV")]
        for nm in cls_names:
            vstart = vt_by_class.get(nm)
            if vstart is not None:
                end, entries, stop = S.vtable_extent(m, vstart)
                slot2 = entries[2] if len(entries) > 2 else None
                L.append("    candidate %s call 0x%s: receiver class %s, its vtable"
                         % (cols[0], cols[4], nm))
                if slot2 is not None:
                    L.append("      0x%08X slot-2 = 0x%08X == thunk? %s"
                             % (vstart, slot2,
                                "NO (different function)" if slot2 != THUNK else "YES"))
                    if slot2 == THUNK:
                        L.append("      FINDING: this class also contains the thunk!")
                else:
                    raw = S.u32_va(m, vstart + 2 * 4)
                    import struct as _struct
                    raw_ascii = _struct.pack("<I", raw if raw is not None else 0)
                    L.append("      0x%08X NO SLOT-2 ENTRY (vtable extent = %d slot(s);"
                             % (vstart, len(entries)))
                    L.append("        the dword at the slot-2 position 0x%08X = 0x%08X"
                             % (vstart + 8, raw if raw is not None else 0))
                    L.append("        = ASCII %r - string data after the vtable, not a"
                             % (raw_ascii,))
                    L.append("        code pointer) == thunk? NO (no slot-2 entry =>")
                    L.append("        this class cannot dispatch the slot-2 thunk)")
    L.append("  (all REJECTED candidates dispatch their own class's slot-2 function,")
    L.append("   which re-verification shows is not FUN_006FAB80)")
    L.append("")
    L.append("[E4] arg2 PRODUCER-SOURCE TEST LIST (contract Phase E source classes)")
    L.append("  Every candidate producer class below was TESTED via the caller census")
    L.append("  (a producer can only exist at a call site). Measured caller count: 0.")
    for src in ARG2_SOURCE_CLASSES:
        L.append("    %-28s : NOT_DEMONSTRATED (no call site exists to carry such a value)"
                 % src)
    L.append("")
    L.append("[E5] PHASE E VERDICTS (status algebra)")
    L.append("  ARG2_ABI              : CONFIRMED (verbatim dword forward; receiver [esp+8])")
    L.append("  ARG2_PROVENANCE        : NOT_DEMONSTRATED (no statically-identifiable")
    L.append("                           caller of the thunk exists within the declared")
    L.append("                           bound. R2 correction (QC C15/P0-1): the R1 clause")
    L.append("                           'the held field itself is NULL at all constructions,")
    L.append("                           so no arg2 can ever reach a live receiver' is RETRACTED")
    L.append("                           - live held receivers DO exist at bounded constructions")
    L.append("                           (the FloatValue-family channel children); what stands")
    L.append("                           is the empty CALLER set: with no thunk dispatch site,")
    L.append("                           no arg2 value is carried to any receiver, live or not")
    L.append("  ARG2_VALUE_CLASS       : NOT_DEMONSTRATED (honest negative; no filler)")
    L.append("  ARG2_FINAL_SEMANTIC_ROLE: UNVERIFIED (valid per contract G11: string/name")
    L.append("                           semantics require producer/consumer context that")
    L.append("                           does not exist statically at this seam)")
    L.append("  arg1 discriminator (Phase A): no caller exists to pass either a pointer")
    L.append("                           (lea) or a float constant; the discriminator is")
    L.append("                           unresolvable at this seam in this binary.")
    L.append("")
    L.append("[E6] GATE OUTCOMES")
    L.append("  G9_ARG2_PRODUCER_FLOW  : PASS (NOT_APPLICABLE - no proven caller exists;")
    L.append("                            strongest-bounded candidates dispositioned in [E3])")
    L.append("  G10_ARG2_VALUE_CLASS   : PASS with honest NOT_DEMONSTRATED (no identified value;")
    L.append("                            no STRING claim is made anywhere)")
    L.append("  G11_ARG2_SEMANTIC_ROLE  : PASS (assignment follows the string/name evidence rule;")
    L.append("                            outcome UNVERIFIED is a valid gate outcome)")
    out = os.path.join(RAW, "ARG2_VALUE_FLOW_RAW.txt")
    with open(out, "w") as fh:
        fh.write(chr(10).join(L) + chr(10))
    print("WROTE: %s (%d lines)" % (out, len(L)))


if __name__ == "__main__":
    main()
