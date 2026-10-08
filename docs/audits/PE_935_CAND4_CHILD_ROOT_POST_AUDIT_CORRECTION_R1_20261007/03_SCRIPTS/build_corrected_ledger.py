"""build_corrected_ledger.py — builds CORRECTED_EDGE_ACCOUNTING_LEDGER.csv for
PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007 (contract §1: C4-C1).

Method: read the SOURCE run's EDGE_ACCOUNTING_LEDGER.csv (the byte-identical BASE copy,
READ-ONLY), copy every original column VERBATIM (csv module round-trip — the original
text is never retyped), and append the corrected content-based adjudication columns from
the explicit per-row map below. The counted set = the historical 24 ANALYZED_NEW units +
the 8 content-proven additional units (RV-01..RV-07 + NEIGH-09, per the authoritative
Desktop post-audit). The exact complete total is UNRESOLVED (9 candidate rows not
adjudicated + 11 repin exemptions not re-verified).

NO new science interpretation is created here: every counted unit's interpretation
already exists in the source ledger's recorded content (verified by substring asserts).
"""
import csv
import io
import os
import sys

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
SRC = os.path.join(REPO, "docs", "audits", "PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007",
                   "EDGE_ACCOUNTING_LEDGER.csv")
PKG = os.path.join(REPO, "docs", "audits", "PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007")
OUT = os.path.join(PKG, "CORRECTED_EDGE_ACCOUNTING_LEDGER.csv")

# ---------------------------------------------------------------- read source
raw = open(SRC, encoding="utf-8").read()
data_lines = [ln for ln in raw.splitlines() if ln and not ln.startswith("#")]
rows = list(csv.DictReader(io.StringIO("\n".join(data_lines)), strict=False))
assert len(rows) == 69, f"expected 69 source rows, got {len(rows)}"
by_class = {}
for r in rows:
    by_class.setdefault(r["LEDGER_CLASS"], []).append(r)
assert {k: len(v) for k, v in by_class.items()} == {
    "ANALYZED_NEW": 24, "RAW_VISIBLE_ONLY": 7, "REPIN_PRIOR_SCOPE": 11,
    "OUT_OF_ANALYZED_EXTENT": 27}, "source class shape mismatch"

# ---------------------------------------------------------------- content asserts
# The 8 additionally-counted rows: their NOT_COUNTED_REASON CONTENT contains the
# recorded interpretations (the literal-rule basis; Desktop C4-C1 table).
CONTENT_EXPECT = {
    "RV-01": "argument construction",
    "RV-02": "temp init of local [esp+0x13]",
    "RV-03": "second temp init of local [esp+0x12]",
    "RV-04": "cleanup of the first temp",
    "RV-05": "cleanup",
    "RV-06": "cleanup",
    "RV-07": "cleanup",
    "NEIGH-09": "receiver esi; result pushed as an arg of FUN_006C9F30",
}
for eid, needle in CONTENT_EXPECT.items():
    r = next(x for x in rows if x["EDGE_ID"] == eid)
    assert needle in r["NOT_COUNTED_REASON"], f"{eid}: expected content missing: {needle!r}"
# All historical ANALYZED_NEW rows carry non-empty recorded interpretations.
for r in by_class["ANALYZED_NEW"]:
    assert r["NEW_INTERPRETATION"].strip(), f"{r['EDGE_ID']}: empty NEW_INTERPRETATION in ANALYZED_NEW"

# ---------------------------------------------------------------- adjudication map
E_NOTE = ("RETAINED_COUNTED: the row's NEW_INTERPRETATION is a recorded interpretation of the "
          "source run (historical ANALYZED_NEW; content non-empty — verified); counted as an "
          "analyzed callsite unit (unchanged by this correction)")
RV_NOTE = {
    "RV-01": ("COUNTED_PER_LITERAL_RULE: the row's NOT_COUNTED_REASON content records an "
              "argument-flow interpretation ('the call's argument construction (a local record "
              "containing this function's VA 0x006C8B20 and size 0x34)'); 'not load-bearing' is "
              "NOT an exemption (correction §1; Desktop C4-C1)"),
    "RV-02": ("COUNTED_PER_LITERAL_RULE: the reason content records a result-flow interpretation "
              "('import-mediated temp init of local [esp+0x13]') at this callsite"),
    "RV-03": ("COUNTED_PER_LITERAL_RULE: the reason content records a result-flow interpretation "
              "('second temp init of local [esp+0x12]') at this callsite"),
    "RV-04": ("COUNTED_PER_LITERAL_RULE: the reason content records a role/flow interpretation "
              "('import-mediated cleanup of the first temp') of this callsite"),
    "RV-05": ("COUNTED_PER_LITERAL_RULE: the reason content records a role interpretation "
              "('cleanup' of the identified temporaries) of this callsite"),
    "RV-06": ("COUNTED_PER_LITERAL_RULE: the reason content records a role interpretation "
              "('cleanup' of the identified temporaries) of this callsite"),
    "RV-07": ("COUNTED_PER_LITERAL_RULE: the reason content records a role interpretation "
              "('cleanup' of the identified temporaries) of this callsite"),
    "NEIGH-09": ("COUNTED_PER_LITERAL_RULE: the reason content records receiver + result-flow "
                 "interpretations ('receiver esi; result pushed as an arg of FUN_006C9F30') at "
                 "this callsite of THE GETTER in an unopened body"),
}
RP_NOTE = ("PRIOR_REPIN_EXEMPTION_RETAINED: the row cites an already-recorded prior interpretation "
           "(prior file/record named; 'free re-pin; no new semantics'); the prior-record citation "
           "was NOT re-verified against the prior packages in this correction; candidate for "
           "future adjudication (contributes to EXACT_NEW_ANALYZED_EDGE_COUNT = UNRESOLVED)")
CLEAN_NOTE = ("NOT_COUNTED_CLEAN: the row content contains no callsite interpretation (window/"
              "topology facts only; explicit 'no interpretation recorded'; no receiver/argument/"
              "result/path-role/semantic-role annotation at this callsite)")
CAND_NOTE = {
    "NEIGH-03": "a body-identity annotation ('second ctor variant')",
    "NEIGH-04": "an allocation-argument annotation ('new(0x68)')",
    "NEIGH-06": "a body-role annotation ('setter +0x118 with release dispatch')",
    "NEIGH-07": "a body-role annotation ('lazy initializer of +0x120')",
    "NEIGH-11": "a body-identity data-fact annotation ('manager vtable slot 2 target — data fact only')",
    "NEIGH-15": "a receiver annotation ('receiver [esp+0x40]')",
    "NEIGH-16": "a topology annotation ('a SECOND caller of FUN_006C8BB0')",
    "NEIGH-21": "a path-role annotation ('the SECOND on-path manager method (declared coverage GAP-2)')",
    "NEIGH-24": ("a prior-family target-arithmetic note ('the target arithmetic is the same "
                 "prior-canon family as E-13') carrying an explicit no-role disclaimer"),
}
E_IDS = [f"E-{i:02d}" for i in range(1, 25)]
RV_IDS = [f"RV-{i:02d}" for i in range(1, 8)]
RP_IDS = [f"RP-{i:02d}" for i in range(1, 12)]
NEIGH_CLEAN = ["NEIGH-01", "NEIGH-02", "NEIGH-05", "NEIGH-08", "NEIGH-10", "NEIGH-12",
               "NEIGH-13", "NEIGH-14", "NEIGH-17", "NEIGH-18", "NEIGH-19", "NEIGH-20",
               "NEIGH-22", "NEIGH-23", "NEIGH-25", "NEIGH-26", "NEIGH-27"]
NEIGH_CAND = sorted(CAND_NOTE)


def adjudicate(eid):
    if eid in E_IDS:
        return "YES", "COUNTED_ANALYZED_UNIT", E_NOTE
    if eid in RV_IDS or eid == "NEIGH-09":
        return "YES", "COUNTED_ANALYZED_UNIT", RV_NOTE[eid]
    if eid in RP_IDS:
        return "NO", "PRIOR_REPIN_EXEMPTION_UNREVERIFIED", RP_NOTE
    if eid in NEIGH_CLEAN:
        return "NO", "NOT_COUNTED_CLEAN", CLEAN_NOTE
    if eid in NEIGH_CAND:
        return ("NO", "CANDIDATE_UNADJUDICATED",
                f"CANDIDATE_UNADJUDICATED: the row content contains {CAND_NOTE[eid]} that MAY "
                "constitute a §3 interpretation; its counting was NOT adjudicated by the "
                "authoritative Desktop post-audit nor by this correction (no new interpretive "
                "science in a records correction); NOT counted in the conservative minimum; "
                "contributes to EXACT_NEW_ANALYZED_EDGE_COUNT = UNRESOLVED")
    raise AssertionError(f"unadjudicated row {eid}")


counts = {}
out_rows = []
for r in rows:
    counted, cls, note = adjudicate(r["EDGE_ID"])
    counts.setdefault(cls, []).append(r["EDGE_ID"])
    out_rows.append([
        r["EDGE_ID"], r["CALLER_START_VA"], r["CALLSITE_VA"], r["TARGET"], r["TARGET_KIND"],
        r["NEW_INTERPRETATION"], r["LEDGER_CLASS"], r["COUNTED"], r["NOT_COUNTED_REASON"],
        r["EVIDENCE"], counted, cls, note,
    ])

assert {k: len(v) for k, v in counts.items()} == {
    "COUNTED_ANALYZED_UNIT": 32, "PRIOR_REPIN_EXEMPTION_UNREVERIFIED": 11,
    "NOT_COUNTED_CLEAN": 17, "CANDIDATE_UNADJUDICATED": 9}, "corrected class shape mismatch"
assert set(counts["COUNTED_ANALYZED_UNIT"]) == set(E_IDS + RV_IDS + ["NEIGH-09"])

# ---------------------------------------------------------------- header + write
HEADER = """# CORRECTED_EDGE_ACCOUNTING_LEDGER — PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007
# Re-adjudication (C4-C1) of the SOURCE run's EDGE_ACCOUNTING_LEDGER.csv (69 rows; the SOURCE
# package is READ-ONLY — the ORIGINAL_* columns below are VERBATIM copies, never retyped; builder:
# 03_SCRIPTS/build_corrected_ledger.py). Basis: the correction contract §1 + the authoritative
# Desktop post-audit (C4-C1; REPORT.md + EDGE_AND_SCOPE_COUNTERCHECKS.json).
#
# RETRACTED source-package claims (superseded; see SUPERSESSION.md):
#   - "ACCOUNTED_EDGE_COUNT = 24" AS A COMPLETE TOTAL: 24 is the count of ledger-labeled
#     ANALYZED_NEW rows only — NOT the complete total of semantically analyzed callsite units.
#   - "INDEPENDENT_RECONSTRUCTED_EDGE_COUNT = 24 (== ACCOUNTED_EDGE_COUNT)" as a complete-census
#     proof: the historical reconstruction re-derived the LEDGER CLASSIFICATION itself (QC-I9
#     subtracts ledger-classified RV/NEIGH rows), not the recorded interpretation content.
#   - "exceedance exactly 24 / +16 past the stop line": the proven minimum is >= 32 units,
#     i.e. at least +24 past MAX 8; the exact exceedance is UNRESOLVED.
#   - "zero semantic analysis hidden under RAW_VISIBLE" as an ACHIEVED state: eight rows
#     (RV-01..RV-07, NEIGH-09) carry recorded interpretations in NOT_COUNTED_REASON while
#     classified not-counted (the J2 row-per-callsite census itself is retained).
#
# CORRECTED ACCOUNTING (conservative PROVEN floor):
#   MINIMUM_NEW_ANALYZED_EDGE_COUNT = 32 (24 historical ANALYZED_NEW + 8 content-proven units)
#   EXACT_NEW_ANALYZED_EDGE_COUNT = UNRESOLVED (9 CANDIDATE_UNADJUDICATED rows + 11 repin
#     exemptions not re-verified; the exact total is not provable from existing records)
#   EDGE_ACCOUNTING_STATUS = BUDGET_EXCEEDED (>= 32 > MAX 8; exceedance >= +24; NOT exact)
#   ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL (historical; stands permanently)
#   RETROACTIVE_PRIOR_AUTHORIZATION = NO
#   ORIGINAL_SCOPE_COMPLIANCE = FAIL (supersedes the source run's
#     PARTIAL_WITH_EXCEEDED_EDGE_BUDGET; historical state — never becomes PASS)
#
# ADJUDICATION RULE (source-run contract §2, literal): a NEW interpretation (receiver / callee
# identity / argument-result flow / path role / semantic role) of a callsite = a counted unit,
# even if the callee body is not opened; "not load-bearing" is NOT an exemption. Adjudication is
# by ROW CONTENT (NEW_INTERPRETATION + NOT_COUNTED_REASON + annotations), NOT by the historical
# LEDGER_CLASS label (the historical QC-I5 checked only NEW_INTERPRETATION emptiness; the
# historical QC-I9 trusted the same ledger's classification — both superseded for census purposes).
# NO new science interpretation is created by this re-adjudication: every counted unit's
# interpretation already exists in the source ledger's recorded content (content asserts in the
# builder; independently re-derived by 03_SCRIPTS/qc_correction.py).
#
# CORRECTED_CLASSES:
#   COUNTED_ANALYZED_UNIT             = 32 rows (COUNTED=YES)
#   PRIOR_REPIN_EXEMPTION_UNREVERIFIED = 11 rows (exemption retained; prior record NOT re-verified)
#   NOT_COUNTED_CLEAN                 = 17 rows (no callsite interpretation in the row content)
#   CANDIDATE_UNADJUDICATED           =  9 rows (annotation MAY constitute a §3 interpretation;
#                                        counting not adjudicated; contributes to EXACT = UNRESOLVED)
"""
COLS = ("EDGE_ID,CALLER_START_VA,CALLSITE_VA,TARGET,TARGET_KIND,NEW_INTERPRETATION_ORIGINAL,"
        "LEDGER_CLASS_ORIGINAL,COUNTED_ORIGINAL,NOT_COUNTED_REASON_ORIGINAL,EVIDENCE_ORIGINAL,"
        "CORRECTED_COUNTED,CORRECTED_CLASS,CORRECTED_ADJUDICATION")

buf = io.StringIO()
buf.write(HEADER)
buf.write(COLS + "\n")
w = csv.writer(buf, lineterminator="\n")
for row in out_rows:
    w.writerow(row)
with open(OUT, "w", encoding="utf-8", newline="") as f:
    f.write(buf.getvalue())

print(f"wrote {OUT}")
print("class census:", {k: len(v) for k, v in counts.items()})
print("counted set:", E_IDS + RV_IDS + ["NEIGH-09"] == counts["COUNTED_ANALYZED_UNIT"])
