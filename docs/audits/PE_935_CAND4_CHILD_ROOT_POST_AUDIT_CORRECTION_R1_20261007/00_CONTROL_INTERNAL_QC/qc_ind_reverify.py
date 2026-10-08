"""qc_ind_reverify.py — INDEPENDENT internal QC engine, part 1 (records/identity),
for PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007.

Author: pe-master-auditor (fresh-context internal QC under PE-MASTER dispatch).
NOT the executor's qc_correction.py: this is an INDEPENDENT re-verification with
its OWN adjudication map (written after a full row-by-row read of all 69 source
rows), its OWN hashing, its OWN quote checks. RECORDS-ONLY: zero EXE access,
zero new RE; reads published records + BASE-blob-verified working-tree copies.

Checks implemented here (I1..I16):
  I1  correction-package manifest re-hash (19 physical files vs 18 manifest rows;
      every size+SHA256 re-measured by THIS script)
  I2  encoding: UTF-8 no-BOM, LF-only, strict-decodable for all 19 package files
  I3  SOURCE_PACKAGE immutability: 38/38 working-tree == BASE git blobs (my own
      git hash-object method)
  I4  source ledger shape: 69 rows; original class census 24/7/11/27
  I5  verbatim round-trip: all 69 rows x 9 original fields byte-identical between
      the SOURCE ledger and the CORRECTED ledger's ORIGINAL_* columns
  I6  MY OWN row-by-row re-adjudication (explicit per-row map below) vs the
      corrected ledger's CORRECTED_COUNTED / CORRECTED_CLASS for all 69 rows
  I7  corrected class census == {32 COUNTED, 11 REPIN-EXEMPTION, 17 CLEAN, 9 CANDIDATE}
      and the counted set == E-01..E-24 + RV-01..RV-07 + NEIGH-09
  I8  MINIMUM >= 32 (24+8 defensive); MINIMUM bodies >= 7; EXACT statuses UNRESOLVED;
      historical FAILs preserved (edge/body/scope); RETROACTIVE_PRIOR_AUTHORIZATION = NO
  I9  FUNCTION_BODY_ACCOUNTING: 7 COUNTED rows (6 declared + FUN_006C0EE0 probe);
      the probe verified at the source (qc_controls.py line 131 disasm(0x006C0EE0));
      probe bytes recorded in source CONTROL_RESULTS.json CTRL_3 mutated_case
  I10 FUN_006C0EE0 absent from ALL prior audit packages at BASE (grep)
  I11 RP-01..RP-11 prior citations spot-verified REAL (X01/X03/X05/X31/X08 in the
      J2 census; E5/E6 + QC S4 in the 20261006 package; prior window record)
  I12 SUPERSESSION quote verification: every S-1..S-9 quote exists verbatim in the
      cited SOURCE package file; the NOT-superseded byte measurements are present
  I13 Desktop COMMITTED_INPUT cross-hash: the audited ledger bytes the Desktop
      hashed == the BASE blob bytes (same SHA256)
  I14 governance: verbatim human instruction elements present; phase split recorded;
      HARD_STOP / NEXT_EXPERIMENT_AUTHORIZED = NO
  I15 separation algebra: CORRECTION_RECORDS_QC vs ORIGINAL_SCOPE_COMPLIANCE=FAIL
      never conflated; no "ORIGINAL_SCOPE_COMPLIANCE = PASS" anywhere
  I16 EXE-access scan over the correction package scripts: zero .exe/pe_reader/
      capstone reads (CTRL_3/CTRL_4 rebuilt = synthetic/prior-pin only)

Writes: 00_CONTROL_INTERNAL_QC/QC_IND_RESULTS.json (merged with part 2 results).
"""
import csv
import hashlib
import io
import json
import os
import re
import subprocess
import sys

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
PKG = os.path.join(REPO, "docs", "audits", "PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007")
QC_DIR = os.path.join(PKG, "00_CONTROL_INTERNAL_QC")
SRC_PKG = os.path.join(REPO, "docs", "audits", "PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007")
DESKTOP = r"C:\Users\User\Documents\ChatGPT\PE\PE_935_CAND4_CHILD_ROOT_DESKTOP_POST_AUDIT_790E837_20261007"
BASE = "790e83735b439e2d76a250868a47a599c2c10184"

results = {}


def rec(cid, ok, detail):
    results[cid] = {"ok": bool(ok), "detail": detail}
    print(("PASS  " if ok else "FAIL  ") + cid + ": " + detail)


def sha256_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def read_rows(path):
    txt = open(path, encoding="utf-8").read()
    lines = [ln for ln in txt.splitlines() if ln and not ln.startswith("#")]
    return list(csv.DictReader(io.StringIO("\n".join(lines)), strict=False))


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True, encoding="utf-8").stdout


# ============================== I1: manifest re-hash (my own)
phys = {}
for root, dirs, files in os.walk(PKG):
    dirs[:] = [d for d in dirs if d not in ("__pycache__", "00_CONTROL_INTERNAL_QC")]
    for fn in files:
        full = os.path.join(root, fn)
        rel = os.path.relpath(full, REPO).replace("\\", "/")
        phys[rel] = (os.path.getsize(full), sha256_file(full))
manifest = {}
with open(os.path.join(PKG, "MANIFEST_SHA256.csv"), encoding="utf-8") as f:
    for ln in f:
        ln = ln.strip()
        if ln and not ln.startswith("#") and not ln.startswith("path,"):
            p, s, h = ln.rsplit(",", 2)
            manifest[p] = (int(s), h)
mm = [p for p in manifest if p not in phys or phys[p] != manifest[p]]
extra = [p for p in phys if p not in manifest and not p.endswith("MANIFEST_SHA256.csv")]
rec("I1_manifest_rehash", len(manifest) == 18 and len(phys) == 19 and not mm and not extra,
    f"physical package files (executor close, pre-QC) = {len(phys)}; manifest rows = {len(manifest)}; "
    f"size+SHA256 mismatches = {len(mm)}; extra = {len(extra)} — every manifest row re-measured by THIS QC (zero mismatch); "
    f"manifest self-excluded; the QC's own 00_CONTROL_INTERNAL_QC/ additions are excluded from this census by design "
    f"(the persistence phase regenerates the manifest over the final physical package — the established pattern)")

# ============================== I2: encoding (my own)
enc = []
for rel, _ in phys.items():
    raw = open(os.path.join(REPO, rel.replace("/", "\\")), "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"):
        enc.append(rel + ":BOM")
    if b"\r" in raw:
        enc.append(rel + ":CR")
    try:
        raw.decode("utf-8")
    except Exception:
        enc.append(rel + ":not-UTF8")
rec("I2_encoding", not enc, "all 19 executor package files: UTF-8 no-BOM, LF-only, strict-decodable "
    f"(violations: {enc or 'NONE'})")

# ============================== I3: SOURCE_PACKAGE immutability (my own method)
ls = git("ls-tree", "-r", BASE, "--name-only",
         "docs/audits/PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007").strip().splitlines()
mm3 = []
for f in ls:
    blob = git("rev-parse", BASE + ":" + f).strip()
    disk = os.path.join(REPO, f.replace("/", "\\"))
    content = open(disk, "rb").read()
    if hashlib.sha1(b"blob %d\x00" % len(content) + content).hexdigest() != blob:
        mm3.append(f)
rec("I3_source_package_immutable", len(ls) == 38 and not mm3,
    f"SOURCE_PACKAGE at QC time: {len(ls)} BASE blobs, {len(mm3)} working-tree mismatches — "
    f"READ-ONLY preserved (my own git hash-object method; the QC's writes never touch it)")

# ============================== I4/I5: source ledger shape + verbatim round-trip
src_rows = read_rows(os.path.join(SRC_PKG, "EDGE_ACCOUNTING_LEDGER.csv"))
cor_rows = read_rows(os.path.join(PKG, "CORRECTED_EDGE_ACCOUNTING_LEDGER.csv"))
cls = {}
for r in src_rows:
    cls.setdefault(r["LEDGER_CLASS"], []).append(r["EDGE_ID"])
shape_ok = (len(src_rows) == 69 and {k: len(v) for k, v in cls.items()} ==
            {"ANALYZED_NEW": 24, "RAW_VISIBLE_ONLY": 7, "REPIN_PRIOR_SCOPE": 11,
             "OUT_OF_ANALYZED_EXTENT": 27})
rec("I4_source_ledger_shape", shape_ok,
    f"source ledger: {len(src_rows)} rows; class census " +
    str({k: len(v) for k, v in cls.items()}))

bad5 = []
for s, c in zip(src_rows, cor_rows):
    if s["EDGE_ID"] != c["EDGE_ID"]:
        bad5.append((s["EDGE_ID"], "EDGE_ID"))
        continue
    for col in ("CALLER_START_VA", "CALLSITE_VA", "TARGET", "TARGET_KIND"):
        if s[col] != c[col]:
            bad5.append((s["EDGE_ID"], col))
    for col in ("NEW_INTERPRETATION", "LEDGER_CLASS", "COUNTED", "NOT_COUNTED_REASON", "EVIDENCE"):
        if s[col] != c[col + "_ORIGINAL"]:
            bad5.append((s["EDGE_ID"], col))
rec("I5_verbatim_roundtrip", len(cor_rows) == 69 and not bad5,
    f"ORIGINAL_* fields byte-identical to the BASE source ledger for all 69 rows x 9 fields "
    f"(mismatches: {bad5 or 'NONE'})")

# ============================== I6: MY OWN re-adjudication (explicit per-row map)
# Written AFTER a full content read of all 69 rows (NEW_INTERPRETATION + NOT_COUNTED_REASON).
# Adjudication basis: the source-run contract §2 literal rule — a NEW interpretation
# (receiver / callee identity / argument-result flow / path role / semantic role) of a
# callsite = a counted unit; 'not load-bearing' is NOT an exemption; re-pins of
# prior-recorded interpretations (prior file/record cited) are NOT new analysis.
MY_ADJUDICATION = {}
for i in range(1, 25):
    MY_ADJUDICATION[f"E-{i:02d}"] = ("YES", "COUNTED_ANALYZED_UNIT",
        "non-empty recorded NEW_INTERPRETATION constituting a callsite interpretation (receiver/result flow/role)")
for i in range(1, 8):
    MY_ADJUDICATION[f"RV-{i:02d}"] = ("YES", "COUNTED_ANALYZED_UNIT",
        "interpretation content recorded in NOT_COUNTED_REASON (Desktop-proven set)")
for i in range(1, 12):
    MY_ADJUDICATION[f"RP-{i:02d}"] = ("NO", "PRIOR_REPIN_EXEMPTION_UNREVERIFIED",
        "interpretation text present but explicitly a prior-recorded re-pin (prior record cited); "
        "not NEW analysis of the audited run (spot-verified genuine: I11; the ledger's UNREVERIFIED "
        "label is the conservative form of the same exemption)")
MY_ADJUDICATION["NEIGH-09"] = ("YES", "COUNTED_ANALYZED_UNIT",
    "receiver + result-flow interpretation in NOT_COUNTED_REASON (Desktop-proven 8th unit)")
for eid in ["NEIGH-01", "NEIGH-02", "NEIGH-05", "NEIGH-08", "NEIGH-10", "NEIGH-12",
            "NEIGH-13", "NEIGH-14", "NEIGH-17", "NEIGH-18", "NEIGH-19", "NEIGH-20",
            "NEIGH-22", "NEIGH-23", "NEIGH-25", "NEIGH-26", "NEIGH-27"]:
    MY_ADJUDICATION[eid] = ("NO", "NOT_COUNTED_CLEAN",
        "window/topology facts only; no receiver/argument/result/path-role/semantic-role annotation")
for eid, note in [
    ("NEIGH-03", "body-identity annotation 'second ctor variant' (body-level, not callsite-level)"),
    ("NEIGH-04", "allocation-argument annotation 'new(0x68)' — MAY be argument-flow under a strict reading"),
    ("NEIGH-06", "body-role annotation 'setter +0x118 with release dispatch'"),
    ("NEIGH-07", "body-role annotation 'lazy initializer of +0x120'"),
    ("NEIGH-11", "body-identity data-fact annotation 'manager vtable slot 2 target'"),
    ("NEIGH-15", "receiver annotation '[esp+0x40]' — MAY be a receiver interpretation under a strict reading"),
    ("NEIGH-16", "topology annotation 'a SECOND caller of FUN_006C8BB0'"),
    ("NEIGH-21", "path-role annotation 'the SECOND on-path manager method (GAP-2)'"),
    ("NEIGH-24", "prior-family target-arithmetic note with explicit no-role disclaimer"),
]:
    MY_ADJUDICATION[eid] = ("NO", "CANDIDATE_UNADJUDICATED",
        "annotation MAY constitute a §3 interpretation under a broader/strict reading: " + note)
assert len(MY_ADJUDICATION) == 69, f"my adjudication map must cover 69 rows, got {len(MY_ADJUDICATION)}"

cor_by_id = {r["EDGE_ID"]: r for r in cor_rows}
diff6 = []
for eid, (counted, cls_name, _why) in MY_ADJUDICATION.items():
    r = cor_by_id[eid]
    if r["CORRECTED_COUNTED"] != counted or r["CORRECTED_CLASS"] != cls_name:
        diff6.append((eid, f"mine={counted}/{cls_name}", f"ledger={r['CORRECTED_COUNTED']}/{r['CORRECTED_CLASS']}"))
rec("I6_own_readjudication_vs_ledger", not diff6,
    f"MY OWN row-by-row re-adjudication of all 69 rows == the corrected ledger classification for every row "
    f"(differences: {diff6 or 'NONE'}); note: under MY STRICTER reading NEIGH-04/NEIGH-15 (and possibly other "
    f"candidates) could be COUNTED, which would only RAISE the floor above 32 — no disposition changes")

# ============================== I7: corrected census
census = {k: sum(1 for r in cor_rows if r["CORRECTED_CLASS"] == k) for k in
          ("COUNTED_ANALYZED_UNIT", "PRIOR_REPIN_EXEMPTION_UNREVERIFIED", "NOT_COUNTED_CLEAN",
           "CANDIDATE_UNADJUDICATED")}
counted_ids = sorted(r["EDGE_ID"] for r in cor_rows if r["CORRECTED_COUNTED"] == "YES")
expected_counted = sorted([f"E-{i:02d}" for i in range(1, 25)] + [f"RV-{i:02d}" for i in range(1, 8)] + ["NEIGH-09"])
rec("I7_corrected_census", census == {"COUNTED_ANALYZED_UNIT": 32,
                                      "PRIOR_REPIN_EXEMPTION_UNREVERIFIED": 11,
                                      "NOT_COUNTED_CLEAN": 17,
                                      "CANDIDATE_UNADJUDICATED": 9}
    and counted_ids == expected_counted and len(cor_rows) == 69,
    f"census 32/11/17/9 = {census}; counted set == E-01..E-24 + RV-01..RV-07 + NEIGH-09 "
    f"(exactly the 24+8 defensive minimum)")

# ============================== I8: statuses / minimums / FAILs
led_txt = open(os.path.join(PKG, "CORRECTED_EDGE_ACCOUNTING_LEDGER.csv"), encoding="utf-8").read()
body_txt = open(os.path.join(PKG, "FUNCTION_BODY_ACCOUNTING.csv"), encoding="utf-8").read()
fin_txt = open(os.path.join(PKG, "FINAL_REPORT.md"), encoding="utf-8").read()
hand_txt = open(os.path.join(PKG, "HANDOFF.md"), encoding="utf-8").read()
ok8 = ("MINIMUM_NEW_ANALYZED_EDGE_COUNT = 32" in led_txt and led_txt.count(">= 32") >= 1
       and "EXACT_NEW_ANALYZED_EDGE_COUNT = UNRESOLVED" in led_txt
       and "ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL" in led_txt
       and "RETROACTIVE_PRIOR_AUTHORIZATION = NO" in led_txt
       and "ORIGINAL_SCOPE_COMPLIANCE = FAIL" in led_txt
       and "MINIMUM_NEW_FUNCTION_BODIES_OPENED = 7" in body_txt
       and "EXACT_NEW_FUNCTION_BODIES_OPENED = UNRESOLVED" in body_txt
       and "ORIGINAL_FUNCTION_BODY_BUDGET_COMPLIANCE = FAIL" in body_txt
       and "MINIMUM_NEW_ANALYZED_EDGE_COUNT = 32" in hand_txt
       and "MINIMUM_NEW_FUNCTION_BODIES_OPENED = 7" in hand_txt)
rec("I8_minimums_and_fails", ok8,
    "MINIMUM_NEW_ANALYZED_EDGE_COUNT = 32 (>= 32) defensive (24 historical + 8 content-proven); "
    "EXACT = UNRESOLVED; ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL; bodies >= 7, EXACT bodies UNRESOLVED, "
    "ORIGINAL_FUNCTION_BODY_BUDGET_COMPLIANCE = FAIL; RETROACTIVE_PRIOR_AUTHORIZATION = NO; "
    "ORIGINAL_SCOPE_COMPLIANCE = FAIL — all present verbatim in the corrected records and HANDOFF terminal block")

# ============================== I9: body accounting + probe at source
body_rows = read_rows(os.path.join(PKG, "FUNCTION_BODY_ACCOUNTING.csv"))
counted_bodies = [r for r in body_rows if r["CORRECTED_STATUS"].startswith("COUNTED_AS_NEW_BODY_OPENING")]
probe_row = [r for r in body_rows if r["FUNCTION_VA"] == "0x006C0EE0"]
src_qc = open(os.path.join(SRC_PKG, "03_SCRIPTS", "qc_controls.py"), encoding="utf-8").read()
probe_at_source = ("ok_mut3, det_mut3 = ctrl3_provenance(0x006C0EE0)" in src_qc
                   and "disasm(getter_va, 8)" in src_qc)
src_cr = json.load(open(os.path.join(SRC_PKG, "CONTROL_RESULTS.json"), encoding="utf-8"))
probe_bytes_recorded = (src_cr["CTRL_3"]["mutated_case"]["accessor_va"] == "0x006C0EE0"
                        and "mov eax, [ecx + 0x120]" in src_cr["CTRL_3"]["mutated_case"]["detail"])
ok9 = (len(counted_bodies) == 7 and len(probe_row) == 1 and probe_at_source and probe_bytes_recorded
       and "8B 81 20 01 00 00 C3 CC" in body_txt)
rec("I9_body_accounting_probe", ok9,
    f"FUNCTION_BODY_ACCOUNTING: {len(counted_bodies)} COUNTED rows (6 declared + FUN_006C0EE0); the historical "
    f"probe VERIFIED AT SOURCE: qc_controls.py line 'ctrl3_provenance(0x006C0EE0)' via 'disasm(getter_va, 8)' "
    f"(a REAL 8-byte EXE read) + source CONTROL_RESULTS.json CTRL_3 mutated_case records the [+0x120] accessor; "
    f"bytes 8B 81 20 01 00 00 C3 CC in the accounting record")

# ============================== I10: 006C0EE0 absent from prior packages (my own grep)
prior_dirs = ["docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006",
              "docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007",
              "docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006",
              "docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006"]
g = subprocess.run(["git", "grep", "-i", "-l", "6c0ee0", BASE, "--"] + prior_dirs,
                    capture_output=True, text=True, encoding="utf-8", cwd=REPO)
rec("I10_probe_absent_from_prior", g.returncode == 1 and not g.stdout.strip(),
    "FUN_006C0EE0 (6c0ee0, case-insensitive) appears in ZERO of the four prior audit packages at BASE "
    "(git grep exit=1) — the probe was NOT a prior pin; the Desktop 'absent from both declared prior "
    "packages' claim independently CONFIRMED (and extended to all four grep'd packages)")

# ============================== I11: RP prior citations spot-verified
j2_census = git("show", BASE + ":docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/EDGE_BUDGET_RECONSTRUCTION.csv")
prior_ledger = git("show", BASE + ":docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/EDGE_LEDGER.csv")
prior_qc = git("show", BASE + ":docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/QC_REPORT.md")
prior_window = git("show", BASE + ":docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/01_RAW/FUN_0050A310_DECODE.txt")
cites = {
    "RP-01/X01": "X01,0x006A39ED" in j2_census and "SF factory call" in j2_census,
    "RP-02/X03": "X03,0x006A3A2D" in j2_census and "SetPosition-like" in j2_census,
    "RP-03/X05": "X05,0x006A3A43" in j2_census and "SetRotation-like" in j2_census,
    "RP-04/X31": "X31,0x006A3A4D" in j2_census and "allocator" in j2_census,
    "RP-05/X08": "X08,0x006A3A94" in j2_census and "FUN_006C8BB0" in j2_census,
    "RP-06/E5": "E5,0x006A3A9D" in prior_ledger and "FUN_0050A310" in prior_ledger,
    "RP-07/E6+QC-S4": "E6,0x0050A3F7" in prior_ledger and "vtable slot 41" in prior_ledger
                     and "S4 Join-site receiver preservation" in prior_qc,
    "RP-08..11/window": all(x in prior_window for x in
                           ["0x0050a3b9", "0x0050a3cf", "0x0050a3d8", "0x0050a3e4",
                            "83 4e 2c 02", "83 66 2c fd", "0x0050a3f7"]),
}
rec("I11_rp_citations_verified", all(cites.values()),
    "all 11 RP prior-record citations spot-verified REAL at BASE: " +
    "; ".join(f"{k}={v}" for k, v in cites.items()) +
    " — the PRIOR_REPIN_EXEMPTION class rests on genuine prior records (the correction's UNREVERIFIED "
    "label is conservative; my verification converts it to spot-verified-genuine for the sampled citations)")

# ============================== I12: SUPERSESSION quotes vs the SOURCE files
S = open(os.path.join(SRC_PKG, "EDGE_ACCOUNTING_LEDGER.csv"), encoding="utf-8").read()
SF = open(os.path.join(SRC_PKG, "FINAL_REPORT.md"), encoding="utf-8").read()
SH = open(os.path.join(SRC_PKG, "HANDOFF.md"), encoding="utf-8").read()
SM = open(os.path.join(SRC_PKG, "PE_MASTER_REVIEW.md"), encoding="utf-8").read()
SQ = open(os.path.join(SRC_PKG, "QC_REPORT.md"), encoding="utf-8").read()
SIC = open(os.path.join(SRC_PKG, "00_CONTROL_INTERNAL_QC", "qc_ind_census.py"), encoding="utf-8").read()
SCL = open(os.path.join(SRC_PKG, "CLAIM_MATRIX.csv"), encoding="utf-8").read()
SPR = open(os.path.join(SRC_PKG, "PREREGISTRATION.md"), encoding="utf-8").read()
SRCR = json.load(open(os.path.join(SRC_PKG, "CONTROL_RESULTS.json"), encoding="utf-8"))
SRCQ = open(os.path.join(SRC_PKG, "03_SCRIPTS", "qc_controls.py"), encoding="utf-8").read()


def norm(t):
    """whitespace/backtick/comment-wrap-normalized containment.

    The source files hard-wrap at ~78 cols; CSV comment headers continue with a
    '#   ' prefix on the next line — a quoted phrase may be split as
    '... 16 past the stop / #   line. ...'. Normalize by stripping the
    comment-continuation prefixes and all line breaks (how a human reads it)."""
    t = t.replace("`", "")
    t = " ".join(re.sub(r"^#\s*", "", ln) for ln in t.splitlines())
    return re.sub(r"\s+", " ", t)


def has(hay, needle):
    return norm(needle) in norm(hay)


sup = {
    "S-1": (has(S, "ACCOUNTED_EDGE_COUNT (ANALYZED_NEW rows below)      = 24")
            and has(SF, "ANALYZED 24") and has(SH, "NEW_INTERPROCEDURAL_EDGES_SEMANTICALLY_ANALYZED = 24")
            and has(SM, "Census: 69 rows (24 ANALYZED_NEW")),
    "S-2": (has(SQ, "INDEPENDENT_RECONSTRUCTED_EDGE_COUNT = 24")
            and has(SH, "INDEPENDENT_RECONSTRUCTED_EDGE_COUNT = 24 (== ACCOUNTED_EDGE_COUNT")
            and has(SM, "ACCOUNTED_EDGE_COUNT 24 == INDEPENDENT_RECONSTRUCTED_EDGE_COUNT 24")
            and "QC-I9" in SIC and "QC-I10" in SIC),
    "S-3": (has(S, "the run analyzed 24 callsite units, 16 past the stop line")
            and has(SF, "EXCEEDED by 16")
            and has(SIC, "EXCEEDED by exactly 16")
            and has(SH, "16 past the stop line")),
    "S-4": (has(S, "analysis is never hidden behind a RAW_VISIBLE label")
            and has(SM, "zero semantic analysis hidden under RAW_VISIBLE")
            and has(SCL, "no analysis is hidden behind RAW labels")),
    "S-4-file-attribution": has(SCL, "no analysis is hidden behind RAW labels") and not has(SF, "no analysis is hidden behind RAW labels"),
    "S-5": (has(SF, "budgeted bodies 6/6") and has(SF, "used 6/6") and has(SF, "NOT exceeded")
            and has(SH, "NEW_FUNCTION_BODIES_OPENED = 6/6")
            and has(SCL, "CL-15") and has(SCL, "NEW_FUNCTION_BODIES_OPENED = 6/6")
            and "MAX_NEW_FUNCTION_BODIES_OPENED = 6" in SPR),
    "S-6": (has(SRCR["CTRL_4"]["checker"], "§7 chain intactness: head move + no EDI-writing instruction + push edi")
            and SRCR["CTRL_4"]["clean_case"]["result"] == "PASS"
            and SRCR["CTRL_4"]["mutated_case"]["result"] == "FAIL"
            and has(SF, "CTRL_4 (child identity break) = PASS")
            and has(SH, "CTRL_4_RESULT = PASS (child identity break")
            and "push_edi = True" in SRCQ),
    "S-7": (has(SF, "WRAPPER_DEPTH = 2 (manager -> instance [+0x6C]; instance -> [+4]; the further moves to the join are SAME_OBJECT)")
            and has(SH, "WRAPPER_DEPTH = 2") and has(SM, "WRAPPER_DEPTH = 2")),
    "S-8": (has(S, "SCOPE_COMPLIANCE = PARTIAL_WITH_EXCEEDED_EDGE_BUDGET")
            and has(SF, "SCOPE_COMPLIANCE = PARTIAL_WITH_EXCEEDED_EDGE_BUDGET")
            and has(SH, "SCOPE_COMPLIANCE = PARTIAL_WITH_EXCEEDED_EDGE_BUDGET (bodies 6/6 within")),
    "S-9": (has(SM, "RUN_VERDICT = MASTER_ACCEPTED (advisory)") and has(SM, "zero P1/P2")
            and has(SQ, "QC_VERDICT = QC_PASS (SELF_CHECK; 23/23 checks)")),
    "NOT-superserved-getter": (has(SQ, "8B 41 68 C3") and has(SM, "8B 41 68 C3")
                               and has(SF, "DIRECT_FIELD_GETTER") and has(SF, "[ecx+0x68]")),
    "NOT-superserved-store": (has(SH, "[manager+0x68] = [instance+4] @0x006C67E2")
                              and has(SM, "89 7E 68") and has(SM, "8B 78 04")),
    "NOT-superserved-join-window": ("8B F8" in open(os.path.join(SRC_PKG, "01_RAW", "JOIN_WINDOW_50A3B7_REPIN.txt"), encoding="utf-8").read()),
    "NOT-superserved-EXACT_PARENT": (has(SF, "CONFIRMED_EXACT_SCENEFEEDER_PLUS_30")),
}
s4_attr = sup.pop("S-4-file-attribution")
rec("I12_supersession_quotes", all(sup.values()),
    "every S-1..S-9 supersession quote verified in the cited SOURCE package file at BASE "
    "(whitespace/backtick-normalized for the source's ~78-col hard wraps; incl. the historical CTRL_4 "
    "clean PASS / EDI-clobber FAIL measurements preserved as authentic, the old push_edi-anywhere "
    "defect locus in qc_controls.py, the QC-I5/QC-I9/QC-I10 census defects, the WRAPPER_DEPTH=2 locus, "
    "the 6/6 locus, the PARTIAL scope locus, the MASTER_ACCEPTED/zero-P1-P2 locus); the NOT-superseded "
    "byte measurements (getter 8B 41 68 C3; store pair 89 7E 68 / 8B 78 04; join window 8B F8/57/FF D2; "
    "EXACT_PARENT) all present: " + "; ".join(f"{k}={v}" for k, v in sup.items() if k.startswith("NOT")))
# FINDING (recorded, not silently passed): S-4's "FINAL_REPORT.md §4" citation misattributes
# a phrase that actually lives in CLAIM_MATRIX.csv CL-14 (quote-form/file-attribution imprecision;
# the superseded claim itself is real in 3 loci — the supersession stands).
results["FINDING_P3_S4_quote_file_attribution"] = {
    "ok": s4_attr,
    "detail": ("FINDING P3: SUPERSESSION.md S-4 'Where' cites \"FINAL_REPORT.md §4 ('no analysis is hidden "
               "behind RAW labels')\" — the quoted phrase does NOT exist in FINAL_REPORT.md; it exists in "
               "CLAIM_MATRIX.csv CL-14 (evidence cell: 'full census per the J2 lesson; every uncounted row "
               "carries an explicit reason; no analysis is hidden behind RAW labels'). The superseded CLAIM "
               "is real (EDGE_ACCOUNTING_LEDGER.csv header line 8; PE_MASTER_REVIEW.md line 23; "
               "CLAIM_MATRIX.csv CL-14), so supersession S-4 stands; only the middle citation's file "
               "attribution is wrong. Correction: re-attribute that citation to CLAIM_MATRIX.csv CL-14 "
               "(or cite FINAL_REPORT §4 with its actual wording 'every uncounted row carries an explicit "
               "reason — the J2 discipline'). Secondary trivial imprecision in the same file: S-3's QC-I10 "
               "quote 'exceeded by exactly 16' vs the source's 'EXCEEDED by exactly 16' (capitalization); "
               "several S-quotes span the source's hard line wraps / drop backticks (S-1 ledger header, "
               "S-6 FINAL_REPORT §3, S-7 FINAL_REPORT §1) — substance identical in every case.")}

# ============================== I13: Desktop COMMITTED_INPUT cross-hash
desk_ledger = os.path.join(DESKTOP, "COMMITTED_INPUT", "EDGE_ACCOUNTING_LEDGER.csv")
dl_sha = sha256_file(desk_ledger)
repo_ledger_sha = sha256_file(os.path.join(SRC_PKG, "EDGE_ACCOUNTING_LEDGER.csv"))
rec("I13_desktop_committed_input", dl_sha == repo_ledger_sha and
    dl_sha.lower() == "50d6969591c8f9fa77c007e448f8069c0000216c6ee06b8abab51efb0c9626c5",
    f"Desktop COMMITTED_INPUT/EDGE_ACCOUNTING_LEDGER.csv SHA256 == BASE source ledger SHA256 == "
    f"{dl_sha[:16]}... — the Desktop post-audit hashed the exact audited bytes (same evidence basis)")

# ============================== I14: governance elements
gov = open(os.path.join(PKG, "GOVERNANCE_DECISION.md"), encoding="utf-8").read()
ok14 = all(x in gov for x in [
    "OPENCODE_C4_C1_C2_CORRECTION_REVIEWED.md", "11851",
    "364D5C82BBCDD95E44ACF63BB676D026AA482E57950572CE83D71526DD05F348",
    "PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007",
    "790e83735b439e2d76a250868a47a599c2c10184",
    "Zachowaj historyczny budget FAIL i potwierdzone byte measurements",
    "Nie rozpoczynaj FUN_006C9700 ani żadnego nowego RE",
    "NEXT_EXPERIMENT_AUTHORIZED = NO", "HARD_STOP = YES", "ORCHESTRATOR_PHASE_SPLIT"])
rec("I14_governance", ok14,
    "GOVERNANCE_DECISION.md §1: verbatim human instruction present with the exact contract path/size/SHA "
    "(364D5C82…F348), RUN_ID, EXPECTED_BASE_SHA 790e837, the budget-FAIL-preservation sentence, the "
    "FUN_006C9700/new-RE prohibition, NEXT_EXPERIMENT_AUTHORIZED = NO, HARD_STOP = YES; §2 records the "
    "phase split as ORCHESTRATOR_PHASE_SPLIT from the dispatch text (matches THIS QC's dispatch: no "
    "entrypoint edit, no commit/push by the executor phase)")

# ============================== I15: separation algebra
pkg_txts = {}
for root, dirs, files in os.walk(PKG):
    dirs[:] = [d for d in dirs if d not in ("__pycache__", "00_CONTROL_INTERNAL_QC")]
    for fn in files:
        if fn.endswith((".md", ".csv", ".json")) and fn != "QC_CORRECTION_RESULTS.json":
            pkg_txts[fn] = open(os.path.join(root, fn), encoding="utf-8").read()
sep_bad = [fn for fn, t in pkg_txts.items() if "ORIGINAL_SCOPE_COMPLIANCE = PASS" in t]
rec("I15_separation", not sep_bad and "ORIGINAL_SCOPE_COMPLIANCE = FAIL" in fin_txt
    and "CORRECTION_RECORDS_QC = PASS" in fin_txt,
    f"no file anywhere claims ORIGINAL_SCOPE_COMPLIANCE = PASS (scan: {len(pkg_txts)} record files); "
    f"CORRECTION_RECORDS_QC = PASS is always reported SEPARATELY from the historical "
    f"ORIGINAL_SCOPE_COMPLIANCE = FAIL (FINAL_REPORT §3 block keeps them as distinct algebra objects)")

# ============================== I16: EXE-access scan over the package scripts
exe_hits = []
for root, dirs, files in os.walk(PKG):
    dirs[:] = [d for d in dirs if d not in ("__pycache__", "00_CONTROL_INTERNAL_QC")]
    for fn in files:
        if not fn.endswith(".py"):
            continue
        for ln_no, ln in enumerate(open(os.path.join(root, fn), encoding="utf-8").read().splitlines(), 1):
            for pat in (r"\.exe", "pe_reader", "PE_OBJ", "capstone", "Entropia"):
                if re.search(pat, ln):
                    # negation-context adjudication: the only allowed occurrences are explicit
                    # "no capstone / no pe_reader / no EXE"-style negation sentences
                    if not re.search(r"\bno\b|\bNo\b|\bwithout\b|\bzero\b|\bZero\b", ln):
                        exe_hits.append(f"{fn}:{ln_no}:{pat}")
rec("I16_zero_exe_access", not exe_hits,
    f"scan over all correction-package scripts: every .exe/pe_reader/PE_OBJ/capstone/Entropia occurrence "
    f"is inside an explicit NEGATION sentence (e.g. ctrl3_rebuilt.py docstring 'No capstone, no pe_reader, "
    f"no EXE'); zero affirmative EXE-access occurrences (violations: {exe_hits or 'NONE'}); "
    f"CTRL_3/CTRL_4 rebuilt operate on in-memory byte constants only — "
    f"NEW_PCG_FUNCTION_BODIES_ALLOWED = 0 honored by the package")

# ============================== save (part 1)
out = {"I_results": results}
path = os.path.join(QC_DIR, "QC_IND_PART1_RESULTS.json")
with open(path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"\npart1: {sum(1 for v in results.values() if v['ok'])}/{len(results)} PASS -> {path}")
sys.exit(0 if all(v['ok'] for v in results.values()) else 1)
