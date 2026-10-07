"""Ledger regeneration check (QC): run a copy of build_ledgers.py with PKG redirected to a
temp dir, then compare the 4 CSVs byte-for-byte with the package's on-disk CSVs.
Proves the on-disk ledgers are exactly what the pinned generator emits (no hand edits)."""
import os, subprocess, sys, hashlib, shutil

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006"
QC = PKG + r"\00_CONTROL_INTERNAL_QC"
TMP = r"C:\Users\User\AppData\Local\Temp\opencode\ledger_regen_test"
if os.path.isdir(TMP): shutil.rmtree(TMP)
os.makedirs(TMP)

src = open(PKG + r"\03_SCRIPTS\build_ledgers.py", encoding="utf-8").read()
src2 = src.replace('PKG = r"' + PKG + '"', 'PKG = r"' + TMP + '"')
# also redirect the results json path (it writes to PKG\03_SCRIPTS\ledger_build_results.json via os.path.join)
assert 'os.path.join(PKG, "03_SCRIPTS"' in src2
p = os.path.join(TMP, "build_ledgers_regen.py")
open(p, "w", encoding="utf-8", newline="").write(src2)
os.makedirs(os.path.join(TMP, "03_SCRIPTS"), exist_ok=True)
r = subprocess.run([sys.executable, p], capture_output=True, text=True)
print("generator exit:", r.returncode)
print(r.stdout)

res = {}
for f in ["FUNCTION_BUDGET.csv", "EDGE_LEDGER.csv", "CANDIDATE_LEDGER.csv", "CLAIM_MATRIX.csv"]:
    a = open(os.path.join(PKG, f), "rb").read()
    b = open(os.path.join(TMP, f), "rb").read()
    res[f] = {"identical": a == b, "pkg_sha": hashlib.sha256(a).hexdigest().upper(),
              "regen_sha": hashlib.sha256(b).hexdigest().upper()}
print({k: v["identical"] for k, v in res.items()})
gen_results = open(os.path.join(TMP, "03_SCRIPTS", "ledger_build_results.json"), encoding="utf-8").read()
pkg_results = open(os.path.join(PKG, "03_SCRIPTS", "ledger_build_results.json"), encoding="utf-8").read()
print("ledger_build_results identical:", gen_results == pkg_results)
import json
json.dump({"csv_byte_identity": res, "ledger_build_results_identical": gen_results == pkg_results},
          open(os.path.join(QC, "ledger_regeneration_check.json"), "w"), indent=2)
