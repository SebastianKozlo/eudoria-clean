#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qc_independent.py — PE-MASTER fresh internal QC (records-only) of
PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006.

Own engine only (no executor validator logic reused for the primary
measurements). READ-ONLY on the source package and the correction package;
results are written to OUT_DIR (00_CONTROL_INTERNAL_QC of the package).
"""
import csv, hashlib, json, os, re

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
PKG = os.path.join(REPO, "docs", "audits",
                   "PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006")
SRC = os.path.join(REPO, "docs", "audits",
                   "PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006")
OUT_DIR = os.path.join(PKG, "00_CONTROL_INTERNAL_QC")

R = {"findings": [], "measures": {}}

def finding(sev, code, detail):
    R["findings"].append({"severity": sev, "code": code, "detail": detail})

def measure(code, value):
    R["measures"][code] = value

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()

def read_rows(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.reader(fh))

def read_dict(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        dr = csv.DictReader(fh, restkey="__EXTRA__", restval=None)
        rows = list(dr)
        fn = list(dr.fieldnames or [])
    return fn, rows

# contract section 6 headers (typed from the contract text, independent)
FUNCTION_HEADER = ["ORD", "FUNCTION_ID", "EXTENT", "BUDGET_ROLE", "FUNCTION_IDENTITY",
                   "IDENTITY_EVIDENCE", "OBSERVED_OPERATION", "FINAL_SEMANTIC_ROLE",
                   "HISTORICAL_INPUT_AVAILABILITY", "CITED_PHYSICAL_SOURCE"]
EDGE_HEADER = ["EDGE_ID", "KIND", "SITE_OR_SOURCE", "INSTRUCTION_VA", "INSTRUCTION_BYTES",
               "TARGET_OR_DESTINATION_ARITHMETIC", "FIELD_REGISTER_VALUE",
               "RECEIVER_PROOF", "PATH_CONDITIONS", "STATUS", "CITED_PHYSICAL_SOURCE"]
STATUS_HEAD_RE = re.compile(r"^(CONFIRMED|UNRESOLVED_IN_BUDGET|UNRESOLVED|EDGE RECORDED|NON-CANONICAL LEAD|UNKNOWN|NOT_CHECKED)\b")
EVIDENCE_PATH_RE = re.compile(r"01_RAW/|00_CONTROL_INTERNAL_QC/|03_SCRIPTS/|\.txt\b|\.json\b|\.csv\b|\.py\b|\.md\b")

# ================================================================ A. corrected-ledger schema (own parser)
def my_schema_check(path, header, pk, name):
    res = {"table": name, "file": os.path.basename(path), "checks": {}, "failures": []}
    raw = open(path, "rb").read()
    res["checks"]["NO_BOM"] = not raw.startswith(b"\xef\xbb\xbf")
    res["checks"]["NO_CRLF"] = b"\r\n" not in raw
    lines = raw.decode("utf-8").split("\n")
    blank_lines = [i + 1 for i, ln in enumerate(lines) if ln.strip() == "" and ln != ""]
    res["checks"]["NO_BLANK_LINES"] = len(blank_lines) == 0
    res["blank_lines"] = blank_lines
    rows = read_rows(path)
    res["header"] = rows[0]
    res["checks"]["HEADER_EXACT"] = rows[0] == header
    res["checks"]["HEADER_UNIQUE"] = len(set(rows[0])) == len(rows[0])
    data = rows[1:]
    res["data_row_count"] = len(data)
    widths = sorted(set(len(r) for r in data))
    res["row_widths"] = widths
    res["checks"]["ROW_WIDTH_EXACT"] = widths == [len(header)]
    fn, drows = read_dict(path)
    extra = missing = 0
    for i, r in enumerate(drows):
        if "__EXTRA__" in r:
            extra += 1
        for k, v in r.items():
            if k != "__EXTRA__" and v is None:
                missing += 1
    res["checks"]["DICTREADER_NO_EXTRA"] = extra == 0
    res["checks"]["DICTREADER_NO_MISSING"] = missing == 0
    res["dictreader_extra"] = extra
    res["dictreader_missing"] = missing
    ids = [r[header.index(pk)] for r in data if len(r) == len(header)]
    res["checks"]["PRIMARY_ID_UNIQUE"] = len(set(ids)) == len(ids)
    empties = []
    for i, r in enumerate(data):
        if len(r) != len(header):
            continue
        for j, col in enumerate(header):
            if r[j] is None or r[j].strip() == "":
                empties.append((i + 2, col))
    res["checks"]["NO_EMPTY_REQUIRED_CELLS"] = len(empties) == 0
    res["empty_cells"] = empties
    if pk == "EDGE_ID":
        vocab = path_fail = swap = sep = 0
        for i, r in enumerate(data):
            if len(r) != len(header):
                continue
            st = r[header.index("STATUS")].strip()
            ct = r[header.index("CITED_PHYSICAL_SOURCE")].strip()
            if not STATUS_HEAD_RE.match(st):
                vocab += 1
            if EVIDENCE_PATH_RE.search(st):
                path_fail += 1
            if ct not in ("UNKNOWN", "NOT_CHECKED") and STATUS_HEAD_RE.match(ct):
                swap += 1
            if st == ct:
                sep += 1
        res["checks"]["STATUS_VOCABULARY"] = vocab == 0
        res["checks"]["STATUS_NOT_EVIDENCE_PATH"] = path_fail == 0
        res["checks"]["CITED_NOT_STATUS_TOKEN"] = swap == 0
        res["checks"]["STATUS_NE_CITED"] = sep == 0
    else:
        res["checks"]["FUNCTION_NO_STATUS_COLUMN"] = "STATUS" not in rows[0]
        prose = ["FUNCTION_IDENTITY", "IDENTITY_EVIDENCE", "OBSERVED_OPERATION",
                 "FINAL_SEMANTIC_ROLE", "HISTORICAL_INPUT_AVAILABILITY"]
        prose_empty = 0
        for r in data:
            if len(r) != len(header):
                continue
            for col in prose:
                if r[header.index(col)].strip() == "":
                    prose_empty += 1
        res["checks"]["FUNCTION_PROSE_NONEMPTY"] = prose_empty == 0
    res["verdict"] = "PASS" if all(res["checks"].values()) else "FAIL"
    return res

fcorr = os.path.join(PKG, "FUNCTION_LEDGER_CORRECTED.csv")
ecorr = os.path.join(PKG, "EDGE_LEDGER_CORRECTED.csv")
A_f = my_schema_check(fcorr, FUNCTION_HEADER, "ORD", "FUNCTION")
A_e = my_schema_check(ecorr, EDGE_HEADER, "EDGE_ID", "EDGE")
measure("A_FUNCTION_SCHEMA", A_f)
measure("A_EDGE_SCHEMA", A_e)

SRC_FILES = set()
for root, _, files in os.walk(SRC):
    for f in files:
        SRC_FILES.add(os.path.relpath(os.path.join(root, f), SRC).replace("\\", "/"))
cited_map = {
    "BYTE_WINDOWS.txt": "01_RAW/BYTE_WINDOWS.txt", "E8_CENSUS.json": "01_RAW/E8_CENSUS.json",
    "GETTER_PIN.txt": "01_RAW/GETTER_PIN.txt", "GETTER_PIN.json": "01_RAW/GETTER_PIN.json",
    "GHIDRA_VERIFY.json": "01_RAW/GHIDRA_VERIFY.json",
    "GHIDRA_DISASM_WINDOWS.txt": "01_RAW/GHIDRA_DISASM_WINDOWS.txt",
    "GHIDRA_DECOMPILES.txt": "01_RAW/GHIDRA_DECOMPILES.txt",
    "GovernanceWriteTime.txt": "01_RAW/GovernanceWriteTime.txt",
    "QC_CONTROLS.json": "01_RAW/QC_CONTROLS.json", "RTTI_PROBES.json": "01_RAW/RTTI_PROBES.json",
    "QC_GATES.csv": "00_CONTROL_INTERNAL_QC/QC_GATES.csv",
    "QC_REPORT_INTERNAL.md": "00_CONTROL_INTERNAL_QC/QC_REPORT_INTERNAL.md",
    "CALLSITE_SHORTLIST.csv": "CALLSITE_SHORTLIST.csv", "FINAL_REPORT.md": "FINAL_REPORT.md",
    "QC_REPORT.md": "QC_REPORT.md", "FUNCTION_LEDGER.csv": "FUNCTION_LEDGER.csv",
    "EDGE_LEDGER.csv": "EDGE_LEDGER.csv", "HANDOFF.md": "HANDOFF.md",
    "PE_MASTER_REVIEW.md": "PE_MASTER_REVIEW.md",
    "COMMITTED_PACKAGE_MANIFEST_SHA256.csv": "COMMITTED_PACKAGE_MANIFEST_SHA256.csv",
    "MANIFEST_REHASH.csv": "00_CONTROL_INTERNAL_QC/MANIFEST_REHASH.csv",
    "FULL_READ_LOG.txt": "00_CONTROL_INTERNAL_QC/FULL_READ_LOG.txt",
    "QC_MEASUREMENTS.txt": "00_CONTROL_INTERNAL_QC/QC_MEASUREMENTS.txt",
    "qc_negative_controls.ps1": "00_CONTROL_INTERNAL_QC/qc_negative_controls.ps1",
}
token_re = re.compile("|".join(re.escape(k) for k in cited_map))
cited_bad = []
for path, header in ((fcorr, FUNCTION_HEADER), (ecorr, EDGE_HEADER)):
    for i, r in enumerate(read_rows(path)[1:]):
        if len(r) != len(header):
            continue
        cited = r[header.index("CITED_PHYSICAL_SOURCE")].strip()
        if cited in ("UNKNOWN", "NOT_CHECKED"):
            continue
        toks = set(token_re.findall(cited))
        if not toks:
            cited_bad.append((os.path.basename(path), i + 2, "no known artifact token"))
        for t in toks:
            if cited_map[t] not in SRC_FILES:
                cited_bad.append((os.path.basename(path), i + 2, "missing on disk: " + cited_map[t]))
measure("A_CITED_ARTIFACT_EXISTENCE", {"bad": cited_bad, "count": len(cited_bad)})

# ================================================================ B. source naive census
fsrc = os.path.join(SRC, "FUNCTION_LEDGER.csv")
esrc = os.path.join(SRC, "EDGE_LEDGER.csv")
fsrc_rows = read_rows(fsrc)
esrc_rows = read_rows(esrc)
fsrc_widths = {r[0]: len(r) for r in fsrc_rows[1:]}
esrc_widths = {r[0]: len(r) for r in esrc_rows[1:]}
measure("B_SOURCE_NAIVE_CENSUS", {
    "function_header_cells": len(fsrc_rows[0]), "function_row_cells": fsrc_widths,
    "edge_header_cells": len(esrc_rows[0]), "edge_row_cells": esrc_widths,
    "function_data_rows": len(fsrc_rows) - 1, "edge_data_rows": len(esrc_rows) - 1})
f_bad = {k: v for k, v in fsrc_widths.items() if v != 10}
e_bad = {k: v for k, v in esrc_widths.items() if v != 11}
measure("B_SOURCE_DEFECTS", {"function_malformed": f_bad, "edge_malformed": e_bad,
                             "function_malformed_count": len(f_bad),
                             "edge_malformed_count": len(e_bad)})

# ================================================================ C. field-by-field reconstruction verification
corr_f = read_rows(fcorr)
corr_e = read_rows(ecorr)
src_f = {r[0]: r for r in fsrc_rows[1:]}
src_e = {r[0]: r for r in esrc_rows[1:]}

func_report = []
for r in corr_f[1:]:
    ordv = r[0]
    s = src_f[ordv]
    rowrep = {"ORD": ordv, "source_cells": len(s), "fields": {}}
    if ordv == "1":
        exp = {"ORD": s[0], "FUNCTION_ID": s[1], "EXTENT": s[2] + "," + s[3],
               "BUDGET_ROLE": s[4], "FUNCTION_IDENTITY": s[5],
               "IDENTITY_EVIDENCE": s[6] + "," + s[7],
               "OBSERVED_OPERATION": s[8] + "," + s[9],
               "FINAL_SEMANTIC_ROLE": "REWRITE_P3_4",
               "HISTORICAL_INPUT_AVAILABILITY": s[11], "CITED_PHYSICAL_SOURCE": s[12]}
    elif ordv == "2":
        exp = {c: s[i] for i, c in enumerate(FUNCTION_HEADER)}
        exp["FUNCTION_IDENTITY"] = "REWRITE_P3_2"
    else:
        exp = {"ORD": s[0], "FUNCTION_ID": s[1], "EXTENT": s[2], "BUDGET_ROLE": s[3],
               "FUNCTION_IDENTITY": s[4], "IDENTITY_EVIDENCE": s[5],
               "OBSERVED_OPERATION": "RECONSTRUCTED",
               "FINAL_SEMANTIC_ROLE": s[6], "HISTORICAL_INPUT_AVAILABILITY": s[7],
               "CITED_PHYSICAL_SOURCE": s[8]}
        if ordv == "5":
            exp["EXTENT"] = "REWRITE_P3_3"
            exp["FINAL_SEMANTIC_ROLE"] = "REWRITE_P3_5"
    for col in FUNCTION_HEADER:
        want = exp[col]
        got = r[FUNCTION_HEADER.index(col)]
        if want == "REWRITE_P3_4":
            rowrep["fields"][col] = {"kind": "P3_4_REWRITE", "corrected": got, "source": s[10],
                                     "equal": got == s[10]}
        elif want == "REWRITE_P3_2":
            rowrep["fields"][col] = {"kind": "P3_2_REWRITE", "corrected": got,
                                     "source": s[4], "equal": got == s[4]}
        elif want == "REWRITE_P3_3":
            rowrep["fields"][col] = {"kind": "P3_3_REWRITE", "corrected": got, "source": s[2],
                                     "equal": got == s[2]}
        elif want == "REWRITE_P3_5":
            rowrep["fields"][col] = {"kind": "P3_5_REWRITE", "corrected": got, "source": s[6],
                                     "equal": got == s[6]}
        elif want == "RECONSTRUCTED":
            rowrep["fields"][col] = {"kind": "RECONSTRUCTED", "corrected": got,
                                     "in_source_row": got in s}
        else:
            rowrep["fields"][col] = {"kind": "VERBATIM" if got == want else "MISMATCH",
                                     "equal": got == want}
    func_report.append(rowrep)
measure("C_FUNCTION_FIELD_REPORT", func_report)

edge_report = []
EDGE_VERBATIM_16 = ["E-GETTER", "E-C1", "E-C1-CALL", "E-C1-STORE", "E-E1-ABI",
                    "E-E2-KEYSTORE", "E-E2-HOLDERSTORE", "E-E2-NINODE", "E-E2-EXTRADATA",
                    "E-E2-REG", "E-M1", "E-M1-PAIR", "E-N1", "E-N2", "E-N3", "E-N4"]
for r in corr_e[1:]:
    eid = r[0]
    s = src_e[eid]
    rowrep = {"EDGE_ID": eid, "source_cells": len(s), "fields": {}}
    for col in EDGE_HEADER:
        got = r[EDGE_HEADER.index(col)]
        if eid in EDGE_VERBATIM_16:
            rowrep["fields"][col] = {"kind": "VERBATIM",
                                     "equal": got == s[EDGE_HEADER.index(col)]}
        elif eid == "E-M1-INSERT" and col == "STATUS":
            rowrep["fields"][col] = {"kind": "P3_5_REWRITE", "corrected": got,
                                     "source": s[9], "equal": got == s[9]}
        elif eid == "E-M1-INSERT":
            rowrep["fields"][col] = {"kind": "VERBATIM",
                                     "equal": got == s[EDGE_HEADER.index(col)]}
        elif eid == "E-C1-PUSH":
            idx = {"EDGE_ID": 0, "KIND": 1, "SITE_OR_SOURCE": 2, "INSTRUCTION_VA": 3,
                   "INSTRUCTION_BYTES": 4, "TARGET_OR_DESTINATION_ARITHMETIC": 5,
                   "FIELD_REGISTER_VALUE": 6, "RECEIVER_PROOF": "JOIN_7_8",
                   "PATH_CONDITIONS": 9, "STATUS": 10, "CITED_PHYSICAL_SOURCE": 11}[col]
            expv = (s[7] + "," + s[8]) if idx == "JOIN_7_8" else s[idx]
            if idx == "JOIN_7_8" and got == s[7] + ", " + s[8]:
                rowrep["fields"][col] = {"kind": "JOIN_7_8_SPACE_NORMALIZED", "exact_join": expv, "corrected": got}
                continue
            rowrep["fields"][col] = {"kind": "JOIN_7_8" if idx == "JOIN_7_8" else "VERBATIM",
                                     "equal": got == expv}
        elif eid == "E-E1-CALL":
            m = {"EDGE_ID": 0, "KIND": 1, "SITE_OR_SOURCE": 2, "INSTRUCTION_VA": 3,
                 "INSTRUCTION_BYTES": 4, "TARGET_OR_DESTINATION_ARITHMETIC": 5,
                 "FIELD_REGISTER_VALUE": 6, "RECEIVER_PROOF": 7,
                 "PATH_CONDITIONS": "RECONSTRUCTED", "STATUS": 8, "CITED_PHYSICAL_SOURCE": 9}[col]
            if m == "RECONSTRUCTED":
                rowrep["fields"][col] = {"kind": "RECONSTRUCTED", "corrected": got,
                                         "in_source_row": got in s}
            else:
                rowrep["fields"][col] = {"kind": "VERBATIM", "equal": got == s[m]}
        elif eid == "E-GB1":
            m = {"EDGE_ID": 0, "KIND": 1, "SITE_OR_SOURCE": 2, "INSTRUCTION_VA": 3,
                 "INSTRUCTION_BYTES": 4, "TARGET_OR_DESTINATION_ARITHMETIC": 5,
                 "FIELD_REGISTER_VALUE": "RECONSTRUCTED", "RECEIVER_PROOF": 6,
                 "PATH_CONDITIONS": 7, "STATUS": 8, "CITED_PHYSICAL_SOURCE": 9}[col]
            if m == "RECONSTRUCTED":
                rowrep["fields"][col] = {"kind": "RECONSTRUCTED", "corrected": got,
                                         "in_source_row": got in s}
            else:
                rowrep["fields"][col] = {"kind": "VERBATIM", "equal": got == s[m]}
        elif eid in ("E-GB2", "E-XD"):
            m = {"EDGE_ID": 0, "KIND": 1, "SITE_OR_SOURCE": 2, "INSTRUCTION_VA": 3,
                 "INSTRUCTION_BYTES": 4, "TARGET_OR_DESTINATION_ARITHMETIC": 5,
                 "FIELD_REGISTER_VALUE": 6, "RECEIVER_PROOF": "RECONSTRUCTED",
                 "PATH_CONDITIONS": 7, "STATUS": 8, "CITED_PHYSICAL_SOURCE": 9}[col]
            if m == "RECONSTRUCTED":
                rowrep["fields"][col] = {"kind": "RECONSTRUCTED", "corrected": got,
                                         "in_source_row": got in s}
            else:
                rowrep["fields"][col] = {"kind": "VERBATIM", "equal": got == s[m]}
    edge_report.append(rowrep)
measure("C_EDGE_FIELD_REPORT", edge_report)

f_mismatch = []
for rowrep in func_report:
    for col, rep in rowrep["fields"].items():
        if rep.get("kind") == "MISMATCH" or (rep.get("kind") == "VERBATIM" and rep.get("equal") is False):
            f_mismatch.append((rowrep["ORD"], col))
e_mismatch = []
for rowrep in edge_report:
    for col, rep in rowrep["fields"].items():
        if rep.get("kind") == "MISMATCH" or (rep.get("kind") in ("VERBATIM", "JOIN_7_8")
                                             and rep.get("equal") is False):
            e_mismatch.append((rowrep["EDGE_ID"], col))
measure("C_MISMATCHES", {"function": f_mismatch, "edge": e_mismatch})

# exact P3 transform verification
T_P3_2 = ("vtable store 0x00A7DCB0 @0x00528EA8",
          "vtable store 0x00A7DCB0 @0x00528EA2 [P3-2 corrected from 0x00528EA8; "
          "at 0x00528EA8 sits the different store 89 9E A4 00 00 00]")
T_P3_3 = ("0x00856190..0x0085620F (RET 4)",
          "0x00856190..0x00856210 (129 B; RET 4 = C2 04 00 @0x0085620E..0x00856210 "
          "[P3-3 corrected from 0x00856190..0x0085620F; the persisted BYTE_WINDOWS "
          "window F00856190_mapinsert_full ends at 0x0085620F and omits the final RET byte 00])")
T_P3_5_F = ("CTRL_C proves the body contains ZERO resource-family calls - NOT a resource join",
            "CTRL_C proves the decoded body contains ZERO DIRECT (E8) calls to the five "
            "examined resource-family addresses - NOT a resource join in the measured scope "
            "[P3-5 scoped wording]")
T_P3_5_E = ("(resource-join NEGATIVE: CTRL_C = zero resource-family E8s in the body)",
            "(resource-join NEGATIVE scoped per P3-5: CTRL_C = zero DIRECT (E8) calls to "
            "the five examined resource-family addresses {FUN_0072F580 FUN_006C9700 "
            "FUN_006CB6F0 FUN_006CB020 FUN_0043A550} in the decoded insert body)")
transforms = {
    "P3_2": corr_f[2][4] == src_f["2"][4].replace(T_P3_2[0], T_P3_2[1]),
    "P3_3": corr_f[5][2] == src_f["5"][2].replace(T_P3_3[0], T_P3_3[1]),
    "P3_5_F": corr_f[5][7] == src_f["5"][6].replace(T_P3_5_F[0], T_P3_5_F[1]),
    "P3_5_E": corr_e[15][9] == src_e["E-M1-INSERT"][9].replace(T_P3_5_E[0], T_P3_5_E[1]),
}
measure("C_EXACT_P3_TRANSFORMS", transforms)

# ================================================================ D. reconstructed-cell traceability
D = {}
frpt = open(os.path.join(SRC, "FINAL_REPORT.md"), "r", encoding="utf-8").read()
s7 = {}
for line in frpt.splitlines():
    m = re.match(r"^\|\s*(FUN_[0-9A-Fa-f]+)[^|]*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|\s*$", line)
    if m:
        s7[m.group(1)] = {"identity": m.group(2).strip(), "obs": m.group(3).strip(),
                          "role": m.group(4).strip(), "hist": m.group(5).strip()}
D["S7_ROWS_PARSED"] = sorted(s7.keys())
ordmap = {"3": "FUN_005247C0", "4": "FUN_00509330", "5": "FUN_00856190",
          "6": "FUN_00401360", "7": "FUN_0064B1E0"}
obs_check = {}
for ordv, fid in ordmap.items():
    corr_obs = corr_f[int(ordv)][FUNCTION_HEADER.index("OBSERVED_OPERATION")]
    s7_obs = s7.get(fid, {}).get("obs", "<missing>")
    exact = corr_obs == s7_obs
    norm = (corr_obs.replace("->", "\u2192") == s7_obs) or (corr_obs == s7_obs.replace("\u2192", "->"))
    obs_check[ordv] = {"fid": fid, "exact": exact, "normalized_equal": norm,
                       "arrow_in_s7": "\u2192" in s7_obs, "arrow_in_corr": "\u2192" in corr_obs}
D["OBSERVED_OPERATION_VS_S7"] = obs_check
corr_obs1 = corr_f[1][FUNCTION_HEADER.index("OBSERVED_OPERATION")]
s7_obs1 = s7.get("FUN_00414130", {}).get("obs", "")
D["ORD1_JOIN"] = {"join_equals_source_c8_c9": corr_obs1 == src_f["1"][8] + "," + src_f["1"][9],
                  "s7_is_strict_prefix_of_corr": corr_obs1.startswith(s7_obs1) and corr_obs1 != s7_obs1,
                  "corr_equals_s7": corr_obs1 == s7_obs1}
bw = open(os.path.join(SRC, "01_RAW", "BYTE_WINDOWS.txt"), "r", encoding="utf-8").read()
D["ORD8_OBS"] = {
    "s6_phrase_in_source_finalreport": "FUN_004157B0 (0x30-B head read only: the vtable store, for the GameClient classification" in re.sub(r"\s+", " ", frpt),
    "window_8BF1_at_B2": "0x004157B0  53 56 8B F1" in bw,
    "window_store_at_B8": "C7 06 18 9F A7 00" in bw,
    "row_identity_fragment": "C7 06 18 9F A7 00 = 0x00A79F18" in src_f["8"][4],
    "row_notdecoded": "further body NOT decoded" in src_f["8"][4],
    "extent_probe_only": "0x30 B probe only" in src_f["8"][2],
}
decomp = open(os.path.join(SRC, "01_RAW", "GHIDRA_DECOMPILES.txt"), "r", encoding="utf-8").read()
D["EDGE_RECON_TRACE"] = {
    "E-E1-CALL_PATH": {
        "frag_in_ord3_identity": "alloc-fail JZ 0x00524816" in src_f["3"][5],
        "frag_in_E-E1-ABI_receiver": "JZ 0x00524816" in src_e["E-E1-ABI"][7],
        "decompile_has_conditional_and_target": ("FUN_00509330" in decomp and "if" in decomp),
        "bytewindow_jz_7414": "74 14" in bw},
    "E-GB1_FIELD": {
        "bytewindow_a1": "A1 5C FE B9 00" in bw,
        "ord6_slot": "returns the object at [0x00B9FE5C]" in src_f["6"][4],
        "ord6_88b": "0x88-B object vtable 0x00A79F18" in src_f["6"][6],
        "egb2_status_confirms_class": src_e["E-GB2"][8].startswith("CONFIRMED")},
    "E-GB2_RECEIVER": {
        "bytewindow_8bf1_b2": "0x004157B0  53 56 8B F1" in bw,
        "bytewindow_store_b8": "C7 06 18 9F A7 00" in bw,
        "ord6_new_88": "PUSH 0x88" in src_f["6"][5] and "new @0x0040138F" in src_f["6"][5],
        "ord6_ctor_call": "ctor FUN_004157B0 @0x004013A9" in src_f["6"][5]},
    "E-XD_RECEIVER": {
        "bytewindow_56_8bf1": "0x0064B1E0  56 8B F1" in bw,
        "e_e2_extradata_push14": "6A 14" in src_e["E-E2-EXTRADATA"][5],
        "e_e2_extradata_new14_jz": "new(0x14)" in src_e["E-E2-EXTRADATA"][7] and "JZ 0x00509492" in src_e["E-E2-EXTRADATA"][7],
        "ord7_key_store": "ExtraData+0x10 = KEY" in src_f["7"][5]},
}
measure("D_TRACEABILITY", D)

# ================================================================ E. rel32 arithmetic recompute
arith = []
def rel32_target(va, rel_bytes):
    rel = int.from_bytes(rel_bytes, "little", signed=False)
    if rel >= 0x80000000:
        rel -= 0x100000000
    return (va + 5 + rel) & 0xFFFFFFFF

for r in corr_e[1:]:
    tcell = r[5]
    for m in re.finditer(r"(0x[0-9A-Fa-f]{8})\+5\+0x([0-9A-Fa-f]{8}) = (0x[0-9A-Fa-f]{8})", tcell):
        va = int(m.group(1), 16); rel = int(m.group(2), 16); tgt = int(m.group(3), 16)
        comp = rel32_target(va, rel.to_bytes(4, "little"))
        arith.append({"row": r[0], "claim": m.group(0), "recomputed": hex(comp), "match": comp == tgt})
    for m in re.finditer(r"(E8(?:\s+[0-9A-Fa-f]{2}){4})\s*@?(0x[0-9A-Fa-f]{8})\s*->\s*(0x[0-9A-Fa-f]{8})",
                         tcell + " " + r[7] + " " + r[8]):
        bb = [int(x, 16) for x in m.group(1).split()[1:]]
        va = int(m.group(2), 16); tgt = int(m.group(3), 16)
        comp = rel32_target(va, bb)
        arith.append({"row": r[0], "claim": m.group(0), "recomputed": hex(comp), "match": comp == tgt})
manual = [
    ("E-GB1", 0x004013A9, [0x02, 0x44, 0x01, 0x00], 0x004157B0),
    ("F-ORD6-new-thunk", 0x0040138F, [0x30, 0xC0, 0x55, 0x00], 0x0095D3C4),
    ("F-ORD3-new-thunk", 0x005247EC, [0xD3, 0x8B, 0x43, 0x00], 0x0095D3C4),
    ("F-ORD7-base-ctor", 0x0064B1E3, [0x98, 0xD5, 0x17, 0x00], 0x007C8780),
    ("F-ORD3-backptr", 0x0052482B, [0xB0, 0x4C, 0xFE, 0xFF], 0x005094E0),
    ("F-ORD3-listreg", 0x0052483D, [0x3E, 0x41, 0x18, 0x00], 0x006A8980),
]
for name, va, bb, tgt in manual:
    comp = rel32_target(va, bb)
    arith.append({"row": name, "claim": "manual %s" % name, "recomputed": hex(comp), "match": comp == tgt})
measure("E_REL32_RECOMPUTE", {"count": len(arith), "matches": sum(1 for a in arith if a["match"]),
                              "items": arith})

# ================================================================ F. source re-hash vs INPUT_IDENTITIES baseline
ii = open(os.path.join(PKG, "INPUT_IDENTITIES.md"), "r", encoding="utf-8").read()
baseline = {}
for line in ii.splitlines():
    m = re.match(r"^\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|\s*`([0-9A-Fa-f]{64})`\s*\|\s*$", line.strip())
    if m:
        baseline[m.group(1)] = (int(m.group(2)), m.group(3).upper())
actual = {}
for rel in baseline:
    p = os.path.join(SRC, rel.replace("/", os.sep))
    actual[rel] = (os.path.getsize(p), sha256(p))
diffs = [rel for rel in baseline if baseline[rel] != actual[rel]]
extra_files = sorted(SRC_FILES - set(baseline.keys()))
measure("F_SOURCE_REHASH", {"baseline_rows": len(baseline), "diffs": diffs,
                            "extra_files_not_in_baseline": extra_files})

# ================================================================ G. correction manifest re-hash
man_path = os.path.join(PKG, "CORRECTION_PACKAGE_MANIFEST_SHA256.csv")
man_rows = []
with open(man_path, "r", encoding="utf-8-sig", newline="") as fh:
    for line in fh:
        if line.startswith("#") or not line.strip():
            continue
        parts = line.strip().split(",")
        if parts[0] == "rel_path":
            continue
        man_rows.append((parts[0], int(parts[1]), parts[2].upper()))
man_bad = []
for rel, size, h in man_rows:
    p = os.path.join(PKG, rel.replace("/", os.sep))
    if not os.path.isfile(p):
        man_bad.append((rel, "missing"))
        continue
    if os.path.getsize(p) != size or sha256(p) != h:
        man_bad.append((rel, "mismatch actual %d %s" % (os.path.getsize(p), sha256(p))))
pkg_files = set()
for root, _, files in os.walk(PKG):
    for f in files:
        pkg_files.add(os.path.relpath(os.path.join(root, f), PKG).replace("\\", "/"))
uncovered = sorted(pkg_files - {m[0] for m in man_rows} - {"CORRECTION_PACKAGE_MANIFEST_SHA256.csv"})
measure("G_MANIFEST", {"rows": len(man_rows), "bad": man_bad, "physical_files_before_qc_records": len(pkg_files),
                       "uncovered_by_manifest": uncovered,
                       "self_excluded": "CORRECTION_PACKAGE_MANIFEST_SHA256.csv" not in {m[0] for m in man_rows}})

# ================================================================ H. P3 / DPA / Q14 content checks
H = {}
gov_src = open(os.path.join(SRC, "GOVERNANCE_DECISION.md"), "r", encoding="utf-8").read()
gwt = open(os.path.join(SRC, "01_RAW", "GovernanceWriteTime.txt"), "r", encoding="utf-8").read()
gov_new = open(os.path.join(PKG, "GOVERNANCE_DECISION.md"), "r", encoding="utf-8").read()
full_sha = re.search(r"SHA256=([0-9A-Fa-f]{64})", gwt).group(1)
m61 = re.search(r"A953107598F7553C8DE5926EE7FA690920117E([0-9A-Fa-f]+?)\.", gov_src)
H["P3_1"] = {
    "full_sha": full_sha, "full_sha_len": len(full_sha),
    "src_amendment_short_len": len(m61.group(0)) - 1 if m61 else None,
    "short_equals_full_minus_239": bool(m61) and full_sha.replace("20117E34923977", "20117E34977") == m61.group(0)[:-1],
    "corr_pkg_has_full_sha": full_sha in gov_new,
    "short_sha_in_both": bool(m61) and m61.group(0)[:-1] in gov_new and m61.group(0)[:-1] in gov_src,
}
mrow = re.search(r"=== F00856190_mapinsert_full : VA (0x00856190\.\.0x[0-9A-Fa-f]+) ===", bw)
qcrpt_src = open(os.path.join(SRC, "QC_REPORT.md"), encoding="utf-8").read()
H["P3_2"] = {"bytewindow_row_EA0": bool(re.search(r"0x00528EA0\s+00 00 C7 06 B0 DC A7 00 89 9E A4 00 00 00", bw)),
             "store_at_EA2": "C7 06 B0 DC A7 00" in bw,
             "different_store_at_EA8": "89 9E A4 00 00 00" in bw,
             "corr_row2_identity_EA2": "@0x00528EA2" in corr_f[2][4],
             "source_row2_identity_EA8": "@0x00528EA8" in src_f["2"][4],
             "source_row2_evidence_already_EA2": "@0x00528EA2" in src_f["2"][5]}
H["P3_3"] = {"window_extent_declared": mrow.group(1) if mrow else None,
             "window_ends_0F": bool(mrow) and mrow.group(1).endswith("0x0085620F"),
             "epilogue_83C410C204": "83 C4 10 C2 04" in bw,
             "source_qc_body_210": "0x00856190..0x00856210" in qcrpt_src,
             "corr_extent_129B": "0x00856190..0x00856210" in corr_f[5][2] and "129 B" in corr_f[5][2],
             "inclusive_bytes": 0x00856210 - 0x00856190 + 1}
handoff_src = open(os.path.join(SRC, "HANDOFF.md"), encoding="utf-8").read()
H["P3_4"] = {"src_handoff_3kinds": "≥3 receiver kinds" in handoff_src,
             "src_finalreport_3kinds": bool(re.search(r"at least three\s+DIFFERENT receiver kinds", frpt)),
             "src_review_3kinds": ">=3 receiver kinds across 6 sites" in open(os.path.join(SRC, "PE_MASTER_REVIEW.md"), encoding="utf-8").read(),
             "corr_row1_wording": ("ClientMovableObject instance (CONFIRMED)" in corr_f[1][7]
                                    and "GameClient singleton (CONFIRMED)" in corr_f[1][7]
                                    and "UNRESOLVED" in corr_f[1][7]
                                    and "STRONGLY_SUPPORTED in examined census scope" in corr_f[1][7]),
             "corr_no_3kinds_proven_active": "receiver kinds proven this run" not in corr_f[1][7]}
pkgtxt = {}
for f in os.listdir(PKG):
    p = os.path.join(PKG, f)
    if os.path.isfile(p):
        pkgtxt[f] = open(p, encoding="utf-8").read()
occ = {}
for f, t in pkgtxt.items():
    hits = [m.start() for m in re.finditer(r"No resource edge exists anywhere", t)]
    if hits:
        occ[f] = [t[max(0, h - 100):h + 100].replace("\n", " ") for h in hits]
H["P3_5"] = {"src_finalreport_s13": "No resource edge exists anywhere in the examined path" in frpt,
             "occurrences_in_new_package": occ,
             "corr_wording_present": "No resource/template/model consumer was established in the examined bounded path." in re.sub(r"\s+", " ", pkgtxt["FINAL_REPORT.md"]),
             "gov_wording_present": "No resource/template/model consumer was established in the examined bounded path." in re.sub(r"\s+", " ", gov_new),
             "five_addr_predicate_in_E-M1-INSERT": all(a in corr_e[15][9] for a in
                 ["FUN_0072F580", "FUN_006C9700", "FUN_006CB6F0", "FUN_006CB020", "FUN_0043A550"])}
gates_rows = read_rows(os.path.join(SRC, "00_CONTROL_INTERNAL_QC", "QC_GATES.csv"))
g2 = [r for r in gates_rows if r and r[0] == "G2"][0]
H["P3_6"] = {"declared_cols": len(gates_rows[0]), "g2_naive_cells": len(g2)}
H["DPA2"] = {"src_q7_label": "PASS WITH ONE DISCLOSED DEVIATION" in qcrpt_src,
             "src_q9_qcpass": "**QC_PASS**" in qcrpt_src,
             "src_7th_function_disclosed": "7th function" in qcrpt_src,
             "src_finalreport_6counted": "COUNTED (6, the contract maximum)" in frpt,
             "new_FAIL_recorded": "ORIGINAL_PROCESS_BUDGET_COMPLIANCE = FAIL" in gov_new,
             "new_HUMAN_ADJUDICATED_NOW": "PROCESS_EXCEPTION_AUTHORIZATION = HUMAN_ADJUDICATED_NOW" in gov_new,
             "new_RETROACTIVE_NO": "RETROACTIVE_PRIOR_AUTHORIZATION = NO" in gov_new,
             "new_HISTORICAL_BREACH_PRESERVED": "HISTORICAL_BREACH_PRESERVED = YES" in gov_new}
br = {}
for f, t in pkgtxt.items():
    ex = len(re.findall(r"BUDGET RESPECTED", t))
    ci = [m.start() for m in re.finditer(r"budget respected", t)]
    if ex or ci:
        br[f] = {"uppercase_count": ex, "lowercase_count": len(ci),
                 "lower_contexts": [t[max(0, h - 80):h + 80].replace("\n", " ") for h in ci]}
H["BUDGET_RESPECTED_SCAN"] = br
H["DPA3"] = {
    "src_attribution_quote": "persistence zrobi osobna faza" in gov_src,
    "src_verbatim_authorizes_commit": "Autoryzuję commit i push" in gov_src,
    "src_verbatim_manifest_last": "manifest LAST, commit/push" in gov_src,
    "src_verbatim_has_no_deferral_inside_block": "NIE commituj" not in gov_src.split("---END VERBATIM HUMAN INSTRUCTION---")[0].split("---BEGIN VERBATIM HUMAN INSTRUCTION---")[1],
    "new_split_source_status": "PERSISTENCE_PHASE_SPLIT_SOURCE = NOT_ESTABLISHED_IN_RECORDED_HUMAN_SOURCE" in gov_new,
    "new_orchestrator_class": "ORCHESTRATOR_PHASE_SPLIT" in gov_new,
    "new_final_pub_auth_present": "FINAL_PUBLICATION_AUTHORIZATION = PRESENT" in gov_new,
    "new_no_never_existed_claim": ("definitely never existed" not in gov_new) and ("nigdy nie istniała" not in gov_new),
}
supersession = open(os.path.join(PKG, "SUPERSESSION.md"), encoding="utf-8").read()
getter_sites = sorted([a["claim"].split("+5")[0] for a in arith
                       if a["match"] and a["claim"].endswith("= 0x00414130")])
H["Q14"] = {
    "1_getter_bytes": corr_e[1][4] == "8B 41 74 C3" and "mov eax,[ecx+0x74]; ret" in corr_f[1][6],
    "2_six_direct_e8_to_getter": getter_sites == ["0x004569D3", "0x00456BEB", "0x0045723E",
                                                   "0x0045A08B", "0x00528FD9", "0x008561AC"],
    "getter_site_count": len(getter_sites),
    "3_cmo_receiver": any("SAME_MOVABLE_OBJECT_PROVEN" in r[9] for r in corr_e[1:] if r[0] in ("E-C1", "E-M1")),
    "4_gameclient_diff": all("DIFFERENT_OBJECT" in r[9] for r in corr_e[1:] if r[0] in ("E-N1", "E-N2", "E-N3")),
    "5_map_identity": "mgr1" in corr_f[5][4] and "[value+0x74]" in corr_f[5][6],
    "6_sf_passthrough": "[SF+0x14]" in corr_f[4][5] and "FUN_0064B1E0" in corr_f[4][6],
    "7_resource_not_established": "RESOURCE_EDGE_STATUS = NOT_ESTABLISHED_IN_EXAMINED_PATH" in supersession,
    "8_world_xyz_no": "WORLD_XYZ_RECOVERED = NO" in supersession,
    "9_static_building": "STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED" in supersession,
    "10_hist_instance_no": "HISTORICAL_INSTANCE_DATA_RECOVERED = NO" in supersession,
}
H["FORBIDDEN"] = {
    "RESOURCE_EDGE_CONFIRMED_files": [f for f, t in pkgtxt.items() if "RESOURCE_EDGE_CONFIRMED" in t],
    "REJECTED_GLOBAL_files": {f: t.count("RESOURCE_EDGE_REJECTED_GLOBAL") for f, t in pkgtxt.items() if "RESOURCE_EDGE_REJECTED_GLOBAL" in t},
}
measure("H_CONTENT", H)

os.makedirs(OUT_DIR, exist_ok=True)
out = json.dumps(R, indent=1, default=str)
with open(os.path.join(OUT_DIR, "QC_INDEPENDENT_MEASUREMENTS.json"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(out + "\n")
print("WROTE", os.path.join(OUT_DIR, "QC_INDEPENDENT_MEASUREMENTS.json"))
print()
print("A_FUNCTION_SCHEMA:", A_f["verdict"], A_f["checks"])
print("A_EDGE_SCHEMA:", A_e["verdict"], A_e["checks"])
print("A_CITED:", len(cited_bad), cited_bad[:5])
print("B malformed F:", len(f_bad), f_bad, " E:", len(e_bad), e_bad)
print("C mismatches F:", f_mismatch)
print("C mismatches E:", e_mismatch)
print("C transforms:", transforms)
print("D s7 rows:", D["S7_ROWS_PARSED"])
print("D obs vs s7:", {k: (v["exact"], v["normalized_equal"], v["arrow_in_s7"]) for k, v in obs_check.items()})
print("D ord1:", D["ORD1_JOIN"])
print("D ord8:", D["ORD8_OBS"])
print("D edge recon:", json.dumps(D["EDGE_RECON_TRACE"], indent=1))
print("E rel32 matches:", sum(1 for a in arith if a["match"]), "/", len(arith))
print("E bad:", [a for a in arith if not a["match"]])
print("F baseline rows:", len(baseline), "diffs:", diffs, "extra:", extra_files)
print("G manifest rows:", len(man_rows), "bad:", man_bad, "uncovered:", uncovered,
      "self_excluded ok:", "CORRECTION_PACKAGE_MANIFEST_SHA256.csv" not in {m[0] for m in man_rows})
print("H P3_1:", H["P3_1"])
print("H P3_2:", H["P3_2"])
print("H P3_3:", H["P3_3"])
print("H P3_4:", H["P3_4"])
print("H P3_5 src s1.3:", H["P3_5"]["src_finalreport_s13"], "| occurrences:", {k: len(v) for k, v in occ.items()},
      "| corr wording:", H["P3_5"]["corr_wording_present"], "| five addr:", H["P3_5"]["five_addr_predicate_in_E-M1-INSERT"])
print("H P3_6:", H["P3_6"])
print("H DPA2:", H["DPA2"])
print("H BUDGET_RESPECTED:", json.dumps(H["BUDGET_RESPECTED_SCAN"], indent=1))
print("H DPA3:", H["DPA3"])
print("H Q14:", H["Q14"])
print("H FORBIDDEN:", H["FORBIDDEN"])
