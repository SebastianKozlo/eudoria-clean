# qc_j1_independent.py — INDEPENDENT execution of QUALIFICATION_GATE_CORRECTED.py (J1).
# PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007
# Internal QC worker: pe-master-auditor (fresh context, NO_NESTED_TASKS, RECORDS/QC ONLY).
#
# Per contract §9 J1 and the PE-MASTER dispatch: execute the corrected gate against
# M1-M5 recreated INDEPENDENTLY from contract §4 textual mutation definitions and the
# Desktop PRODUCTION_GATE_COUNTEREXAMPLES.json record (input identity). The executor's
# fixture-maker functions (make_m1..make_m5) are NOT copied; my fixtures are my own
# constructions. The gate itself is the object under test: its source is hash-pinned to
# the package manifest value, then exec'd as a module (no __main__, no package writes).
#
# My own adversarial extensions beyond the contract minimum:
#   M5B   — PERFECT synthetic->real relabel (edge-local flags ALSO removed): proves the
#            relabel bypass is closed by POLICY even when the SCHEMA marking check passes.
#   CONNECTED — clean counterpart of M4 (connected declared endpoints) to demonstrate the
#            P_CONNECT clean PASS -> mutated FAIL falsifier pair on this checker.
#   PIN_FALSIFIER — a real chain with ONE mutated expect byte: proves PIN_CHECK actually
#            FAILS on byte mismatch (the executor's own suite never exercised PIN FAIL).
#   SCHEMA_FALSIFIER — duplicate edge ids: proves the schema uniqueness check fires.
#   UNKNOWN_TYPE — unknown edge type: proves KNOWN_EDGE_TYPES enforcement fires.
#   ID_RENAME — chain_id AND edge ids renamed: verdict dicts must be identical (no ID
#            hard-coding anywhere in the verdict logic).
# NO new RE: every EXE byte read is at an ALREADY-PUBLISHED pin VA (source run / Desktop
# counterexamples). No FUN_006C66D0 / FUN_007BF470 decoding. Read-only outside my QC dir.
import hashlib
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
GATE_PATH = os.path.join(PKG, "QUALIFICATION_GATE_CORRECTED.py")
GATE_SHA_EXPECT = "B07B64FF2E3771E6CF728C03BB990C8A815B3ADB1FCCB06DBED0FE3B784F6517"
OUT = os.path.join(HERE, "results_j1_independent.json")

res = {"checks": {}, "cases": {}, "probes": {}}

# ---- 0. hash-pin the gate source exactly as shipped (manifest value) -------------
gs = open(GATE_PATH, "rb").read()
gate_sha = hashlib.sha256(gs).hexdigest().upper()
res["checks"]["gate_source_sha_matches_manifest"] = gate_sha == GATE_SHA_EXPECT

# ---- exec the gate module (namespace exec; __main__ guard prevents main()) --------
ns = {"__name__": "gate_under_test", "__file__": GATE_PATH}
exec(compile(gs, GATE_PATH, "exec"), ns)
res["checks"]["real_science_auto_qualification_is_DISABLED"] = \
    ns["REAL_SCIENCE_AUTO_QUALIFICATION"] == "DISABLED"
res["checks"]["qc_positive_chain_qualification_status"] = \
    ns["QC_POSITIVE_CHAIN_QUALIFICATION"] == "NOT_ESTABLISHED_AS_GENERAL_AUTHORITY"
ev = ns["evaluate_chain"]

# ---- my OWN pinned-EXE reader (independent of the gate's implementation) ---------
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
data = open(EXE, "rb").read()
res["checks"]["exe_identity"] = (
    len(data) == 8015872 and
    hashlib.sha256(data).hexdigest().upper() ==
    "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31")
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
coff = e_lfanew + 4
nsec = struct.unpack_from("<H", data, coff + 2)[0]
sopt = struct.unpack_from("<H", data, coff + 16)[0]
sec0 = coff + 20 + sopt
secs = []
for i in range(nsec):
    off = sec0 + 40 * i
    vsz, va, rsz, ro = struct.unpack_from("<IIII", data, off + 8)
    secs.append((va, max(vsz, rsz), ro))


def my_read(va, n):
    rva = va - 0x400000
    for vs, sz, ro in secs:
        if vs <= rva < vs + sz:
            return data[ro + (rva - vs):ro + (rva - vs) + n]
    raise ValueError("unmapped %x" % va)


def my_hex(va, n):
    return " ".join("%02X" % b for b in my_read(va, n))


# The 5 published real-chain pins (source run / Desktop counterexample record) —
# re-verified from the EXE by MY OWN reader before use:
PINS = [
    ("r1", "sf_creation", 0x006A39ED, 5, "E8 CE 0D E8 FF"),
    ("r2", "sf_store", 0x006A39F6, 3, "89 46 18"),
    ("r3", "parent_identity_access", 0x0050A3E9, 3, "8B 4E 30"),
    ("r4", "parent_receiver", 0x0050A3F7, 2, "FF D2"),
    ("r6", "join_operation", 0x007B5846, 3, "01 5E 04"),
]
pin_ok = all(my_hex(va, n) == exp for _i, _t, va, n, exp in PINS)
res["checks"]["five_published_pins_reverified_own_reader"] = pin_ok
# the two mutated-pin VAs of M2/M3 (real EXE bytes, already published by the Desktop
# counterexample record + source run): re-verified by my own reader:
res["checks"]["m2_store_pin_bytes_own_reader"] = my_hex(0x0050A3AC, 3) == "89 7E 20"
res["checks"]["m3_accessor_pin_bytes_own_reader"] = my_hex(0x008BD720, 4) == "8D 41 18 C3"
# vtable data slots already published (source QC S8 + internal QC):
res["checks"]["slot41_own_reader"] = \
    struct.unpack("<I", my_read(0x00A8CCF4 + 0xA4, 4))[0] == 0x007B5810


def E(eid, etype, **kw):
    d = {"id": eid, "type": etype}
    d.update(kw)
    return d


# ---- MY OWN fixtures (independent construction from contract §4 + Desktop record) -
def my_real_cand4():
    return {
        "chain_id": "MY-REAL-CAND4-INDEPENDENT",
        "is_synthetic": False,
        "edges": [
            E("myr1", "sf_creation", va=0x006A39ED, nbytes=5, expect="E8 CE 0D E8 FF"),
            E("myr2", "sf_store", va=0x006A39F6, nbytes=3, expect="89 46 18"),
            E("myr3", "parent_identity_access", va=0x0050A3E9, nbytes=3,
              expect="8B 4E 30", field="+0x30"),
            E("myr4", "parent_receiver", va=0x0050A3F7, nbytes=2, expect="FF D2",
              receiver="SF30_NODE", child_arg="CHILD_OBJ"),
            E("myr6", "join_operation", va=0x007B5846, nbytes=3, expect="01 5E 04",
              mechanism="children_array_insert_on_parent",
              parent="SF30_NODE", child="CHILD_OBJ"),
        ],
    }


def my_synthetic_clean():
    return {
        "chain_id": "MY-SYNTH-BASELINE",
        "is_synthetic": True,
        "edges": [
            E("b1", "sf_creation", synthetic=True),
            E("b2", "sf_store", synthetic=True),
            E("b3", "parent_identity_access", field="+0x30", synthetic=True),
            E("b4", "parent_receiver", receiver="SF30_NODE", child_arg="CHILD_OBJ",
              synthetic=True),
            E("b5", "child_provenance", op="physically_established_model_resource_op",
              identity_preserved=True, synthetic=True),
            E("b6", "join_operation", mechanism="children_array_insert_on_parent",
              parent="SF30_NODE", child="CHILD_OBJ", synthetic=True),
            E("b7", "visual_role", proof="physical_visual_role_proof", synthetic=True),
        ],
    }


def my_m1():  # contract §4 M1: ONLY textual child provenance + identity=True + visual proof
    c = my_real_cand4()
    c["chain_id"] = "MY-M1-BARE-DECLARATION"
    c["edges"].append(E("myr5", "child_provenance",
                        op="physically_established_model_resource_op",
                        identity_preserved=True))
    c["edges"].append(E("myr7", "visual_role", proof="physical_visual_role_proof"))
    return c


def my_m2():  # parent-identity evidence = correct bytes of the SF+0x20 STORE, decl +0x30
    c = my_m1()
    c["chain_id"] = "MY-M2-STORE-BYTES-DECL-PLUS30"
    for e in c["edges"]:
        if e["type"] == "parent_identity_access":
            e["va"] = 0x0050A3AC
            e["nbytes"] = 3
            e["expect"] = "89 7E 20"
    return c


def my_m3():  # join-operation evidence = 4-byte accessor/RET @0x008BD720
    c = my_m1()
    c["chain_id"] = "MY-M3-ACCESSOR-AS-JOIN"
    for e in c["edges"]:
        if e["type"] == "join_operation":
            e["va"] = 0x008BD720
            e["nbytes"] = 4
            e["expect"] = "8D 41 18 C3"
    return c


def my_m4():  # provenance endpoints explicitly break connectivity
    c = my_m1()
    c["chain_id"] = "MY-M4-DISCONNECTED-PROVENANCE"
    for e in c["edges"]:
        if e["type"] == "child_provenance":
            e["from_object"] = "OTHER_RESOURCE_RESULT"
            e["to_object"] = "OTHER_CHILD_UNRELATED_TO_CALL"
    return c


def my_m5():  # synthetic relabelled ONLY at top level
    c = my_synthetic_clean()
    c["chain_id"] = "MY-M5-TOPLEVEL-RELABEL"
    c["is_synthetic"] = False
    return c


def my_m5b():  # PERFECT relabel: edge-local synthetic flags removed as well
    c = my_synthetic_clean()
    c["chain_id"] = "MY-M5B-PERFECT-RELABEL"
    c["is_synthetic"] = False
    for e in c["edges"]:
        e.pop("synthetic", None)
    return c


def my_connected():  # clean counterpart of M4: endpoints that DO connect
    c = my_m1()
    c["chain_id"] = "MY-CONNECTED-ENDPOINTS"
    for e in c["edges"]:
        if e["type"] == "child_provenance":
            e["from_object"] = "RESOURCE_RESULT"
            e["to_object"] = "CHILD_OBJ"
    return c


def my_ctrl_a():
    c = my_synthetic_clean()
    c["chain_id"] = "MY-CTRL-A"
    for e in c["edges"]:
        if e["type"] == "parent_receiver":
            e["receiver"] = "OTHER_NODE"
    return c


def my_ctrl_b():
    c = my_synthetic_clean()
    c["chain_id"] = "MY-CTRL-B"
    c["edges"] = [e for e in c["edges"] if e["type"] != "child_provenance"]
    return c


def my_ctrl_c():
    c = my_synthetic_clean()
    c["chain_id"] = "MY-CTRL-C"
    for e in c["edges"]:
        if e["type"] == "parent_identity_access":
            e["field"] = "+0x34"
    return c


def my_pin_falsifier():  # real chain, ONE expect byte mutated -> PIN_CHECK must FAIL
    c = my_real_cand4()
    c["chain_id"] = "MY-PIN-FALSIFIER"
    for e in c["edges"]:
        if e["type"] == "parent_identity_access":
            e["expect"] = "8B 4E 31"
    return c


def my_schema_falsifier():  # duplicate edge ids -> SCHEMA must FAIL
    c = my_synthetic_clean()
    c["chain_id"] = "MY-SCHEMA-FALSIFIER"
    c["edges"].append(dict(c["edges"][0]))  # duplicate id b1
    return c


def my_unknown_type():
    c = my_synthetic_clean()
    c["chain_id"] = "MY-UNKNOWN-TYPE"
    c["edges"].append(E("b8", "magic_edge", synthetic=True))
    return c


def run(name, chain):
    r = ev(chain)
    res["cases"][name] = {
        "SCHEMA": r["SCHEMA_CHECK"]["verdict"],
        "PIN": r["PIN_CHECK"]["verdict"],
        "STRUCTURAL": r["STRUCTURAL_CONSISTENCY_CHECK"]["verdict"],
        "MECHANICAL": r["MECHANICAL_VERDICT"],
        "SCIENCE": r["SCIENCE_QUALIFICATION"]["verdict"],
        "structural_failures": r["STRUCTURAL_CONSISTENCY_CHECK"]["failures"],
        "schema_failures": r["SCHEMA_CHECK"]["failures"],
        "predicates_reached": r["STRUCTURAL_CONSISTENCY_CHECK"]["detail"]["predicates_reached"],
    }
    return r


# ---- run all cases on the SAME corrected production gate ---------------------------
syn = run("synthetic_clean_mine", my_synthetic_clean())
ca = run("CTRL_A_mine", my_ctrl_a())
cb = run("CTRL_B_mine", my_ctrl_b())
cc = run("CTRL_C_mine", my_ctrl_c())
rc4 = run("real_CAND4_mine", my_real_cand4())
m1 = run("M1_mine", my_m1())
m2 = run("M2_mine", my_m2())
m3 = run("M3_mine", my_m3())
m4 = run("M4_mine", my_m4())
m5 = run("M5_mine", my_m5())
m5b = run("M5B_perfect_relabel_mine", my_m5b())
conn = run("CONNECTED_mine", my_connected())
pinf = run("PIN_FALSIFIER_mine", my_pin_falsifier())
schemaf = run("SCHEMA_FALSIFIER_mine", my_schema_falsifier())
unk = run("UNKNOWN_TYPE_mine", my_unknown_type())

C = res["cases"]
ck = res["checks"]

# ---- contract §9 J1 expectations --------------------------------------------------
ck["J1a_M1_to_M5_all_NOT_QUALIFIED"] = all(
    C[k]["SCIENCE"] == "NOT_QUALIFIED" for k in
    ("M1_mine", "M2_mine", "M3_mine", "M4_mine", "M5_mine"))
ck["J1b_CTRL_A_B_C_causal_on_corrected_gate"] = (
    C["CTRL_A_mine"]["MECHANICAL"] == "FAIL"
    and any(f.startswith("P_PARENT_FAIL") for f in C["CTRL_A_mine"]["structural_failures"])
    and C["CTRL_B_mine"]["MECHANICAL"] == "FAIL"
    and any(f.startswith("P_CHILD_FAIL") for f in C["CTRL_B_mine"]["structural_failures"])
    and C["CTRL_C_mine"]["MECHANICAL"] == "FAIL"
    and any(f.startswith("P_PARENT_FAIL") for f in C["CTRL_C_mine"]["structural_failures"]))
ck["J1c_synthetic_clean_PASS_machinery_only"] = (
    C["synthetic_clean_mine"]["MECHANICAL"] == "PASS"
    and C["synthetic_clean_mine"]["SCIENCE"] == "SYNTHETIC_MACHINERY_TEST_ONLY")
ck["J1d_real_CAND4_remains_NOT_QUALIFIED"] = (
    C["real_CAND4_mine"]["SCIENCE"] == "NOT_QUALIFIED"
    and C["real_CAND4_mine"]["MECHANICAL"] == "FAIL"
    and C["real_CAND4_mine"]["PIN"] == "PASS")
ck["J1e_no_acceptance_by_bare_declaration"] = (
    C["M1_mine"]["SCIENCE"] == "NOT_QUALIFIED"
    and C["M1_mine"]["MECHANICAL"] == "PASS")
ck["J1f_no_synthetic_to_real_relabel_bypass"] = (
    C["M5_mine"]["SCIENCE"] == "NOT_QUALIFIED"
    and C["M5_mine"]["MECHANICAL"] == "FAIL"
    and C["M5B_perfect_relabel_mine"]["SCIENCE"] == "NOT_QUALIFIED")  # policy backstop
ck["J1g_no_unrelated_byte_pin_bypass"] = (
    C["M2_mine"]["SCIENCE"] == "NOT_QUALIFIED"
    and C["M2_mine"]["PIN"] == "PASS")  # real STORE bytes accepted by byte-equality,
# but the chain still receives NO science qualification (policy)
ck["J1h_no_broken_connectivity_bypass"] = (
    C["M4_mine"]["SCIENCE"] == "NOT_QUALIFIED"
    and C["M4_mine"]["MECHANICAL"] == "FAIL"
    and any(f.startswith("P_CONNECT_FAIL") for f in C["M4_mine"]["structural_failures"]))
ck["J1i_M4_clean_PASS_mutated_FAIL_same_checker"] = (
    C["CONNECTED_mine"]["predicates_reached"]["P_CONNECT"] == "EVALUATED"
    and C["CONNECTED_mine"]["MECHANICAL"] == "PASS"
    and C["M4_mine"]["MECHANICAL"] == "FAIL")
ck["J1j_M5_clean_PASS_mutated_FAIL_same_checker"] = (
    C["synthetic_clean_mine"]["SCHEMA"] == "PASS"
    and C["M5_mine"]["SCHEMA"] == "FAIL")
ck["J1k_no_SCIENCE_PASS_anywhere_in_my_runs"] = all(
    C[k]["SCIENCE"] != "SCIENCE_PASS" for k in C)
ck["J1l_PIN_CHECK_falsifier_fires"] = (
    C["PIN_FALSIFIER_mine"]["PIN"] == "FAIL"
    and C["PIN_FALSIFIER_mine"]["MECHANICAL"] == "FAIL")
ck["J1m_SCHEMA_falsifier_fires"] = (
    C["SCHEMA_FALSIFIER_mine"]["SCHEMA"] == "FAIL")
ck["J1n_unknown_type_rejected"] = C["UNKNOWN_TYPE_mine"]["SCHEMA"] == "FAIL"

# ---- ID-hard-coding probes: rename chain_id AND all edge ids ----------------------
def rename_ids(chain, tag):
    c = json.loads(json.dumps(chain))  # deep copy via json (my own, not copy.deepcopy)
    c["chain_id"] = "RENAMED-" + tag + "-" + c["chain_id"]
    for i, e in enumerate(c["edges"]):
        e["id"] = "zz%d" % i
    return c


for nm, base in (("M1", my_m1()), ("realCAND4", my_real_cand4()),
                 ("synthetic", my_synthetic_clean()), ("M4", my_m4())):
    a = ev(base)
    b = ev(rename_ids(base, nm))
    same = (a["SCHEMA_CHECK"] == b["SCHEMA_CHECK"]
            and a["PIN_CHECK"] == b["PIN_CHECK"]
            and a["STRUCTURAL_CONSISTENCY_CHECK"] == b["STRUCTURAL_CONSISTENCY_CHECK"]
            and a["MECHANICAL_VERDICT"] == b["MECHANICAL_VERDICT"]
            and a["SCIENCE_QUALIFICATION"]["verdict"] == b["SCIENCE_QUALIFICATION"]["verdict"])
    res["probes"]["rename_" + nm] = same
ck["J1o_no_id_hard_coding_renamed_chains_identical"] = all(
    res["probes"].values())

res["OVERALL"] = "PASS" if all(ck.values()) else "FAIL"
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(res, fh, indent=2)
    fh.write("\n")
print("J1 independent gate run: OVERALL=%s" % res["OVERALL"])
for k in sorted(ck):
    print("  %-52s %s" % (k, ck[k]))
