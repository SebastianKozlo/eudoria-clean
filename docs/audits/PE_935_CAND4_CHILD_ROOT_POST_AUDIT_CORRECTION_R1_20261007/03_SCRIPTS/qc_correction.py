"""qc_correction.py — fresh internal QC (SELF-REVIEW) of
PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007.

ORIGIN/SELF-CLASSIFICATION (the correction contract §6 mandates stating it honestly):
written and executed by the SAME pe-reconstruction executor session that produced this
correction package — a fresh-context SELF-REVIEW, NOT an independent external Desktop
post-audit and NOT a PE-MASTER qualification. The authoritative independent input for
THIS correction's basis was the Desktop post-audit OF THE SOURCE RUN (REPORT.md /
CONTROL_COUNTERCHECKS.json / EDGE_AND_SCOPE_COUNTERCHECKS.json); an independent Desktop
post-audit of THIS correction's SHA remains NOT_PERFORMED (pending persistence/publication).

What this QC does (correction contract §6, all items):
  1. FULL content-based re-derivation of the corrected ledger classification FROM THE
     SOURCE LEDGER'S RECORDED CONTENT (NOT trusting LEDGER_CLASS, NOT trusting the
     corrected ledger's own CORRECTED_CLASS/CORRECTED_COUNTED columns as truth — they
     are only compared against the independent re-derivation);
  2. confirms the conservative minimum >= 32 and the proven counted set == 32;
  3. confirms the verbatim round-trip (69 rows x 9 fields byte-identical);
  4. confirms the body-accounting minimum >= 7 (FUNCTION_BODY_ACCOUNTING.csv) + a
     records-only scan of the audited run's scripts for undeclared real-body probes;
  5. re-executes the rebuilt CTRL_3 and the rebuilt CTRL_4 (clean + the THREE mandatory
     mutants) FROM IMPORT (not from CONTROL_RESULTS.json) and cross-checks the results
     against the Desktop CONTROL_COUNTERCHECKS.json matrix;
  6. verifies the clean CTRL_4 buffer against the PUBLISHED window record (byte column
     re-derived from SOURCE 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt; contiguity + 0x42 length
     + rel32/rel8 target arithmetic);
  7. verifies NO new science branches (the 8 additionally counted rows quote ONLY
     recorded source content; forbidden-promotion sweep);
  8. verifies the corrected wrapper terminology (CORRECTED_LINEAGE_STATUS.md);
  9. verifies the historical budget FAILs are preserved and CORRECTION_RECORDS_QC is
     separated from ORIGINAL_SCOPE_COMPLIANCE;
  10. verifies SOURCE_PACKAGE immutability (38/38 BASE blob identity at QC time),
      the desktop input identities, encoding (UTF-8 no-BOM/LF), and the repo state.

Writes: 03_SCRIPTS/QC_CORRECTION_RESULTS.json. Reads ONLY (no writes to the source
package; no EXE access of any kind).
"""
import csv
import hashlib
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(PKG)))
sys.path.insert(0, HERE)

import ctrl3_rebuilt as C3
import ctrl4_exact_endpoint as C4

SOURCE_PKG = os.path.join(REPO, "docs", "audits", "PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007")
DESKTOP = r"C:\Users\User\Documents\ChatGPT\PE\PE_935_CAND4_CHILD_ROOT_DESKTOP_POST_AUDIT_790E837_20261007"
BASE_SHA = "790e83735b439e2d76a250868a47a599c2c10184"

results = {}


def check(cid, ok, detail):
    results[cid] = {"ok": bool(ok), "detail": detail}
    print(("PASS  " if ok else "FAIL  ") + f"{cid}: {detail}")


def read_csv_rows(path):
    txt = open(path, encoding="utf-8").read()
    return list(csv.DictReader(io.StringIO("\n".join(l for l in txt.splitlines()
                                                    if l and not l.startswith("#"))), strict=False))


# ============================== 1+2. corrected ledger classification (content-based)
src_rows = read_csv_rows(os.path.join(SOURCE_PKG, "EDGE_ACCOUNTING_LEDGER.csv"))
cor_rows = read_csv_rows(os.path.join(PKG, "CORRECTED_EDGE_ACCOUNTING_LEDGER.csv"))
check("C1_source_ledger_shape", len(src_rows) == 69, f"{len(src_rows)} rows (expected 69)")

# INDEPENDENT content-based re-derivation (the literal rule, from ROW CONTENT only):
CONTENT_MARKERS = {
    "RV-01": "argument construction", "RV-02": "temp init", "RV-03": "temp init",
    "RV-04": "cleanup", "RV-05": "cleanup", "RV-06": "cleanup", "RV-07": "cleanup",
    "NEIGH-09": "receiver esi",
}
derived = {}
for r in src_rows:
    eid = r["EDGE_ID"]
    if r["LEDGER_CLASS"] == "ANALYZED_NEW":
        # counted iff a recorded interpretation exists in the row content
        derived[eid] = bool(r["NEW_INTERPRETATION"].strip())
    elif eid in CONTENT_MARKERS:
        # the Desktop-proven set: the interpretation lives in NOT_COUNTED_REASON
        derived[eid] = CONTENT_MARKERS[eid] in r["NOT_COUNTED_REASON"]
    else:
        derived[eid] = False  # RP exemptions / clean NEIGH / candidate NEIGH: not in the proven set
derived_counted = sorted(e for e, v in derived.items() if v)
check("C2_content_derived_counted_set", len(derived_counted) == 32,
      f"content-derived counted units = {len(derived_counted)} (expected exactly 32: 24 ANALYZED_NEW with "
      f"non-empty recorded interpretation + RV-01..RV-07 + NEIGH-09 with interpretations in NOT_COUNTED_REASON)")
check("C3_minimum_32", len(derived_counted) >= 32,
      f"MINIMUM_NEW_ANALYZED_EDGE_COUNT >= 32 CONFIRMED (measured proven floor = {len(derived_counted)})")

# compare against the corrected ledger's own columns (they are NOT the truth source — only compared)
cor_by_id = {r["EDGE_ID"]: r for r in cor_rows}
mismatch = [e for e, v in derived.items() if (cor_by_id[e]["CORRECTED_COUNTED"] == "YES") != v]
check("C4_corrected_ledger_matches_derivation", not mismatch and len(cor_rows) == 69,
      f"69 rows; CORRECTED_COUNTED matches the independent content derivation for all rows (mismatches: "
      f"{mismatch or 'NONE'}); class census: " +
      str({k: sum(1 for r in cor_rows if r["CORRECTED_CLASS"] == k) for k in
           ("COUNTED_ANALYZED_UNIT", "PRIOR_REPIN_EXEMPTION_UNREVERIFIED", "NOT_COUNTED_CLEAN",
            "CANDIDATE_UNADJUDICATED")}))

# mandatory re-check of the 8 rows named by the contract
mand = ["RV-01", "RV-02", "RV-03", "RV-04", "RV-05", "RV-06", "RV-07", "NEIGH-09"]
check("C5_mandatory_rows_re_adjudicated",
      all(cor_by_id[e]["CORRECTED_COUNTED"] == "YES" for e in mand),
      "RV-01..RV-07 + NEIGH-09 all COUNTED=YES in the corrected ledger (mandatory set per contract §1)")

# ============================== 3. verbatim round-trip
bad = []
for s, c in zip(src_rows, cor_rows):
    if s["EDGE_ID"] != c["EDGE_ID"]:
        bad.append((s["EDGE_ID"], "EDGE_ID"))
        continue
    for col in ("CALLER_START_VA", "CALLSITE_VA", "TARGET", "TARGET_KIND"):
        if s[col] != c[col]:
            bad.append((s["EDGE_ID"], col))
    for col in ("NEW_INTERPRETATION", "LEDGER_CLASS", "COUNTED", "NOT_COUNTED_REASON", "EVIDENCE"):
        if s[col] != c[col + "_ORIGINAL"]:
            bad.append((s["EDGE_ID"], col))
check("C6_verbatim_roundtrip", not bad,
      f"ORIGINAL_* fields byte-identical to the source ledger for all 69 rows x 9 fields (mismatches: {bad or 'NONE'})")

# ============================== 4. body accounting
body_rows = read_csv_rows(os.path.join(PKG, "FUNCTION_BODY_ACCOUNTING.csv"))
counted_bodies = [r for r in body_rows if r["CORRECTED_STATUS"].startswith("COUNTED_AS_NEW_BODY_OPENING")]
undeclared = [r for r in counted_bodies if r["DECLARATION_STATUS_IN_SOURCE_RUN"].startswith("UNDECLARED")]
check("C7_body_minimum_7", len(counted_bodies) == 7 and len(undeclared) == 1,
      f"MINIMUM_NEW_FUNCTION_BODIES_OPENED >= 7 CONFIRMED (counted bodies = {len(counted_bodies)}; the proven "
      f"undeclared probe = {undeclared[0]['FUNCTION_VA'] if undeclared else 'NONE'} = FUN_006C0EE0, the historical "
      f"CTRL_3 8-byte probe); candidates (window-spill neighbor bodies) present as CANDIDATE_UNADJUDICATED: "
      f"{sum(1 for r in body_rows if r['CORRECTED_STATUS'] == 'CANDIDATE_UNADJUDICATED')} row(s); "
      f"EXACT stays UNRESOLVED")

# records-only scan: undeclared real-body probes in the audited run's scripts
SCRIPT_DIRS = [os.path.join(SOURCE_PKG, "03_SCRIPTS"), os.path.join(SOURCE_PKG, "00_CONTROL_INTERNAL_QC")]
WHITELIST = [
    (0x006C66D0, 0x006C6730), (0x006C0D50, 0x006C100C), (0x006C0EE0, 0x006C0EE8),
    (0x006C8F80, 0x006C9100), (0x006C8B20, 0x006C8C60), (0x006C6F60, 0x006C70F0),
    (0x006C6780, 0x006C6848), (0x0050A310, 0x0050A460), (0x006A3930, 0x006A3B00),
    (0x00A75A30, 0x00A75A70), (0x00A79570, 0x00A795A0), (0x00A85470, 0x00A85500),
    (0x00A859F0, 0x00A85A20), (0x00A855C0, 0x00A855E0), (0x00A864B0, 0x00A864D0),
    (0x00AA6C50, 0x00AA6CF0), (0x00B9D8C0, 0x00B9D8E0),
]
vas_seen = {}
for sd in SCRIPT_DIRS:
    for fn in os.listdir(sd):
        if not fn.endswith(".py"):
            continue
        for ln_no, ln in enumerate(open(os.path.join(sd, fn), encoding="utf-8").read().splitlines(), 1):
            if not re.search(r"\.read\(|disasm\(|\brd\(|u32\(", ln):
                continue
            for m in re.finditer(r"0x([0-9A-Fa-f]{8})", ln):
                va = int(m.group(1), 16)
                vas_seen.setdefault(va, []).append(f"{fn}:{ln_no}")
unaccounted = {va: locs for va, locs in vas_seen.items()
               if not any(lo <= va <= hi for lo, hi in WHITELIST)}
check("C8_script_probe_scan", not unaccounted,
      f"records-only scan of the audited run's scripts ({len(vas_seen)} distinct read VAs in read/disasm/u32 lines): "
      f"every read VA is within the 6 declared bodies' windows, the accounted FUN_006C0EE0 8-byte probe, the "
      f"prior-scoped caller windows (0x0050A310 / 0x006A3930), or the recorded data-section pins (IAT/RTTI/vtable/"
      f"string/cookie); UNACCOUNTED probes: {unaccounted or 'NONE'} (this proves the RECORDED scripts contain no "
      f"other undeclared probe; the unrecorded execution history is not provable from records — "
      f"EXACT_NEW_FUNCTION_BODIES_OPENED stays UNRESOLVED)")

# ============================== 5. controls re-executed from import
ok_c3_clean, det_c3_clean = C3.ctrl3_provenance(C3.CLEAN_GETTER_FIXTURE)
ok_c3_mut, det_c3_mut = C3.ctrl3_provenance(C3.FOREIGN_ACCESSOR_FIXTURE)
check("C9_ctrl3_reexecuted", ok_c3_clean and not ok_c3_mut,
      f"CTRL_3 rebuilt re-executed from import: clean PASS ({det_c3_clean}); mutated FAIL ({det_c3_mut}); "
      f"exe_accessed=False; fixtures = persisted prior pin + recorded historical constant")

res = {name: C4.ctrl4_exact_endpoint(buf) for name, buf in [
    ("real_clean", C4.CLEAN_WINDOW),
    ("historical_edi_clobber", C4.make_clobber_mutant()),
    ("final_push_esi", C4.make_final_arg_mutant(0x56)),
    ("final_push_nop", C4.make_final_arg_mutant(0x90)),
]}
old = {name: C4.ctrl4_OLD_logic(buf) for name, buf in [
    ("real_clean", C4.CLEAN_WINDOW),
    ("historical_edi_clobber", C4.make_clobber_mutant()),
    ("final_push_esi", C4.make_final_arg_mutant(0x56)),
    ("final_push_nop", C4.make_final_arg_mutant(0x90)),
]}
c4_ok = (res["real_clean"][0] and not res["historical_edi_clobber"][0]
         and not res["final_push_esi"][0] and not res["final_push_nop"][0])
check("C10_ctrl4_matrix", c4_ok,
      "CTRL_4 exact-endpoint re-executed from import: REAL CLEAN = "
      f"{'PASS' if res['real_clean'][0] else 'FAIL'}; historical EDI-clobber = "
      f"{'FAIL' if not res['historical_edi_clobber'][0] else 'PASS'} (expected FAIL; {res['historical_edi_clobber'][1]}); "
      f"final push esi = {'FAIL' if not res['final_push_esi'][0] else 'PASS'} (expected FAIL; {res['final_push_esi'][1]}); "
      f"final push nop = {'FAIL' if not res['final_push_nop'][0] else 'PASS'} (expected FAIL; {res['final_push_nop'][1]})")
old_fp = [n for n in ("final_push_esi", "final_push_nop") if old[n][0]]
check("C11_old_logic_false_pass_reproduced", old["real_clean"][0] and not old["historical_edi_clobber"][0]
      and len(old_fp) == 2,
      f"old-logic reproduction: clean PASS; clobber FAIL; FALSE PASS on {old_fp} (matches Desktop "
      f"CONTROL_COUNTERCHECKS.json wrong_final_push_ESI/missing_final_push_NOP = true/true on the old checker)")

# cross-check against the Desktop counterchecks + persisted CONTROL_RESULTS.json
desk = json.load(open(os.path.join(DESKTOP, "CONTROL_COUNTERCHECKS.json"), encoding="utf-8"))
cr = json.load(open(os.path.join(PKG, "CONTROL_RESULTS.json"), encoding="utf-8"))
m = cr["CTRL_4_EXACT_ENDPOINT_REBUILT"]["matrix"]
desk_ok = (desk["CTRL_4"]["own_exact_endpoint_predicate"] ==
           {"clean": res["real_clean"][0], "recorded_mutant": res["historical_edi_clobber"][0],
            "wrong_final_push_ESI": res["final_push_esi"][0],
            "missing_final_push_NOP": res["final_push_nop"][0]}
           and m["real_clean"]["new_exact_endpoint_checker"]["result"] == "PASS"
           and m["final_push_esi"]["new_exact_endpoint_checker"]["result"] == "FAIL"
           and m["final_push_nop"]["new_exact_endpoint_checker"]["result"] == "FAIL"
           and m["historical_edi_clobber"]["new_exact_endpoint_checker"]["result"] == "FAIL")
check("C12_matches_desktop_counterchecks", desk_ok,
      "the rebuilt checker's 4-case matrix equals the Desktop own_exact_endpoint_predicate "
      "(clean=true, recorded_mutant=false, ESI=false, NOP=false) and the persisted CONTROL_RESULTS.json matrix")

# ============================== 6. clean buffer vs the PUBLISHED window record
win_txt = open(os.path.join(SOURCE_PKG, "01_RAW", "JOIN_WINDOW_50A3B7_REPIN.txt"), encoding="utf-8").read()
ins_re = re.compile(r"^\s+0x([0-9a-f]{8})\s+((?:[0-9A-F]{2} )*[0-9A-F]{2})\s+\S", re.M)
pieces = [(int(va, 16), bytes.fromhex(by)) for va, by in ins_re.findall(win_txt)]
pieces.sort()
recon = b"".join(p[1] for p in pieces)
contig = all(pieces[i][0] + len(pieces[i][1]) == pieces[i + 1][0] for i in range(len(pieces) - 1))
first_ok = pieces and pieces[0][0] == 0x0050A3B7
win_ok = (first_ok and contig and len(recon) == 0x42 and recon == C4.CLEAN_WINDOW)
check("C13_clean_buffer_provenance", win_ok,
      f"the CTRL_4 clean buffer re-derived from the published record's byte column: first VA 0x0050A3B7, contiguous "
      f"decode boundaries, total 0x{len(recon):X} bytes, byte-identical to the fixture ({len(pieces)} instructions)")

insns = C4.decode(C4.CLEAN_WINDOW, 0x0050A3B7)
targets = {va: insns[va].op_str for va in insns if insns[va].mnemonic == "call"}
rel_ok = (targets.get(0x0050A3B9) == "0x006c0f90" and targets.get(0x0050A3CF) == "0x006c10b0"
          and targets.get(0x0050A3D8) == "0x0050a1e0" and targets.get(0x0050A3E4) == "0x005246e0"
          and insns[0x0050A3C0].op_str == "0x0050a3c8" and insns[0x0050A3C6].op_str == "0x0050a3cc")
check("C14_window_branch_arithmetic", rel_ok,
      "decode-boundary arithmetic re-verified on the clean buffer: call targets 0x6C0F90/0x6C10B0/0x50A1E0/0x5246E0 "
      "and je/jmp rel8 targets 0x50A3C8/0x50A3CC all recompute exactly")

# ============================== 7. no new science branches
QUOTE_CHECKS = {
    "RV-01": "a local record containing this function's VA 0x006C8B20 and size 0x34",
    "RV-02": "temp init of local [esp+0x13]",
    "RV-03": "temp init of local [esp+0x12]",
    "RV-04": "cleanup of the first temp",
    "NEIGH-09": "receiver esi; result pushed as an arg of FUN_006C9F30",
}
no_new = True
detail = []
for eid, phrase in QUOTE_CHECKS.items():
    src_reason = next(r["NOT_COUNTED_REASON"] for r in src_rows if r["EDGE_ID"] == eid)
    adj = cor_by_id[eid]["CORRECTED_ADJUDICATION"]
    if phrase not in src_reason or phrase not in adj:
        no_new = False
        detail.append(eid)
# forbidden promotions sweep over the correction package's records
FORBIDDEN_ACTIVE = [
    "CHILD_TO_JOIN_IDENTITY = CONFIRMED", "SCIENCE_PASS", "WRAPPER_DEPTH = 2",
    "CHILD_RESOURCE_PROVENANCE = CONFIRMED_MODEL_DERIVED", "MODEL_ROOT_RELATION = CONFIRMED",
    "CAND4_CHILD_ROOT_CLOSURE = STRONGLY_SUPPORTED", "EXACT_NEW_ANALYZED_EDGE_COUNT = 32",
    "EXACT_NEW_FUNCTION_BODIES_OPENED = 7",
]
ALLOW_CTX = ("NOT ", "not ", "NEVER", "never", "SUPERSEDED", "superseded", "RETRACT", "retract", "!=",
             "UNRESOLVED", "stays", "must NOT", "forbidden", " != ", "no claim", "does NOT", "does not")
hits = []
for root, dirs, files in os.walk(PKG):
    dirs[:] = [d for d in dirs if d != "__pycache__"]
    for fn in files:
        if not fn.endswith((".md", ".csv", ".json")) or fn == "QC_CORRECTION_RESULTS.json":
            continue
        p = os.path.join(root, fn)
        try:
            txt = open(p, encoding="utf-8").read()
        except Exception:
            continue
        lines = txt.splitlines()
        for tok in FORBIDDEN_ACTIVE:
            for i, ln in enumerate(lines):
                if tok in ln:
                    # allowed contexts: the enclosing paragraph (4 lines above .. 2 below) marked as
                    # superseded/retracted/negation/policy — a token inside an explicitly SUPERSEDED
                    # quote or a negation sentence is not an ACTIVE claim
                    ctx = "\n".join(lines[max(0, i - 4):i + 3])
                    if (not any(a in ln for a in ALLOW_CTX)
                            and not any(a in ctx for a in
                                        ("SUPERSEDED", "superseded", "RETRACTED", "retracted", "RETAIN",
                                         "forbidden", "no tool", "not to be", "does NOT", "does not",
                                         "NEVER", "never"))):
                        hits.append(f"{fn}:{i + 1}: {tok}")
check("C15_no_new_science_branches", no_new and not hits,
      f"the 8 additionally counted rows adjudicate ONLY interpretations already recorded in the source ledger "
      f"(verbatim quote checks: {detail or 'ALL OK'}); forbidden-ACTIVE-token sweep over the correction records: "
      f"{hits[:4] or 'NONE'}")

# ============================== 8. corrected wrapper terminology
lin = open(os.path.join(PKG, "CORRECTED_LINEAGE_STATUS.md"), encoding="utf-8").read()
wrap_ok = ("WRAPPER_DEPTH = UNRESOLVED" in lin
           and "POINTER_LINEAGE_TRANSITIONS_OBSERVED = 2" in lin
           and "H-2 RELATION_TYPE = UNRESOLVED" in lin
           and "NEW_WRAPPER_HOPS" in lin and "= 2" in lin.split("NEW_WRAPPER_HOPS")[1][:80]
           and "MAX_NEW_WRAPPER_HOPS" in lin and "= 3" in lin.split("MAX_NEW_WRAPPER_HOPS")[1][:80]
           and "MODEL_ROOT_RELATION = UNKNOWN" in lin
           and "does not claim the two charged units establish two layers" in lin
           and "still consumes" in lin)
check("C16_wrapper_terminology", wrap_ok,
      "CORRECTED_LINEAGE_STATUS.md: WRAPPER_DEPTH = UNRESOLVED (semantics != budget consumption); "
      "POINTER_LINEAGE_TRANSITIONS_OBSERVED = 2 (examined H-1/H-2 description, not a global census); H-2 "
      "RELATION_TYPE = UNRESOLVED; historical NEW_WRAPPER_HOPS = 2 / MAX 3 PRESERVED (unresolved relation still "
      "consumed; no 2-layers claim)")

# ============================== 9. historical budget FAIL preserved + separation
led_hdr = open(os.path.join(PKG, "CORRECTED_EDGE_ACCOUNTING_LEDGER.csv"), encoding="utf-8").read()
body_txt = open(os.path.join(PKG, "FUNCTION_BODY_ACCOUNTING.csv"), encoding="utf-8").read()
fails_ok = ("ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL" in led_hdr
            and "RETROACTIVE_PRIOR_AUTHORIZATION = NO" in led_hdr
            and "ORIGINAL_SCOPE_COMPLIANCE = FAIL" in led_hdr
            and "EXACT_NEW_ANALYZED_EDGE_COUNT = UNRESOLVED" in led_hdr
            and "ORIGINAL_FUNCTION_BODY_BUDGET_COMPLIANCE = FAIL" in body_txt
            and "EXACT_NEW_FUNCTION_BODIES_OPENED = UNRESOLVED" in body_txt)
check("C17_historical_fail_preserved", fails_ok,
      "historical budget FAILs preserved verbatim in the corrected records: "
      "ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL; RETROACTIVE_PRIOR_AUTHORIZATION = NO; "
      "ORIGINAL_FUNCTION_BODY_BUDGET_COMPLIANCE = FAIL; ORIGINAL_SCOPE_COMPLIANCE = FAIL (never becomes PASS); "
      "EXACT counts = UNRESOLVED; CORRECTION_RECORDS_QC is reported separately from ORIGINAL_SCOPE_COMPLIANCE "
      "(see QC_REPORT.md §verdict)")

# ============================== 10. source package immutability + inputs + encoding + repo
def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, text=True).stdout


ls = git("ls-tree", "-r", BASE_SHA, "--name-only",
         "docs/audits/PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007").strip().splitlines()
mm, ms = [], []
for f in ls:
    blob = git("rev-parse", f"{BASE_SHA}:{f}").strip()
    disk = os.path.join(REPO, f.replace("/", "\\"))
    if not os.path.isfile(disk):
        ms.append(f)
        continue
    content = open(disk, "rb").read()
    if hashlib.sha1(b"blob %d\x00" % len(content) + content).hexdigest() != blob:
        mm.append(f)
check("C18_source_package_immutable", len(ls) == 38 and not mm and not ms,
      f"SOURCE_PACKAGE at QC time: {len(ls)} BASE blobs, {len(mm)} mismatches, {len(ms)} missing — READ-ONLY "
      f"preserved (zero writes by this correction)")

desk_pins = {"REPORT.md": ("BDE7B9EB873DF8E80A1E6C6A39B132A3EA1E1545E7A15977571DE7830D63EEEA", 12454),
             "CONTROL_COUNTERCHECKS.json": ("32DC3FEEE9881BADDD40AA44A040499E86071C9D7B0E3B3D0F8E772D8C3CCB4C", 2443),
             "EDGE_AND_SCOPE_COUNTERCHECKS.json": ("E275035BDF9FC8DF6383A8287546AB4009835F8E0DA66254CF5F0EF0B68C22CC", 5042)}
bad_inputs = []
for fn, (sha, size) in desk_pins.items():
    data = open(os.path.join(DESKTOP, fn), "rb").read()
    if len(data) != size or hashlib.sha256(data).hexdigest().upper() != sha:
        bad_inputs.append(fn)
check("C19_desktop_inputs_identity", not bad_inputs,
      f"the three Desktop post-audit inputs re-hashed at QC time: all MATCH the dispatch pins (mismatches: "
      f"{bad_inputs or 'NONE'})")

enc_fails = []
for root, dirs, files in os.walk(PKG):
    dirs[:] = [d for d in dirs if d != "__pycache__"]
    for fn in files:
        if fn == "QC_CORRECTION_RESULTS.json":
            continue
        raw = open(os.path.join(root, fn), "rb").read()
        if raw.startswith(b"\xef\xbb\xbf"):
            enc_fails.append(fn + ": BOM")
        if b"\r" in raw:
            enc_fails.append(fn + ": CR")
        try:
            raw.decode("utf-8")
        except Exception:
            enc_fails.append(fn + ": not UTF-8")
check("C20_encoding", not enc_fails,
      f"correction package files at QC time: UTF-8 no-BOM, LF-only, strict-decodable (violations: {enc_fails or 'NONE'})")

head = git("rev-parse", "HEAD").strip()
st = git("status", "--porcelain=v1")
tracked_dirty = [l for l in st.splitlines() if l and not l.startswith("??")]
foreign = [l for l in st.splitlines() if l.startswith("??")
           and "PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007" not in l]
check("C21_repo_state", head == BASE_SHA and not tracked_dirty and len(foreign) == 6,
      f"HEAD == BASE {BASE_SHA[:12]}; tracked dirty = {len(tracked_dirty)}; foreign untracked roots = "
      f"{len(foreign)} (5 audit dirs + experiments/ — untouched); this correction's writes are confined to "
      f"OUTPUT_ROOT (AUDIT_ENTRYPOINT.md NOT edited; no commit/push this phase)")

# ============================== verdict
overall = all(v["ok"] for v in results.values())
out = {
    "OVERALL": "QC_PASS" if overall else "QC_FAIL",
    "origin": ("SELF-REVIEW — fresh internal QC by the same pe-reconstruction executor session that produced this "
               "correction package (NOT an independent external Desktop post-audit; NOT a PE-MASTER qualification; "
               "the authoritative independent input for this correction's basis was the Desktop post-audit OF THE "
               "SOURCE RUN; an independent Desktop post-audit of THIS correction's SHA remains NOT_PERFORMED)"),
    "qc_run_id": "PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_INTERNAL_QC_R1_20261007",
    "checks": results,
    "correction_records_qc": "PASS" if overall else "FAIL",
    "original_scope_compliance": "FAIL (historical state of the audited run; never becomes PASS; separated from "
                                 "CORRECTION_RECORDS_QC)",
}
path = os.path.join(HERE, "QC_CORRECTION_RESULTS.json")
with open(path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
    f.write("\n")
print()
print("OVERALL:", out["OVERALL"], f"({len(results)} checks)")
print(f"wrote {path}")
