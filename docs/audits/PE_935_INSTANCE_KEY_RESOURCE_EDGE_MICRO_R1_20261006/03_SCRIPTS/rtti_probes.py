# rtti_probes.py - bounded MSVC RTTI chain probes (data identity probes, not
# function analysis). CALIBRATION FIRST (fail-closed): the walker must reproduce
# the BASE-canon SceneFeederObject + ClientMovableObject + MovableObject names
# from their vtables before any new probe is trusted.
# Probes (this run, bounded):
#   0x00A7D458  SceneFeederObject vtable   (calibration, BASE canon)
#   0x00A7DCB0  ClientMovableObject vtable (calibration, BASE canon)
#   0x00A91E4C  MovableObject vtable       (calibration, BASE canon)
#   0x00A79F18  vtable stored by FUN_004157B0 (the 0x88-B singleton ctor)  [receiver classification]
#   0x00A83274  vtable stored by FUN_0064B1E0 (the 0x14-B key-carrying obj) [non-canonical lead probe]
#   0x00A7D444  third arg of FUN_007B6A80 registration in the SF ctor tail  [probe - expected NOT a class vtable]

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe935k_core import Exe

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "01_RAW")
os.makedirs(OUT, exist_ok=True)

ex = Exe()

def rtti_name(vtable_va):
    """MSVC RTTI walk: [vt-4]=COL, [COL+0xC]=TD, name=TD+8 (null-terminated)."""
    col = ex.u32(vtable_va - 4)
    if col is None or col == 0:
        return {"ok": False, "reason": "no COL pointer at vt-4"}
    td = ex.u32(col + 0xC)
    if td is None or td == 0:
        return {"ok": False, "reason": "no TD pointer at COL+0xC", "col": "0x%08X" % col}
    off = ex.va_to_off(td)
    if off is None:
        return {"ok": False, "reason": "TD not file-backed", "col": "0x%08X" % col, "td": "0x%08X" % td}
    raw = ex.raw[off + 8:off + 8 + 96]
    name = raw.split(b"\x00")[0]
    printable = all(32 <= c < 127 for c in name) and len(name) > 0
    if not printable:
        return {"ok": False, "reason": "TD name not printable ASCII", "col": "0x%08X" % col,
                "td": "0x%08X" % td}
    return {"ok": True, "col": "0x%08X" % col, "td": "0x%08X" % td,
            "name": name.decode("ascii")}

CALIBRATION = [
    (0x00A7D458, ".?AVSceneFeederObject@@"),
    (0x00A7DCB0, ".?AVClientMovableObject@@"),
    (0x00A91E4C, ".?AVMovableObject@@"),
]
PROBES = [
    (0x00A79F18, "vtable stored by FUN_004157B0 (0x88-B singleton ctor at [0x00B9FE5C])"),
    (0x00A83274, "vtable stored by FUN_0064B1E0 (0x14-B key-carrying object, key at +0x10)"),
    (0x00A7D444, "third stack arg of the FUN_007B6A80 registration call in FUN_00509330 tail"),
]

results = {"calibration": [], "probes": [], "calibration_passed": False}
cal_ok = True
for vt, expect in CALIBRATION:
    r = rtti_name(vt)
    entry = {"vtable": "0x%08X" % vt, "expected": expect,
             "walk": r if r.get("ok") else r, "match": bool(r.get("ok") and r.get("name") == expect)}
    results["calibration"].append(entry)
    if not entry["match"]:
        cal_ok = False
results["calibration_passed"] = cal_ok

if not cal_ok:
    results["probes"] = "SKIPPED_FAIL_CLOSED (calibration did not pass)"
else:
    for vt, why in PROBES:
        r = rtti_name(vt)
        r["probe_why"] = why
        r["vtable"] = "0x%08X" % vt
        results["probes"].append(r)

with open(os.path.join(OUT, "RTTI_PROBES.json"), "w") as f:
    json.dump(results, f, indent=1)

print("CALIBRATION PASSED:", cal_ok)
for e in results["calibration"]:
    print("  vt %s -> %s (match=%s)" % (e["vtable"], e["walk"].get("name"), e["match"]))
for p in results["probes"]:
    print("PROBE vt %s (%s):" % (p.get("vtable"), p.get("probe_why")))
    if p.get("ok"):
        print("   COL=%s TD=%s NAME=%r" % (p["col"], p["td"], p["name"]))
    else:
        print("   NOT-A-CLASS-VTABLE: %s (col=%s td=%s)" % (
            p.get("reason"), p.get("col"), p.get("td")))
