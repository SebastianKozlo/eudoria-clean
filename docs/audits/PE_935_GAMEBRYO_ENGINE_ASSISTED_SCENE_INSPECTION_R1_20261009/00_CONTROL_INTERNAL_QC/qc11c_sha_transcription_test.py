#!/usr/bin/env python3
"""QC11c — DECISIVE raw-byte test: do COUNTERMODEL_RESULTS.json and
FINAL_REPORT.md contain 63/65-char SHA strings for the cm raw outputs,
or is the drop a display artifact? Compares raw bytes of both files with
the true disk hashes. Appends to q11c findings JSON."""
import hashlib
import json
import re

PKG = ("D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean/docs/audits/"
       "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009")
RAW = PKG + "/00_RECORDS_CORRECTION/countermodels/raw"
CMR = PKG + "/00_RECORDS_CORRECTION/COUNTERMODEL_RESULTS.json"
FR = PKG + "/FINAL_REPORT.md"

files = {
    "cm1": ("cm1_escaped_local_output.json", RAW + "/cm1_escaped_local_output.json"),
    "cm2": ("cm2_alias_model_output.json", RAW + "/cm2_alias_model_output.json"),
    "cm3": ("cm3_dword_float_copy_output.json", RAW + "/cm3_dword_float_copy_output.json"),
    "cm4": ("cm4_escaped_subject_outslot_output.json", RAW + "/cm4_escaped_subject_outslot_output.json"),
    "cm5": ("cm5_callback_return_alias_output.json", RAW + "/cm5_callback_return_alias_output.json"),
}

cmr_text = open(CMR, encoding="utf-8").read()
fr_text = open(FR, encoding="utf-8").read()

out = {"tests": []}
for key, (fname, path) in files.items():
    true_sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    # find the sha recorded in COUNTERMODEL_RESULTS.json (inside "(N B, sha256 <hex>)")
    m_cmr = re.search(re.escape(fname) + r" \(\d+ B, sha256 ([0-9a-f]+)\)", cmr_text)
    # find the sha recorded in FINAL_REPORT index (path|size|sha)
    m_fr = re.search(re.escape(fname) + r"\|(\d+)\|([0-9a-f]+)", fr_text)
    rec_cmr = m_cmr.group(1) if m_cmr else None
    rec_fr = m_fr.group(2) if m_fr else None
    t = {
        "file": fname,
        "true_disk_sha": true_sha,
        "true_len": len(true_sha),
        "cmr_recorded_sha": rec_cmr,
        "cmr_len": len(rec_cmr) if rec_cmr else None,
        "cmr_matches_disk": rec_cmr == true_sha,
        "fr_recorded_sha": rec_fr,
        "fr_len": len(rec_fr) if rec_fr else None,
        "fr_matches_disk": rec_fr == true_sha,
    }
    out["tests"].append(t)
    print(json.dumps(t, indent=1))

json.dump(out, open(PKG + "/00_CONTROL_INTERNAL_QC/q11c_sha_transcription_test.json",
                    "w", encoding="utf-8"), indent=1)
