# s7_post_correction_bijection.py — post-correction manifest-bijection verification
# For every file row in the (byte-unchanged, historical) starting manifest, recompute
# size+SHA256 and compare. Expected mismatches: EXACTLY the 10 corrected files.
# Also verify: no manifest-covered file is missing; disk-not-in-manifest delta.
import sys, os, json, hashlib
sys.dont_write_bytecode = True

pkg = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
manifest = os.path.join(pkg, "06_REPORT", "MANIFEST_SHA256.csv")

EXPECTED_CHANGED = {
    "02_ANALYSIS/FIELD_TO_DESTINATION_TRACE.md",
    "02_ANALYSIS/CONSUMER_TRACE.md",
    "02_ANALYSIS/SEMANTIC_ASSESSMENT.md",
    "02_ANALYSIS/NEGATIVE_CONTROLS.md",
    "02_ANALYSIS/DESTINATION_CONSUMER_CENSUS.json",
    "02_ANALYSIS/BLAST_RADIUS.md",
    "02_ANALYSIS/VFS_TO_PARSER_TRACE.md",
    "06_REPORT/REPORT.md",
    "06_REPORT/EVIDENCE_INDEX.md",
    "06_REPORT/HANDOFF.md",
}

def parse_csv_line(line):
    fields, sb, inq = [], [], False
    for ch in line:
        if inq:
            if ch == '"':
                inq = False
            else:
                sb.append(ch)
        else:
            if ch == '"':
                inq = True
            elif ch == ',':
                fields.append("".join(sb)); sb = []
            else:
                sb.append(ch)
    fields.append("".join(sb))
    return fields

lines = open(manifest, encoding="utf-8").read().splitlines()
file_rows, note_rows = 0, 0
mismatch, match, missing = [], 0, []
for ln in lines[1:]:
    if not ln.strip():
        continue
    f = parse_csv_line(ln)
    if f[0] == "NOTE":
        note_rows += 1
        continue
    file_rows += 1
    rel = f[0]
    full = os.path.join(pkg, rel.replace("/", "\\"))
    if not os.path.isfile(full):
        missing.append(rel)
        continue
    b = open(full, "rb").read()
    ok = (str(len(b)) == f[1]) and (hashlib.sha256(b).hexdigest().upper() == f[2].upper())
    if ok:
        match += 1
    else:
        mismatch.append(rel)

disk_files = []
for root, dirs, files in os.walk(pkg):
    for fn in files:
        p = os.path.join(root, fn)
        rel = os.path.relpath(p, pkg).replace("\\", "/")
        disk_files.append(rel)
manifest_set = set()
for ln in lines[1:]:
    if ln.strip():
        f = parse_csv_line(ln)
        if f[0] != "NOTE":
            manifest_set.add(f[0])
disk_set = set(disk_files)
not_in_manifest = sorted(disk_set - manifest_set - {"06_REPORT/MANIFEST_SHA256.csv"})
ghosts = sorted(manifest_set - disk_set)

mismatch_set = set(mismatch)
print("MANIFEST FILE ROWS:", file_rows, "| NOTE rows:", note_rows)
print("MATCH (unchanged, byte-identical to the starting manifest):", match)
print("MISMATCH:", len(mismatch), sorted(mismatch_set))
print("MISSING:", missing)
print("EXPECTED_CHANGED == MISMATCH:", mismatch_set == EXPECTED_CHANGED)
print("DISK_NOT_IN_MANIFEST (new files + the manifest itself):", len(not_in_manifest))
for x in not_in_manifest:
    print("   +", x)
print("GHOSTS (manifest rows without disk files):", ghosts)
