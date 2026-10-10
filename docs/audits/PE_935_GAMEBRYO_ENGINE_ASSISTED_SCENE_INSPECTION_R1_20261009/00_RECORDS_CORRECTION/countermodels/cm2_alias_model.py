#!/usr/bin/env python3
# CM-2 — alias countermodel (distinct producing chains, same address)
# Run: PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009, Work Package A.
#
# LABEL: LOGICAL_COUNTERMODEL_REPRODUCTION — NOT actual execution of FUN_006C2E00.
# NO callback/helper body was opened. Independently written short Python logic
# demonstration reproducing the logical countermodel supplied in
# C:\Users\User\Documents\ChatGPT\PE\PE_TEMPLATE_FINAL_CONSUMER_DESKTOP_POST_AUDIT_F99FEBE_20261009\CLAIM_SUFFICIENCY_COUNTERMODELS.json
# (group "alias_model"; attribution to Desktop preserved). Expected values below
# are the Desktop-supplied constants.
#
# Modeled shape: two DIFFERENT static producing chains (an incoming-argument load
# vs a lookup-call return) both resolve to the SAME address; the container-role
# fields (+4 cursor / +8 end) and the range-role fields (+0x14 begin / +0x18 end)
# are disjoint offsets, so one aliased object can serve both roles with no
# conflicting access in the examined window.

import json

# --- Desktop-supplied expected constants (CLAIM_SUFFICIENCY_COUNTERMODELS.json) ---
EXP_LOOKUP_RETURN = 2097152
EXP_INCOMING_CONTAINER = 2097152
EXP_FIELDS = {"+4_cursor": 3145728,
              "+8_capacity_end": 3145984,
              "+14_range_begin": 4194304,
              "+18_range_end": 4194336}


def producing_chain_incoming_param(incoming_slot_value):
    """Chain A (container): a load from the caller's incoming argument slot.

    Distinct static provenance: this chain never touches the lookup call.
    """
    return incoming_slot_value


def producing_chain_lookup_return(lookup_result_value):
    """Chain B (template pointer P): the return value of a lookup call.

    Distinct static provenance: this chain never touches the incoming slot.
    """
    return lookup_result_value


def main():
    # the two chains are statically distinct (different sources) ...
    chains_share_instructions = False

    container_addr = producing_chain_incoming_param(EXP_INCOMING_CONTAINER)
    template_addr = producing_chain_lookup_return(EXP_LOOKUP_RETURN)
    same_address = container_addr == template_addr

    # one object serves both roles at the same address
    obj = {4: EXP_FIELDS["+4_cursor"], 8: EXP_FIELDS["+8_capacity_end"],
           0x14: EXP_FIELDS["+14_range_begin"], 0x18: EXP_FIELDS["+18_range_end"]}

    container_role_reads = {off: obj[off] for off in (4, 8)}       # [esi+4]/[esi+8] role
    range_role_reads = {off: obj[off] for off in (0x14, 0x18)}     # [P+0x14]/[P+0x18] role

    disjoint_offsets = set(container_role_reads).isdisjoint(set(range_role_reads))
    fields_match_expected = (container_role_reads[4] == EXP_FIELDS["+4_cursor"]
                             and container_role_reads[8] == EXP_FIELDS["+8_capacity_end"]
                             and range_role_reads[0x14] == EXP_FIELDS["+14_range_begin"]
                             and range_role_reads[0x18] == EXP_FIELDS["+18_range_end"])

    ok = (same_address and disjoint_offsets and fields_match_expected
          and not chains_share_instructions)
    out = {
        "countermodel_id": "CM-2_ALIAS_MODEL",
        "label": "LOGICAL_COUNTERMODEL_REPRODUCTION - NOT actual execution of FUN_006C2E00; NO callback/helper body opened",
        "source": "Desktop CLAIM_SUFFICIENCY_COUNTERMODELS.json group 'alias_model' (attribution preserved)",
        "lookup_return": template_addr,
        "incoming_container": container_addr,
        "same_address": same_address,
        "producing_chains_statically_distinct": not chains_share_instructions,
        "compatible_field_example": {
            "+4_cursor": container_role_reads[4],
            "+8_capacity_end": container_role_reads[8],
            "+14_range_begin": range_role_reads[0x14],
            "+18_range_end": range_role_reads[0x18],
        },
        "field_offset_sets_disjoint": disjoint_offsets,
        "matches_desktop_expected": ok,
        "interpretation": ("distinct SSA/provenance sources can resolve to the same address; "
                           "this is not evidence that real P equals container - it shows the "
                           "examined window cannot decide CONTAINER_VS_P_ALIAS_RELATION"),
    }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
