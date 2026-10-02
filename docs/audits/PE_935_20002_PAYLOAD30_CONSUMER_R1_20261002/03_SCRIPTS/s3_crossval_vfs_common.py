#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CROSS-VALIDATION ONLY (contract S14: prior tool used ONLY as cross-validation, labeled as such).
Executor's own framing parse = 03_SCRIPTS/s1_framing_census.py (independent implementation).
Prior tool = JOIN R1 04_TOOLS/vfs_common.py read_vfs().

Compares: record count, per-record frame_start / payload boundaries, exact-EOF status.
Independent-source rationale: the prior tool's grammar {magic, base u32@+8, records@+16,
<IIII header, stride align} is a SEPARATE implementation lineage; agreement of the two
walks on all 1366 boundaries is a consistency check, NOT the primary evidence (the primary
evidence is the executor's own in-run walk + physical bytes).
"""
import sys

# PROCESS NOTE (executor incident repair, documented in 06_REPORT\HANDOFF.md):
# the first execution of this script imported the prior tool WITHOUT suppressing
# bytecode, which caused CPython to create 04_TOOLS\__pycache__\vfs_common.cpython-312.pyc
# inside the JOIN R1 package (a write outside OUTPUT_ROOT). The artifact was deleted and
# the pre-existing group restored to its byte-identical state (verified: 228 files,
# latest write 2026-09-30). This flag prevents any recurrence on re-run.
sys.dont_write_bytecode = True

import json

sys.path.insert(0, r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928\04_TOOLS")
import vfs_common  # prior tool (READ-ONLY reference import)

OUT = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002\01_RAW\CROSSVALIDATION_vfs_common.json"

VFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs"
r = vfs_common.read_vfs(VFS)
rep = {
    "run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
    "generator": "03_SCRIPTS/s3_crossval_vfs_common.py",
    "role": "CROSS_VALIDATION_ONLY (prior tool lineage; labeled)",
    "prior_tool": "JOIN R1 04_TOOLS/vfs_common.py read_vfs()",
    "executor_tool": "03_SCRIPTS/s1_framing_census.py (independent in-run implementation)",
    "prior_tool_result": {
        "ok": r["ok"], "magic": r["magic"], "base": r["base"], "record_count": len(r["records"]),
        "stop_pos": r["stop_pos"], "eof_ok": r["eof_ok"], "crc_fail": r["crc_fail"],
        "ver_bad": r["ver_bad"], "errors": r["errors"],
    },
}

# boundary agreement vs executor rows
exec_rows = []
with open(r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002\01_RAW\RECORD_FRAMING.jsonl") as f:
    for line in f:
        exec_rows.append(json.loads(line))

agree_frame = agree_payload_start = agree_payload_len = agree_id = 0
mismatches = []
prior_records = r["records"]
if len(prior_records) != len(exec_rows):
    mismatches.append("RECORD COUNT MISMATCH: prior=%d executor=%d" % (len(prior_records), len(exec_rows)))
for pr, er in zip(prior_records, exec_rows):
    if pr["file_offset"] == er["frame_start"]:
        agree_frame += 1
    else:
        mismatches.append("frame_start rec %d: prior=%d exec=%d" % (er["record_index"], pr["file_offset"], er["frame_start"]))
    if (pr["file_offset"] + 16) == er["payload_start"]:
        agree_payload_start += 1
    if pr["size"] == er["payload_length"]:
        agree_payload_len += 1
    if pr["id"] == int(er["record_id_hex"], 16):
        agree_id += 1

rep["agreement"] = {
    "records_compared": len(exec_rows),
    "frame_start_agree": agree_frame,
    "payload_start_agree": agree_payload_start,
    "payload_length_agree": agree_payload_len,
    "record_id_agree": agree_id,
    "mismatches": mismatches,
    "verdict": "FULL_BOUNDARY_AGREEMENT" if not mismatches else "DISAGREEMENT",
}
with open(OUT, "w") as f:
    json.dump(rep, f, indent=2)
print(json.dumps(rep["prior_tool_result"], indent=1))
print(rep["agreement"]["verdict"], "frame", agree_frame, "pstart", agree_payload_start,
      "plen", agree_payload_len, "id", agree_id, "of", len(exec_rows))
