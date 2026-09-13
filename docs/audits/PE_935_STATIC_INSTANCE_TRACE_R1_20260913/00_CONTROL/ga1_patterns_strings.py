# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_STATIC_INSTANCE_TRACE_R1_20260913
# STAGE GA1: Z3 pattern decode + string xrefs (world loaders Z5, viewer strings Z4).
#
# 1) For VAs 0x0053270C, 0x00532769, 0x0083427E: containing function, instruction
#    containing each VA (boundaries!), +/- window disasm with raw bytes, callers.
# 2) IAT resolution for 0x00A75A38/0x00A75A40/0x00A75A5C (imports called near pattern 2).
# 3) Xrefs to key strings: portals.bnt, TerrainEditZones.bnt, .tez, .prt, portals\,
#    TerrainEditZones\, Data\Parameters\, viewer strings (m_worldTranslate...),
#    NetImmerseScene::Root, ArkClientWorldObjectLogic::OnDelayedTextureUpdated,
#    VegetationClimates, hierarchy.vfs, templates.vfs.
# Writes: 01_RAW\ghidra_output\GA1_*.json/txt

import json
import os
import time
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.decompiler import DecompInterface

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913"
OUT_RAW = os.path.join(RUN_ROOT, "01_RAW", "ghidra_output")
if not os.path.isdir(OUT_RAW):
    os.makedirs(OUT_RAW)

monitor = ConsoleTaskMonitor()
fm = currentProgram.getFunctionManager()
listing = currentProgram.getListing()
rm = currentProgram.getReferenceManager()
st = currentProgram.getSymbolTable()

EXEC = {
    "run_id": "PE_935_STATIC_INSTANCE_TRACE_R1_20260913",
    "phase": "GA1_patterns_and_strings",
    "program": currentProgram.getName(),
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}

PATTERN_VAS = [0x0053270C, 0x00532769, 0x0083427E]

STRINGS = [
    ("portals_bnt", 0x00A7A7CC),
    ("TerrainEditZones_bnt", 0x00A7A790),
    ("dot_tez", 0x00A7A71C),
    ("dot_prt", 0x00A7A72C),
    ("portals_dir", 0x00A7A894),
    ("TEZ_dir", 0x00A7A86C),
    ("Data_Parameters", 0x00A97E58),
    ("data_dir", 0x00A797D4),
    ("m_worldTranslate", 0x00A8D864),
    ("m_worldRotate", 0x00A8D854),
    ("m_worldScale", 0x00A8D844),
    ("m_kWorldBound", 0x00A8D834),
    ("NetImmerseScene_Root", 0x00A972FC),
    ("NetImmerseScene_Scene", 0x00A972E3),
    ("CWO_Logic_OnDelayedTextureUpdated", 0x00A7D624),
    ("m_ContainsPortals", 0x00A86334),
    ("m_ContainsPortalDefinitions", 0x00A86348),
    ("VegetationClimates_hint", None),  # found by search
    ("templates_vfs", 0x00A86D30),
    ("hierarchy_vfs_search", None),
]

def bytes_hex(inst):
    try:
        bts = inst.getBytes()
        return " ".join("%02x" % (b & 0xFF) for b in bts)
    except:
        return None

def func_of(va):
    return fm.getFunctionContaining(toAddr(va))

def dump_window(center_va, n_before=8, n_after=8):
    # walk back n_before instructions from the instruction containing center_va
    center_inst = listing.getInstructionContaining(toAddr(center_va))
    if center_inst is None:
        # try exact
        center_inst = listing.getInstructionAt(toAddr(center_va))
    out = []
    if center_inst is None:
        return None, "NO_INSTRUCTION_AT_VA (data or mid-instruction unknown)"
    insts = []
    cur = center_inst
    for _ in range(n_before):
        p = cur.getPrevious()
        if p is None:
            break
        cur = p
    it = cur
    for _ in range(n_before + n_after + 1):
        if it is None:
            break
        insts.append(it)
        it = it.getNext()
    for i in insts:
        mark = " <<<" if i.getAddress().getOffset() == center_va else ""
        out.append("0x%08X  %-30s %-8s %s%s" % (
            i.getAddress().getOffset(), bytes_hex(i) or "",
            i.getMnemonicString(), i.toString().split(None, 1)[-1] if " " in i.toString() else "", mark))
    return center_inst, "\n".join(out)

def callers_of(func):
    if func is None:
        return []
    res = []
    for r in rm.getReferencesTo(func.getEntryPoint()):
        if r.getReferenceType().isCall():
            fa = r.getFromAddress()
            fn = fm.getFunctionContaining(fa)
            res.append({"from_va": "0x%08X" % fa.getOffset(),
                        "in_function": fn.getName() if fn else None,
                        "func_entry": ("0x%08X" % fn.getEntryPoint().getOffset()) if fn else None})
    return res

def decompile(func, max_secs=60):
    if func is None:
        return None
    di = DecompInterface()
    di.openProgram(currentProgram)
    try:
        res = di.decompileFunction(func, max_secs, monitor)
        if res.decompileCompleted():
            return res.getDecompiledFunction().getC()
    except:
        return None
    finally:
        di.dispose()

def main():
    # ---------- 1) patterns ----------
    pat_out = {}
    for va in PATTERN_VAS:
        rec = {}
        inst, window = dump_window(va)
        rec["va"] = "0x%08X" % va
        if inst is not None:
            rec["containing_instruction"] = {
                "va": "0x%08X" % inst.getAddress().getOffset(),
                "bytes": bytes_hex(inst),
                "text": inst.toString(),
                "flow_type": str(inst.getFlowType()),
            }
        else:
            rec["containing_instruction"] = None
            rec["note"] = window
        fn = func_of(va)
        if fn is not None:
            rec["function"] = {"name": fn.getName(),
                               "entry": "0x%08X" % fn.getEntryPoint().getOffset(),
                               "body": "0x%08X-0x%08X" % (fn.getBody().getMinAddress().getOffset(),
                                                          fn.getBody().getMaxAddress().getOffset())}
            rec["callers"] = callers_of(fn)
        pat_out["0x%08X" % va] = rec

    with open(os.path.join(OUT_RAW, "GA1_PATTERNS.json"), "w") as f:
        json.dump({"exec": EXEC, "patterns": pat_out}, f, indent=2)

    # disasm windows file
    with open(os.path.join(OUT_RAW, "GA1_PATTERN_WINDOWS.txt"), "w") as f:
        for va in PATTERN_VAS:
            inst, window = dump_window(va, 10, 12)
            f.write("=== 0x%08X ===\n" % va)
            f.write((window or "none") + "\n\n")
            fn = func_of(va)
            f.write("function: %s\n" % (fn.getName() + " @0x%08X" % fn.getEntryPoint().getOffset()
                                        if fn else "NONE"))
            if fn is not None:
                f.write("callers: %s\n" % json.dumps(callers_of(fn)))
            f.write("decompiled (bounded):\n")
            c = decompile(fn)
            f.write((c or "// decompile failed")[:12000] + "\n\n")

    # ---------- 2) IAT resolution ----------
    iat = {}
    for va in [0x00A75A38, 0x00A75A40, 0x00A75A5C]:
        a = toAddr(va)
        syms = st.getSymbols(a)
        refs = []
        for r in rm.getReferencesTo(a):
            refs.append("0x%08X" % r.getFromAddress().getOffset())
        iat["0x%08X" % va] = {
            "symbols": [s.getName() for s in syms],
            "referenced_from": refs[:20],
        }
    with open(os.path.join(OUT_RAW, "GA1_IAT.json"), "w") as f:
        json.dump(iat, f, indent=2)

    # ---------- 3) string xrefs ----------
    def find_string_va(text):
        # search defined data strings for exact text
        di = listing.getDefinedData(True)
        for d in di:
            v = d.getValue()
            if v is not None and hasattr(v, "toString") and v.toString() == text:
                return d.getAddress().getOffset(), d
        return None, None

    sx = {}
    for label, va in STRINGS:
        rec = {"label": label}
        if va is None:
            fva, d = find_string_va(label.replace("_hint", "").replace("hierarchy_vfs_search", "hierarchy.vfs"))
            rec["found_va"] = ("0x%08X" % fva) if fva else None
        else:
            fva = va
            rec["found_va"] = "0x%08X" % va
        if fva:
            refs = []
            for r in rm.getReferencesTo(toAddr(fva)):
                fa = r.getFromAddress()
                fn = fm.getFunctionContaining(fa)
                refs.append({
                    "from_va": "0x%08X" % fa.getOffset(),
                    "ref_type": str(r.getReferenceType()),
                    "in_function": fn.getName() if fn else None,
                    "func_entry": ("0x%08X" % fn.getEntryPoint().getOffset()) if fn else None,
                })
            rec["refs"] = refs
        sx[label] = rec

    with open(os.path.join(OUT_RAW, "GA1_STRING_XREFS.json"), "w") as f:
        json.dump({"exec": EXEC, "strings": sx}, f, indent=2)

    print("GA1_DONE patterns=3 iat=3 strings=%d" % len(STRINGS))

main()
