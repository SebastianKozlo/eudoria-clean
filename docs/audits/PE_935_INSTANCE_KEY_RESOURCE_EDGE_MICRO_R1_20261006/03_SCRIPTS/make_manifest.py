# make_manifest.py - manifest generator for
# PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006 (generated LAST).
# Standalone: imports NOTHING from this package (so it creates no __pycache__).
# Scope per the contract s6 = every physical file under this package MINUS the
# manifest itself MINUS the AUDIT_ENTRYPOINT.md row -- per the human dispatch
# the entrypoint file was NOT edited in this phase and the persistence phase
# will REGENERATE the manifest including it (recorded in the manifest header).
# After writing, the script re-verifies the bijection IN-PROCESS: re-enumerates
# the tree, re-hashes every row, and exits non-zero on ANY missing/extra/
# duplicate/size/SHA mismatch.

import hashlib
import os
import sys

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_NAME = "COMMITTED_PACKAGE_MANIFEST_SHA256.csv"
MANIFEST_PATH = os.path.join(PKG, MANIFEST_NAME)
SCOPE_NOTE = ("# scope: every physical file under this package minus the manifest "
              "itself; AUDIT_ENTRYPOINT.md NOT edited in this phase (per the human "
              "dispatch the persistence phase adds the row and REGENERATES this "
              "manifest including it)")


def enumerate_files():
    files = []
    for root, dirs, names in os.walk(PKG):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for n in names:
            p = os.path.join(root, n)
            if os.path.abspath(p) == os.path.abspath(MANIFEST_PATH):
                continue
            files.append(os.path.relpath(p, PKG).replace("\\", "/"))
    return sorted(files)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


if len(sys.argv) > 1 and sys.argv[1] == "--count-only":
    n = len(enumerate_files())
    print("PACKAGE_FILES_MINUS_MANIFEST=%d" % n)
    print("PHYSICAL_TOTAL_INCLUDING_MANIFEST=%d" % (n + 1))
    sys.exit(0)

rows = []
for rel in enumerate_files():
    p = os.path.join(PKG, rel)
    size = os.path.getsize(p)
    sha = sha256_of(p)
    rows.append((rel.replace("\\", "/"), size, sha))

with open(MANIFEST_PATH, "w", newline="\n") as f:
    f.write(SCOPE_NOTE + "\n")
    f.write("REL_PATH,SIZE_BYTES,SHA256\n")
    for rel, size, sha in rows:
        f.write("%s,%d,%s\n" % (rel, size, sha))

# ---- IN-PROCESS BIJECTION + FULL RE-HASH VERIFICATION ----
errors = []
seen = set()
for rel, size, sha in rows:
    if rel in seen:
        errors.append("DUPLICATE row: %s" % rel)
    seen.add(rel)
    p = os.path.join(PKG, rel.replace("/", "\\"))
    if not os.path.isfile(p):
        errors.append("MISSING file for row: %s" % rel)
        continue
    if os.path.getsize(p) != size:
        errors.append("SIZE mismatch: %s" % rel)
    if sha256_of(p) != sha:
        errors.append("SHA mismatch: %s" % rel)
current = set(enumerate_files())
listed = set(r[0] for r in rows)
for extra in sorted(current - listed):
    errors.append("EXTRA file on disk not in manifest: %s" % extra)
for missing in sorted(listed - current):
    errors.append("ROW without file: %s" % missing)

print("MANIFEST_ROWS=%d" % len(rows))
print("PHYSICAL_PACKAGE_FILE_COUNT=%d" % (len(current) + 1))
print("BIJECTION_ERRORS=%d" % len(errors))
for e in errors:
    print("  ERROR: %s" % e)
if errors:
    print("MANIFEST_VERIFICATION=FAIL")
    sys.exit(2)
print("MANIFEST_VERIFICATION=PASS (zero missing/extra/duplicate/size/SHA mismatches)")
