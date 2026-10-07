"""QUALIFICATION_GATE_CORRECTED — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007.

Correction of Desktop post-audit finding J1/P2 (PE_935_MODEL_CHILD_SF_JOIN_DESKTOP_POST_AUDIT_064B7F4_20261007):
the ORIGINAL production gate (SOURCE_RUN_PACKAGE 03_SCRIPTS/qualification_gate.py at BASE 064b7f4,
SHA256 EF2D8E1F01D63BD004CC8F4087BDBC8194F51EACC38579DC0B2AC2FCDCC400AD — READ-ONLY, unchanged, not executed
for any qualification here) accepted DECLARATIONS without physical evidence: adding only textual
child_provenance/identity=True/visual proof strings made a real chain PASS.

Corrected machinery policy (contract §4):
  REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED
  - This tool NEVER issues a positive SCIENCE qualification for a real (non-synthetic) chain.
  - It returns SEPARATELY: SCHEMA_CHECK, PIN_CHECK, STRUCTURAL_CONSISTENCY_CHECK — each PASS/FAIL/NOT_CHECKED
    strictly per the checks actually performed. NONE of these PASSes is a SCIENCE_PASS.
  - A synthetic fixture may PASS only as a SYNTHETIC MACHINERY TEST (never PCG evidence, never promotion).
  - A real candidate MUST NOT receive automatic SCIENCE_PASS from declarative fields (status strings,
    boolean identity_preserved, literal texts like 'physically_established_model_resource_op' /
    'physical_visual_role_proof', matching bytes at an unrelated VA, top-level is_synthetic=False).
  - Where the tool cannot independently bind every required semantic assertion to physical evidence records
    and exact endpoints, the science verdict is NOT_QUALIFIED with MANUAL_PHYSICAL_EVIDENCE_REQUIRED.
  - The real CAND-4 chain MUST remain NOT QUALIFIED (A and D unresolved).
  - NO general semantic verifier for the EXE is built here: PIN_CHECK verifies BYTE EQUALITY at declared VAs
    only; it does NOT decode instructions and does NOT bind bytes to the claimed semantic meaning.

Mechanical predicates actually implemented (declared-fields only, ID-agnostic — no candidate/mutation IDs
anywhere in the rejection logic):
  SCHEMA:   required keys, known edge types, unique edge ids, synthetic-marking consistency
            (a real chain may not contain edge-local synthetic=True edges, and a synthetic chain must mark
            every edge synthetic=True) — catches the M5 relabel.
  PIN:      byte equality of every edge carrying va/nbytes/expect against the hash-pinned EXE;
            NOT_CHECKED when a chain carries zero byte claims.
  STRUCTURAL: P_PARENT (creation+store+identity_access(+0x30)+receiver==node),
            P_CHILD (provenance edge with the declared op + identity flag),
            P_CONNECT (declared provenance endpoints must connect to the join child argument),
            P_OPERATION (mechanism + parent/child binding to the receiver edge),
            P_VISUAL (declared proof string presence) — catches CTRL-A/B/C and the M4 broken connectivity.

HONEST REJECTION-MECHANISM DISCLOSURE (contract §4): with real-science auto-qualification disabled BY POLICY,
M1/M2/M3 are NOT QUALIFIED through that policy — the mechanical checks do NOT detect their specific defects
(M2's byte pin is a REAL STORE at the pinned VA; M3's byte pin is a REAL accessor/RET at the pinned VA;
PIN_CHECK verifies presence, not semantics). The counterexample run therefore establishes THE ABSENCE OF
AUTOMATIC SCIENCE PROMOTION, not validator detection of a specific wrong opcode/endpoint. M4 and M5 are
additionally rejected by mechanical predicates (connectivity / synthetic-marking consistency). The
declared-mechanical-predicate pairs each show clean PASS -> mutated FAIL on THIS same checker.

Outputs: 03_SCRIPTS/gate_corrected_results.json (full machine results)
         GATE_COUNTEREXAMPLES.json (per-counterexample record, package root)
"""
import copy
import hashlib
import json
import struct
import sys

# ---------------------------------------------------------------- policy header
REAL_SCIENCE_AUTO_QUALIFICATION = "DISABLED"
QC_POSITIVE_CHAIN_QUALIFICATION = "NOT_ESTABLISHED_AS_GENERAL_AUTHORITY"

# ------------------------------------------------------------- pinned EXE (QC)
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_SIZE = 8015872
EXE_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

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


# ------------------------------------------------------------- the chain model
KNOWN_EDGE_TYPES = {"sf_creation", "sf_store", "parent_identity_access", "parent_receiver",
                    "child_provenance", "join_operation", "visual_role"}
DEFAULT_PARENT_NODE = "SF30_NODE"


def edge(eid, etype, **kw):
    d = {"id": eid, "type": etype}
    d.update(kw)
    return d


# The REAL CAND-4 chain as published by the audited source run (its 5 byte pins are the
# source run's already-published claims; re-verified here by PIN_CHECK).
REAL_CAND4 = {
    "chain_id": "REAL_CAND-4-ACLD-PATH-SLOT41-ATTACH",
    "is_synthetic": False,
    "edges": [
        edge("r1", "sf_creation", va=0x006A39ED, nbytes=5, expect="E8 CE 0D E8 FF"),
        edge("r2", "sf_store", va=0x006A39F6, nbytes=3, expect="89 46 18"),
        edge("r3", "parent_identity_access", va=0x0050A3E9, nbytes=3, expect="8B 4E 30",
             field="+0x30"),
        edge("r4", "parent_receiver", va=0x0050A3F7, nbytes=2, expect="FF D2",
             receiver="SF30_NODE", child_arg="CHILD_OBJ"),
        # r5 (child_provenance) INTENTIONALLY ABSENT: unresolved in the source run (A).
        edge("r6", "join_operation", va=0x007B5846, nbytes=3, expect="01 5E 04",
             mechanism="children_array_insert_on_parent", parent="SF30_NODE", child="CHILD_OBJ"),
        # r7 (visual_role) INTENTIONALLY ABSENT: unresolved in the source run (D).
    ],
}

SYNTHETIC_CLEAN = {
    "chain_id": "SYNTHETIC_GATE_TEST_ONLY",
    "is_synthetic": True,
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


# --------------------------------------------------------------- the checks
def schema_check(chain):
    """Declared-shape validation. ID-agnostic: inspects only the chain's own fields."""
    fails = []
    if not isinstance(chain.get("chain_id"), str) or not chain.get("chain_id"):
        fails.append("SCHEMA_FAIL: chain_id missing/not a non-empty string")
    if not isinstance(chain.get("is_synthetic"), bool):
        fails.append("SCHEMA_FAIL: is_synthetic missing/not a bool")
    edges = chain.get("edges")
    if not isinstance(edges, list) or not edges:
        fails.append("SCHEMA_FAIL: edges missing/empty/not a list")
        return "FAIL", fails, {}
    ids = [e.get("id") for e in edges]
    if any(not isinstance(i, str) or not i for i in ids):
        fails.append("SCHEMA_FAIL: an edge lacks a non-empty string id")
    if len(set(ids)) != len(ids):
        fails.append("SCHEMA_FAIL: duplicate edge ids")
    for e in edges:
        if e.get("type") not in KNOWN_EDGE_TYPES:
            fails.append(f"SCHEMA_FAIL: edge {e.get('id')} has unknown type {e.get('type')!r}")
    # synthetic-marking consistency (whole chain, no ID exceptions)
    edge_syn = [bool(e.get("synthetic")) for e in edges]
    if chain.get("is_synthetic") is True and not all(edge_syn):
        fails.append("SCHEMA_FAIL: SYNTHETIC_MARKING_INCONSISTENCY: chain is synthetic "
                     "but not every edge is marked synthetic=True")
    if chain.get("is_synthetic") is False and any(edge_syn):
        fails.append("SCHEMA_FAIL: SYNTHETIC_MARKING_INCONSISTENCY: chain claims real "
                     "(is_synthetic=False) but contains edge-local synthetic=True edges")
    return ("PASS" if not fails else "FAIL"), fails, {"edges_checked": len(edges)}


def pin_check(chain):
    """Byte-equality verification of declared byte claims against the pinned EXE.
    SCOPE: presence/equality ONLY — no instruction decode, NO semantic binding of the
    bytes to the edge's claimed meaning (contract §4 forbids a general semantic verifier)."""
    byte_results = {}
    ok_all = True
    n = 0
    for e in chain.get("edges", []):
        if "va" not in e:
            continue
        n += 1
        try:
            got = hexb(e["va"], e["nbytes"])
            ok = got == e["expect"]
        except Exception as ex:  # unmapped VA / bad fields
            got, ok = f"ERROR: {ex}", False
        byte_results[e["id"]] = f"va {e.get('va'):#010x} got '{got}' expect '{e.get('expect')}' match={ok}"
        if not ok:
            ok_all = False
    if n == 0:
        return "NOT_CHECKED", [], {"byte_claims": 0,
                                   "scope": "no edge in this chain declares a byte claim; nothing checked"}
    return ("PASS" if ok_all else "FAIL"), ([] if ok_all else ["PIN_CHECK_FAIL: at least one declared byte claim mismatches the pinned EXE"]), {
        "byte_claims": n,
        "scope": "byte presence/equality at the declared VAs only; NOT semantic binding",
    }


def structural_check(chain):
    """Declared-field structural predicates. ID-agnostic."""
    fails = []
    reached = {}
    edges = chain.get("edges", [])
    has_creation = any(e["type"] == "sf_creation" for e in edges)
    has_store = any(e["type"] == "sf_store" for e in edges)
    pia = [e for e in edges if e["type"] == "parent_identity_access" and e.get("field") == "+0x30"]
    rcv = [e for e in edges if e["type"] == "parent_receiver"]
    cp = [e for e in edges if e["type"] == "child_provenance"]
    jo = [e for e in edges if e["type"] == "join_operation"]
    vr = [e for e in edges if e["type"] == "visual_role"]

    # P_PARENT
    reached["P_PARENT"] = "EVALUATED"
    if not (has_creation and has_store and pia):
        fails.append("P_PARENT_FAIL: missing sf_creation/sf_store/parent_identity_access(+0x30)")
    elif not rcv:
        fails.append("P_PARENT_FAIL: no parent_receiver edge")
    else:
        node = pia[0].get("to", DEFAULT_PARENT_NODE)
        for r in rcv:
            if r.get("receiver") != node:
                fails.append(f"P_PARENT_FAIL: receiver {r.get('receiver')} != the SF+0x30 node ({node})")

    # P_CHILD (declared fields only — this PASS is NEVER a science qualification)
    reached["P_CHILD"] = "EVALUATED"
    if not cp:
        fails.append("P_CHILD_FAIL: no child_provenance edge (model/resource provenance not established)")
    else:
        e = cp[0]
        if e.get("op") != "physically_established_model_resource_op":
            fails.append("P_CHILD_FAIL: child provenance op not physically established")
        if not e.get("identity_preserved"):
            fails.append("P_CHILD_FAIL: child identity not preserved (wrapper/clone break)")

    # P_CONNECT (declared endpoint connectivity; NOT_CHECKED when no endpoints declared)
    if cp and rcv and ("to_object" in cp[0] or "from_object" in cp[0]):
        reached["P_CONNECT"] = "EVALUATED"
        if "to_object" in cp[0] and cp[0].get("to_object") != rcv[0].get("child_arg"):
            fails.append(f"P_CONNECT_FAIL: provenance to_object {cp[0].get('to_object')!r} "
                         f"!= the join child argument {rcv[0].get('child_arg')!r}")
    else:
        reached["P_CONNECT"] = "NOT_CHECKED (no declared provenance endpoints to compare)"

    # P_OPERATION
    reached["P_OPERATION"] = "EVALUATED"
    if not jo:
        fails.append("P_OPERATION_FAIL: no join_operation edge")
    else:
        e = jo[0]
        if e.get("mechanism") != "children_array_insert_on_parent":
            fails.append("P_OPERATION_FAIL: mechanism is not a parent-child binding on the exact parent")
        if rcv:
            if e.get("parent") != rcv[0].get("receiver"):
                fails.append("P_OPERATION_FAIL: operation parent != join receiver node")
            if e.get("child") != rcv[0].get("child_arg"):
                fails.append("P_OPERATION_FAIL: operation child != the receiver's child argument")

    # P_VISUAL
    reached["P_VISUAL"] = "EVALUATED"
    if not vr:
        fails.append("P_VISUAL_FAIL: no visual_role edge")
    elif vr[0].get("proof") != "physical_visual_role_proof":
        fails.append("P_VISUAL_FAIL: visual role proof not physical")

    return ("PASS" if not fails else "FAIL"), fails, {"predicates_reached": reached}


def evaluate_chain(chain):
    """The corrected gate. Returns the separate mechanical checks + the two verdicts.
    No chain_id / candidate-id / mutation-id is consulted anywhere in the verdict logic."""
    sc, sc_fails, sc_detail = schema_check(chain)
    pc, pc_fails, pc_detail = pin_check(chain)
    st, st_fails, st_detail = structural_check(chain)
    mechanical = "PASS" if (sc == "PASS" and st == "PASS" and pc != "FAIL") else "FAIL"
    if chain.get("is_synthetic") is True:
        science = "SYNTHETIC_MACHINERY_TEST_ONLY"
        sci_reasons = ["synthetic fixture: mechanical result is a machinery test only; "
                       "never PCG evidence; never promotes INSTANCE_MODEL_NODE_JOIN"]
    else:
        science = "NOT_QUALIFIED"
        sci_reasons = [
            "REAL_SCIENCE_AUTO_QUALIFICATION_DISABLED (contract §4 policy of this correction)",
            "MANUAL_PHYSICAL_EVIDENCE_REQUIRED: this tool cannot independently bind every required "
            "semantic assertion (child model/resource provenance, visual role, semantic meaning of "
            "pinned bytes) to physical evidence records and exact endpoints from declared fields alone",
        ]
        if st != "PASS":
            sci_reasons.append("additionally: structural predicates FAIL (declared shape inconsistent)")
        if pc == "FAIL":
            sci_reasons.append("additionally: declared byte claims FAIL PIN_CHECK")
    return {
        "SCHEMA_CHECK": {"verdict": sc, "failures": sc_fails, "detail": sc_detail},
        "PIN_CHECK": {"verdict": pc, "failures": pc_fails, "detail": pc_detail},
        "STRUCTURAL_CONSISTENCY_CHECK": {"verdict": st, "failures": st_fails, "detail": st_detail},
        "MECHANICAL_VERDICT": mechanical,
        "SCIENCE_QUALIFICATION": {"verdict": science, "reasons": sci_reasons,
                                  "note": "no code path in this tool yields SCIENCE_PASS; the corrected "
                                          "status is QC_POSITIVE_CHAIN_QUALIFICATION = "
                                          "NOT_ESTABLISHED_AS_GENERAL_AUTHORITY"},
    }


# ----------------------------------------------------- counterexample fixtures
# RECREATED INDEPENDENTLY from contract §4 (lines 179–199), not copied from the Desktop JSON.

def make_m1():
    c = copy.deepcopy(REAL_CAND4)
    c["chain_id"] = "M1-real-fake-AD-by-declaration"
    c["edges"].append(edge("r5", "child_provenance",
                           op="physically_established_model_resource_op", identity_preserved=True))
    c["edges"].append(edge("r7", "visual_role", proof="physical_visual_role_proof"))
    return c, ["+r5 child_provenance (op=physically_established_model_resource_op, "
               "identity_preserved=True; NO va/bytes/evidence record)",
               "+r7 visual_role (proof=physical_visual_role_proof; NO va/bytes/evidence record)"]


def make_m2():
    c, changed = make_m1()
    c["chain_id"] = "M2-real-parent-pin-swapped-to-SF20-store"
    for e in c["edges"]:
        if e["id"] == "r3":
            e["va"] = 0x0050A3AC
            e["nbytes"] = 3
            e["expect"] = "89 7E 20"  # the REAL EXE bytes of mov [esi+0x20],edi (a STORE)
    changed.append("r3 parent_identity_access byte pin replaced with the real SF+0x20 STORE bytes "
                   "@0x0050A3AC (89 7E 20); the field declaration still claims the +0x30 parent load")
    return c, changed


def make_m3():
    c, changed = make_m1()
    c["chain_id"] = "M3-real-join-pin-swapped-to-accessor-ret"
    for e in c["edges"]:
        if e["id"] == "r6":
            e["va"] = 0x008BD720
            e["nbytes"] = 4
            e["expect"] = "8D 41 18 C3"  # lea eax,[ecx+0x18]; ret — the 4-byte accessor/RET
    changed.append("r6 join_operation byte pin replaced with the 4-byte accessor/RET @0x008BD720 "
                   "(8D 41 18 C3); the declared mechanism (children_array_insert_on_parent) unchanged")
    return c, changed


def make_m4():
    c, changed = make_m1()
    c["chain_id"] = "M4-real-provenance-endpoints-disconnected"
    for e in c["edges"]:
        if e["id"] == "r5":
            e["from_object"] = "OTHER_RESOURCE_RESULT"
            e["to_object"] = "OTHER_CHILD_UNRELATED_TO_CALL"
    changed.append("r5 child_provenance given explicit endpoints "
                   "from_object=OTHER_RESOURCE_RESULT -> to_object=OTHER_CHILD_UNRELATED_TO_CALL "
                   "(breaking connectivity to the join child argument CHILD_OBJ)")
    return c, changed


def make_m5():
    c = copy.deepcopy(SYNTHETIC_CLEAN)
    c["chain_id"] = "M5-synthetic-relabelled-real-top-level"
    c["is_synthetic"] = False  # top-level relabel ONLY; edge-local synthetic=True flags remain
    return c, ["top-level is_synthetic flipped True -> False on the synthetic fixture; "
               "all edge-local synthetic=True flags left unchanged"]


def make_ctrl_a():
    c = copy.deepcopy(SYNTHETIC_CLEAN)
    c["chain_id"] = "CTRL-A-parent-other-node"
    for e in c["edges"]:
        if e["type"] == "parent_receiver":
            e["receiver"] = "OTHER_NODE"
    return c, ["parent_receiver.receiver: SF30_NODE -> OTHER_NODE"]


def make_ctrl_b():
    c = copy.deepcopy(SYNTHETIC_CLEAN)
    c["chain_id"] = "CTRL-B-child-provenance-removed"
    c["edges"] = [e for e in c["edges"] if e["type"] != "child_provenance"]
    return c, ["child_provenance edge removed"]


def make_ctrl_c():
    c = copy.deepcopy(SYNTHETIC_CLEAN)
    c["chain_id"] = "CTRL-C-identity-edge-broken"
    for e in c["edges"]:
        if e["type"] == "parent_identity_access":
            e["field"] = "+0x34"
    return c, ["parent_identity_access.field: +0x30 -> +0x34"]


# ------------------------------------------------------------------------- run
def main():
    results = {
        "tool": "QUALIFICATION_GATE_CORRECTED.py",
        "run_id": "PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007",
        "policy": {
            "REAL_SCIENCE_AUTO_QUALIFICATION": REAL_SCIENCE_AUTO_QUALIFICATION,
            "QC_POSITIVE_CHAIN_QUALIFICATION": QC_POSITIVE_CHAIN_QUALIFICATION,
            "no_code_path_yields_SCIENCE_PASS": True,
            "pin_check_scope": "byte presence/equality at declared VAs only; NO semantic binding; "
                               "no instruction decoding; no general EXE semantic verifier (contract §4)",
        },
        "pinned_exe": {"size": len(data), "sha256": hashlib.sha256(data).hexdigest().upper()},
        "cases": {},
    }

    cases = [
        ("synthetic_clean_control", SYNTHETIC_CLEAN, [], "baseline"),
        ("CTRL_A", make_ctrl_a()[0], make_ctrl_a()[1], "control"),
        ("CTRL_B", make_ctrl_b()[0], make_ctrl_b()[1], "control"),
        ("CTRL_C", make_ctrl_c()[0], make_ctrl_c()[1], "control"),
        ("real_CAND4_clean_unresolved", REAL_CAND4, [], "real"),
        ("M1", make_m1()[0], make_m1()[1], "counterexample"),
        ("M2", make_m2()[0], make_m2()[1], "counterexample"),
        ("M3", make_m3()[0], make_m3()[1], "counterexample"),
        ("M4", make_m4()[0], make_m4()[1], "counterexample"),
        ("M5", make_m5()[0], make_m5()[1], "counterexample"),
    ]

    for name, chain, ch, kind in cases:
        r = evaluate_chain(chain)
        r["chain_id"] = chain["chain_id"]
        r["is_synthetic"] = chain["is_synthetic"]
        r["changed_fields_vs_base"] = ch
        r["case_kind"] = kind
        results["cases"][name] = r

    # ID-hard-coding negative probes: identical chains under renamed chain_ids must
    # produce identical verdicts (the gate never rejects/accepts by identity).
    id_probes = {}
    for probe_name, base in [("probe_M1_renamed", make_m1()[0]),
                             ("probe_real_CAND4_renamed", copy.deepcopy(REAL_CAND4)),
                             ("probe_synthetic_renamed", copy.deepcopy(SYNTHETIC_CLEAN))]:
        renamed = copy.deepcopy(base)
        renamed["chain_id"] = "RENAME_PROBE_" + base["chain_id"]
        id_probes[probe_name] = {
            "original": evaluate_chain(base),
            "renamed": evaluate_chain(renamed),
            "verdicts_identical": evaluate_chain(base) == evaluate_chain(renamed),
        }
    results["id_hard_coding_probes"] = id_probes

    c = results["cases"]
    self_checks = {
        "synthetic_clean_machinery_pass_never_science":
            c["synthetic_clean_control"]["MECHANICAL_VERDICT"] == "PASS"
            and c["synthetic_clean_control"]["SCIENCE_QUALIFICATION"]["verdict"] == "SYNTHETIC_MACHINERY_TEST_ONLY",
        "ctrl_a_fails_by_parent_predicate":
            c["CTRL_A"]["MECHANICAL_VERDICT"] == "FAIL"
            and any(f.startswith("P_PARENT_FAIL") for f in c["CTRL_A"]["STRUCTURAL_CONSISTENCY_CHECK"]["failures"]),
        "ctrl_b_fails_by_child_predicate":
            c["CTRL_B"]["MECHANICAL_VERDICT"] == "FAIL"
            and any(f.startswith("P_CHILD_FAIL") for f in c["CTRL_B"]["STRUCTURAL_CONSISTENCY_CHECK"]["failures"]),
        "ctrl_c_fails_by_parent_identity_predicate":
            c["CTRL_C"]["MECHANICAL_VERDICT"] == "FAIL"
            and any(f.startswith("P_PARENT_FAIL") for f in c["CTRL_C"]["STRUCTURAL_CONSISTENCY_CHECK"]["failures"]),
        "real_CAND4_remains_not_qualified":
            c["real_CAND4_clean_unresolved"]["SCIENCE_QUALIFICATION"]["verdict"] == "NOT_QUALIFIED"
            and c["real_CAND4_clean_unresolved"]["MECHANICAL_VERDICT"] == "FAIL",
        "real_CAND4_pins_verified_but_pins_are_not_semantics":
            c["real_CAND4_clean_unresolved"]["PIN_CHECK"]["verdict"] == "PASS"
            and c["real_CAND4_clean_unresolved"]["PIN_CHECK"]["detail"]["byte_claims"] == 5,
        "M1_not_qualified":
            c["M1"]["SCIENCE_QUALIFICATION"]["verdict"] == "NOT_QUALIFIED",
        "M2_not_qualified":
            c["M2"]["SCIENCE_QUALIFICATION"]["verdict"] == "NOT_QUALIFIED",
        "M3_not_qualified":
            c["M3"]["SCIENCE_QUALIFICATION"]["verdict"] == "NOT_QUALIFIED",
        "M4_not_qualified_plus_mechanical_connectivity_fail":
            c["M4"]["SCIENCE_QUALIFICATION"]["verdict"] == "NOT_QUALIFIED"
            and c["M4"]["MECHANICAL_VERDICT"] == "FAIL"
            and any(f.startswith("P_CONNECT_FAIL") for f in c["M4"]["STRUCTURAL_CONSISTENCY_CHECK"]["failures"]),
        "M5_not_qualified_plus_mechanical_schema_fail":
            c["M5"]["SCIENCE_QUALIFICATION"]["verdict"] == "NOT_QUALIFIED"
            and c["M5"]["MECHANICAL_VERDICT"] == "FAIL"
            and any("SYNTHETIC_MARKING_INCONSISTENCY" in f for f in c["M5"]["SCHEMA_CHECK"]["failures"]),
        "no_science_pass_anywhere":
            all(r["SCIENCE_QUALIFICATION"]["verdict"] != "SCIENCE_PASS" for r in results["cases"].values()),
        "no_bare_declaration_acceptance":
            c["M1"]["SCIENCE_QUALIFICATION"]["verdict"] == "NOT_QUALIFIED"
            and c["M1"]["MECHANICAL_VERDICT"] == "PASS",
        "id_probes_verdicts_identical":
            all(p["verdicts_identical"] for p in id_probes.values()),
        "exe_sha_verified": True,
    }
    results["self_checks"] = self_checks
    results["OVERALL"] = "PASS" if all(self_checks.values()) else "FAIL"

    out_full = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007\03_SCRIPTS\gate_corrected_results.json"
    with open(out_full, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(results, fh, indent=2)
        fh.write("\n")

    # ---------------- GATE_COUNTEREXAMPLES.json (per-counterexample record) -------
    def why_non_circular(case_key):
        if case_key in ("M1", "M2", "M3"):
            return ("the NOT QUALIFIED verdict is produced by the pre-registered, uniformly-applied "
                    "policy REAL_SCIENCE_AUTO_QUALIFICATION=DISABLED (contract §4) which withholds "
                    "automatic science qualification from EVERY real chain — including the UNMUTATED "
                    "real CAND-4 — and not from any inspection of this mutation's specific fields; the "
                    "gate code contains no candidate-ID/mutation-ID rejection branch (proven by the "
                    "renamed-chain probes returning identical verdicts); PIN_CHECK is byte-equality only "
                    "and never claims semantic binding")
        if case_key == "M4":
            return ("P_CONNECT is a declared-field predicate applied uniformly to any chain that declares "
                    "provenance endpoints: to_object must equal the join child argument; it fires on the "
                    "declared mismatch itself, not on any identity of this fixture (renamed-probe "
                    "equivalence holds)")
        if case_key == "M5":
            return ("SYNTHETIC_MARKING_INCONSISTENCY is a schema predicate applied uniformly: a chain "
                    "claiming is_synthetic=False may not contain edge-local synthetic=True edges; it fires "
                    "on the inconsistent declaration itself, not on any fixture identity")
        return ("control mutations reproduce the causal predicate failures of the source run's own "
                "CTRL-A/B/C on the same checker implementation")

    cx = {
        "run_id": "PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007",
        "recreation_basis": "contract §4 (OPENCODE_J1_J3_CORRECTION_REVIEWED.md) textual mutation "
                            "definitions M1–M5, recreated independently by this correction; the Desktop's "
                            "PRODUCTION_GATE_COUNTEREXAMPLES.json (SHA256 6632C6D1…066D16) is an input "
                            "identity only and was not copied as the fixture source",
        "checker": "QUALIFICATION_GATE_CORRECTED.py (this package)",
        "policy": {"REAL_SCIENCE_AUTO_QUALIFICATION": "DISABLED",
                   "QC_POSITIVE_CHAIN_QUALIFICATION": "NOT_ESTABLISHED_AS_GENERAL_AUTHORITY"},
        "policy_disclosure": (
            "With real-science auto-qualification disabled BY POLICY, M1/M2/M3 are NOT QUALIFIED "
            "through that policy. The mechanical checks do NOT detect M1/M2/M3's specific defects: "
            "M1's added edges carry no byte claims at all; M2's substituted pin is a REAL EXE STORE at "
            "the pinned VA (89 7E 20 @0x0050A3AC) and M3's substituted pin is a REAL accessor/RET at the "
            "pinned VA (8D 41 18 C3 @0x008BD720) — PIN_CHECK verifies byte presence/equality only, never "
            "semantic binding. This run therefore establishes THE ABSENCE OF AUTOMATIC SCIENCE PROMOTION "
            "for real chains, NOT validator detection of a specific wrong opcode/endpoint. M4 and M5 are "
            "additionally rejected by mechanical predicates (P_CONNECT connectivity; SCHEMA "
            "synthetic-marking consistency), each showing clean PASS -> mutated FAIL on this same checker. "
            "CTRL-A/B/C retain their causal mechanical FAILs."
        ),
        "cases": {},
    }
    for name in ["M1", "M2", "M3", "M4", "M5"]:
        r = results["cases"][name]
        cx["cases"][name] = {
            "expected_by_contract": "NOT QUALIFIED",
            "changed_fields": r["changed_fields_vs_base"],
            "predicates_reached": {
                "SCHEMA_CHECK": r["SCHEMA_CHECK"]["verdict"],
                "PIN_CHECK": r["PIN_CHECK"]["verdict"],
                "PIN_CHECK_byte_claims": r["PIN_CHECK"]["detail"].get("byte_claims"),
                "STRUCTURAL_CONSISTENCY_CHECK": r["STRUCTURAL_CONSISTENCY_CHECK"]["verdict"],
                "structural_predicates": r["STRUCTURAL_CONSISTENCY_CHECK"]["detail"]["predicates_reached"],
                "structural_failures": r["STRUCTURAL_CONSISTENCY_CHECK"]["failures"],
                "schema_failures": r["SCHEMA_CHECK"]["failures"],
            },
            "mechanical_verdict": r["MECHANICAL_VERDICT"],
            "science_qualification_verdict": r["SCIENCE_QUALIFICATION"]["verdict"],
            "science_qualification_reasons": r["SCIENCE_QUALIFICATION"]["reasons"],
            "causal_rejection_reason": (
                ("policy: REAL_SCIENCE_AUTO_QUALIFICATION=DISABLED + MANUAL_PHYSICAL_EVIDENCE_REQUIRED "
                 "(no mechanical predicate detects this mutation; the mechanical verdict is PASS)")
                if name in ("M1", "M2", "M3")
                else ("mechanical predicate: " + ("P_CONNECT_FAIL (declared provenance endpoints do not "
                      "connect to the join child argument)" if name == "M4"
                      else "SCHEMA SYNTHETIC_MARKING_INCONSISTENCY (real-declaring chain with "
                           "edge-local synthetic edges)"))
            ),
            "why_non_circular": why_non_circular(name),
        }
    cx["retained_controls"] = {
        name: {
            "mechanical_verdict": results["cases"][name]["MECHANICAL_VERDICT"],
            "science_qualification_verdict": results["cases"][name]["SCIENCE_QUALIFICATION"]["verdict"],
            "changed_fields": results["cases"][name]["changed_fields_vs_base"],
            "failures": (results["cases"][name]["STRUCTURAL_CONSISTENCY_CHECK"]["failures"]
                         + results["cases"][name]["SCHEMA_CHECK"]["failures"]),
        } for name in ["CTRL_A", "CTRL_B", "CTRL_C"]
    }
    cx["synthetic_clean_control"] = {
        "mechanical_verdict": results["cases"]["synthetic_clean_control"]["MECHANICAL_VERDICT"],
        "science_qualification_verdict": "SYNTHETIC_MACHINERY_TEST_ONLY",
        "note": "a synthetic PASS is a machinery test only; never PCG evidence; never promotion",
    }
    cx["real_CAND4_clean_unresolved"] = {
        "mechanical_verdict": results["cases"]["real_CAND4_clean_unresolved"]["MECHANICAL_VERDICT"],
        "science_qualification_verdict": "NOT_QUALIFIED",
        "reasons": results["cases"]["real_CAND4_clean_unresolved"]["SCIENCE_QUALIFICATION"]["reasons"],
        "note": "A and D remain unresolved; the real candidate stays NOT QUALIFIED (contract §4)",
    }
    cx["id_hard_coding_probes"] = {k: v["verdicts_identical"] for k, v in id_probes.items()}
    cx["findings_do_not_promote_science"] = True
    cx["OVERALL"] = results["OVERALL"]

    out_cx = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007\GATE_COUNTEREXAMPLES.json"
    with open(out_cx, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(cx, fh, indent=2)
        fh.write("\n")

    print(json.dumps({"OVERALL": results["OVERALL"],
                      "self_checks": self_checks}, indent=2))
    return 0 if results["OVERALL"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
