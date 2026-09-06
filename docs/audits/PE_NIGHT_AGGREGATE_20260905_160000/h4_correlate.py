#!/usr/bin/env python3
"""The H4 correlation: which probe API call window contains the DEVICEMAP reads?"""
import csv

CSV = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\01_RAW\h4_probe.pml.csv"
MARKS = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\01_RAW\h4_probe_marks.txt"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\01_RAW\h4_correlation.txt"

marks = []
for line in open(MARKS, encoding="utf-8", errors="replace"):
    if line.startswith("MARK"):
        p = line.strip().split(" ", 2)
        marks.append((p[1], p[2]))
lines = ["markers: {}".format(marks)]

rows = list(csv.DictReader(open(CSV, encoding="utf-8", errors="replace")))
T = '\ufeff"Time of Day"'
for r in rows:
    r["Time of Day"] = r.pop(T)
pyid = [r for r in rows if "python" in r.get("Process Name", "").lower()]
lines.append("probe process rows: {}".format(len(pyid)))

# the display-registry rows of the probe
disp = [r for r in pyid if ("DEVICEMAP" in r["Path"]) or ("4d36e968" in r["Path"])
        or ("HardwareInformation" in r["Path"])]
lines.append("display-registry rows: {}".format(len(disp)))
for r in disp:
    lines.append("  {} {} {} {}".format(r["Time of Day"], r["Operation"][:18],
                                       r["Path"][:76], r["Result"][:10]))

# correlate each display row to a marker window
windows = []
for i, (ts, label) in enumerate(marks):
    if label.endswith("_BEGIN"):
        base = label[:-6]
        end = None
        for ts2, lab2 in marks[i + 1:]:
            if lab2.startswith(base) and lab2.endswith("_END"):
                end = ts2
                break
        windows.append((base, ts, end))
lines.append("\nwindows: {}".format(windows))


def tkey(t):
    # '10:47:55.8451234 AM'-style -> sortable numeric (ignore AM/PM nuance for the same morning)
    p = t.split(" ")
    hms = p[0]
    return hms


for r in disp:
    t = tkey(r["Time of Day"])
    hit = [base for base, b, e in windows if e and b <= t <= e]
    lines.append("row @{} -> window: {}".format(t, hit or "OUTSIDE"))

print("\n".join(lines))
open(OUT, "w", encoding="utf-8").write("\n".join(lines))
