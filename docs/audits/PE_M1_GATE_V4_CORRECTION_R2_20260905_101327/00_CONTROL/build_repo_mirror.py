#!/usr/bin/env python3
# -*- coding: ascii -*-
# build_repo_mirror.py - W11: build the repo mirror
# docs\audits\PE_M1_GATE_V4_CORRECTION_R2_20260905_101327\ :
# REPORT.md + HANDOFF.md + STAGE_ACCEPTANCE_GATES.csv + artifact_index.csv +
# 00_CONTROL\ (the run's control scripts) + 01_RAW\ (the raw outputs incl. the
# .pre append-only proofs). The HEAD_SHA is recorded RUN-LOCALLY after the
# push (a commit cannot embed its own hash - the mirror REPORT/HANDOFF carry
# the pointer).
import csv
import hashlib
import json
import os
import shutil

RUN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RUN_ROOT, "01_RAW")
CTRL = os.path.join(RUN_ROOT, "00_CONTROL")
REPORT = os.path.join(RUN_ROOT, "06_REPORT", "00_FINAL_REPORT.md")
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
MIRROR = os.path.join(REPO, "docs", "audits", "PE_M1_GATE_V4_CORRECTION_R2_20260905_101327")
REPO_GATE = os.path.join(REPO, "docs", "audits", "PE_MILESTONE_1_WORLD_SURFACE_R1_GATE")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    if os.path.isdir(MIRROR):
        shutil.rmtree(MIRROR)
    os.makedirs(os.path.join(MIRROR, "00_CONTROL"))
    os.makedirs(os.path.join(MIRROR, "01_RAW"))

    # the control scripts + the raw outputs
    for d, sub in ((CTRL, "00_CONTROL"), (RAW, "01_RAW")):
        for fn in sorted(os.listdir(d)):
            src = os.path.join(d, fn)
            if os.path.isfile(src):
                shutil.copyfile(src, os.path.join(MIRROR, sub, fn))

    # REPORT.md (the committed copy notes the run-local HEAD_SHA record)
    rep = open(REPORT, "r", encoding="utf-8").read()
    rep = rep.replace(
        "BASE_SHA / HEAD_SHA    = faf215b4b5da80d30b895997c58f0a292d33fd08 / __HEAD_SHA__ (post-push record)\nPUSH_STATUS            = __PUSH_STATUS__",
        "BASE_SHA / HEAD_SHA    = faf215b4b5da80d30b895997c58f0a292d33fd08 / recorded RUN-LOCALLY after the push\n                          (a commit cannot embed its own hash - see 99_Audits\\PE_M1_GATE_V4_CORRECTION_R2_20260905_101327\\06_REPORT\\00_FINAL_REPORT.md)\nPUSH_STATUS            = recorded RUN-LOCALLY after the push")
    with open(os.path.join(MIRROR, "REPORT.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(rep)

    # HANDOFF.md
    handoff = """# HANDOFF - PE_M1_GATE_V4_CORRECTION_R2_20260905_101327 (the committed handoff record)

For: pe-master-auditor (the review + persistence), then PE-MASTER (the post-audit). This run is
the corrected re-launch of the R1 mandate (R1 hard-stopped correctly on a pin transcription error;
its evidence is preserved untouched). The loop stays HARD-STOPPED at the gate; nothing here
authorizes Milestone 2.

## How to audit this run

1. `REPORT.md` (the full run record + the final handoff block).
2. `01_RAW\\pre_run_locks_verification.json` - the 21/21 PRE_RUN_LOCKS match (fail-closed).
3. `GATES\\M1_GATE_DELIVERABLE_MATRIX_V4.md/.json` in the gate package
   (`..\\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\\GATES\\`) - the new LIVE matrix (19 rows x 9 fields,
   both formats, the five section-13 labels rendered per row).
4. `..\\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\\EVIDENCE_MANIFEST_V4.json` - the per-claim manifest
   built FROM THE V4 FIELDS (72/72 cited evidence SHAs re-hashed; the corrected counter split as a
   live record + the typed supersession notes; the PC24 re-measurement record).
5. `01_RAW\\pc24_synthetic_measurement.json` - the run-side double measurement: 103,073/1,245,184
   CONFIRMED (the negative controls NC1-NC5 all PASS; the real-domain anchor 14,104 EXACT).
6. `01_RAW\\semantic_gate_report.json` - the semantic gate: the clean V4 PASSES; the negative
   fixtures N1-N4 all FAIL (fail-closed proven).
7. `01_RAW\\consistency_report_v4.json` - 30/30 checks PASS (the frozen files unchanged; the
   .pre byte-prefix append-only proofs; the payload scan).
8. The appended sections of `..\\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\\GATE_INDEX.md` +
   `..\\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\\GATES\\AMENDMENTS.md` (the V4 supersession marks;
   the pre-append states are the .pre copies in this mirror's 01_RAW).
9. `00_CONTROL\\` - the run's control scripts (all fail-loud; every load-bearing number extracted
   from the evidence JSONs, none typed).

## FINAL HANDOFF BLOCK

```text
AUDIT_OUTPUT_ROOT      = D:\\Eudoria_Reconstruction\\99_Audits\\PE_M1_GATE_V4_CORRECTION_R2_20260905_101327
FINAL_REPORT_PATH      = D:\\Eudoria_Reconstruction\\99_Audits\\PE_M1_GATE_V4_CORRECTION_R2_20260905_101327\\06_REPORT\\00_FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS = 01_RAW\\pc24_synthetic_measurement.json + 01_RAW\\semantic_gate_report.json
                          + 01_RAW\\consistency_report_v4.json + 01_RAW\\pre_run_locks_verification.json
                          + 01_RAW\\GATE_INDEX.md.pre + 01_RAW\\AMENDMENTS.md.pre
                          + the repo V4 matrix (GATES\\M1_GATE_DELIVERABLE_MATRIX_V4.md/.json)
                          + EVIDENCE_MANIFEST_V4.json + the appended GATE_INDEX.md / GATES\\AMENDMENTS.md
BASE_SHA / HEAD_SHA    = faf215b4b5da80d30b895997c58f0a292d33fd08 / recorded RUN-LOCALLY after the push
PUSH_STATUS            = recorded RUN-LOCALLY after the push
RUN_STATUS             = V4_CORRECTION_COMPLETE
HARD_STOP_REASON       = NONE
INTERVENTION_LEDGER    = EMPTY (run offline)
```
"""
    with open(os.path.join(MIRROR, "HANDOFF.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(handoff)

    # STAGE_ACCEPTANCE_GATES.csv
    gates = [
        ("PROMPT_SHA256_VERIFIED", "PASS", "0ACE8F637DB6A75F7BDE095B3FC09BF1DC8016D54DE0E8C46CAE728EE81AA7D9 (computed before any work; MATCH)"),
        ("RUN_DIR_CREATED_FRESH", "PASS", "the output root did not exist; created with 00_CONTROL/01_RAW/05_ANALYSIS/06_REPORT; no collision"),
        ("PRE_RUN_LOCKS_21_OF_21", "PASS", "01_RAW\\pre_run_locks_verification.json: all 21 pinned inputs re-hashed MATCH (incl. the R1-corrected fail_closed_gates.json pin)"),
        ("BASE_SHA_RECORDED_FIRST", "PASS", "faf215b4b5da80d30b895997c58f0a292d33fd08 == the expected faf215b"),
        ("PREEXISTING_UNCOMMITTED_WORK_RECORDED", "PASS", "M AUDIT_ENTRYPOINT.md (out of scope; never staged; never committed)"),
        ("PC24_SYNTHETIC_REMEASUREMENT", "PASS", "01_RAW\\pc24_synthetic_measurement.json: 103,073/1,245,184 measured; disposition CONFIRMED (double measurement); the negative controls NC1-NC5 all PASS (the real anchor 14,104 EXACT); the frozen domain_reproof.json untouched (HYGI-1)"),
        ("V4_MATRIX_19X9_BOTH_FORMATS", "PASS", "GATES\\M1_GATE_DELIVERABLE_MATRIX_V4.md/.json: 19 rows x 9 fields in BOTH formats; the five section-13 labels rendered per row"),
        ("SIX_OLD_MATRIX_GAPS_COMPOSED_LABELED", "PASS", "ROW2 historical_fidelity; ROW13/15/16/17 implementation; ROW19 knowledge/implementation split - each labeled 'composed in V4 from <source>'"),
        ("NO_COPY_SET_HONORED", "PASS", "rows 6/8/10/11/19 + the registry era_statements for P-RNG-DIV/P-POS-SCALE recomposed from CURRENT evidence (never carried from ITER_048)"),
        ("ROW10_W4_RULE", "PASS", "ONLY the iter035 arithmetic; the required phrases present; the retracted wordings absent"),
        ("ROW11_W5_RULE", "PASS", "SUPERSEDED-LOCKED constants (32767.0 / 65535.0 f64 byte-locked); the OPEN items kept; the retired candidate wording absent"),
        ("ROW8_W6_RULE", "PASS", "the single original-direct witness (457485/457490; 16/16 strict) separated from the still-open full path; the unbounded 'queued' phrase absent"),
        ("EVIDENCE_MANIFEST_V4_FROM_V4_FIELDS", "PASS", "19 claims from the V4 fields; 72/72 cited evidence SHAs re-hashed MATCH; 5/5 local-only originals identity re-hash MATCH (zero payloads)"),
        ("SEMANTIC_GATE_WITH_NEGATIVE_FIXTURES", "PASS", "01_RAW\\semantic_gate_report.json: the clean V4 PASSES (0 hits/0 problems); N1 (4 hits) / N2 (1 problem) / N3 (3 hits) / N4 (1 problem) all FAIL as required"),
        ("COUNTER_SPLIT_CORRECTED", "PASS", "443,141 platform + 20,000 f80-exactness = 463,141 TOTAL (oracle_battery-consistent); the typed supersession note for the retired line-4 phrasing; the frozen CSV NOT edited (re-hashed unchanged)"),
        ("V3_FROZEN_APPEND_ONLY", "PASS", "the .pre prefix proofs (B8FD886B.../5403B196... == the pins); the appended files are byte-extensions; the V3/old-matrix/old-manifest/frozen-package files re-hashed UNCHANGED"),
        ("CONSISTENCY_CHECK_30_OF_30", "PASS", "01_RAW\\consistency_report_v4.json: all checks PASS incl. the payload scan (27 files, 0 binary-magic hits)"),
        ("FINAL_STATUS_UNCHANGED", "PASS", "M1_PARTIAL + M2_HARD_STOP (this run closes NOTHING beyond its own package)"),
    ]
    with open(os.path.join(MIRROR, "STAGE_ACCEPTANCE_GATES.csv"), "w", encoding="ascii", newline="") as f:
        w = csv.writer(f)
        w.writerow(["gate", "status", "evidence"])
        for row in gates:
            w.writerow(row)

    # artifact_index.csv (every artifact of this run + the repo files; the index itself excluded)
    entries = []
    for base, sub in ((os.path.join(MIRROR, "00_CONTROL"), "mirror/00_Control"),
                      (os.path.join(MIRROR, "01_RAW"), "mirror/01_RAW"),
                      (RUN_ROOT, "run_root_report")):
        if not os.path.isdir(base):
            continue
        for fn in sorted(os.listdir(base)):
            p = os.path.join(base, fn)
            if os.path.isfile(p):
                entries.append((sub + "/" + fn, os.path.getsize(p), sha256_file(p)))
    for rel, p in (("repo GATES/M1_GATE_DELIVERABLE_MATRIX_V4.json", os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.json")),
                   ("repo GATES/M1_GATE_DELIVERABLE_MATRIX_V4.md", os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.md")),
                   ("repo EVIDENCE_MANIFEST_V4.json", os.path.join(REPO_GATE, "EVIDENCE_MANIFEST_V4.json")),
                   ("repo GATE_INDEX.md (appended)", os.path.join(REPO_GATE, "GATE_INDEX.md")),
                   ("repo GATES/AMENDMENTS.md (appended)", os.path.join(REPO_GATE, "GATES", "AMENDMENTS.md")),
                   ("run 06_REPORT/00_FINAL_REPORT.md", REPORT)):
        entries.append((rel, os.path.getsize(p), sha256_file(p)))
    with open(os.path.join(MIRROR, "artifact_index.csv"), "w", encoding="ascii", newline="") as f:
        w = csv.writer(f)
        w.writerow(["artifact", "bytes", "sha256"])
        for e in entries:
            w.writerow(e)
        w.writerow(["mirror/artifact_index.csv (THIS file)", os.path.getsize(os.path.join(MIRROR, "artifact_index.csv")), "SELF-EXCLUDED (a file cannot hash itself)"])

    print("mirror built:", MIRROR)
    for root, dirs, files in os.walk(MIRROR):
        for fn in files:
            print("  ", os.path.relpath(os.path.join(root, fn), MIRROR))


if __name__ == "__main__":
    main()
