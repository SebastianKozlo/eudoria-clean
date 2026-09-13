# -*- coding: utf-8 -*-
# PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 — S14 VA evidence extraction (offline)
# For every VA cited in the report: raw bytes at the site (VA->file offset via S0 table),
# so the VA_EVIDENCE_REGISTRY carries file->SHA->VA->bytes per the run contract §11.

import hashlib
import json
import os
import struct

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

SECS = [(".text", 0x00401000, 0x00A75000, 4096, 6766592),
        (".rdata", 0x00A75000, 0x00B6C000, 6770688, 1011712),
        (".data", 0x00B6C000, 0x00BA96E4, 7782400, 212992)]

def va_to_file(va):
    for n, vs, ve, rp, rs in SECS:
        if vs <= va < ve:
            return rp + (va - vs), n
    return None, None

# (label, va, n_bytes, note)
EVIDENCE = [
    # Z1: attribute system core
    ("FUN_00845f70_attr_setter", 0x00845F70, 16, "attr setter (walker push via FUN_005275e0)"),
    ("FUN_00413440_lock", 0x00413440, 8, "EnterCriticalSection guard"),
    ("FUN_008544d0_resolver", 0x008544D0, 16, "container-key map lookup -> [hit+8]"),
    ("FUN_0085b840_walker_start", 0x0085B840, 16, "singleton(0x8c)+FUN_008544d0"),
    ("FUN_004154f0_singleton8c", 0x004154F0, 16, "getter of DAT_00ba12e8 manager"),
    ("FUN_008550c0_ctor_0x8c", 0x008550C0, 16, "manager ctor (3 CriticalSections + map)"),
    ("FUN_00843d60_walk_start", 0x00843D60, 12, "walker init: *out=key; FUN_00841920"),
    ("FUN_00846840_attr_pos_fetch", 0x00846840, 16, "position-from-tree (0x6A4/0x6A5/0x6A8/0x6A9)"),
    ("FUN_00854720_attr_triple", 0x00854720, 12, "triple read +0x68/+0x6c/+0x70"),
    ("FUN_008452d0_attr_get_int", 0x008452D0, 12, "int attr getter (0x4E26-family users)"),
    ("FUN_00845360_attr_get_float", 0x00845360, 12, "float attr getter"),
    ("FUN_00844020_attr_check", 0x00844020, 12, "attr existence check"),
    ("FUN_00846430_transform_filter", 0x00846430, 16, "is-transform-attr filter {0x6a8,0x6a9,0x6a4,0x6a5,0x6ac,0x23}"),
    ("FUN_00413590_critsec_init", 0x00413590, 12, "InitializeCriticalSection wrapper"),
    # Z1: writers / dispatchers
    ("FUN_0043f4b0_attr_dispatcher", 0x0043F4B0, 16, "attr-change visual dispatcher (attach model scale 1.0)"),
    ("FUN_005146b0_attr_propagate", 0x005146B0, 16, "attr propagation (0x2720/0x271f/0x3f3 writes)"),
    ("FUN_004387a0_set_6a5", 0x004387A0, 16, "writes attr 0x6a5 + 0x271b/0x271c=0x6ac"),
    ("FUN_00847270_attrtype_dispatch", 0x00847270, 16, "attr-type dispatch {0x6a4/0x6a5->0x619fa; 0x6a8/0x6a9->0x619f9}"),
    ("FUN_008553d0_constructor_walker", 0x008553D0, 16, "builds objects from attribute tree (0x4e34/0x38b0/0x4e38)"),
    # Z1: the builder chain
    ("FUN_00567770_record_builder", 0x00567770, 16, "placement-record builder (setters f60/f90/fb0/fd0)"),
    ("FUN_00567c50_entity_update", 0x00567C50, 16, "3-path driver (0x170d/0x1bdc checks; FUN_00567770 call)"),
    ("FUN_0058db50_update_path", 0x0058DB50, 16, "CWO update path -> FUN_00567c50"),
    ("FUN_005b72c0_msg_b9_handler", 0x005B72C0, 16, "0xB9 message handler -> FUN_00567c50"),
    ("FUN_00514ef0_transform_handler", 0x00514EF0, 16, "transform-set handler (0x2b/0x2c writes) + builder"),
    # Z2: executor + queue
    ("FUN_004b2950_execute", 0x004B2950, 16, "executor Execute (direct or deferred)"),
    ("FUN_004b18d0_msg_dispatch", 0x004B18D0, 16, "message-type dispatcher (case 0xb9)"),
    ("FUN_004b1890_enqueue", 0x004B1890, 12, "deferred ring push {type,x,payload}"),
    ("FUN_004b15f0_executor_ctor", 0x004B15F0, 16, "ArkClientPacketExecutor ctor"),
    ("FUN_00419dd0_commsubsystem_ctor", 0x00419DD0, 16, "CommunicationSubsystem ctor (executor at +0x28)"),
    ("FUN_0040de60_cursor", 0x0040DE60, 12, "cursor advance {+0xC+=n; flag@0x11}"),
    ("FUN_00752700_queue_read_t1", 0x00752700, 16, "entry read {u32,u32,u8,u8}"),
    ("FUN_00752640_queue_read_t2", 0x00752640, 16, "entry read {u32,u32,u8}"),
    ("FUN_0040e0d0_payload_clone", 0x0040E0D0, 12, "payload memcpy clone"),
    # Z2: CWO tables (data refs)
    ("TABLE_00A7D764", 0x00A7D764, 64, "16-entry handler run incl. FUN_00514ef0"),
    ("TABLE_00A7D8EC", 0x00A7D8EC, 64, "74-entry message handler run (head)"),
    ("TABLE_00A7DA34", 0x00A7DA34, 64, "72-entry message handler run (head)"),
    ("STR_00A7D624_CWO_Logic", 0x00A7D624, 64, "'ArkClientWorldObjectLogic::OnDelayedTextureUpdated'"),
    # Z1: network layer
    ("FUN_00833ea0_net_recv", 0x00833EA0, 16, "network receive loop (ntohl, frames)"),
    ("FUN_008310d0_staticpacket", 0x008310D0, 16, "ArkStaticPacket connection-protocol parse"),
    ("FUN_00830030_staticpacket_ctor", 0x00830030, 16, "ArkStaticPacket ctor store"),
    ("FUN_00464370_case_a2", 0x00464370, 16, "case 0xa2 singleton (0x110, ctor FUN_00570480)"),
    # Z1: file channel
    ("FUN_0094dfc0_paramstore_init", 0x0094DFC0, 16, "Data\\Parameters\\ store init (0xa4 store, VFS reader)"),
    ("FUN_0094ba00_path_str", 0x0094BA00, 16, "builds 'Data\\Parameters\\' string"),
    ("FUN_00730c90_vfs_parser", 0x00730C90, 16, "VFS cursor parser (templates.vfs per RUN3)"),
    ("FUN_00972df0_vfs_reader", 0x00972DF0, 16, "VFS file reader (paramstore)"),
    # Z4: D-field
    ("FUN_0048ada0_getter_D", 0x0048ADA0, 8, "getter +0x10 (D) stub"),
    ("FUN_00861240_getter_D_f32", 0x00861240, 8, "fld [ecx+0x10] float D getter"),
    ("FUN_00746550_getter_B", 0x00746550, 8, "getter +0x04 (B) stub"),
    ("FUN_007ce1e0_getter_A", 0x007CE1E0, 8, "getter +0x08 (A) stub"),
    ("FUN_006b22d0_getter_C", 0x006B22D0, 8, "getter +0x0C (C) stub"),
    ("FUN_00567b40_capacity_push", 0x00567B40, 16, "capacity-gated queue push (D arg)"),
    # Z3: portals
    ("FUN_0084b270_portalitem_create", 0x0084B270, 16, "ArkPortalResourceItemFactory slot1 (create+read)"),
    ("FUN_00852a90_portalitem_ctor", 0x00852A90, 16, "item ctor (vtable + CellGraph at +0x10)"),
    ("FUN_00852750_prt_graphreader", 0x00852750, 16, ".prt graph reader (u16, sub, u32 count, cells)"),
    ("FUN_00852a30_prt_tagreader", 0x00852A30, 12, "tag byte reader (vtable slot1 of cell)"),
    ("FUN_0041b870_portalfactory_s0", 0x0041B870, 16, "ArkPortalResourceItemFactory slot0"),
    ("VTABLE_00A91C88_portalfactory", 0x00A91C88, 16, "factory vtable [0041B870, 0084B270, 008E0010]"),
    ("VTABLE_00A91D04_portalitem", 0x00A91D04, 16, "item vtable [00852B80...]"),
    # Z2: vtables
    ("VTABLE_00A7C1FC_executor", 0x00A7C1FC, 8, "[004B1210 dtor, 004B2950 Execute]"),
    ("VTABLE_00A8784C_paramcontainer", 0x00A8784C, 24, "ArkParameterContainer [00761230 create, ...]"),
    ("VTABLE_00A877DC_paramtransf", 0x00A877DC, 24, "ArkParameterTransformation [00760FE0 create, ...]"),
    ("VTABLE_00A86B48_arkobject", 0x00A86B48, 24, "ArkObject base [00764740, 008E0010, 009154A0, 007263E0, 008E0110, 00726340]"),
    ("CLASSIMPL_00A86FBC_paramcontainer", 0x00A86FBC, 8, "ArkObjectClassImpl<Container> [0073C2A0, 0073A160 create]"),
    ("CLASSIMPL_00A8701C_realworlditem", 0x00A8701C, 8, "ArkObjectClassImpl<RealWorldItem> [0073C420, 0073A9E0 create]"),
]

def main():
    data = open(EXE, "rb").read()
    sha = hashlib.sha256(data).hexdigest().upper()
    rows = []
    for label, va, n, note in EVIDENCE:
        off, sec = va_to_file(va)
        if off is None:
            rows.append({"label": label, "va": "0x%08X" % va, "error": "VA outside mapped sections"})
            continue
        raw = data[off:off+n]
        rows.append({
            "label": label,
            "va": "0x%08X" % va,
            "section": sec,
            "file_offset": off,
            "raw_bytes_hex": raw.hex(),
            "note": note,
        })
    result = {
        "run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
        "stage": "S14_va_evidence",
        "exe_sha256": sha,
        "mapping_rule": "file_offset = section.raw_ptr + (VA - section.va_start)",
        "evidence": rows,
    }
    with open(os.path.join(OUT, "S14_VA_EVIDENCE.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("evidence rows:", len(rows))
    missing = [r["label"] for r in rows if "error" in r]
    if missing:
        print("MISSING:", missing)

if __name__ == "__main__":
    main()
