#!/usr/bin/env python3
"""Display-enum canon gap — the primary-evidence analysis of the death trace.
WHAT did the client do at display enumeration before the silent -1 exit?
Read-only analysis of the second session's ProcMon CSV (LOCAL, 282k rows)."""
import csv

CSV = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_AUTOMATION_R1_20260905_140126\04_RUNTIME\live_test\entropia_death_trace.csv"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\DISPLAY_DEATH_ANALYSIS.txt"

rows = list(csv.DictReader(open(CSV, encoding="utf-8", errors="replace")))
T = '\ufeff"Time of Day"'
for r in rows:
    r["Time of Day"] = r.pop(T)
e = [r for r in rows if r["Process Name"] == "Entropia.exe"]
lines = [f"total rows: {len(rows)}; Entropia.exe rows: {len(e)}"]

disp_kw = ("display", "video", "gpu", "dxgi", "d3d", "vga", "nv-", "nvidia", "amd", "radeon", "monitor")
disp = [r for r in e if any(s in r["Path"].lower() for s in disp_kw)]
lines.append(f"display-related rows: {len(disp)}")
for r in disp[:40]:
    lines.append(f"{r['Time of Day'][3:21]} | {r['Operation'][:22]:22} | {r['Path'][:90]:90} | {r['Result'][:16]}")

# the LAST 40 operations of the process (the death window)
lines.append("\n=== LAST 40 OPERATIONS (the death window) ===")
for r in e[-40:]:
    lines.append(f"{r['Time of Day'][3:21]} | {r['Operation'][:22]:22} | {r['Path'][:90]:90} | {r['Result'][:16]} | {(r.get('Detail') or '')[:40]}")

# the errors/not-found in the whole Entropia lifetime
bad = [r for r in e if r["Result"] not in ("SUCCESS", "FAST IO DISALLOWED", "FILE LOCKED WITH ONLY READERS", "BUFFER OVERFLOW", "NO SUCH FILE", "NAME INVALID", "NAME NOT FOUND", "PATH NOT FOUND")]
nf = [r for r in e if r["Result"] in ("NAME NOT FOUND", "PATH NOT FOUND", "NO SUCH FILE")]
lines.append(f"\nnot-found/path errors: {len(nf)}")
for r in nf[:20]:
    lines.append(f"  {r['Operation'][:20]:20} {r['Path'][:90]:90} {r['Result']}")

# registry display reads
reg = [r for r in e if "registry" in r["Path"].lower() or "HKLM" in r["Path"]]
regd = [r for r in reg if any(s in r["Path"].lower() for s in ("display", "video", "dx"))]
lines.append(f"\nregistry rows: {len(reg)}; display-registry rows: {len(regd)}")
for r in regd[:30]:
    lines.append(f"  {r['Operation'][:18]:18} {r['Path'][:100]:100} {r['Result'][:14]}")

open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("\n".join(lines[:90]))
