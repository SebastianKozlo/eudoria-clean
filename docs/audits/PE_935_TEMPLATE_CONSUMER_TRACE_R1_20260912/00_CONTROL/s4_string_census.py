# -*- coding: utf-8 -*-
# Ghidra headless postScript (Jython) - RUN PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
# STAGE S4: string census in Entropia.exe (EU 9.3.5, pcg_install, SHA E7785430...).
#
# Contract step 1: find occurrences of the VFS/template/model strings and census them with VAs.
# Patterns (case-sensitive unless noted): ArkVFS02, templates, hierarchy, .vfs, .nif, .bvi,
#   models, \models\, plus the path-surface: .tga, .dds, .cfg, .bnt, Parameters, Volumes,
#   Cache, Data\ (variants). Raw memory scan (not only defined strings) so constructed or
#   non-defined instances are caught too.
#
# For every raw hit: VA, memory block (section), defined-data overlap (string value at VA),
# and ALL references TO the hit address (and to the containing string start when different),
# each with containing function + instruction bytes + mnemonic.
#
# Writes: 01_RAW\ghidra_output\S4_STRING_CENSUS.json  (and a compact .csv)
# READ-ONLY on the program. No PE2/2003 addresses used anywhere.

import json
import os
import time
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.program.model.mem import MemoryAccessException  # noqa

try:
    from org.python.core import jarray  # noqa
except:
    pass

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912"
OUT_RAW = os.path.join(RUN_ROOT, "01_RAW", "ghidra_output")
if not os.path.isdir(OUT_RAW):
    os.makedirs(OUT_RAW)

monitor = ConsoleTaskMonitor()
fm = currentProgram.getFunctionManager()
rm = currentProgram.getReferenceManager()
listing = currentProgram.getListing()
mem = currentProgram.getMemory()

EXEC = {
    "run_id": "PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912",
    "phase": "S4_STRING_CENSUS",
    "script": "s4_string_census.py",
    "program": currentProgram.getName(),
    "program_sha256_declared": "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31",
    "started": time.strftime("%Y-%m-%d %H:%M:%S"),
}


def jdump(name, obj):
    p = os.path.join(OUT_RAW, name)
    f = open(p, "w")
    f.write(json.dumps(obj, indent=2))
    f.close()
    return p


def hex_pattern(s):
    return " ".join("%02x" % (ord(c) & 0xFF) for c in s)


PATTERNS = [
    "ArkVFS02",
    "ArkVFS",
    "AVFS",
    "templates",
    "Templates",
    "hierarchy",
    "Hierarchy",
    ".vfs",
    ".nif",
    ".bvi",
    "models",
    "Models",
    "\\models\\",
    ".tga",
    ".dds",
    ".cfg",
    ".bnt",
    "Parameters",
    "Volumes",
    "Cache",
    "Data\\",
]

mem_start = None
mem_end = None
for b in mem.getBlocks():
    if mem_start is None or b.getStart().getOffset() < mem_start:
        mem_start = b.getStart().getOffset()
    if mem_end is None or b.getEnd().getOffset() > mem_end:
        mem_end = b.getEnd().getOffset()

census = {}
hits_total = 0

for pat in PATTERNS:
    needle = hex_pattern(pat)
    found = []
    cur = mem_start
    limit = 2000  # safety cap per pattern
    while len(found) < limit:
        hit = None
        try:
            hit = mem.findBytes(toAddr(cur), toAddr(mem_end), needle, True, monitor)
        except:
            break
        if hit is None:
            break
        va = hit.getOffset()
        found.append(va)
        cur = va + 1
    recs = []
    for va in found[:200]:  # per-hit detail cap for very frequent patterns
        blk = mem.getBlock(toAddr(va))
        d = listing.getDataAt(toAddr(va))
        # widen to the containing defined data object if any
        d_cont = listing.getDataContaining(toAddr(va))
        val = None
        dtype = None
        dstart = None
        if d_cont is not None and d_cont.hasStringValue():
            try:
                val = d_cont.getValue()
            except:
                val = None
            dtype = str(d_cont.getDataType())
            dstart = d_cont.getAddress().getOffset()
        # references to THIS va
        refs = rm.getReferencesTo(toAddr(va))
        ref_list = []
        for r in refs:
            fa = r.getFromAddress()
            fn = fm.getFunctionContaining(fa)
            inst = listing.getInstructionAt(fa)
            if inst is None:
                inst = listing.getInstructionContaining(fa)
            ib = None
            mn = None
            if inst is not None:
                try:
                    bts = inst.getBytes()
                    ib = " ".join("%02x" % (x & 0xFF) for x in bts)
                except:
                    ib = None
                mn = inst.getMnemonicString()
            ref_list.append({
                "from_va": "0x%08X" % fa.getOffset(),
                "ref_type": str(r.getReferenceType()),
                "in_function": fn.getName() if fn is not None else None,
                "func_entry": ("0x%08X" % fn.getEntryPoint().getOffset()) if fn is not None else None,
                "mnemonic": mn,
                "bytes": ib,
            })
        # references to the containing string START if wider (only if not equal)
        ref_list_start = []
        if dstart is not None and dstart != va:
            refs2 = rm.getReferencesTo(toAddr(dstart))
            for r in refs2:
                fa = r.getFromAddress()
                fn = fm.getFunctionContaining(fa)
                inst = listing.getInstructionAt(fa)
                if inst is None:
                    inst = listing.getInstructionContaining(fa)
                ref_list_start.append({
                    "from_va": "0x%08X" % fa.getOffset(),
                    "ref_type": str(r.getReferenceType()),
                    "in_function": fn.getName() if fn is not None else None,
                    "func_entry": ("0x%08X" % fn.getEntryPoint().getOffset()) if fn is not None else None,
                })
        recs.append({
            "va": "0x%08X" % va,
            "section": blk.getName() if blk is not None else None,
            "defined_string_at": val,
            "defined_type": dtype,
            "defined_string_start": ("0x%08X" % dstart) if dstart is not None else None,
            "refs_to_va": ref_list,
            "refs_to_string_start": ref_list_start,
        })
    census[pat] = {"raw_hit_count": len(found), "hits": recs}
    hits_total += len(found)

EXEC["patterns"] = PATTERNS
EXEC["hits_total"] = hits_total
EXEC["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
jdump("S4_STRING_CENSUS.json", {"census": census, "exec": EXEC})

# compact csv
csvp = os.path.join(OUT_RAW, "S4_STRING_CENSUS.csv")
f = open(csvp, "w")
f.write("pattern,va,section,defined_string_at,refs_to_va_count\n")
for pat, c in census.items():
    for h in c["hits"]:
        f.write("%s,%s,%s,\"%s\",%d\n" % (
            pat, h["va"], h["section"] or "",
            (h["defined_string_at"] or "").replace('"', "'"),
            len(h["refs_to_va"])))
f.close()

print("S4_STRING_CENSUS_DONE hits_total=%d" % hits_total)
for pat in PATTERNS:
    print("  %-12s raw_hits=%d" % (pat, census[pat]["raw_hit_count"]))
