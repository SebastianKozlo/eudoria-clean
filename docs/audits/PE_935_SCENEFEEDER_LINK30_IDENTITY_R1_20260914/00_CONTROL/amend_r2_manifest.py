# -*- coding: utf-8 -*-
# PE_935_SCENEFEEDER_LINK30_AMEND_R2_20260914 (completion batch C1) - bounded
# MANIFEST_SHA256.csv updater, C1 edition.
#
# Delta vs this script's R2 edition (pre-batch SHA256
# 5A20758EC65BA6E37E185E7E759DF7297B9F134C4AEFDB34B83488A2A61CE8D4, carried by the
# pre-batch SCRIPT_SHA256.csv row):
#   1. the authorized/expected-change set is EXTENDED with 06_REPORT/HANDOFF.md
#      (the completion batch applies the AMEND_LOG_R2 section-2h prepared text +
#      the gates-line annotation), so the authorized change set vs the PUBLISHED
#      package == exactly {06_REPORT/REPORT.md, 06_REPORT/QC_AUDIT_R1.md,
#      03_EVIDENCE/README.md, 00_CONTROL/SCRIPT_SHA256.csv, 06_REPORT/HANDOFF.md};
#   2. the change set is verified against the PUBLISHED 32-row manifest baseline
#      (embedded below as PUBLISHED_BASELINE; byte-equal to the committed
#      06_REPORT/MANIFEST_SHA256.csv at BASE_SHA 3644e5ac...; an auditor re-derives
#      it with `git show HEAD:docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/06_REPORT/MANIFEST_SHA256.csv`)
#      because the on-disk manifest already carries the R2-amendment hashes (37
#      rows) and would mask the amendment-total change set;
#   3. the five new-file rows are NOT re-added (already present in the on-disk
#      manifest since the R2 updater run); they are re-asserted present and on
#      disk, with the two batch-edited ones (the log, this script) asserted
#      CHANGED vs their pre-batch manifest rows and the other three asserted
#      byte-identical;
#   4. the output is the final 37-row manifest with FRESH disk hashes for every
#      row (so 06_REPORT/AMEND_LOG_R2.md's row carries the log's FINAL hash and
#      this script's own row carries its post-edit hash).
# Unchanged semantics: verify EVERY row fail-closed against disk; all published
# rows outside the authorized change set byte-identical to the baseline;
# self-exclusion held (the manifest is never a row, L12); deterministic output
# (rows sorted by path, csv QUOTE_MINIMAL, CRLF line endings); build twice and
# compare. The manifest's own on-disk SHA256 is not self-recordable (L12) - it is
# reported in the executor's delivery notice.
#
# ONE-SHOT: run exactly ONCE, as the LAST package mutation of the completion
# batch (after the C1..C5 content edits, after this script's own edit, and after
# the SCRIPT_SHA256.csv refresh). Any later re-run fails fail-closed by design
# (the same one-shot character as the R2 edition).
#
# STATIC-ONLY amendment bookkeeping: no binary decode here, no git mutation, no
# git invocation (the baseline is embedded; this script is self-contained).

import csv
import hashlib
import io
import os
import sys

PKG = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
       r"\PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914")
MAN = os.path.join(PKG, "06_REPORT", "MANIFEST_SHA256.csv")

EXPECTED_CHANGE = {
    "06_REPORT/REPORT.md",
    "06_REPORT/QC_AUDIT_R1.md",
    "03_EVIDENCE/README.md",
    "00_CONTROL/SCRIPT_SHA256.csv",
    "06_REPORT/HANDOFF.md",
}
NEW_ROWS = {
    "06_REPORT/AMEND_LOG_R2.md",
    "01_RAW/F1_GLOBALPTR_PROOF_RAW.txt",
    "00_CONTROL/f1_globalptr_proof.py",
    "00_CONTROL/amend_r2_manifest.py",
    "02_ANALYSIS/SF30_WRITER_CENSUS_SUPERSESSION_R2.md",
}
# the two new-file rows the completion batch itself edits (before the re-run)
BATCH_EDITED_NEW = {
    "06_REPORT/AMEND_LOG_R2.md",
    "00_CONTROL/amend_r2_manifest.py",
}

# The PUBLISHED 32-row manifest baseline (BASE_SHA 3644e5ac... == HEAD, the
# LINK30 publication commit). Embedded read-only; generated from
# `git show HEAD:docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/06_REPORT/MANIFEST_SHA256.csv`.
PUBLISHED_BASELINE = {
    "00_CONTROL/RUN_CONTRACT.md": "7416a3c9642d4e088abbfb5548242e1511e966c63468e12839842270810d6609",
    "00_CONTROL/SCRIPT_SHA256.csv": "0c2de0b2c7db5fdde7d71d883351a8fe540a49c8b7aa9d809312561be2228b61",
    "00_CONTROL/SOURCE_IDENTITIES.json": "0f6a72721168222619bda4bc3913d7f71e9aac151919986e831d0015e57bb1ff",
    "00_CONTROL/census.py": "7c4d705575238ddc4a27d01dcc1ea92bade8fa0ee42d400eb2697f1d75b4723f",
    "00_CONTROL/census_state.json": "d175e7919c8fa662b089e1e4ee5569ea4a606f6d315bb101af0f7e568add87a3",
    "00_CONTROL/finalize.py": "4df58fbf8132168976554189ef4b758a4554d29698f72f32f5bc1cfe46c0b868",
    "00_CONTROL/qc_probe/out_qc1_counters.txt": "dfe4b37d71cdbaaddc28dbd0c422207f359c1fa1881ecfe2b0beadae4001e0b4",
    "00_CONTROL/qc_probe/out_qc2_bytes.txt": "db3bc4cf5c79181a4eac01da5fbff5ff57598f96a9a33300a14796a3fa5d0bbe",
    "00_CONTROL/qc_probe/out_qc3_sweep.txt": "05509b777dbb9ccce3c945b816951c487c0fc7e8d3a1e343a8e18035f3daaa46",
    "00_CONTROL/qc_probe/out_qc4_sample_scope.txt": "6786160f8597510eae019b930372865980ecac40a857aa54b37a0ac612a2f466",
    "00_CONTROL/qc_probe/out_qc4b_scope_bytes.txt": "741cff6084a5d7a8bc52afa9b2aec3663c96f34d9cc8cd4e0542e909f020b5a3",
    "00_CONTROL/qc_probe/out_qc5_final.txt": "71b99bc7403497fa9f7f63544fd4f8f99efc8ed5905320481eafb2c6a0128ac0",
    "00_CONTROL/qc_probe/qc1_counters.py": "bb7ff3ad8b19a635a79c843797a3e20781ae9f3a9d5d37397bfff5ec9338aa65",
    "00_CONTROL/qc_probe/qc2_bytes.py": "dce9091ab93877b78e39309e7b2afd244c630ba7d31f32e5fb591c7ec6e6c98b",
    "00_CONTROL/qc_probe/qc3_sweep.py": "9af5b188d3a21fb7a6bdab4e2d2fd21acfa69548fd14a8beec8f96f6b8601e8d",
    "00_CONTROL/qc_probe/qc4_sample_scope.py": "22e9ac4cf76625076fa7b2d5e8ea200bcc041b8a20fc15b07634a29d49b3d942",
    "00_CONTROL/qc_probe/qc4b_scope_bytes.py": "430b80ce6ab7b52d2b4f456b15b86552fd0c7d11b3faede5bbb4c16270dd8959",
    "00_CONTROL/qc_probe/qc5_final.py": "2ddad0cb40384d3d040f568e0039be04b5752ff19ad141b56957df5ffa56e1b0",
    "00_CONTROL/sf30_core.py": "cd6bc11f2af482fd587bf24d6291242caf652fb0189cebb83b7a18a2ee42907e",
    "01_RAW/POSITIVE_CONTROL_0050A050.txt": "4bfd3bb14bc815bd8b2b1b4d150430a40df4e848c54ec1214c3898342cfa8d18",
    "01_RAW/SF30_RTTI_RAW.txt": "399c4cfb5a83728b019d51de805bff2fdc2f5d753e87c909f8e0a43e8326aee5",
    "01_RAW/SF30_WRITER_RAW.txt": "64402a73013b52943e10ae17bb115f466a0d3bef98aa3835915cf3c1cd572248",
    "02_ANALYSIS/SF30_PROVENANCE.md": "a2f48326ce7b795b8b4067c6e719cbdbf0a082627a1c2b660c36d980a296452c",
    "02_ANALYSIS/SF30_WRITER_CENSUS.csv": "71552e2a4bfc120da0be1a7e108a41a03c873addd238637dd7c18f3c968824d0",
    "03_EVIDENCE/README.md": "fdbe55b810583ec33833b16a8da48553bdb207a4a14474d087445004f64bc360",
    "06_REPORT/AMEND_LOG_R1.md": "52b19b44c50eb924a2e7b6967ec9b26d4224959ade02019581acbc41d3d2ad2d",
    "06_REPORT/HANDOFF.md": "71a2b1c127ecf4f7191bb9d8e3b3b769b2e41eaaf38137c8d6ca45610e943bc8",
    "06_REPORT/MANIFEST_NOTE_PUBLICATION.md": "6f832230769d78ed02a7a6daf26875e548bdf559e7f8b4cc42c8781a47fd0410",
    "06_REPORT/PE_MASTER_REVIEW.md": "411e471701161013ce0f7b3067cd8d099248745107c17126e01c1fda5892b7f0",
    "06_REPORT/QC_AUDIT_R1.md": "b80dd10b42f9a40ec1e211cf3dd508d4206b35017b3e3f64370aac338ef6040a",
    "06_REPORT/REPORT.md": "e08a5875790f5a3fdca539c5a3be4c717515d08abbe5937f73cd33ceece5436d",
    "06_REPORT/STAGE_ACCEPTANCE_GATES.csv": "375798e82c80e7ed4ec388db486a22856c9409a5a397ff10582e1d0188121968",
}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def disk(rel):
    return sha256_file(os.path.join(PKG, *rel.split("/")))


def build():
    rows = sorted(set(PUBLISHED_BASELINE) | NEW_ROWS)
    assert "06_REPORT/MANIFEST_SHA256.csv" not in rows, "self-listed (L12)"
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["file", "sha256"])
    for rel in rows:
        if rel == "06_REPORT/MANIFEST_SHA256.csv":
            continue
        w.writerow([rel, disk(rel)])
    return buf.getvalue().encode("utf-8")


def main():
    raw = open(MAN, "rb").read()
    assert raw.endswith(b"\r\n"), "unexpected manifest line-ending format"
    parsed = list(csv.reader(io.StringIO(raw.decode("utf-8"))))
    header, data = parsed[0], [r for r in parsed[1:] if r]
    assert header == ["file", "sha256"], "unexpected manifest header: %r" % header
    man = {r[0]: r[1] for r in data}
    assert len(man) == len(data) == 37, "expected 37 data rows, got %d" % len(data)
    assert "06_REPORT/MANIFEST_SHA256.csv" not in man, "manifest self-listed (L12 violated)"

    # 1. the row set must be exactly baseline | new rows (nothing added/removed)
    assert set(man) == set(PUBLISHED_BASELINE) | NEW_ROWS, "row set mismatch"

    # 2. fail-closed existence for every expected path
    for rel in sorted(set(PUBLISHED_BASELINE) | NEW_ROWS):
        p = os.path.join(PKG, *rel.split("/"))
        assert os.path.exists(p), "expected path not on disk: %s" % rel

    # 3. the change set vs the PUBLISHED baseline == EXACTLY the authorized set
    changed = set()
    for rel, h in PUBLISHED_BASELINE.items():
        if disk(rel) != h:
            changed.add(rel)
    assert changed == EXPECTED_CHANGE, (
        "change set mismatch vs published baseline; expected %s, measured %s"
        % (sorted(EXPECTED_CHANGE), sorted(changed)))

    # 4. all other published rows byte-identical to the baseline
    for rel, h in PUBLISHED_BASELINE.items():
        if rel not in EXPECTED_CHANGE:
            assert disk(rel) == h, "published row not byte-identical: %s" % rel

    # 5. new-file rows: present in the manifest; the two batch-edited ones must
    #    differ from their pre-batch manifest rows, the other three byte-identical
    for rel in sorted(NEW_ROWS):
        assert rel in man, "new-file row missing from manifest: %s" % rel
        if rel in BATCH_EDITED_NEW:
            assert disk(rel) != man[rel], "batch-edited new row unchanged: %s" % rel
        else:
            assert disk(rel) == man[rel], "new row not byte-identical: %s" % rel

    # 6. deterministic build (build twice, compare)
    out1 = build()
    out2 = build()
    assert out1 == out2, "determinism self-check failed"

    # 7. output asserts: 37 rows, self-exclusion, baseline/changed split
    new_parsed = list(csv.reader(io.StringIO(out1.decode("utf-8"))))
    assert new_parsed[0] == ["file", "sha256"]
    new_man = {r[0]: r[1] for r in new_parsed[1:]}
    assert len(new_man) == len(new_parsed) - 1 == 37, (
        "expected 37 data rows, got %d" % (len(new_parsed) - 1))
    assert "06_REPORT/MANIFEST_SHA256.csv" not in new_man, "self-exclusion violated in output"
    assert set(new_man) == set(PUBLISHED_BASELINE) | NEW_ROWS
    for rel, h in PUBLISHED_BASELINE.items():
        if rel in EXPECTED_CHANGE:
            assert new_man[rel] != h, "expected-change row not changed in output: %s" % rel
        else:
            assert new_man[rel] == h, "unchanged published row altered in output: %s" % rel
    for rel in NEW_ROWS:
        assert new_man[rel] == disk(rel), "new row hash != disk: %s" % rel

    # 8. write
    with open(MAN, "wb") as f:
        f.write(out1)
    print("AMEND_R2 C1 MANIFEST UPDATE OK: 37 data rows (32 published + 5 new); "
          "change set vs published baseline == %s; new-file rows present == %d; "
          "all other published rows byte-identical; self-exclusion held; "
          "every output row == disk." % (sorted(EXPECTED_CHANGE), len(NEW_ROWS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
