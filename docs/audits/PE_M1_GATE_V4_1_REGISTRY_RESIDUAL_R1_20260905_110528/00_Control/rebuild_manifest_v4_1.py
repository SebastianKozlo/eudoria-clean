#!/usr/bin/env python3
# -*- coding: ascii -*-
# rebuild_manifest_v4_1.py - W1 (the manifest echo rebuild): EVIDENCE_MANIFEST_V4.json
# rebuilt FROM THE V4.1 FIELDS:
#   (a) era_bounded_registry_v4[11]/[13] <- the EDITED V4.1 matrix registry entries
#       (mechanical re-derivation from the edited file, never hand-copied);
#   (b) built_from SHAs updated to the post-edit V4 md/json SHAs;
# everything else verified IDENTICAL (fail-loud on any other change).
# The why field in the echo is the typed SUPERSESSION record; the historical
# open-item triple is the typed RETRACTION record (permitted carriers only).
import copy
import hashlib
import json
import os
import sys

RUN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RUN_ROOT, "01_RAW")
REPO_GATE = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE"
V4_JSON = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.json")
V4_MD = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.md")
MANIFEST = os.path.join(REPO_GATE, "EVIDENCE_MANIFEST_V4.json")

PIN_MANIFEST = "A1E0F5B9C9B342645D9EFAF74319CD9839096B25EC6414C9B7CE165816AB69F8"
PIN_V4_JSON_PRE_EDIT = "11FB16B0A175CE183F5C46E734737921DBA0BA72CD975C447CF197C2046F9C58"
PIN_V4_MD_PRE_EDIT = "5B90D2C43B3B0D9E5D9CBB05A387557862A61647D1A29F437F6F18416A744ACD"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def dump_exact(doc):
    return (json.dumps(doc, indent=1, ensure_ascii=True) + "\n").replace("\n", "\r\n").encode("ascii")


def main():
    sha_manifest = sha256_file(MANIFEST)
    if sha_manifest != PIN_MANIFEST:
        raise SystemExit("HARD STOP: the manifest pre-edit SHA mismatch (%s)" % sha_manifest)
    # the edited V4.1 matrix must be the composed state (not the pre-edit pins)
    sha_json_now, sha_md_now = sha256_file(V4_JSON), sha256_file(V4_MD)
    if sha_json_now == PIN_V4_JSON_PRE_EDIT or sha_md_now == PIN_V4_MD_PRE_EDIT:
        raise SystemExit("HARD STOP: the V4 md/json are still the pre-edit state - run compose_registry_v4_1.py first")

    with open(MANIFEST, "r", encoding="ascii", newline="") as f:
        original = json.load(f)
    if dump_exact(original) != open(MANIFEST, "rb").read():
        raise SystemExit("HARD STOP: the manifest round-trip format is not exact - refusing to edit")
    with open(V4_JSON, "r", encoding="ascii", newline="") as f:
        v41 = json.load(f)

    new = copy.deepcopy(original)
    # (a) the registry echo rebuilt FROM THE V4.1 FIELDS (all 19 entries mechanically
    #     re-derived from the edited matrix - byte-equal for the 17 untouched ones)
    new["era_bounded_registry_v4"] = copy.deepcopy(v41["era_bounded_registry_v4"])
    # (b) built_from SHAs updated
    new["built_from"]["M1_GATE_DELIVERABLE_MATRIX_V4.json"]["sha256"] = sha_json_now
    new["built_from"]["M1_GATE_DELIVERABLE_MATRIX_V4.md"]["sha256"] = sha_md_now

    # everything else identical (fail-loud)
    for k, v in original.items():
        if k in ("era_bounded_registry_v4", "built_from"):
            continue
        if json.dumps(v, sort_keys=True) != json.dumps(new[k], sort_keys=True):
            raise SystemExit("HARD STOP: the manifest rebuild leaked into key %r" % k)
    # the echo equality: the rebuilt echo == the matrix registry (mechanical proof)
    if json.dumps(new["era_bounded_registry_v4"], sort_keys=True) != json.dumps(v41["era_bounded_registry_v4"], sort_keys=True):
        raise SystemExit("HARD STOP: the manifest echo != the V4.1 matrix registry")
    # the 17 untouched echo entries still identical to the pre-edit echo
    old_others = [e for i, e in enumerate(original["era_bounded_registry_v4"]) if i not in (11, 13)]
    new_others = [e for i, e in enumerate(new["era_bounded_registry_v4"]) if i not in (11, 13)]
    if json.dumps(old_others, sort_keys=True) != json.dumps(new_others, sort_keys=True):
        raise SystemExit("HARD STOP: the 17 untouched echo entries changed")
    # built_from: only the two SHAs changed; the pc24 entry untouched
    if json.dumps(original["built_from"]["pc24_synthetic_measurement.json"], sort_keys=True) != \
       json.dumps(new["built_from"]["pc24_synthetic_measurement.json"], sort_keys=True):
        raise SystemExit("HARD STOP: the pc24 built_from entry changed")
    if original["built_from"]["M1_GATE_DELIVERABLE_MATRIX_V4.json"]["repo_path"] != new["built_from"]["M1_GATE_DELIVERABLE_MATRIX_V4.json"]["repo_path"] \
            or original["built_from"]["M1_GATE_DELIVERABLE_MATRIX_V4.md"]["repo_path"] != new["built_from"]["M1_GATE_DELIVERABLE_MATRIX_V4.md"]["repo_path"]:
        raise SystemExit("HARD STOP: the built_from repo_paths changed")

    with open(MANIFEST, "wb") as f:
        f.write(dump_exact(new))
    sha_manifest_new = sha256_file(MANIFEST)

    record = {
        "run_id": "PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528",
        "work_item": "W1 - rebuild EVIDENCE_MANIFEST_V4.json from the V4.1 fields",
        "pre_edit_manifest_sha256": sha_manifest,
        "post_edit_manifest_sha256": sha_manifest_new,
        "built_from_updated": {"M1_GATE_DELIVERABLE_MATRIX_V4.json": sha_json_now,
                               "M1_GATE_DELIVERABLE_MATRIX_V4.md": sha_md_now},
        "rebuild_rule": "the registry echo mechanically re-derived FROM THE EDITED V4.1 matrix registry (all 19 entries); built_from SHAs updated; every other key verified IDENTICAL (fail-loud)",
        "script_sha256": sha256_file(os.path.abspath(__file__)),
    }
    with open(os.path.join(RAW, "manifest_rebuild_record_v4_1.json"), "w", encoding="ascii", newline="") as f:
        json.dump(record, f, indent=1)
        f.write("\n")
    print("W1 manifest: %s -> %s" % (sha_manifest, sha_manifest_new))
    return 0


if __name__ == "__main__":
    sys.exit(main())
