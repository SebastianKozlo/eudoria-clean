# -*- coding: utf-8 -*-
# errata_live_scan.py - repo-wide scan for LIVE copies of the T-01..T-32
# formulations (contract return item: whether any live copy exists beyond
# the register targets). STATIC-ONLY read-only scan of the repo tree.
#
# Method: for each search key derived from the T-01..T-32 register
# (contract section 3.4), scan all text files in the repo (git-tracked tree
# + the untracked experiments/ NOT excluded - it is scanned read-only for
# completeness but classified as foreign). Classify each hit:
#   IN_REGISTER - the exact target file/line from the register
#   HISTORICAL_PACKAGE - inside a published/legacy audit package other than
#                the register target line (quote/context layers)
#   LIVE_ELSEWHERE - any other location (these are the "live copies")

import hashlib
import json
import os

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"

# search keys per T-group (distinctive fragments of the register quotes)
KEYS = [
    ("T01_T02_subkursor", ["sub-kursor (FUN_007343E0"]),
    ("T03_subpakiet_kursora", ["deserializacja FUN_007453D0 z sub-pakietu kursora"]),
    ("T04_SUB_kursora", ["(z SUB-kursora)"]),
    ("T05_subpakiet_SE-R4-1", ["sub-pakiet (FUN_007343E0"]),
    ("T06_subkursor_u16_header", ["FUN_007343E0 (sub-kursor u16-header)"]),
    ("T07_gates_subkursora", ["z sub-kursora"]),
    ("T08_T16_entrypoint", ["sub-packet via FUN_007343E0"]),
    ("T08_undeoded_typo", ["undeoded"]),
    ("T09_brak_korekty_chain", ["setter f90", "ctor kopiuje do instancji"]),
    ("T16_T17_statics_channel", ["NOT covered by the movable channel"]),
    ("T17_nie_objete_kanalem", ["NIE objęte tym kanałem"]),
    ("T19_zrodlo_insertow", ["Źródło insertów = komunikaty", "Zrodlo insertu = KOMUNIKATY"]),
    ("T20_T27_GB4_row", ["Zrodlo insertu = KOMUNIKATY"]),
    ("T21_T24_pin_004C4875", ["0x004C4875", "004C4875"]),
    ("T25_0x25_wpisow", ["0x25 wpisów", "0x25 wpisow", "0x25 entries"]),
    ("T26_offbyone_004C4789", ["004C4789", "0x004C4789"]),
    ("T28_T29_CSV_poprawny", ["wiersz CSV był poprawny", "wiersz CSV byl poprawny",
                              "Bramka CSV GB4", "była poprawna", "byla poprawna"]),
    ("T30_T31_rb_find", ["rb-find FUN_00971780", "rb-find"]),
    ("T32_transform_296445", ["transform 296445"]),
]

EXCLUDE_DIRS = {".git", "node_modules", "__pycache__"}

hits = {}
for root, dirs, files in os.walk(REPO):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for fn in files:
        p = os.path.join(root, fn)
        ext = os.path.splitext(fn)[1].lower()
        if ext in (".png", ".jpg", ".jpeg", ".glb", ".bin", ".dat",
                   ".vfs", ".exe", ".dll", ".nif", ".bnt", ".ark",
                   ".db", ".gbf", ".prp", ".pyc", ".zip", ".7z", ".whl",
                   ".wav", ".mp3", ".mp4", ".ico", ".woff", ".woff2",
                   ".ttf", ".eot", ".map"):
            continue
        try:
            with open(p, "rb") as f:
                data = f.read()
        except OSError:
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            try:
                text = data.decode("latin-1")
            except Exception:
                continue
        for key_id, frags in KEYS:
            for frag in frags:
                if frag in text:
                    # find line numbers
                    lines = []
                    for i, line in enumerate(text.splitlines(), 1):
                        if frag in line:
                            lines.append(i)
                    if lines:
                        hits.setdefault(key_id, []).append({
                            "file": os.path.relpath(p, REPO),
                            "fragment": frag,
                            "lines": lines[:20],
                            "n_lines": len(lines),
                        })

# classification
REGISTER_TARGETS = {
    "docs/audits/PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/REPORT.md",
    "docs/audits/PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/QC_REPORT.md",
    "docs/audits/PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/ERRATA_R4.md",
    "docs/audits/PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/HANDOFF.md",
    "docs/audits/PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/STAGE_ACCEPTANCE_GATES.csv",
    "docs/audits/PE_935_ORIGIN_SEAM_DESKTOP_AUDIT_R1_20260913/AUDYT.md",
    "docs/audits/PE_935_ORIGIN_SEAM_DESKTOP_AUDIT_R1_20260913/REPORT.md",
    "docs/audits/PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913/06_REPORT/REPORT.md",
    "docs/audits/PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913/06_REPORT/ERRATA_R3.md",
    "AUDIT_ENTRYPOINT.md",
}

out = {}
for key_id, hitlist in sorted(hits.items()):
    classified = []
    for h in hitlist:
        rel = h["file"].replace("\\", "/")
        if rel in REGISTER_TARGETS:
            cls = "IN_REGISTER"
        elif rel.startswith("docs/audits/"):
            cls = "HISTORICAL_PACKAGE"
        elif rel.startswith("experiments/"):
            cls = "FOREIGN_UNTRACKED"
        else:
            cls = "LIVE_ELSEWHERE"
        classified.append({"file": rel, "class": cls,
                           "fragment": h["fragment"],
                           "lines": h["lines"],
                           "n_lines": h["n_lines"]})
    out[key_id] = classified
    print("%s:" % key_id)
    for c in classified:
        print("   [%s] %s lines=%s" % (c["class"], c["file"],
                                       c["lines"][:8]))

dst = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "02_ANALYSIS", "ERRATA_LIVE_SCAN.json")
with open(dst, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print("DONE -> 02_ANALYSIS/ERRATA_LIVE_SCAN.json")
