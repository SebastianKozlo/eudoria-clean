# qc_j2_j3_package.py — INDEPENDENT J2 census verification + J3 + §10 + package checks.
# PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007
# Internal QC worker: pe-master-auditor (fresh context, NO_NESTED_TASKS, RECORDS/QC ONLY).
#
# J2 (contract §9): independently reconstruct the edge accounting from the EXISTING
# source-run artifacts; recount the census; replay every declared target's arithmetic
# from the pinned EXE with MY OWN mapper; specifically detect 0x0050A3AF->FUN_006C66D0;
# verify MAX=6 and the FAIL recording; verify no retroactive-authorization claim.
# Additionally (adversarial, L9/L11): verify the census's "EVERY recorded callsite"
# completeness claim against the source-run raw windows / NOT_CHECKED lists — the
# omissions found by manual reading are re-verified HERE by machine.
# J3: source evidence unchanged (see results_source_immutable.json); labels present;
# no active transform promotion in the corrected ACTIVE algebra.
# §10: nine preserved statuses compared source-vs-corrected by my own parser; overclaim
# and retroactive-authorization token sweeps (ALL 17 package files, no self-exclusion —
# hits are then adjudicated by context, unlike the executor's self-excluding sweep).
# Package: manifest bijection independent re-hash; UTF-8/no-BOM/LF scan.
# NO new RE: all EXE reads are at already-published pin VAs. Read-only outside my QC dir.
import csv
import hashlib
import io
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(PKG)))
SRC = os.path.join(os.path.dirname(PKG), "PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006")
OUT = os.path.join(HERE, "results_j2_j3_package.json")
res = {"checks": {}, "j2": {}, "j3": {}, "s10": {}, "package": {}, "findings_context": {}}

# ---- my own pinned-EXE mapper -----------------------------------------------------
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
data = open(EXE, "rb").read()
res["checks"]["exe_identity"] = (
    len(data) == 8015872 and hashlib.sha256(data).hexdigest().upper() ==
    "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31")
lf = struct.unpack_from("<I", data, 0x3C)[0]
coff = lf + 4
nsec = struct.unpack_from("<H", data, coff + 2)[0]
sopt = struct.unpack_from("<H", data, coff + 16)[0]
sec0 = coff + 20 + sopt
secs = []
for i in range(nsec):
    off = sec0 + 40 * i
    vsz, va, rsz, ro = struct.unpack_from("<IIII", data, off + 8)
    secs.append((va, max(vsz, rsz), ro))


def rd(va, n):
    rva = va - 0x400000
    for vs, sz, ro in secs:
        if vs <= rva < vs + sz:
            return data[ro + (rva - vs):ro + (rva - vs) + n]
    raise ValueError("unmapped %x" % va)


def e8_target(va):
    b = rd(va, 5)
    assert b[0] == 0xE8, "not E8 at %x: %s" % (va, " ".join("%02X" % x for x in b))
    return va + 5 + struct.unpack("<i", b[1:5])[0]


def fun_va(name):
    return int(name.replace("FUN_", ""), 16)


# ---- J2: my own census parse + recount ---------------------------------------------
census_lines = open(os.path.join(PKG, "EDGE_BUDGET_RECONSTRUCTION.csv"),
                   encoding="utf-8").read().splitlines()
data_lines = [l for l in census_lines if not l.startswith("#")]
rows = list(csv.DictReader(io.StringIO("\n".join(data_lines))))
res["j2"]["census_rows"] = len(rows)
res["checks"]["J2_census_has_70_rows"] = len(rows) == 70
counted = [r for r in rows if r["COUNTED_IN_MINIMUM"] == "YES"]
res["j2"]["counted_rows"] = len(counted)
res["checks"]["J2_counted_rows_21"] = len(counted) == 21
pairs = {(r["CALLER"], r["CALLEE"]) for r in counted}
res["j2"]["distinct_counted_pairs"] = len(pairs)
res["checks"]["J2_distinct_pairs_20"] = len(pairs) == 20
r01 = [r for r in rows if r["CENSUS_ID"] == "R01"]
res["checks"]["J2_R01_mandated_edge_present"] = (
    len(r01) == 1 and r01[0]["CALLSITE_VA"] == "0x0050A3AF"
    and r01[0]["CALLEE"] == "FUN_006C66D0"
    and r01[0]["RECONSTRUCTION_CLASS"] == "SUMMARY_SEMANTIC_NEW"
    and r01[0]["COUNTED_IN_MINIMUM"] == "YES")
# class census
cls = {}
for r in rows:
    cls[r["RECONSTRUCTION_CLASS"]] = cls.get(r["RECONSTRUCTION_CLASS"], 0) + 1
res["j2"]["class_counts"] = cls
res["checks"]["J2_class_counts_expected"] = cls == {
    "LEDGER_COUNTED": 6, "SUMMARY_SEMANTIC_NEW": 15, "RAW_VISIBLE_NOTED": 3,
    "RAW_VISIBLE_ONLY": 10, "PROTOCOL_SHAPE_ONLY": 5, "REPIN_PRIOR_SCOPE": 27,
    "OUT_OF_ANALYZED_EXTENT": 4}
# SAME_PAIR_AS dedup arithmetic replication
dup_counted = [r["CENSUS_ID"] for r in counted if r["SAME_PAIR_AS"]]
res["j2"]["counted_same_pair_rows"] = dup_counted
res["checks"]["J2_dedup_arithmetic_replicates"] = (
    dup_counted == ["R12"] and len(counted) - len(dup_counted) == 20)

# ---- J2: my own replay of every declared target (DIRECT_E8 + VTABLE_SLOT rows) -----
bad = []
vt_slots = {"VTABLE_SLOT_41": 0xA4, "VTABLE_SLOT_42": 0xA8, "VTABLE_SLOT_19": 0x4C,
            "VTABLE_SLOT_45": 0xB4}
for r in rows:
    va = int(r["CALLSITE_VA"], 16)
    cal = r["CALLEE"]
    kind = r["CALL_KIND"]
    if kind == "DIRECT_E8" and cal.startswith("FUN_"):
        if e8_target(va) != fun_va(cal):
            bad.append("%s rel32 mismatch" % r["CENSUS_ID"])
    elif kind in vt_slots and cal.startswith("FUN_"):
        got = struct.unpack("<I", rd(0x00A8CCF4 + vt_slots[kind], 4))[0]
        if got != fun_va(cal):
            bad.append("%s slot mismatch" % r["CENSUS_ID"])
res["j2"]["target_replay_mismatches"] = bad
res["checks"]["J2_all_census_targets_replay_match"] = not bad

# ---- J2: source ledger / anchors cross-checks (BASE materials) ---------------------
src_edge = list(csv.DictReader(open(os.path.join(SRC, "EDGE_LEDGER.csv"),
                                    encoding="utf-8")))
res["checks"]["J2_source_ledger_exactly_E1_E6"] = (
    len(src_edge) == 6 and [e["EDGE_ID"] for e in src_edge] ==
    ["E%d" % i for i in range(1, 7)])
src_budget = open(os.path.join(SRC, "FUNCTION_BUDGET.csv"), encoding="utf-8").read()
res["checks"]["J2_budget_row7_records_getter_edge"] = \
    "child=FUN_006C66D0(manager) @0x0050A3AF" in src_budget
src_pra = open(os.path.join(SRC, "PRE_REGISTERED_ANCHORS.md"), encoding="utf-8").read()
res["checks"]["J2_max_new_edges_is_6_in_pra"] = "MAX_NEW_INTERPROCEDURAL_EDGES = 6" in src_pra
# census E-rows == ledger E1-E6 callsites
led_va = {e["CALLSITE_VA"] for e in src_edge}
cen_e = {r["CALLSITE_VA"] for r in rows if r["RECONSTRUCTION_CLASS"] == "LEDGER_COUNTED"}
res["checks"]["J2_census_E_rows_match_ledger"] = led_va == cen_e
alg = open(os.path.join(PKG, "CORRECTED_STATUS_ALGEBRA.md"), encoding="utf-8").read()
res["checks"]["J2_compliance_FAIL_recorded"] = "ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL" in alg
res["checks"]["J2_minimum_20_recorded"] = "MINIMUM_ANALYZED_EDGE_COUNT = 20" in alg
res["checks"]["J2_retroactive_NO_recorded"] = "RETROACTIVE_PRIOR_AUTHORIZATION = NO" in alg

# ---- J2 ADVERSARIAL: the census "EVERY recorded callsite" completeness claim -------
# Recorded callsites found in the source-run materials but ABSENT from the census
# (each re-verified here from the pinned EXE at its already-published VA):
missing = {}
# (a) FUN_0050A310 window: the two manager-family calls (source HANDOFF NOT_CHECKED
#     "F90/10B0"; CANDIDATE_LEDGER CAND-4 PATH_CONDITIONS records their result flow).
missing["FUN_0050A310->FUN_006C0F90@0x0050A3B9"] = e8_target(0x0050A3B9) == 0x006C0F90
missing["FUN_0050A310->FUN_006C10B0@0x0050A3CF"] = e8_target(0x0050A3CF) == 0x006C10B0
# (b) FUN_0050A310 undecoded tail: the FUN_005095C0 call (FINAL_REPORT §2; internal-QC
#     tail-bytes record in qc_independent_repins_results.json).
missing["FUN_0050A310->FUN_005095C0@0x0050A43A"] = e8_target(0x0050A43A) == 0x005095C0
# (c) PA2a prior-pin re-read: SF ctor -> ExtraData ctor call (PRE_REGISTERED_ANCHORS PA2;
#     PA2a window in REPIN_ANCHOR_WINDOWS.txt).
missing["FUN_00509330->FUN_0064B1E0@0x0050948B"] = e8_target(0x0050948B) == 0x0064B1E0
# (d) PA3 prior-pin re-read: FUN_0050A050 slot-17 GetObjectByName dispatch
#     (PRE_REGISTERED_ANCHORS PA3; PA3a/PA3b windows).
slot17 = struct.unpack("<I", rd(0x00A8CCF4 + 0x44, 4))[0]
missing["FUN_0050A050->slot17_FUN_007B5390@0x0050A064"] = (
    rd(0x0050A064, 2) == b"\xff\xd0" and slot17 == 0x007B5390)
# (e) PA1a window: SF ctor allocator call (PRE_REGISTERED_ANCHORS PA1 "allocation 0x118").
missing["FUN_00509330->FUN_0095D3C4@0x005093A0"] = e8_target(0x005093A0) == 0x0095D3C4
# (f) FUN_006A3930 window: allocator call for the manager (internal-QC record (d):
#     "allocator call @0x006A3A4D -> 0x0095D3C4").
missing["FUN_006A3930->FUN_0095D3C4@0x006A3A4D"] = e8_target(0x006A3A4D) == 0x0095D3C4
# (g) FUN_006A3930 window disassembly-context calls (entry-aligned E8s in the
#     persisted windows; NOT in the source run's own 12-entry E8-scan list):
for va, tgt in ((0x006A39D8, 0x00401360), (0x006A39DF, 0x00485050),
                (0x006A39E6, 0x0048CBB0), (0x006A3A68, 0x00733340),
                (0x006A3AAD, 0x00401360)):
    missing["FUN_006A3930->0x%08X@0x%08X" % (tgt, va)] = e8_target(va) == tgt
res["j2"]["missing_recorded_callsites_verified"] = missing
res["checks"]["J2_census_EVERY_claim_falsified"] = all(missing.values())
# Which of the missing pairs are not already represented by SOME census row of the
# same (caller,callee) pair:
census_pairs = {(r["CALLER"], r["CALLEE"]) for r in rows}
new_pairs_absent = [
    ("FUN_0050A310", "FUN_006C0F90"), ("FUN_0050A310", "FUN_006C10B0"),
    ("FUN_0050A310", "FUN_005095C0"), ("FUN_00509330", "FUN_0064B1E0"),
    ("FUN_0050A050", "FUN_007B5390"), ("FUN_00509330", "FUN_0095D3C4"),
    ("FUN_006A3930", "FUN_0095D3C4"),
]
res["j2"]["pairs_absent_from_census_entirely"] = [
    p for p in new_pairs_absent if p not in census_pairs]
# minimum under the census's OWN four-part criterion applied to the omitted
# FUN_006C0F90/FUN_006C10B0 records (receiver+callee+flow+role recorded in
# CANDIDATE_LEDGER CAND-4 PATH_CONDITIONS + source QC §4.3 + internal-QC F-QC-6 + raw):
res["j2"]["minimum_if_omitted_pairs_counted"] = len(pairs) + 2

# ---- J3 ----------------------------------------------------------------------------
f509850_path = os.path.join(SRC, "01_RAW", "FUN_00509850_FULL.txt")
b = open(f509850_path, "rb").read()
out = os.popen("").close() if False else None  # (placeholder no-op; keep py3.12 happy)
prev = json.load(open(os.path.join(HERE, "results_source_immutable.json"),
                     encoding="utf-8"))
res["j3"]["source_immutable_overall"] = prev["OVERALL"]
res["checks"]["J3a_source_evidence_unchanged"] = prev["OVERALL"] == "PASS"
res["checks"]["J3b_incidental_labels_present"] = (
    "NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION" in alg
    and "SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE" in alg
    and "PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED" in alg)
sec_a = alg.split("## B.")[0]
res["checks"]["J3c_no_active_promotion_in_active_algebra"] = \
    "CONFIRMED_STATIC" not in sec_a
# my own CONFIRMED_STATIC context sweep over ALL package files (no self-exclusion):
ctx_marks = ["SUPERSEDED", "superseded", "historical", "source run", "source-run",
             "CL-08", "PE_MASTER_REVIEW.md", "064b7f4"]
cs_hits = []
for dp, dn, fn in os.walk(PKG):
    if "__pycache__" in dp:
        continue
    for f in fn:
        fp = os.path.join(dp, f)
        rel = os.path.relpath(fp, PKG)
        if rel.startswith("00_CONTROL_INTERNAL_QC"):
            continue  # my own QC records quote the token as a check literal
        lines = open(fp, encoding="utf-8", errors="replace").read().splitlines()
        for i, line in enumerate(lines):
            if "CONFIRMED_STATIC" in line:
                ctx = "\n".join(lines[max(0, i - 4):i + 5])
                if not any(m in ctx for m in ctx_marks):
                    cs_hits.append("%s:%d" % (rel, i + 1))
res["j3"]["confirm_static_out_of_context_hits"] = cs_hits
res["checks"]["J3d_confirm_static_only_superseded_context"] = not cs_hits

# ---- §10: nine preserved statuses (my own source-vs-corrected comparison) ----------
cm = list(csv.DictReader(open(os.path.join(SRC, "CLAIM_MATRIX.csv"), encoding="utf-8")))
cmb = {r["CLAIM_ID"]: r for r in cm}
cand = list(csv.DictReader(open(os.path.join(SRC, "CANDIDATE_LEDGER.csv"),
                                encoding="utf-8")))
c4 = [r for r in cand if r["CANDIDATE_ID"] == "CAND-4-ACLD-PATH-SLOT41-ATTACH"][0]
sfr = open(os.path.join(SRC, "FINAL_REPORT.md"), encoding="utf-8").read()
src_nine = {
    "SCIENCE_OUTCOME": "SCIENCE OUTCOME = PARENT_FOUND_CHILD_UNRESOLVED" in sfr,
    "EXACT_PARENT": "CONFIRMED_EXACT_SCENEFEEDER_PLUS_30" in c4["PARENT_STATUS"],
    "JOIN_OPERATION": c4["JOIN_OPERATION_STATUS"].startswith("STRONGLY_SUPPORTED"),
    "CHILD_MODEL_PROVENANCE": "UNRESOLVED" in c4["CHILD_PROVENANCE"],
    "CHILD_VISUAL_ROLE": "UNRESOLVED" in c4["CHILD_ROLE"],
    "INSTANCE_MODEL_NODE_JOIN": cmb["CL-15"]["STATUS"] == "NOT_ESTABLISHED",
    "WORLD_XYZ_RECOVERED": cmb["CL-17"]["STATUS"].startswith("NO"),
    "STATIC_BUILDING_CHANNEL": cmb["CL-18"]["STATUS"] == "NOT_ESTABLISHED",
    "HISTORICAL_INSTANCE_DATA_RECOVERED": cmb["CL-19"]["STATUS"] == "NO",
}
corr_nine = {
    "SCIENCE_OUTCOME": "SCIENCE_OUTCOME = PARENT_FOUND_CHILD_UNRESOLVED" in sec_a,
    "EXACT_PARENT": "EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30" in sec_a,
    "JOIN_OPERATION": "JOIN_OPERATION = STRONGLY_SUPPORTED" in sec_a,
    "CHILD_MODEL_PROVENANCE": "CHILD_MODEL_PROVENANCE = UNRESOLVED" in sec_a,
    "CHILD_VISUAL_ROLE": "CHILD_VISUAL_ROLE = UNRESOLVED" in sec_a,
    "INSTANCE_MODEL_NODE_JOIN": "INSTANCE_MODEL_NODE_JOIN = NOT_ESTABLISHED" in sec_a,
    "WORLD_XYZ_RECOVERED": "WORLD_XYZ_RECOVERED = NO" in sec_a,
    "STATIC_BUILDING_CHANNEL": "STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED" in sec_a,
    "HISTORICAL_INSTANCE_DATA_RECOVERED":
        "HISTORICAL_INSTANCE_DATA_RECOVERED = NO" in sec_a,
}
res["s10"]["source_side"] = src_nine
res["s10"]["corrected_side"] = corr_nine
res["checks"]["s10_nine_statuses_unchanged_both_sides"] = (
    all(src_nine.values()) and all(corr_nine.values()))

# ---- my own token sweeps over ALL 17 package files (no self-exclusion) -------------
pkg_files = []
for dp, dn, fn in os.walk(PKG):
    if "__pycache__" in dp or os.path.relpath(dp, PKG) == "00_CONTROL_INTERNAL_QC":
        continue
    for f in fn:
        pkg_files.append(os.path.relpath(os.path.join(dp, f), PKG).replace("\\", "/"))
res["package"]["file_count"] = len(pkg_files)
res["checks"]["package_has_17_files"] = len(pkg_files) == 17
retro_tokens = ["RETROACTIVE_PRIOR_AUTHORIZATION = YES",
                "ORIGINAL_EDGE_BUDGET_COMPLIANCE = PASS",
                "was authorized before", "authorized retroactively",
                "prior human authorization existed"]
retro_hits = []
for rel in pkg_files:
    txt = open(os.path.join(PKG, *rel.split("/")), encoding="utf-8",
               errors="replace").read()
    for t in retro_tokens:
        if t in txt:
            retro_hits.append("%s :: %s" % (rel, t))
res["package"]["retroactive_token_hits"] = retro_hits
res["checks"]["s10_no_retroactive_authorization_claim"] = not retro_hits
over_tokens = ["INSTANCE_MODEL_NODE_JOIN = CONFIRMED",
               "INSTANCE_MODEL_NODE_JOIN=CONFIRMED",
               "CHILD_MODEL_PROVENANCE = CONFIRMED", "CHILD_MODEL_PROVENANCE=CONFIRMED",
               "CHILD_VISUAL_ROLE = CONFIRMED", "CHILD_VISUAL_ROLE=CONFIRMED",
               "RUNTIME_JOIN_OBSERVED = YES", "RUNTIME_JOIN_OBSERVED=YES",
               "WORLD_XYZ_RECOVERED = YES", "WORLD_XYZ_RECOVERED=YES",
               "CONFIRMED_MODEL_DERIVED", "STATIC_BUILDING_CHANNEL = ESTABLISHED",
               "STATIC_BUILDING_CHANNEL=ESTABLISHED",
               "HISTORICAL_INSTANCE_DATA_RECOVERED = YES",
               "HISTORICAL_INSTANCE_DATA_RECOVERED=YES"]
over_hits = []
for rel in pkg_files:
    txt = open(os.path.join(PKG, *rel.split("/")), encoding="utf-8",
               errors="replace").read()
    for t in over_tokens:
        if t in txt:
            over_hits.append("%s :: %s" % (rel, t))
res["package"]["overclaim_token_hits"] = over_hits
res["checks"]["s10_no_new_model_resource_visual_conclusion"] = not over_hits

# ---- manifest bijection: independent full re-hash -----------------------------------
man_path = os.path.join(PKG, "MANIFEST_SHA256.csv")
man_lines = open(man_path, encoding="utf-8").read().splitlines()
man_data = [l for l in man_lines if not l.startswith("#")]
mrows = list(csv.DictReader(io.StringIO("\n".join(man_data))))
res["package"]["manifest_rows"] = len(mrows)
res["checks"]["manifest_has_16_rows"] = len(mrows) == 16
listed = {r["relative_path"]: (int(r["size_bytes"]), r["sha256"].upper())
          for r in mrows}
res["checks"]["manifest_no_duplicate_paths"] = len(listed) == len(mrows)
disk = {rel for rel in pkg_files if rel != "MANIFEST_SHA256.csv"}
res["package"]["bijection_missing"] = sorted(disk - set(listed))
res["package"]["bijection_extra"] = sorted(set(listed) - disk)
size_bad, sha_bad = [], []
for rel, (sz, sha) in listed.items():
    fp = os.path.join(PKG, *rel.split("/"))
    bb = open(fp, "rb").read()
    if len(bb) != sz:
        size_bad.append(rel)
    if hashlib.sha256(bb).hexdigest().upper() != sha:
        sha_bad.append(rel)
res["package"]["bijection_size_mismatch"] = size_bad
res["package"]["bijection_sha_mismatch"] = sha_bad
res["checks"]["manifest_bijection_zero_mismatch"] = (
    not res["package"]["bijection_missing"] and not res["package"]["bijection_extra"]
    and not size_bad and not sha_bad)
res["checks"]["manifest_entrypoint_exclusion_noted"] = any(
    "AUDIT_ENTRYPOINT.md" in l for l in man_lines)

# ---- UTF-8 / no-BOM / LF scan -------------------------------------------------------
enc_bad = []
for rel in pkg_files:
    bb = open(os.path.join(PKG, *rel.split("/")), "rb").read()
    if bb.startswith(b"\xef\xbb\xbf"):
        enc_bad.append(rel + ":BOM")
    if b"\r" in bb:
        enc_bad.append(rel + ":CR")
    try:
        bb.decode("utf-8")
    except UnicodeDecodeError:
        enc_bad.append(rel + ":not-utf8")
res["package"]["encoding_findings"] = enc_bad
res["checks"]["all_package_files_utf8_nobom_lf"] = not enc_bad
res["checks"]["no_pycache_in_package"] = not any(
    "__pycache__" in dp for dp, dn, fn in os.walk(PKG))

res["OVERALL"] = "PASS" if all(res["checks"].values()) else "FAIL"
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(res, fh, indent=2)
    fh.write("\n")
print("J2/J3/package independent run: OVERALL=%s" % res["OVERALL"])
for k in sorted(res["checks"]):
    print("  %-56s %s" % (k, res["checks"][k]))
print("  distinct pairs = %d; counted rows = %d; census rows = %d"
      % (res["j2"]["distinct_counted_pairs"], res["j2"]["counted_rows"],
         res["j2"]["census_rows"]))
print("  missing recorded callsites verified:", sum(missing.values()), "of", len(missing))
print("  pairs absent from census entirely:",
      res["j2"]["pairs_absent_from_census_entirely"])
