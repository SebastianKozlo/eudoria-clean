"""qc_controls.py — the four contract §9 controls.

Each control runs ONE mechanical checker over:
  (a) the CLEAN case (the real measured values, or a synthetic fixture marked
      SYNTHETIC_MACHINERY_TEST_ONLY for the machinery test), expecting PASS, and
  (b) the MUTATED case (the specific relation broken), expecting FAIL,
with the same checker, the same range, and the cause recorded. No new EXE fields
or objects are searched; no analysis beyond the persisted records of this run.
All reads are fail-closed through the pinned EXE reader (pe_reader, scratch).
"""
import json
import sys

sys.path.insert(0, r"C:\Users\User\AppData\Local\Temp\opencode\PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007")
sys.path.insert(0, r"C:\Users\User\AppData\Local\Temp\opencode\PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007\capstone_lib")

import capstone
from pe_reader import PE_OBJ

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = True

OUT = {}


def disasm(va, n):
    code = PE_OBJ.read(va, n)
    return list(md.disasm(code, va))


# ---------------------------------------------------------------- CTRL_1
# Visual-role classifier (the §6 evidence legs). The same checker is used for
# the clean fixture, the mutated (NiControllerSequence model-adjacency-only)
# case, and the REAL CAND-4 child evidence set.
def ctrl1_visual_role(ev):
    """Return (main_visual_confirmed:boolean, reason:str). CONFIRMED_MAIN_VISUAL_ROOT requires
    resource-derived contained model AND typed containment AND exact-wrapper-as-child AND a
    positive principal-visual consumer/choice/install/storage proof. Adjacency alone never
    qualifies (contract §9.1: the pinned NiControllerSequence is not main visual by adjacency)."""
    legs = {
        "resource_derived_contained_model": ev.get("resource_derived_contained_model", False),
        "typed_containment": ev.get("typed_containment", False),
        "exact_wrapper_used_as_child": ev.get("exact_wrapper_used_as_child", False),
        "positive_consumer_proof": ev.get("positive_consumer_proof", False),
    }
    adj_only = ev.get("model_adjacency_only", False)
    if adj_only and not all(legs.values()):
        return False, "REJECT_MODEL_ADJACENCY_ONLY: NiControllerSequence/sequence-control adjacency does not qualify as main visual (contract §9.1)"
    if all(legs.values()):
        return True, "all four §6 legs present"
    missing = [k for k, v in legs.items() if not v]
    return False, "missing §6 proof legs: " + ",".join(missing)


clean1 = {"resource_derived_contained_model": True, "typed_containment": True,
          "exact_wrapper_used_as_child": True, "positive_consumer_proof": True,
          "synthetic": "SYNTHETIC_MACHINERY_TEST_ONLY"}
mut1 = {"model_adjacency_only": True, "object_class": "NiControllerSequence",
        "prior_pin": "source-run CH3 canon: the named 0x110 object of instance creator FUN_006CB6F0 (NiControllerSequence per the R2 adjudication)",
        "synthetic": "SYNTHETIC_MACHINERY_TEST_ONLY"}
real1 = {"resource_derived_contained_model": True, "typed_containment": False,
         "exact_wrapper_used_as_child": False, "positive_consumer_proof": False,
         "note": "the REAL CAND-4 child evidence of THIS run (CL-07/CL-10/CL-11)"}
r_clean1 = ctrl1_visual_role(clean1)
r_mut1 = ctrl1_visual_role(mut1)
r_real1 = ctrl1_visual_role(real1)
OUT["CTRL_1"] = {
    "checker": "ctrl1_visual_role (the §6 evidence-leg classifier; one code path for clean/mutated/real)",
    "clean_case": {"input": clean1, "result": "PASS" if r_clean1[0] else "FAIL", "detail": r_clean1[1]},
    "mutated_case": {"input": mut1, "result": "PASS" if r_mut1[0] else "FAIL",
                     "expected": "FAIL",
                     "detail": r_mut1[1],
                     "cause": "the adjacency-only mutation removed every §6 proof leg; the predicate did not survive"},
    "real_input_case": {"input": real1, "result": "PASS" if r_real1[0] else "FAIL",
                        "detail": r_real1[1],
                        "classification": "POLICY_ONLY — the REAL child is not confirmed main-visual by ABSENCE of the §6 proof legs (evidence-absence), not by detection of a specific defect; recorded per contract §9 (no detection claim)"},
    "verdict": "PASS" if (r_clean1[0] and not r_mut1[0]) else "FAIL",
    "range": "same checker; same §6 leg set; clean fixture vs adjacency-only mutation vs the real child evidence",
}

# ---------------------------------------------------------------- CTRL_2
# Wrapper/containment relation checker: the writer's store must target the declared
# field of the wrapper AND draw its value from the declared instance-field read.
def ctrl2_containment(store_bytes_va, expect_store_off, read_bytes_va, expect_read_off):
    store_ins = disasm(store_bytes_va, 3)[0]
    read_ins = disasm(read_bytes_va, 3)[0]
    store_ops = store_ins.op_str.replace("dword ptr ", "")
    read_ops = read_ins.op_str.replace("dword ptr ", "")
    # capstone 5.0.7 prints small offsets without the 0x prefix ("[esi + 0x68]" vs "[eax + 4]")
    store_ok = store_ins.mnemonic == "mov" and (
        f"[esi + 0x{expect_store_off:x}]" in store_ops or f"[esi + {expect_store_off}]" in store_ops)
    read_ok = read_ins.mnemonic == "mov" and (
        f"[eax + 0x{expect_read_off:x}]" in read_ops or f"[eax + {expect_read_off}]" in read_ops)
    return store_ok and read_ok, f"store '{store_ins.mnemonic} {store_ops}' ok={store_ok}; read '{read_ins.mnemonic} {read_ops}' ok={read_ok}"


ok_clean2, det_clean2 = ctrl2_containment(0x006C67E2, 0x68, 0x006C67BE, 0x4)
ok_mut2, det_mut2 = ctrl2_containment(0x006C7008, 0x68, 0x006C67BE, 0x4)  # mutated: the +0x6C store (real EXE bytes of the OTHER manager field) as the "wrapper" store
OUT["CTRL_2"] = {
    "checker": "ctrl2_containment (store-offset == declared child-field offset AND source-read == declared instance-field offset; one code path)",
    "clean_case": {"store_va": "0x006C67E2", "read_va": "0x006C67BE",
                   "result": "PASS" if ok_clean2 else "FAIL", "detail": det_clean2},
    "mutated_case": {"store_va": "0x006C7008",
                     "mutation": "the containment relation broken: the producer's [+0x6C] instance-cache store (real EXE bytes of a DIFFERENT manager field) substituted as the child-field store",
                     "result": "PASS" if ok_mut2 else "FAIL",
                     "expected": "FAIL",
                     "detail": det_mut2,
                     "cause": "the store offset no longer matches the declared +0x68 containment field"},
    "verdict": "PASS" if (ok_clean2 and not ok_mut2) else "FAIL",
    "range": "same checker; same 3-byte instruction range class (89/8B stores/loads); clean = the measured writer pair; mutated = the foreign-field store",
}

# ---------------------------------------------------------------- CTRL_3
# Wrong-manager-field checker: the provenance predicate binds the GETTER's field
# offset to the PRODUCER's written field offset. Correct bytes of a foreign field
# must NOT qualify as provenance of THIS getter.
GETTER_VA = 0x006C66D0
def ctrl3_provenance(getter_va):
    ins = disasm(getter_va, 8)[0]
    op = ins.op_str.replace("dword ptr ", "")
    if ins.mnemonic != "mov" or "[ecx + 0x68]" not in op:
        return False, f"accessor '{ins.mnemonic} {op}' does not read [ecx+0x68]"
    return True, f"accessor reads {op} == the producer-written field"


ok_clean3, det_clean3 = ctrl3_provenance(GETTER_VA)
# mutated accessor: real EXE bytes of a DIFFERENT manager-field accessor (the
# [+0x6C]-region accessor family does not exist verbatim; use the REAL [+0x120]
# getter FUN_006C0EE0 as the foreign-field accessor — its bytes are REAL EXE
# bytes of a foreign field of the same class family).
ok_mut3, det_mut3 = ctrl3_provenance(0x006C0EE0)
OUT["CTRL_3"] = {
    "checker": "ctrl3_provenance (getter field offset == producer-written offset 0x68; one code path)",
    "clean_case": {"accessor_va": "0x006C66D0", "result": "PASS" if ok_clean3 else "FAIL", "detail": det_clean3},
    "mutated_case": {"accessor_va": "0x006C0EE0",
                     "mutation": "the accessor substituted with the REAL EXE bytes of a foreign manager field ([+0x120] getter of the same class family)",
                     "result": "PASS" if ok_mut3 else "FAIL",
                     "expected": "FAIL",
                     "detail": det_mut3,
                     "cause": "correct bytes of a foreign field do not qualify as provenance of THIS getter (+0x68)"},
    "verdict": "PASS" if (ok_clean3 and not ok_mut3) else "FAIL",
    "range": "same checker; same accessor instruction shape; clean = the real getter; mutated = the real foreign-field accessor",
}

# ---------------------------------------------------------------- CTRL_4
# Child-identity preservation checker over the §7 caller window: the chain is
# INTACT iff (mov edi,eax @0x0050A3B7) AND (no EDI-WRITING instruction between
# 0x0050A3B7 and 0x0050A3F6) AND (push edi @0x0050A3F6). An injected EDI clobber
# must break CONFIRMED.
WIN_VA, WIN_LEN = 0x0050A3B7, 0x42  # 0x0050A3B7..0x0050A3F8
def ctrl4_preservation(window_bytes, base_va):
    ins_list = list(md.disasm(bytes(window_bytes), base_va))
    if not ins_list:
        return False, "window not decodable"
    first = ins_list[0]
    if not (first.mnemonic == "mov" and "edi, eax" in first.op_str):
        return False, f"chain head missing (got '{first.mnemonic} {first.op_str}')"
    edi_write = None
    push_edi = False
    for ins in ins_list[1:]:
        if ins.mnemonic == "push" and ins.op_str == "edi":
            push_edi = True
            continue
        # any instruction that WRITES edi (reg_write set contains EDI and it is a destination)
        try:
            if ins.regs_write and capstone.x86.X86_REG.EDI in ins.regs_write:
                edi_write = f"0x{ins.address:08x} {ins.mnemonic} {ins.op_str}"
        except Exception:
            pass
        if ins.mnemonic in ("mov", "lea", "pop", "xor", "add", "sub") and ins.op_str.startswith("edi"):
            edi_write = edi_write or f"0x{ins.address:08x} {ins.mnemonic} {ins.op_str}"
    if edi_write:
        return False, f"EDI clobbered at {edi_write}"
    if not push_edi:
        return False, "push edi @0x0050A3F6 missing"
    return True, "chain intact: mov edi,eax; no EDI write before push edi; push edi present"


clean_bytes = bytearray(PE_OBJ.read(WIN_VA, WIN_LEN))
ok_clean4, det_clean4 = ctrl4_preservation(clean_bytes, WIN_VA)
# mutated: inject a synthetic EDI clobber at 0x0050A3DD (the mov ecx,[esi+0x8C] slot):
# replace 6 bytes with 'mov edi, dword ptr [0xB9D8D0]' (8B 3D D0 D8 B9 00) — SYNTHETIC mutation
mut_bytes = bytearray(PE_OBJ.read(WIN_VA, WIN_LEN))
off = 0x0050A3DD - WIN_VA
mut_bytes[off:off + 6] = bytes([0x8B, 0x3D, 0xD0, 0xD8, 0xB9, 0x00])
ok_mut4, det_mut4 = ctrl4_preservation(mut_bytes, WIN_VA)
OUT["CTRL_4"] = {
    "checker": "ctrl4_preservation (§7 chain intactness: head move + no EDI-writing instruction + push edi; one code path)",
    "clean_case": {"window": "0x0050A3B7..0x0050A3F8 (the measured §7 window; free re-pin)",
                   "result": "PASS" if ok_clean4 else "FAIL", "detail": det_clean4},
    "mutated_case": {"window": "same window with a SYNTHETIC EDI clobber injected at 0x0050A3DD (8B 3D D0 D8 B9 00)",
                     "result": "PASS" if ok_mut4 else "FAIL",
                     "expected": "FAIL",
                     "detail": det_mut4,
                     "cause": "an EDI-writing instruction between the head move and push edi breaks the return->final-child relation; CHILD_TO_JOIN_IDENTITY cannot remain CONFIRMED"},
    "verdict": "PASS" if (ok_clean4 and not ok_mut4) else "FAIL",
    "range": "same checker; same window range; clean = the real measured bytes; mutated = the same bytes with the injected clobber",
    "note": "the REAL chain is reported at STRONGLY_SUPPORTED (CL-12): the checker's clean PASS covers the CALLER side only; the four intervening callee bodies remain NOT_CHECKED (ABI support, not proof)",
}

# ---------------------------------------------------------------- summary
OUT["SUMMARY"] = {
    "CTRL_1_RESULT": OUT["CTRL_1"]["verdict"],
    "CTRL_2_RESULT": OUT["CTRL_2"]["verdict"],
    "CTRL_3_RESULT": OUT["CTRL_3"]["verdict"],
    "CTRL_4_RESULT": OUT["CTRL_4"]["verdict"],
    "all_four_machinery_controls": (
        "PASS" if all(OUT[c]["verdict"] == "PASS" for c in ("CTRL_1", "CTRL_2", "CTRL_3", "CTRL_4")) else "FAIL"),
    "scope_note": "machinery falsifiability only — SYNTHETIC PASS is not PCG science; no new EXE fields/objects were searched for the controls; the real-input classifications (incl. the POLICY_ONLY note) are recorded per case",
    "decoder": "capstone 5.0.7 (cs_version (5,0,1280)); pinned EXE fail-closed reads",
}

with open(r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007\CONTROL_RESULTS.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(OUT, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(json.dumps(OUT["SUMMARY"], indent=2))
