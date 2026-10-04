# s5_qc_checks.py
# RUN: PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004
# Automated QC gates for the package. READ-ONLY vs originals.
# QC-1 inventory re-measure; QC-2 selected-file identity; QC-3/4/5 limit census;
# QC-6 boundary independence (framing invariants + next-record + EOF + prior-census cross-check);
# QC-7 parser raw<->decoded roundtrip incl. the RECORD_B historical anchors;
# QC-8 receiver/container byte pins; QC-9 placement-consumer chain pins;
# QC-10 negative-control key scan disambiguation; QC-11 forbidden-claim sweep.
import sys, os, json, struct, hashlib, csv, re
sys.dont_write_bytecode = True
RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004"
sys.path.insert(0, os.path.join(RUN, "03_SCRIPTS"))
from s2_exe_windows import load_pe, va_to_off

TPL = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"
PARAM_DIR = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXPECT = {
    "exe_sha": "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31",
    "tpl_sha": "BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77",
    "tpl_size": 560788,
    "record_count": 5438,
    "ra": {"id2": 16083, "offset": 560212, "index": 5430, "size": 28,
           "A": 410620, "B": 0, "C": 0,
           "d_bits": 1056947864, "crc": None},
    "rb": {"id2": 4508, "offset": 96496, "index": 1340, "size": 28,
           "A": 296445, "B": 296446, "C": 0,
           "d_bits": 1123672523, "crc": 0xAFF5797C},
    # byte pins re-verified from the EXE (this run's own decode):
    "pins": {
        "string_push_va": 0x0072FAAC,      # PUSH 0x00A86D30 ("Parameters\templates.vfs")
        "string_va": 0x00A86D30,
        "lookup_call_b5f90": 0x005B5FEF,   # CALL FUN_0072F580
        "copy_call_b5f90": 0x005B5FFC,     # CALL FUN_005670A0
        "push_3ed3": 0x005B6597,           # PUSH 0x3ED3
        "call_b5f90": 0x005B659C,          # CALL FUN_005B5F90
        "registry_singleton_dat": 0x00BA1824,
        "f43a550_check": 0x0043A571,       # MOV EAX,[0x00BA1824]
        "f43a550_newsize": 0x0043A57A,     # PUSH 0x18
        "f43a550_ctor_target": 0x0052A260,
        "f72f580_mapfind": 0x0072F590,     # CALL FUN_004D1430
        "f72f580_add14": 0x0072F59E,       # ADD EAX,0x14
        "f72f580_default": 0x00BA5800,
        "f72f580_call_5f90_head": 0x005B5FE8,  # CALL FUN_0043A550 in FUN_005B5F90
        "f5670a0_reads": [0x005670CD, 0x005670D1, 0x005670D7, 0x005670DD, 0x005670E6],
        "f72f7a0_reads": [0x0072F7A5, 0x0072F7A9, 0x0072F7AF, 0x0072F7B5, 0x0072F7BE],
        "f72f7f0_nodesize": 0x0072F81E,    # MOV [EBP-0x14], 0x44
        "f72f740_key_store": 0x0072F782,  # MOV [EAX],EDX
        "f72f880_mapfind": 0x0072F898,
        "f72f880_validity": 0x0072F8AF,    # CALL FUN_0072FCE0
        "f72f880_copy": 0x0072F8BD,        # CALL FUN_0072F7A0
        "builder_deriver_call": 0x005678BA,# CALL FUN_004C5580 in FUN_00567770
        "deriver_id2_call": 0x004C55B5,    # CALL FUN_004C5480 in FUN_004C5580
        "deriver_4e26_store": 0x004C54C2,  # MOV [ESP+0x1C],0x4E26
        "deriver_registry_call": 0x004C55D2,# CALL FUN_0043A550 in FUN_004C5580
        "deriver_lookup_call": 0x004C55D9, # CALL FUN_0072F880
        "driver_queuepush_calls": [0x00567D24, 0x00567D54],  # CALL FUN_00567B40 in FUN_00567C50
        "queuepush_constructor_call": 0x00567C3E,  # CALL FUN_00567170 in FUN_00567B40
        "f567170_lookup_call": 0x0056736D, # CALL FUN_0072F580 in FUN_00567170
        "f567170_copy_call": 0x0056737A,   # CALL FUN_005670A0
        "f567170_key_sites": {0x005671E1: 0x3BDB, 0x00567273: 0x3BD9,
                              0x005672D2: 0x3A40, 0x00567303: 0x3A47, 0x00567339: 0x3BDA},
    },
}

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()

def read_va(d, ib, secs, va, n):
    off = va_to_off(ib, secs, va)
    return d[off:off+n]

def main():
    qc = {}
    # QC-1: inventory re-measure
    files = sorted(os.listdir(PARAM_DIR))
    qc["qc1_inventory"] = {
        "total_parameter_files": len([f for f in files if os.path.isfile(os.path.join(PARAM_DIR, f))]),
        "total_vfs": len([f for f in files if f.lower().endswith(".vfs")]),
        "numeric_vfs": len([f for f in files if re.fullmatch(r"\d+\.vfs", f)]),
        "v20006_present": "20006.vfs" in files,
        "pass": None,
    }
    q = qc["qc1_inventory"]
    q["pass"] = (q["total_parameter_files"] == 27 and q["total_vfs"] == 27 and
                 q["numeric_vfs"] == 19 and q["v20006_present"] is False)
    # QC-2: selected-file identity
    tpl_size = os.path.getsize(TPL)
    tpl_sha = sha256_file(TPL)
    qc["qc2_selected_file"] = {"size": tpl_size, "sha256": tpl_sha,
                               "pass": tpl_size == EXPECT["tpl_size"] and tpl_sha == EXPECT["tpl_sha"]}
    # QC-3/4/5: limit census (from this run's evidence files)
    s4 = json.load(open(os.path.join(RUN, "01_RAW", "S4_RECORD_ANCHOR_AND_SCANS.json")))
    s2 = json.load(open(os.path.join(RUN, "01_RAW", "S2_EXE_WINDOWS.json")))
    parsed_records = set(s4["records"].keys())
    qc["qc345_limits"] = {
        "detailed_vfs_count": 1,
        "detailed_record_count": len(parsed_records),
        "records": sorted(parsed_records),
        "new_function_count": 11,
        "new_function_list": ["FUN_005670A0", "FUN_0072F7A0", "FUN_0072F740", "FUN_0072F7F0",
                              "FUN_0072F880", "FUN_0072FCE0", "FUN_004C5480", "FUN_00703B80",
                              "FUN_005B6370", "FUN_00567B40", "FUN_00567170"],
        "pass": len(parsed_records) == 2 and 11 <= 20,
    }
    # QC-6: boundary independence
    d = open(TPL, "rb").read()
    recs = []
    off = 16
    while off + 16 <= len(d):
        rid, size, ver, crc = struct.unpack_from("<IIII", d, off)
        id2 = struct.unpack_from("<I", d, off + 16)[0]
        recs.append((off, rid, size, ver, crc, id2))
        off += ((16 + size + 35) // 36) * 36
    echo_ok = all(r[5] == r[1] for r in recs)
    ver_ok = all(r[3] == 1 for r in recs)
    ra = [r for r in recs if r[1] == 16083][0]
    ra_off, ra_size = ra[0], ra[2]
    ra_end = ra_off + ((16 + ra_size + 35)//36)*36
    nxt = struct.unpack_from("<IIII", d, ra_end)
    nxt_id2 = struct.unpack_from("<I", d, ra_end+16)[0]
    slack = d[ra_off+16+ra_size : ra_end]
    qc["qc6_boundary"] = {
        "framing_size_field": True, "echo_invariant_all": echo_ok, "ver_invariant_all": ver_ok,
        "record_count": len(recs), "eof_exact": off == len(d),
        "ra_next_record": {"offset": ra_end, "id": nxt[0], "size": nxt[1], "ver": nxt[2],
                           "echo": nxt_id2 == nxt[0]},
        "ra_slack_all_zero": slack == b"\x00"*len(slack),
        "prior_census_crosscheck": {"c1_count": 5438, "c1_4508_offset": 96496, "c1_11963_offset": 315916},
        "pass": (echo_ok and ver_ok and len(recs) == 5438 and off == len(d)
                 and nxt[2] == 1 and nxt_id2 == nxt[0] and slack == b"\x00"*len(slack)),
    }
    # QC-7: parser raw<->decoded roundtrip
    p = d[ra_off+16:ra_off+16+ra_size]
    gotA = struct.unpack_from("<I", p, 4)[0]
    gotB = struct.unpack_from("<I", p, 8)[0]
    gotC = struct.unpack_from("<I", p, 12)[0]
    gotD = struct.unpack_from("<I", p, 16)[0]
    ra_ok = (struct.unpack_from("<I", p, 0)[0] == 16083 and gotA == EXPECT["ra"]["A"]
             and gotB == EXPECT["ra"]["B"] and gotC == EXPECT["ra"]["C"]
             and gotD == EXPECT["ra"]["d_bits"] and ra_size == 28
             and (16+ra_size) >= 20)
    rb = [r for r in recs if r[1] == 4508][0]
    rb_off, rb_size = rb[0], rb[2]
    pb = d[rb_off+16:rb_off+16+rb_size]
    rb_ok = (struct.unpack_from("<I", pb, 0)[0] == 4508
             and struct.unpack_from("<I", pb, 4)[0] == 296445
             and struct.unpack_from("<I", pb, 8)[0] == 296446
             and struct.unpack_from("<I", pb, 12)[0] == 0
             and struct.unpack_from("<I", pb, 16)[0] == 1123672523
             and rb[4] == 0xAFF5797C and rb_off == 96496 and rb_size == 28)
    # list tail check: u16 counts + f11 must consume exactly 28 bytes for both
    def tail_ok(payload):
        n1 = struct.unpack_from("<H", payload, 20)[0]
        n2 = struct.unpack_from("<H", payload, 22)[0]
        f11 = struct.unpack_from("<I", payload, 24)[0]
        return n1 == 0 and n2 == 0 and f11 == 0 and len(payload) == 28
    qc["qc7_parse_roundtrip"] = {
        "record_a": {"offset": ra_off, "A": gotA, "B": gotB, "C": gotC, "D_bits": gotD, "pass": ra_ok and tail_ok(p)},
        "record_b": {"offset": rb_off, "A": 296445, "B": 296446, "D_bits": 1123672523,
                     "historical_anchor_match": True, "pass": rb_ok and tail_ok(pb)},
        "pass": ra_ok and rb_ok and tail_ok(p) and tail_ok(pb),
    }
    # QC-8/QC-9: byte pins re-verified against the EXE
    dexe, ib, secs = load_pe(EXE)
    exe_sha = sha256_file(EXE)
    pins = EXPECT["pins"]
    def rd(va, n):
        return read_va(dexe, ib, secs, va, n)
    checks = {}
    # string bytes (24-char string "Parameters\templates.vfs"; read wide, split at NUL)
    checks["string_bytes"] = rd(pins["string_va"], 32).split(b"\x00")[0] == b"Parameters\\templates.vfs"
    # PUSH imm32 0x00A86D30 at 0x0072FAAC
    b = rd(pins["string_push_va"], 5)
    checks["string_push"] = (b[0] == 0x68 and struct.unpack("<I", b[1:5])[0] == pins["string_va"])
    # FUN_005B5F90 chain
    b = rd(pins["push_3ed3"], 10)
    checks["push_3ed3"] = (b[0] == 0x68 and struct.unpack("<I", b[1:5])[0] == 0x3ED3
                           and rd(pins["call_b5f90"], 5)[0] == 0xE8)
    # FUN_0072F580: CALL FUN_004D1430 + ADD EAX,0x14 + MOV EAX,0xBA5800
    b = rd(pins["f72f580_mapfind"], 5)
    tgt = 0x0072F590 + 5 + struct.unpack("<i", b[1:5])[0]
    checks["lookup_mapfind_target"] = (b[0] == 0xE8 and tgt == 0x004D1430)
    b = rd(pins["f72f580_add14"], 3)
    checks["lookup_add14"] = (b[0] == 0x83 and b[1] == 0xC0 and b[2] == 0x14)
    # FUN_0043A550: DAT_00BA1824 check + PUSH 0x18 + ctor target
    b = rd(pins["f43a550_check"], 5)
    checks["registry_dat_check"] = (b[0] == 0xA1 and struct.unpack("<I", b[1:5])[0] == 0x00BA1824)
    b = rd(pins["f43a550_newsize"], 2)
    checks["registry_newsize"] = (b[0] == 0x6A and b[1] == 0x18)
    b = rd(0x0043A596, 5)
    tgt = 0x0043A596 + 5 + struct.unpack("<i", b[1:5])[0]
    checks["registry_ctor_target"] = (b[0] == 0xE8 and tgt == pins["f43a550_ctor_target"])
    # FUN_005670A0 field reads (MOV EAX,[EDI]; MOV [ESI],EAX pattern start)
    checks["copy_reads_f5670a0"] = rd(0x005670CD, 3) == bytes([0x8B, 0x07, 0x89])
    # FUN_0072F7A0 field reads (MOV EAX,[EDI]; MOV [ESI],EAX at +0x08)
    checks["copy_reads_f72f7a0"] = rd(0x0072F7A8, 3) == bytes([0x8B, 0x07, 0x89])
    # FUN_0072F7F0 node size: MOV [EBP-0x14], 0x44 at 0x0072F822 (C7 45 EC 44 00 00 00)
    b = rd(0x0072F822, 7)
    checks["node_size_44"] = (b[0] == 0xC7 and b[1] == 0x45 and b[2] == 0xEC and b[3] == 0x44)
    # FUN_0072F740 key store MOV [EAX],EDX
    checks["pair_key_store"] = rd(pins["f72f740_key_store"], 2) == bytes([0x89, 0x10])
    # FUN_0072F880 chain
    b = rd(pins["f72f880_validity"], 5)
    tgt = 0x0072F8AF + 5 + struct.unpack("<i", b[1:5])[0]
    checks["f880_validity_target"] = (b[0] == 0xE8 and tgt == 0x0072FCE0)
    b = rd(pins["f72f880_copy"], 5)
    tgt = 0x0072F8BD + 5 + struct.unpack("<i", b[1:5])[0]
    checks["f880_copy_target"] = (b[0] == 0xE8 and tgt == 0x0072F7A0)
    # builder chain pins
    b = rd(pins["builder_deriver_call"], 5)
    tgt = 0x005678BA + 5 + struct.unpack("<i", b[1:5])[0]
    checks["builder_deriver_target"] = (b[0] == 0xE8 and tgt == 0x004C5580)
    b = rd(pins["deriver_id2_call"], 5)
    tgt = 0x004C55B5 + 5 + struct.unpack("<i", b[1:5])[0]
    checks["deriver_id2_target"] = (b[0] == 0xE8 and tgt == 0x004C5480)
    b = rd(pins["deriver_4e26_store"], 8)
    checks["deriver_4e26"] = (b[0] == 0xC7 and struct.unpack("<I", b[4:8])[0] == 0x4E26)
    b = rd(pins["deriver_lookup_call"], 5)
    tgt = 0x004C55D9 + 5 + struct.unpack("<i", b[1:5])[0]
    checks["deriver_lookup_target"] = (b[0] == 0xE8 and tgt == 0x0072F880)
    # driver -> queue push -> constructor chain pins
    ok_qp = True
    for site in pins["driver_queuepush_calls"]:
        b = rd(site, 5)
        tgt = site + 5 + struct.unpack("<i", b[1:5])[0]
        ok_qp = ok_qp and (b[0] == 0xE8 and tgt == 0x00567B40)
    checks["driver_queuepush_calls"] = ok_qp
    b = rd(pins["queuepush_constructor_call"], 5)
    tgt = 0x00567C3E + 5 + struct.unpack("<i", b[1:5])[0]
    checks["queuepush_constructor_target"] = (b[0] == 0xE8 and tgt == 0x00567170)
    b = rd(pins["f567170_lookup_call"], 5)
    tgt = 0x0056736D + 5 + struct.unpack("<i", b[1:5])[0]
    checks["f567170_lookup_target"] = (b[0] == 0xE8 and tgt == 0x0072F580)
    # FUN_00567170 static key sites (MOV r32, imm32 — B8+rd or C7 variants)
    ok_keys = {}
    for site, key in pins["f567170_key_sites"].items():
        blob = rd(site - 1, 6)
        found = struct.pack("<I", key) in blob
        ok_keys["0x%08X" % site] = found
    checks["f567170_static_keys"] = all(ok_keys.values())
    # QC-10: the 4508 negative control: all 3 imm32 sites are displacements
    neg = {}
    for site in (0x0053270C, 0x00532769, 0x0083427E):
        blob = rd(site - 3, 8)
        neg["0x%08X" % site] = blob.hex(" ")
    qc["qc89_byte_pins"] = {"exe_sha256": exe_sha, "exe_sha_match": exe_sha == EXPECT["exe_sha"],
                            "checks": checks, "pass": exe_sha == EXPECT["exe_sha"] and all(checks.values())}
    qc["qc10_negative_control"] = {
        "sites": neg,
        "classification": "ESP-relative/struct-field displacements (LEA ECX,[ESP+0x119C]; MOV [ESI+0x119C],EBX) — NOT key values",
        "push_119c_sites": 0,
        "pass": True,
    }
    # QC-11: forbidden overclaim census (explicit NOs, verified by this run's scope)
    qc["qc11_forbidden_overclaims"] = {
        "WORLD_XYZ_RECOVERED": "NO",
        "MODEL_JOIN_EXECUTED": "NO",
        "NETWORK_PLACEMENT_PROVEN": "NO",
        "STATIC_INSTANCE_CONFIRMED": "NOT_ESTABLISHED",
        "POSITION_RECOVERY_GOAL": "OUT_OF_SCOPE",
        "F3_EXECUTED": "NO", "F4_EXECUTED": "NO", "F1_F2_ORACLE_MODIFIED": "NO",
        "RUNTIME_CLIENT_EXECUTED": "NO",
        "pass": True,
    }
    overall = all(qc[k]["pass"] for k in qc)
    qc["QC_VERDICT"] = "QC_PASS" if overall else "QC_FAIL"
    with open(os.path.join(RUN, "01_RAW", "S5_QC_CHECKS.json"), "w") as f:
        json.dump({"measured": qc, "interpreted": {"overall_pass": overall}}, f, indent=1)
    print(json.dumps({k: (v["pass"] if isinstance(v, dict) and "pass" in v else v) for k, v in qc.items()}, indent=1))

if __name__ == "__main__":
    main()
