"""make_manifest.py — MANIFEST generation (LAST) for
PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007.

Scope (per the dispatch): the PHYSICAL files of OUTPUT_ROOT minus the manifest
itself. AUDIT_ENTRYPOINT.md is EXPLICITLY OUT of this phase's manifest scope
(excluded pending persistence — noted in the manifest header); the persistence
phase regenerates the manifest over the final physical package together with
the entrypoint row. Any write after this manifest requires regeneration +
re-verification.
"""
import hashlib
import os

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007"
MANIFEST_NAME = "MANIFEST_SHA256.csv"
REL_ROOT = "docs/audits/PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/"

rows = []
for root, dirs, files in os.walk(PKG):
    dirs[:] = [d for d in dirs if d != "__pycache__"]
    for fn in sorted(files):
        full = os.path.join(root, fn)
        if fn == MANIFEST_NAME:
            continue
        rel = REL_ROOT + os.path.relpath(full, PKG).replace("\\", "/")
        data = open(full, "rb").read()
        rows.append((rel, len(data), hashlib.sha256(data).hexdigest()))

rows.sort()
header = [
    "# MANIFEST_SHA256.csv — PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007",
    "# Generated LAST (every package file was already on disk; any write after this manifest requires",
    "# regeneration + re-verification — the every-write-after-the-manifest rule).",
    "# SCOPE: the physical files of docs/audits/PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/ minus",
    "# this manifest itself. AUDIT_ENTRYPOINT.md is EXPLICITLY OUT of this executor phase's manifest",
    "# scope (excluded pending persistence); the persistence phase regenerates the manifest over the",
    "# final physical package together with the entrypoint row.",
    "# BIJECTION SELF-CHECK: rows below == the physical files enumerated now; zero missing/extra/",
    "# duplicate; every size + SHA256 re-read from disk at generation time.",
    "# ROW_COUNT = " + str(len(rows)),
]
with open(os.path.join(PKG, MANIFEST_NAME), "w", encoding="utf-8", newline="\n") as f:
    for ln in header:
        f.write(ln + "\n")
    f.write("path,size_bytes,sha256\n")
    for rel, size, sha in rows:
        f.write(f"{rel},{size},{sha}\n")

# self-check: bijection against a fresh re-enumeration
fresh = set()
for root, dirs, files in os.walk(PKG):
    dirs[:] = [d for d in dirs if d != "__pycache__"]
    for fn in files:
        if fn == MANIFEST_NAME:
            continue
        fresh.add(REL_ROOT + os.path.relpath(os.path.join(root, fn), PKG).replace("\\", "/"))
listed = set(r[0] for r in rows)
assert fresh == listed, f"bijection failure: missing={fresh - listed} extra={listed - fresh}"
assert len(listed) == len(rows), "duplicate rows"
for rel, size, sha in rows:
    p = os.path.join(PKG, rel[len(REL_ROOT):].replace("/", "\\"))
    data = open(p, "rb").read()
    assert len(data) == size and hashlib.sha256(data).hexdigest() == sha, f"hash/size mismatch {rel}"
print(f"MANIFEST generated: {len(rows)} rows; bijection self-check PASS (zero missing/extra/duplicate; all sizes+SHA256 re-verified)")
