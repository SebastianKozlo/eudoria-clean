"""qc_correction.py — fresh-context internal QC (SELF_CHECK) of
PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007.

Contract §9/§10 of OPENCODE_J1_J3_CORRECTION_REVIEWED.md. This QC independently tests the
J1/J2/J3 corrections against the SOURCE_RUN_PACKAGE materials at BASE 064b7f4 (read as
physical files ONLY after verifying them byte-identical to the BASE git blobs) and against
the pinned EXE (re-verification of already-published pins only — NO new RE). The QC does not
repair executor records in place; it records its own findings to
03_SCRIPTS/qc_correction_results.json.

Self-classification: this is the executor's own fresh-context internal QC (SELF_CHECK). It is
NOT an independent external Desktop post-audit and NOT a PE-MASTER qualification.
"""
import csv
import hashlib
import io
import json
import os
import struct
import subprocess
import sys

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
PKG = os.path.join(REPO, "docs", "audits",
                   "PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007")
SRC = os.path.join(REPO, "docs", "audits",
                   "PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006")
BASE = "064b7f4aa4f3961f1a44212b2423e298eb51c291"
SRC_AGG_EXPECT = "ab21cbc3991c91b19bd884f851e0fe24f1eba251b48e24643a71f6169be65b5b"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
OUT = os.path.join(PKG, "03_SCRIPTS", "qc_correction_results.json")

res = {"checks": {}, "findings": [], "self_classification":
       "executor fresh-context internal QC (SELF_CHECK); NOT independent Desktop post-audit; "
       "NOT PE-MASTER qualification"}


def chk(name, ok, detail):
    res["checks"][name] = {"ok": bool(ok), "detail": detail}
    if not ok:
        res["findings"].append(f"FAILED CHECK {name}: {detail}")


# ---------------------------------------------------------------- pinned EXE
data = open(EXE, "rb").read()
exe_ok = len(data) == 8015872 and hashlib.sha256(data).hexdigest().upper() == \
    "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
chk("X0_exe_identity", exe_ok,
    f"size {len(data)}; sha {hashlib.sha256(data).hexdigest().upper()}")
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
coff = e_lfanew + 4
nsec = struct.unpack_from("<H", data, coff + 2)[0]
size_opt = struct.unpack_from("<H", data, coff + 16)[0]
sec0 = coff + 20 + size_opt
sections = []
for i in range(nsec):
    off = sec0 + 40 * i
    vsize, va, rsize, roff = struct.unpack_from("<IIII", data, off + 8)
    sections.append((va, max(vsize, rsize), roff))


def read(va, n):
    rva = va - 0x400000
    for va_s, sz, roff in sections:
        if va_s <= rva < va_s + sz:
            return data[roff + (rva - va_s):roff + (rva - va_s) + n]
    raise ValueError(f"VA {va:#x} unmapped")


# ------------------------------------------------- source package re-hash (J3)
out = subprocess.run(["git", "ls-tree", "-r", BASE, "--",
                      "docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/"],
                     cwd=REPO, capture_output=True, text=True).stdout
blob_rows = [l.split("\t") for l in out.splitlines() if l.strip()]
mism = []
digest_lines = []
for meta, path in blob_rows:
    _, typ, gsha = meta.split()
    fp = os.path.join(REPO, *path.split("/"))
    if not os.path.isfile(fp):
        mism.append(f"MISSING {path}")
        continue
    b = open(fp, "rb").read()
    bsha = hashlib.sha1(b"blob %d\x00" % len(b) + b).hexdigest()
    if bsha != gsha:
        mism.append(f"BLOB_MISMATCH {path}")
    digest_lines.append(path + " " + hashlib.sha256(b).hexdigest())
agg = hashlib.sha256(("\n".join(sorted(digest_lines)) + "\n").encode()).hexdigest()
chk("J3a_source_package_unchanged",
    len(blob_rows) == 49 and not mism and agg == SRC_AGG_EXPECT,
    f"49 BASE blobs; physical-vs-blob mismatches: {mism if mism else 'NONE'}; "
    f"aggregate {agg}; expected {SRC_AGG_EXPECT}")

f509850 = open(os.path.join(SRC, "01_RAW", "FUN_00509850_FULL.txt"), "rb").read()
chk("J3d_transform_evidence_file_unchanged",
    hashlib.sha1(b"blob %d\x00" % len(f509850) + f509850).hexdigest() ==
    [m.split()[2] for m, p in blob_rows if p.endswith("01_RAW/FUN_00509850_FULL.txt")][0],
    "01_RAW/FUN_00509850_FULL.txt (the J3 physical transform record) byte-identical to its BASE blob")

# ------------------------------------------------------------- J3 record labels
alg = open(os.path.join(PKG, "CORRECTED_STATUS_ALGEBRA.md"), encoding="utf-8").read()
sec_a = alg.split("## B.")[0]
chk("J3b_incidental_labels_present",
    "NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION" in alg
    and "SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE" in alg
    and "PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED" in alg,
    "corrected records label the new transform trace incidental/out-of-scope and preserve the measurements")
chk("J3c_no_active_transform_promotion_survives",
    "CONFIRMED_STATIC" not in sec_a,
    "CORRECTED_STATUS_ALGEBRA.md section A (ACTIVE statuses) contains no CONFIRMED_STATIC "
    "promotion; the historical value appears only in superseded/historical context")

# --------------------------------------------------------------------- J1
gate = json.load(open(os.path.join(PKG, "03_SCRIPTS", "gate_corrected_results.json"),
                      encoding="utf-8"))
cx = json.load(open(os.path.join(PKG, "GATE_COUNTEREXAMPLES.json"), encoding="utf-8"))
c = gate["cases"]
chk("J1_gate_overall_pass", gate["OVERALL"] == "PASS" and all(gate["self_checks"].values()),
    "corrected gate self-checks all true")
chk("J1_M1_to_M5_not_qualified",
    all(c[f"M{i}"]["SCIENCE_QUALIFICATION"]["verdict"] == "NOT_QUALIFIED" for i in range(1, 6)),
    "M1–M5 all NOT QUALIFIED on the corrected production gate")
chk("J1_M4_M5_mechanical_catch",
    c["M4"]["MECHANICAL_VERDICT"] == "FAIL" and c["M5"]["MECHANICAL_VERDICT"] == "FAIL"
    and any(f.startswith("P_CONNECT_FAIL") for f in c["M4"]["STRUCTURAL_CONSISTENCY_CHECK"]["failures"])
    and any("SYNTHETIC_MARKING_INCONSISTENCY" in f for f in c["M5"]["SCHEMA_CHECK"]["failures"]),
    "M4 broken-connectivity and M5 synthetic->real relabel each fail a MECHANICAL predicate "
    "(clean PASS -> mutated FAIL on the same checker)")
chk("J1_M1_M2_M3_policy_rejection_disclosed",
    all(c[f"M{i}"]["MECHANICAL_VERDICT"] == "PASS" for i in (1, 2, 3))
    and all(c[f"M{i}"]["SCIENCE_QUALIFICATION"]["verdict"] == "NOT_QUALIFIED" for i in (1, 2, 3))
    and "ABSENCE OF AUTOMATIC SCIENCE PROMOTION" in cx["policy_disclosure"],
    "M1/M2/M3 pass mechanically and are rejected BY POLICY (honestly disclosed: no detection "
    "of a specific wrong opcode/endpoint; PIN_CHECK is byte-equality only)")
chk("J1_ctrl_abc_retained_causal",
    all(c[n]["MECHANICAL_VERDICT"] == "FAIL" for n in ("CTRL_A", "CTRL_B", "CTRL_C"))
    and any(f.startswith("P_PARENT_FAIL") for f in c["CTRL_A"]["STRUCTURAL_CONSISTENCY_CHECK"]["failures"])
    and any(f.startswith("P_CHILD_FAIL") for f in c["CTRL_B"]["STRUCTURAL_CONSISTENCY_CHECK"]["failures"])
    and any(f.startswith("P_PARENT_FAIL") for f in c["CTRL_C"]["STRUCTURAL_CONSISTENCY_CHECK"]["failures"]),
    "original CTRL-A/B/C retained; each FAILs by its proper mechanical predicate")
chk("J1_synthetic_clean_machinery_only",
    c["synthetic_clean_control"]["MECHANICAL_VERDICT"] == "PASS"
    and c["synthetic_clean_control"]["SCIENCE_QUALIFICATION"]["verdict"] == "SYNTHETIC_MACHINERY_TEST_ONLY",
    "clean synthetic fixture PASSES only as a machinery test (never science)")
chk("J1_real_cand4_remains_not_qualified",
    c["real_CAND4_clean_unresolved"]["SCIENCE_QUALIFICATION"]["verdict"] == "NOT_QUALIFIED"
    and c["real_CAND4_clean_unresolved"]["MECHANICAL_VERDICT"] == "FAIL",
    "real CAND-4 (A/D unresolved) remains NOT QUALIFIED")
chk("J1_no_science_pass_anywhere",
    all(r["SCIENCE_QUALIFICATION"]["verdict"] != "SCIENCE_PASS" for r in c.values()),
    "no case receives SCIENCE_PASS")
chk("J1_no_id_hard_coding",
    all(p["verdicts_identical"] for p in gate["id_hard_coding_probes"].values()),
    "renamed-chain probes return identical verdicts (no candidate/mutation-ID rejection branch)")
# independent re-verification of the real chain's 5 pins (own reads)
pin_expect = {0x006A39ED: "E8 CE 0D E8 FF", 0x006A39F6: "89 46 18",
              0x0050A3E9: "8B 4E 30", 0x0050A3F7: "FF D2", 0x007B5846: "01 5E 04"}
pin_ok = all(" ".join(f"{b:02X}" for b in read(va, len(e.split()))) == e
             for va, e in pin_expect.items())
chk("J1_real_chain_pins_reverified_from_exe", pin_ok,
    "the 5 published real-chain byte pins independently re-read from the pinned EXE — MATCH "
    "(re-verification of already-published pins only; no new RE)")

# --------------------------------------------------------------------- J2
census_path = os.path.join(PKG, "EDGE_BUDGET_RECONSTRUCTION.csv")
raw_lines = open(census_path, encoding="utf-8").read().splitlines()
data_lines = [l for l in raw_lines if not l.startswith("#")]
rows = list(csv.DictReader(io.StringIO("\n".join(data_lines))))
counted = [r for r in rows if r["COUNTED_IN_MINIMUM"] == "YES"]
pairs = {(r["CALLER"], r["CALLEE"]) for r in counted}
mandated = [r for r in rows if r["CALLSITE_VA"] == "0x0050A3AF" and r["CALLEE"] == "FUN_006C66D0"]
chk("J2_census_parses", len(rows) == 70 and len(data_lines) == len(rows) + 1,
    f"census rows {len(rows)}; header + 70 data rows")
chk("J2_counted_rows", len(counted) == 21,
    "COUNTED_IN_MINIMUM=YES rows = 21 (E1–E6 + R01–R15)")
chk("J2_distinct_pairs_minimum_20", len(pairs) == 20 and len(mandated) == 1
    and mandated[0]["RECONSTRUCTION_CLASS"] == "SUMMARY_SEMANTIC_NEW",
    f"distinct counted (caller,callee) pairs = {len(pairs)}; mandated "
    "0x0050A3AF->FUN_006C66D0 present as SUMMARY_SEMANTIC_NEW (R01)")
# ledger cross-check from the BASE source package
src_edge = list(csv.DictReader(open(os.path.join(SRC, "EDGE_LEDGER.csv"), encoding="utf-8")))
src_pra = open(os.path.join(SRC, "PRE_REGISTERED_ANCHORS.md"), encoding="utf-8").read()
src_budget = open(os.path.join(SRC, "FUNCTION_BUDGET.csv"), encoding="utf-8").read()
chk("J2_ledger_has_exactly_6",
    len(src_edge) == 6 and [e["EDGE_ID"] for e in src_edge] == [f"E{i}" for i in range(1, 7)],
    "source EDGE_LEDGER.csv (BASE) has exactly rows E1–E6 — the ledger measured list length")
chk("J2_budget_row7_records_getter_edge",
    "child=FUN_006C66D0(manager) @0x0050A3AF" in src_budget,
    "source FUNCTION_BUDGET row#7 itself records the uncharged getter edge "
    "(receiver=manager; child argument) — independent reconstruction basis")
chk("J2_contractual_max_is_6", "MAX_NEW_INTERPROCEDURAL_EDGES = 6" in src_pra,
    "source PRE_REGISTERED_ANCHORS.md: MAX_NEW_INTERPROCEDURAL_EDGES = 6 (not retroactively changed)")
chk("J2_compliance_fail_recorded",
    "ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL" in alg
    and "MINIMUM_ANALYZED_EDGE_COUNT = 20" in alg
    and "RETROACTIVE_PRIOR_AUTHORIZATION = NO" in alg
    and len(pairs) > 6,
    f"process compliance FAIL recorded: {len(pairs)} minimum analyzed pairs > max 6")
# independent mechanical replay: rel32 targets of direct-E8 census rows + vtable slots
def fun_va(name):
    return int(name.replace("FUN_", ""), 16)


bad_t = []
for r in rows:
    va = int(r["CALLSITE_VA"], 16)
    cal = r["CALLEE"]
    if r["CALL_KIND"] == "DIRECT_E8" and cal.startswith("FUN_"):
        b = read(va, 5)
        if b[0] != 0xE8:
            bad_t.append(f"{r['CENSUS_ID']}: byte0 {b[0]:02X} not E8")
            continue
        tgt = va + 5 + struct.unpack("<i", b[1:5])[0]
        if tgt != fun_va(cal):
            bad_t.append(f"{r['CENSUS_ID']}: rel32 target {tgt:#010x} != {cal}")
    elif r["CALL_KIND"] == "VTABLE_SLOT_41":
        if struct.unpack("<I", read(0x00A8CCF4 + 0xA4, 4))[0] != fun_va(cal):
            bad_t.append(f"{r['CENSUS_ID']}: slot41 != {cal}")
    elif r["CALL_KIND"] == "VTABLE_SLOT_42":
        if struct.unpack("<I", read(0x00A8CCF4 + 0xA8, 4))[0] != fun_va(cal):
            bad_t.append(f"{r['CENSUS_ID']}: slot42 != {cal}")
    elif r["CALL_KIND"] == "VTABLE_SLOT_19":
        if struct.unpack("<I", read(0x00A8CCF4 + 0x4C, 4))[0] != fun_va(cal):
            bad_t.append(f"{r['CENSUS_ID']}: slot19 != {cal}")
    elif r["CALL_KIND"] == "VTABLE_SLOT_45":
        if struct.unpack("<I", read(0x00A8CCF4 + 0xB4, 4))[0] != fun_va(cal):
            bad_t.append(f"{r['CENSUS_ID']}: slot45 != {cal}")
chk("J2_census_targets_mechanically_replayed",
    not bad_t,
    f"rel32/vtable replay of every DIRECT_E8 and VTABLE_SLOT census row against the pinned "
    f"EXE: {bad_t if bad_t else 'ALL MATCH'} (replay of already-published arithmetic; no new RE)")
# no retroactive-authorization / actual-count overclaims in the correction package
# (sweep covers every package file EXCEPT this QC script and its own results file,
#  which legitimately contain the forbidden tokens as check literals)
QC_SELF = {"qc_correction.py", "qc_correction_results.json"}
def package_files():
    for dp, dn, fn in os.walk(PKG):
        for f in sorted(fn):
            if f in QC_SELF:
                continue
            yield os.path.relpath(os.path.join(dp, f), PKG), os.path.join(dp, f)


forbidden = ["RETROACTIVE_PRIOR_AUTHORIZATION = YES", "ORIGINAL_EDGE_BUDGET_COMPLIANCE = PASS",
             "was authorized before", "authorized retroactively"]
hits = []
for rel, fp in package_files():
    txt = open(fp, encoding="utf-8", errors="replace").read()
    for t in forbidden:
        if t in txt:
            hits.append(f"{rel}: {t}")
chk("J2_no_retroactive_authorization_claim", not hits,
    f"forbidden-token sweep of the package (self excluded): {hits if hits else 'CLEAN'}")

# --------------------------------------------------------------------- §10
cm = list(csv.DictReader(open(os.path.join(SRC, "CLAIM_MATRIX.csv"), encoding="utf-8")))
cm_by = {r["CLAIM_ID"]: r for r in cm}
cand = list(csv.DictReader(open(os.path.join(SRC, "CANDIDATE_LEDGER.csv"), encoding="utf-8")))
c4 = [r for r in cand if r["CANDIDATE_ID"] == "CAND-4-ACLD-PATH-SLOT41-ATTACH"][0]
fr = open(os.path.join(SRC, "FINAL_REPORT.md"), encoding="utf-8").read()
src_statuses_ok = (
    "SCIENCE OUTCOME = PARENT_FOUND_CHILD_UNRESOLVED" in fr
    and "CONFIRMED_EXACT_SCENEFEEDER_PLUS_30" in c4["PARENT_STATUS"]
    and c4["JOIN_OPERATION_STATUS"].startswith("STRONGLY_SUPPORTED")
    and "UNRESOLVED" in c4["CHILD_PROVENANCE"] and "UNRESOLVED" in c4["CHILD_ROLE"]
    and cm_by["CL-15"]["STATUS"] == "NOT_ESTABLISHED"
    and cm_by["CL-16"]["STATUS"].startswith("NO") and cm_by["CL-17"]["STATUS"] == "NO"
    and cm_by["CL-18"]["STATUS"] == "NOT_ESTABLISHED" and cm_by["CL-19"]["STATUS"] == "NO")
active_expected = {
    "SCIENCE_OUTCOME = PARENT_FOUND_CHILD_UNRESOLVED",
    "EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30",
    "JOIN_OPERATION = STRONGLY_SUPPORTED",
    "CHILD_MODEL_PROVENANCE = UNRESOLVED",
    "CHILD_VISUAL_ROLE = UNRESOLVED",
    "INSTANCE_MODEL_NODE_JOIN = NOT_ESTABLISHED",
    "WORLD_XYZ_RECOVERED = NO",
    "STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED",
    "HISTORICAL_INSTANCE_DATA_RECOVERED = NO",
}
corrected_ok = all(t in sec_a for t in active_expected)
chk("X1_nine_statuses_unchanged", src_statuses_ok and corrected_ok,
    "the 9 preserved statuses are identical in the source records (BASE) and the corrected "
    "ACTIVE algebra: no unintended science diff")
over_tokens = ["INSTANCE_MODEL_NODE_JOIN = CONFIRMED", "INSTANCE_MODEL_NODE_JOIN=CONFIRMED",
               "CHILD_MODEL_PROVENANCE = CONFIRMED", "CHILD_MODEL_PROVENANCE=CONFIRMED",
               "CHILD_VISUAL_ROLE = CONFIRMED", "CHILD_VISUAL_ROLE=CONFIRMED",
               "RUNTIME_JOIN_OBSERVED = YES", "RUNTIME_JOIN_OBSERVED=YES",
               "WORLD_XYZ_RECOVERED = YES", "WORLD_XYZ_RECOVERED=YES",
               "CONFIRMED_MODEL_DERIVED", "STATIC_BUILDING_CHANNEL = ESTABLISHED",
               "STATIC_BUILDING_CHANNEL=ESTABLISHED",
               "HISTORICAL_INSTANCE_DATA_RECOVERED = YES", "HISTORICAL_INSTANCE_DATA_RECOVERED=YES"]
ohits = []
for rel, fp in package_files():
    txt = open(fp, encoding="utf-8", errors="replace").read()
    for t in over_tokens:
        if t in txt:
            ohits.append(f"{rel}: {t}")
chk("X2_no_new_model_resource_visual_conclusion", not ohits,
    f"overclaim-token sweep of the package (self excluded): {ohits if ohits else 'CLEAN'}")
mark = ["SUPERSEDED", "superseded", "historical", "source run", "source-run", "CL-08",
        "PE_MASTER_REVIEW.md"]
chits = []
for rel, fp in package_files():
    lines = open(fp, encoding="utf-8", errors="replace").read().splitlines()
    for i, line in enumerate(lines):
        if "CONFIRMED_STATIC" in line:
            ctx = "\n".join(lines[max(0, i - 4):i + 5])
            if not any(m in ctx for m in mark):
                chits.append(f"{rel}:{i + 1}")
chk("X3_confirm_static_only_in_supersession_context", not chits,
    f"every CONFIRMED_STATIC occurrence sits in a supersession/historical context "
    f"(line or +/-4 lines around it): {chits if chits else 'CLEAN'}")

# --------------------------------------------------------------------- repo
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
st = subprocess.run(["git", "status", "--porcelain"], cwd=REPO, capture_output=True, text=True).stdout
tracked_mod = [l for l in st.splitlines() if l and not l.startswith("??")]
untracked_roots = sorted(set(l[3:].rstrip("/") for l in st.splitlines() if l.startswith("??")))
known_foreign = {"docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001",
                 "docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003",
                 "docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914",
                 "docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930",
                 "docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928",
                 "experiments",
                 "docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007"}
chk("G1_repo_state", head == BASE and not tracked_mod
    and set(untracked_roots) == known_foreign,
    f"HEAD {head}; tracked modifications: {tracked_mod if tracked_mod else 'NONE'}; "
    f"untracked roots: {untracked_roots}")
pyc = [os.path.join(dp, d) for dp, dn, fn in os.walk(PKG) for d in dn if d == "__pycache__"]
chk("G2_no_pycache", not pyc, f"__pycache__ dirs under OUTPUT_ROOT: {pyc if pyc else 'NONE'}")
bad_enc = []
file_count = 0
for dp, dn, fn in os.walk(PKG):
    for f in fn:
        file_count += 1
        fp = os.path.join(dp, f)
        b = open(fp, "rb").read()
        if b.startswith(b"\xef\xbb\xbf"):
            bad_enc.append(f"{f}: BOM")
        if b"\r" in b:
            bad_enc.append(f"{f}: CR byte")
        try:
            b.decode("utf-8")
        except UnicodeDecodeError:
            bad_enc.append(f"{f}: not UTF-8")
chk("G3_utf8_no_bom_lf", not bad_enc,
    f"all {file_count} package files UTF-8 no-BOM LF: {bad_enc if bad_enc else 'CLEAN'}")

res["package_file_count_at_qc"] = file_count
res["OVERALL"] = "QC_PASS" if all(v["ok"] for v in res["checks"].values()) else "QC_FAIL"
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(res, f, indent=2)
    f.write("\n")
print(json.dumps({"OVERALL": res["OVERALL"],
                  "failed": [k for k, v in res["checks"].items() if not v["ok"]]}, indent=2))
sys.exit(0 if res["OVERALL"] == "QC_PASS" else 1)
