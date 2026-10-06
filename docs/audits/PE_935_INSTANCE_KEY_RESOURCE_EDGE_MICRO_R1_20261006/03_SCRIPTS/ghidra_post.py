# ghidra_post.py - Ghidra 11.2.1 headless postscript for
# PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006.
# Independent-tool verification of:
#   - the getter function identity/boundary at 0x00414130
#   - the instruction-start status of each raw E8 census candidate
#   - all references to 0x00414130 (Ghidra's own reference graph)
#   - decompilation of the budgeted functions (bounded micro-run)
# Writes JSON + text to the given output dir. Read-only analysis of a
# sandbox COPY of the pinned EXE; no original file is touched.

import json
import os

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT_DIR = r"C:\Users\User\AppData\Local\Temp\opencode\PE935K_GHIDRA\out"

af = currentProgram.getAddressFactory()
listing = currentProgram.getListing()
rm = currentProgram.getReferenceManager()
fm = currentProgram.getFunctionManager()
monitor = ConsoleTaskMonitor()

getter = af.getAddress("0x00414130")
candidates = ["0x004569D3", "0x00456BEB", "0x0045723E", "0x0045A08B",
              "0x00528FD9", "0x008561AC"]

decompile_funcs = ["0x00414130", "0x00528E50", "0x005247C0", "0x00509330",
                   "0x00856190"]

result = {"measurement": "Ghidra 11.2.1 independent verification",
          "program": currentProgram.getName(),
          "language": str(currentProgram.getLanguageID()),
          "image_base": str(currentProgram.getImageBase()),
          "getter": {}, "candidates": [], "references_to_getter": [],
          "decompiles": {}}

# --- getter identity ---
inst = listing.getInstructionAt(getter)
f = fm.getFunctionAt(getter)
g = {"instruction_at_exact_address": str(inst) if inst else None,
     "mnemonic": inst.getMnemonicString() if inst else None,
     "bytes": str(inst.getBytes()) if inst else None,
     "function_at": str(f) if f else None,
     "function_body": str(f.getBody()) if f else None}
result["getter"] = g

# --- candidates: instruction-start verification ---
for cs in candidates:
    a = af.getAddress(cs)
    inst_at = listing.getInstructionAt(a)
    inst_containing = listing.getInstructionContaining(a)
    entry = {"candidate_va": cs}
    if inst_at is not None:
        fn = fm.getFunctionContaining(a)
        entry["instruction_start"] = "PROVEN_EXACT"
        entry["mnemonic"] = inst_at.getMnemonicString()
        entry["bytes_hex"] = " ".join("%02X" % (b & 0xFF) for b in inst_at.getBytes())
        entry["flow_type"] = str(inst_at.getFlowType())
        entry["containing_function"] = str(fn) if fn else None
        entry["function_entry"] = ("0x%08X" % fn.getEntryPoint().getOffset()) if fn else None
        # if it is a CALL, get its primary called target from the flow
        refs = inst_at.getFlows()
        entry["flow_targets"] = ["0x%08X" % r.getOffset() for r in refs]
        # references FROM this instruction
        irefs = rm.getReferencesFrom(a)
        entry["references_from"] = [{"type": str(r.getReferenceType()),
                                     "to": "0x%08X" % r.getToAddress().getOffset()} for r in irefs]
    elif inst_containing is not None:
        entry["instruction_start"] = "REFUTED_MID_INSTRUCTION"
        entry["containing_instruction"] = str(inst_containing)
        entry["containing_instruction_start"] = "0x%08X" % inst_containing.getAddress().getOffset()
        entry["containing_instruction_bytes_hex"] = " ".join(
            "%02X" % (b & 0xFF) for b in inst_containing.getBytes())
    else:
        entry["instruction_start"] = "UNDEFINED_REGION"
    result["candidates"].append(entry)

# --- all references to the getter ---
for ref in rm.getReferencesTo(getter):
    fra = ref.getFromAddress()
    finst = listing.getInstructionAt(fra)
    fnc = fm.getFunctionContaining(fra)
    result["references_to_getter"].append({
        "from": "0x%08X" % fra.getOffset(),
        "type": str(ref.getReferenceType()),
        "is_call": ref.getReferenceType().isCall(),
        "instruction": str(finst) if finst else None,
        "function": str(fnc) if fnc else None,
    })

# --- bounded decompiles ---
di = DecompInterface()
di.openProgram(currentProgram)
for fva in decompile_funcs:
    a = af.getAddress(fva)
    fn = fm.getFunctionAt(a)
    if fn is None:
        fn = fm.getFunctionContaining(a)
    if fn is None:
        result["decompiles"][fva] = "NO_FUNCTION"
        continue
    res = di.decompileFunction(fn, 120, monitor)
    if res.decompileCompleted():
        result["decompiles"][fva] = res.getDecompiledFunction().getC()
    else:
        result["decompiles"][fva] = "DECOMPILE_FAILED: %s" % res.getErrorMessage()

# --- disassembly windows (bounded) ---
windows = {
    "W_00414130_getter": ("0x00414120", 32),
    "W_004569D3_newcand": ("0x00456993", 96),
    "W_00456BEB_newcand": ("0x00456BAB", 96),
    "W_0045723E_newcand": ("0x004571FE", 96),
    "W_0045A08B_newcand": ("0x0045A04B", 96),
    "W_00528F60_ctor": ("0x00528F60", 192),
    "W_00856170_insert": ("0x00856170", 128),
}
disasm = {}
for name, (sva, size) in windows.items():
    a = af.getAddress(sva)
    lines = []
    it = listing.getInstructions(a, True)
    count = 0
    for ins in it:
        s = ins.getAddress().getOffset()
        if s > a.getOffset() + size:
            break
        b = " ".join("%02X" % (x & 0xFF) for x in ins.getBytes())
        lines.append("0x%08X  %-24s  %s %s" % (s, b, ins.getMnemonicString(),
                                                str(ins)))
        count += 1
        if count > 80:
            break
    disasm[name] = lines
result["disassembly_windows"] = disasm

if not os.path.isdir(OUT_DIR):
    os.makedirs(OUT_DIR)
with open(os.path.join(OUT_DIR, "GHIDRA_VERIFY.json"), "w") as f:
    json.dump(result, f, indent=1)
with open(os.path.join(OUT_DIR, "GHIDRA_DISASM_WINDOWS.txt"), "w") as f:
    for name, lines in disasm.items():
        f.write("=== %s ===\n" % name)
        for ln in lines:
            f.write(ln + "\n")
        f.write("\n")
with open(os.path.join(OUT_DIR, "GHIDRA_DECOMPILES.txt"), "w") as f:
    for fva, src in result["decompiles"].items():
        f.write("=== %s ===\n%s\n\n" % (fva, src))
print("PE935K postscript done -> %s" % OUT_DIR)
