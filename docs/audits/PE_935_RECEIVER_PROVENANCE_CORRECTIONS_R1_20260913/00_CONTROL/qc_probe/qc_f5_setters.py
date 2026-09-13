# -*- coding: utf-8 -*-
# QC F5: independent verification of function-start attributions + setter usage
# classification. My own byte-level methods:
#  (a) prologue check at disputed starts (0x004475A0 vs 0x00447630; 0x004C46C0 vs
#      0x004C47F0; 0x0046E640 vs 0x0046E790; boundary 0x00567170/0x00567770),
#  (b) own scan of each of the 24 ctor-caller function bodies for calls to the
#      4 record setters (f60/f90/fb0/fd0),
#  (c) own scan of the 15 f90-caller functions for attr-function calls
#      (0x0085B840/0x00843D60/0x008544D0/0x00844020/0x00846840/0x00854720) and
#      singleton getters (0x004143F0/0x004154F0/0x00415570).
# pe-master-auditor INTERNAL_QC. STATIC-ONLY.
import struct, sys, json
sys.path.insert(0, r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\00_CONTROL\qc_probe")
from qc_core import Bin, save_json

b = Bin(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe")
R = {}

# --- (a) disputed function starts: prologue check ---
starts = {
    "A_0x004475A0": 0x004475A0, "B_0x00447630": 0x00447630,
    "C_0x004C46C0": 0x004C46C0, "D_0x004C47F0": 0x004C47F0,
    "E_0x0046E640": 0x0046E640, "F_0x0046E790": 0x0046E790,
    "G_0x00567170": 0x00567170, "H_0x00567770": 0x00567770,
}
R["disputed_starts"] = {k: dict(dump=b.hexd(v, 32)) for k, v in starts.items()}
# what is at 0x0056776x (boundary)?
R["boundary_0056770_00567770"] = b.hexd(0x00567740, 0x40)

def calls_in_range(lo, hi, targets):
    res = {t: [] for t in targets}
    o = lo
    while o < hi - 5:
        if b.rd(o, 1) == b"\xE8":
            rel = struct.unpack_from("<i", b.rd(o + 1, 4), 0)[0]
            tgt = o + 5 + rel
            if tgt in res:
                res[tgt].append(o)
        o += 1
    return res

SETTERS = [0x00730F60, 0x00730F90, 0x00730FB0, 0x00730FD0]
ATTRS = [0x0085B840, 0x00843D60, 0x008544D0, 0x00844020, 0x00846840, 0x00854720]
SINGLETONS = [0x004143F0, 0x004154F0, 0x00415570]

# --- (b) 24 ctor-caller functions: setter usage ---
ctor_funcs = {
    0x00456770: [0x004567BC], 0x00457C00: [0x00457C2A], 0x00457E30: [0x00457E76],
    0x0046AA90: [0x0046AAE3], 0x004B9960: [0x004B9A7D], 0x004C5BD0: [0x004C5BFB],
    0x004E3B70: [0x004E3C60], 0x004FF620: [0x004FF93C], 0x0050BAF0: [0x0050BB1C],
    0x0050C0C0: [0x0050C147], 0x0050CC70: [0x0050D1FC], 0x0050D480: [0x0050D730],
    0x0050E490: [0x0050F098, 0x0050F5C8], 0x0050FCF0: [0x0050FD39],
    0x005106A0: [0x005106D1], 0x00511070: [0x005110DA], 0x006C8000: [0x006C8065],
    0x006C80C0: [0x006C812D], 0x0072FA30: [0x0072FB8E],
    0x00447630: [0x0044A19E, 0x0044AAA4], 0x00459270: [0x0045929D],
    0x00567770: [0x00567891], 0x0067BC90: [0x0067BCD9], 0x0067CCD0: [0x0067CD19],
}
def next_start(va):
    o = b.va2off(va)
    end = o
    while end + 3 < b.size:
        if b.raw[end] == 0xCC and b.raw[end+1] == 0xCC and b.raw[end+2] == 0xCC:
            break
        end += 1
    return b.off2va(end)

R["ctor_caller_setter_usage"] = {}
with_setters = []
without = []
for f, sites in ctor_funcs.items():
    # function end: next CC CC CC run (my own boundary walk)
    end_va = next_start(f)
    calls = calls_in_range(f, end_va, SETTERS)
    n = sum(len(v) for v in calls.values())
    R["ctor_caller_setter_usage"][hex(f)] = dict(my_end=hex(end_va), n_setter_calls=n,
                                                 by_setter={hex(t): [hex(x) for x in v] for t, v in calls.items() if v})
    (with_setters if n else without).append(hex(f))
R["ctor_callers_summary"] = dict(funcs=len(ctor_funcs), with_setters=sorted(with_setters),
                                 without_setters=sorted(without), n_without=len(without))

# --- (c) 15 f90-caller functions: attr/singleton calls ---
f90_funcs = {
    0x0050BED0: [0x0050BFEF], 0x00457CD0: [0x00457D67], 0x00459270: [0x004592EC],
    0x00442190: [0x00442298], 0x00567770: [0x00567906], 0x00567170: [0x0056739B],
    0x00447630: [0x0044AAFD], 0x004B3A00: [0x004B3B26], 0x0043A200: [0x0043A253],
    0x004C47F0: [0x004C48F4], 0x0046E790: [0x0046E7E1], 0x00488920: [0x00488958],
    0x005B5F90: [0x005B601A], 0x0067BC90: [0x0067BD0E], 0x0067CCD0: [0x0067CD4E],
}
R["f90_caller_classification"] = {}
for f, sites in f90_funcs.items():
    end_va = next_start(f)
    a = calls_in_range(f, end_va, ATTRS)
    s = calls_in_range(f, end_va, SINGLETONS)
    na = sum(len(v) for v in a.values())
    ns = sum(len(v) for v in s.values())
    R["f90_caller_classification"][hex(f)] = dict(
        my_end=hex(end_va), n_attr_calls=na, n_singleton_calls=ns,
        attr_calls={hex(t): [hex(x) for x in v] for t, v in a.items() if v},
        singleton_calls={hex(t): [hex(x) for x in v] for t, v in s.items() if v})

# --- verify the 2-site functions are real (both ctor sites inside one body) ---
R["two_site_funcs"] = {}
for f in (0x00447630, 0x0050E490):
    end_va = next_start(f)
    R["two_site_funcs"][hex(f)] = dict(start=hex(f), my_end=hex(end_va),
                                       ctor_sites=[hex(s) for s in ctor_funcs[f]],
                                       inside=all(f <= s < end_va for s in ctor_funcs[f]))

p = save_json("QC_F5_SETTERS.json", R)
print("saved", p)
print("ctor-callers: funcs", R["ctor_callers_summary"]["funcs"], "with", len(R["ctor_callers_summary"]["with_setters"]), "without", R["ctor_callers_summary"]["n_without"])
print("with_setters:", R["ctor_callers_summary"]["with_setters"])
print()
for f, v in R["f90_caller_classification"].items():
    print(f, "end", v["my_end"], "attr", v["n_attr_calls"], v["attr_calls"], "| singl", v["n_singleton_calls"], v["singleton_calls"])
print()
print("two-site:", json.dumps(R["two_site_funcs"], indent=1))
