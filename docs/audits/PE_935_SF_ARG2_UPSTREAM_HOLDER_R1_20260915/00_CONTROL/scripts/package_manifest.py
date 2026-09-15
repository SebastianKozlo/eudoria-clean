"""
package_manifest.py - final packaging: script hashes + package manifest.
- Cleans __pycache__/.pyc from the package (contract 12).
- Writes 00_CONTROL/SCRIPT_SHA256.csv (all scripts + hashes).
- Writes 06_REPORT/MANIFEST_SHA256.csv for every package file EXCEPT the
  manifest itself (L12 self-exclusion rule) and EXCEPT 06_REPORT/QC_AUDIT.md
  (the fresh-context QC session's own record; per contract 13 the QC file
  is a post-manifest addition the executor must not hash or touch - R2 note,
  QC_AUDIT.md was added by the G13 QC session AFTER the R1 manifest).
Re-measures size+SHA256+PE layout FIRST (fail-closed).
"""
import sys
import os
import hashlib
import capstone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import s0_common as S

RUN_DIR = os.path.dirname(os.path.dirname(HERE))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    m, s0 = S.require_identity()
    gen_sha = S.script_self_sha256(os.path.abspath(__file__))
    # clean pyc artifacts
    removed = []
    for root, dirs, files in os.walk(RUN_DIR):
        for d in list(dirs):
            if d == "__pycache__":
                p = os.path.join(root, d)
                for fn in os.listdir(p):
                    os.remove(os.path.join(p, fn))
                os.rmdir(p)
                removed.append(p)
        for fn in files:
            if fn.endswith(".pyc"):
                os.remove(os.path.join(root, fn))
                removed.append(os.path.join(root, fn))
    # script hashes
    scripts_dir = os.path.join(RUN_DIR, "00_CONTROL", "scripts")
    lines = ["SCRIPT,SHA256,BYTES"]
    for fn in sorted(os.listdir(scripts_dir)):
        if fn.endswith(".py"):
            p = os.path.join(scripts_dir, fn)
            lines.append("%s,%s,%d" % (fn, sha256_file(p), os.path.getsize(p)))
    with open(os.path.join(RUN_DIR, "00_CONTROL", "SCRIPT_SHA256.csv"), "w") as f:
        f.write(chr(10).join(lines) + chr(10))
    # package manifest (self-excluding; QC_AUDIT.md excluded - QC's own record)
    man_path = os.path.join(RUN_DIR, "06_REPORT", "MANIFEST_SHA256.csv")
    mlines = ["FILE,SHA256,BYTES"]
    n = 0
    for root, dirs, files in os.walk(RUN_DIR):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for fn in sorted(files):
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, RUN_DIR).replace("\\", "/")
            if rel == "06_REPORT/MANIFEST_SHA256.csv":
                continue  # L12 self-exclusion
            if rel == "06_REPORT/QC_AUDIT.md":
                continue  # QC session's own record (post-manifest QC addition)
            if fn.endswith(".pyc"):
                continue
            mlines.append("%s,%s,%d" % (rel, sha256_file(p), os.path.getsize(p)))
            n += 1
    with open(man_path, "w") as f:
        f.write(chr(10).join(mlines) + chr(10))
    print("S0 PASS (identity re-measured): %s" % s0)
    print("GENERATOR: package_manifest.py (SHA256=%s)" % gen_sha)
    print("pyc artifacts removed: %d" % len(removed))
    print("scripts hashed: %d" % (len(lines) - 1))
    print("manifest rows: %d (self-excluded + QC_AUDIT.md excluded)" % n)


if __name__ == "__main__":
    main()
