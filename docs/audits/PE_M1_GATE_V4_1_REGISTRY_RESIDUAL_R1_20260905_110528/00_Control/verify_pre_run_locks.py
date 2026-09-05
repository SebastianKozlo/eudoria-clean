#!/usr/bin/env python3
"""PRE_RUN_LOCKS verification for PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528.

Fail-closed: ANY pinned-input SHA mismatch => HARD STOP (NEXT_PROMPT sections 2 and 4(a)).
Re-hashes EVERY pin: (1) this run's NEXT_PROMPT.md, (2) the 5 current-live editable pins
(SHA-locked BEFORE any edit), (3) the full frozen list (the R2 mandate's 18-pin list,
exact 64-hex values from the R2 NEXT_PROMPT section 2, including the old EVIDENCE_MANIFEST.json).
"""
import hashlib
import json
import os
from datetime import datetime, timezone

RUN_ID = "PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528"
ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528"
GATE = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE"
REPAIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439"
OUT = os.path.join(ROOT, "01_RAW", "pre_run_locks_verification.json")

PINS = [
    # (label, path, pinned_sha256, section)
    ("NEXT_PROMPT_md_this_run (launcher step 1)",
     r"D:\Eudoria_Reconstruction\99_Audits\PE_MASTER_HANDOFFS\PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528\NEXT_PROMPT.md",
     "909256DED9CCEE615B31679FA2DE9570BC9F512B898327E84E6D28431A28828F", "launcher"),
    # CURRENT-LIVE editable (SHA-lock BEFORE start)
    ("V4_md_current_live_editable",
     os.path.join(GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.md"),
     "5B90D2C43B3B0D9E5D9CBB05A387557862A61647D1A29F437F6F18416A744ACD", "current_live"),
    ("V4_json_current_live_editable",
     os.path.join(GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.json"),
     "11FB16B0A175CE183F5C46E734737921DBA0BA72CD975C447CF197C2046F9C58", "current_live"),
    ("EVIDENCE_MANIFEST_V4_json_current_live_editable",
     os.path.join(GATE, "EVIDENCE_MANIFEST_V4.json"),
     "A1E0F5B9C9B342645D9EFAF74319CD9839096B25EC6414C9B7CE165816AB69F8", "current_live"),
    ("GATE_INDEX_md_current_pre_append",
     os.path.join(GATE, "GATE_INDEX.md"),
     "FD68060A63184B94753493D87A04CFB33FBA9667C07DD91D4D5B47810F1CC558", "current_live"),
    ("GATES_AMENDMENTS_md_current_pre_append",
     os.path.join(GATE, "GATES", "AMENDMENTS.md"),
     "C8FF0ABE475E7D37CE790F89CFB941E0FA4A5A0BA23B27921534EFFC6D51D347", "current_live"),
    # FROZEN (R2 mandate's 18-pin list; exact values from R2 NEXT_PROMPT section 2)
    ("V3_json_GATE_dir_FROZEN",
     os.path.join(GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V3.json"),
     "0E46AB2C94EA1BA7B4527950A4D8851AB69DFA48B7DCDDD449F9A52BD39931F8", "frozen"),
    ("V3_md_GATE_dir_FROZEN",
     os.path.join(GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V3.md"),
     "B0B69F0634774CC4032A471D7F69BFF7312D427166DC24217C26B93B2DFF797F", "frozen"),
    ("old_matrix_md_frozen_copy",
     os.path.join(GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX.md"),
     "F0C7D0F29EEE32F156D4BBF9565724009188BBE8C1C9B0F4CA0BBEC4184D76E1", "frozen"),
    ("old_matrix_json_frozen_copy",
     os.path.join(GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX.json"),
     "F373E60ABF87BF04CF7CC72A98423B19E861054D3B1F5F10CDD3C2041D478928", "frozen"),
    ("AMENDMENT_ITER035_ROWS10_11_json",
     os.path.join(GATE, "GATES", "AMENDMENT_ITER035_ROWS10_11.json"),
     "2B1FF548D1323BA46D1A8B533BF8BA943B5A508390637C632817D90B58254385", "frozen"),
    ("EVIDENCE_MANIFEST_json_old_superseded_FROZEN",
     os.path.join(GATE, "EVIDENCE_MANIFEST.json"),
     "0E6FCE502CE487EAFEEA603854AE135D81D40E8AA800F04EB98AB1D5D1459947", "frozen"),
    ("HANDOFF_md_package_frozen",
     os.path.join(GATE, "HANDOFF.md"),
     "C431BB62C57C68B4399BA478BABD309AFCCDCE4F09B81CA9742D27050EC81EB0", "frozen"),
    ("RETRACTIONS_md_package_frozen",
     os.path.join(GATE, "RETRACTIONS.md"),
     "A29758BF8DFB0D17BAB8BDADBABE4B26771E3A2F5A5498C3D8F3FF64F83C648B", "frozen"),
    ("UNRESOLVED_md_package_frozen",
     os.path.join(GATE, "UNRESOLVED.md"),
     "2525CEDFF04B9FD9A0D32917E252C2B7EEB7D463C0D0A26E8294617F6BD80240", "frozen"),
    ("Charter_NEXT_PROMPT_s12_14",
     r"D:\Eudoria_Reconstruction\99_Audits\PE_MASTER_HANDOFFS\PE_MILESTONE_1_WORLD_SURFACE_R1_20260906_043000\NEXT_PROMPT.md",
     "7A10CD2BE286499540C6668C90E63897781BF6B472541FF0CCB75ADA84562ECA", "frozen"),
    ("repair_STAGE_ACCEPTANCE_GATES_csv_frozen",
     os.path.join(REPAIR, "STAGE_ACCEPTANCE_GATES.csv"),
     "3277E5C7A520A87E3F4FFB8157FE6AA576A8F412F023996AC8D58C4676905A3E", "frozen"),
    ("repair_evidence_oracle_battery_json",
     os.path.join(REPAIR, "01_RAW", "oracle_battery.json"),
     "B04A3175F9E32669795D115271525E344AB823A8071171498845459D267DBFCE", "frozen"),
    ("repair_evidence_domain_reproof_json",
     os.path.join(REPAIR, "01_RAW", "domain_reproof.json"),
     "E654D2EF34BFF061FACF18794BE2F6A036B8BEFD847ED9308C0990F1795DEC3E", "frozen"),
    ("repair_evidence_fail_closed_gates_json",
     os.path.join(REPAIR, "01_RAW", "fail_closed_gates.json"),
     "645C9FC472FA4E93445C539FB375EDADB4DF5890D59B03715F9E914E50C52775", "frozen"),
    ("repair_evidence_PE_SECTION_MAP_json",
     os.path.join(REPAIR, "03_STATIC", "PE_SECTION_MAP.json"),
     "C5688A5300C4119FD22EA74FD0D739B1E6DFCC77D112C910395061FF1ED11804", "frozen"),
    ("repair_evidence_CONSTANT_ADDRESS_LOCK_json",
     os.path.join(REPAIR, "03_STATIC", "CONSTANT_ADDRESS_LOCK.json"),
     "6F4A9A6ED2E26F18C59AEB88F571374B73647C80FE19F65D5F0B6466A8D80304", "frozen"),
    ("repair_evidence_offline_rechecks_json",
     os.path.join(REPAIR, "01_RAW", "offline_rechecks.json"),
     "C80E65D62147E8DED2DE9C3D8EE028DE14BF619CB80C69BE71D30C8F0DEB4E32", "frozen"),
    ("Entropia_exe_identity_only_never_committed",
     r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe",
     "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31", "frozen"),
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    results = []
    match = mismatch = missing = 0
    for label, path, pinned, section in PINS:
        if not os.path.isfile(path):
            missing += 1
            results.append({"pin": label, "section": section, "path": path,
                            "pinned_sha256": pinned, "verdict": "MISSING_FILE"})
            continue
        actual = sha256_file(path)
        ok = (actual == pinned.upper())
        if ok:
            match += 1
        else:
            mismatch += 1
        results.append({"pin": label, "section": section, "path": path,
                        "pinned_sha256": pinned, "actual_sha256": actual,
                        "verdict": "MATCH" if ok else "MISMATCH"})

    verdict = "PRE_RUN_LOCKS_ALL_MATCH" if (mismatch == 0 and missing == 0) else "PRE_RUN_LOCKS_FAILURE_HARD_STOP"
    report = {
        "run_id": RUN_ID,
        "purpose": "NEXT_PROMPT section 2 PRE_RUN_LOCKS re-hash (fail-closed; ANY mismatch => HARD STOP per sections 2 and 4(a))",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "tool": "python 3.12.10 hashlib.sha256 (streamed 1MiB chunks)",
        "pin_count": len(PINS),
        "verdict": verdict,
        "match_count": match,
        "mismatch_count": mismatch,
        "missing_count": missing,
        "pin_composition": "1 launcher NEXT_PROMPT + 5 current-live editable (SHA-locked BEFORE edit) + 18 frozen (R2 mandate's 18-pin list, exact 64-hex values from the R2 NEXT_PROMPT section 2)",
        "results": results,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(json.dumps({"verdict": verdict, "match": match, "mismatch": mismatch, "missing": missing,
                      "report": OUT}, indent=2))
    if mismatch or missing:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
