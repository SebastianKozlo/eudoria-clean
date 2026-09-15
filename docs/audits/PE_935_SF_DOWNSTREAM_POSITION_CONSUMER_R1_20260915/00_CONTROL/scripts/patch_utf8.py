"""patch_utf8.py — one-shot: make all package-generator open() calls explicit UTF-8 (run-local helper)."""
import io
import re

BASE = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915\00_CONTROL\scripts"

for name in ("gen_raw_evidence.py", "gen_manifest.py"):
    p = BASE + "\\" + name
    src = io.open(p, encoding="utf-8").read()
    new, n = re.subn(r'(with open\((?:os\.path\.join\([^)]*(?:\)[^)]*)*?\)|\w+), )"w"\)',
                     lambda m: m.group(1) + '"w", encoding="utf-8")', src)
    io.open(p, "w", encoding="utf-8", newline="").write(new)
    print(name, "patched opens:", n)
