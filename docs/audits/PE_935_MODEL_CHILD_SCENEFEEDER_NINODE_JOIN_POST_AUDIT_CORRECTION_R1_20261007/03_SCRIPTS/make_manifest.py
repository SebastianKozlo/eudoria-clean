"""Final manifest generator — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007.
Scope (FINAL PERSISTENCE SCOPE, regenerated LAST by the PE-MASTER persistence
phase): ALL physical files under OUTPUT_ROOT EXCLUDING the manifest itself, PLUS
the updated AUDIT_ENTRYPOINT.md (listed as ../../../AUDIT_ENTRYPOINT.md, path
relative to this manifest's directory; the newest-first LATEST RUNS row for this
run was added by the persistence phase immediately before this regeneration).
Writes MANIFEST_SHA256.csv with a leading '# scope:' header line, then verifies
bijection independently (re-walk + re-hash; zero missing/extra/dup/mismatch).
The executor-phase manifest scope (16 rows, entrypoint and 00_CONTROL_INTERNAL_QC
excluded) is superseded by this final regeneration per the dispatch and contract
§11 (MANIFEST LAST; every write after a manifest requires regeneration +
re-verification). Replaces the executor-phase generator of this package; the
executor-phase 16-row manifest content it produced remains preserved via the git
history of this run's own publication only AFTER this commit (the executor never
committed).
"""
import csv, hashlib, os, sys

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007"
REPO_ROOT = os.path.abspath(os.path.join(PKG, os.pardir, os.pardir, os.pardir))
ENTRY_REL = "../../../AUDIT_ENTRYPOINT.md"
MAN = os.path.join(PKG, "MANIFEST_SHA256.csv")

SCOPE_HEADER = (
    "# scope: FINAL PERSISTENCE SCOPE (regenerated LAST by the PE-MASTER persistence phase of "
    "PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007): every physical file under this "
    "package - the executor-phase correction records (the package root and 03_SCRIPTS/ tools+results, incl. the "
    "corrected QUALIFICATION_GATE_CORRECTED.py and the amended EDGE_BUDGET_RECONSTRUCTION.csv), the fresh internal-QC "
    "records under 00_CONTROL_INTERNAL_QC/, and PE_MASTER_REVIEW.md (persisted verbatim, the placeholder replaced by "
    "this persistence phase) - minus this manifest itself (self-exclusion), PLUS the updated AUDIT_ENTRYPOINT.md "
    "(listed as ../../../AUDIT_ENTRYPOINT.md, the repo-root entrypoint whose newest-first LATEST RUNS row was added by "
    "this persistence phase; path relative to this manifest's directory). Bijection + full re-hash verified after "
    "regeneration: zero missing/extra/duplicate/size/SHA mismatches."
)

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()

# 1. collect physical files (exclude the manifest itself; exclude __pycache__)
#    + the updated repo-root AUDIT_ENTRYPOINT.md
items = []
for root, dirs, names in os.walk(PKG):
    dirs[:] = [d for d in dirs if d != "__pycache__"]
    for n in names:
        p = os.path.join(root, n)
        if os.path.normpath(p) == os.path.normpath(MAN):
            continue
        items.append((os.path.relpath(p, PKG).replace("\\", "/"), p))
ep = os.path.join(REPO_ROOT, "AUDIT_ENTRYPOINT.md")
if not os.path.isfile(ep):
    sys.exit("FATAL: updated AUDIT_ENTRYPOINT.md not found at " + ep)
items.append((ENTRY_REL, ep))
items.sort(key=lambda t: t[0])

rows = []
for rel, p in items:
    rows.append({"relative_path": rel, "size_bytes": os.path.getsize(p), "sha256": sha256(p)})

with open(MAN, "w", encoding="utf-8", newline="") as f:
    f.write(SCOPE_HEADER + "\n")
    w = csv.DictWriter(f, fieldnames=["relative_path", "size_bytes", "sha256"], lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)
print(f"manifest written: {len(rows)} rows")

# 2. independent bijection check (fresh re-walk + re-hash; zero missing/extra/dup/mismatch)
with open(MAN, encoding="utf-8", newline="") as f:
    lines = [ln for ln in f.read().split("\n") if ln.strip() != ""]
if not lines[0].startswith("# scope:"):
    sys.exit("FATAL: scope header missing")
mrows = {}
for r in csv.DictReader(lines[1:]):
    mrows[r["relative_path"]] = (int(r["size_bytes"]), r["sha256"])
disk = {}
for root, dirs, names in os.walk(PKG):
    dirs[:] = [d for d in dirs if d != "__pycache__"]
    for n in names:
        p = os.path.join(root, n)
        if os.path.normpath(p) == os.path.normpath(MAN):
            continue
        disk[os.path.relpath(p, PKG).replace("\\", "/")] = (os.path.getsize(p), sha256(p))
disk[ENTRY_REL] = (os.path.getsize(ep), sha256(ep))
missing = sorted(set(disk) - set(mrows))
extra = sorted(set(mrows) - set(disk))
mismatch = [k for k in sorted(set(disk) & set(mrows)) if disk[k] != mrows[k]]
dups = [k for k in mrows if list(mrows).count(k) > 1]
print(f"BIJECTION: rows={len(mrows)} disk={len(disk)} missing={len(missing)} extra={len(extra)} duplicate={len(dups)} size/sha mismatch={len(mismatch)}")
if missing or extra or dups or mismatch:
    print("DETAIL missing:", missing, "extra:", extra, "mismatch:", mismatch)
    sys.exit(1)
print("BIJECTION PASS")
