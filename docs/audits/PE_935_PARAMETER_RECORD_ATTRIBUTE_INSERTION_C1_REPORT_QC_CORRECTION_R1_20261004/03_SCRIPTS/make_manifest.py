# make_manifest.py
# Generates COMMITTED_PACKAGE_MANIFEST_SHA256.csv LAST (self-excluded).
# Scope = the files committed by THIS correction run minus the manifest itself:
#   - every file of this package (except the manifest),
#   - the 8 narrowly corrected R1 docs,
#   - AUDIT_ENTRYPOINT.md (one new row).
# Header: relative_path,size_bytes,sha256 (repo-root-relative, forward slashes).
import os, hashlib

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
RUN = "docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004"
R1 = "docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004"
MANIFEST = os.path.join(RUN, "COMMITTED_PACKAGE_MANIFEST_SHA256.csv")

COMMITTED = [
    RUN + "/FINAL_REPORT.md",
    RUN + "/HANDOFF.md",
    RUN + "/INPUT_IDENTITIES.md",
    RUN + "/QC_TARGETED_REPORT.md",
    RUN + "/SUPERSESSION_LEDGER.md",
    RUN + "/CORRECTED_DOC_DELTAS.md",
    RUN + "/01_RAW/QC_TARGETED.json",
    RUN + "/01_RAW/QC_MUTATION_AB_SWAP.json",
    RUN + "/01_RAW/EXE_BYTE_PROOFS.json",
    RUN + "/03_SCRIPTS/qc_targeted.py",
    RUN + "/03_SCRIPTS/make_manifest.py",
    R1 + "/FINAL_REPORT.md",
    R1 + "/HANDOFF.md",
    R1 + "/PARSER_CHAIN.md",
    R1 + "/RECORD_A.md",
    R1 + "/RECORD_B.md",
    R1 + "/QC_REPORT.md",
    R1 + "/RECEIVER_INSERTION_CHAIN.md",
    R1 + "/PLACEMENT_CONSUMER_EDGE.md",
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
