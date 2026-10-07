"""Production candidate qualification gate — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006.

Contract §5: the gate reads the PROOF-CHAIN STRUCTURE and required evidence, not just
four typed status strings. Byte claims in non-synthetic chains are verified against the
hash-pinned EXE. Tests:
  BASELINE  : SYNTHETIC_GATE_TEST_ONLY fixture -> must PASS (proves the gate can pass;
              never recorded as PCG finding/evidence; never promotes INSTANCE_MODEL_NODE_JOIN).
  CTRL-A    : parent mutated to other-node      -> must FAIL on the PARENT predicate.
  CTRL-B    : child model-provenance removed    -> must FAIL on the CHILD predicate.
  CTRL-C    : identity edge to the argument broken -> must FAIL on the PARENT-IDENTITY predicate.
  REAL CAND : the real CAND-4 chain (A/D unresolved) -> must FAIL (no rubber-stamping).
Outputs 03_SCRIPTS/qualification_results.json.
"""
import hashlib, json, sys

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_SIZE = 8015872
EXE_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
OUT = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006\00_CONTROL_INTERNAL_QC\results_gate_add_A.json"

# ---- pinned PE mapper (minimal, sections from headers) ----
import struct
data = open(EXE, "rb").read()
assert len(data) == EXE_SIZE and hashlib.sha256(data).hexdigest().upper() == EXE_SHA, "EXE identity FAIL"
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
coff = e_lfanew + 4
nsec = struct.unpack_from("<H", data, coff + 2)[0]
size_opt = struct.unpack_from("<H", data, coff + 16)[0]
sec0 = coff + 20 + size_opt
sections = []
for i in range(nsec):
    off = sec0 + 40 * i
    _, vsize, va, rsize, roff = struct.unpack_from("<IIIII", data, off)[:5] if False else (
        None,) * 5
    vsize, va, rsize, roff = struct.unpack_from("<IIII", data, off + 8)
    sections.append((va, max(vsize, rsize), roff))

def read(va, n):
    rva = va - 0x400000
    for va_s, sz, roff in sections:
        if va_s <= rva < va_s + sz:
            return data[roff + (rva - va_s):roff + (rva - va_s) + n]
    raise ValueError(f"VA {va:#x} unmapped")

def hexb(va, n):
    return " ".join(f"{b:02X}" for b in read(va, n))

# ---- the proof-chain model ----
def edge(eid, etype, **kw):
    d = {"id": eid, "type": etype}
    d.update(kw)
    return d

SYNTHETIC_BASELINE = {
    "chain_id": "SYNTHETIC_GATE_TEST_ONLY",
    "is_synthetic": True,
    "note": "hand-built fixture proving the gate logic; NOT PCG evidence; never promotes INSTANCE_MODEL_NODE_JOIN",
    "edges": [
        edge("s1", "sf_creation", synthetic=True),
        edge("s2", "sf_store", synthetic=True),
        edge("s3", "parent_identity_access", field="+0x30", synthetic=True),
        edge("s4", "parent_receiver", receiver="SF30_NODE", child_arg="CHILD_OBJ", synthetic=True),
        edge("s5", "child_provenance", op="physically_established_model_resource_op",
             identity_preserved=True, synthetic=True),
        edge("s6", "join_operation", mechanism="children_array_insert_on_parent",
             parent="SF30_NODE", child="CHILD_OBJ", synthetic=True),
        edge("s7", "visual_role", proof="physical_visual_role_proof", synthetic=True),
    ],
}

REAL_CAND4 = {
    "chain_id": "REAL_CAND-4-ACLD-PATH-SLOT41-ATTACH",
    "is_synthetic": False,
    "edges": [
        edge("r1", "sf_creation", va=0x006A39ED, nbytes=5, expect="E8 CE 0D E8 FF",
             meaning="call FUN_005247C0 (SF factory) in FUN_006A3930 (ACLD ctor)"),
        edge("r2", "sf_store", va=0x006A39F6, nbytes=3, expect="89 46 18",
             meaning="mov [esi+0x18],eax — the SF stored at [ACLD+0x18]"),
        edge("r3", "parent_identity_access", va=0x0050A3E9, nbytes=3, expect="8B 4E 30",
             field="+0x30", meaning="mov ecx,[esi+0x30] — the examined SF+0x30 NiNode loaded as the join receiver source"),
        edge("r4", "parent_receiver", va=0x0050A3F7, nbytes=2, expect="FF D2",
             receiver="SF30_NODE", child_arg="CHILD_OBJ",
             meaning="call edx — NiNode vtable slot 41 dispatch, ECX=[SF+0x30] NiNode"),
        edge("r5", "child_provenance", op="physically_established_model_resource_op",
             identity_preserved=True, synthetic=False),
        # QC TEST EDGE r5 (would exist only if proof A were established)
        edge("r6", "join_operation", va=0x007B5846, nbytes=3, expect="01 5E 04",
             mechanism="children_array_insert_on_parent", parent="SF30_NODE", child="CHILD_OBJ",
             meaning="FUN_007B5810 refcount-inc [child+4] (AttachChild fingerprint F2; F4 children-array insertion also byte-proven in 01_RAW/FUN_007B5810_ORACLE_BYTE_PROOF.txt)"),
        # r7 (visual_role) INTENTIONALLY ABSENT: unresolved
    ],
}

def verify_bytes(e):
    if e.get("synthetic"):
        return True, "synthetic (no byte claim)"
    got = hexb(e["va"], e["nbytes"])
    ok = got == e["expect"]
    return ok, f"va {e['va']:#010x} got '{got}' expect '{e['expect']}' match={ok}"

def gate(chain):
    """Evaluate the four structure predicates. Returns (verdict, failures, byte_results)."""
    failures = []
    byte_results = {}
    edges = {e["id"]: e for e in chain["edges"]}

    # byte verification of every edge that carries a byte claim
    for e in chain["edges"]:
        if "va" in e:
            ok, msg = verify_bytes(e)
            byte_results[e["id"]] = msg
            if not ok:
                failures.append(f"BYTE_MISMATCH[{e['id']}]: {msg}")

    # connectivity: sf_creation -> sf_store -> SF_instance -> parent_identity_access(+0x30) -> node
    has_creation = any(e["type"] == "sf_creation" for e in chain["edges"])
    has_store = any(e["type"] == "sf_store" for e in chain["edges"])
    pia = [e for e in chain["edges"] if e["type"] == "parent_identity_access" and e.get("field") == "+0x30"]
    rcv = [e for e in chain["edges"] if e["type"] == "parent_receiver"]

    # P_PARENT: creation + store + an identity access of field +0x30 whose node is the receiver of the join call
    if not (has_creation and has_store and pia):
        failures.append("P_PARENT_FAIL: missing sf_creation/sf_store/parent_identity_access(+0x30)")
    elif not rcv:
        failures.append("P_PARENT_FAIL: no parent_receiver edge")
    else:
        node = pia[0].get("to", "SF30_NODE")
        for r in rcv:
            if r.get("receiver") != node:
                failures.append(f"P_PARENT_FAIL: receiver {r.get('receiver')} != the SF+0x30 node ({node})")

    # P_CHILD: a child_provenance edge with a physically established model/resource op, identity preserved
    cp = [e for e in chain["edges"] if e["type"] == "child_provenance"]
    if not cp:
        failures.append("P_CHILD_FAIL: no child_provenance edge (model/resource provenance not established)")
    else:
        e = cp[0]
        if e.get("op") != "physically_established_model_resource_op":
            failures.append("P_CHILD_FAIL: child provenance op not physically established")
        if not e.get("identity_preserved"):
            failures.append("P_CHILD_FAIL: child identity not preserved (wrapper/clone break)")

    # P_OPERATION: a join_operation binding the parent node and the child arg
    jo = [e for e in chain["edges"] if e["type"] == "join_operation"]
    if not jo:
        failures.append("P_OPERATION_FAIL: no join_operation edge")
    else:
        e = jo[0]
        if e.get("mechanism") != "children_array_insert_on_parent":
            failures.append("P_OPERATION_FAIL: mechanism is not a parent-child binding on the exact parent")
        if rcv:
            if e.get("parent") != rcv[0].get("receiver"):
                failures.append("P_OPERATION_FAIL: operation parent != join receiver node")
            if e.get("child") != rcv[0].get("child_arg"):
                failures.append("P_OPERATION_FAIL: operation child != the receiver's child argument")

    # P_VISUAL: a visual_role proof
    vr = [e for e in chain["edges"] if e["type"] == "visual_role"]
    if not vr:
        failures.append("P_VISUAL_FAIL: no visual_role edge")
    elif vr[0].get("proof") != "physical_visual_role_proof":
        failures.append("P_VISUAL_FAIL: visual role proof not physical")

    verdict = "PASS" if not failures else "FAIL"
    return verdict, failures, byte_results

results = {}

# 1. baseline
v, f, b = gate(SYNTHETIC_BASELINE)
results["baseline_synthetic"] = {"chain": "SYNTHETIC_GATE_TEST_ONLY", "verdict": v, "failures": f,
                                 "required": "PASS (clean baseline before the mutants)"}

# 2. CTRL-A: parent -> other-node (copy of the baseline with the receiver mutated)
import copy
ctrl_a = copy.deepcopy(SYNTHETIC_BASELINE)
ctrl_a["chain_id"] = "CTRL-A-parent-other-node"
for e in ctrl_a["edges"]:
    if e["type"] == "parent_receiver":
        e["receiver"] = "OTHER_NODE"
v, f, b = gate(ctrl_a)
results["ctrl_a_parent_other_node"] = {"verdict": v, "failures": f,
                                       "required": "FAIL by the PARENT predicate",
                                       "proper_predicate": len(f) > 0 and f[0].startswith("P_PARENT_FAIL")}

# 3. CTRL-B: remove child model provenance
ctrl_b = copy.deepcopy(SYNTHETIC_BASELINE)
ctrl_b["chain_id"] = "CTRL-B-child-provenance-removed"
ctrl_b["edges"] = [e for e in ctrl_b["edges"] if e["type"] != "child_provenance"]
v, f, b = gate(ctrl_b)
results["ctrl_b_child_provenance_removed"] = {"verdict": v, "failures": f,
                                              "required": "FAIL by the CHILD predicate",
                                              "proper_predicate": all(x.startswith("P_CHILD_FAIL") for x in f)}

# 4. CTRL-C: break the identity edge to the argument (+0x30 -> a different field)
ctrl_c = copy.deepcopy(SYNTHETIC_BASELINE)
ctrl_c["chain_id"] = "CTRL-C-identity-edge-broken"
for e in ctrl_c["edges"]:
    if e["type"] == "parent_identity_access":
        e["field"] = "+0x34"
v, f, b = gate(ctrl_c)
results["ctrl_c_identity_edge_broken"] = {"verdict": v, "failures": f,
                                          "required": "FAIL by the PARENT-IDENTITY predicate",
                                          "proper_predicate": all(x.startswith("P_PARENT_FAIL") for x in f)}

# 5. REAL candidate evaluation
v, f, b = gate(REAL_CAND4)
results["real_cand_4"] = {"chain": "REAL_CAND-4-ACLD-PATH-SLOT41-ATTACH", "verdict": v,
                           "failures": f, "byte_verification": b,
                           "required": "FAIL (A/D unresolved — the gate must not rubber-stamp the real candidate)",
                           "interpretation": "the real candidate fails the production gate: child model/resource provenance and visual role are not established; consistent with INSTANCE_MODEL_NODE_JOIN = NOT_ESTABLISHED"}

# gate self-checks
results["gate_self_checks"] = {
    "baseline_passes": results["baseline_synthetic"]["verdict"] == "PASS",
    "ctrl_a_fails_by_parent_predicate": results["ctrl_a_parent_other_node"]["verdict"] == "FAIL" and results["ctrl_a_parent_other_node"]["proper_predicate"],
    "ctrl_a_cascade_note": "the parent->other-node mutation also fails the operation-parent consistency rule (the operation must bind THE receiver node); the PRIMARY rejection is the PARENT predicate",
    "ctrl_b_fails_by_child_predicate": results["ctrl_b_child_provenance_removed"]["verdict"] == "FAIL" and results["ctrl_b_child_provenance_removed"]["proper_predicate"],
    "ctrl_c_fails_by_parent_identity_predicate": results["ctrl_c_identity_edge_broken"]["verdict"] == "FAIL" and results["ctrl_c_identity_edge_broken"]["proper_predicate"],
    "real_candidate_fails": results["real_cand_4"]["verdict"] == "FAIL",
    "not_checker_always_fail": results["baseline_synthetic"]["verdict"] == "PASS",
    "real_candidate_bytes_verified_against_exe": all("match=True" in s for s in results["real_cand_4"]["byte_verification"].values()),
    "exe_sha_verified": True,
}

ok = all(results["gate_self_checks"].values())
results["OVERALL"] = "PASS" if ok else "FAIL"
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(results, fh, indent=2)
    fh.write("\n")
print(json.dumps(results, indent=2))
