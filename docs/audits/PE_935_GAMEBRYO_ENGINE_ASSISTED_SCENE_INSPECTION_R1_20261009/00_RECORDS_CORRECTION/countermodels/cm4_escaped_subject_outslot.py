#!/usr/bin/env python3
# CM-4 — escaped subject out-slot countermodel
# Run: PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009, Work Package A.
#
# LABEL: LOGICAL_COUNTERMODEL_REPRODUCTION — NOT actual execution of FUN_006C2E00.
# NO callback/helper body was opened. Independently written short Python logic
# demonstration reproducing the logical countermodel supplied in
# C:\Users\User\Documents\ChatGPT\PE\PE_TEMPLATE_FINAL_CONSUMER_DESKTOP_POST_AUDIT_F99FEBE_20261009\CLAIM_SUFFICIENCY_COUNTERMODELS.json
# (group "escaped_subject_outslot"; attribution to Desktop preserved). Expected
# values below are the Desktop-supplied constants.
#
# Modeled shape (subject FUN_006C3640, growth path): the subject computes the
# address of its OWN arg1 slot (entry_offset 4; LEA @0x006C367C) and passes it to
# the CLOSED growth helper; a stub helper may rewrite that slot through the
# escaped pointer; the subject's LATE read (@0x006C3691) then loads whatever is
# in the slot, and the final store *arg1 := container (@0x006C3695) writes
# through the RE-READ pointer. Reloading the slot after the call does not
# establish preservation of its initial contents.

import json

# --- Desktop-supplied expected constants (CLAIM_SUFFICIENCY_COUNTERMODELS.json) ---
EXP_INITIAL_OUT_POINTER = 5242880        # 0x500000
EXP_STUB_REWRITTEN = 6291456             # 0x600000
EXP_LEA_ENTRY_OFFSET = 4

NONVOLATILE = ("ebx", "esi", "edi", "ebp")
ARG1_SLOT_ENTRY_OFFSET = 4               # the subject's own arg1 slot (entry [esp+4])
FRAME_BASE = 0x00200000
ARG1_SLOT_ADDR = FRAME_BASE + ARG1_SLOT_ENTRY_OFFSET


def stub_closed_growth_helper(mem, regs, out_slot_addr):
    """Models a possible FUN_006C2E00 behavior honoring the observable ABI.

    Receives the ESCAPED &arg1 address (helper arg3 in the real call setup).
    Writes a different out-pointer through it, preserving callee-saved registers
    and the expected stack cleanup.
    """
    saved = {r: regs[r] for r in NONVOLATILE}
    mem[out_slot_addr] = EXP_STUB_REWRITTEN              # write through the escaped pointer
    for r in NONVOLATILE:
        regs[r] = saved[r]
    return 20                                            # derived callee cleanup preserved


def main():
    mem = {ARG1_SLOT_ADDR: EXP_INITIAL_OUT_POINTER}      # arg1 slot holds the initial out-pointer
    regs = {r: 0xB000 + i for i, r in enumerate(NONVOLATILE)}
    regs_before = dict(regs)

    lea_entry_offset = ARG1_SLOT_ADDR - FRAME_BASE       # = 4 (the LEA's entry offset)
    escaped = True                                       # the slot address IS passed to the helper
    cleanup = stub_closed_growth_helper(mem, regs, ARG1_SLOT_ADDR)

    # the subject's late read (mov eax,[esp+0x14]) loads the CURRENT slot contents
    late_read = mem[ARG1_SLOT_ADDR]
    # the final store (*arg1 := container) goes through the RE-READ pointer
    late_store_destination = late_read

    initial_pointer_preservation = (late_read == EXP_INITIAL_OUT_POINTER)
    ok = (lea_entry_offset == EXP_LEA_ENTRY_OFFSET
          and escaped
          and late_read == EXP_STUB_REWRITTEN
          and late_store_destination == EXP_STUB_REWRITTEN
          and initial_pointer_preservation is False
          and all(regs[r] == regs_before[r] for r in NONVOLATILE)
          and cleanup == 20)
    out = {
        "countermodel_id": "CM-4_ESCAPED_SUBJECT_OUTSLOT",
        "label": "LOGICAL_COUNTERMODEL_REPRODUCTION - NOT actual execution of FUN_006C2E00; NO callback/helper body opened",
        "source": "Desktop CLAIM_SUFFICIENCY_COUNTERMODELS.json group 'escaped_subject_outslot' (attribution preserved)",
        "subject_arg1_slot_escapes": escaped,
        "lea_006C367C_entry_offset": lea_entry_offset,
        "initial_out_pointer": EXP_INITIAL_OUT_POINTER,
        "stub_rewritten_out_pointer": mem[ARG1_SLOT_ADDR],
        "late_store_destination": late_store_destination,
        "initial_pointer_preservation": initial_pointer_preservation,
        "abi_conditions_preserved": all(regs[r] == regs_before[r] for r in NONVOLATILE) and cleanup == 20,
        "matches_desktop_expected": ok,
        "interpretation": ("a closed helper receiving &arg1 can rewrite the slot without "
                           "violating the ABI; the subject's late read is byte-correct for "
                           "the CURRENT contents, and does not establish that the initial "
                           "out-pointer survived the helper"),
    }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
