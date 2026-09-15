# w6_manifest.py — PE_935_SF_ARG2_PROVENANCE_R1_20260914 (00_CONTROL)
# W6 (part 2): SCRIPT_SHA256.csv + MANIFEST_SHA256.csv (family convention: every
# package file, SHA256, no self-row, zero missing, zero duplicate paths).
# Run AFTER all other package files exist. Deterministic (sorted paths).

import hashlib
import os
import sys

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_ARG2_PROVENANCE_R1_20260914"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def rel_list(root, skip_dirs=None):
    skip_dirs = skip_dirs or set()
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        for d in list(dirnames):
            if d in skip_dirs:
                dirnames.remove(d)
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace("\\", "/")
            out.append((rel, full))
    return sorted(out)


def main():
    files = rel_list(PKG)
    seen = set()
    dups = []
    for rel, _ in files:
        if rel in seen:
            dups.append(rel)
        seen.add(rel)
    missing = [rel for rel, full in files if not os.path.exists(full)]

    # MANIFEST_SHA256.csv — every package file EXCEPT itself (no self-row)
    manifest_path = os.path.join(PKG, "06_REPORT", "MANIFEST_SHA256.csv")
    with open(manifest_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("path,sha256\n")
        for rel, full in files:
            if rel == "06_REPORT/MANIFEST_SHA256.csv":
                continue
            f.write(f"{rel},{sha256_file(full)}\n")

    # SCRIPT_SHA256.csv — every 00_CONTROL script, except the CSVs themselves
    scripts = [(rel, full) for rel, full in files
               if rel.startswith("00_CONTROL/") and rel.endswith(".py")]
    script_csv = os.path.join(PKG, "00_CONTROL", "SCRIPT_SHA256.csv")
    with open(script_csv, "w", encoding="utf-8", newline="\n") as f:
        f.write("path,sha256\n")
        for rel, full in sorted(scripts):
            f.write(f"{rel},{sha256_file(full)}\n")

    # recompute manifest AFTER writing SCRIPT_SHA256.csv so it includes it
    files2 = rel_list(PKG)
    with open(manifest_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("path,sha256\n")
        for rel, full in files2:
            if rel == "06_REPORT/MANIFEST_SHA256.csv":
                continue
            f.write(f"{rel},{sha256_file(full)}\n")

    total = len(files2) - 1  # minus the manifest self-row
    print(f"MANIFEST rows: {total}; duplicate paths: {len(dups)}; missing: {len(missing)}")
    if dups:
        print("DUPLICATE PATHS:", dups)
    if missing:
        print("MISSING:", missing)


if __name__ == "__main__":
    main()
