#!/usr/bin/env python3
# QC-R3 Q2: DISCRIMINATING BRANCH-SELECTION DETECTOR (contract CORRECTION_RUN_CONTRACT.md §6).
# An executable in-memory reimplementation of FUN_0075F660's decoded control flow + the
# descriptor dataflow, driven by STATIC BYTES read through my own PE parser.
# Variants: (A) descriptor+0 = NULL; (B) descriptor+0 = NON-NULL (proven 0xBA937C state);
# (C) virtual slot +0x14 points to a synthetic different target.
# The validator must demonstrate PATH-SELECTION CHANGE detection across A/B/C, and must
# FAIL (detect) three mutant models that ignore non-NULL / predict fallback despite non-NULL /
# do not derive the virtual target from the vtable slot value.
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc3_pe32_x86 import PE32

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
QC_DIR = os.path.join(PKG, "04_QC", "QC_R3_DESKTOP_CORRECTION")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
pe = PE32(EXE)

# ---- static evidence, read from the physical EXE with my own parser (no executor code) ----
# Proven lazy-init store (byte-pinned @0x977A68): runtime [0x00BA937C] = vtable 0x00A9C670.
PROVEN_OBJECT_VA = 0x00BA937C
PROVEN_VTABLE_FROM_STORE_INSTRUCTION = 0x00A9C670  # immediate of MOV dword [0xBA937C],imm @0x977A68
SLOT_OFF = 0x14
# static vtable slot dword read from .rdata
STATIC_SLOT_DWORD = pe.u32_at_va(PROVEN_VTABLE_FROM_STORE_INSTRUCTION + SLOT_OFF)      # @0xA9C684
# RTTI identity of the reader object (vtable-4 -> COL -> TD -> name)
COL = pe.u32_at_va(PROVEN_VTABLE_FROM_STORE_INSTRUCTION - 4)
TD = pe.u32_at_va(COL + 0xC)
RTTI_NAME = pe.read_va(TD + 8, 48).split(b"\x00")[0].decode("ascii", "replace")
# fallback family targets from the dispatch fallback block (byte-pinned)
FALLBACK_ARRAY = 0x00412D80    # TEST byte [desc+0xc],1 != 0 path
FALLBACK_SCALAR = 0x004129C0   # TEST byte [desc+0xc],1 == 0 path

# reader-object vtable identity assertion (from static bytes)
identity = {
    "store_instruction_pinned": "MOV dword [0x00BA937C],0x00A9C670 @0x977A68 (bytes C7057C93BA0070C6A900, verified in Q1)",
    "runtime_objtable[0x00BA937C]_predicted": hex(PROVEN_VTABLE_FROM_STORE_INSTRUCTION),
    "static_slot_dword_va": hex(PROVEN_VTABLE_FROM_STORE_INSTRUCTION + SLOT_OFF),
    "static_slot_dword_value": hex(STATIC_SLOT_DWORD),
    "slot_dword_is_FUN_009777F0": STATIC_SLOT_DWORD == 0x009777F0,
    "rtti_col": hex(COL), "rtti_td": hex(TD), "rtti_name": RTTI_NAME,
    "rtti_is_ArkRTTraitsInt": RTTI_NAME == ".?AUArkRTTraitsInt@@",
}

# ---- my executable reimplementation of the decoded dispatch (FUN_0075f660) ----
def dispatch(descriptor, vtable_of_object, slot_value_of_vtable):
    """Faithful reimplementation of the decoded control flow:
    MOV ECX,[EAX] (desc+0); TEST ECX,ECX; JZ fallback; MOV EAX,[ECX] (vtable);
    MOV EAX,[EAX+0x14] (slot); CALL EAX.
    vtable_of_object: callable object->vtable ; slot_value_of_vtable: callable vtable->target."""
    obj = descriptor[0]                      # MOV ECX,dword ptr [EAX]
    if obj == 0:                             # TEST ECX,ECX ; JE 0x75F687
        # fallback block @0x75F687: TEST byte [desc+0xc],1 ; MOV EAX,[desc+4]
        if (descriptor[3] & 1) != 0:          # dword list index 3 == byte offset 0xC
            return ("FALLBACK", FALLBACK_ARRAY)
        return ("FALLBACK", FALLBACK_SCALAR)
    vtable = vtable_of_object(obj)           # MOV EAX,dword ptr [ECX]
    target = slot_value_of_vtable(vtable)    # MOV EAX,dword ptr [EAX+0x14]
    return ("VIRTUAL", target)               # CALL EAX

# the PROVEN world: object 0xBA937C -> vtable 0xA9C670 (lazy-init store), slot from static bytes
def proven_vtable_of_object(obj):
    assert obj == PROVEN_OBJECT_VA, "unexpected object"
    return PROVEN_VTABLE_FROM_STORE_INSTRUCTION

def static_slot_of_vtable(vt):
    return pe.u32_at_va(vt + SLOT_OFF)   # read the slot dword from the physical EXE

# ---- A/B/C variants ----
variants = {}

# (A) descriptor+0 = NULL  ->  the JZ IS taken -> FALLBACK (legal path; NOT invalid input)
desc_A = [0, 1, 0x15, 0xC0]                    # desc+0 NULL, +4 type, +8 field, +0xc flags (list index = byte offset//4)
variants["A_descriptor_null"] = dispatch(desc_A, proven_vtable_of_object, static_slot_of_vtable)

# (B) descriptor+0 = NON-NULL (the proven 0xBA937C state) -> VIRTUAL, target = static slot dword
desc_B = [PROVEN_OBJECT_VA, 1, 0x15, 0xC0]
variants["B_descriptor_nonnull_proven"] = dispatch(desc_B, proven_vtable_of_object, static_slot_of_vtable)

# (C) virtual slot +0x14 points to a SYNTHETIC different target -> prediction must change
SYNTHETIC_VTABLE = 0x00A79000  # a synthetic vtable VA inside the image; we patch its slot below
desc_C = [PROVEN_OBJECT_VA, 1, 0x15, 0xC0]
def synth_vtable_of_object(obj):
    return SYNTHETIC_VTABLE
def synth_slot_of_vtable(vt):
    # synthetic slot value, different from 0x009777F0
    return 0x00412540   # the old fallback reader address as the synthetic different target
variants["C_synthetic_slot_target"] = dispatch(desc_C, synth_vtable_of_object, synth_slot_of_vtable)

abc_table = {
    "A_descriptor_null": {"descriptor_plus_0": "NULL",
                          "predicted_kind": variants["A_descriptor_null"][0],
                          "predicted_target": hex(variants["A_descriptor_null"][1]),
                          "expected": "FALLBACK (FUN_00412d80/FUN_004129c0 family)"},
    "B_descriptor_nonnull_proven": {"descriptor_plus_0": "0x00BA937C (proven non-NULL)",
                                    "predicted_kind": variants["B_descriptor_nonnull_proven"][0],
                                    "predicted_target": hex(variants["B_descriptor_nonnull_proven"][1]),
                                    "expected": "VIRTUAL = static slot dword 0x009777F0 (FUN_009777F0)"},
    "C_synthetic_slot_target": {"descriptor_plus_0": "0x00BA937C (non-NULL)",
                                "vtable": "synthetic",
                                "predicted_kind": variants["C_synthetic_slot_target"][0],
                                "predicted_target": hex(variants["C_synthetic_slot_target"][1]),
                                "expected": "VIRTUAL = the SYNTHETIC slot value (0x00412540) - MUST differ from B"},
}

# ---- the DETECTOR: discrimination predicates (contract §6) ----
det = {}

# 1. path-selection change across A/B/C
det["A_is_fallback"] = variants["A_descriptor_null"] == ("FALLBACK", FALLBACK_SCALAR)  # 0xC0 & 1 == 0
det["B_is_virtual_0x9777F0"] = variants["B_descriptor_nonnull_proven"] == ("VIRTUAL", 0x009777F0)
det["C_target_changes_with_slot"] = (variants["C_synthetic_slot_target"][0] == "VIRTUAL"
                                     and variants["C_synthetic_slot_target"][1] != variants["B_descriptor_nonnull_proven"][1]
                                     and variants["C_synthetic_slot_target"][1] == 0x00412540)
det["A_vs_B_selection_change"] = variants["A_descriptor_null"][0] != variants["B_descriptor_nonnull_proven"][0]
det["B_vs_C_target_change"] = variants["B_descriptor_nonnull_proven"][1] != variants["C_synthetic_slot_target"][1]

# 2. mutant models the validator MUST detect (fail) - each mutant is a known-buggy reimplementation
mutants = {}
# mutant 1: descriptor non-NULL IGNORED (always takes the fallback)
def mutant_ignore_nonnull(descriptor, vt_of, slot_of):
    return ("FALLBACK", FALLBACK_SCALAR)
r = mutant_ignore_nonnull(desc_B, proven_vtable_of_object, static_slot_of_vtable)
mutants["M1_ignore_nonnull"] = {
    "predicted": [r[0], hex(r[1])],
    "detection": "DETECTED-SELECTION-ERROR" if r != ("VIRTUAL", 0x009777F0) else "NOT_DETECTED",
}
# mutant 2: fallback predicted despite the proven non-NULL (variant of M1 with flag-dependent fallback)
def mutant_fallback_despite_nonnull(descriptor, vt_of, slot_of):
    obj = descriptor[0]
    if obj == 0 or obj != 0:      # buggy: always fallback
        if (descriptor[3] & 1) != 0:
            return ("FALLBACK", FALLBACK_ARRAY)
        return ("FALLBACK", FALLBACK_SCALAR)
    return ("VIRTUAL", slot_of(vt_of(obj)))
r = mutant_fallback_despite_nonnull(desc_B, proven_vtable_of_object, static_slot_of_vtable)
mutants["M2_fallback_despite_nonnull"] = {
    "predicted": [r[0], hex(r[1])],
    "detection": "DETECTED-SELECTION-ERROR" if r != ("VIRTUAL", 0x009777F0) else "NOT_DETECTED",
}
# mutant 3: virtual target NOT derived from the vtable slot value (hard-coded 0x009777F0)
def mutant_hardcoded_target(descriptor, vt_of, slot_of):
    obj = descriptor[0]
    if obj == 0:
        return ("FALLBACK", FALLBACK_SCALAR if (descriptor[3] & 1) == 0 else FALLBACK_ARRAY)
    return ("VIRTUAL", 0x009777F0)   # ignores the actual slot value
r_C = mutant_hardcoded_target(desc_C, synth_vtable_of_object, synth_slot_of_vtable)
r_B = mutant_hardcoded_target(desc_B, proven_vtable_of_object, static_slot_of_vtable)
mutants["M3_hardcoded_slot_target"] = {
    "predicted_B": [r_B[0], hex(r_B[1])],
    "predicted_C": [r_C[0], hex(r_C[1])],
    "C_followed_synthetic_slot": r_C[1] == 0x00412540,
    "detection": "DETECTED-TARGET-NOT-DERIVED-FROM-SLOT" if r_C[1] != 0x00412540 else "NOT_DETECTED",
}
det["all_mutants_detected"] = (mutants["M1_ignore_nonnull"]["detection"] != "NOT_DETECTED"
                               and mutants["M2_fallback_despite_nonnull"]["detection"] != "NOT_DETECTED"
                               and mutants["M3_hardcoded_slot_target"]["detection"] != "NOT_DETECTED")

# 3. NULL is LEGAL input (the negative control must NOT insist NULL is invalid)
det["null_is_legal_fallback"] = variants["A_descriptor_null"][0] == "FALLBACK"

# 4. the proven-state prediction (the QC gate: fallback NOT selected for tag 17; virtual target proven)
det["tag17_selected_reader_is_FUN_009777F0"] = variants["B_descriptor_nonnull_proven"] == ("VIRTUAL", 0x009777F0)
det["tag17_fallback_NOT_selected"] = variants["B_descriptor_nonnull_proven"][0] != "FALLBACK"

# 5. reader-object vtable identity from static bytes
det["runtime_objtable_identity"] = (identity["runtime_objtable[0x00BA937C]_predicted"] == "0xa9c670"
                                     and identity["slot_dword_is_FUN_009777F0"]
                                     and identity["rtti_is_ArkRTTraitsInt"])

res = {
    "q": "Q2_branch_selection_model",
    "static_evidence": identity,
    "abc_table": abc_table,
    "detector": {k: bool(v) for k, v in det.items()},
    "mutant_models": mutants,
    "verdict": "PASS" if all([
        det["A_is_fallback"], det["B_is_virtual_0x9777F0"], det["C_target_changes_with_slot"],
        det["A_vs_B_selection_change"], det["B_vs_C_target_change"],
        det["all_mutants_detected"], det["null_is_legal_fallback"],
        det["tag17_selected_reader_is_FUN_009777F0"], det["tag17_fallback_NOT_selected"],
        det["runtime_objtable_identity"],
    ]) else "FAIL",
}
res["failed_predicates"] = [k for k, v in det.items() if not v]
out = os.path.join(QC_DIR, "QC_R3_BRANCH_MODEL_RESULT.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)
print(json.dumps({"abc_table": abc_table, "detector": res["detector"], "mutants": mutants,
                  "verdict": res["verdict"], "failed": res["failed_predicates"]}, indent=2))
