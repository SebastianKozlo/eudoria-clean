"""Independent gate tests (QC falsifiers) — PE_935_MODEL_CHILD_SF_JOIN internal QC.

Tests (my own, on COPIES of the executor's gate script with ONLY the OUT path and the
declared mutation changed; the package's own qualification_results.json is never touched):
  T1 GATE_REPLAY   : byte-identical copy, OUT redirected -> must reproduce identical results
                     (repeatability; independence comes from my own re-pins, not from this).
  T2 BYTE_FALSIFIER: r3 expect mutated 8B 4E 30 -> 8B 4E 31 -> the REAL chain must FAIL with
                     BYTE_MISMATCH[r3] (proves the byte predicate is load-bearing, not decorative).
  T3 ADD_A         : REAL chain + a well-formed child_provenance edge -> P_CHILD failure must
                     DISAPPEAR while P_VISUAL remains (proves P_CHILD discriminates on structure).
  T4 ADD_A_D       : REAL chain + child_provenance + visual_role -> the chain shape PASSES with
                     all 5 real byte claims intact (proves the PASS barrier for the real chain was
                     exactly A and D; no other predicate blocks it).
Outputs in 00_CONTROL_INTERNAL_QC/: results_gate_replay.json, results_gate_falsifier_byte.json,
results_gate_add_A.json, results_gate_add_AD.json, gate_tests_summary.json
"""
import hashlib, json, os, subprocess, sys

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006"
QC = PKG + r"\00_CONTROL_INTERNAL_QC"
GATE = PKG + r"\03_SCRIPTS\qualification_gate.py"
ORIG_RESULTS = PKG + r"\03_SCRIPTS\qualification_results.json"

src = open(GATE, encoding="utf-8").read()
gate_sha = hashlib.sha256(src.encode()).hexdigest().upper()

def variant(name, replacements):
    v = src
    for old, new in replacements:
        assert old in v, f"pattern not found for {name}: {old[:60]}"
        v = v.replace(old, new)
    p = os.path.join(QC, f"gate_{name}.py")
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(v)
    return p

summary = {"gate_source": GATE, "gate_sha256": gate_sha, "tests": {}}

# T1: replay with OUT redirected only
p1 = variant("replay", [('OUT = r"' + PKG + r'\03_SCRIPTS\qualification_results.json"',
                        'OUT = r"' + QC + r'\results_gate_replay.json"')])
r = subprocess.run([sys.executable, p1], capture_output=True, text=True)
replay = json.load(open(os.path.join(QC, "results_gate_replay.json")))
orig = json.load(open(ORIG_RESULTS))
same = replay == orig
summary["tests"]["T1_gate_replay"] = {
    "exit": r.returncode, "results_identical_to_package": same,
    "overall": replay.get("OVERALL"),
    "real_cand_4_verdict": replay.get("real_cand_4", {}).get("verdict"),
}

# T2: byte falsifier (mutate the r3 expected bytes)
p2 = variant("falsifier_byte", [
    ('OUT = r"' + PKG + r'\03_SCRIPTS\qualification_results.json"',
     'OUT = r"' + QC + r'\results_gate_falsifier_byte.json"'),
    ('expect="8B 4E 30"', 'expect="8B 4E 31"'),
])
r = subprocess.run([sys.executable, p2], capture_output=True, text=True)
fals = json.load(open(os.path.join(QC, "results_gate_falsifier_byte.json")))
real_f = fals.get("real_cand_4", {})
byte_mismatch_fired = any("BYTE_MISMATCH[r3]" in f for f in real_f.get("failures", []))
summary["tests"]["T2_byte_falsifier"] = {
    "exit": r.returncode, "real_cand_4_verdict": real_f.get("verdict"),
    "byte_mismatch_r3_fired": byte_mismatch_fired,
    "failures": real_f.get("failures"),
}

# T3: add a well-formed child_provenance edge (r5) to the REAL chain
p3 = variant("add_A", [
    ('OUT = r"' + PKG + r'\03_SCRIPTS\qualification_results.json"',
     'OUT = r"' + QC + r'\results_gate_add_A.json"'),
    ('        # r5 (child_provenance) INTENTIONALLY ABSENT: unresolved within budget (FUN_006C66D0 undecoded)',
     '        edge("r5", "child_provenance", op="physically_established_model_resource_op",\n'
     '             identity_preserved=True, synthetic=False),\n'
     '        # QC TEST EDGE r5 (would exist only if proof A were established)'),
])
r = subprocess.run([sys.executable, p3], capture_output=True, text=True)
addA = json.load(open(os.path.join(QC, "results_gate_add_A.json")))
real_a = addA.get("real_cand_4", {})
pchild_gone = not any(f.startswith("P_CHILD_FAIL") for f in real_a.get("failures", []))
pvisual_kept = any(f.startswith("P_VISUAL_FAIL") for f in real_a.get("failures", []))
summary["tests"]["T3_add_child_provenance"] = {
    "exit": r.returncode, "real_cand_4_verdict": real_a.get("verdict"),
    "P_CHILD_failure_disappeared": pchild_gone, "P_VISUAL_failure_remains": pvisual_kept,
    "failures": real_a.get("failures"),
}

# T4: add child_provenance + visual_role -> the real chain shape should PASS
p4 = variant("add_AD", [
    ('OUT = r"' + PKG + r'\03_SCRIPTS\qualification_results.json"',
     'OUT = r"' + QC + r'\results_gate_add_AD.json"'),
    ('        # r5 (child_provenance) INTENTIONALLY ABSENT: unresolved within budget (FUN_006C66D0 undecoded)',
     '        edge("r5", "child_provenance", op="physically_established_model_resource_op",\n'
     '             identity_preserved=True, synthetic=False),\n'
     '        # QC TEST EDGE r5 (would exist only if proof A were established)'),
    ('        # r7 (visual_role) INTENTIONALLY ABSENT: unresolved',
     '        edge("r7", "visual_role", proof="physical_visual_role_proof", synthetic=False),\n'
     '        # QC TEST EDGE r7 (would exist only if proof D were established)'),
])
r = subprocess.run([sys.executable, p4], capture_output=True, text=True)
addAD = json.load(open(os.path.join(QC, "results_gate_add_AD.json")))
real_ad = addAD.get("real_cand_4", {})
all_bytes_ok = all("match=True" in s for s in real_ad.get("byte_verification", {}).values())
summary["tests"]["T4_add_A_and_D"] = {
    "exit": r.returncode, "real_cand_4_verdict": real_ad.get("verdict"),
    "all_5_real_byte_claims_verified": all_bytes_ok,
    "interpretation": "the REAL chain shape (r1/r2/r3/r4/r6 byte-proven) PASSES the production gate "
                     "exactly when A and D edges are added — the actual barriers were A and D, "
                     "and no hidden predicate blocks the real chain (QC probe of gate logic; "
                     "NOT a science claim — r5/r7 here are QC TEST EDGES, the science status of "
                     "A/D remains UNRESOLVED)",
}

ok_all = (summary["tests"]["T1_gate_replay"]["results_identical_to_package"]
          and summary["tests"]["T2_byte_falsifier"]["byte_mismatch_r3_fired"]
          and summary["tests"]["T3_add_child_provenance"]["P_CHILD_failure_disappeared"]
          and summary["tests"]["T3_add_child_provenance"]["P_VISUAL_failure_remains"]
          and summary["tests"]["T4_add_A_and_D"]["real_cand_4_verdict"] == "PASS")
summary["OVERALL"] = "PASS" if ok_all else "FAIL"
with open(os.path.join(QC, "gate_tests_summary.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(summary, f, indent=2)
    f.write("\n")
print(json.dumps(summary, indent=2))
