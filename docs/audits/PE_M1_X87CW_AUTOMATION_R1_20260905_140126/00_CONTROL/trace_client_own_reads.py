#!/usr/bin/env python3
"""trace_client_own_reads.py — the client's OWN reads: the MindArk registry,
the wd config files, the Data\\ subtree accesses."""
import csv

csv.field_size_limit(10 ** 9)
path = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_AUTOMATION_R1_20260905_140126\04_RUNTIME\live_test\entropia_death_trace.csv"
rows = []
with open(path, encoding="utf-8-sig", errors="replace", newline="") as f:
    r = csv.reader(f)
    hdr = next(r)
    idx = {n: i for i, n in enumerate(hdr)}
    for row in r:
        if len(row) < 5 or "Entropia" not in row[idx["Process Name"]]:
            continue
        rows.append((row[idx["Time of Day"]], row[idx["Operation"]],
                     row[idx["Path"]], row[idx["Result"]],
                     (row[idx["Detail"]] if "Detail" in idx else "")[:60]))

print("=== MINDARK registry accesses ===")
for t, op, p, res, det in rows:
    if "MindArk" in p:
        print(f"{t} | {op:22} | {p[:100]} | {res} | {det}")
print()
print("=== the wd\\ config/data file probes (txt/dat/cfg/ini/xml/log/bat/cache dirs) ===")
for t, op, p, res, det in rows:
    low = p.lower()
    if ("sandbox\\wd\\" in low.replace("/", "\\") or "\\data\\" in low) and any(
            ext in low for ext in (".txt", ".dat", ".cfg", ".ini", ".xml", ".log", ".bat", "cache", "settings", "version", "login")):
        print(f"{t} | {op:22} | ...{p[-90:]} | {res} | {det}")
print()
print("=== pcg_install accesses (the registry-installed original dir) ===")
for t, op, p, res, det in rows:
    if "pcg_install" in p:
        print(f"{t} | {op:22} | ...{p[-90:]} | {res} | {det}")
