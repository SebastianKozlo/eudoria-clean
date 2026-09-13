#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913 - Z5a: artifact manifest generator.

Zapis: 06_REPORT\artifact_index.csv (relative_path,size_bytes,sha256).
Zasady: bez self-row (precedens L12); payload policy: asercja, ze pakiet nie zawiera plikow
        oryginalow (.nif/.bvi/.bnt/.exe/.vfs/ark/dll) ani plikow binarnych > 2 MB (safety-net;
        caly pakiet to tekstowe metadane/wyniki/skrypty).
"""

import csv
import hashlib
import os
import sys

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913"
SELF_REL = r"06_REPORT\artifact_index.csv"
FORBIDDEN_EXT = {".nif", ".bvi", ".bnt", ".exe", ".vfs", ".ark", ".dll", ".dmp", ".rep"}
MAX_SIZE = 2 * 1024 * 1024

ERRORS = []


def die(msg):
    ERRORS.append(msg)
    sys.stderr.write("[FAIL] " + msg + "\n")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    rows = []
    for dirpath, _dirnames, filenames in os.walk(RUN_ROOT):
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, RUN_ROOT)
            if rel == SELF_REL:
                continue
            ext = os.path.splitext(fn)[1].lower()
            size = os.path.getsize(full)
            if ext in FORBIDDEN_EXT:
                die("payload policy violation: %s" % rel)
            if size > MAX_SIZE:
                die("file exceeds 2MB safety-net: %s (%d B)" % (rel, size))
            rows.append((rel, size, sha256_file(full)))

    rows.sort()
    out_path = os.path.join(RUN_ROOT, "06_REPORT", "artifact_index.csv")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f)
        w.writerow(["relative_path", "size_bytes", "sha256"])
        for rel, size, sha in rows:
            w.writerow([rel, size, sha])

    if ERRORS:
        sys.exit(1)
    print("manifest rows: %d (self excluded)" % len(rows))
    for rel, size, sha in rows:
        print("%s|%d|%s" % (rel, size, sha))
    print("[Z5A] MANIFEST DONE")


if __name__ == "__main__":
    main()
