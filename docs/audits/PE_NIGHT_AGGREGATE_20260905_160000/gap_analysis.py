#!/usr/bin/env python3
"""The gap analysis: EVERY row between the log checks and the display enum (7.4ms)."""
import csv

rows = list(csv.DictReader(open(r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_AUTOMATION_R1_20260905_140126\04_RUNTIME\live_test\entropia_death_trace.csv", encoding="utf-8", errors="replace")))
T = '\ufeff"Time of Day"'
for r in rows:
    r["Time of Day"] = r.pop(T)
e = [r for r in rows if r["Process Name"] == "Entropia.exe"]

# the gap: after 9:40.3388376 (the 2nd log miss), before 9:40.3462753 (DEVICEMAP)
lo = "9:40.3388376 PM"
hi = "9:40.3462753 PM"


def key(r):
    return r["Time of Day"]


gap = [r for r in e if lo < key(r) < hi]
print(f"rows in the gap: {len(gap)}")
for r in gap:
    print("{} {:24} {:78} {:14} {}".format(key(r)[3:21], r["Operation"][:24], (r["Path"] or "")[:78], r["Result"][:14], (r.get("Detail") or "")[:40]))
