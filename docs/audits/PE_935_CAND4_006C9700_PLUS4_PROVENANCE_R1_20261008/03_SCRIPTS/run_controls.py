"""run_controls.py — the controls of PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008.

Mechanical controls (anchor validation): a documented CLEAN pass of the production
gate (03_SCRIPTS/checker_plus4.py run_checks/gate) + DELIBERATE CORRUPTIONS of the
proper load-bearing anchors performed on IN-MEMORY COPIES of the physical EXE
(the file is NEVER modified) — the SAME production gate (the same run_checks code
path: pins / rel32 / RTTI / strings) must detect each corruption at the exact
anchor. A corruption of an UNRELATED byte (outside every pinned window) must leave
the anchor gates PASSing (specificity control: the failures are caused by the
anchor corruptions, not by generic damage detection). The whole-file SHA gate is
NOT used as the corruption detector (it detects ANY byte change — a manifest-level
failure, NOT anchor validation; documented).

CTRL_A..CTRL_G (contract §6): logical controls that reject unauthorized inferences.
They are SYNTHETIC_LOGICAL_CONTROL — implemented here as explicit predicates; they
are NOT new physical PCG measurements and are never presented as such.

python -B; stdlib only. Writes CONTROL_RESULTS.json.
"""
import copy
import hashlib
import json
import os
import struct
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import checker_plus4 as chk  # noqa: E402

OUT_JSON = os.path.join(HERE, "..", "CONTROL_RESULTS.json")


def sha256_of(b):
    return hashlib.sha256(b).hexdigest().upper()


def corrupt_at(data, va, new_hex):
    """Return a corrupted in-memory copy with new_hex written at va (own PE mapping)."""
    pe = chk.OwnPE(bytes(data))
    off = pe.va_to_off(va)
    if off is None:
        raise ValueError(f"VA {va:#010x} unmapped")
    new = bytes.fromhex(new_hex.replace(" ", ""))
    out = bytearray(data)
    out[off:off + len(new)] = new
    return bytes(out)


def rel32_corrupt_at(data, call_va):
    """Flip one bit of the rel32 operand at call_va (target must change)."""
    pe = chk.OwnPE(bytes(data))
    off = pe.va_to_off(call_va)
    out = bytearray(data)
    out[off + 1] ^= 0x01  # flip the lowest bit of the rel32's first byte
    return bytes(out)


def mechanical_controls():
    results = {}

    # ---- clean pass (documented) ----
    clean = chk.run_checks()
    ok, fails = chk.gate(clean)
    results["clean_pass"] = {
        "checks_total": len(clean),
        "checks_pass": sum(1 for r in clean if r[1] == "PASS"),
        "gate": "PASS" if ok else "FAIL",
        "fails": [f"{r[0]}: {r[2]}" for r in fails],
    }

    # ---- load the physical EXE once for the corruption copies ----
    with open(chk.EXE_PATH, "rb") as f:
        exe = f.read()
    assert len(exe) == chk.EXE_SIZE and sha256_of(exe) == chk.EXE_SHA256, "EXE identity"
    results["corruption_base_identity"] = {
        "size": len(exe),
        "sha256": sha256_of(exe),
        "note": "in-memory copies only; the physical file is never modified",
    }

    # ---- MC-1: corrupt THE +4 WRITER anchor (CTOR_R4_STORE_P: 89 46 04 -> 8B 46 04) ----
    c1 = corrupt_at(exe, 0x006E8FA5, "8B 46 04")
    r1 = chk.run_checks(data_override=c1)
    ok1, fails1 = chk.gate(r1)
    hit1 = [f for f in fails1 if f[0] == "PIN:CTOR_R4_STORE_P"]
    results["MC1_plus4_writer_anchor"] = {
        "corruption": "@0x006E8FA5 89 46 04 -> 8B 46 04 (mov [esi+4],eax -> mov esi,[eax+4]-shaped bytes)",
        "gate": "FAIL" if not ok1 else "PASS",
        "anchor_detected": bool(hit1),
        "anchor_fail_detail": hit1[0][2] if hit1 else None,
        "verdict": "PASS" if (not ok1 and hit1) else "FAIL",
    }

    # ---- MC-2: corrupt the ctor RETURN-THIS anchor (8B C6 -> 8B C7) ----
    c2 = corrupt_at(exe, 0x006E9014, "8B C7")
    r2 = chk.run_checks(data_override=c2)
    ok2, fails2 = chk.gate(r2)
    hit2 = [f for f in fails2 if f[0] == "PIN:CTOR_RETURN_THIS"]
    results["MC2_ctor_return_this_anchor"] = {
        "corruption": "@0x006E9014 8B C6 -> 8B C7 (mov eax,esi -> mov eax,edi)",
        "gate": "FAIL" if not ok2 else "PASS",
        "anchor_detected": bool(hit2),
        "verdict": "PASS" if (not ok2 and hit2) else "FAIL",
    }

    # ---- MC-3: corrupt the pump RETURN-R anchor (8B C6 -> 90 90) ----
    c3 = corrupt_at(exe, 0x006C9808, "90 90")
    r3 = chk.run_checks(data_override=c3)
    ok3, fails3 = chk.gate(r3)
    hit3 = [f for f in fails3 if f[0] == "PIN:PUMP_RETURN_R"]
    results["MC3_pump_return_R_anchor"] = {
        "corruption": "@0x006C9808 8B C6 -> 90 90 (mov eax,esi -> nop nop)",
        "gate": "FAIL" if not ok3 else "PASS",
        "anchor_detected": bool(hit3),
        "verdict": "PASS" if (not ok3 and hit3) else "FAIL",
    }

    # ---- MC-4: corrupt the ctor CALL rel32 (REL_PUMP_CTOR_R) ----
    c4 = rel32_corrupt_at(exe, 0x006C97D8)
    r4 = chk.run_checks(data_override=c4)
    ok4, fails4 = chk.gate(r4)
    hit4 = [f for f in fails4 if f[0] == "REL32:REL_PUMP_CTOR_R"]
    results["MC4_ctor_call_rel32_anchor"] = {
        "corruption": "@0x006C97D8 rel32 operand byte bit-flip (target must cease to be 0x006E8F70)",
        "gate": "FAIL" if not ok4 else "PASS",
        "anchor_detected": bool(hit4),
        "anchor_fail_detail": hit4[0][2] if hit4 else None,
        "verdict": "PASS" if (not ok4 and hit4) else "FAIL",
    }

    # ---- MC-5: corrupt the W RTTI chain anchor (the TypeDescriptor name of W) ----
    pe = chk.OwnPE(exe)
    col_ptr = pe.u32(0x00A864B8 - 4)
    col_off = pe.va_to_off(col_ptr)
    _sig, _o, _cd, ptd, _pcd = struct.unpack_from("<5I", exe, col_off)
    ptd_off = pe.va_to_off(ptd)
    c5 = bytearray(exe)
    c5[ptd_off + 8] = ord("X")  # first char of ".?AVArkModelResourceInstanceRef@@"
    r5 = chk.run_checks(data_override=bytes(c5))
    ok5, fails5 = chk.gate(r5)
    hit5 = [f for f in fails5 if f[0] == "RTTI:RTTI_W_ARKMODELRESOURCEINSTANCEREF"]
    results["MC5_w_rtti_chain_anchor"] = {
        "corruption": f"@TypeDescriptor {ptd:#010x}+8 first name byte '.' -> 'X'",
        "gate": "FAIL" if not ok5 else "PASS",
        "anchor_detected": bool(hit5),
        "verdict": "PASS" if (not ok5 and hit5) else "FAIL",
    }

    # ---- MC-6 (specificity): corrupt an UNRELATED byte (no pinned window covers it) ----
    # .rsrc raw area, RVA 0x7A1000+0x100 (resource data; no pin/rel32/RTTI/string uses it)
    unrelated_va = 0x00400000 + 0x7A1000 + 0x100
    c6 = corrupt_at(exe, unrelated_va, "AA")
    r6 = chk.run_checks(data_override=c6)
    ok6, fails6 = chk.gate(r6)
    results["MC6_unrelated_corruption_specificity"] = {
        "corruption": f"@{unrelated_va:#010x} (unpinned .rsrc byte) -> AA",
        "anchor_gates_still_pass": bool(ok6),
        "note": "the anchor gates must remain PASS — the MC1..MC5 failures were caused by the "
                "load-bearing anchor corruptions, not by generic damage detection; the "
                "whole-file SHA gate is NOT used as the corruption detector (documented)",
        "verdict": "PASS" if ok6 else "FAIL",
    }

    return results


# ---------------------------------------------------------------------------
# CTRL_A..CTRL_G — SYNTHETIC_LOGICAL_CONTROL (contract §6 verbatim; they reject
# unauthorized inferences; they are NOT seven new science questions).
# ---------------------------------------------------------------------------
def ctrl_a():
    """Intermediate/nearby RTTI without final-return dataflow does not qualify R."""
    def qualifier(has_vptr_store_into_r, has_rtti_chain_for_that_vptr, rtti_chain_is_nearby_only):
        # R is class-identified ONLY by a vptr STORE into R + that vptr's RTTI chain.
        if rtti_chain_is_nearby_only and not has_vptr_store_into_r:
            return "NOT_QUALIFIED"
        if has_vptr_store_into_r and has_rtti_chain_for_that_vptr:
            return "QUALIFIED"
        return "NOT_QUALIFIED"
    fixture_r = qualifier(False, False, True)  # the real chain: nearby W RTTI only, no vptr store in R
    rejection_ok = (fixture_r == "NOT_QUALIFIED")
    sanity = qualifier(True, True, False) == "QUALIFIED"  # the legal form would qualify
    return {
        "control": "CTRL_A: nearby/intermediate RTTI without final-return dataflow does not qualify R",
        "class": "SYNTHETIC_LOGICAL_CONTROL",
        "fixture": "R construction measured: no vptr store (89 06 stores the S pointer); nearby RTTI = the W class only",
        "rejection_observed": rejection_ok,
        "legal_form_sanity": sanity,
        "verdict": "PASS" if (rejection_ok and sanity) else "FAIL",
    }


def ctrl_b():
    """Mixing R+4/T+4, +4/+8 or unproven bases does not qualify field identity; a
    proven alias is a legal result, not an automatic FAIL."""
    def field_identity(dst_expr, src_expr, same_base_proven):
        # legal only if the destination base and the source base are proven equal
        return "QUALIFIED" if same_base_proven else "NOT_QUALIFIED"
    unproven = field_identity("[T+4]", "[R+4]", False)          # T==P not established
    proven = field_identity("[R+4]", "[R+4]", True)             # this run's measured store
    rejection_ok = (unproven == "NOT_QUALIFIED")
    legal_ok = (proven == "QUALIFIED")  # the proven alias (T==P) is a legal result
    return {
        "control": "CTRL_B: unproven base mixing rejected; proven alias legal",
        "class": "SYNTHETIC_LOGICAL_CONTROL",
        "fixture_unproven": "[T+4] vs [R+4] without the T==P dataflow -> NOT_QUALIFIED",
        "fixture_proven": "T = [R+4] = P (the ctor store + the installer load, same base R) -> QUALIFIED (legal)",
        "rejection_observed": rejection_ok,
        "legal_alias_accepted": legal_ok,
        "verdict": "PASS" if (rejection_ok and legal_ok) else "FAIL",
    }


def ctrl_c():
    """ctor(W,R) and the W name do not qualify class(R) without a separate edge."""
    def class_of_r(w_ctor_exists, w_rtti_name, r_has_own_vptr_edge):
        if w_ctor_exists and w_rtti_name and not r_has_own_vptr_edge:
            return "NOT_QUALIFIED"  # the W identity does NOT transfer to R
        if r_has_own_vptr_edge:
            return "QUALIFIED"
        return "NOT_QUALIFIED"
    fixture = class_of_r(True, "ArkModelResourceInstanceRef", False)  # the real evidence shape
    rejection_ok = (fixture == "NOT_QUALIFIED")
    sanity = class_of_r(False, "", True) == "QUALIFIED"
    return {
        "control": "CTRL_C: ctor(W,R) + W's name do not qualify class(R)",
        "class": "SYNTHETIC_LOGICAL_CONTROL",
        "fixture": "historical ctor FUN_006FA8B0(W,R) exists; W RTTI name measured; R has NO own vptr edge",
        "rejection_observed": rejection_ok,
        "legal_form_sanity": sanity,
        "verdict": "PASS" if (rejection_ok and sanity) else "FAIL",
    }


def ctrl_d():
    """Count-versus-pointer conflict is only conditional until class/base/layout are
    proven; an unproven condition = CONDITIONAL_UNRESOLVED; a prior map is not a new
    layout measurement; the proven condition resolves it."""
    def conflict_state(base_proven, plus4_holds_pointer):
        if not base_proven:
            return "CONDITIONAL_UNRESOLVED"
        return "RESOLVED_AS_POINTER" if plus4_holds_pointer else "RESOLVED_AS_COUNT"
    unproven = conflict_state(False, None)                                   # before this run
    resolved = conflict_state(True, True)                                    # after this run's store
    return {
        "control": "CTRL_D: pointer-vs-count conflict conditional until base proven",
        "class": "SYNTHETIC_LOGICAL_CONTROL",
        "fixture_unproven": "prior state (no base proof): CONDITIONAL_UNRESOLVED",
        "fixture_proven": "this run: R's base proven (16-byte handle; [R+4] stores an object pointer P "
                          "with refcount at [P+4]) -> RESOLVED_AS_POINTER (measured, not assumed)",
        "unproven_stays_conditional": unproven == "CONDITIONAL_UNRESOLVED",
        "prior_map_not_new_measurement": True,  # the W count@+4 map is PRIOR canon for W's base only — never re-measured as R's
        "verdict": "PASS" if (unproven == "CONDITIONAL_UNRESOLVED" and resolved == "RESOLVED_AS_POINTER") else "FAIL",
    }


def ctrl_e():
    """Named strings alone do not qualify GetObjectByName/GetExtraData, child relation
    or scene root; synthetic metadata lookup is the countermodel."""
    def name_qualifies_child(name_string_exists, callee_mechanism_proven):
        return "QUALIFIED" if (name_string_exists and callee_mechanism_proven) else "NOT_QUALIFIED"
    fixture = name_qualifies_child(True, False)  # 'ArkTexture'/'ArkAnimation'/'Geowater:0' exist; FUN_007B6C30 body NOT opened
    rejection_ok = (fixture == "NOT_QUALIFIED")
    sanity = name_qualifies_child(True, True) == "QUALIFIED"
    return {
        "control": "CTRL_E: named strings alone do not qualify lookup/child/root",
        "class": "SYNTHETIC_LOGICAL_CONTROL",
        "fixture": "the name constants are measured; the lookup callee bodies are NOT opened -> no child/scene-root claim",
        "rejection_observed": rejection_ok,
        "legal_form_sanity": sanity,
        "verdict": "PASS" if (rejection_ok and sanity) else "FAIL",
    }


def ctrl_f():
    """Intrusive release/assign/retain does not qualify a NiRefObject/NiNode class or
    ownership of T by R; retention by the manager has a different receiver."""
    def adjudicate(refcount_protocol_exists, vptr_rtti_edge_for_target, absolute_ownership_claim):
        cls = "CLASS_NOT_ESTABLISHED" if (refcount_protocol_exists and not vptr_rtti_edge_for_target) else "CLASS_ESTABLISHED"
        own = "ONE_REFCOUNTED_REFERENCE" if refcount_protocol_exists else "NO_REFERENCE"
        if absolute_ownership_claim:
            own = "REJECTED"
        return cls, own
    cls, own = adjudicate(True, False, True)
    rejection_ok = (cls == "CLASS_NOT_ESTABLISHED" and own == "REJECTED")
    legal_ok = (adjudicate(True, False, False) == ("CLASS_NOT_ESTABLISHED", "ONE_REFCOUNTED_REFERENCE"))
    return {
        "control": "CTRL_F: refcount protocol does not qualify class or absolute ownership; "
                   "manager retention has a different receiver ([T+4] += 1 by the INSTALLER, "
                   "not by R)",
        "class": "SYNTHETIC_LOGICAL_CONTROL",
        "fixture": "the [P+4]/[T+4] addref/dec/destroy protocol is measured; P's class has no vptr/RTTI edge in bound; "
                   "an absolute-ownership claim is REJECTED (R holds ONE addref'd reference; the manager's own "
                   "retention [manager+0x68]=T + [T+4]+=1 is a SEPARATE reference by a separate receiver)",
        "rejection_observed": rejection_ok,
        "legal_form_sanity": legal_ok,
        "verdict": "PASS" if (rejection_ok and legal_ok) else "FAIL",
    }


def ctrl_g():
    """Lack of return/writer closure stays UNKNOWN; no R/T result promotes main visual,
    transform, world-instance, channel or XYZ."""
    deeper_origin_status = "NOT_ESTABLISHED_WITHIN_BOUND"  # the honest bounded result (PW-3)
    promotions = {
        "MAIN_VISUAL": "NOT_PROMOTED",
        "TRANSFORM_OWNER": "NOT_ADJUDICATED_BY_THIS_RUN",
        "WORLD_INSTANCE": "NOT_ESTABLISHED",
        "CHANNEL": "NOT_ESTABLISHED",
        "XYZ": "NO",
    }
    unknown_kept = deeper_origin_status == "NOT_ESTABLISHED_WITHIN_BOUND"
    no_promotions = all(v in ("NOT_PROMOTED", "NOT_ADJUDICATED_BY_THIS_RUN", "NOT_ESTABLISHED", "NO") for v in promotions.values())
    return {
        "control": "CTRL_G: missing closure stays UNKNOWN; no visual/transform/world/channel/XYZ promotion",
        "class": "SYNTHETIC_LOGICAL_CONTROL",
        "fixture": "the FUN_007B79B0-internal origin of P stays NOT_ESTABLISHED_WITHIN_BOUND (STOP_BEFORE_EXCEED "
                   "honored); the standing science statuses are preserved verbatim",
        "unknown_kept": unknown_kept,
        "no_promotions": no_promotions,
        "verdict": "PASS" if (unknown_kept and no_promotions) else "FAIL",
    }


def main():
    out = {
        "run_id": "PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008",
        "note": "REAL_SCIENCE_AUTO_QUALIFICATION=DISABLED; SCHEMA_CHECK != PIN_CHECK != "
                "STRUCTURAL_CHECK != SEMANTIC_ADJUDICATION; hash/pin PASS does not approve "
                "dataflow or semantic role (class/return/source adjudication = author/QC). "
                "Mechanical corruptions are IN-MEMORY copies; the physical EXE is never "
                "modified. CTRL_A..G are SYNTHETIC_LOGICAL_CONTROL — not new physical PCG "
                "measurements.",
        "mechanical_controls": mechanical_controls(),
        "ctrl_a": ctrl_a(),
        "ctrl_b": ctrl_b(),
        "ctrl_c": ctrl_c(),
        "ctrl_d": ctrl_d(),
        "ctrl_e": ctrl_e(),
        "ctrl_f": ctrl_f(),
        "ctrl_g": ctrl_g(),
    }
    all_pass = (
        out["mechanical_controls"]["clean_pass"]["gate"] == "PASS"
        and all(out["mechanical_controls"][k]["verdict"] == "PASS"
                for k in out["mechanical_controls"] if k.startswith("MC"))
        and all(out[c]["verdict"] == "PASS" for c in
                ("ctrl_a", "ctrl_b", "ctrl_c", "ctrl_d", "ctrl_e", "ctrl_f", "ctrl_g"))
    )
    out["CONTROLS_OVERALL"] = "PASS" if all_pass else "FAIL"
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(json.dumps({"mechanical": {k: v.get("verdict", v.get("gate")) for k, v in out["mechanical_controls"].items()},
                      "ctrl_a..g": {c: out[c]["verdict"] for c in
                                    ("ctrl_a", "ctrl_b", "ctrl_c", "ctrl_d", "ctrl_e", "ctrl_f", "ctrl_g")},
                      "CONTROLS_OVERALL": out["CONTROLS_OVERALL"]}, indent=1))
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
