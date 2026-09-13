# -*- coding: utf-8 -*-
# PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 — S4b RTTI COL -> VTABLE resolution (offline)
# Same method as RUN3 S4 (TD -> COL hits -> vtable), targeting the classes NEW to this run:
# ArkParameter* family, ArkPacket* network family, ArkObjectFileStorage, and the
# ArkClientWorldObjectManager/CWOData bind-descriptor neighborhoods (mf pointers in
# static bind data are extracted as raw dwords around the bind type descriptors).

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

# class name string VA (from S1_RTTI_CENSUS of RUN 3)
CLASSES = {
    "ArkParameterContainer": 0x00B8ED14,
    "ArkParameterTransformation": 0x00B8EC08,
    "ArkParameterSetObject": 0x00B8E65C,
    "ArkParameterCommon": 0x00B8D8E0,
    "ArkParameterServerGlobal": 0x00B8EAF0,
    "ArkParameterServerLocal": 0x00B8EDA0,
    "ArkParameterCreature": 0x00B8E8A4,
    "ArkParameterAction": 0x00B8EC90,
    "ArkParameterBlueprint": 0x00B8CFDC,
    "ArkParameterTool": 0x00B8D1CC,
    "ArkParameterMakeup": 0x00B8EFCC,
    "ArkPacket": 0x00B96E50,
    "ArkStaticPacket": 0x00B96E98,
    "ArkPacketDecoder": 0x00B96F70,
    "ArkCommunicator": 0x00B96EB8,
    "ArkChannelAuth": 0x00B96F94,
    "ArkClientPacketExecutor": 0x00B733A8,
    "ArkPacketExecutorInterface": 0x00B7337C,
    "ArkClientObjectManagerImpl": 0x00B73124,
    "ArkObjectService": 0x00B730E0,
    "ArkObjectCommander": 0x00B73100,
}

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

def main():
    data = open(EXE, "rb").read()

    def scan_dword(value, secs=(".rdata", ".data")):
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

    out = {}
    for cls, str_va in CLASSES.items():
        rec = {"class": cls, "name_string_va": "0x%08X" % str_va}
        td = str_va - 8
        rec["type_descriptor_va"] = "0x%08X" % td
        col_hits = scan_dword(td)
        rec["col_pointer_hits"] = ["0x%08X" % h for h in col_hits]
        vts = []
        for p in col_hits:
            col = p - 0x0C
            for q in scan_dword(col):
                vt = q + 4
                vt_file = va_to_file(vt)
                if vt_file is None:
                    continue
                e0 = struct.unpack_from("<I", data, vt_file)[0]
                if 0x00401000 <= e0 < 0x00A75000:
                    vts.append({"col": "0x%08X" % col, "vtable": "0x%08X" % vt})
        rec["vtables"] = vts
        # enumerate vtable entries (up to 40) pointing into .text
        for v in vts:
            entries = []
            vt = int(v["vtable"], 16)
            off = va_to_file(vt)
            for i in range(40):
                e = struct.unpack_from("<I", data, off + i * 4)[0]
                if 0x00401000 <= e < 0x00A75000:
                    entries.append({"slot": i, "va": "0x%08X" % e})
                else:
                    break
            v["entries"] = entries
        out[cls] = rec

    # bind-descriptor neighborhoods: raw dwords around ArkClientWorldObjectManager
    # bind TDs and the CWOData bind TD; also scan for the TD of ArkObjectFileStorage
    bind_window = {}
    for label, va, span in [
        ("bind_mf0_ArkClientWorldObjectManager", 0x00B6F928, 0x60),
        ("bind_mf1_ArkClientWorldObjectManager", 0x00B6F9C8, 0x60),
        ("bind_free_CWOData_ArkClientWorldObjectLogic", 0x00B78CC8, 0x60),
    ]:
        off = va_to_file(va)
        dwords = []
        for i in range(span // 4):
            d = struct.unpack_from("<I", data, off + i * 4)[0]
            dwords.append({"at": "0x%08X" % (va + i * 4), "dword": "0x%08X" % d,
                           "text_ptr": bool(0x00401000 <= d < 0x00A75000)})
        bind_window[label] = dwords

    # ArkObjectFileStorage: find name string
    ofs_hits = []
    pat = b".?AVArkObjectFileStorage@@\x00"
    off = 0
    while True:
        off = data.find(pat, off)
        if off < 0:
            break
        ofs_hits.append("0x%08X" % file_to_va(off))
        off += 1
    out["ArkObjectFileStorage"] = {"name_string_hits": ofs_hits}

    result = {
        "run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
        "stage": "S4b_rtti_vtables_new_classes",
        "classes": out,
        "bind_windows": bind_window,
    }
    with open(os.path.join(OUT, "S4B_RTTI_VTABLES_NEW.json"), "w") as f:
        json.dump(result, f, indent=2)

    for cls, rec in out.items():
        if cls == "ArkObjectFileStorage":
            print("%-40s name_string=%s" % (cls, rec["name_string_hits"]))
            continue
        vts = " ".join(v["vtable"] for v in rec["vtables"])
        print("%-40s TD=%s COLs=%d vt=%d %s" % (cls, rec["type_descriptor_va"],
              len(rec["col_pointer_hits"]), len(rec["vtables"]), vts))

if __name__ == "__main__":
    main()
