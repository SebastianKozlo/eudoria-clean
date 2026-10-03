#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S6 CURATE G3 — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
Curates the LOCAL-ONLY Ghidra scratch dump g3_falsifier_path.json into the repo
package: 01_RAW/G3_FALSIFIER_PATH.json + 01_RAW/G3_DECOMPILE_<label>_<va>.c,
and prints the decompiles/listings for immediate analysis.

Interpreter: python 3.12.10. Invoke: python 03_SCRIPTS/s6_curate_g3.py
"""

import json
import os

RUN_ID = "PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003"
HERE = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.normpath(os.path.join(HERE, "..", "01_RAW"))
G3 = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003\g3_falsifier_path.json"


def main():
    with open(G3, "r") as f:
        g3 = json.load(f)
    os.makedirs(RAWDIR, exist_ok=True)
    dump = {
        "run_id": RUN_ID,
        "stage": "G3_curated_falsifier_path",
        "source": {
            "ghidra": "11.2.1 PUBLIC (analyzeHeadless; fresh project LANDMARK4057)",
            "target": "sandbox copy of D:\\Eudoria_Reconstruction\\pcg_install\\Entropia.exe (SHA256 E7785430... pinned)",
            "postscript": "03_SCRIPTS/g3_falsifier_path.py (hash in 03_SCRIPTS/SCRIPT_SHA256.csv)",
            "byte_integrity": "same Ghidra bytes pipeline as the 951/951-verified g1 listing (01_RAW/RAW_BYTE_PINS.json method)",
        },
        "measured": g3.get("measured", {}),
        "errors": g3.get("errors", []),
    }
    with open(os.path.join(RAWDIR, "G3_FALSIFIER_PATH.json"), "w", encoding="utf-8") as f:
        json.dump(dump, f, indent=2)

    fns = g3.get("measured", {}).get("functions", {})
    for label, d in sorted(fns.items()):
        va = d.get("entry", d.get("va", "0")).replace("0x", "")
        name = "G3_DECOMPILE_%s_%s.c" % (label, va)
        with open(os.path.join(RAWDIR, name), "w", encoding="utf-8") as f:
            f.write("// %s decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)\n" % label)
            f.write("// listing + callers + callees: 01_RAW/G3_FALSIFIER_PATH.json\n")
            f.write((d.get("decompile_c") or "") if d.get("decompile_ok") else
                    "// decompile failed: %s\n" % d.get("decompile_error"))
        print("=" * 100)
        print("### %s @%s size=%s cc=%s signature=%s" % (label, d.get("entry"), d.get("size_bytes"),
                                                        d.get("calling_convention"), d.get("signature")))
        print("params:", d.get("parameters"))
        print("callers_count:", d.get("caller_call_sites_count"),
              "first60:", d.get("caller_call_sites_first60"))
        print("callee_targets:", d.get("callee_targets"))
        print("--- listing ---")
        for i in d.get("listing", []):
            print("%s  %-22s %s" % (i["addr"], i["bytes"], i["text"]))
        if d.get("decompile_ok"):
            print("--- decompile ---")
            print(d.get("decompile_c"))
        print()


if __name__ == "__main__":
    main()
