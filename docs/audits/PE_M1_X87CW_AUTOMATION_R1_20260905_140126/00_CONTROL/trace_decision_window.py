#!/usr/bin/env python3
"""trace_decision_window.py — the rows between the last import load and the
DEVICEMAP query: the client's OWN first reads (the pre-exit checks)."""
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
                     (row[idx["Detail"]] if "Detail" in idx else "")[:70]))

# the window boundaries (from the prior analysis): .3192 -> .3443
lo, hi = "3:49:40.3192", "3:49:40.3444"
sel = [x for x in rows if lo <= x[0] <= hi]
print("rows in window:", len(sel))
skip_noise = ("RegSetInfoKey", "RegQueryKey", "FASTIO_RELEASE", "FASTIO_ACQUIRE",
              "CloseFile", "IRP_MJ_CLOSE", "CreateFileMapping", "QueryNameInformationFile",
              "QueryBasicInformationFile", "QueryOpen", "RegCloseKey", "Thread Create",
              "Thread Exit", "RegQueryValue.*Session Manager")
for t, op, p, res, det in sel:
    if any(s in op for s in skip_noise):
        continue
    tail = p[-95:]
    print(f"{t} | {op:26} | ...{tail} | {res} | {det}")
