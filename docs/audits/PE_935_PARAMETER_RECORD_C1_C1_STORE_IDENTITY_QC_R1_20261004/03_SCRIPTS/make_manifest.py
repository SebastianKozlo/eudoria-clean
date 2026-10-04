# make_manifest.py
# Generates COMMITTED_PACKAGE_MANIFEST_SHA256.csv LAST (self-excluded).
# Scope = the files committed by THIS run minus the manifest itself:
#   - every file of this package (except the manifest),
#   - AUDIT_ENTRYPOINT.md (one new LATEST RUNS row).
# NO historical package file was modified or is in scope (BASE 97bdf95
# preserved byte-identical; `git status` confirmed no tracked-file changes).
# Header: relative_path,size_bytes,sha256 (repo-root-relative, forward slashes).
import os, hashlib

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
RUN = "docs/audits/PE_935_PARAMETER_RECORD_C1_C1_STORE_IDENTITY_QC_R1_20261004"
MANIFEST = os.path.join(RUN, "COMMITTED_PACKAGE_MANIFEST_SHA256.csv")

COMMITTED = [
    RUN + "/FINAL_REPORT.md",
    RUN + "/HANDOFF.md",
    RUN + "/INPUT_IDENTITIES.md",
    RUN + "/QC_TARGETED_REPORT.md",
    RUN + "/SUPERSESSION_LEDGER.md",
    RUN + "/01_RAW/BASE_MUTANT_C_REPRODUCTION.json",
    RUN + "/01_RAW/QC_TARGETED.json",
    RUN + "/01_RAW/QC_MUTATION_BATTERY_POST_FIX.json",
    RUN + "/01_RAW/ORACLE_EVIDENCE.json",
    RUN + "/03_SCRIPTS/qc_targeted_c1c1.py",
    RUN + "/03_SCRIPTS/make_manifest.py",
    "AUDIT_ENTRYPOINT.md",
]

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()

def main():
    rows = []
    for rel in COMMITTED:
        p = os.path.join(REPO, *rel.split("/"))
        assert os.path.isfile(p), "missing committed file: " + rel
        rows.append((rel, os.path.getsize(p), sha256_file(p)))
    out = os.path.join(REPO, *MANIFEST.split("/"))
    with open(out, "w", newline="") as f:
        f.write("relative_path,size_bytes,sha256\r\n")
        for rel, size, sha in rows:
            f.write("%s,%d,%s\r\n" % (rel, size, sha))
    print("manifest rows:", len(rows), "->", MANIFEST)
    for rel, size, sha in rows:
        print(" ", rel, size, sha[:16] + "...")

if __name__ == "__main__":
    main()
