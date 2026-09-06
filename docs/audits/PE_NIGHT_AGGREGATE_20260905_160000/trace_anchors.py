#!/usr/bin/env python3
"""The MindArk/registry anchor check: where do the registry reads sit in the trace timeline?"""
import csv

rows = list(csv.DictReader(open(r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_AUTOMATION_R1_20260905_140126\04_RUNTIME\live_test\entropia_death_trace.csv", encoding="utf-8", errors="replace")))
T = '\ufeff"Time of Day"'
for r in rows:
    r["Time of Day"] = r.pop(T)
e = [r for r in rows if r["Process Name"] == "Entropia.exe"]

# the timeline anchors: MindArk registry, the Entropia.log checks, the display reads, the thread exits
print("=== the anchors in timeline order ===")
anchors = []
for r in e:
    p = r["Path"]
    if "MindArk" in p:
        anchors.append(("REG-MINDARK", r))
    elif r["Operation"] == "CreateFile" and ("Entropia.log" in p or "Entropia.dmp" in p or "entropia" in p.lower()):
        anchors.append(("LOG", r))
    elif "DEVICEMAP" in p or "4d36e968" in p:
        anchors.append(("DISP-ENUM", r))
    elif r["Operation"] == "Thread Exit":
        anchors.append(("EXIT", r))
anchors.sort(key=lambda x: x[1]["Time of Day"])
for kind, r in anchors[:40]:
    p = r["Path"]
    short = p.split("\\")[-1] if p else ""
    print("{} {} {:16} {:70} {}".format(r["Time of Day"][3:21], kind, r["Operation"][:16], (p[:70]), r["Result"][:10]))
