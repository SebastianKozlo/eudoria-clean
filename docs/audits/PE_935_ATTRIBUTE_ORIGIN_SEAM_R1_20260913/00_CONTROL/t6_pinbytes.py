# -*- coding: utf-8 -*-
# PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 - T6: BYTE PINNING of every
# load-bearing claim. Raw bytes at exact VAs (own PE mapping). Sites chosen
# from Ghidra decompile + isCall census (both recorded in 01_RAW).
# STATIC-ONLY.

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_core import PE, hexdump

RUN_ID = "PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

PINS = {
    # GB1 value class
    "GB1_ctor_MOVableObject_head_0085B1B0": (0x0085B1B0, 0x24),
    "GB1_vtable_write_0085B1C3": (0x0085B1C3, 0x10),
    "GB1_variant_store_0085B1CC_894608": (0x0085B1CC, 0x8),
    "GB1_keyfield_deref_call_0085B204": (0x0085B200, 0x14),
    "GB1_dtor_slot0_0085B7F0": (0x0085B7F0, 0x18),
    "GB1_vtable_minus4_00A91E48": (0x00A91E48, 8),
    "GB1_COL_00AB33D0": (0x00AB33D0, 16),
    "GB1_TD_00B7997C": (0x00B7997C, 40),
    "GB1_clientvtable_write_00528EA3": (0x00528EA3, 8),
    "GB1_clientvtable_minus4_00A7DCAC": (0x00A7DCAC, 8),
    "GB1_paramsetid_lea_0085AD50": (0x0085AD50, 8),
    "GB1_provider_00746570_head": (0x00746570, 0x20),
    # GB2 insert seam
    "GB2_insert_head_00856190": (0x00856190, 0x18),
    "GB2_keygetter_call_008561AC": (0x008561AC, 0x12),
    "GB2_pair_prep_008561B5": (0x008561B5, 0x18),
    "GB2_rehash_call_008561C5": (0x008561C5, 6),
    "GB2_findorcreate_call_008561D6": (0x008561D6, 6),
    "GB2_flag_check_008561DB": (0x008561DB, 8),
    "GB2_failpath_delctor_008561E3": (0x008561E3, 0x14),
    "GB2_node_alloc_pair_copy_00854260": (0x00854260, 0x30),
    "GB2_findorcreate_body_00854D90": (0x00854D90, 0x40),
    "GB2_creator_new_004C4792": (0x004C4792, 0x14),
    "GB2_creator_ctor_call_004C47B0": (0x004C47B0, 0x1A),
    "GB2_creator_insert_call_004C47DA": (0x004C47D3, 0x14),
    "GB2_map_ctor_call_008550FE": (0x008550FE, 0x14),
    "GB2_mgrctor_CS_alloc_00855164": (0x00855160, 0x18),
    # GB3 key model
    "GB3_driver_arg1_key_00567C88": (0x00567C88, 0x14),
    "GB3_driver_this_00567CA8": (0x00567CA8, 0xC),
    "GB3_driver_singl_cmp_00567CC4": (0x00567CC4, 0x10),
    "GB3_driver_dsite1_00567D14": (0x00567D14, 0x14),
    "GB3_driver_dsite2_00567D44": (0x00567D44, 0x14),
    "GB3_driver_dsite3_00567F55": (0x00567F55, 0x22),
    "GB3_driver_queuepush1_00567D24": (0x00567D24, 6),
    "GB3_builder_keywalk_call_005677C4": (0x005677C4, 6),
    "GB3_builder_reg_call_00567985": (0x00567985, 6),
    "GB3_builder_selector_call_005679B8": (0x005679B8, 6),
    "GB3_builder_walker_call_005679D1": (0x005679D1, 6),
    "GB3_driveA_sites_00469299": (0x00469299, 6),
    "GB3_driveA_sites_004692AB": (0x004692AB, 6),
    "GB3_driveA_sites_00469419": (0x00469419, 6),
    "GB3_driveA_driver_call_0058E0B7": (0x0058E0B7, 6),
    "GB3_driveB_readcursor_call_005B73B3": (0x005B73B3, 6),
    "GB3_driveB_driver_call_005B7567": (0x005B7567, 6),
    "GB3_driveC_driver_call_00515345": (0x00515345, 6),
    "GB3_driveC_vtable_slot_00A7D778": (0x00A7D778, 8),
    "GB3_driveC_vtable_rtti_00A7D764": (0x00A7D760, 8),
    "GB3_builder_f90_site_00567906": (0x00567906, 6),
    "GB3_builder_fb0_site_00567F36_check": (0x005678DC, 6),
    # GB4 data source
    "GB4_dispatcher_head_004B18D0": (0x004B18D0, 0x18),
    "GB4_dispatch_case0xB9_004B1A16": (0x004B1A16, 6),
    "GB4_dispatch_case0xB0_004B198B": (0x004B198B, 6),
    "GB4_dispatch_case0xC6_004B1AC1": (0x004B1AC1, 6),
    "GB4_dispatch_case0xC7_004B1AD9": (0x004B1AD9, 6),
    "GB4_readcursor_00752700_head": (0x00752700, 0x20),
    "GB4_readcursor_00752640_head": (0x00752640, 0x18),
    "GB4_placement_deser_007453D0_head": (0x007453D0, 0x20),
    "GB4_registry_builder_str_0072FA30": (0x0072FA30, 0x18),
    "GB4_registry_vfsread_call_0072FAF1": (0x0072FAF1, 6),
    "GB4_registry_recordread_call_0072FBA5": (0x0072FBA5, 6),
    "GB4_registryinit_caller_00452497": (0x00452497, 6),
    # positive control (PKG_A record chain)
    "POS_parser_record_store_00730CE6": (0x00730CE6, 8),
    "POS_rblookup_0072F580_head": (0x0072F580, 0x20),
    "POS_bodyset_getter_call_006C3F74": (0x006C3F74, 6),
    "POS_parserA_firstread_00730C90_head": (0x00730C90, 0x18),
}


def main():
    pe = PE(EXE)
    res = {"run_id": RUN_ID, "stage": "T6_byte_pins", "pins": {}, "errors": []}
    for name, (va, ln) in sorted(PINS.items()):
        res["pins"][name] = {"va": "0x%08X" % va, "len": ln,
                             "hexdump": hexdump(pe, va, ln)}
    with open(os.path.join(OUT, "T6_BYTE_PINS.json"), "w") as f:
        json.dump(res, f, indent=2)
    print("T6 done: %d pins" % len(PINS))

if __name__ == "__main__":
    main()
