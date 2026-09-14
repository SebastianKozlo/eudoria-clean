# -*- coding: utf-8 -*-
# GB6-manifest: SHA256 census of GHIDRA_LOCAL copy (AT_COPY phase).
# Each manifest describes EXACTLY the state it covers. AT_COPY = state right
# after robocopy from PKG_A (expected db.67/db.68 checkpoints, 10 files).
import hashlib
import os
import sys

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
GH = os.path.join(RUN_ROOT, "00_CONTROL", "GHIDRA_LOCAL")

def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else "at_copy"
    rows = []
    for dirpath, dirnames, filenames in os.walk(GH):
        for fn in sorted(filenames):
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, GH).replace("\\", "/")
            h = hashlib.sha256()
            with open(p, "rb") as f:
                for blk in iter(lambda: f.read(1 << 20), b""):
                    h.update(blk)
            rows.append((h.hexdigest().upper(), rel, os.path.getsize(p)))
    rows.sort(key=lambda r: r[1])
    out = os.path.join(RUN_ROOT, "00_CONTROL", "GHIDRA_LOCAL_MANIFEST_%s.csv" % phase)
    with open(out, "w") as f:
        f.write("sha256\trelpath\tsize\n")
        for hh, rel, sz in rows:
            f.write("%s\t%s\t%d\n" % (hh, rel, sz))
    print("GHIDRA_LOCAL manifest (%s): %d files" % (phase, len(rows)))
    for hh, rel, sz in rows:
        print("  %s\t%s" % (hh[:16], rel))

if __name__ == "__main__":
    main()
