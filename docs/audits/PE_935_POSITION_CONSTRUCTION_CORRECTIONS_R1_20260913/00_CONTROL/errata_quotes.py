# -*- coding: utf-8 -*-
# errata_quotes.py - extract the exact verbatim quote lines for ERRATA_R5
# targets T-01..T-32 from the historical packages (UTF-8 exact, no console).
# STATIC-ONLY read of historical (NIETYKANE) files.

import json
import os

A = (r"D:\Eudoria_Reconstruction\99_Audits"
     r"\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913")
D = (r"D:\Eudoria_Reconstruction\99_Audits"
     r"\PE_935_ORIGIN_SEAM_DESKTOP_AUDIT_R1_20260913")
R = (r"D:\Eudoria_Reconstruction\99_Audits"
     r"\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913")
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"

FILES = {
    "REPORT": os.path.join(A, "06_REPORT", "REPORT.md"),
    "QC_REPORT": os.path.join(A, "06_REPORT", "QC_REPORT.md"),
    "ERRATA_R4": os.path.join(A, "06_REPORT", "ERRATA_R4.md"),
    "HANDOFF": os.path.join(A, "06_REPORT", "HANDOFF.md"),
    "GATES": os.path.join(A, "06_REPORT", "STAGE_ACCEPTANCE_GATES.csv"),
    "SEAM_FLOW_MAP": os.path.join(A, "02_ANALYSIS", "SEAM_FLOW_MAP.md"),
    "RESEARCH": os.path.join(A, "06_REPORT", "RESEARCH_FINDINGS.md"),
    "AUDYT": os.path.join(D, "AUDYT.md"),
    "DESKTOP_REPORT": os.path.join(D, "REPORT.md"),
    "R_REPORT": os.path.join(R, "06_REPORT", "REPORT.md"),
    "ERRATA_R3": os.path.join(R, "06_REPORT", "ERRATA_R3.md"),
    "ENTRYPOINT": os.path.join(REPO, "AUDIT_ENTRYPOINT.md"),
}


def get_lines(path, line_nos):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return {n: lines[n - 1].rstrip("\n") for n in line_nos}


def line_count(path):
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)


quotes = {}

quotes["REPORT_30"] = get_lines(FILES["REPORT"], [30])
quotes["REPORT_27_34"] = get_lines(FILES["REPORT"], list(range(27, 35)))
quotes["REPORT_52"] = get_lines(FILES["REPORT"], [52])
quotes["REPORT_54"] = get_lines(FILES["REPORT"], [54])
quotes["REPORT_55"] = get_lines(FILES["REPORT"], [55])
quotes["REPORT_97"] = get_lines(FILES["REPORT"], [97])
quotes["REPORT_99"] = get_lines(FILES["REPORT"], [99])
quotes["REPORT_120_124"] = get_lines(FILES["REPORT"], list(range(120, 125)))
quotes["REPORT_138_140"] = get_lines(FILES["REPORT"], list(range(138, 141)))
quotes["REPORT_171"] = get_lines(FILES["REPORT"], [171])
quotes["REPORT_191_193"] = get_lines(FILES["REPORT"], list(range(191, 194)))

quotes["QC_46_57"] = get_lines(FILES["QC_REPORT"], list(range(46, 58)))
quotes["QC_75_77"] = get_lines(FILES["QC_REPORT"], list(range(75, 78)))

quotes["ERRATA_R4_73_77"] = get_lines(FILES["ERRATA_R4"], list(range(73, 78)))
quotes["ERRATA_R4_97"] = get_lines(FILES["ERRATA_R4"], [97])
quotes["ERRATA_R4_102_104"] = get_lines(FILES["ERRATA_R4"],
                                        list(range(102, 105)))
quotes["ERRATA_R4_127_128"] = get_lines(FILES["ERRATA_R4"], [127, 128])
quotes["ERRATA_R4_199_201"] = get_lines(FILES["ERRATA_R4"],
                                        list(range(199, 202)))
quotes["ERRATA_R4_225_229"] = get_lines(FILES["ERRATA_R4"],
                                        list(range(225, 230)))

quotes["HANDOFF_18_28"] = get_lines(FILES["HANDOFF"], list(range(18, 29)))

quotes["GATES_5"] = get_lines(FILES["GATES"], [5])
quotes["GATES_11"] = get_lines(FILES["GATES"], [11])

quotes["SEAM_FLOW_MAP_29"] = get_lines(FILES["SEAM_FLOW_MAP"], [29])
quotes["SEAM_FLOW_MAP_46"] = get_lines(FILES["SEAM_FLOW_MAP"], [46])
quotes["SEAM_FLOW_MAP_68"] = get_lines(FILES["SEAM_FLOW_MAP"], [68])

quotes["RESEARCH_20"] = get_lines(FILES["RESEARCH"], [20])
quotes["RESEARCH_73"] = get_lines(FILES["RESEARCH"], [73])

quotes["AUDYT_55"] = get_lines(FILES["AUDYT"], [55])
quotes["DESKTOP_REPORT_55"] = get_lines(FILES["DESKTOP_REPORT"], [55])

quotes["R_REPORT_121"] = get_lines(FILES["R_REPORT"], [121])
quotes["R_REPORT_124"] = get_lines(FILES["R_REPORT"], [124])
quotes["R_REPORT_216_219"] = get_lines(FILES["R_REPORT"],
                                       list(range(216, 220)))

quotes["ERRATA_R3_70_71"] = get_lines(FILES["ERRATA_R3"], [70, 71])
quotes["ERRATA_R3_127_128"] = get_lines(FILES["ERRATA_R3"], [127, 128])

# entrypoint line 31 (long) + the specific fragments
quotes["ENTRYPOINT_31"] = get_lines(FILES["ENTRYPOINT"], [31])

# verify local == published for the quoted files (repo docs/audits copies)
import hashlib

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest().upper()


pairs = [
    (FILES["REPORT"],
     os.path.join(REPO, "docs", "audits",
                  "PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913", "REPORT.md")),
    (FILES["AUDYT"],
     os.path.join(REPO, "docs", "audits",
                  "PE_935_ORIGIN_SEAM_DESKTOP_AUDIT_R1_20260913", "AUDYT.md")),
    (FILES["R_REPORT"],
     os.path.join(REPO, "docs", "audits",
                  "PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913",
                  "REPORT.md")),
]
match = []
for local, repo in pairs:
    if os.path.isfile(repo):
        m = sha(local) == sha(repo)
        match.append({"local": local, "repo": repo, "identical": m})
    else:
        match.append({"local": local, "repo": repo,
                      "identical": "repo-path-missing"})

out = {"quotes": quotes, "published_match": match,
       "file_line_counts": {k: line_count(v)
                            for k, v in FILES.items() if os.path.isfile(v)}}
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "02_ANALYSIS", "ERRATA_R5_QUOTES.json")
with open(dst, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print("quotes extracted -> 02_ANALYSIS/ERRATA_R5_QUOTES.json")
for m in match:
    print("  local==repo published: %s (%s)" % (m["identical"],
                                                os.path.basename(m["local"])))
