# s3_more_windows.py
# RUN: PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004
# Additional raw windows for the new-function decodes (FUN_0072F7A0-family,
# reader loop, constructor bodies, driver region). READ-ONLY.
import sys, os, json, struct
sys.dont_write_bytecode = True
RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004"
sys.path.insert(0, os.path.join(RUN, "03_SCRIPTS"))
from s2_exe_windows import load_pe, va_to_off  # reuse mapper

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

WIN = {
    # registry-class region before FUN_0072F880 (contains FUN_005670A0 call site 0x0072F784)
    "region_0072F700_0072F880": (0x0072F700, 384),
    # validity check FUN_0072FCE0
    "FUN_0072FCE0_full": (0x0072FCE0, 96),
    # reader loop full (FUN_0072FA30 body: read/parse/copy/insert loop)
    "FUN_0072FA30_body_2": (0x0072FA30, 640),
    # FUN_005B5F90 body after the copy (template-copy local use)
    "FUN_005B5F90_body_2": (0x005B6000, 320),
    # FUN_00567170 body after the copy call @0x0056737A
    "FUN_00567170_body_2": (0x0056737A, 384),
    # region containing the FUN_00567170 call site 0x00567C3E (function start search)
    "region_00567BD0_00567C50": (0x00567BD0, 128),
    # FUN_00567C50 head (driver)
    "FUN_00567C50_head": (0x00567C50, 128),
    # driver->builder call site region @0x0056836C
    "FUN_00567C50_call_builder_region": (0x00568340, 96),
    # FUN_00567030 (queue push family) + FUN_00567B40 (capacity push)
    "FUN_00567B40_head": (0x00567B40, 96),
    # FUN_00844020 (attribute-flag reader; established getter)
    "FUN_00844020_head": (0x00844020, 64),
    # FUN_00843DD0 (attribute object resolver)
    "FUN_00843DD0_head": (0x00843DD0, 96),
    # FUN_00703B80 (the 0x4E26 property machinery)
    "FUN_00703B80_head": (0x00703B80, 160),
}

def main():
    d, image_base, secs = load_pe(EXE)
    out = {}
    for k, (va, size) in WIN.items():
        off = va_to_off(image_base, secs, va)
        out[k] = {"va": "0x%08X" % va, "size": size,
                  "bytes": d[off:off+size].hex(" ") if off is not None else None}
    with open(os.path.join(RUN, "01_RAW", "S3_MORE_WINDOWS.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("captured:", len(out))

if __name__ == "__main__":
    main()
