#!/usr/bin/env python3
"""05_ANALYSIS: controller attachment census (era PCG_9_3_5).

Q: EDGE_COUNTS shows 126 NiFlipController blocks but only 118
(NiTexturingProperty, NiFlipController) controller edges. Where do the
remaining controllers get referenced from (incoming links census)?
Read-only; frozen R61; same corpus pins as the main driver.
"""
import sys, os, json, struct, hashlib
sys.dont_write_bytecode = True
RUN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RUN_DIR, "05_ANALYSIS", "CONTROLLER_ATTACHMENT_ANALYSIS.json")
MODELS_BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
R61_SOURCE_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\01_source"
sys.path.insert(0, R61_SOURCE_DIR)
from pe_nif_reader import PENifReader  # noqa: E402

REF_FIELDS = ("controller", "next_controller", "target", "extra_data",
              "data_ref", "source_texture_ref")

with open(MODELS_BNT, "rb") as f:
    data = f.read()
fs = len(data)
istart = struct.unpack_from("<I", data, fs - 8)[0]
count = struct.unpack_from("<I", data, istart)[0]
pos = istart + 4
entries = []
for _ in range(count):
    ne = pos
    while data[ne] != 0x0A:
        ne += 1
    name = data[pos:ne].decode("ascii", "replace")
    size, off = struct.unpack_from("<II", data, ne + 1)
    entries.append((name, size, off))
    pos = ne + 17

reader = PENifReader()
flip_total = 0
attached_via_texprop = 0
incoming_census = {}      # (field_name, parent_type) -> count
unattached_examples = []
for name, size, off in entries:
    payload = data[off:off + size]
    try:
        res = reader.parse_bytes(payload, source_name=name)
    except Exception:
        continue
    if res.parse_status != "PASS":
        continue
    blocks = res.blocks
    block_by_idx = {b.block_index: b for b in blocks}
    flips = [b for b in blocks if b.block_type == "NiFlipController"]
    if not flips:
        continue
    flip_total += len(flips)
    attached = set()
    # census every block field that points at a flip controller
    for b in blocks:
        if b.block_type == "NiFlipController":
            continue
        fld = b.fields or {}
        for key, val in fld.items():
            vals = val if isinstance(val, list) else [val]
            for v in vals:
                if isinstance(v, int) and v in {f.block_index for f in flips}:
                    k = (key, b.block_type)
                    incoming_census[k] = incoming_census.get(k, 0) + 1
                    if key == "controller" and b.block_type == "NiTexturingProperty":
                        attached.update(x for x in [v])
    for f in flips:
        if f.block_index in attached:
            attached_via_texprop += 1
        elif len(unattached_examples) < 20:
            unattached_examples.append({
                "nif": name, "flip_block": f.block_index,
                "num_sources": (f.fields or {}).get("num_sources"),
                "texture_slot": (f.fields or {}).get("texture_slot"),
                "target": (f.fields or {}).get("target"),
            })

out = {
    "era": "PCG_9_3_5",
    "flip_controller_blocks_total": flip_total,
    "attached_via_nitexprop_controller": attached_via_texprop,
    "unattached_count": flip_total - attached_via_texprop,
    "incoming_link_census_(field,parent_type)->occurrences": {
        "%s@%s" % k: v for k, v in sorted(incoming_census.items())},
    "unattached_examples_head": unattached_examples,
    "note": ("Controller-edge definition (M3-4.5 V2 ANIM-01): "
             "(NiTexturingProperty, NiFlipController) via fields['controller']. "
             "Incoming-link census shows every reference source for flip "
             "controllers; anything not via NiTexturingProperty.controller is "
             "NOT a controller binding edge under the canon method."),
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "unattached_examples_head"}, indent=1))
print("examples:", json.dumps(unattached_examples[:8]))
