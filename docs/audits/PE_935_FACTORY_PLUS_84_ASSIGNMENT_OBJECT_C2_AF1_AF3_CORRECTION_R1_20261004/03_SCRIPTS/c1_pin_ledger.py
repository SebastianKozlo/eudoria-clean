# c1_pin_ledger.py
# RUN: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004
# F84-C2 re-validation of the AUTHORITATIVE same-VA pin ledger with the
# CORRECTED decoder + CORRECTED boundary machinery (AF2 repair).
#
# The pin table itself is PRESERVED physical evidence from the F84 chain
# (133 records; NOT rediscovered here - the contract forbids re-deriving the
# setter/constructor merely to reproduce established work). What changes in C2:
#   * boundary confirmation is strong-anchor-only (KNOWN_FUNCTION_ENTRY with
#     recorded anchor provenance); C1's CC-padding/RET-delimited confirmations
#     are demoted to HEURISTIC_START_CANDIDATE (never confirming);
#   * a proven decode covering a pin VA mid-instruction is a REFUTED pin
#     (a pin defect - honestly counted as a failure, never silently kept);
#   * call promotion requires an unprefixed 5-byte E8 rel32 at a
#     strong-anchor-confirmed boundary;
#   * per-pin boundary_start / boundary_refuted_by persisted for QC
#     re-derivation (AF1: the QC re-derives every load-bearing field from the
#     pinned EXE and compares against BOTH the JSON and the CSV).
#
# Outputs (default; --out overrides the 01_RAW JSON path, --csv overrides the
# CSV path): 01_RAW/C1_PIN_EVIDENCE.json + CORRECTED_PIN_LEDGER.csv
# READ-ONLY vs the pinned EXE. No Ghidra, no client execution.

import argparse
import csv
import hashlib
import json
import os
import struct
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pebnd  # noqa: E402
import x86dec  # noqa: E402

RUN = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
       r"\PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004")

# ---------------------------------------------------------------------------
# The authoritative pin table (PRESERVED from the F84 chain; re-measured this
# run against the pinned EXE with the corrected machinery).
# kind: "call" (E8 rel32 validation, expect_target), "bytes" (byte pin,
# expect_bytes), "imm8"/"imm32" (expect_bytes + expect_imm), "mem"
# (expect_bytes + expect_ea), "declassified" (published-as-call record that
# must NOT remain classified as CALL; measured honestly).
# corr: (historical_field, historical_value) for F84-C1 corrected pins.
# ---------------------------------------------------------------------------
PINS = [
    # ---- setter chain (FUN_0070C680) ----
    ("setter_entry", 0x0070C680, "bytes", "6A FF", None, None, "chain:setter", None),
    ("setter_this_ESI", 0x0070C6BA, "bytes", "8B F1", None, None, "chain:setter", None),
    ("setter_EDI_zero", 0x0070C6BC, "bytes", "33 FF", None, None, "chain:setter", None),
    ("setter_guard_CMP_plus_84", 0x0070C6BE, "mem", "39 BE 84 00 00 00", ("ESI", None, 1, 0x84), None, "chain:setter", None),
    ("setter_guard_JE", 0x0070C6C4, "bytes", "74 07", None, None, "chain:setter", None),
    ("setter_PUSH_0xA4", 0x0070C6F9, "imm32", "68 A4 00 00 00", None, 0xA4, "chain:setter;P3:0xA4=164", None),
    ("setter_alloc_new_call", 0x0070C6FE, "call", None, None, 0x0095D3C4, "chain:setter(aux:allocator)", None),
    ("setter_alloc_fail_JE", 0x0070C711, "bytes", "74 09", None, None, "chain:setter", None),
    ("setter_MOV_ECX_new", 0x0070C713, "bytes", "8B C8", None, None, "chain:setter", None),
    ("setter_CALL_stream_ctor", 0x0070C715, "call", None, None, 0x00972380, "chain:setter;PRESERVED_CORE", None),
    ("setter_fail_XOR_EAX", 0x0070C71C, "bytes", "33 C0", None, None, "chain:setter", None),
    ("THE_STORE_plus_84", 0x0070C71E, "mem", "89 86 84 00 00 00", ("ESI", None, 1, 0x84), None, "chain:setter;PRESERVED_CORE:ASSIGNMENT_VA", None),
    ("setter_post_store_MOV_ECX", 0x0070C73B, "bytes", "8B C8", None, None, "chain:setter", None),
    ("setter_post_store_CALL", 0x0070C742, "call", None, None, 0x00972DF0, "chain:setter(target-pin-only;body NOT decoded)", None),
    # ---- bulk-attach loop (FUN_00703E80) ----
    ("loop_entry", 0x00703E80, "bytes", "83 EC 08", None, None, "chain:loop", None),
    ("loop_list_end_load", 0x00703E83, "mem", "8B 41 7C", ("ECX", None, 1, 0x7C), None, "chain:loop", None),
    ("loop_list_begin_load", 0x00703E87, "mem", "8B 71 78", ("ECX", None, 1, 0x78), None, "chain:loop", None),
    ("loop_MOV_EDI_elem", 0x00703EA7, "mem", "8B 3E", ("ESI", None, 1, 0), None, "chain:loop", None),
    ("loop_MOV_ECX_elem", 0x00703EB0, "bytes", "8B CF", None, None, "chain:loop", None),
    ("loop_CALL_modecond", 0x00703EA9, "call", None, None, 0x00703CD0, "chain:loop", None),
    ("loop_PUSH_0x40_slotpred", 0x00703EB4, "imm8", "6A 40", None, 0x40, "chain:loop", None),
    ("loop_CALL_slotpred", 0x00703EB6, "call", None, None, 0x0070CC80, "chain:loop", None),
    ("loop_PUSH_0x20", 0x00703EC3, "imm8", "6A 20", None, 0x20, "chain:loop", None),
    ("loop_CALL_flagtest_0x20", 0x00703EC5, "call", None, None, 0x0070BF40, "chain:loop", None),
    ("loop_MOV_ECX_elem_path2", 0x00703EDC, "mem", "8B 0E", ("ESI", None, 1, 0), None, "chain:loop", None),
    ("loop_PUSH_0x2000", 0x00703EDE, "imm32", "68 00 20 00 00", None, 0x2000, "chain:loop", None),
    ("loop_CALL_flagtest_0x2000", 0x00703EE3, "call", None, None, 0x0070BF40, "chain:loop", None),
    ("loop_MOV_ECX_elem_path3", 0x00703EEC, "mem", "8B 0E", ("ESI", None, 1, 0), None, "chain:loop", None),
    ("loop_PUSH_EBX_arg", 0x00703EEE, "bytes", "53", None, None, "chain:loop", None),
    ("loop_PUSH_EBP_arg", 0x00703EEF, "bytes", "55", None, None, "chain:loop", None),
    ("loop_CALL_setter", 0x00703EF0, "call", None, None, 0x0070C680, "chain:loop", None),
    ("loop_stride_ADD_ESI_4", 0x00703EF5, "bytes", "83 C6 04", None, None, "chain:loop", None),
    # ---- driver (FUN_004B0980) ----
    ("driver_entry", 0x004B0980, "bytes", "6A FF", None, None, "chain:driver", None),
    ("driver_call1", 0x004B09AF, "call", None, None, 0x00401360, "chain:driver", None),
    ("driver_call2", 0x004B09B6, "call", None, None, 0x007AD080, "chain:driver", None),
    ("driver_call3", 0x004B09BD, "call", None, None, 0x00417FA0, "chain:driver", None),
    ("driver_PUSH_cache_str", 0x004B09CD, "imm32", "68 3C A8 A7 00", None, 0x00A7A83C, "chain:driver(string 'Cache\\')", None),
    ("driver_call_after_cache_str", 0x004B09E7, "call", None, None, 0x00401E70, "chain:driver", None),
    ("driver_PUSH_parameters_str", 0x004B09F3, "imm32", "68 58 A2 A7 00", None, 0x00A7A258, "chain:driver(string 'Parameters\\')", None),
    ("driver_MOV_EBX_1", 0x004B0A01, "imm32", "BB 01 00 00 00", None, 1, "correction:context(what 0x004B0A02 sits inside)", None),
    ("driver_declassified_0x004B0A02", 0x004B0A02, "declassified", None, None, None, "correction:F84-C1(historical 'driver_call_after_parameters_str' target 0x514B0A07)",
     ("driver_call_after_parameters_str@S3_CHAINS.json", "va=0x004B0A02,target=0x514B0A07")),
    ("driver_local_0x80", 0x004B0A46, "mem", "C7 44 24 1C 80 00 00 00", ("ESP", None, 1, 0x1C), 0x80, "chain:driver(local {0x80})", None),
    ("driver_local_8", 0x004B0A4E, "mem", "C7 44 24 20 08 00 00 00", ("ESP", None, 1, 0x20), 8, "chain:driver(local {8})", None),
    ("driver_real_call_0x004B0A1E", 0x004B0A1E, "call", None, None, 0x00401E70, "correction:F84-C1(the real CALL in the region)",
     ("driver_call_pre_attach@S3_CHAINS.json(superseded)", "va=0x004B0A21,target=0x190F8E25")),
    ("driver_declassified_0x004B0A21", 0x004B0A21, "declassified", None, None, None, "correction:F84-C1(byte inside the rel32 of the CALL @0x004B0A1E)",
     ("driver_call_pre_attach@S3_CHAINS.json", "va=0x004B0A21,target=0x190F8E25")),
    ("driver_CALL_manager_getter", 0x004B0A56, "call", None, None, 0x00415470, "chain:driver", None),
    ("driver_MOV_ECX_manager", 0x004B0A5B, "bytes", "8B C8", None, None, "chain:driver", None),
    ("driver_CALL_bulk_attach", 0x004B0A5D, "call", None, None, 0x00703E80, "chain:driver", None),
    # ---- registration (FUN_00707FB0) ----
    ("register_entry", 0x00707FB0, "bytes", "6A FF", None, None, "chain:registration", None),
    ("register_MOV_EBX_this", 0x00707FD6, "bytes", "8B D9", None, None, "chain:registration", None),
    ("register_CALL_dispatcher", 0x00707FDF, "call", None, None, 0x0073C870, "chain:registration", None),
    ("register_MOV_EDI_factory", 0x00707FE4, "bytes", "8B F8", None, None, "chain:registration", None),
    ("register_EDI_saved_for_append", 0x00708025, "mem", "89 7C 24 30", ("ESP", None, 1, 0x30), None,
     "correction:F84-C1(published 'edi_saved_for_append=0x00708030' was an operand-displacement misread)",
     ("edi_saved_for_append@S3_CHAINS.json", "0x00708030")),
    ("append_MOV_EAX_list_end", 0x00708065, "mem", "8B 43 7C", ("EBX", None, 1, 0x7C), None, "chain:registration", None),
    ("append_CMP_capacity", 0x00708068, "mem", "3B 83 80 00 00 00", ("EBX", None, 1, 0x80), None, "chain:registration", None),
    ("append_LEA_list_begin", 0x0070806E, "mem", "8D 4B 78", ("EBX", None, 1, 0x78), None, "chain:registration", None),
    ("append_store_elem", 0x00708077, "mem", "89 38", ("EAX", None, 1, 0), None, "chain:registration", None),
    ("append_end_plus_4", 0x00708079, "mem", "83 41 04 04", ("ECX", None, 1, 4), 4, "chain:registration", None),
    # ---- manager-mode init + enumeration (FUN_007080C0) ----
    ("modeinit_entry", 0x007080C0, "mem", "8B 44 24 04", ("ESP", None, 1, 4), None, "chain:modeinit", None),
    ("modeinit_MOV_EDI_this", 0x007080C6, "bytes", "8B F9", None, None, "chain:modeinit", None),
    ("modeinit_store_mode", 0x007080CA, "mem", "89 07", ("EDI", None, 1, 0), None, "chain:modeinit", None),
    ("modeinit_first_range_ESI_init", 0x007080D6, "imm32", "BE 20 4E 00 00", None, 0x4E20, "chain:modeinit(measured enumeration evidence)", None),
    ("modeinit_first_range_CALL_register", 0x007080E3, "call", None, None, 0x00707FB0, "chain:modeinit", None),
    ("modeinit_first_range_CMP_bound", 0x007080EB, "imm32", "81 FE 4C 4E 00 00", None, 0x4E4C, "chain:modeinit(measured enumeration evidence)", None),
    ("modeinit_second_range_ESI_init", 0x007080F3, "imm32", "BE C1 5D 00 00", None, 0x5DC1, "chain:modeinit", None),
    ("modeinit_second_range_CALL_register", 0x007080FB, "call", None, None, 0x00707FB0, "chain:modeinit", None),
    ("modeinit_second_range_CMP_bound", 0x00708103, "imm32", "81 FE D2 5D 00 00", None, 0x5DD2, "chain:modeinit", None),
    ("modeinit_caller_PUSH_2", 0x0041751B, "imm8", "6A 02", None, 2, "chain:modeinit(caller)", None),
    ("modeinit_caller_MOV_ECX", 0x00417522, "bytes", "8B C8", None, None, "chain:modeinit(caller)", None),
    ("modeinit_caller_CALL", 0x00417524, "call", None, None, 0x007080C0, "chain:modeinit(caller)", None),
    # ---- factory ctor/init chain ----
    ("base_ctor_entry", 0x0070CF80, "bytes", "6A FF", None, None, "chain:factory_init", None),
    ("base_ctor_EBX_zero", 0x0070CFBC, "bytes", "33 DB", None, None, "chain:factory_init", None),
    ("NULL_INIT_store_plus_84", 0x0070D013, "mem", "89 9E 84 00 00 00", ("ESI", None, 1, 0x84), None,
     "known-store:INITIALIZATION_NULL(physical re-pin)", None),
    ("derived_ctor_entry", 0x0073B820, "bytes", "6A FF", None, None, "chain:factory_init", None),
    ("derived_ctor_PUSH_classid_20006", 0x0073B871, "imm32", "68 26 4E 00 00", None, 0x4E26, "chain:factory_init", None),
    ("derived_ctor_MOV_ECX_this", 0x0073B876, "bytes", "8B CE", None, None, "chain:factory_init", None),
    ("derived_ctor_CALL_base_ctor", 0x0073B87D, "call", None, None, 0x0070CF80, "chain:factory_init", None),
    ("derived_ctor_factory_vtable_store", 0x0073B89B, "mem", "C7 06 C4 70 A8 00", ("ESI", None, 1, 0), 0x00A870C4,
     "chain:factory_init(the FACTORY class vtable 0x00A870C4; prior canon)", None),
    ("lazyinit_CMP_singleton_null", 0x0073E2B1, "mem", "83 3D 0C 59 BA 00 00", (None, None, 1, 0x00BA590C), 0, "chain:lazy_init", None),
    ("lazyinit_PUSH_0x118_factory_size", 0x0073E2CC, "imm32", "68 18 01 00 00", None, 0x118,
     "chain:lazy_init;P3:0x118=280=THE FACTORY size (NOT the assigned object's 0xA4=164)", None),
    ("lazyinit_CALL_ctor", 0x0073E2EB, "call", None, None, 0x0073B820, "chain:lazy_init", None),
    ("lazyinit_store_singleton", 0x0073E302, "mem", "A3 0C 59 BA 00", (None, None, 1, 0x00BA590C), None, "chain:lazy_init", None),
    ("selector_getter_20006_load", 0x0073C8D8, "mem", "A1 0C 59 BA 00", (None, None, 1, 0x00BA590C), None, "chain:dispatcher", None),
    ("selector_getter_RET", 0x0073C8DD, "bytes", "C3", None, None, "chain:dispatcher", None),
    ("dispatcher_entry_MOV_arg1", 0x0073C870, "mem", "8B 4C 24 04", ("ESP", None, 1, 4), None, "chain:dispatcher", None),
    ("dispatcher_entry_XOR_EAX", 0x0073C874, "bytes", "33 C0", None, None, "chain:dispatcher", None),
    ("dispatcher_jmp_table_indirect", 0x0073C8B4, "mem", "FF 24 8D FC C9 73 00", (None, "ECX", 4, 0x0073C9FC), None, "chain:dispatcher", None),
    # ---- manager getter (FUN_00415470) + manager ctor ----
    ("manager_getter_entry", 0x00415470, "bytes", "6A FF", None, None, "chain:manager", None),
    ("manager_getter_PUSH_0x100", 0x0041549A, "imm32", "68 00 01 00 00", None, 0x100, "chain:manager", None),
    ("manager_getter_CALL_ctor", 0x004154B9, "call", None, None, 0x00707E50, "chain:manager", None),
    ("manager_getter_store_global", 0x004154BE, "mem", "A3 E4 12 BA 00", (None, None, 1, 0x00BA12E4), None, "chain:manager", None),
    ("manager_ctor_entry", 0x00707E50, "bytes", "6A FF", None, None, "chain:manager", None),
    ("manager_ctor_list_begin_zero", 0x00707EB0, "mem", "89 5E 78", ("ESI", None, 1, 0x78), None, "chain:manager", None),
    ("manager_ctor_list_end_zero", 0x00707EB3, "mem", "89 5E 7C", ("ESI", None, 1, 0x7C), None, "chain:manager", None),
    ("manager_ctor_cap_zero", 0x00707EB6, "mem", "89 9E 80 00 00 00", ("ESI", None, 1, 0x80), None, "chain:manager", None),
    # ---- consumer (FUN_0070DCF0) ----
    ("consumer_entry", 0x0070DCF0, "bytes", "6A FF", None, None, "chain:consumer", None),
    ("consumer_MOV_ESI_this", 0x0070DD16, "bytes", "8B F1", None, None, "chain:consumer", None),
    ("consumer_XOR_EBX", 0x0070DD18, "bytes", "33 DB", None, None, "chain:consumer", None),
    ("consumer_gate_CMP_plus_84", 0x0070DD1A, "mem", "39 9E 84 00 00 00", ("ESI", None, 1, 0x84), None, "chain:consumer", None),
    ("consumer_gate_JE", 0x0070DD20, "bytes", "0F 84 C5 00 00 00", None, None, "chain:consumer", None),
    ("consumer_load_stream_1", 0x0070DD6A, "mem", "8B 8E 84 00 00 00", ("ESI", None, 1, 0x84), None, "chain:consumer", None),
    ("consumer_CALL_record_reader", 0x0070DD75, "call", None, None, 0x00971AD0, "chain:consumer", None),
    ("consumer_load_stream_2", 0x0070DD7E, "mem", "8B 8E 84 00 00 00", ("ESI", None, 1, 0x84), None, "chain:consumer", None),
    ("consumer_CALL_advance", 0x0070DD84, "call", None, None, 0x00971650, "chain:consumer", None),
    ("consumer_CALL_apply", 0x0070DDBD, "call", None, None, 0x0070DC20, "chain:consumer", None),
    # ---- slot predicate (FUN_0070CC80) ----
    ("slotpred_entry", 0x0070CC80, "bytes", "53", None, None, "chain:slotpred", None),
    ("slotpred_MOV_ESI_this", 0x0070CC83, "bytes", "8B F1", None, None, "chain:slotpred", None),
    ("slotpred_slot_end_load_8C", 0x0070CC89, "mem", "8B 96 8C 00 00 00", ("ESI", None, 1, 0x8C), None, "chain:slotpred", None),
    ("slotpred_slot_begin_load_88", 0x0070CC8F, "mem", "8B BE 88 00 00 00", ("ESI", None, 1, 0x88), None, "chain:slotpred", None),
    ("slotpred_callback_MOV_EAX_imm32", 0x0070CC9B, "imm32", "B8 F0 BE 70 00", None, 0x0070BEF0,
     "correction:F84-C1(historical declared VA 0x0070CC9A but read bytes at 0x0070CC9B)",
     ("slotpred_callback_ptr@s1_identify_and_anchors.py", "va=0x0070CC9A,hex_read_at=0x0070CC9B")),
    ("slotpred_CALL_scan", 0x0070CCA3, "call", None, None, 0x0070C8D0, "chain:slotpred(scan helper)", None),
    # ---- flag test (FUN_0070BF40, literal transcription-level) ----
    ("flagtest_entry_load_ECX_4", 0x0070BF40, "mem", "8B 41 04", ("ECX", None, 1, 4), None, "hygiene:FUN_0070BF40 literal transcription", None),
    # ---- stream ctor (FUN_00972380) ----
    ("stream_ctor_entry", 0x00972380, "bytes", "6A FF", None, None, "chain:stream_ctor", None),
    ("stream_ctor_this_ESI", 0x009723A6, "bytes", "8B F1", None, None, "chain:stream_ctor", None),
    ("stream_ctor_member_18_minus1", 0x009723D3, "mem", "C7 46 18 FF FF FF FF", ("ESI", None, 1, 0x18), 0xFFFFFFFF, "chain:stream_ctor", None),
    ("stream_ctor_LEA_EDI_cursor_3C", 0x00972427, "mem", "8D 7E 3C", ("ESI", None, 1, 0x3C), None, "chain:stream_ctor", None),
    ("stream_ctor_PUSH_1", 0x0097242A, "imm8", "6A 01", None, 1, "chain:stream_ctor", None),
    ("stream_ctor_PUSH_0x80", 0x0097242C, "imm32", "68 80 00 00 00", None, 0x80, "chain:stream_ctor", None),
    ("stream_ctor_cursor_size_store", 0x00972443, "mem", "C7 47 04 80 00 00 00", ("EDI", None, 1, 4), 0x80, "chain:stream_ctor", None),
    ("stream_ctor_buffer_alloc_CALL", 0x0097244A, "call", None, None, 0x0095D3BE,
     "correction:F84-C1(historical pin VA 0x00972449; the new(0x80) allocation CALL)",
     ("cursor_at_3C_buffer_new@s1_identify_and_anchors.py", "va=0x00972449")),
    ("stream_ctor_buffer_store", 0x00972452, "mem", "89 07", ("EDI", None, 1, 0), None, "chain:stream_ctor", None),
    ("stream_ctor_flag_store", 0x00972454, "mem", "C6 47 11 01", ("EDI", None, 1, 0x11), 1, "chain:stream_ctor", None),
    ("stream_ctor_tail_88_flag_1", 0x00972499, "mem", "89 86 88 00 00 00", ("ESI", None, 1, 0x88), None, "chain:stream_ctor", None),
    ("stream_ctor_tail_8C_size_0x80", 0x0097249F, "mem", "C7 86 8C 00 00 00 80 00 00 00", ("ESI", None, 1, 0x8C), 0x80, "chain:stream_ctor", None),
    ("stream_ctor_tail_90", 0x009724A9, "mem", "89 AE 90 00 00 00", ("ESI", None, 1, 0x90), None, "chain:stream_ctor", None),
    ("stream_ctor_tail_94_flag_1", 0x009724AF, "mem", "89 86 94 00 00 00", ("ESI", None, 1, 0x94), None, "chain:stream_ctor", None),
    ("stream_ctor_tail_98_size_0x80", 0x009724B5, "mem", "C7 86 98 00 00 00 80 00 00 00", ("ESI", None, 1, 0x98), 0x80, "chain:stream_ctor", None),
    ("stream_ctor_tail_9C", 0x009724BF, "mem", "89 AE 9C 00 00 00", ("ESI", None, 1, 0x9C), None, "chain:stream_ctor", None),
    ("stream_ctor_return_this", 0x009724C5, "bytes", "8B C6", None, None, "chain:stream_ctor", None),
    ("stream_ctor_RET", 0x009724D9, "bytes", "C3", None, None, "chain:stream_ctor(extent end)", None),
    # ---- reader bridge (FUN_0070BFD0) ----
    ("bridge_read_plus_84", 0x0070BFD0, "mem", "8B 89 84 00 00 00", ("ECX", None, 1, 0x84), None, "chain:bridge(transcription)", None),
    ("bridge_CALL_target", 0x0070BFDF, "call", None, None, 0x009724E0, "chain:bridge(transcription);correction:historical s1 PROSE note said 'CALL 0x009724DF' but the historical S1 MACHINE record and this re-measure both give 0x009724E0 (E8 FC 64 26 00 @0x0070BFDF)", None),
    # ---- LEAD (recorded, NOT used as evidence of anything) ----
    ("lead_templates_region_ctor_callsite", 0x0072FA76, "call", None, None, 0x00972380,
     "LEAD_ONLY(reader-family class coincidence; no bridge claim)", None),
]


def entry_this_regs(text, tva, entry_va, win=0x40):
    """Machine-check MOV reg,ECX (8B xx with mod=3 rm=1) in the entry window.
    Returns the set of register names that receive ECX near the entry."""
    regs = set()
    i = entry_va - tva
    end = i + win
    steps = 0
    while i < end and i < len(text) and steps < 64:
        ins = x86dec.decode(text, i)
        if ins is None:
            break
        if (not ins.prefixes and ins.opcode == 0x8B and ins.mod == 3
                and ins.rm == 1):
            regs.add(x86dec.REGS32[ins.reg])
        i += ins.length
        steps += 1
    return regs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(RUN, "01_RAW", "C1_PIN_EVIDENCE.json"))
    ap.add_argument("--csv", default=os.path.join(RUN, "CORRECTED_PIN_LEDGER.csv"))
    args = ap.parse_args()

    data, ib, secs, text, tva = pebnd.load_text()
    sha = hashlib.sha256(data).hexdigest()
    exe_ok = (sha.upper() == pebnd.PINNED_EXE_SHA256 and len(data) == pebnd.PINNED_EXE_SIZE)
    cache = pebnd._BoundaryCache(text, tva)

    out = {
        "run": "PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004",
        "stage": "C1",
        "exe": {"path": pebnd.EXE_PATH, "size": len(data), "sha256": sha,
                "pinned_match": exe_ok},
        "boundary_policy": ("AF2-CORRECTED: BOUNDARY_CONFIRMED requires a sequential "
                            "fail-closed decode from a STRONG anchor (KNOWN_FUNCTION_ENTRY "
                            "with recorded anchor provenance) landing exactly on the pin "
                            "VA; raw CC-padding/RET-delimited starts are "
                            "HEURISTIC_START_CANDIDATE only - recorded, never confirming, "
                            "never promoting; a proven decode covering the VA "
                            "mid-instruction REFUTES the pin (pin defect, honest failure); "
                            "multi-start is NOT a trusted source; no inference is made "
                            "from failed decodes"),
        "call_validation_policy": ("byte[VA]==0xE8 AND the 5-byte form is unprefixed AND "
                                   "all 5 operand bytes present AND boundary CONFIRMED "
                                   "from a strong anchor -> TARGET=VA+5+signed_rel32"
                                   "(VA+1); otherwise FAIL|FAIL_MID_INSTRUCTION|"
                                   "FAIL_PREFIXED|NOT_VERIFIED and NO target promoted"),
        "anchor_registry": pebnd.anchor_registry(),
        "pins": [],
        "censuses": {},
    }

    rows = []
    n_fail = 0
    for (cid, va, kind, expect_bytes, expect_ea, expect_imm, source, corr) in PINS:
        off = va - tva
        rec = {"claim_id": cid, "instruction_va": "0x%08X" % va, "kind": kind,
               "source": source}
        if corr:
            rec["historical_correction"] = {"field": corr[0], "historical_value": corr[1]}
        ins = x86dec.decode(text, off) if 0 <= off < len(text) else None
        opcode_bytes = text[off:off + (ins.length if ins else 0)].hex(" ").upper() if ins else None
        bstatus, bsrc, bstart, brefuted = pebnd.boundary_confirm(text, tva, va, cache)
        rec["opcode_bytes"] = opcode_bytes
        rec["instruction_length"] = ins.length if ins else None
        rec["boundary_status"] = bstatus
        rec["boundary_source"] = bsrc
        rec["boundary_start"] = ("0x%08X" % bstart) if bstart else None
        rec["boundary_refuted_by"] = ("0x%08X" % brefuted) if brefuted else None
        row = {"claim_id": cid, "instruction_va": "0x%08X" % va,
               "opcode_bytes": opcode_bytes or "",
               "instruction_length": ins.length if ins else "",
               "operand_kind": "none", "operand_offset": "", "operand_width": "",
               "raw_operand": "", "measured_operand": "", "measured_target": "",
               "boundary_source": bsrc or "",
               "boundary_status": bstatus, "boundary_start": ("0x%08X" % bstart) if bstart else "",
               "boundary_refuted_by": ("0x%08X" % brefuted) if brefuted else "",
               "status": "", "source": source}

        if kind == "declassified":
            b = text[off] if 0 <= off < len(text) else None
            rec["measured_byte"] = ("0x%02X" % b) if b is not None else None
            rec["byte_is_E8"] = (b == 0xE8)
            cv = pebnd.validate_direct_call(text, tva, va, cache)
            rec["call_validation"] = cv["call_validation"]
            # FAIL/FAIL_MID_INSTRUCTION here is the DESIRED measured outcome for
            # a declassified record (the published CALL classification cannot
            # stand); it is not a battery failure.
            rec["evidence_window_8bytes"] = text[off:off + 8].hex(" ").upper()
            # same-VA discipline: opcode_bytes = the instruction bytes AT the
            # declared VA, of instruction_length bytes (the 8-byte evidence
            # window lives in the JSON above)
            d_ins = x86dec.decode(text, off)
            row["opcode_bytes"] = text[off:off + (d_ins.length if d_ins else 1)].hex(" ").upper()
            row["instruction_length"] = d_ins.length if d_ins else 1
            row["measured_target"] = "NONE"
            row["status"] = "DECLASSIFIED_NOT_A_CALL"
            out["pins"].append(rec)
            rows.append(row)
            continue

        if kind == "call":
            cv = pebnd.validate_direct_call(text, tva, va, cache)
            rec["byte_is_E8"] = cv["byte_is_E8"]
            rec["prefixed_form"] = cv["prefixed_form"]
            rec["operand_complete"] = cv["operand_complete"]
            rec["call_validation"] = cv["call_validation"]
            row["operand_kind"] = "rel32"
            row["operand_offset"] = 1
            row["operand_width"] = 4
            row["raw_operand"] = text[off + 1:off + 5].hex(" ").upper() if cv["operand_complete"] or (
                cv["call_validation"] == "NOT_VERIFIED" and off + 5 <= len(text)) else ""
            if cv["call_validation"] == "PASS":
                row["measured_target"] = "0x%08X" % cv["target"]
                ok = (cv["target"] == expect_imm)
                row["status"] = "VALIDATED" if ok else "FAIL"
                if corr and ok:
                    row["status"] = "CORRECTED_VALIDATED"
                if not ok:
                    n_fail += 1
            elif cv["call_validation"] == "NOT_VERIFIED":
                # AF2-corrected: no strong anchor reaches this callsite; the
                # target is NOT promoted (the C1 padding-derived confirmation
                # is superseded); the byte/operand evidence is still recorded.
                rec["apparent_target_not_promoted"] = cv["apparent_target_not_promoted"]
                row["measured_target"] = ("NOT_PROMOTED(apparent=%s)"
                                         % cv["apparent_target_not_promoted"]
                                         if cv["apparent_target_not_promoted"]
                                         else "NOT_PROMOTED")
                row["status"] = "NOT_VERIFIED"
            elif cv["call_validation"] == "FAIL_MID_INSTRUCTION":
                # proven interior on a strong-anchor decode path: pin defect
                row["measured_target"] = "NONE"
                row["status"] = "FAIL_MID_INSTRUCTION"
                n_fail += 1
            else:
                row["measured_target"] = "NONE"
                row["status"] = "FAIL"
                n_fail += 1
            out["pins"].append(rec)
            rows.append(row)
            continue

        # byte / imm / mem pins: full-instruction bytes derived from the SAME VA
        bytes_ok = (opcode_bytes == expect_bytes)
        rec["expected_bytes"] = expect_bytes
        rec["bytes_match"] = bytes_ok
        if ins is not None and ins.memop:
            ea = {
                "operand_width": 32 if not ins.has66 else 16,
                "segment": ins.segment,
                "base_register": x86dec.REGS32[ins.ea_base] if ins.ea_base is not None else None,
                "index_register": x86dec.REGS32[ins.ea_index] if ins.ea_index is not None else None,
                "scale": ins.ea_scale,
                "raw_displacement": ("0x%08X" % ins.disp_raw) if ins.disp_width else "NONE",
                "signed_displacement": ins.disp_signed if ins.disp_width else 0,
                "effective_displacement": ins.disp_signed if ins.disp_width else 0,
            }
            if expect_ea is not None:
                # 4-tuple: (base_name|None, index_name|None, scale, signed_disp|addr)
                eb, ei, esc, ed = expect_ea
                got_base = ea["base_register"]
                got_index = ea["index_register"]
                base_ok = (got_base == eb)
                index_ok = (got_index == ei)
                scale_ok = (ins.ea_scale == esc)
                if eb is None and ei is None:
                    disp_ok = (ins.ea_base is None and ins.ea_index is None
                               and ins.disp_raw == ed)
                    ea_ok = disp_ok
                else:
                    disp_ok = (ins.disp_signed == ed)
                    ea_ok = base_ok and index_ok and scale_ok and disp_ok
                rec["ea_match"] = ea_ok
                if not ea_ok:
                    n_fail += 1
            # EA operand offset = start of the displacement bytes
            if ins.disp_width:
                disp_off = ins.length - ins.disp_width - (ins.imm_width or 0)
                row["operand_offset"] = disp_off
                row["operand_width"] = ins.disp_width
                row["raw_operand"] = text[off + disp_off:off + disp_off + ins.disp_width].hex(" ").upper()
                row["operand_kind"] = "mem32" if ins.disp_width == 4 else "mem8"
            else:
                row["operand_kind"] = "mem0"
            # address provenance: register names are NOT proof
            prov = "UNRESOLVED"
            if ins.ea_base is not None:
                base_name = x86dec.REGS32[ins.ea_base]
                if bstatus == "CONFIRMED" and bsrc == "KNOWN_FUNCTION_ENTRY" \
                        and bstart in pebnd.KNOWN_ENTRIES:
                    thisregs = entry_this_regs(text, tva, bstart)
                    if base_name in thisregs:
                        prov = "THIS_OF_KNOWN_FUNCTION:" + pebnd.KNOWN_ENTRIES[bstart]
                elif ins.ea_base is None and ins.ea_index is None:
                    prov = "ABSOLUTE_STATIC_ADDRESS"
            elif ins.ea_base is None and ins.ea_index is None:
                prov = "ABSOLUTE_STATIC_ADDRESS"
            ea["address_provenance_status"] = prov
            rec["effective_address"] = ea
            row["measured_operand"] = ins.ea_text()
            row["measured_operand"] += " | base=%s;index=%s;scale=%d;raw=%s;signed=%d;effective=%d;prov=%s" % (
                ea["base_register"], ea["index_register"], ea["scale"],
                ea["raw_displacement"], ea["signed_displacement"],
                ea["effective_displacement"], prov)
        if ins is not None and ins.imm_width:
            ioff = ins.length - ins.imm_width
            row["operand_kind"] = "imm%d" % (ins.imm_width * 8)
            row["operand_offset"] = ioff
            row["operand_width"] = ins.imm_width
            row["raw_operand"] = text[off + ioff:off + ioff + ins.imm_width].hex(" ").upper()
            row["measured_operand"] = "0x%X (%d)" % (ins.imm_raw, ins.imm_raw)
            if expect_imm is not None:
                imm_ok = (ins.imm_raw == expect_imm)
                rec["imm_match"] = imm_ok
                if not imm_ok:
                    n_fail += 1
        if bytes_ok and bstatus == "CONFIRMED":
            row["status"] = "VALIDATED"
            if corr:
                row["status"] = "CORRECTED_VALIDATED"
        elif bytes_ok and bstatus == "UNRESOLVED":
            row["status"] = "VALIDATED_BYTES_BOUNDARY_UNRESOLVED"
        elif bytes_ok and bstatus == "REFUTED_MID_INSTRUCTION":
            # a pin VA proven interior on a strong-anchor decode path is a pin
            # defect - honest failure, never silently kept
            row["status"] = "FAIL_MID_INSTRUCTION"
            n_fail += 1
        else:
            row["status"] = "FAIL"
            n_fail += 1
        out["pins"].append(rec)
        rows.append(row)

    # ---- censuses: singleton/global dword references in .text ----
    for gva, label in ((0x00BA590C, "factory_singleton_00BA590C"),
                       (0x00BA12E4, "manager_global_00BA12E4")):
        pat = struct.pack("<I", gva)
        sites = []
        k = 0
        while True:
            i = text.find(pat, k)
            if i == -1:
                break
            sites.append("0x%08X" % (tva + i))
            k = i + 1
        out["censuses"][label] = {"count": len(sites), "sites": sites}

    # dispatcher jump-table entry 5 (selector 20006) value
    off5 = (0x0073C9FC + 5 * 4) - tva
    entry5 = struct.unpack_from("<I", text, off5)[0]
    out["censuses"]["dispatcher_entry5_selector_20006"] = {
        "table_va": "0x0073C9FC", "entry5_va": "0x%08X" % (0x0073C9FC + 20),
        "entry5_value": "0x%08X" % entry5}

    # driver string constants (bounded reads)
    def rstring(va):
        o = pebnd.va_to_off(ib, secs, va)
        end = data.find(b"\x00", o)
        return data[o:end].decode("ascii", "replace")
    out["censuses"]["driver_strings"] = {
        "0x00A7A83C": rstring(0x00A7A83C), "0x00A7A258": rstring(0x00A7A258)}

    out["pin_totals"] = {
        "total_pins": len(PINS),
        "fail_count": n_fail,
        "corrected_records": [r["claim_id"] for r in rows
                              if r["status"].startswith("CORRECTED")
                              or r["status"] == "DECLASSIFIED_NOT_A_CALL"],
        "status_tally": {},
    }
    for r in rows:
        out["pin_totals"]["status_tally"][r["status"]] = \
            out["pin_totals"]["status_tally"].get(r["status"], 0) + 1

    with open(args.out, "w", newline="\n") as f:
        json.dump(out, f, indent=1)

    with open(args.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["claim_id", "instruction_va", "opcode_bytes", "instruction_length",
                    "operand_kind", "operand_offset", "operand_width", "raw_operand",
                    "measured_operand", "measured_target", "boundary_source",
                    "boundary_status", "boundary_start", "boundary_refuted_by",
                    "status", "source"])
        for r in rows:
            w.writerow([r["claim_id"], r["instruction_va"], r["opcode_bytes"],
                        r["instruction_length"], r["operand_kind"], r["operand_offset"],
                        r["operand_width"], r["raw_operand"], r["measured_operand"],
                        r["measured_target"], r["boundary_source"], r["boundary_status"],
                        r["boundary_start"], r["boundary_refuted_by"],
                        r["status"], r["source"]])

    print("C1 done. pins=%d fail=%d exe_ok=%s statuses=%s" % (
        len(PINS), n_fail, exe_ok,
        json.dumps(out["pin_totals"]["status_tally"])))


if __name__ == "__main__":
    main()
