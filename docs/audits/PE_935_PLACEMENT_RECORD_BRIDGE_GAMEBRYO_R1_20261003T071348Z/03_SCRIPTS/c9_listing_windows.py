# C9 - PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
# Ghidra instruction-listing windows for byte-pinning load-bearing edges.
# Jython 2.7 (Ghidra 11.2.1). Output: 01_RAW/C9_LISTING_WINDOWS.json

import json

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
RESULT_PATH = PKG + r"\01_RAW\C9_LISTING_WINDOWS.json"

WINDOWS = [
    ("L01_emitter_006c3f50", 0x006C3F50, 0x006C3FC0),
    ("L02_lookup_impl_0072f580", 0x0072F580, 0x0072F5B0),
    ("L03_mapfind_004d1430", 0x004D1430, 0x004D1480),
    ("L04_reader_0072fa30_open", 0x0072FAD0, 0x0072FC00),
    ("L05_perrecord_00971ad0", 0x00971AD0, 0x00971B60),
    ("L06_parse_fields_00730c90", 0x00730C90, 0x00730DA0),
    ("L07_ctor_00726e70", 0x00726E70, 0x00726F10),
    ("L08_place_constr_00567170", 0x00567340, 0x00567420),
    ("L09_pos_setter_00730f90", 0x00730F90, 0x00730FD0),
    ("L10_rot_setter_00730fb0", 0x00730FB0, 0x00730FF0),
    ("L11_deserB_004c47f0", 0x004C47F0, 0x004C4A00),
    ("L12_poslerp_00848ea0", 0x00848F60, 0x00848FC0),
    ("L13_attach_thunk_b", 0x0077C0B0, 0x0077C130),
    ("L14_attach_impl_d60", 0x00779D60, 0x00779DA0),
    ("L15_attach_impl_e70", 0x00779E70, 0x00779EC0),
    ("L16_driver_k02_id2", 0x005B6560, 0x005B65E0),
    ("L17_ctor_base_objects_004c5580_strs", 0x004C5A80, 0x004C5B40),
    ("L18_insert_0072f8d0_keycmp", 0x0072F8D0, 0x0072F920),
    ("L19_pump_006c9700", 0x006C9700, 0x006C9790),
    ("L20_instcreator_006cb6f0", 0x006CB780, 0x006CB880),
]

result = {
    "run_id": "PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z",
    "stage": "C9_listing_windows",
    "measured": {"windows": {}},
    "interpreted": {},
    "errors": [],
}

listing = currentProgram.getListing()
for (label, start_va, end_va) in WINDOWS:
    ins = []
    try:
        it = listing.getInstructions(toAddr(start_va), True)
        while it.hasNext():
            i = it.next()
            a = i.getAddress().getOffset()
            if a > end_va:
                break
            ins.append({
                "addr": "0x%08X" % a,
                "bytes": " ".join("%02X" % b for b in i.getBytes()),
                "text": i.toString(),
            })
    except Exception as e:
        result["errors"].append("window %s: %s" % (label, str(e)))
    result["measured"]["windows"][label] = {
        "start": "0x%08X" % start_va, "end": "0x%08X" % end_va, "instructions": ins}

with open(RESULT_PATH, "w") as f:
    json.dump(result, f, indent=2)
print("C9 written:", RESULT_PATH)
for (label, s, e) in WINDOWS:
    w = result["measured"]["windows"].get(label, {})
    print("%s instructions=%s" % (label, len(w.get("instructions", []))))
print("errors:", result["errors"])
