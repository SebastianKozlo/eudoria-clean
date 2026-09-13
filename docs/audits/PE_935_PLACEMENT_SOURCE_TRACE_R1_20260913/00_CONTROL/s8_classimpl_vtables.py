# -*- coding: utf-8 -*-
# PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 — S8 ClassImpl vtables + static instances
# Resolve vtables of ArkObjectClassImpl<...>/ArkObjectImpl<...> (the factory classes)
# via the same TD->COL->vtable method, then scan .data/.bss for STATIC instances
# (dword == vtable VA at object offset 0) of:
#   parameter classes, real-world classes, packet classes, manager classes.

import json
import os
import struct

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

SECS = [
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

# name-string VA - 8 = TD (from RUN3 S1 census + this run)
CLASSIMPL = {
    "ArkObjectClassImpl_ArkParameterTransformation": 0x00B8DA28,
    "ArkObjectClassImpl_ArkParameterContainer": 0x00B8DAF0,
    "ArkObjectClassImpl_ArkParameterSetObject": 0x00B8DEB0,
    "ArkObjectClassImpl_ArkParameterServerLocal": 0x00B8DB80,
    "ArkObjectClassImpl_ArkParameterServerGlobal": 0x00B8DB38,
    "ArkObjectClassImpl_ArkRealWorldItem": 0x00B8DD18,
    "ArkObjectClassImpl_ArkRealWorldProvider": 0x00B8DD58,
    "ArkObjectClassImpl_ArkInteractiveWorldObject": 0x00B8DCD0,
    "ArkObjectClassImpl_ArkObject": None,
    "ArkObjectImpl_ArkParameterTransformation": 0x00B8EBA8,
    "ArkObjectImpl_ArkParameterContainer": 0x00B8ECB8,
    "ArkObjectImpl_ArkRealWorldItem": 0x00B8E8D8,
    "ArkObjectImpl_ArkRealWorldProvider": 0x00B8E850,
    "ArkObjectImpl_ArkInteractiveWorldObject": 0x00B8EE50,
    "ArkObjectImpl_ArkParameterSetObject": 0x00B8E600,
}

INSTANCE_VTABLES = {
    "ArkParameterContainer": 0x00A8784C,
    "ArkParameterTransformation": 0x00A877DC,
    "ArkParameterSetObject": 0x00A87260,
    "ArkRealWorldItem": 0x00A873D8,
    "ArkRealWorldProvider": 0x00A878F4,
    "ArkInteractiveWorldObject": 0x00A86C68,
    "ArkPacketDecoder": 0x00A91A6C,
    "ArkStaticPacket": 0x00A91A44,
    "ArkCommunicator": 0x00A91A4C,
    "ArkClientPacketExecutor": 0x00A7C1FC,
    "ArkObjectService": 0x00A7BF9C,
    "ArkObjectCommander": 0x00A7BFCC,
    "ArkClientObjectManagerImpl_v1": 0x00A7C028,
    "ArkClientObjectManagerImpl_v2": 0x00A7C0A0,
    "ArkPortalCell": 0x00A91CF8,
    "ArkPortalCellGraph": 0x00A91CB4,
    "ArkPortalResourceItem": 0x00A91D04,
}

def scan_dword(value, secs):
    hits = []
    pat = struct.pack("<I", value)
    for n, vs, ve, rp, rs in SECS:
        if n not in secs:
            continue
        off = rp
        while True:
            off = data.find(pat, off, rp + rs)
            if off < 0:
                break
            hits.append(file_to_va(off))
            off += 1
    return hits

data = open(EXE, "rb").read()

def main():
    out = {}
    for cls, str_va in CLASSIMPL.items():
        rec = {"class": cls}
        if str_va is None:
            # find ArkObjectClassImpl<ArkObject... not needed; skip
            out[cls] = rec
            continue
        td = str_va - 8
        rec["td"] = "0x%08X" % td
        col_hits = scan_dword(td, (".rdata", ".data"))
        rec["col_hits"] = ["0x%08X" % h for h in col_hits]
        vts = []
        for p in col_hits:
            col = p - 0x0C
            for q in scan_dword(col, (".rdata", ".data")):
                vt = q + 4
                f = va_to_file(vt)
                if f is None:
                    continue
                e0 = struct.unpack_from("<I", data, f)[0]
                if 0x00401000 <= e0 < 0x00A75000:
                    entries = []
                    for i in range(8):
                        e = struct.unpack_from("<I", data, f + i * 4)[0]
                        if 0x00401000 <= e < 0x00A75000:
                            entries.append("0x%08X" % e)
                        else:
                            break
                    vts.append({"vtable": "0x%08X" % vt, "entries": entries})
        rec["vtables"] = vts
        # static instances of the ClassImpl (object in .data with vtable at +0)
        for v in vts:
            vt_int = int(v["vtable"], 16)
            inst = scan_dword(vt_int, (".data",))
            v["static_instances"] = ["0x%08X" % h for h in inst]
        out[cls] = rec

    inst = {}
    for cls, vt in INSTANCE_VTABLES.items():
        hits = scan_dword(vt, (".data",))
        inst[cls] = {"vtable": "0x%08X" % vt,
                     "static_instances_data": ["0x%08X" % h for h in hits]}

    result = {
        "run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
        "stage": "S8_classimpl_vtables_static_instances",
        "classimpl": out,
        "instance_scan": inst,
    }
    with open(os.path.join(OUT, "S8_CLASSIMPL_VTABLES.json"), "w") as f:
        json.dump(result, f, indent=2)
    for cls, rec in out.items():
        if "vtables" in rec:
            print("=== %s" % cls)
            for v in rec["vtables"]:
                print("  vt=%s inst=%s" % (v["vtable"], v.get("static_instances")))
    print()
    for cls, rec in inst.items():
        print("INST %-32s %s" % (cls, rec["static_instances_data"]))

main()
