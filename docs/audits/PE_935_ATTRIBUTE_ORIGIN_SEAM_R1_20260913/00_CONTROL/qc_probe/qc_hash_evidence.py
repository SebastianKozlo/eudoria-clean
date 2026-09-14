"""qc_hash_evidence.py — hash ALL executor evidence files BEFORE and AFTER QC.
Independent census: every file under the package except 00_CONTROL/GHIDRA_LOCAL internals
(covered by their own SHA manifests) and __pycache__ (bytecode cache, not evidence).
Mode: before|after  -> writes QC_HASH_{mode}.json
"""
import hashlib
import json
import os
import sys

PKG = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
EXCLUDE_PARTS = {os.path.normcase(os.path.join("00_Control", "GHIDRA_Local")), os.path.normcase("__pycache__")}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def census(root):
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        if any(part in os.path.normcase(rel) for part in EXCLUDE_PARTS):
            dirnames[:] = []
            continue
        if rel == "00_CONTROL" and os.path.normcase("qc_probe") in [os.path.normcase(d) for d in dirnames]:
            pass  # qc_probe = auditor's own tools; include them for transparency but tagged below
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            relpath = os.path.relpath(full, root)
            try:
                out[relpath] = {"sha256": sha256_file(full), "size": os.path.getsize(full)}
            except OSError as e:
                out[relpath] = {"error": str(e)}
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "before"
    files = census(PKG)
    # separate auditor's own qc_probe files (created during QC) from executor evidence
    own = {k: v for k, v in files.items() if os.path.normcase("qc_probe") in os.path.normcase(k)}
    evidence = {k: v for k, v in files.items() if os.path.normcase("qc_probe") not in os.path.normcase(k)}
    doc = {
        "mode": mode,
        "package_root": PKG,
        "evidence_file_count": len(evidence),
        "evidence": evidence,
        "auditor_own_files": own,
    }
    outp = os.path.join(PKG, "00_CONTROL", "qc_probe", "QC_HASH_%s.json" % mode)
    with open(outp, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=1, sort_keys=True)
    print("mode=%s evidence_files=%d -> %s" % (mode, len(evidence), outp))


if __name__ == "__main__":
    main()
