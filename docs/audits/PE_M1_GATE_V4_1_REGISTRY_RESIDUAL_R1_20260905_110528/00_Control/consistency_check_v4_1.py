#!/usr/bin/env python3
# -*- coding: ascii -*-
# consistency_check_v4_1.py - W3 of PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528:
# the fail-closed internal-consistency check of the V4.1 package (pass 1;
# writes 01_RAW\consistency_report_v4_1.json). The FINAL 100%-of-commit-set
# payload scan is performed by payload_scan_final_v4_1.py AFTER the repo mirror
# is built (this pass scans the current state: the 5 repo gate-package files +
# the run tree). Verifies:
#  (1) every FROZEN pinned input UNCHANGED after the run + the completed-run
#      dirs preserved (incl. the R2/R1 dirs);
#  (2) the two APPENDED files: .pre copies == the pinned pre-append values AND
#      the current files are byte-extensions of the .pre copies;
#  (3) the V4.1 structural facts verified INDEPENDENTLY (19x9 non-vacuous in
#      both formats; the five section-13 labels per MD row; BOTH registry
#      entries composed + labeled + typed per the byte locks);
#  (4) every evidence SHA cited by the manifest re-hashed from the physical
#      file (73 claim sources + 5 local-only originals);
#  (5) the counter split consistency vs oracle_battery.json;
#  (6) the registry echo == the V4.1 matrix registry + the built_from SHAs ==
#      the actual files;
#  (7) the PC24 record consistency (the manifest record == the R2 raw
#      measurement artifact, SHA-pinned);
#  (8) the SHAs recorded inside the GATE_INDEX append == the actual files;
#  (9) the payload scan (pass 1): every to-be-committed file present now is
#      TEXT with no proprietary binary payload magics.
import hashlib
import json
import os
import re
import sys

RUN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RUN_ROOT, "01_RAW")
REPO_GATE = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE"
REPAIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439"
R2_RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_GATE_V4_CORRECTION_R2_20260905_101327"
R1_RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_GATE_V4_CORRECTION_R1_20260905_100405"

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
}
APPEND_PINS = {
    "gate_index": (os.path.join(REPO_GATE, "GATE_INDEX.md"), os.path.join(RAW, "GATE_INDEX.md.pre"), "FD68060A63184B94753493D87A04CFB33FBA9667C07DD91D4D5B47810F1CC558"),
    "amendments": (os.path.join(REPO_GATE, "GATES", "AMENDMENTS.md"), os.path.join(RAW, "AMENDMENTS.md.pre"), "C8FF0ABE475E7D37CE790F89CFB941E0FA4A5A0BA23B27921534EFFC6D51D347"),
}
V4_JSON = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.json")
V4_MD = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.md")
MANIFEST = os.path.join(REPO_GATE, "EVIDENCE_MANIFEST_V4.json")
PC24_R2 = os.path.join(R2_RUN, "01_RAW", "pc24_synthetic_measurement.json")
PC24_PINNED_SHA = "01B96D259F0FB09A6D724F8A4843938483D845736946FD73DEEBEBF4A74EA9DF"

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
        actual = sha256_file(path)
        record("frozen_unchanged:%s" % name, actual == sha, "pinned %s actual %s" % (sha[:16], actual[:16]))
    # the completed-run dirs preserved (read-only records; the R2/R1 lock + report records exist)
    record("r2_completed_run_dir_preserved",
           os.path.isfile(os.path.join(R2_RUN, "01_RAW", "pre_run_locks_verification.json"))
           and os.path.isfile(os.path.join(R2_RUN, "06_REPORT", "00_FINAL_REPORT.md")),
           "the R2 run dir records present (read-only)")
    record("r1_completed_run_dir_preserved",
           os.path.isfile(os.path.join(R1_RUN, "01_RAW", "pre_run_locks_verification.json")),
           "the R1 blocked-run dir records present (read-only)")

    # (2) the appended files: .pre == pins; current == byte-extension of .pre
    for name, (cur, pre, pin) in APPEND_PINS.items():
        pre_sha = sha256_file(pre)
        record("pre_copy_pin:%s" % name, pre_sha == pin, "pre sha %s pinned %s" % (pre_sha[:16], pin[:16]))
        pre_b = open(pre, "rb").read()
        cur_b = open(cur, "rb").read()
        record("append_only_prefix:%s" % name, cur_b.startswith(pre_b), "current len %d, pre len %d" % (len(cur_b), len(pre_b)))

    # (3) the V4.1 structure verified independently
    with open(V4_JSON, "r", encoding="ascii", newline="") as f:
        v4 = json.load(f)
    with open(V4_MD, "r", encoding="ascii", newline="") as f:
        md_text = f.read().replace("\r\n", "\n")
    rows = v4["final_matrix_19_rows_v4"]
    struct_ok = len(rows) == 19
    for r in rows:
        for fld in NINE:
            v = r.get(fld)
            if v is None or (isinstance(v, str) and not v.strip()) or (isinstance(v, list) and not v):
                struct_ok = False
    record("v4_1_json_19x9_nonvacuous", struct_ok, "19 rows checked")
    md_ok = True
    for m in re.finditer(r"### ROW (\d+) - ", md_text):
        start = m.end()
        nxt = md_text.find("### ROW ", start)
        section = md_text[start:nxt if nxt > 0 else len(md_text)]
        for label in FIVE_LABELS:
            if not re.search(r"\*\*%s:?\*\*:?\s*\S" % label, section):
                md_ok = False
    record("v4_1_md_five_labels_rendered_19_rows", md_ok, "the five section-13 labels in every MD row")
    # BOTH registry entries composed + labeled + typed (independent re-verification)
    reg = v4["era_bounded_registry_v4"]
    comp_ok = True
    for e, const, addr in ((reg[11], "32767.0", "0x00a7d7a8"), (reg[13], "65535.0", "0x00a8c758")):
        m_ = e["missing"].lower()
        w = e.get("why")
        h = e.get("historical_open_item_record")
        comp_ok = comp_ok and "composed in v4.1" in m_ and "none for the divisor" in m_ and const in m_ and addr in m_ \
            and "historical open-item record follows" in m_
        comp_ok = comp_ok and "composed in v4.1" in e["resume_path"].lower() and "actual-cw" in e["resume_path"].lower()
        comp_ok = comp_ok and isinstance(w, dict) and "SUPERSESSION" in w.get("record_type", "").upper() \
            and "disproven" in w.get("statement", "").lower() and "file-backed .rdata" in w.get("statement", "").lower()
        comp_ok = comp_ok and isinstance(h, dict) and "RETRACTION" in h.get("record_type", "").upper()
        comp_ok = comp_ok and "SUPERSEDED-LOCKED" in e["v4_status"]
    record("v4_1_registry_both_entries_composed_labeled_typed", comp_ok,
           "missing/resume labeled 'composed in V4.1' + the byte-locked constants; why = the typed SUPERSESSION record; the historical record = the typed RETRACTION record")

    # (4) every cited evidence SHA re-hashed from the physical file
    with open(MANIFEST, "r", encoding="ascii", newline="") as f:
        manifest = json.load(f)
    src_total = src_match = 0
    src_null = 0
    src_bad = []
    for c in manifest["claims_19_rows"]:
        for s in c["sources"]:
            lp = s.get("local_path")
            if s.get("sha256") is None:
                # the honest null-SHA disposition (ROW_19/iter034; verified at the R2
                # post-audit): recorded without a frozen SHA; the note must carry it
                src_null += 1
                if "WITHOUT a frozen SHA" not in s.get("note", ""):
                    src_bad.append("%s: null sha WITHOUT the disposition note" % s.get("file"))
                continue
            if not lp or not os.path.isfile(lp):
                src_total += 1
                src_bad.append("%s: MISSING %s" % (s.get("file"), lp))
                continue
            src_total += 1
            if sha256_file(lp).upper() == s["sha256"].upper():
                src_match += 1
            else:
                src_bad.append("%s: SHA MISMATCH at %s" % (s.get("file"), lp))
    record("cited_evidence_sha_rehash_all", src_total > 0 and src_match == src_total and not src_bad,
           "%d/%d cited evidence files re-hashed MATCH from the physical files + %d honest null-SHA disposition (ROW_19/iter034, the noted frozen-matrix pointer)" % (src_match, src_total, src_null) + ("; bad: %s" % src_bad[:3] if src_bad else ""))
    lo_total = lo_match = 0
    for s in manifest["local_only_original_sources"]:
        lo_total += 1
        if sha256_file(s["path"]).upper() == s["sha256"].upper():
            lo_match += 1
    record("local_only_originals_identity_rehash", lo_total == lo_match,
           "%d/%d local-only originals re-hashed MATCH (identity metadata only, zero payloads committed)" % (lo_match, lo_total))

    # (5) the counter split consistency vs oracle_battery.json
    with open(os.path.join(REPAIR, "01_RAW", "oracle_battery.json"), "r", encoding="ascii", newline="") as f:
        ob = json.load(f)
    pcv = ob["platform_cross_validation"]
    platform = pcv["m2e_f32_checked"] + pcv["subnormal_band_f32_checked"] + pcv["f64_checked"] + pcv["arbitrary_rationals_f32_checked"]
    f80 = pcv["f80_exactness_sweep_checked"]
    mcs = manifest["oracle_counter_split"]
    record("counter_split_consistency", platform == 443141 and f80 == 20000 and mcs["platform_cross_validation_samples"] == platform
           and mcs["f80_exactness_sweep_samples"] == f80 and mcs["total"] == 463141,
           "oracle_battery: platform %d + f80 %d = %d TOTAL; the manifest record agrees (443,141 + 20,000 = 463,141)" % (platform, f80, platform + f80))

    # (6) the registry echo == the matrix registry; built_from == the actual files
    record("manifest_echo_equals_v4_1_matrix_registry",
           json.dumps(manifest["era_bounded_registry_v4"], sort_keys=True) == json.dumps(reg, sort_keys=True),
           "the echo mechanically identical to the V4.1 matrix registry (rebuilt from the V4.1 fields)")
    v4j_sha, v4m_sha, mv4_sha = sha256_file(V4_JSON), sha256_file(V4_MD), sha256_file(MANIFEST)
    record("manifest_built_from_shas_updated",
           manifest["built_from"]["M1_GATE_DELIVERABLE_MATRIX_V4.json"]["sha256"].upper() == v4j_sha
           and manifest["built_from"]["M1_GATE_DELIVERABLE_MATRIX_V4.md"]["sha256"].upper() == v4m_sha,
           "built_from carries the actual post-edit SHAs (%s / %s)" % (v4j_sha[:12], v4m_sha[:12]))

    # (7) the PC24 record consistency (the manifest record == the R2 raw artifact, SHA-pinned)
    pc24_sha = sha256_file(PC24_R2)
    with open(PC24_R2, "r", encoding="ascii", newline="") as f:
        pc24 = json.load(f)
    mrec = manifest["pc24_synthetic_remeasurement"]
    record("pc24_measurement_consistency",
           pc24_sha == PC24_PINNED_SHA
           and pc24["measured_synthetic_pc24_mismatches"] == 103073
           and pc24["all_negative_controls_pass"] is True
           and pc24["disposition"]["disposition"] == "CONFIRMED"
           and mrec["measured_synthetic_pc24_mismatches"] == pc24["measured_synthetic_pc24_mismatches"]
           and mrec["disposition"]["disposition"] == "CONFIRMED"
           and mrec["total_synthetic_comparisons"] == 1245184,
           "the R2 artifact SHA == the pinned %s; measured 103,073/1,245,184; disposition CONFIRMED (triple-confirmed per the PE-MASTER post-audit); the manifest record agrees" % PC24_PINNED_SHA[:12])

    # (8) the SHAs recorded inside the GATE_INDEX append == the actual files
    gi_text = open(APPEND_PINS["gate_index"][0], "r", encoding="utf-8", errors="replace").read()
    record("gate_index_append_sha_records",
           (v4j_sha in gi_text) and (v4m_sha in gi_text) and (mv4_sha in gi_text),
           "the appended record carries the actual V4.1/manifest SHAs (%s / %s / %s)" % (v4j_sha[:12], v4m_sha[:12], mv4_sha[:12]))
    # cross-artifact: the semantic gate report scanned exactly these SHAs
    gate_report = os.path.join(RAW, "semantic_gate_report_v4_1.json")
    with open(gate_report, "r", encoding="ascii", newline="") as f:
        gr = json.load(f)
    record("semantic_gate_report_sha_agreement",
           gr["scanned"]["v4_1_json"]["sha256"].upper() == v4j_sha
           and gr["scanned"]["v4_1_md"]["sha256"].upper() == v4m_sha
           and gr["scanned"]["manifest_v4_1"]["sha256"].upper() == mv4_sha
           and gr["verdict"] == "PASS",
           "the gate report scanned the exact current files and its verdict is PASS")

    # (9) the payload scan (pass 1): everything this run will commit IS text, no binary magics
    commit_files = [V4_JSON, V4_MD, MANIFEST, APPEND_PINS["gate_index"][0], APPEND_PINS["amendments"][0]]
    for scan_dir in (RAW, os.path.join(RUN_ROOT, "00_CONTROL"), os.path.join(RUN_ROOT, "06_REPORT")):
        if not os.path.isdir(scan_dir):
            continue
        for dirpath, dirnames, filenames in os.walk(scan_dir):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fn in filenames:
                if fn.endswith(".pyc"):
                    continue
                commit_files.append(os.path.join(dirpath, fn))
    payload_bad = []
    for p in commit_files:
        head = open(p, "rb").read(512)
        if b"\x00" in head or head[:4] in (b"BNT2", b"BNT\x02") or head[:3] == b"\x00\x00\x0a" or head[:2] == b"AK":
            payload_bad.append(p)
    record("payload_scan_pass1_no_proprietary_payloads", not payload_bad,
           "%d to-be-committed files scanned (pass 1); binary-magic hits: %d (the FINAL 100%%-of-commit-set scan runs post-mirror-build: payload_scan_final_v4_1.json)" % (len(commit_files), len(payload_bad)))

    report = {
        "run_id": "PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528",
        "work_item": "W3 - the fail-closed internal-consistency check of the V4.1 package (pass 1; the final 100% payload scan is payload_scan_final_v4_1.json)",
        "checks": results,
        "verdict": "PASS" if ok_all else "FAIL",
        "script_sha256": sha256_file(os.path.abspath(__file__)),
        "v4_1_file_shas": {"M1_GATE_DELIVERABLE_MATRIX_V4.json": v4j_sha,
                           "M1_GATE_DELIVERABLE_MATRIX_V4.md": v4m_sha,
                           "EVIDENCE_MANIFEST_V4.json": mv4_sha},
    }
    with open(os.path.join(RAW, "consistency_report_v4_1.json"), "w", encoding="ascii", newline="") as f:
        json.dump(report, f, indent=1)
        f.write("\n")
    print("CONSISTENCY CHECK (V4.1, pass 1):", report["verdict"])
    for r in results:
        print("  [%s] %s - %s" % (r["verdict"], r["check"], r["detail"]))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
