# -*- coding: utf-8 -*-
# g7_census.py - G7-IMMUTABLE census (composite + per-file SHA) for the
# historical packages + originals. Run BEFORE and AFTER (phase argument).
# STATIC-ONLY. Nothing outside the run directory is modified by this tool.

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

TARGETS = [
    r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe",
    (r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters"
     r"\templates.vfs"),
    r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ORIGIN_SEAM_DESKTOP_AUDIT_R1_20260913",
    r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913",
    r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913",
    r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_PLACEMENT_ROUND1_20260913",
    r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_PLACEMENT_DESKTOP_AUDIT_R1_20260913",
    r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913",
    r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
    r"D:\Eudoria_Reconstruction\99_Audits\PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913",
]


def sha_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def census():
    data = {}
    composite = hashlib.sha256()
    for t in TARGETS:
        if os.path.isfile(t):
            s = sha_of(t)
            data[t] = {"type": "file", "sha256": s,
                       "size": os.path.getsize(t)}
            composite.update(s.encode())
        elif os.path.isdir(t):
            files = {}
            for dp, dns, fns in os.walk(t):
                dns[:] = sorted(dns)
                for fn in sorted(fns):
                    p = os.path.join(dp, fn)
                    if os.path.isfile(p):
                        rel = os.path.relpath(p, t)
                        s = sha_of(p)
                        files[rel] = {"sha256": s,
                                      "size": os.path.getsize(p)}
                        composite.update((rel + "|" + s).encode())
            data[t] = {"type": "dir", "files": files,
                       "count": len(files)}
        else:
            data[t] = {"type": "missing"}
    return {"composite": composite.hexdigest().upper(), "targets": data}


if __name__ == "__main__":
    phase = sys.argv[1] if len(sys.argv) > 1 else "before"
    out = os.path.join(HERE, "..", "01_RAW",
                       "G7_CENSUS_%s.json" % phase)
    c = census()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(c, f, indent=1, sort_keys=True)
    for t, v in c["targets"].items():
        if v["type"] == "dir":
            print("%s: %d files" % (t, v["count"]))
        elif v["type"] == "file":
            print("%s: %s (%d B)" % (t, v["sha256"][:16], v["size"]))
        else:
            print("%s: MISSING" % t)
    print("composite: %s" % c["composite"])
    print("DONE -> 01_RAW/G7_CENSUS_%s.json" % phase)
