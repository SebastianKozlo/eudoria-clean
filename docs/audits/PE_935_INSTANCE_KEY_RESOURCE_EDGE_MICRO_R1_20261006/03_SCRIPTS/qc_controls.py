# qc_controls.py - targeted QC controls for PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006.
# Contract s5 controls, all on the ACTUAL generated evidence, EXE never modified:
#   (a) MANDATORY: getter offset +0x74 -> +0x78 mutation WITHOUT changing the EXE
#       -> clean PASS -> mutated FAIL (two variants: byte-pin expectation +
#       semantic-decode claim).
#   (b) receiver/identity-edge removal: the ctor receiver chain gate
#       (MOV ESI,ECX prologue capture + ClientMovableObject vtable store +
#        MOV ECX,ESI re-establishment before the call) -> clean PASS ->
#        mutated-copy FAIL.
#   (c) resource-join negative on the REAL examined key-to-map operation
#       (FUN_00856190 insert): map-destination pins + ZERO resource-family E8s
#       in the decoded insert body + falsifier: injected fake E8->FUN_0072F580
#       in a mutated copy FLIPS the detector to FAIL.
# Plus: EXE identity re-verification at QC time; census recount; getter
# boundary re-read. Output: 01_RAW/QC_CONTROLS.json

import hashlib
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe935k_core import Exe, hexs, EXE_PATH, EXE_SHA256, EXE_SIZE_BYTES

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "01_RAW")

ex = Exe()
results = {"controls": [], "exe_identity": {}, "census_recount": {}}


def record(name, clean_pass, mutated_fail, details):
    results["controls"].append({
        "control": name,
        "clean_pass": bool(clean_pass),
        "mutated_fail": bool(mutated_fail),
        "verdict": "PASS" if (clean_pass and mutated_fail) else "FAIL",
        "details": details,
    })


# ---- EXE identity at QC time ----
with open(EXE_PATH, "rb") as f:
    raw_all = f.read()
sha = hashlib.sha256(raw_all).hexdigest().upper()
results["exe_identity"] = {
    "size": len(raw_all), "size_match": len(raw_all) == EXE_SIZE_BYTES,
    "sha256": sha, "sha_match": sha == EXE_SHA256,
}

# ---- census recount (independent re-enumeration) ----
t_lo, t_hi = ex.text_range()
o_lo = ex.va_to_off(t_lo)
tgt = 0x00414130
hits = 0
for o in range(o_lo, o_lo + (t_hi - t_lo) - 4):
    if ex.raw[o] == 0xE8:
        va = t_lo + (o - o_lo)
        rel = struct.unpack_from("<i", ex.raw, o + 1)[0]
        if (va + 5 + rel) & 0xFFFFFFFF == tgt:
            hits += 1
results["census_recount"] = {"e8_hits_targeting_getter": hits,
                             "expected_from_census": 6,
                             "match": hits == 6}

# ---- getter boundary re-read ----
gb = ex.read(0x00414130, 4)
after = ex.read(0x00414134, 8)
results["getter_boundary_reread"] = {
    "bytes": hexs(gb), "after_ret": hexs(after),
    "ret_is_c3": gb[3] == 0xC3, "padding_is_cc": all(b == 0xCC for b in after),
}

# ============ CONTROL (a): getter offset mutation +0x74 -> +0x78 ============
def pin_gate(expected_offset):
    """Byte-pin gate: EXE bytes at 0x00414130 must be 8B 41 <offset> C3."""
    b = ex.read(0x00414130, 4)
    return (b[0] == 0x8B and b[1] == 0x41 and b[2] == expected_offset and b[3] == 0xC3), hexs(b)


def semantic_gate(claimed_offset):
    """Semantic-decode gate: the decoded instruction must be mov eax,[ecx+claimed]; ret."""
    b = ex.read(0x00414130, 4)
    if not (b[0] == 0x8B and (b[1] >> 6) & 3 == 1 and ((b[1] >> 3) & 7) == 0 and (b[1] & 7) == 1):
        return False, "modrm mismatch"
    if b[2] != claimed_offset:
        return False, "disp8 mismatch: claimed 0x%02X, physical 0x%02X" % (claimed_offset, b[2])
    if b[3] != 0xC3:
        return False, "no ret"
    return True, "mov eax,[ecx+0x%02X]; ret" % b[2]


ok_clean, byts = pin_gate(0x74)
ok_mut, _ = pin_gate(0x78)
sem_clean, sem_msg_clean = semantic_gate(0x74)
sem_mut, sem_msg_mut = semantic_gate(0x78)
record(
    "CTRL_A_GETTER_OFFSET_MUTATION",
    ok_clean and sem_clean,
    (not ok_mut) and (not sem_mut),
    {
        "clean": "byte-pin PASS (%s) + semantic PASS (%s)" % (byts, sem_msg_clean),
        "mutated": "expected offset changed to +0x78 WITHOUT touching the EXE: "
                   "byte-pin %s + semantic %s (%s)" % (
                       "FAIL" if not ok_mut else "PASS(false-pass!)",
                       "FAIL" if not sem_mut else "PASS(false-pass!)", sem_msg_mut),
        "measured_quantity": "EXE bytes at VA 0x00414130",
        "independent_source_of_truth": "physical EXE file re-read by this gate",
        "why_non_circular": "the gate compares an INDEPENDENT expectation against the "
                            "physical bytes; the mutation changes only the expectation",
        "failure_case_detected": "if the physical byte at 0x00414132 were 0x78 (or the "
                                 "getter pin were wrong), the clean gate would already FAIL; "
                                 "the +0x78 mutated expectation FAILS against the true bytes",
        "coverage_limit": "covers the 4-byte getter pin only; not every consumer instruction",
    },
)

# ============ CONTROL (b): receiver/identity edge removal ============
# Claim: ECX at the getter call 0x00528FD9 == ESI == the ClientMovableObject ctor this.
# Essential identity edges (all byte-pinned in this run):
#   E1: 0x00528E76  8B F1             MOV ESI,ECX            (prologue this-capture)
#   E2: 0x00528EA2  C7 06 B0 DC A7 00 MOV [ESI],0x00A7DCB0   (CMO vtable store; RTTI-named)
#   E3: 0x00528FD2  8B CE             MOV ECX,ESI            (receiver re-establishment)
#   E4: 0x00528FD9  E8 52 B1 EE FF    CALL 0x00414130        (the call itself)

def receiver_gate(window):
    """window = dict VA->bytes; all four edges must hold."""
    checks = {
        "E1_mov_esi_ecx": window[0x00528E76] == bytes.fromhex("8BF1"),
        "E2_cmo_vtable_store": window[0x00528EA2] == bytes.fromhex("C706B0DCA700"),
        "E3_mov_ecx_esi": window[0x00528FD2] == bytes.fromhex("8BCE"),
        "E4_call_getter": window[0x00528FD9] == bytes.fromhex("E852B1EEFF"),
    }
    return all(checks.values()), checks


window_clean = {
    0x00528E76: ex.read(0x00528E76, 2),
    0x00528EA2: ex.read(0x00528EA2, 6),
    0x00528FD2: ex.read(0x00528FD2, 2),
    0x00528FD9: ex.read(0x00528FD9, 5),
}
ok_b, checks_clean = receiver_gate(window_clean)
# mutated copy: remove the receiver re-establishment edge (E3: MOV ECX,ESI ->
# MOV ECX,EBP) - in-memory only, EXE untouched
window_mut = dict(window_clean)
window_mut[0x00528FD2] = bytes.fromhex("8BCD")
ok_b_mut, checks_mut = receiver_gate(window_mut)
record(
    "CTRL_B_RECEIVER_IDENTITY_EDGE_REMOVAL",
    ok_b,
    not ok_b_mut,
    {
        "clean": "all four identity edges byte-pinned: %s" % checks_clean,
        "mutated": "edge E3 removed (mutated in-memory copy 8B CE -> 8B CD, EXE "
                   "untouched): gate checks %s -> gate FAIL (receiver no longer "
                   "proven == ctor this)" % checks_mut,
        "claim_that_depends": "the selected receiver-proven branch: ECX at "
                              "0x00528FD9 == the ClientMovableObject ctor this",
        "measured_quantity": "four byte-pinned identity edges of the receiver chain",
        "independent_source_of_truth": "physical EXE bytes at the four VAs",
        "why_non_circular": "the gate fails when any edge is absent or altered; the "
                            "mutation alters only the copied evidence",
        "failure_case_detected": "with E3 removed, the receiver claim FAILS (the "
                                 "essential edge is load-bearing)",
        "coverage_limit": "covers the ctor callsite receiver chain; not the "
                          "GameClient/other receivers",
    },
)

# ============ CONTROL (c): resource-join negative on the real key-to-map op ============
# FUN_00856190 body (0x00856190..0x00856210) is the REAL examined key-to-map
# operation. The negative: the key destination is the mgr1 identity hash_map,
# NOT a resource/template/model registry.
# Pins: P1 0x008561B8 8D 73 10      LEA ESI,[EBX+0x10]  (mgr1 map at this+0x10)
#       P2 0x008561C1 89 7C 24 14   MOV [ESP+0x14],EDI  (the pair value = the instance)
#       P3 the decoded body contains ZERO E8 calls into the resource family
#          {0x0072F580 template lookup, 0x006C9700 model pump, 0x006CB6F0 instance
#           creator, 0x006CB020 named-instance builder, 0x0043A550 registry getter}

BODY_LO, BODY_HI = 0x00856190, 0x00856210
RESOURCE_FAMILY = [0x0072F580, 0x006C9700, 0x006CB6F0, 0x006CB020, 0x0043A550]


def resource_join_negative(body_bytes):
    """Returns (map_pins_ok, resource_calls_found_list)."""
    pins_ok = (
        body_bytes[0x008561B8 - BODY_LO:0x008561BB - BODY_LO] == bytes.fromhex("8D7310")
        and body_bytes[0x008561C1 - BODY_LO:0x008561C5 - BODY_LO] == bytes.fromhex("897C2414")
    )
    found = []
    for o in range(0, len(body_bytes) - 4):
        if body_bytes[o] == 0xE8:
            va = BODY_LO + o
            rel = struct.unpack_from("<i", body_bytes, o + 1)[0]
            t = (va + 5 + rel) & 0xFFFFFFFF
            if t in RESOURCE_FAMILY:
                found.append((hex(va), hex(t)))
    return pins_ok, found


body = ex.read(BODY_LO, BODY_HI - BODY_LO)
pins_clean, res_clean = resource_join_negative(body)
neg_clean = pins_clean and (len(res_clean) == 0)
# falsifier: inject a fake E8 -> FUN_0072F580 into a mutated copy (in-memory)
body_mut = bytearray(body)
# falsifier injection site (honest description, record-repair F3): fake_at =
# len(body)-5 -> VA 0x0085620B, which OVERWRITES the live epilogue bytes
# 83 C4 10 C2 04 (ADD ESP,0x10; RET 4) of the in-memory copy — it is NOT padding
# and the copied body is NOT kept intact. This is acceptable for the control's
# purpose: the copy exists solely to exercise the E8-target detector on a
# demonstrably fake resource call; the physical EXE is untouched.
fake_at = len(body_mut) - 5
body_mut[fake_at] = 0xE8
fake_va = BODY_LO + fake_at
struct.pack_into("<i", body_mut, fake_at + 1, 0x0072F580 - (fake_va + 5))
pins_mut, res_mut = resource_join_negative(bytes(body_mut))
neg_mut_detect = (len(res_mut) == 1)  # the detector must find the injected call
record(
    "CTRL_C_RESOURCE_JOIN_NEGATIVE_KEY_TO_MAP",
    neg_clean,
    neg_mut_detect,
    {
        "clean": "map pins %s; resource-family E8 calls found in the decoded insert "
                 "body: %s (expected ZERO)" % (pins_clean, res_clean),
        "mutated": "falsifier: fake E8->FUN_0072F580 injected at 0x%08X in an "
                   "in-memory copy: detector found %s (expected the injected 1) "
                   "-> the detector demonstrably FAILs on a real resource join" % (
                       fake_va, res_mut),
        "real_examined_operation": "FUN_00856190 hash_map insert (mgr1+0x10 identity "
                                   "map, key=[value+0x74], value=the instance object)",
        "why_this_is_a_negative": "the examined key-to-map operation maps instance-key "
                                   "-> the SAME instance object (identity map; duplicate "
                                   "path calls the value's deleting dtor) - byte-distinct "
                                   "from the templates.vfs RB-tree registry (root "
                                   "0x00BA1824, FUN_0043A550/FUN_0072F580) - so the "
                                   "key-to-map join is NOT a resource join",
        "measured_quantity": "byte pins + E8 target census inside the insert body",
        "independent_source_of_truth": "physical EXE body bytes + the resource-family "
                                        "address list from BASE canon (read as input)",
        "why_non_circular": "the detector enumerates E8 targets directly; the falsifier "
                            "proves it detects an injected resource call",
        "failure_case_detected": "any real E8 into the resource family inside the insert "
                                 "body would flip clean PASS to FAIL",
        "coverage_limit": "covers the decoded insert body only; not other map operations",
    },
)

# ---- verdicts ----
all_pass = all(c["verdict"] == "PASS" for c in results["controls"])
results["overall"] = {
    "all_controls_pass": all_pass,
    "exe_identity_ok": results["exe_identity"]["size_match"] and results["exe_identity"]["sha_match"],
    "census_recount_ok": results["census_recount"]["match"],
    "getter_boundary_ok": results["getter_boundary_reread"]["ret_is_c3"] and results["getter_boundary_reread"]["padding_is_cc"],
}

with open(os.path.join(OUT, "QC_CONTROLS.json"), "w") as f:
    json.dump(results, f, indent=1)

print("EXE identity: size_match=%s sha_match=%s" % (
    results["exe_identity"]["size_match"], results["exe_identity"]["sha_match"]))
print("Census recount: %s (expected 6)" % hits)
print("Getter boundary: %s" % results["getter_boundary_reread"])
for c in results["controls"]:
    print("%s: clean_pass=%s mutated_fail=%s -> %s" % (
        c["control"], c["clean_pass"], c["mutated_fail"], c["verdict"]))
print("OVERALL: %s" % results["overall"])
