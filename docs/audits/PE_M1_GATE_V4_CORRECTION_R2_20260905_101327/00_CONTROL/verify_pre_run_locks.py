#!/usr/bin/env python3
"""PRE_RUN_LOCKS verification for PE_M1_GATE_V4_CORRECTION_R2_20260905_101327.

NEXT_PROMPT section 2 mandate: re-hash ALL 21 pinned inputs before any work.
ANY mismatch => HARD STOP (sections 2 and 4(a)). Fail-closed.
The R2 pin list carries the R1-corrected fail_closed_gates.json pin
(...D59B0371...), independently re-verified by pe-master-auditor.
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

RUN_ID = "PE_M1_GATE_V4_CORRECTION_R2_20260905_101327"
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "01_RAW", "pre_run_locks_verification.json")

# (pin_name, path, pinned_sha256) — pins from NEXT_PROMPT.md section 2 (R2 corrected list)
# Paths cross-referenced against the R1 blocked-run evidence (read-only, preserved).
PINS = [
    ("NEXT_PROMPT_md_this_run (launcher step 1)",
     r"D:\Eudoria_Reconstruction\99_Audits\PE_MASTER_HANDOFFS\PE_M1_GATE_V4_CORRECTION_R2_20260905_101327\NEXT_PROMPT.md",
     "0ACE8F637DB6A75F7BDE095B3FC09BF1DC8016D54DE0E8C46CAE728EE81AA7D9"),
    ("V3_json_GATE_dir_FROZEN",
     r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\GATES\M1_GATE_DELIVERABLE_MATRIX_V3.json",
     "0E46AB2C94EA1BA7B4527950A4D8851AB69DFA48B7DCDDD449F9A52BD39931F8"),
    ("V3_md_GATE_dir_FROZEN",
     r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\GATES\M1_GATE_DELIVERABLE_MATRIX_V3.md",
     "B0B69F0634774CC4032A471D7F69BFF7312D427166DC24217C26B93B2DFF797F"),
    ("old_matrix_md_frozen_copy",
     r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\GATES\M1_GATE_DELIVERABLE_MATRIX.md",
     "F0C7D0F29EEE32F156D4BBF9565724009188BBE8C1C9B0F4CA0BBEC4184D76E1"),
    ("old_matrix_json_frozen_copy",
     r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\GATES\M1_GATE_DELIVERABLE_MATRIX.json",
     "F373E60ABF87BF04CF7CC72A98423B19E861054D3B1F5F10CDD3C2041D478928"),
    ("AMENDMENT_ITER035_ROWS10_11_json",
     r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\GATES\AMENDMENT_ITER035_ROWS10_11.json",
     "2B1FF548D1323BA46D1A8B533BF8BA943B5A508390637C632817D90B58254385"),
    ("GATE_INDEX_md_current_pre_append",
     r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\GATE_INDEX.md",
     "B8FD886BEF3575C048AA1978DE5908D6E0F8068A91EFC172EEB6456391A8A04B"),
    ("GATES_AMENDMENTS_md_current_pre_append",
     r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\GATES\AMENDMENTS.md",
     "5403B19613CD9B6E39C134A9029F92506907B61289BC522523C1C370B4F57125"),
    ("EVIDENCE_MANIFEST_json_current_to_supersede",
     r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\EVIDENCE_MANIFEST.json",
     "0E6FCE502CE487EAFEEA603854AE135D81D40E8AA800F04EB98AB1D5D1459947"),
    ("HANDOFF_md_package_frozen",
     r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\HANDOFF.md",
     "C431BB62C57C68B4399BA478BABD309AFCCDCE4F09B81CA9742D27050EC81EB0"),
    ("RETRACTIONS_md_package_frozen",
     r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\RETRACTIONS.md",
     "A29758BF8DFB0D17BAB8BDADBABE4B26771E3A2F5A5498C3D8F3FF64F83C648B"),
    ("UNRESOLVED_md_package_frozen",
     r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\UNRESOLVED.md",
     "2525CEDFF04B9FD9A0D32917E252C2B7EEB7D463C0D0A26E8294617F6BD80240"),
    ("Charter_NEXT_PROMPT_s12_14",
     r"D:\Eudoria_Reconstruction\99_Audits\PE_MASTER_HANDOFFS\PE_MILESTONE_1_WORLD_SURFACE_R1_20260906_043000\NEXT_PROMPT.md",
     "7A10CD2BE286499540C6668C90E63897781BF6B472541FF0CCB75ADA84562ECA"),
    ("repair_STAGE_ACCEPTANCE_GATES_csv_frozen",
     r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\STAGE_ACCEPTANCE_GATES.csv",
     "3277E5C7A520A87E3F4FFB8157FE6AA576A8F412F023996AC8D58C4676905A3E"),
    ("repair_evidence_oracle_battery_json",
     r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\01_RAW\oracle_battery.json",
     "B04A3175F9E32669795D115271525E344AB823A8071171498845459D267DBFCE"),
    ("repair_evidence_domain_reproof_json",
     r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\01_RAW\domain_reproof.json",
     "E654D2EF34BFF061FACF18794BE2F6A036B8BEFD847ED9308C0990F1795DEC3E"),
    ("repair_evidence_fail_closed_gates_json (R1-corrected pin)",
     r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\01_RAW\fail_closed_gates.json",
     "645C9FC472FA4E93445C539FB375EDADB4DF5890D59B03715F9E914E50C52775"),
    ("repair_evidence_PE_SECTION_MAP_json",
     r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\03_STATIC\PE_SECTION_MAP.json",
     "C5688A5300C4119FD22EA74FD0D739B1E6DFCC77D112C910395061FF1ED11804"),
    ("repair_evidence_CONSTANT_ADDRESS_LOCK_json",
     r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\03_STATIC\CONSTANT_ADDRESS_LOCK.json",
     "6F4A9A6ED2E26F18C59AEB88F571374B73647C80FE19F65D5F0B6466A8D80304"),
    ("repair_evidence_offline_rechecks_json",
     r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\01_RAW\offline_rechecks.json",
     "C80E65D62147E8DED2DE9C3D8EE028DE14BF619CB80C69BE71D30C8F0DEB4E32"),
    ("Entropia_exe_identity_only_never_committed",
     r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe",
     "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"),
]


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main() -> int:
    results = []
    match = mismatch = missing = 0
    for name, path, pinned in PINS:
        if not os.path.isfile(path):
            missing += 1
            results.append({"pin": name, "path": path, "pinned_sha256": pinned,
                            "actual_sha256": None, "verdict": "MISSING"})
            continue
        actual = sha256_file(path)
        ok = (actual.upper() == pinned.upper())
        if ok:
            match += 1
        else:
            mismatch += 1
        results.append({"pin": name, "path": path, "pinned_sha256": pinned,
                        "actual_sha256": actual,
                        "verdict": "MATCH" if ok else "MISMATCH"})
    verdict = "PRE_RUN_LOCKS_ALL_MATCH" if (mismatch == 0 and missing == 0) else "PRE_RUN_LOCKS_MISMATCH"
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
        "r1_history_note": "R1 (PE_M1_GATE_V4_CORRECTION_R1_20260905_100405) HARD-STOPPED on a single-nibble pin transcription error in the R1 prompt (pinned ...D5970371... vs the true ...D59B0371... for fail_closed_gates.json); this R2 list carries the corrected pin independently re-verified by pe-master-auditor (Get-FileHash + certutil cross-check 2026-09-05 10:13).",
        "results": results,
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"verdict={verdict} match={match} mismatch={mismatch} missing={missing}")
    for r in results:
        if r["verdict"] != "MATCH":
            print(f"  {r['verdict']}: {r['pin']} pinned={r['pinned_sha256']} actual={r['actual_sha256']}")
    return 0 if verdict == "PRE_RUN_LOCKS_ALL_MATCH" else 1


if __name__ == "__main__":
    sys.exit(main())
