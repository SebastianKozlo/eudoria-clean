# -*- coding: utf-8 -*-
# QC F1-KEY part 3: arg2 classification per registration + full dumps of the 4 pairs.
# pe-master-auditor INTERNAL_QC. STATIC-ONLY.
import struct, sys, json
sys.path.insert(0, r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\00_CONTROL\qc_probe")
from qc_core import Bin, save_json

b = Bin(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe")
R = {}
CT_CLASS = 0x0070CF80
calls = b.calls(CT_CLASS, 0xE8)

ES = struct.pack("<I", 0x00A7957B)  # empty-string constant

def classify(site_va):
    w = b.rd(site_va - 48, 48)
    # last 68-imm32 in window = arg1 (per part-1 probe)
    imm = None; imm_at = None
    for i in range(len(w) - 5, -1, -1):
        if w[i] == 0x68:
            imm = struct.unpack_from("<I", w, i + 1)[0]
            imm_at = site_va - 48 + i
            break
    # arg2: find PUSH empty-string (68 ES) or LEA EAX,[ESP+..]; PUSH EAX (50) BEFORE the imm push
    a2 = None; a2_at = None
    if imm_at is not None:
        pre = b.rd(site_va - 48, imm_at - (site_va - 48))
        j = pre.find(b"\x68" + ES)
        if j >= 0:
            a2 = "empty_string_0x00A7957B"; a2_at = site_va - 48 + j
        else:
            # find LEA EAX,[ESP+imm8] (8D 44 24 xx) followed (within 2 bytes) by 50
            for k in range(len(pre) - 4):
                if pre[k] == 0x8D and pre[k + 1] == 0x44 and pre[k + 2] == 0x24:
                    m = pre.find(b"\x50", k + 4, k + 12)
                    if m >= 0:
                        a2 = "ptr_local_ESP+%02X" % pre[k + 3]; a2_at = site_va - 48 + k
                        break
    return dict(imm32=imm, imm_push_at=hex(imm_at) if imm_at else None,
                arg2=a2, arg2_at=hex(a2_at) if a2_at else None)

res = [dict(call_site=hex(c["site_va"]), **classify(c["site_va"])) for c in calls]
R["sites"] = res
imm = [r for r in res if r["imm32"] is not None]
R["summary"] = dict(total=len(res), with_imm32=len(imm),
                    arg2_empty_string=len([r for r in imm if r["arg2"] and r["arg2"].startswith("empty")]),
                    arg2_ptr_local=len([r for r in imm if r["arg2"] and r["arg2"].startswith("ptr_local")]),
                    arg2_unclassified=len([r for r in imm if not r["arg2"]]))

# full dumps of the 4 required pair regions
R["dump_surgeon_0073AB60"] = b.hexd(0x0073ABA8, 0x28)
R["dump_container_0073A0C0"] = b.hexd(0x0073A108, 0x20)
R["dump_realworlditem_0073A940"] = b.hexd(0x0073A988, 0x20)
R["dump_20006_0073B820"] = b.hexd(0x0073B868, 0x20)

p = save_json("QC_F1_REGARGS3.json", R)
print(R["summary"])
for r in res:
    if r["imm32"] in (0x4E43, 0x4E3E, 0x4E42, 0x4E26) or r["imm32"] is None:
        print(r)
print()
print(R["dump_surgeon_0073AB60"])
print()
print(R["dump_container_0073A0C0"])
print()
print(R["dump_realworlditem_0073A940"])
print()
print(R["dump_20006_0073B820"])
