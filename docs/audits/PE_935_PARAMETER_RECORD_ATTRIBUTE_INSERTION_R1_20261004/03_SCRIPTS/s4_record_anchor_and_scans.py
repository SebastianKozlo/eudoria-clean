# s4_record_anchor_and_scans.py
# RUN: PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004
# Purpose: (1) anchor RECORD_A (templates.vfs record id2=16083) and RECORD_B (id2=4508)
# with full physical identity + raw window hashes; (2) recompute the client parse
# (FUN_00730C90 byte-decoded destinations) from the raw payload bytes; (3) evaluate
# the FUN_0072FCE0 registry-validity predicate for RECORD_A; (4) all-encodings imm32
# scan for the hardcoded keys (0x3ED3/0x3ED2 + FUN_00567170's key set + 0x119C negative);
# (5) the "Parameters\templates.vfs" reader-path string verification.
# READ-ONLY against originals; writes only inside the run package.
import sys, os, json, struct, hashlib
sys.dont_write_bytecode = True
RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004"
sys.path.insert(0, os.path.join(RUN, "03_SCRIPTS"))
from s2_exe_windows import load_pe, va_to_off

TPL = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXPECT_TPL_SHA = "BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77"

def walk(d):
    N = len(d); off = 16; recs = []
    while off + 16 <= N:
        rid, size, ver, crc = struct.unpack_from("<IIII", d, off)
        assert ver == 1 and 4 <= size <= 60000 and off + 16 + size <= N
        id2 = struct.unpack_from("<I", d, off + 16)[0]
        assert id2 == rid
        recs.append((off, rid, size, ver, crc))
        off += ((16 + size + 35) // 36) * 36
    assert off == N
    return recs

def sha(b):
    return hashlib.sha256(b).hexdigest().upper()

def parse_payload(payload):
    # Client parse FUN_00730C90 destinations (this run's own byte decode):
    # u32 payload[0]->obj+0x00 (id2); payload[1]->obj+0x08 (A); payload[2]->obj+0x04 (B);
    # payload[3]->obj+0x0C (C); f32 payload[4]->obj+0x10 (D_f32);
    # list1 (u16 count + count*string) -> obj+0x14; list2 (u16 count + count*u32) -> obj+0x20;
    # u32 f11 -> obj+0x2C.
    obj = {}
    obj["id2"] = struct.unpack_from("<I", payload, 0)[0]
    obj["A"] = struct.unpack_from("<I", payload, 4)[0]
    obj["B"] = struct.unpack_from("<I", payload, 8)[0]
    obj["C"] = struct.unpack_from("<I", payload, 12)[0]
    obj["D_f32_bits"] = struct.unpack_from("<I", payload, 16)[0]
    obj["D_f32"] = struct.unpack_from("<f", payload, 16)[0]
    p = 20
    n1 = struct.unpack_from("<H", payload, p)[0]; p += 2
    list1 = []
    for _ in range(n1):
        slen = struct.unpack_from("<H", payload, p)[0]; p += 2
        s = payload[p:p+slen].decode("ascii", "replace"); p += slen
        list1.append(s)
    n2 = struct.unpack_from("<H", payload, p)[0]; p += 2
    list2 = list(struct.unpack_from("<%dI" % n2, payload, p)) if n2 else []
    p += 4 * n2
    f11 = struct.unpack_from("<I", payload, p)[0]; p += 4
    obj["list1"] = list1; obj["list2"] = list2; obj["f11"] = f11
    obj["consumed"] = p
    return obj

def main():
    d = open(TPL, "rb").read()
    tpl_sha = sha(d)
    assert tpl_sha == EXPECT_TPL_SHA, "templates.vfs identity mismatch!"
    recs = walk(d)
    out = {"templates_vfs": {"size": len(d), "sha256": tpl_sha,
                             "record_count": len(recs),
                             "framing": "header16={id u32,size u32,ver u32,crc u32}; block=ceil((16+size)/36)*36; first record at offset 16; payload id2 echoes header id (independent invariants)"},
           "records": {}}
    for label, want_id in (("RECORD_A", 16083), ("RECORD_B", 4508)):
        hits = [r for r in recs if r[1] == want_id]
        assert len(hits) == 1, (want_id, hits)
        off, rid, size, ver, crc = hits[0]
        payload = d[off+16:off+16+size]
        obj = parse_payload(payload)
        out["records"][label] = {
            "id2": want_id, "hex_id2": "0x%04X" % want_id,
            "index": recs.index(hits[0]), "file_offset": off,
            "header": {"id": rid, "size": size, "ver": ver, "crc32": "0x%08X" % crc},
            "payload_len": size,
            "payload_hex": payload.hex(" "),
            "payload_sha256": sha(payload),
            "record_window_sha256": sha(d[off:off+16+size]),
            "parsed": obj,
            "parse_consumed_equals_size": obj["consumed"] == size,
            "f72fce0_validity": (obj["id2"] != 0) and (obj["A"] != 0 or obj["B"] != 0 or obj["C"] != 0),
            "eof_of_block": off + ((16 + size + 35)//36)*36,
        }
    # independent boundary checks for RECORD_A
    ra = out["records"]["RECORD_A"]
    off, size = ra["file_offset"], ra["payload_len"]
    nxt = off + ((16 + size + 35)//36)*36
    # next record header must exist and parse (unless EOF)
    ok_next = None
    if nxt < len(d):
        nid, nsize, nver, _ = struct.unpack_from("<IIII", d, nxt)
        nid2 = struct.unpack_from("<I", d, nxt+16)[0]
        ok_next = {"offset": nxt, "id": nid, "size": nsize, "ver": nver, "id2_echo": nid2 == nid}
    out["records"]["RECORD_A"]["next_record_check"] = ok_next
    # trailing slack must be all zero (padding invariant)
    slack = d[off+16+size : nxt]
    out["records"]["RECORD_A"]["slack_zero"] = (slack == b"\x00" * len(slack))
    out["records"]["RECORD_A"]["slack_len"] = len(slack)

    # EXE-side: all-encodings imm32 scan for the hardcoded keys + the 4508 negative
    edx, ib, secs = load_pe(EXE)
    def scan_imm32(imm):
        pat = struct.pack("<I", imm)
        sites = []
        for s in secs:
            if s["name"] != ".text":
                continue
            blob = edx[s["rawptr"]:s["rawptr"]+s["rawsize"]]
            start = 0
            while True:
                i = blob.find(pat, start)
                if i < 0:
                    break
                sites.append("0x%08X" % (ib + s["vaddr"] + i))
                start = i + 1
        return sites
    imms = {}
    for imm in (0x3ED3, 0x3ED2, 0x3BD9, 0x3BDA, 0x3BDB, 0x3A47, 0x3A40, 0x119C):
        imms["0x%04X" % imm] = scan_imm32(imm)
    out["imm32_all_encodings_text"] = imms
    # the reader path string
    soff = va_to_off(ib, secs, 0x00A86D30)
    out["reader_path_string"] = {"va": "0x00A86D30",
                                  "bytes": edx[soff:soff+24].hex(" "),
                                  "ascii": edx[soff:soff+24].split(b"\x00")[0].decode("ascii", "replace")}
    with open(os.path.join(RUN, "01_RAW", "S4_RECORD_ANCHOR_AND_SCANS.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({"RECORD_A_offset": ra["file_offset"], "RECORD_A_parsed": out["records"]["RECORD_A"]["parsed"],
                      "validity": ra["f72fce0_validity"], "next_ok": ok_next, "slack_zero": out["records"]["RECORD_A"]["slack_zero"],
                      "imm32": {k: len(v) for k, v in imms.items()},
                      "string": out["reader_path_string"]["ascii"]}, indent=1))

if __name__ == "__main__":
    main()
