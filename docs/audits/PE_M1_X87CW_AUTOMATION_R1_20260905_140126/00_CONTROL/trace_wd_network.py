#!/usr/bin/env python3
"""trace_wd_network.py — the sandbox-wd file activity + the network ops from the
ProcMon death trace."""
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
        t = row[idx["Time of Day"]]
        op = row[idx["Operation"]]
        p = row[idx["Path"]]
        res = row[idx["Result"]]
        det = row[idx["Detail"]] if "Detail" in idx else ""
        rows.append((t, op, p, res, det[:80]))

wd = "PE_M1_X87CW_EXECUTION_R1_20260905_125139"
print("=== ALL ops touching the sandbox wd tree (file activity) ===")
n = 0
skip = ("QueryNameInformationFile", "CloseFile", "IRP_MJ_CLOSE", "CreateFileMapping",
        "FASTIO_RELEASE_FOR_SECTION_SYNCHRONIZATION", "FASTIO_ACQUIRE_FOR_SECTION_SYNCHRONIZATION")
for t, op, p, res, det in rows:
    if wd in p and op not in skip:
        n += 1
        tail = p[-90:]
        print(f"{t} | {op:26} | ...{tail} | {res} | {det}")
        if n > 40:
            break
print("wd ops shown:", n)
print()
print("=== the network ops ===")
for t, op, p, res, det in rows:
    if any(k in op for k in ("TCP", "UDP", "DNS")) or "connect" in op.lower():
        print(f"{t} | {op:26} | {p[:90]} | {res} | {det[:50]}")
