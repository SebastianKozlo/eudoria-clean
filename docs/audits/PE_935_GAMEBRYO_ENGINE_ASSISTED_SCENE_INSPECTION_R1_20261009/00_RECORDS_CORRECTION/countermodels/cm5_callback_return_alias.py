#!/usr/bin/env python3
# CM-5 — callback-return-aliases-receiver countermodel
# Run: PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009, Work Package A.
#
# LABEL: LOGICAL_COUNTERMODEL_REPRODUCTION — NOT actual execution of FUN_006C2E00
# (and NOT execution of the callback 0x008BD720). NO callback/helper body was
# opened. Independently written short Python logic demonstration of the alias
# mechanism described in Desktop REPORT.md section 3 (PE_TEMPLATE_FINAL_CONSUMER_
# DESKTOP_POST_AUDIT_F99FEBE_20261009): a hypothetical callback that returns its
# receiver makes the subject's later [EAX]/[EAX+4] reads touch the element that was
# previously only addressed via EDI. Expected shape pre-registered in this run's
# PREREGISTRATION.md (the concrete values are this run's own construction; the
# Desktop JSON supplies no numbers for this prose case).
#
# Modeled shape (subject FUN_006C3640, loop body): the element address reaches the
# callback as its thiscall receiver (ECX, from EDI). The census fact is that the
# subject window contains ZERO memory operands with EDI as base — the element is
# never dereferenced DIRECTLY. The callback's return EAX is then dereferenced
# ([EAX], [EAX+4]) and the pair is copied into the container. If the callback
# returns its receiver, those reads reach element memory through EAX.

import json

ELEMENT_ADDR = 0x00300000
ELEMENT_DWORDS = [0x11111111, 0x22222222]          # element's first two dwords
CONTAINER = []

# census fact modeled from the f99febe package (BODY_CFG_AND_ACCESS_CENSUS):
# tracked carriers EDI/EBP/EBX appear as memory bases 0 times in W-SUBJ
EXP_DIRECT_EDI_BASED_MEMORY_OPERANDS = 0


def stub_callback_returning_receiver(receiver_ecx):
    """Models a legitimate thiscall whose return value IS its receiver."""
    return receiver_ecx


def subject_loop_body(element_addr):
    direct_edi_based_memory_operands = 0            # census fact: no [EDI...] operand exists
    eax = stub_callback_returning_receiver(element_addr)      # CALL EBX -> EAX
    d0 = read_mem(eax)                              # [EAX]  @0x006C3668
    d1 = read_mem(eax + 4)                          # [EAX+4] @0x006C366C
    CONTAINER.append((d0, d1))                      # pair copied into the container
    return direct_edi_based_memory_operands, (d0, d1)


MEM = {ELEMENT_ADDR + 4 * i: v for i, v in enumerate(ELEMENT_DWORDS)}


def read_mem(addr):
    return MEM[addr]


def main():
    direct_ops, copied_pair = subject_loop_body(ELEMENT_ADDR)
    alias_route_read_element = (copied_pair == tuple(ELEMENT_DWORDS))
    ok = (direct_ops == EXP_DIRECT_EDI_BASED_MEMORY_OPERANDS and alias_route_read_element)
    out = {
        "countermodel_id": "CM-5_CALLBACK_RETURN_ALIASES_RECEIVER",
        "label": "LOGICAL_COUNTERMODEL_REPRODUCTION - NOT actual execution of FUN_006C2E00; NO callback/helper body opened",
        "source": "Desktop REPORT.md (PE_TEMPLATE_FINAL_CONSUMER_DESKTOP_POST_AUDIT_F99FEBE_20261009) section 3 prose shape; expected values pre-registered in this run's PREREGISTRATION.md",
        "direct_edi_based_memory_operands": direct_ops,
        "expected_direct_edi_based_memory_operands": EXP_DIRECT_EDI_BASED_MEMORY_OPERANDS,
        "callback_returned_receiver": True,
        "copied_pair_via_EAX_reads": ["0x%08x" % v for v in copied_pair],
        "element_first_two_dwords": ["0x%08x" % v for v in ELEMENT_DWORDS],
        "alias_route_read_element": alias_route_read_element,
        "matches_preregistered_expected": ok,
        "interpretation": ("zero DIRECT EDI-based memory operands does not prove the same "
                           "address is never read: with the callback returning its receiver, "
                           "the element memory IS read through EAX. The census stays valid "
                           "as a DIRECT-operand count; the absolute 'never dereferenced' "
                           "reading is not established"),
    }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
