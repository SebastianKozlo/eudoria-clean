# -*- coding: utf-8 -*-
# PE_935_STATIC_INSTANCE_TRACE_R1_20260913 — S4 RTTI COL -> VTABLE resolution (offline)
# MSVC RTTI: TypeDescriptor(TD) { vftable*, spare, .?AVName@@ }
#   COL (??_R3) { sig=0, offset, cdOffset, TD* @+0x0C, ClassDescriptor* @+0x10 }
#   vtable[-1] (dword at vtable-4) = COL*
# So: find dwords == TD -> each hit P gives COL = P-0x0C; find dwords == COL
#     -> each hit Q gives vtable = Q+4 (when Q-4 is referenced as code ptr base).
# Target classes: Ni + Ark world/instance/portal/object classes.

import json
import os
import struct

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

IMAGE_BASE = 0x00400000
SECS = [  # (name, va_start, va_end, raw_ptr, raw_size)
    (".text", 0x00401000, 0x00A75000, 4096, 6766592),
    (".rdata", 0x00A75000, 0x00B6C000, 6770688, 1011712),
    (".data", 0x00B6C000, 0x00BA96E4, 7782400, 212992),
]

def va_to_file(va):
    for n, vs, ve, rp, rs in SECS:
        if vs <= va < ve:
            return rp + (va - vs)
    return None

def file_to_va(off):
    for n, vs, ve, rp, rs in SECS:
        if rp <= off < rp + rs:
            return vs + (off - rp)
    return None

# class name string VA (from S1 census)
CLASSES = {
    "NiAVObject": 0x00B90078,
    "NiNode": 0x00B936D0,
    "NiCamera": 0x00B938E8,
    "NiTriShape": 0x00B93E04,
    "NiObjectNET": None,
    "ArkSceneObject": 0x00B9D79C,
    "ArkSceneObjectFactory": 0x00B9D3E0,
    "ArkModelSource": 0x00B9D428,
    "ArkModelInterface": 0x00B9D830,
    "ArkModelResourceInstanceRef": 0x00B8CACC,
    "ArkModelResourceItem": 0x00B8C2D0,
    "ArkModelResourceItemFactory": 0x00B8BEBC,
    "ArkRealWorldItem": 0x00B8E94C,
    "ArkRealWorldProvider": 0x00B8EEAC,
    "ArkInteractiveWorldObject": 0x00B8D2E8,
    "ArkClientInteractiveWorldObjectImpl": 0x00B70F1C,
    "ArkClientDefaultObjectImpl": 0x00B70778,
    "ArkObject": 0x00B8CFC4,
    "ArkObjectClass": 0x00B8D070,
    "ArkPortalCell": 0x00B9743C,
    "ArkPortalCellGraph": 0x00B973BC,
    "ArkPortalPortal": 0x00B97484,
    "ArkPortalResourceItem": 0x00B9745C,
    "ArkPortalResourceItemFactory": 0x00B97368,
    "ArkPortalIdGenerator": 0x00B97414,
    "WorldSubsystem": 0x00B717A0,
    "ArkClientDynamicObject": 0x00B7F564,
    "ArkRefObject": 0x00B8CAB0,
    "ArkVegetationClimate": 0x00B970DC,
    "ArkVegetationClimateFactory": 0x00B970AC,
    "ArkTerrainEditZoneFactory": 0x00B9D1F4,
    "ArkTerrainEditZoneGroup": 0x00B9D51C,
    "ArkTerrainPatchFactory": 0x00B9D128,
    "ArkHeightFieldSource": 0x00B9D688,
    "ArkClientObjectManagerImpl": 0x00B73124,
    "ArkObjectService": 0x00B730E0,
    "ArkObjectCommander": 0x00B73100,
    "ArkEffectSequenceFactory": 0x00B73A98,
    "ArkVegetationModelClient": 0x00B9D808,
    "ArkVegetationSceneObjectSimple": 0x00B9D7BC,
    "ArkHeightFieldInterface": 0x00B79A78,
}

def main():
    data = open(EXE, "rb").read()

    def scan_dword(value, start_sec=(".rdata", ".data")):
        hits = []
        pat = struct.pack("<I", value)
        for n, vs, ve, rp, rs in SECS:
            if n not in start_sec:
                continue
            off = rp
            while True:
                off = data.find(pat, off, rp + rs)
                if off < 0:
                    break
                hits.append(file_to_va(off))
                off += 1
        return hits

    out = {}
    for cls, str_va in CLASSES.items():
        rec = {"class": cls, "name_string_va": ("0x%08X" % str_va) if str_va else None}
        if str_va is None:
            # find NiObjectNET name
            str_va = None
            pat = b".?AVNiObjectNET@@\x00"
            off = data.find(pat)
            if off >= 0:
                str_va = file_to_va(off)
                rec["name_string_va"] = "0x%08X" % str_va
            else:
                out[cls] = rec
                continue
        td = str_va - 8  # TypeDescriptor object VA
        rec["type_descriptor_va"] = "0x%08X" % td
        col_hits = scan_dword(td)
        rec["col_pointer_hits"] = ["0x%08X" % h for h in col_hits]
        vts = []
        for p in col_hits:
            col = p - 0x0C
            for q in scan_dword(col):
                vt = q + 4
                # validate: entry0 at vt should point into .text
                vt_file = va_to_file(vt)
                if vt_file is None:
                    continue
                e0 = struct.unpack_from("<I", data, vt_file)[0]
                if 0x00401000 <= e0 < 0x00A75000:
                    vts.append({"col": "0x%08X" % col, "vtable": "0x%08X" % vt})
        rec["vtables"] = vts
        out[cls] = rec

    with open(os.path.join(OUT, "S4_RTTI_VTABLES.json"), "w") as f:
        json.dump({"run_id": "PE_935_STATIC_INSTANCE_TRACE_R1_20260913",
                   "stage": "S4_rtti_vtables", "classes": out}, f, indent=2)

    for cls, rec in out.items():
        print("%-36s TD=%s COLs=%d vtables=%d %s" % (
            cls, rec.get("type_descriptor_va"), len(rec.get("col_pointer_hits", [])),
            len(rec.get("vtables", [])),
            " ".join(v["vtable"] for v in rec.get("vtables", []))))

if __name__ == "__main__":
    main()
