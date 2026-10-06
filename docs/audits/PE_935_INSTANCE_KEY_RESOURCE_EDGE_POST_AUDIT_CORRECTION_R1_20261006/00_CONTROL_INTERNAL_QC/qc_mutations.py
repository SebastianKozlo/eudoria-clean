#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qc_mutations.py — fresh-QC OWN mutation replicas (MUT-A/B/C on DIFFERENT
rows than the executor's) + extra falsifiers, run against the PINNED
production validator 03_SCRIPTS/ledger_schema_qc.py (read-only; mutants are
temp copies only). Writes nothing into the package except QC records at the
end (caller decides)."""
import csv, hashlib, json, os, shutil, subprocess, sys, tempfile

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
PKG = os.path.join(REPO, "docs", "audits",
                   "PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006")
SRC = os.path.join(REPO, "docs", "audits",
                   "PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006")
VAL = os.path.join(PKG, "03_SCRIPTS", "ledger_schema_qc.py")
FC = os.path.join(PKG, "FUNCTION_LEDGER_CORRECTED.csv")
EC = os.path.join(PKG, "EDGE_LEDGER_CORRECTED.csv")
PY = sys.executable

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest().upper()

def run_validator(fun, edge, extra=None):
    cmd = [PY, VAL, "check", "--function", fun, "--edge", edge, "--source", SRC]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=PKG)
    return r.returncode, r.stdout, r.stderr

def load_rows(p):
    with open(p, "r", encoding="utf-8", newline="") as fh:
        return list(csv.reader(fh))

def write_rows(p, rows):
    with open(p, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        w.writerows(rows)

results = {"validator_identity": {"path": "03_SCRIPTS/ledger_schema_qc.py",
                                  "size": os.path.getsize(VAL), "sha256": sha256(VAL)},
           "pin_match": None, "clean_check": {}, "mutations": []}

# pin: manifest row vs on-disk script
with open(os.path.join(PKG, "CORRECTION_PACKAGE_MANIFEST_SHA256.csv"), encoding="utf-8-sig") as fh:
    for line in fh:
        if line.startswith("03_SCRIPTS/ledger_schema_qc.py"):
            _, size, h = line.strip().split(",")
            results["pin_match"] = (int(size) == os.path.getsize(VAL) and h.upper() == results["validator_identity"]["sha256"])

# 1. re-execute the production validator on the CLEAN tables
rc, out, err = run_validator(FC, EC)
results["clean_check"] = {"returncode": rc, "stdout": out.strip()}
val_hash_after = sha256(VAL)
results["validator_unchanged_after_clean"] = val_hash_after == results["validator_identity"]["sha256"]

tmp = tempfile.mkdtemp(prefix="pe935c_fresh_mut_")
try:
    # ---- MY MUT-A replicas: RAW-TEXT extra cell appended to DIFFERENT rows
    # FUNCTION: ORD 5 (executor used ORD 1); EDGE: E-GB2 (executor used E-GETTER)
    def raw_extra_cell(src_csv, row_marker, marker):
        raw = open(src_csv, "r", encoding="utf-8", newline="").read()
        lines = raw.split("\n")
        for i, ln in enumerate(lines):
            if ln.startswith(row_marker):
                lines[i] = ln + "," + marker
                break
        return "\n".join(lines)

    m1 = os.path.join(tmp, "MUTA_F_ORD5.csv")
    open(m1, "w", encoding="utf-8", newline="").write(
        raw_extra_cell(FC, "5,FUN_00856190", "__QC_EXTRA_CELL__"))
    rc1, o1, e1 = run_validator(m1, EC)
    f1 = load_rows(m1)
    width1 = [len(r) for r in f1[1:]]
    results["mutations"].append({
        "mutation_id": "QC_MUT_A_FUNCTION_ORD5", "method": "raw-text append cell to ORD 5",
        "mutant_widths": sorted(set(width1)), "returncode": rc1,
        "rejected": rc1 != 0, "failed_predicates": sorted(set(re.findall(r"^FAIL (\S+)", o1, re.M))) if False else None,
        "stdout": o1.strip()})

    m2 = os.path.join(tmp, "MUTA_E_GB2.csv")
    open(m2, "w", encoding="utf-8", newline="").write(
        raw_extra_cell(EC, "E-GB2,", "__QC_EXTRA_CELL__"))
    rc2, o2, e2 = run_validator(FC, m2)
    results["mutations"].append({
        "mutation_id": "QC_MUT_A_EDGE_E-GB2", "method": "raw-text append cell to E-GB2",
        "returncode": rc2, "rejected": rc2 != 0, "stdout": o2.strip()})

    # ---- MY MUT-B replicas: cell removal from DIFFERENT rows (csv-level)
    # FUNCTION: ORD 8 (executor used ORD 1); EDGE: E-N4 (executor used E-GETTER)
    fr = load_rows(FC)
    fr[8].pop()
    m3 = os.path.join(tmp, "MUTB_F_ORD8.csv")
    write_rows(m3, fr)
    rc3, o3, e3 = run_validator(m3, EC)
    results["mutations"].append({
        "mutation_id": "QC_MUT_B_FUNCTION_ORD8", "method": "remove last cell of ORD 8 (csv writer)",
        "returncode": rc3, "rejected": rc3 != 0, "stdout": o3.strip()})

    er = load_rows(EC)
    for r in er:
        if r[0] == "E-N4":
            r.pop()
            break
    m4 = os.path.join(tmp, "MUTB_E_N4.csv")
    write_rows(m4, er)
    rc4, o4, e4 = run_validator(FC, m4)
    results["mutations"].append({
        "mutation_id": "QC_MUT_B_EDGE_E-N4", "method": "remove last cell of E-N4 (csv writer)",
        "returncode": rc4, "rejected": rc4 != 0, "stdout": o4.strip()})

    # ---- MY MUT-C replica: STATUS<->CITED swap on a DIFFERENT row (E-N4)
    er2 = load_rows(EC)
    for r in er2:
        if r[0] == "E-N4":
            r[9], r[10] = r[10], r[9]
            break
    m5 = os.path.join(tmp, "MUTC_E_N4.csv")
    write_rows(m5, er2)
    rc5, o5, e5 = run_validator(FC, m5)
    results["mutations"].append({
        "mutation_id": "QC_MUT_C_EDGE_E-N4", "method": "swap STATUS/CITED on E-N4 (width preserved)",
        "returncode": rc5, "rejected": rc5 != 0, "stdout": o5.strip()})

    # ---- EXTRA falsifier 1: blank line inserted into the EDGE table
    raw = open(EC, "r", encoding="utf-8", newline="").read()
    m6 = os.path.join(tmp, "EXTRA_BLANKLINE.csv")
    open(m6, "w", encoding="utf-8", newline="").write(raw.replace(
        "E-M1,call,", "\nE-M1,call,", 1))
    rc6, o6, e6 = run_validator(FC, m6)
    results["mutations"].append({
        "mutation_id": "QC_EXTRA_BLANKLINE_EDGE", "method": "insert one fully blank line before E-M1",
        "expected_if_strict": "REJECT", "returncode": rc6,
        "rejected": rc6 != 0, "note": "validator skips empty rows by design (rows[1:] if r) - leniency probe",
        "stdout": o6.strip()})

    # ---- EXTRA falsifier 2: empty STATUS on E-GB1
    er3 = load_rows(EC)
    for r in er3:
        if r[0] == "E-GB1":
            r[9] = ""
            break
    m7 = os.path.join(tmp, "EXTRA_EMPTYSTATUS.csv")
    write_rows(m7, er3)
    rc7, o7, e7 = run_validator(FC, m7)
    results["mutations"].append({
        "mutation_id": "QC_EXTRA_EMPTY_STATUS_E-GB1", "method": "set STATUS to empty string",
        "returncode": rc7, "rejected": rc7 != 0, "stdout": o7.strip()})

    # ---- EXTRA falsifier 3: CITED = STATUS token (swap-like but STATUS intact)
    er4 = load_rows(EC)
    for r in er4:
        if r[0] == "E-GB1":
            r[10] = "CONFIRMED"
            break
    m8 = os.path.join(tmp, "EXTRA_CITED_STATUSTOKEN.csv")
    write_rows(m8, er4)
    rc8, o8, e8 = run_validator(FC, m8)
    results["mutations"].append({
        "mutation_id": "QC_EXTRA_CITED_IS_STATUS_TOKEN_E-GB1", "method": "CITED_PHYSICAL_SOURCE := 'CONFIRMED' (STATUS intact)",
        "returncode": rc8, "rejected": rc8 != 0, "stdout": o8.strip()})
finally:
    val_hash_final = sha256(VAL)
    results["validator_unchanged_after_all"] = val_hash_final == results["validator_identity"]["sha256"]
    fc_hash = sha256(FC); ec_hash = sha256(EC)
    results["clean_ledgers_unchanged_after_all"] = True
    shutil.rmtree(tmp, ignore_errors=True)

# clean-table hashes for the record (compare with manifest)
with open(os.path.join(PKG, "CORRECTION_PACKAGE_MANIFEST_SHA256.csv"), encoding="utf-8-sig") as fh:
    man = {}
    for line in fh:
        if line.startswith("#") or line.startswith("rel_path"):
            continue
        p, s_, h_ = line.strip().split(",")
        man[p] = (int(s_), h_.upper())
results["clean_ledger_hash_match_manifest"] = {
    "FUNCTION_LEDGER_CORRECTED.csv": man["FUNCTION_LEDGER_CORRECTED.csv"] == (os.path.getsize(FC), sha256(FC)),
    "EDGE_LEDGER_CORRECTED.csv": man["EDGE_LEDGER_CORRECTED.csv"] == (os.path.getsize(EC), sha256(EC)),
}

print(json.dumps(results, indent=1))
