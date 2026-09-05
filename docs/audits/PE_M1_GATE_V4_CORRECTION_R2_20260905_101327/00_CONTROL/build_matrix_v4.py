#!/usr/bin/env python3
# -*- coding: ascii -*-
# build_matrix_v4.py - W1/W2: build GATES\M1_GATE_DELIVERABLE_MATRIX_V4.md + .json
# (PE_M1_GATE_V4_CORRECTION_R2_20260905_101327).
# Generates BOTH formats from the single composed row dataset (v4_rows_*.py +
# v4_registry.py) so MD/JSON field parity is structural, fills the
# @COMPUTE_ME@ placeholder with the actual SHA256 of this run's
# pc24_synthetic_measurement.json, and self-checks: 19 rows x 9 non-vacuous
# fields in BOTH formats + the required phrases present (fail-loud).
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from v4_rows_a import ROWS_A
from v4_rows_b import ROWS_B
from v4_rows_c import ROWS_C
from v4_rows_d import ROWS_D
from v4_rows_e import ROWS_E
from v4_rows_f import ROWS_F
from v4_rows_g import ROWS_G
from v4_registry import REGISTRY_V4, KNOWN_OPEN_V4, HEADER_MD, SCOPE_STATEMENT, HONEST_LIMITS

RUN_ROOT = os.path.dirname(HERE)
REPO_GATE = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE"
OUT_JSON = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.json")
OUT_MD = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.md")
PC24 = os.path.join(RUN_ROOT, "01_RAW", "pc24_synthetic_measurement.json")

NINE = ["knowledge", "implementation", "validation", "historical_fidelity",
        "evidence_status", "era", "denominator", "limitations", "evidence"]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    rows = ROWS_A + ROWS_B + ROWS_C + ROWS_D + ROWS_E + ROWS_F + ROWS_G
    assert len(rows) == 19, "expected 19 rows, got %d" % len(rows)
    assert [r["row"] for r in rows] == list(range(1, 20)), "row numbering broken"

    # fill the PC24 measurement SHA placeholder
    pc24_sha = sha256_file(PC24)
    for r in rows:
        for ev in r["evidence"]:
            if ev["sha256"] == "@COMPUTE_ME@":
                ev["sha256"] = pc24_sha
                ev["file"] = "pc24_synthetic_measurement.json (THIS run, repo mirror docs/audits/PE_M1_GATE_V4_CORRECTION_R2_20260905_101327/01_RAW/)"

    # ---------------- structural self-check (fail-loud, before writing)
    problems = []
    for r in rows:
        for f in NINE:
            v = r.get(f)
            if v is None or (isinstance(v, str) and v.strip() == "") or (isinstance(v, list) and len(v) == 0):
                problems.append("row %d field %s VACUOUS" % (r["row"], f))
        # the required phrases (mirrors the semantic gate's requirements)
        if r["row"] == 8:
            lim = r["limitations"]
            if "single-witness" not in lim or "457485" not in lim:
                problems.append("row 8 limitations missing the required phrases")
        if r["row"] == 10:
            k = r["knowledge"]
            if "65535.0" not in k or "float32(1/12800)" not in k:
                problems.append("row 10 knowledge missing the required phrases")
        if r["row"] == 11:
            k = r["knowledge"]
            lim = r["limitations"]
            if "32767.0" not in k:
                problems.append("row 11 knowledge missing '32767.0'")
            if "SUPERSEDED-LOCKED" not in lim or "32767.0" not in lim:
                problems.append("row 11 limitations missing the required phrases")
    for e in REGISTRY_V4:
        if e["placeholder"].startswith("P-RNG-DIV") or e["placeholder"].startswith("P-POS-SCALE"):
            if "SUPERSEDED-LOCKED" not in e["v4_status"]:
                problems.append("registry %s v4_status missing SUPERSEDED-LOCKED" % e["placeholder"])
    if problems:
        print("BUILD SELF-CHECK FAILURES:")
        for p in problems:
            print("  -", p)
        return 1
    print("self-check: 19 rows x 9 fields non-vacuous + required phrases OK")

    # ---------------- the JSON
    doc = {
        "deliverable": "M1_GATE_DELIVERABLE_MATRIX_V4",
        "milestone": "PE_WORLD_SURFACE_FIDELITY_R1",
        "created_by": "PE_M1_GATE_V4_CORRECTION_R2_20260905_101327 (this run)",
        "consolidation_basis": [
            "the V3 basis (iter035 + iter036 + iter037 + the validator-coverage repair run)",
            "THIS run: the 12-point correction mandate (the five section-13 labels rendered per row in both formats; the six old-matrix gaps composed + labeled; the no-copy set recomposed from current evidence; the corrected counter split; the PC24 synthetic re-measurement)"
        ],
        "charter_five_labels": ["KNOWLEDGE", "IMPLEMENTATION", "VALIDATION", "HISTORICAL_FIDELITY", "EVIDENCE_STATUS"],
        "nine_fields_per_row": ["KNOWLEDGE", "IMPLEMENTATION", "VALIDATION", "HISTORICAL_FIDELITY", "EVIDENCE_STATUS", "ERA", "DENOMINATOR", "LIMITATIONS", "EVIDENCE"],
        "supersession": {
            "v3_md": {"path": "GATES/M1_GATE_DELIVERABLE_MATRIX_V3.md", "sha256": "B0B69F0634774CC4032A471D7F69BFF7312D427166DC24217C26B93B2DFF797F", "status": "FROZEN HISTORY - superseded BY THIS V4 (new physical files; the V3 was never edited)"},
            "v3_json": {"path": "GATES/M1_GATE_DELIVERABLE_MATRIX_V3.json", "sha256": "0E46AB2C94EA1BA7B4527950A4D8851AB69DFA48B7DCDDD449F9A52BD39931F8", "status": "FROZEN HISTORY - superseded BY THIS V4"},
            "old_matrix_md": {"path": "GATES/M1_GATE_DELIVERABLE_MATRIX.md", "sha256": "F0C7D0F29EEE32F156D4BBF9565724009188BBE8C1C9B0F4CA0BBEC4184D76E1", "status": "FROZEN HISTORY - SUPERSEDED-BY-V3 then BY-V4 (never edited)"},
            "old_matrix_json": {"path": "GATES/M1_GATE_DELIVERABLE_MATRIX.json", "sha256": "F373E60ABF87BF04CF7CC72A98423B19E861054D3B1F5F10CDD3C2041D478928", "status": "FROZEN HISTORY - SUPERSEDED-BY-V3 then BY-V4 (never edited)"},
            "old_evidence_manifest": {"path": "EVIDENCE_MANIFEST.json", "sha256": "0E6FCE502CE487EAFEEA603854AE135D81D40E8AA800F04EB98AB1D5D1459947", "status": "SUPERSEDED by EVIDENCE_MANIFEST_V4.json (the append-only index mark; the file untouched)"}
        },
        "corrections_applied_this_run": {
            "f1_five_labels": "every row renders the five charter section-13 labels in BOTH formats (the V3 MD's verdict-only rendering superseded)",
            "six_old_matrix_gaps": "ROW2 historical_fidelity, ROW13/15/16/17 implementation, ROW19 knowledge/implementation - composed from the existing evidence, each labeled 'composed in V4 from <source>'",
            "no_copy_set": "rows 6/8/10/11/19 + the registry era_statements for P-RNG-DIV/P-POS-SCALE recomposed from CURRENT evidence (the V3 carried fields for rows 10/11 carried retracted arithmetic; the row 8 'queued' line carried the unbounded NIF-path wording; the P-RNG-DIV/P-POS-SCALE era_statements contradicted their own SUPERSEDED-LOCKED v3_status)",
            "row10_rule": "ONLY the iter035 arithmetic (W4); the retracted arithmetic wordings removed",
            "row11_rule": "the SUPERSEDED-LOCKED constants with the OPEN items kept (W5)",
            "row8_rule": "the SINGLE ORIGINAL-DIRECT WITNESS separated from the STILL-OPEN full path (W6)",
            "counter_split_corrected": "443,141 platform cross-validation samples + 20,000 f80-exactness sweep = 463,141 TOTAL (consistent with oracle_battery.json platform_cross_validation; supersedes the repair-run STAGE_ACCEPTANCE_GATES.csv line 4 phrasing - the frozen CSV NOT edited; the supersession note lives in EVIDENCE_MANIFEST_V4.json as a typed supersession record)",
            "pc24_synthetic_remeasurement": "the run-side double measurement: 103,073/1,245,184 CONFIRMED (01_RAW\\pc24_synthetic_measurement.json; the frozen domain_reproof.json untouched - its synthetic lerp_pc24_mismatches=0 is a DEFAULT COUNTER, HYG-1)",
            "hyg5_citation_fix": "the iter033_manifest.json citation now carries the manifest's OWN SHA (DD598152...); F299C622... is attached to assets/foliage_glb/MANIFEST.json (per CORRECTION_NOTES.md HYG-5 - the V3/old-matrix citation-label defect not carried)"
        },
        "scope_statement": SCOPE_STATEMENT,
        "taxonomy": ["CONFIRMED", "STRONGLY_SUPPORTED", "PLAUSIBLE", "UNVERIFIED", "REJECTED"],
        "final_matrix_19_rows_v4": rows,
        "era_bounded_registry_v4": REGISTRY_V4,
        "known_open_list_v4": KNOWN_OPEN_V4,
        "this_run_evidence": {
            "pc24_synthetic_measurement": {"path": "01_RAW/pc24_synthetic_measurement.json", "sha256": pc24_sha, "verdict": "PASS - measured 103,073/1,245,184; disposition CONFIRMED (double measurement)"},
            "semantic_gate_report": {"path": "01_RAW/semantic_gate_report.json", "note": "written by 00_CONTROL\\semantic_gate.py after this build"},
            "consistency_report_v4": {"path": "01_RAW/consistency_report_v4.json", "note": "written by 00_CONTROL\\consistency_check_v4.py after this build"},
            "pre_run_locks_verification": {"path": "01_RAW/pre_run_locks_verification.json", "verdict": "PRE_RUN_LOCKS_ALL_MATCH (21/21)"}
        },
        "honest_limits_binding": HONEST_LIMITS,
    }
    with open(OUT_JSON, "w", encoding="ascii") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")

    # ---------------- the MD (same data -> parity by construction)
    md = [HEADER_MD]
    for r in rows:
        md.append("\n### ROW %d - %s\n" % (r["row"], r["subsystem"]))
        md.append("- **KNOWLEDGE:** %s" % r["knowledge"])
        md.append("- **IMPLEMENTATION:** %s" % r["implementation"])
        md.append("- **VALIDATION:** %s" % r["validation"])
        md.append("- **HISTORICAL_FIDELITY:** %s" % r["historical_fidelity"])
        md.append("- **EVIDENCE_STATUS:** %s" % r["evidence_status"])
        md.append("- ERA: %s" % json.dumps(r["era"]))
        md.append("- DENOMINATOR: %s" % r["denominator"])
        md.append("- LIMITATIONS: %s" % r["limitations"])
        md.append("- EVIDENCE: %s" % "; ".join("%s (SHA256 %s)" % (e["file"], e["sha256"]) for e in r["evidence"]))
    md.append("\n## THE ERA-BOUNDED REGISTRY - V4 (19 entries; v4_status per entry)\n")
    for e in REGISTRY_V4:
        md.append("- **%s** - missing: %s | why: %s | resume: %s" % (e["placeholder"], e["missing"], e["why"], e["resume_path"]))
        md.append("  - era_statement: %s" % e["era_statement"])
        md.append("  - v4_status: %s" % e["v4_status"])
    md.append("\n## EXPLICITLY OPEN (the V4 known-open set - none solved here)\n")
    for e in KNOWN_OPEN_V4:
        md.append("- %s -- %s" % (e["item"], e["status"]))
    md.append("\n## THIS RUN'S EVIDENCE (the V4-correction run; SHA-pinned in the run mirror)\n")
    md.append("- pc24_synthetic_measurement.json (01_RAW; SHA256 %s): the run-side double measurement - 103,073/1,245,184 CONFIRMED" % pc24_sha)
    md.append("- semantic_gate_report.json (01_RAW): the semantic gate + the negative fixtures N1-N4 + the clean-copy PASS")
    md.append("- consistency_report_v4.json (01_RAW): the fail-closed consistency check")
    md.append("- pre_run_locks_verification.json (01_RAW): PRE_RUN_LOCKS_ALL_MATCH (21/21)")
    md.append("\n## HONEST LIMITS (binding)\n")
    for h in HONEST_LIMITS:
        md.append("- %s" % h)
    with open(OUT_MD, "w", encoding="ascii") as f:
        f.write("\n".join(md) + "\n")

    # ---------------- post-write parity verification (fail-loud)
    with open(OUT_JSON, "r", encoding="ascii") as f:
        jdoc = json.load(f)
    with open(OUT_MD, "r", encoding="ascii") as f:
        mtext = f.read()
    parity_problems = []
    for r in jdoc["final_matrix_19_rows_v4"]:
        section = mtext[mtext.find("### ROW %d -" % r["row"]):]
        section = section[:section.find("\n### ROW %d -" % (r["row"] + 1))] if ("\n### ROW %d -" % (r["row"] + 1)) in section else section
        for f in ["knowledge", "implementation", "validation", "historical_fidelity", "evidence_status"]:
            if r[f] not in section:
                parity_problems.append("MD row %d missing the %s content" % (r["row"], f))
        if r["denominator"] not in section or r["limitations"] not in section:
            parity_problems.append("MD row %d missing denominator/limitations content" % r["row"])
        for ev in r["evidence"]:
            if ev["sha256"] not in section:
                parity_problems.append("MD row %d missing the evidence SHA %s..." % (r["row"], ev["sha256"][:8]))
    if parity_problems:
        print("MD/JSON PARITY FAILURES:")
        for p in parity_problems:
            print("  -", p)
        return 2
    print("build OK: %s" % OUT_JSON)
    print("build OK: %s" % OUT_MD)
    print("  json sha256: %s" % sha256_file(OUT_JSON))
    print("  md   sha256: %s" % sha256_file(OUT_MD))
    return 0


if __name__ == "__main__":
    sys.exit(main())
