#!/usr/bin/env python3
# CM-1 — escaped-local countermodel (three cases)
# Run: PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009, Work Package A.
#
# LABEL: LOGICAL_COUNTERMODEL_REPRODUCTION — NOT actual execution of FUN_006C2E00.
# NO callback/helper body was opened. This is an independently written short Python
# logic demonstration reproducing the logical countermodel supplied in
# C:\Users\User\Documents\ChatGPT\PE\PE_TEMPLATE_FINAL_CONSUMER_DESKTOP_POST_AUDIT_F99FEBE_20261009\CLAIM_SUFFICIENCY_COUNTERMODELS.json
# (group "escaped_local"; attribution to Desktop preserved). Expected values below
# are the Desktop-supplied constants.
#
# Modeled shape (all addresses/roles abstract; era PCG/EU 9.3.5, STATIC_ONLY context):
#   caller frame local pair at PAIR_PTR: [PAIR_PTR] = insert key, [PAIR_PTR+4] = LOCAL_1
#   LOCAL_1 receives the initial getter value ([P+8] initial read) at the save site.
#   fast path:        no helper call between save and reload -> later arg6 = LOCAL_1 as saved.
#   growth path:      the PAIR address escapes into the CLOSED helper before the reload.
#                     The stub helper honors the observable ABI conditions
#                     (callee-saved registers preserved; expected stack cleanup preserved)
#                     and MAY or MAY NOT write through the escaped address.
#   later arg6  = re-read of LOCAL_1 after the path.

import json

# --- Desktop-supplied expected constants (CLAIM_SUFFICIENCY_COUNTERMODELS.json) ---
EXP_INITIAL_GETTER = 305419896            # 0x12345678
EXP_PAIR_PTR = 0x0010000C                 # "0x10000c"
EXP_LATER_ARG6 = {"FAST_PATH": 305419896,
                  "GROWTH_PRESERVES_LOCAL": 305419896,
                  "GROWTH_MUTATES_ESCAPED_LOCAL": 2271560481}   # 0x87654321
EXP_EQUAL_INITIAL = {"FAST_PATH": True,
                     "GROWTH_PRESERVES_LOCAL": True,
                     "GROWTH_MUTATES_ESCAPED_LOCAL": False}

NONVOLATILE = ("ebx", "esi", "edi", "ebp")   # x86 callee-saved class
DERIVED_GROWTH_CLEANUP_BYTES = 20            # frame-balance-derived callee cleanup (5 args)


def stub_closed_growth_helper(mem, regs, pair_ptr, mutate_local):
    """Models a possible FUN_006C2E00 behavior honoring the observable ABI.

    Receives the ESCAPED pair address (an argument passed by the caller).
    Reads the pair (as an append would); optionally writes through it.
    Preserves all callee-saved registers and cleans exactly the expected bytes.
    """
    saved = {r: regs[r] for r in NONVOLATILE}          # prologue: save nonvolatile regs
    _key = mem[pair_ptr]                                # helper reads the pair (append input)
    _val = mem[pair_ptr + 4]
    if mutate_local:                                    # helper MAY write the escaped local
        mem[pair_ptr + 4] = 2271560481
    for r in NONVOLATILE:                               # epilogue: restore nonvolatile regs
        regs[r] = saved[r]
    return DERIVED_GROWTH_CLEANUP_BYTES                # RET imm16-style callee cleanup


def run_case(case):
    mem = {EXP_PAIR_PTR: 0x66, EXP_PAIR_PTR + 4: 0}    # LOCAL_2 (key), LOCAL_1
    regs = {r: 0xA000 + i for i, r in enumerate(NONVOLATILE)}
    regs_before = dict(regs)

    # save site: initial getter value stored into LOCAL_1
    mem[EXP_PAIR_PTR + 4] = EXP_INITIAL_GETTER
    stack_depth = 0

    if case == "FAST_PATH":
        pass                                            # no helper call on the fast path
    else:
        # growth path: caller pushes 5 dword args (incl. the ESCAPED pair address)
        stack_depth += 5 * 4
        cleanup = stub_closed_growth_helper(mem, regs, EXP_PAIR_PTR,
                                            mutate_local=(case == "GROWTH_MUTATES_ESCAPED_LOCAL"))
        stack_depth -= cleanup                          # callee-cleans per derived balance

    # reload site: later arg6 = re-read of LOCAL_1
    later_arg6 = mem[EXP_PAIR_PTR + 4]

    return {
        "case": case,
        "initial_getter_value": EXP_INITIAL_GETTER,
        "pair_pointer": hex(EXP_PAIR_PTR),
        "later_arg6": later_arg6,
        "equal_initial": later_arg6 == EXP_INITIAL_GETTER,
        "stub_preserves_nonvolatile_registers": all(regs[r] == regs_before[r] for r in NONVOLATILE),
        "stub_preserves_expected_stack_cleanup": stack_depth == 0,
    }


def main():
    cases = ["FAST_PATH", "GROWTH_PRESERVES_LOCAL", "GROWTH_MUTATES_ESCAPED_LOCAL"]
    results, all_ok = [], True
    for c in cases:
        r = run_case(c)
        ok = (r["later_arg6"] == EXP_LATER_ARG6[c]
              and r["equal_initial"] == EXP_EQUAL_INITIAL[c]
              and r["stub_preserves_nonvolatile_registers"] is True
              and r["stub_preserves_expected_stack_cleanup"] is True)
        r["matches_desktop_expected"] = ok
        all_ok = all_ok and ok
        results.append(r)
    out = {
        "countermodel_id": "CM-1_ESCAPED_LOCAL",
        "label": "LOGICAL_COUNTERMODEL_REPRODUCTION - NOT actual execution of FUN_006C2E00; NO callback/helper body opened",
        "source": "Desktop CLAIM_SUFFICIENCY_COUNTERMODELS.json group 'escaped_local' (attribution preserved)",
        "cases": results,
        "ALL_CASES_REPRODUCED": all_ok,
    }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
