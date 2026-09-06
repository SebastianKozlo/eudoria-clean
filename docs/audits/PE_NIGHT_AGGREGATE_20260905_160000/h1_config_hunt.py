#!/usr/bin/env python3
"""PE_HOURLY_LOOP H1-A — the intro-video config-hunt (the x87 CW unblock test prep).
(a) the command-line switch census in the exe (the classic -nologo/-windowed class);
(b) the .bik/.bink strings (the intro video files);
(c) the boot-config surface: the wd\\ file types + the MindArk registry keys on this machine."""
import os
import struct
import winreg

EXE = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\04_RUNTIME\sandbox\wd\Entropia.exe"
WD = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\04_RUNTIME\sandbox\wd"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\H1_CONFIG_HUNT.txt"

d = open(EXE, "rb").read()
lines = []

# (a) the switch census: the ASCII strings starting with '-' (len 2-16)
lines.append("=== switch-like strings (the '-'-prefixed, printable) ===")
found = []
i = 0
while True:
    i = d.find(b"-", i + 1)
    if i == -1:
        break
    # the candidate: '-X...' preceded by a non-alnum, followed by 1-14 lowercase alnum
    if i + 1 < len(d) and 0x61 <= d[i + 1] <= 0x7A:
        j = i + 1
        while j < len(d) and j - i <= 15 and (0x61 <= d[j] <= 0x7A or d[j] == 0x2E or d[j] == 0x5F):
            j += 1
        s = d[i:j]
        if 2 <= len(s) <= 15 and j < len(d) and (d[j] == 0 or d[j] == 0x00):
            if s not in [f[0] for f in found]:
                va_off = i
                found.append((s, va_off))
lines.append(f"unique: {len(found)}")
SWITCH_FILTER = (b"-n", b"-w", b"-f", b"-s", b"-d", b"-c", b"-m", b"-b", b"-r", b"-p", b"-l", b"-a", b"-v", b"-e")
for s, off in found:
    if s.startswith(SWITCH_FILTER) and len(s) >= 3:
        lines.append(f"  {s.decode()}")

# (b) the .bik strings
lines.append("\n=== the .bik/.bink strings ===")
for pat in (b".bik", b".bink", b"intro", b"Intro", b"logo", b"Logo", b"attract"):
    i = d.find(pat)
    cnt = 0
    while i != -1 and cnt < 6:
        # the surrounding string
        a = i
        while a > 0 and 0x20 <= d[a - 1] <= 0x7E and (i - a) < 32:
            a -= 1
        b = i
        while b < len(d) and 0x20 <= d[b] <= 0x7E and (b - i) < 32:
            b += 1
        s = d[a:b]
        if len(s) > 3 and s.isascii():
            lines.append(f"  [{pat.decode()}] @0x{a:X}: {s.decode()}")
        cnt += 1
        i = d.find(pat, i + 1)

# (c1) the wd file types
lines.append("\n=== the wd\\ file extensions ===")
from collections import Counter
ext = Counter()
for fn in os.listdir(WD):
    e = os.path.splitext(fn)[1].lower() or "(none)"
    ext[e] += 1
lines.append(", ".join(f"{k}x{v}" for k, v in ext.most_common()))

# (c2) the .ini/.cfg files anywhere in the sandbox tree
lines.append("\n=== the ini/cfg files under the sandbox ===")
for root, dirs, files in os.walk(os.path.dirname(WD)):
    for fn in files:
        if fn.lower().endswith((".ini", ".cfg", ".xml")):
            lines.append("  " + os.path.join(root, fn).replace(os.path.dirname(WD), "..."))

# (c3) the MindArk registry keys on this machine
lines.append("\n=== the MindArk registry keys ===")
for hive, label in ((winreg.HKEY_LOCAL_MACHINE, "HKLM"), (winreg.HKEY_CURRENT_USER, "HKCU"),
                    (winreg.HKEY_LOCAL_MACHINE, "HKLM-WOW64")):
    for sub in (r"Software\MindArk", r"SOFTWARE\WOW6432Node\MindArk"):
        try:
            k = winreg.OpenKey(hive, sub)
            names = []
            i = 0
            while True:
                try:
                    names.append(winreg.EnumKey(k, i))
                except OSError:
                    break
                i += 1
            lines.append(f"  {label}\\{sub}: EXISTS; subkeys: {names[:8]}")
            k.Close()
        except OSError:
            lines.append(f"  {label}\\{sub}: ABSENT")

print("\n".join(lines))
open(OUT, "w", encoding="utf-8").write("\n".join(lines))
