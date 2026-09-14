# -*- coding: utf-8 -*-
# PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914 (persistence STEP 1g) - deterministic
# fail-closed MANIFEST_SHA256.csv builder for the cleanup package.
#
# Canonical run: D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe -B cleanup_r1_manifest.py
# (run with -B: no bytecode; no __pycache__ may exist anywhere in the package - asserted).
#
# Semantics (project conventions; self-exclusion per L12 - the same precedent as the
# LINK30 package manifest):
#   - enumerates EVERY file under the package root (dynamic census);
#   - asserts the census == the embedded EXPECTED set (33 paths) plus, if already
#     generated, the manifest itself - fail-closed on ANY surprise file;
#   - asserts no __pycache__ directory and no .pyc file anywhere in the package;
#   - hashes every covered file with SHA256; writes 06_REPORT/MANIFEST_SHA256.csv with
#     columns relative_path,size,sha256 (header included), rows sorted by path,
#     csv QUOTE_MINIMAL, CRLF line endings, UTF-8;
#   - SELF-EXCLUSION (L12): the manifest is NEVER a row - it cannot contain its own
#     hash; its own on-disk SHA256 is reported in the delivery notice instead;
#   - deterministic: the manifest content is built twice and compared before writing;
#   - re-runnable: a re-run rebuilds the identical manifest from disk (idempotent).

import csv
import hashlib
import io
import os
import sys

PKG = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
       r"\PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914")
MAN_REL = "06_REPORT/MANIFEST_SHA256.csv"
MAN_PATH = os.path.join(PKG, "06_REPORT", "MANIFEST_SHA256.csv")

EXPECTED = {
    # 00_CONTROL (7 executor/formalizer files + this script + the completion log)
    "00_CONTROL/RUN_CONTRACT.md",
    "00_CONTROL/SOURCE_IDENTITIES.json",
    "00_CONTROL/GIT_OBSERVATIONS_AT_FORMALIZE.md",
    "00_CONTROL/cleanup_verify_identities.py",
    "00_CONTROL/ebp_alias_classifier.py",
    "00_CONTROL/e_ebp_reval.py",
    "00_CONTROL/nirtti_bounded_probe.py",
    "00_CONTROL/cleanup_r1_manifest.py",
    "00_CONTROL/PERSISTENCE_COMPLETION_LOG.md",
    # 01_RAW (10)
    "01_RAW/E1_CALLER_PROVENANCE_CENSUS.txt",
    "01_RAW/E1_FUN_007EAC00_DISASM.txt",
    "01_RAW/E2_CALLER_PROVENANCE_CENSUS.txt",
    "01_RAW/E2_FUN_0082DAC0_DISASM.txt",
    "01_RAW/EBP_CLASSIFIER_TEST_OUTPUTS.txt",
    "01_RAW/ENTROPIA_PE_OPTIONAL_HEADER_DUMP.txt",
    "01_RAW/GIT_OBSERVATIONS_AT_CLEANUP_START.md",
    "01_RAW/IDENTITY_VERIFICATION_AT_END.txt",
    "01_RAW/IDENTITY_VERIFICATION_AT_START.txt",
    "01_RAW/NIRTTI_BOUNDED_PROBE_0xBA7270.txt",
    # 02_ANALYSIS (6 executor + the STEP-1a EBP_REVALIDATION.md)
    "02_ANALYSIS/CANONICAL_STATE_RECONCILIATION.md",
    "02_ANALYSIS/EBP_CLASSIFIER_RULE_V2.md",
    "02_ANALYSIS/EBP_REVALIDATION.md",
    "02_ANALYSIS/F5_DISPOSITION.md",
    "02_ANALYSIS/SCIENCE_STATUS_MATRIX.csv",
    "02_ANALYSIS/SLOT17_AUDIT_FINDINGS_DISPOSITION.md",
    "02_ANALYSIS/SLOT17_ERRATA.md",
    # 03_EVIDENCE (2)
    "03_EVIDENCE/EVIDENCE_INDEX.csv",
    "03_EVIDENCE/README.md",
    # 06_REPORT (4 + the STEP-1f PE_MASTER_REVIEW.md; manifest self-excluded per L12)
    "06_REPORT/HANDOFF.md",
    "06_REPORT/QC_AUDIT.md",
    "06_REPORT/PE_MASTER_REVIEW.md",
    "06_REPORT/REPORT.md",
    "06_REPORT/STAGE_ACCEPTANCE_GATES.csv",
}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def enumerate_disk():
    found = set()
    for root, dirs, files in os.walk(PKG):
        for d in dirs:
            assert d != "__pycache__", "forbidden __pycache__ directory: %s" % os.path.join(root, d)
        for name in files:
            assert not name.endswith(".pyc"), "forbidden bytecode file: %s" % os.path.join(root, name)
            full = os.path.join(root, name)
            rel = os.path.relpath(full, PKG).replace("\\", "/")
            found.add(rel)
    return found


def build():
    buf = io.StringIO()
    w = csv.writer(buf)  # default lineterminator \r\n; QUOTE_MINIMAL
    w.writerow(["relative_path", "size", "sha256"])
    for rel in sorted(EXPECTED):
        full = os.path.join(PKG, *rel.split("/"))
        size = os.path.getsize(full)
        assert size > 0, "unexpected zero-size package file: %s" % rel
        w.writerow([rel, size, sha256_file(full)])
    return buf.getvalue().encode("utf-8")


def main():
    found = enumerate_disk()
    allowed = set(EXPECTED)
    if os.path.exists(MAN_PATH):
        allowed.add(MAN_REL)
    assert found == allowed, (
        "package census mismatch; unexpected=%s missing=%s"
        % (sorted(found - allowed), sorted(allowed - found)))
    assert len(EXPECTED) == 33, "expected row count drifted: %d" % len(EXPECTED)
    assert MAN_REL not in EXPECTED, "manifest self-listed (L12 violated)"

    out1 = build()
    out2 = build()
    assert out1 == out2, "determinism self-check failed"
    assert out1.endswith(b"\r\n"), "unexpected manifest line-ending format"

    with open(MAN_PATH, "wb") as f:
        f.write(out1)

    # post-write re-read verification: the on-disk manifest parses and matches the build
    raw = open(MAN_PATH, "rb").read()
    assert raw == out1, "on-disk manifest != built manifest"
    parsed = list(csv.reader(io.StringIO(raw.decode("utf-8"))))
    assert parsed[0] == ["relative_path", "size", "sha256"], "bad header"
    rows = [r for r in parsed[1:] if r]
    assert len(rows) == 33, "expected 33 data rows, got %d" % len(rows)
    assert MAN_REL not in {r[0] for r in rows}, "self-exclusion violated in output"
    print("CLEANUP_R1 MANIFEST OK: 33 data rows (every package file; the manifest "
          "self-excluded per L12); census fail-closed; deterministic (build-twice equal); "
          "CRLF/UTF-8; row set == EXPECTED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
