# Jython script for Ghidra 11.2.1 headless (RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002)
# Pass 15 (S5 CONSUMER CENSUS): for EVERY caller of FUN_0070c180 (the tag->descriptor
# lookup, 202 callsites), capture the preceding instructions to detect the tag argument;
# classify sites that use the immediate tag 0x11 (17). Also scan the whole .text for the
# pattern 'imm 0x11 followed by call into the accessor family' and for direct accesses
# of value_array + 0x54 (21*4) after a [reg+0x40] load.
# @category PE_935_20002
import json
import os
from ghidra.util.task import ConsoleTaskMonitor

OUT_DIR = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002\01_RAW\GHIDRA_ROUTING"
if not os.path.isdir(OUT_DIR):
    os.makedirs(OUT_DIR)

monitor = ConsoleTaskMonitor()
program = currentProgram
fm = program.getFunctionManager()
listing = program.getListing()
rm = program.getReferenceManager()

result = {"run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
          "generator": "03_SCRIPTS/s3_ghidra_routing_pass15.py"}

def addr(v):
    return program.getAddressFactory().getAddress("0x%X" % v)

sites = []
for ref in rm.getReferencesTo(addr(0x70C180)):
    if not ref.getReferenceType().isCall():
        continue
    from_a = ref.getFromAddress()
    cf = fm.getFunctionContaining(from_a)
    ctx = []
    prev = from_a.subtract(0x20)
    it = listing.getInstructions(prev, True)
    for ins in it:
        if ins.getAddress().getOffset() > from_a.getOffset():
            break
        ctx.append("%s %s" % (ins.getAddress().toString(), ins.toString()))
    sites.append({
        "call_site": "0x%X" % from_a.getOffset(),
        "caller": cf.getName() if cf else None,
        "caller_entry": "0x%X" % cf.getEntryPoint().getOffset() if cf else None,
        "ctx": ctx[-10:],
    })

result["callsites_total"] = len(sites)
# classify: tag-0x11 candidates = '0x11' appears in the last 10 instructions before the call
tag11 = []
for s in sites:
    joined = " ; ".join(s["ctx"])
    if ("0x11" in joined) or ("PUSH 0x11" in joined) or (",0x11" in joined.replace(" ", "")):
        # verify it looks like an immediate 0x11 (not 0x110 / 0x11xx)
        import re
        hits = re.findall(r"(?:PUSH|MOV|MOVZX|CMP)[^;]*?0x11\b", joined)
        if hits:
            s["tag11_hits"] = hits
            tag11.append(s)
result["tag11_candidate_sites"] = [{"call_site": s["call_site"], "caller": s["caller"],
                                    "caller_entry": s["caller_entry"], "ctx": s["ctx"],
                                    "tag11_hits": s["tag11_hits"]} for s in tag11]
result["all_sites"] = sites

with open(os.path.join(OUT_DIR, "PASS15_GHIDRA_DUMP.json"), "w") as fh:
    json.dump(result, fh, indent=1)
print("S5 CENSUS PASS15 DONE: total=%d tag11_candidates=%d" % (len(sites), len(tag11)))
