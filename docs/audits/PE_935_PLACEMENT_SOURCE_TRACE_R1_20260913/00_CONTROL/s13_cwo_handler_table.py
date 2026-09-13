# -*- coding: utf-8 -*-
# PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 — S13 CWO handler table dump (offline)
# FUN_00514ef0 (transform-set -> placement-record builder driver) is referenced as
# DATA at 0x00A7D778 (.rdata), next to the 'ArkClientWorldObjectLogic::...' assert
# strings (0x00A7D624 from RUN3 census). Dump the region 0x00A7D000-0x00A7E200:
# strings + dword interpretation; build the handler-table map.

import json
import os
import struct

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

SECS = [(".text", 0x00401000, 0x00A75000, 4096, 6766592),
        (".rdata", 0x00A75000, 0x00B6C000, 6770688, 1011712)]

def va_to_file(va):
    for n, vs, ve, rp, rs in SECS:
        if vs <= va < ve:
            return rp + (va - vs)
    return None

def read_cstr(data, off, maxlen=80):
    end = data.find(b"\x00", off, off + maxlen)
    if end < 0:
        return None
    s = data[off:end]
    if len(s) == 0:
        return ""
    try:
        t = s.decode("ascii")
        if all(32 <= ord(c) < 127 for c in t):
            return t
    except:
        pass
    return None

def main():
    data = open(EXE, "rb").read()
    lo, hi = 0x00A7D400, 0x00A7E400
    rows = []
    off = va_to_file(lo)
    i = 0
    while lo + i < hi:
        va = lo + i
        o = va_to_file(va)
        dw = struct.unpack_from("<I", data, o)[0]
        txt = read_cstr(data, o)
        rows.append({"va": "0x%08X" % va, "dword": "0x%08X" % dw,
                     "as_text": txt if txt else None,
                     "dword_in_text": bool(0x00401000 <= dw < 0x00A75000)})
        i += 4

    # handler-table candidates: consecutive runs of text pointers
    runs = []
    cur = []
    for r in rows:
        if r["dword_in_text"]:
            cur.append(r)
        else:
            if len(cur) >= 4:
                runs.append(cur)
            cur = []
    if len(cur) >= 4:
        runs.append(cur)

    result = {
        "run_id": "PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913",
        "stage": "S13_cwo_handler_table",
        "region": ["0x00A7D400", "0x00A7E400"],
        "pointer_runs": [
            {"start": r[0]["va"], "len": len(r),
             "entries": [e["dword"] for e in r]} for r in runs
        ],
        "rows_text": [r for r in rows if r["as_text"]][:60],
    }
    with open(os.path.join(OUT, "S13_CWO_HANDLER_TABLE.json"), "w") as f:
        json.dump(result, f, indent=2)
    for r in result["pointer_runs"]:
        print("run @%s len=%d: %s" % (r["start"], r["len"], " ".join(r["entries"][:12])))
    print()
    for r in result["rows_text"]:
        print("%s %s" % (r["va"], r["as_text"]))

if __name__ == "__main__":
    main()
