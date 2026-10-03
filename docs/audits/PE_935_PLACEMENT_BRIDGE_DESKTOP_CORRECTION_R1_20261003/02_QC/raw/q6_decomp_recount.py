#!/usr/bin/env python
"""QC-F6 decompilation recount (targeted QC, order ss8A).

Independent machine recount of the historical run's decompilation records:
  - iterate historical 01_RAW/C*.json
  - for each file, take measured.decompilations (if present)
  - count records per file
  - extract each record's function entry by THREE routes and cross-check:
      (a) the record's function_entry / va field
      (b) trailing hex address in the record KEY
      (c) first FUN_xxxxxxxx token in the decompiled 'c' code (the function's
          own definition signature)
  - compute UNIQUE_FUNCTION_ENTRY across the whole C*.json set
  - list duplicate entries (entry -> [(file, key), ...])
No file is modified; the store is read as bytes only.
"""
import json
import re
import os
import sys

RAW = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
       r"\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z\01_RAW")

def norm(va):
    if va is None:
        return None
    s = str(va).strip().lower()
    if s.startswith("0x"):
        s = s[2:]
    s = s.lstrip("0")
    return s if s else "0"

def entry_from_code(c):
    if not c:
        return None
    m = re.search(r"FUN_([0-9a-fA-F]{6,8})", c)
    return norm("0x" + m.group(1)) if m else None

def entry_from_key(k):
    m = re.search(r"([0-9a-fA-F]{6,8})$", k)
    return norm("0x" + m.group(1)) if m else None

def main():
    files = sorted(f for f in os.listdir(RAW) if f.upper().startswith("C")
                   and f.lower().endswith(".json"))
    total = 0
    per_file = {}
    entries = {}
    route_mismatch = []
    for fn in files:
        path = os.path.join(RAW, fn)
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            try:
                doc = json.load(fh)
            except Exception as e:
                print("PARSE_FAIL %s: %s" % (fn, e))
                continue
        dec = None
        if isinstance(doc, dict):
            m = doc.get("measured")
            if isinstance(m, dict):
                dec = m.get("decompilations")
        if dec is None:
            per_file[fn] = 0
            continue
        per_file[fn] = len(dec)
        total += len(dec)
        for key, rec in dec.items():
            if not isinstance(rec, dict):
                continue
            fe_field = norm(rec.get("function_entry") or rec.get("va"))
            fe_key = entry_from_key(key)
            fe_code = entry_from_code(rec.get("c"))
            chosen = fe_field or fe_code or fe_key
            if not (fe_field == fe_code == fe_key) and not (
                    fe_field and fe_code and fe_field == fe_code):
                route_mismatch.append((fn, key, fe_field, fe_key, fe_code))
            entries.setdefault(chosen, []).append((fn, key))
    print("PER-FILE DECOMPILATION RECORDS:")
    for fn in files:
        print("  %s = %s" % (fn, per_file.get(fn, 0)))
    print("TOTAL_RECORDS = %d" % total)
    print("UNIQUE_FUNCTION_ENTRY = %d" % len(entries))
    dups = {e: srcs for e, srcs in entries.items() if len(srcs) > 1}
    print("DUPLICATE_ENTRIES = %d" % len(dups))
    for e, srcs in sorted(dups.items()):
        print("  dup 0x%s: %s" % (e, srcs))
    print("ROUTE_MISMATCHES (field vs key vs code) = %d" % len(route_mismatch))
    for fn, key, a, b, c in route_mismatch[:10]:
        print("  mismatch %s:%s field=%s key=%s code=%s" % (fn, key, a, b, c))

if __name__ == "__main__":
    main()
