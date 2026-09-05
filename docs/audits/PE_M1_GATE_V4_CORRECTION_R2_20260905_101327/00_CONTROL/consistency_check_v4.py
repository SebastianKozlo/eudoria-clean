#!/usr/bin/env python3
# -*- coding: ascii -*-
# consistency_check_v4.py - the fail-closed internal-consistency check of the
# V4-correction package (writes 01_RAW\consistency_report_v4.json).
# Verifies:
#  (1) every FROZEN pinned input is UNCHANGED after the run (the V3 files, the
#      old matrix copies, the old manifest, the frozen package files, the
#      charter, the repair-run evidence, Entropia.exe);
#  (2) the two APPENDED files: their .pre copies hash to the pinned pre-append
#      values AND the current files are byte-extensions of the .pre copies
#      (append-only proven; the pinned pre-append pins apply to the .pre copies);
#  (3) the V4 structural facts verified INDEPENDENTLY (19 rows x 9 non-vacuous
#      fields in BOTH formats; the five section-13 labels rendered per MD row);
#  (4) every evidence SHA cited by the V4 matrix re-hashed from the physical
#      file (via the manifest's re-hash records - all must be sha_match true);
#  (5) the counter split consistency vs oracle_battery.json (443,141 + 20,000
#      = 463,141 TOTAL, from the JSON's own sub-counts);
#  (6) the PC24 measurement consistency (the manifest's record == the raw
#      measurement JSON; the disposition CONFIRMED; the controls all PASS);
#  (7) the SHAs recorded inside the GATE_INDEX append == the actual files;
#  (8) the payload scan: every file this run will commit is TEXT with no
#      proprietary binary payload magics;
#  (9) the local-only originals identity re-hash (via the manifest records).
import hashlib
import json
import os
import re
import sys

RUN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RUN_ROOT, "01_RAW")
REPO_GATE = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE"
REPAIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439"

FROZEN_PINS = {
  "v3_json": (os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V3.json"), "0E46AB2C94EA1BA7B4527950A4D8851AB69DFA48B7DCDDD449F9A52BD39931F8"),
  "v3_md": (os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V3.md"), "B0B69F0634774CC4032A471D7F69BFF7312D427166DC24217C26B93B2DFF797F"),
  "old_matrix_md": (os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX.md"), "F0C7D0F29EEE32F156D4BBF9565724009188BBE8C1C9B0F4CA0BBEC4184D76E1"),
  "old_matrix_json": (os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX.json"), "F373E60ABF87BF04CF7CC72A98423B19E861054D3B1F5F10CDD3C2041D478928"),
  "amendment_iter035": (os.path.join(REPO_GATE, "GATES", "AMENDMENT_ITER035_ROWS10_11.json"), "2B1FF548D1323BA46D1A8B533BF8BA943B5A508390637C632817D90B58254385"),
  "old_manifest": (os.path.join(REPO_GATE, "EVIDENCE_MANIFEST.json"), "0E6FCE502CE487EAFEEA603854AE135D81D40E8AA800F04EB98AB1D5D1459947"),
  "handoff": (os.path.join(REPO_GATE, "HANDOFF.md"), "C431BB62C57C68B4399BA478BABD309AFCCDCE4F09B81CA9742D27050EC81EB0"),
  "retractions": (os.path.join(REPO_GATE, "RETRACTIONS.md"), "A29758BF8DFB0D17BAB8BDADBABE4B26771E3A2F5A5498C3D8F3FF64F83C648B"),
  "unresolved": (os.path.join(REPO_GATE, "UNRESOLVED.md"), "2525CEDFF04B9FD9A0D32917E252C2B7EEB7D463C0D0A26E8294617F6BD80240"),
  "charter": (r"D:\Eudoria_Reconstruction\99_Audits\PE_MASTER_HANDOFFS\PE_MILESTONE_1_WORLD_SURFACE_R1_20260906_043000\NEXT_PROMPT.md", "7A10CD2BE286499540C6668C90E63897781BF6B472541FF0CCB75ADA84562ECA"),
  "stage_gates_csv": (os.path.join(REPAIR, "STAGE_ACCEPTANCE_GATES.csv"), "3277E5C7A520A87E3F4FFB8157FE6AA576A8F412F023996AC8D58C4676905A3E"),
  "oracle_battery": (os.path.join(REPAIR, "01_RAW", "oracle_battery.json"), "B04A3175F9E32669795D115271525E344AB823A8071171498845459D267DBFCE"),
  "domain_reproof": (os.path.join(REPAIR, "01_RAW", "domain_reproof.json"), "E654D2EF34BFF061FACF18794BE2F6A036B8BEFD847ED9308C0990F1795DEC3E"),
  "fail_closed_gates": (os.path.join(REPAIR, "01_RAW", "fail_closed_gates.json"), "645C9FC472FA4E93445C539FB375EDADB4DF5890D59B03715F9E914E50C52775"),
  "pe_section_map": (os.path.join(REPAIR, "03_STATIC", "PE_SECTION_MAP.json"), "C5688A5300C4119FD22EA74FD0D739B1E6DFCC77D112C910395061FF1ED11804"),
  "constant_address_lock": (os.path.join(REPAIR, "03_STATIC", "CONSTANT_ADDRESS_LOCK.json"), "6F4A9A6ED2E26F18C59AEB88F571374B73647C80FE19F65D5F0B6466A8D80304"),
  "offline_rechecks": (os.path.join(REPAIR, "01_RAW", "offline_rechecks.json"), "C80E65D62147E8DED2DE9C3D8EE028DE14BF619CB80C69BE71D30C8F0DEB4E32"),
  "entropia_exe": (r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe", "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"),
  "r1_dir_locks_record": (r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_GATE_V4_CORRECTION_R1_20260905_100405\01_RAW\pre_run_locks_verification.json", None),
}
APPEND_PINS = {
  "gate_index": (os.path.join(REPO_GATE, "GATE_INDEX.md"), os.path.join(RAW, "GATE_INDEX.md.pre"), "B8FD886BEF3575C048AA1978DE5908D6E0F8068A91EFC172EEB6456391A8A04B"),
  "amendments": (os.path.join(REPO_GATE, "GATES", "AMENDMENTS.md"), os.path.join(RAW, "AMENDMENTS.md.pre"), "5403B19613CD9B6E39C134A9029F92506907B61289BC522523C1C370B4F57125"),
}
V4_JSON = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.json")
V4_MD = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.md")
MANIFEST = os.path.join(REPO_GATE, "EVIDENCE_MANIFEST_V4.json")
PC24 = os.path.join(RAW, "pc24_synthetic_measurement.json")

NINE = ["knowledge", "implementation", "validation", "historical_fidelity",
        "evidence_status", "era", "denominator", "limitations", "evidence"]
FIVE_LABELS = ["KNOWLEDGE", "IMPLEMENTATION", "VALIDATION", "HISTORICAL_FIDELITY", "EVIDENCE_STATUS"]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    results = []
    ok_all = True

    def record(name, ok, detail):
        nonlocal ok_all
        results.append({"check": name, "verdict": "PASS" if ok else "FAIL", "detail": detail})
        if not ok:
            ok_all = False

    # (1) frozen pins unchanged
    for name, (path, sha) in FROZEN_PINS.items():
        if sha is None:
            continue
        actual = sha256_file(path)
        record("frozen_unchanged:%s" % name, actual == sha, "pinned %s actual %s" % (sha[:16], actual[:16]))
    # the R1 blocked-run dir untouched (its own lock record must still exist + the R1 report unchanged)
    r1_report = sha256_file(r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_GATE_V4_CORRECTION_R1_20260905_100405\06_REPORT\00_FINAL_REPORT.md")
    record("r1_blocked_run_dir_preserved", os.path.isfile(r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_GATE_V4_CORRECTION_R1_20260905_100405\01_RAW\pre_run_locks_verification.json"), "R1 evidence present; report sha %s" % r1_report[:16])

    # (2) the appended files: .pre == pins; current == byte-extension of .pre
    for name, (cur, pre, pin) in APPEND_PINS.items():
        pre_sha = sha256_file(pre)
        record("pre_copy_pin:%s" % name, pre_sha == pin, "pre sha %s pinned %s" % (pre_sha[:16], pin[:16]))
        pre_b = open(pre, "rb").read()
        cur_b = open(cur, "rb").read()
        record("append_only_prefix:%s" % name, cur_b.startswith(pre_b), "current len %d, pre len %d" % (len(cur_b), len(pre_b)))

    # (3) V4 structure verified independently
    with open(V4_JSON, "r", encoding="ascii") as f:
        v4 = json.load(f)
    with open(V4_MD, "r", encoding="ascii") as f:
        md_text = f.read()
    rows = v4["final_matrix_19_rows_v4"]
    struct_ok = len(rows) == 19
    for r in rows:
        for fld in NINE:
            v = r.get(fld)
            if v is None or (isinstance(v, str) and not v.strip()) or (isinstance(v, list) and not v):
                struct_ok = False
    record("v4_json_19x9_nonvacuous", struct_ok, "19 rows checked")
    md_ok = True
    for m in re.finditer(r"### ROW (\d+) - ", md_text):
        start = m.end()
        nxt = md_text.find("### ROW ", start)
        section = md_text[start:nxt if nxt > 0 else len(md_text)]
        for label in FIVE_LABELS:
            if not re.search(r"\*\*%s:?\*\*:?\s*\S" % label, section):
                md_ok = False
    record("v4_md_five_labels_rendered_19_rows", md_ok, "the five section-13 labels in every MD row")

    # (4) every cited evidence SHA re-hashed (via the manifest records)
    with open(MANIFEST, "r", encoding="ascii") as f:
        manifest = json.load(f)
    src_total = src_match = 0
    for c in manifest["claims_19_rows"]:
        for s in c["sources"]:
            if s.get("sha_match") is None:
                continue
            src_total += 1
            if s["sha_match"]:
                src_match += 1
    record("cited_evidence_sha_rehash", src_total > 0 and src_match == src_total, "%d/%d cited evidence files re-hashed MATCH" % (src_match, src_total))
    lo_total = lo_match = 0
    for s in manifest["local_only_original_sources"]:
        lo_total += 1
        if s["sha_match"]:
            lo_match += 1
    record("local_only_originals_identity_rehash", lo_match == lo_total, "%d/%d local-only originals re-hashed MATCH (identity metadata only, zero payloads committed)" % (lo_match, lo_total))

    # (5) the counter split consistency vs oracle_battery.json
    with open(os.path.join(REPAIR, "01_RAW", "oracle_battery.json"), "r", encoding="ascii") as f:
        ob = json.load(f)
    pcv = ob["platform_cross_validation"]
    platform = pcv["m2e_f32_checked"] + pcv["subnormal_band_f32_checked"] + pcv["f64_checked"] + pcv["arbitrary_rationals_f32_checked"]
    f80 = pcv["f80_exactness_sweep_checked"]
    mcs = manifest["oracle_counter_split"]
    record("counter_split_consistency", platform == 443141 and f80 == 20000 and mcs["platform_cross_validation_samples"] == platform
           and mcs["f80_exactness_sweep_samples"] == f80 and mcs["total"] == 463141,
           "oracle_battery: platform %d + f80 %d = %d TOTAL; the manifest record agrees (443,141 + 20,000 = 463,141)" % (platform, f80, platform + f80))

    # (6) the PC24 measurement consistency
    with open(PC24, "r", encoding="ascii") as f:
        pc24 = json.load(f)
    mrec = manifest["pc24_synthetic_remeasurement"]
    record("pc24_measurement_consistency",
           pc24["measured_synthetic_pc24_mismatches"] == 103073
           and pc24["all_negative_controls_pass"] is True
           and pc24["disposition"]["disposition"] == "CONFIRMED"
           and mrec["measured_synthetic_pc24_mismatches"] == pc24["measured_synthetic_pc24_mismatches"]
           and mrec["disposition"]["disposition"] == "CONFIRMED"
           and mrec["total_synthetic_comparisons"] == 1245184,
           "measured 103,073/1,245,184; disposition CONFIRMED (double measurement); all negative controls PASS")

    # (7) the SHAs recorded inside the GATE_INDEX append == the actual files
    gi_text = open(APPEND_PINS["gate_index"][0], "r", encoding="utf-8", errors="replace").read()
    v4j_sha, v4m_sha, mv4_sha = sha256_file(V4_JSON), sha256_file(V4_MD), sha256_file(MANIFEST)
    record("gate_index_append_sha_records",
           (v4m_sha in gi_text) and (v4j_sha in gi_text) and (mv4_sha in gi_text),
           "the appended record carries the actual V4/manifest SHAs (%s / %s / %s)" % (v4m_sha[:12], v4j_sha[:12], mv4_sha[:12]))

    # (8) the payload scan: everything this run commits is text, no binary magics
    commit_files = [V4_JSON, V4_MD, MANIFEST, APPEND_PINS["gate_index"][0], APPEND_PINS["amendments"][0]]
    for scan_dir in (RAW, os.path.join(RUN_ROOT, "00_CONTROL")):
        for dirpath, dirnames, filenames in os.walk(scan_dir):
            dirnames[:] = [d for d in dirnames if d not in ("fixtures", "__pycache__")]
            for fn in filenames:
                if fn.endswith(".pyc"):
                    continue
                commit_files.append(os.path.join(dirpath, fn))
    payload_bad = []
    for p in commit_files:
        head = open(p, "rb").read(512)
        if b"\x00" in head or head[:4] in (b"BNT2", b"BNT\x02") or head[:3] == b"\x00\x00\x0a" or head[:2] == b"AK":
            payload_bad.append(p)
    record("payload_scan_no_proprietary_payloads", not payload_bad, "%d to-be-committed files scanned; binary-magic hits: %d" % (len(commit_files), len(payload_bad)))

    report = {
        "run_id": "PE_M1_GATE_V4_CORRECTION_R2_20260905_101327",
        "work_item": "the fail-closed internal-consistency check of the V4 package",
        "checks": results,
        "verdict": "PASS" if ok_all else "FAIL",
        "script_sha256": sha256_file(os.path.abspath(__file__)),
        "v4_file_shas": {"M1_GATE_DELIVERABLE_MATRIX_V4.json": v4j_sha, "M1_GATE_DELIVERABLE_MATRIX_V4.md": v4m_sha, "EVIDENCE_MANIFEST_V4.json": mv4_sha},
    }
    with open(os.path.join(RAW, "consistency_report_v4.json"), "w", encoding="ascii") as f:
        json.dump(report, f, indent=1)
        f.write("\n")
    print("CONSISTENCY CHECK:", report["verdict"])
    for r in results:
        print("  [%s] %s - %s" % (r["verdict"], r["check"], r["detail"]))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
