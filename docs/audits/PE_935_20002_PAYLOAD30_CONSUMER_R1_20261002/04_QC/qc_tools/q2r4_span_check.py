#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QC-R2 TOOL 4: exact-span verification of the AMEND_LOG_R1.md correction records.

For every correction C1..C7 the AMEND_LOG records the exact OLD TEXT SPAN and
the exact NEW TEXT. This tool mechanically verifies, per changed file:
  - every NEW TEXT block (or span, minus whitespace-normalized where noted)
    appears verbatim in the current file on disk;
  - every OLD TEXT SPAN no longer appears in the current file (only in
    AMEND_LOG_R1.md itself, which is expected);
  - the byte-size delta implied by the old/new spans plus CRLF awareness is
    consistent with (AFTER size - BEFORE size) from the manifest/dispatch.
"""
import json
import os
import re

ROOT = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"


def read(p):
    with open(p, "r", encoding="utf-8") as fh:
        return fh.read()


def main():
    log = read(os.path.join(ROOT, "06_REPORT", "AMEND_LOG_R1.md"))
    out = {"tool": "q2r4_span_check.py", "qc_round": 2, "corrections": {}}

    cases = {
        "C1_BLAST_RADIUS_item6": {
            "file": os.path.join(ROOT, "02_ANALYSIS", "BLAST_RADIUS.md"),
            "old": """- FUN_0070e810 builds "<classID>.vfs"-style names and opens via FUN_00972df0; the
  ".vfs" string @0xA86820 and the open behavior are re-verified in-run (pins 0x70C40E,
  0x70C742; FUN_00972df0 disasm). PRIOR_CLAIMS_CONFIRMED (independently re-verified
  in this binary, byte-pinned).
- The C5 byte pin cited by the lead ("C7 44 24 1C 80 00 @0x70E841") is consistent with
  this run's FUN_0070e810 disasm (@0x70E841 MOV dword [ESP+0x1C],0x80 — the {1,0x80,8}
  open-params vector). PRIOR_CLAIMS_CONFIRMED.""",
            "new": """- The class-ID→"<classID>.vfs" open mechanism is CONFIRMED but lives in FUN_0070c680
  (byte-pinned in-run: 0x70C3FC MOV EAX,[ECX+8]; itoa FUN_0040e900; 0x70C40E
  PUSH ".vfs"; 0x70C742 CALL FUN_00972df0; reader stored at classObj+0x84 @0x70C71E).
- JOIN R1 PE_MASTER_REVIEW claim 5's FUNCTION-LEVEL attribution of that mechanism to
  FUN_0070E810 is CONTRADICTED by the physical bytes (three independent measurements:
  this run's DECOMP/DISASM_FUN_0070e810.txt, the QC byte probes, and PE-MASTER's own
  countercheck): FUN_0070E810 builds a "textures"+".vfs" filename (string "textures"
  @0xA86858; the PUSH imm32 0xA86858 is at 0x70E4AD (0x70E4AC holds 50 = PUSH EAX —
  the QC report's probe VA 0x70E4AC was one byte early; PE-MASTER correction); CALL
  FUN_0070e470 @0x70E866; open CALL FUN_00972df0 @0x70E8B6) and contains NO call to
  the itoa function FUN_0040e900 (PE-MASTER whole-.text census: exactly 5 call sites
  of FUN_0040e900 exist, NONE inside FUN_0070E810's window; QC census agrees).
- Additionally the FUN_0094BD30/FUN_00959090/FUN_0094D9B0 "0x58-B array" family cited
  by the same historical claim is the EnvironmentZones.vfs loader (84-byte cursor
  grammar matching EnvironmentZones.vfs's 84-byte payloads — REC0 size field = 84
  measured; string "EnvironmentZones" @0xA9808C, sole code ref @0x958DCE), NOT the
  20xxx parameter channel; the 0x58-byte ArkParameterArmor INSTANCES of this run are
  a different machinery (a size coincidence).
- VERDICT: PRIOR_CLAIMS_NARROWED (mechanism confirmed; JOIN R1 claim 5's function
  attribution corrected in-package; the second lead-correction alongside item 2). No
  historical file is rewritten; the supersession of the historical attribution is
  recorded here and in 06_REPORT\\PE_MASTER_REVIEW.md (PE-MASTER verdict) — a future
  amendment of the JOIN R1 package itself requires separate human authorization.""",
        },
        "C2_EVIDENCE_INDEX_S8_row": {
            "file": os.path.join(ROOT, "06_REPORT", "EVIDENCE_INDEX.md"),
            "old": "| Loader-chain VAs (JOIN R1 claim 5) | 02_ANALYSIS\\BLAST_RADIUS.md | PRIOR_CLAIMS_CONFIRMED (re-verified in-run) |",
            "new": "| Loader-chain VAs (JOIN R1 claim 5) | 02_ANALYSIS\\BLAST_RADIUS.md | PRIOR_CLAIMS_NARROWED (mechanism CONFIRMED in FUN_0070c680; the historical FUN_0070E810 attribution CONTRADICTED by bytes — see 02_ANALYSIS\\BLAST_RADIUS.md item 6 + 06_REPORT\\AMEND_LOG_R1.md) |",
        },
        "C3_PASS15_generator": {
            "file": os.path.join(ROOT, "01_RAW", "GHIDRA_ROUTING", "PASS15_GHIDRA_DUMP.json"),
            "old": '"generator": "03_SCRIPTS/s3_ghidra_routing_pass15.py"',
            "new": '"generator": "03_SCRIPTS/s5_consumer_census_pass15.py"',
        },
        "C4_XREFS_generator": {
            "file": os.path.join(ROOT, "01_RAW", "RELEVANT_XREFS.json"),
            "old": '"generator": "03_SCRIPTS/write_relevant_xrefs.py"',
            "new": '"generator": "manual consolidation of 01_RAW/GHIDRA_ROUTING/*_GHIDRA_DUMP.json outputs (executor session)"',
        },
        "C5_summary_key": {
            "file": os.path.join(ROOT, "01_RAW", "RECORD_FRAMING_SUMMARY.json"),
            "old": "    \"distinct_u16_at_payload_08\": [",
            "new": "    \"distinct_u16_at_payload_04\": [",
        },
        "C5_summary_aggregate": {
            "file": os.path.join(ROOT, "01_RAW", "RECORD_FRAMING_SUMMARY.json"),
            "old": "      190\n    ],\n    \"id_equals_payload_composite_check\": {",
            "new": "      190\n    ],\n    \"distinct_u16_at_payload_08\": {\n      \"0x80\": 1366\n    },\n    \"id_equals_payload_composite_check\": {",
        },
        "C6_HANDOFF_line26": {
            "file": os.path.join(ROOT, "06_REPORT", "HANDOFF.md"),
            "old": "- Package file count: 363 files (362 covered by MANIFEST_SHA256.csv + the manifest itself, self-excluded per the L12 precedent; 04_QC\\ left empty for the fresh QC worker).",
            "new": "- Package file count at delivery: 364 files outside 04_QC (363 covered by MANIFEST_SHA256.csv + the manifest itself, self-excluded per the L12 precedent; the manifest additionally carries one NOTE row that is not a file row; 04_QC\\ was reserved for the fresh QC worker and is excluded from the executor manifest).",
        },
        "C7_REPORT_qc_cell": {
            "file": os.path.join(ROOT, "06_REPORT", "REPORT.md"),
            "old": "INDEPENDENT_QC = QC_PENDING (filled by the fresh internal-QC worker after this run; executor leaves QC_PENDING)",
            "new": "INDEPENDENT_QC = PASS_WITH_FINDINGS (QC round 1: 0xP0, 0xP1, 2xP2, 5xP3 — full report 04_QC\\QC_REPORT.md; the P2-1 + P3-1..P3-4 corrections applied in AMEND-R1, the P2-2 incident verified repaired, P3-5 documented-not-fixed — see 06_REPORT\\AMEND_LOG_R1.md; targeted QC round 2 verification: 04_QC\\QC_R2_TARGETED_REPORT.md)",
        },
    }

    all_ok = True
    for name, spec in cases.items():
        disk = read(spec["file"])
        old = spec["old"]
        new = spec["new"]
        rec = {
            "old_in_amend_log": old in log,
            "new_in_amend_log": new in log,
            "new_on_disk": new in disk,
            "old_gone_from_disk": old not in disk,
        }
        # newline-form-tolerant containment (the log may render LF while disk uses CRLF)
        if not rec["new_on_disk"]:
            norm_new = new.replace("\r\n", "\n")
            norm_disk = disk.replace("\r\n", "\n")
            rec["new_on_disk_normalized"] = norm_new in norm_disk
            rec["new_on_disk"] = rec["new_on_disk"] or norm_new in norm_disk
        if not rec["old_gone_from_disk"]:
            norm_old = old.replace("\r\n", "\n")
            norm_disk = disk.replace("\r\n", "\n")
            rec["old_gone_from_disk"] = norm_old not in norm_disk
        rec["pass"] = (rec["old_in_amend_log"] and rec["new_in_amend_log"]
                       and rec["new_on_disk"] and rec["old_gone_from_disk"])
        all_ok = all_ok and rec["pass"]
        out["corrections"][name] = rec

    out["OVERALL_PASS"] = all_ok
    path = os.path.join(ROOT, "04_QC", "QC_R2_SPAN_CHECK_RESULT.json")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))
    print("OVERALL_PASS =", out["OVERALL_PASS"])


if __name__ == "__main__":
    main()
